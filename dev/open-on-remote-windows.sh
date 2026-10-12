#!/usr/bin/env bash
set -euo pipefail

# Opens a file in a Windows editor on a remote machine via SSH.
# Uses schtasks /IT to escape Windows SSH session isolation so the editor
# appears on the interactive desktop, and rewrites local paths to a UNC
# share path so the remote editor can reach the file.
#
# Usage: SUPERPOWERS_OPEN_CMD=~/path/to/open-on-remote-windows.sh
#
# Required env vars:
#   REMOTE_SSH         - SSH target, e.g. "user@host"
#   REMOTE_EDITOR      - Windows path to editor exe,
#                        e.g. 'C:\Program Files\Sublime Text\sublime_text.exe'
#   LOCAL_SHARE_ROOT   - Local path prefix to strip, e.g. "/home/alice"
#   REMOTE_UNC_PREFIX  - Path prefix the remote editor sees, e.g. '\\myhost\alice'
#                        or a mapped drive letter such as 'Y:'. A drive letter is
#                        fine because the editor launches in the interactive
#                        session, which has the mapping; the SSH session does not.

: "${REMOTE_SSH:?REMOTE_SSH must be set (e.g. user@host)}"
: "${REMOTE_EDITOR:?REMOTE_EDITOR must be set (Windows path to editor exe)}"
: "${LOCAL_SHARE_ROOT:?LOCAL_SHARE_ROOT must be set (local path prefix)}"
: "${REMOTE_UNC_PREFIX:?REMOTE_UNC_PREFIX must be set (UNC share path)}"

# Resolve to an absolute path first: the LOCAL_SHARE_ROOT prefix strip below
# is a no-op on a relative path, which would silently drop leading path
# components and point the remote editor at a non-existent file (empty buffer).
FILE="$(realpath -s -- "$1")"
REMOTE_USER="${REMOTE_SSH%@*}"

rel="${FILE#"$LOCAL_SHARE_ROOT"/}"
win_rel="${rel//\//\\}"
unc_path="${REMOTE_UNC_PREFIX}\\${win_rel}"

# The remote editor reads $FILE over a UNC/SMB share. Flush local buffers and
# wait until the file is non-empty before launching, so Sublime never opens a
# stale zero-length view right after a fresh write. The trailing settle gives
# the Windows SMB client a beat so it doesn't serve a cached zero-length stat.
# NOTE: this does NOT fix Sublime reusing an already-open empty tab — for a path
# that already has a (stale) tab, use File > Revert.
sync
for _ in $(seq 1 20); do
  [ -s "$FILE" ] && break
  sleep 0.1
done
sleep 0.3

# The remote command runs under whatever shell the Windows SSH server hands out,
# which on this fleet is bash (git-bash), not cmd.exe. So the launcher is written
# as a bash script piped over stdin rather than a cmd.exe "&" chain: under bash,
# ">nul" creates a file literally named nul and "&" backgrounds rather than
# sequences, so a cmd.exe-shaped chain fails while still looking plausible.
# MSYS_NO_PATHCONV stops MSYS rewriting schtasks' /create and /tn into paths.
#
# The editor path and target are base64'd because ssh flattens its command into
# one string that the remote shell re-parses: 'C:\Program Files\...' contains
# spaces and would otherwise be word-split into broken arguments.
#
# schtasks /IT runs the task on the interactive desktop, which is what makes the
# editor visible at all. It is also why REMOTE_UNC_PREFIX may be a mapped drive
# letter: the SSH session cannot see that mapping, but the interactive one can.
editor_b64="$(printf '%s' "${REMOTE_EDITOR}" | base64 -w0)"
target_b64="$(printf '%s' "${unc_path}" | base64 -w0)"

ssh -o BatchMode=yes "${REMOTE_SSH}" bash -s -- \
  "${editor_b64}" "${target_b64}" "${REMOTE_USER}" <<'REMOTE'
set -euo pipefail
editor="$(printf '%s' "$1" | base64 -d)"
target="$(printf '%s' "$2" | base64 -d)"
remote_user="$3"

bat_unix="/c/Users/${remote_user}/open-spec.bat"
bat_win="C:\\Users\\${remote_user}\\open-spec.bat"

printf '@echo off\r\nstart "" "%s" "%s"\r\n' "$editor" "$target" > "$bat_unix"

export MSYS_NO_PATHCONV=1
schtasks /create /tn OpenSpec /tr "$bat_win" /sc once /st 00:00 /f /IT >/dev/null
schtasks /run /tn OpenSpec >/dev/null
REMOTE
