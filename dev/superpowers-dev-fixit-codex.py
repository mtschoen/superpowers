#!/usr/bin/env python3
"""
Register this worktree as `superpowers@superpowers-dev` in Codex CLI's
plugin system, and remove the published `superpowers@claude-plugins-official`
if present so it stops shadowing.

Codex stores all plugin config in ~/.codex/config.toml and caches plugin
files under ~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/.
Unlike Claude Code (which supports installPath pointing at a live directory),
Codex always copies into the cache. To get live-edit behavior, this script:

  1. Registers a `superpowers-dev` local marketplace pointing at the worktree.
  2. Installs `superpowers@superpowers-dev` via `codex plugin add`.
  3. Replaces the cache copy with a directory junction to the worktree,
     so skill edits are immediately visible without re-installing.
  4. Disables `superpowers@claude-plugins-official` if it was enabled.

The junction means `codex plugin list` may show the plugin as "not installed"
(cosmetic -- the Codex plugin loader reads config.toml's `enabled = true`
and resolves the cache path, which the junction transparently serves).

Idempotent. Safe to re-run after `codex plugin marketplace upgrade` or
any other operation that resets the install routing.

WORKTREE_PATH is derived from this script's location: the script assumes
it lives at `<worktree>/dev/superpowers-dev-fixit-codex.py`.
"""

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WORKTREE_PATH = Path(__file__).resolve().parent.parent
CODEX_HOME = Path.home() / ".codex"
CONFIG_TOML = CODEX_HOME / "config.toml"

MARKETPLACE_KEY = "superpowers-dev"
DEV_KEY = "superpowers@superpowers-dev"
OFFICIAL_KEY = "superpowers@claude-plugins-official"


def rmtree_readonly_handler(func, path, exc_info):
    """Handle read-only files (e.g. .git/objects) during rmtree."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def load_codex_version() -> str:
    plugin_json = WORKTREE_PATH / ".codex-plugin" / "plugin.json"
    return json.loads(plugin_json.read_text())["version"]


def find_codex() -> str | None:
    """Return the codex executable path, or None if not found."""
    result = shutil.which("codex")
    if result:
        return result
    # Windows npm global install puts a .ps1 wrapper; try .cmd too
    result = shutil.which("codex.cmd")
    return result


def run_codex(arguments: list[str]) -> subprocess.CompletedProcess:
    """Run a codex CLI command, returning the CompletedProcess."""
    codex = find_codex()
    if not codex:
        print("ERROR: codex not found in PATH", file=sys.stderr)
        sys.exit(1)
    return subprocess.run(
        [codex] + arguments,
        capture_output=True,
        text=True,
        timeout=30,
    )


def marketplace_registered() -> bool:
    """Check if the superpowers-dev marketplace is already in config.toml."""
    if not CONFIG_TOML.exists():
        return False
    content = CONFIG_TOML.read_text()
    return f"[marketplaces.{MARKETPLACE_KEY}]" in content


def plugin_enabled() -> bool:
    """Check if superpowers@superpowers-dev is enabled in config.toml."""
    if not CONFIG_TOML.exists():
        return False
    content = CONFIG_TOML.read_text()
    return f'[plugins."{DEV_KEY}"]' in content


def official_enabled() -> bool:
    """Check if superpowers@claude-plugins-official is enabled in config.toml."""
    if not CONFIG_TOML.exists():
        return False
    content = CONFIG_TOML.read_text()
    return f'[plugins."{OFFICIAL_KEY}"]' in content


def cache_path(version: str) -> Path:
    return (
        CODEX_HOME
        / "plugins"
        / "cache"
        / MARKETPLACE_KEY
        / "superpowers"
        / version
    )


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


def fix_marketplace() -> bool:
    """Register the local worktree as a superpowers-dev marketplace."""
    if marketplace_registered():
        print(f"  marketplace {MARKETPLACE_KEY}: already registered")
        return False

    result = run_codex(["plugin", "marketplace", "add", str(WORKTREE_PATH)])
    if result.returncode != 0:
        print(f"  ERROR adding marketplace: {result.stderr.strip()}", file=sys.stderr)
        return False

    print(f"  marketplace {MARKETPLACE_KEY}: registered -> {WORKTREE_PATH}")
    return True


def fix_plugin(version: str) -> bool:
    """Install superpowers@superpowers-dev from the local marketplace."""
    changed = False

    # Remove official if present
    if official_enabled():
        result = run_codex(["plugin", "remove", OFFICIAL_KEY])
        if result.returncode == 0:
            print(f"  {OFFICIAL_KEY}: removed (was shadowing dev)")
            changed = True
        else:
            print(f"  WARNING: could not remove {OFFICIAL_KEY}: {result.stderr.strip()}")

    # Skip install if already enabled and junction is correct
    target = cache_path(version)
    if plugin_enabled() and is_junction(target):
        resolved = os.readlink(target)
        resolved_normalized = Path(resolved.removeprefix("\\\\?\\"))
        if resolved_normalized == WORKTREE_PATH:
            print(f"  {DEV_KEY}: already installed with correct junction")
            return changed

    # Install dev plugin (this creates a cache copy that fix_junction replaces)
    result = run_codex(["plugin", "add", DEV_KEY])
    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "already installed" in stderr.lower():
            print(f"  {DEV_KEY}: already installed")
        else:
            print(f"  ERROR installing plugin: {stderr}", file=sys.stderr)
            return changed
    else:
        print(f"  {DEV_KEY}: installed from local marketplace")
        changed = True

    return changed


def fix_junction(version: str) -> bool:
    """Replace the cache copy with a junction to the worktree."""
    target = cache_path(version)

    if is_junction(target):
        resolved = os.readlink(target)
        resolved_normalized = Path(resolved.removeprefix("\\\\?\\"))
        if resolved_normalized == WORKTREE_PATH:
            print(f"  cache junction: already points at worktree")
            return False
        else:
            print(f"  cache junction: points at {resolved}, updating")

    if target.exists():
        if target.is_dir() and not is_junction(target):
            shutil.rmtree(target, onexc=rmtree_readonly_handler)
        elif is_junction(target):
            # Remove old junction
            target.unlink() if target.is_symlink() else os.rmdir(target)

    # Create parent dirs if needed
    target.parent.mkdir(parents=True, exist_ok=True)

    if os.name == "nt":
        # Use cmd mklink /J for junctions (no admin required)
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(target), str(WORKTREE_PATH)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  ERROR creating junction: {result.stderr.strip()}", file=sys.stderr)
            return False
    else:
        # Unix: plain symlink
        target.symlink_to(WORKTREE_PATH)

    print(f"  cache junction: {target} -> {WORKTREE_PATH}")
    return True


def main() -> int:
    if not (WORKTREE_PATH / ".codex-plugin" / "plugin.json").is_file():
        print(f"ERROR: no .codex-plugin/plugin.json under {WORKTREE_PATH}", file=sys.stderr)
        return 1

    if not find_codex():
        print("ERROR: codex CLI not found in PATH -- skipping Codex setup", file=sys.stderr)
        return 1

    version = load_codex_version()
    print(f"Codex: registering {DEV_KEY} -> {WORKTREE_PATH} (version {version})")

    changed_any = False
    changed_any |= fix_marketplace()
    changed_any |= fix_plugin(version)
    changed_any |= fix_junction(version)

    if not changed_any:
        print("Codex: already in sync -- nothing to do.")
    else:
        print("Codex: done. Restart Codex for changes to take effect.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
