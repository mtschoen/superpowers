#!/usr/bin/env python3
"""
SessionStart hook: verify the superpowers plugin is loading from this
worktree (`superpowers@superpowers-dev`) and not the cached published
version.

If out of sync, prints a warning to stdout. SessionStart-hook stdout is
injected into Claude's context (same channel as --append-system-prompt), so
the agent sees this and can surface it to the user.

Always exits 0 — never blocks the session.

WORKTREE_PATH is derived from this script's location: the script assumes
it lives at `<worktree>/dev/superpowers-dev-check.py`. To use a different
worktree as the dev install, run this script from that worktree's `dev/`.
"""

import json
import sys
from pathlib import Path

# Windows: Python defaults stdout to cp1252, which crashes on the warning
# emoji below. Reconfigure once so the SessionStart hook runs cleanly.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WORKTREE_PATH = Path(__file__).resolve().parent.parent
CLAUDE_HOME = Path.home() / ".claude"
KNOWN_MARKETPLACES = CLAUDE_HOME / "plugins" / "known_marketplaces.json"
INSTALLED_PLUGINS = CLAUDE_HOME / "plugins" / "installed_plugins.json"
SETTINGS = CLAUDE_HOME / "settings.json"
FIXIT = f"python3 {WORKTREE_PATH}/dev/superpowers-dev-fixit.py"

MARKETPLACE_KEY = "superpowers-dev"
DEV_KEY = "superpowers@superpowers-dev"
OFFICIAL_KEY = "superpowers@claude-plugins-official"


def find_problems() -> list[str]:
    problems: list[str] = []

    try:
        marketplaces = json.loads(KNOWN_MARKETPLACES.read_text())
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        problems.append(f"could not read {KNOWN_MARKETPLACES}: {exc}")
        marketplaces = {}

    market_entry = marketplaces.get(MARKETPLACE_KEY)
    if not isinstance(market_entry, dict):
        problems.append(
            f"marketplace {MARKETPLACE_KEY!r} not registered in known_marketplaces.json. "
            f"Loader can't resolve {DEV_KEY}, so the plugin silently won't load."
        )
    elif market_entry.get("installLocation") != str(WORKTREE_PATH):
        problems.append(
            f"marketplace {MARKETPLACE_KEY!r} installLocation is "
            f"{market_entry.get('installLocation')!r}, expected {str(WORKTREE_PATH)!r}."
        )

    try:
        installed = json.loads(INSTALLED_PLUGINS.read_text())
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return problems + [f"could not read {INSTALLED_PLUGINS}: {exc}"]

    entries = installed.get("plugins", {}).get(DEV_KEY, [])
    user_entries = [e for e in entries if e.get("scope") == "user"]
    if not user_entries:
        problems.append(
            f"{DEV_KEY} not registered (user scope). Cached/published superpowers is loading instead."
        )
    else:
        path = user_entries[0].get("installPath")
        if path != str(WORKTREE_PATH):
            problems.append(
                f"{DEV_KEY} points at {path!r}, expected {str(WORKTREE_PATH)!r}."
            )

    try:
        enabled = json.loads(SETTINGS.read_text()).get("enabledPlugins", {})
    except (FileNotFoundError, json.JSONDecodeError):
        enabled = {}

    if enabled.get(DEV_KEY) is not True:
        problems.append(f"{DEV_KEY} is not enabled in settings.json.")
    if enabled.get(OFFICIAL_KEY) is True:
        problems.append(
            f"{OFFICIAL_KEY} is still enabled — it will shadow the dev install."
        )

    return problems


def main() -> int:
    problems = find_problems()
    if not problems:
        return 0

    print("⚠️  superpowers-dev plugin is OUT OF SYNC with the local worktree.")
    print()
    print("Detected problems:")
    for p in problems:
        print(f"  - {p}")
    print()
    print(f"Tell the user to run:  {FIXIT}")
    print(f"(Worktree: {WORKTREE_PATH})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
