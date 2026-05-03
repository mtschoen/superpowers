#!/usr/bin/env python3
"""
Register this worktree as `superpowers@superpowers-dev` in Claude Code's
installed plugins, and disable the published `superpowers@claude-plugins-official`
so it stops shadowing.

Workaround for upstream bug: anthropics/claude-code#20593 (plugin installer
matches on plugin name only and ignores the @marketplace qualifier).

Idempotent. Safe to re-run after `/plugin marketplace update` or any other
operation that resets the install routing.

WORKTREE_PATH is derived from this script's location: the script assumes
it lives at `<worktree>/dev/superpowers-dev-fixit.py`. To register a
different worktree as the dev install, run this script from that
worktree's `dev/`.
"""

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKTREE_PATH = Path(__file__).resolve().parent.parent
CLAUDE_HOME = Path.home() / ".claude"
INSTALLED_PLUGINS = CLAUDE_HOME / "plugins" / "installed_plugins.json"
SETTINGS = CLAUDE_HOME / "settings.json"

DEV_KEY = "superpowers@superpowers-dev"
OFFICIAL_KEY = "superpowers@claude-plugins-official"


def backup(path: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = path.with_suffix(path.suffix + f".bak.{stamp}")
    shutil.copy2(path, dest)
    return dest


def load_worktree_version() -> str:
    plugin_json = WORKTREE_PATH / ".claude-plugin" / "plugin.json"
    return json.loads(plugin_json.read_text())["version"]


def fix_installed_plugins(version: str) -> bool:
    data = json.loads(INSTALLED_PLUGINS.read_text())
    plugins = data.setdefault("plugins", {})
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    desired_entry = {
        "scope": "user",
        "installPath": str(WORKTREE_PATH),
        "version": version,
        "installedAt": now,
        "lastUpdated": now,
    }

    existing = plugins.get(DEV_KEY, [])
    user_entries = [e for e in existing if e.get("scope") == "user"]
    other_entries = [e for e in existing if e.get("scope") != "user"]

    if (
        len(user_entries) == 1
        and user_entries[0].get("installPath") == str(WORKTREE_PATH)
        and user_entries[0].get("version") == version
    ):
        return False

    if user_entries:
        desired_entry["installedAt"] = user_entries[0].get("installedAt", now)
    plugins[DEV_KEY] = other_entries + [desired_entry]

    backup_path = backup(INSTALLED_PLUGINS)
    INSTALLED_PLUGINS.write_text(json.dumps(data, indent=2) + "\n")
    print(f"  installed_plugins.json: updated (backup: {backup_path.name})")
    return True


def fix_settings() -> bool:
    data = json.loads(SETTINGS.read_text())
    enabled = data.setdefault("enabledPlugins", {})

    changed = False
    if enabled.get(DEV_KEY) is not True:
        enabled[DEV_KEY] = True
        changed = True
    if enabled.get(OFFICIAL_KEY) is not False:
        enabled[OFFICIAL_KEY] = False
        changed = True

    if changed:
        backup_path = backup(SETTINGS)
        SETTINGS.write_text(json.dumps(data, indent=2) + "\n")
        print(f"  settings.json: updated (backup: {backup_path.name})")
    return changed


def main() -> int:
    if not (WORKTREE_PATH / ".claude-plugin" / "plugin.json").is_file():
        print(f"ERROR: no plugin.json under {WORKTREE_PATH}", file=sys.stderr)
        return 1

    version = load_worktree_version()
    print(f"Registering {DEV_KEY} → {WORKTREE_PATH} (version {version})")

    changed_any = False
    changed_any |= fix_installed_plugins(version)
    changed_any |= fix_settings()

    if not changed_any:
        print("Already in sync — nothing to do.")
    else:
        print("Done. Restart Claude Code for changes to take effect.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
