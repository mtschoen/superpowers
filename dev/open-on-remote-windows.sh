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
#   REMOTE_UNC_PREFIX  - UNC replacement, e.g. '\\myhost\alice'

: "${REMOTE_SSH:?REMOTE_SSH must be set (e.g. user@host)}"
: "${REMOTE_EDITOR:?REMOTE_EDITOR must be set (Windows path to editor exe)}"
: "${LOCAL_SHARE_ROOT:?LOCAL_SHARE_ROOT must be set (local path prefix)}"
: "${REMOTE_UNC_PREFIX:?REMOTE_UNC_PREFIX must be set (UNC share path)}"

FILE="$1"
REMOTE_USER="${REMOTE_SSH%@*}"

rel="${FILE#$LOCAL_SHARE_ROOT/}"
win_rel="${rel//\//\\}"
unc_path="${REMOTE_UNC_PREFIX}\\${win_rel}"

ssh -o BatchMode=yes "${REMOTE_SSH}" \
  "echo \"${REMOTE_EDITOR}\" \"${unc_path}\" > C:\Users\\${REMOTE_USER}\open-spec.bat & schtasks /create /tn OpenSpec /tr C:\Users\\${REMOTE_USER}\open-spec.bat /sc once /st 00:00 /f /IT >nul 2>&1 & schtasks /run /tn OpenSpec >nul 2>&1"
