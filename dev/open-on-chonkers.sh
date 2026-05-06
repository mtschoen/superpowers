#!/usr/bin/env bash
set -euo pipefail

# Opens a llamabox file in Sublime Text on chonkers via the interactive desktop.
# Uses schtasks /IT to escape Windows SSH session isolation.
#
# Usage: SUPERPOWERS_OPEN_CMD=~/superpowers/dev/open-on-chonkers.sh

FILE="$1"
REMOTE_USER="mtsch"
REMOTE_HOST="chonkers"
SUBLIME='C:\Program Files\Sublime Text\sublime_text.exe'
SHARE_ROOT="/home/schoen"
UNC_PREFIX='\\llamabox\schoen'

rel="${FILE#$SHARE_ROOT/}"
win_rel="${rel//\//\\}"
unc_path="${UNC_PREFIX}\\${win_rel}"

ssh -o BatchMode=yes "${REMOTE_USER}@${REMOTE_HOST}" \
  "echo \"${SUBLIME}\" \"${unc_path}\" > C:\Users\\${REMOTE_USER}\open-spec.bat & schtasks /create /tn OpenSpec /tr C:\Users\\${REMOTE_USER}\open-spec.bat /sc once /st 00:00 /f /IT >nul 2>&1 & schtasks /run /tn OpenSpec >nul 2>&1"
