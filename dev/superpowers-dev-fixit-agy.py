#!/usr/bin/env python3
"""
Register this worktree as the superpowers plugin for Antigravity (agy),
replacing the default copy with a directory junction so skill edits are
immediately visible.

AGY stores plugins under ~/.gemini/config/plugins/<name>/. The
`agy plugin install <path>` command copies the source into that location.
To get live-edit behavior, this script:

  1. Runs `agy plugin install <worktree>` to register the plugin.
  2. Replaces the copy at ~/.gemini/config/plugins/superpowers/ with a
     directory junction to the worktree.

Idempotent. Safe to re-run after `agy plugin install` overwrites the
junction with a fresh copy.

WORKTREE_PATH is derived from this script's location: the script assumes
it lives at `<worktree>/dev/superpowers-dev-fixit-agy.py`.
"""

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WORKTREE_PATH = Path(__file__).resolve().parent.parent
GEMINI_PLUGINS = Path.home() / ".gemini" / "config" / "plugins"
PLUGIN_DIR = GEMINI_PLUGINS / "superpowers"


def rmtree_readonly_handler(func, path, exc_info):
    """Handle read-only files (e.g. .git/objects) during rmtree."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def find_agy() -> str | None:
    """Return the agy executable path, or None if not found."""
    result = shutil.which("agy")
    if result:
        return result
    result = shutil.which("agy.exe")
    return result


def is_junction(path: Path) -> bool:
    """Check if path is a Windows directory junction (reparse point)."""
    if not path.exists():
        return False
    try:
        return path.is_symlink() or (
            os.name == "nt"
            and path.is_dir()
            and bool(os.readlink(path))
        )
    except OSError:
        return False


def fix_install() -> bool:
    """Run agy plugin install to register the plugin (first-time only).

    Only runs when the plugin dir doesn't exist at all. If the dir exists
    (as junction or plain copy), fix_junction() handles it. Running
    `agy plugin install` over a junction is destructive -- it tries to
    overwrite files through the junction and can zero them out on failure.
    """
    agy = find_agy()
    if not agy:
        print("ERROR: agy not found in PATH", file=sys.stderr)
        return False

    # Skip if the plugin dir already exists in any form
    if PLUGIN_DIR.exists():
        if is_junction(PLUGIN_DIR):
            resolved = os.readlink(PLUGIN_DIR)
            resolved_normalized = Path(resolved.removeprefix("\\\\?\\"))
            if resolved_normalized == WORKTREE_PATH:
                print("  agy plugin: already a junction to worktree")
            else:
                print(f"  agy plugin: junction exists (-> {resolved}), fix_junction will update")
        else:
            print("  agy plugin: directory exists, fix_junction will replace with junction")
        return False

    result = subprocess.run(
        [agy, "plugin", "install", str(WORKTREE_PATH)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        print(f"  ERROR installing: {stderr or stdout}", file=sys.stderr)
        return False

    print(f"  agy plugin: installed from {WORKTREE_PATH}")
    return True


def fix_junction() -> bool:
    """Replace the plugin copy with a junction to the worktree."""
    if is_junction(PLUGIN_DIR):
        resolved = os.readlink(PLUGIN_DIR)
        resolved_normalized = Path(resolved.removeprefix("\\\\?\\"))
        if resolved_normalized == WORKTREE_PATH:
            print("  junction: already points at worktree")
            return False
        else:
            print(f"  junction: points at {resolved}, updating")
            os.rmdir(PLUGIN_DIR)

    if PLUGIN_DIR.exists() and PLUGIN_DIR.is_dir():
        shutil.rmtree(PLUGIN_DIR, onexc=rmtree_readonly_handler)

    PLUGIN_DIR.parent.mkdir(parents=True, exist_ok=True)

    if os.name == "nt":
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(PLUGIN_DIR), str(WORKTREE_PATH)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  ERROR creating junction: {result.stderr.strip()}", file=sys.stderr)
            return False
    else:
        PLUGIN_DIR.symlink_to(WORKTREE_PATH)

    print(f"  junction: {PLUGIN_DIR} -> {WORKTREE_PATH}")
    return True


def main() -> int:
    if not (WORKTREE_PATH / "gemini-extension.json").is_file():
        print(f"ERROR: no gemini-extension.json under {WORKTREE_PATH}", file=sys.stderr)
        return 1

    if not find_agy():
        print("ERROR: agy CLI not found in PATH -- skipping AGY setup", file=sys.stderr)
        return 1

    print(f"AGY: registering superpowers -> {WORKTREE_PATH}")

    changed_any = False
    changed_any |= fix_install()
    changed_any |= fix_junction()

    if not changed_any:
        print("AGY: already in sync -- nothing to do.")
    else:
        print("AGY: done. Restart AGY for changes to take effect.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
