# SDD artifact conventions: open reconciliation (needs a dedicated session)

> **Status: OPEN design debt.** This is a problem capture, not a decision. After
> merging superpowers upstream, our older "prune spec" convention and the new SDD
> artifact system coexist with unresolved contradictions. Updating our global advice
> (skills-dev `CLAUDE.md`, possibly `~/.claude/CLAUDE.md`, and the SDD skill text)
> needs dedicated thinking in a fresh session. Captured 2026-06-21 while building the
> `using-a-debugger` skill, where the contradiction surfaced concretely.

## The two artifact systems we now run in parallel

| | "Prune spec" (our older convention) | SDD (merged upstream) |
|---|---|---|
| **Home** | `docs/superpowers/{specs,plans}/` | `.superpowers/sdd/` (set by `subagent-driven-development/scripts/sdd-workspace`) |
| **Git status** | tracked + committed | **gitignored** - `sdd-workspace` writes a self-ignoring `*` `.gitignore`; our repos also list `.superpowers/` in the top-level `.gitignore` |
| **Lifecycle** | distilled into the plan header on spec to plan handoff, then **manually deleted at branch-finish** | ephemeral scratch, **never committed**, implicitly disposable |
| **Contents** | spec, implementation plan | task briefs, implementer reports, `progress.md` ledger |
| **Doc that defines it** | skills-dev `CLAUDE.md` "Specs and plans"; this repo's `docs/superpowers/` | `subagent-driven-development/SKILL.md` + `scripts/sdd-workspace` |

## The contradictions

1. **The durable audit trail evaporates.** Our advice says "delete the plan at
   branch-finish; `git log` is the audit trail." But the *detailed* record - the SDD
   per-task reports and `progress.md` ledger - is **gitignored**, so it is NOT in
   `git log`. It lives only in the working tree and **vanishes on a fresh clone or a
   submodule re-add.** Concretely: building `using-a-debugger`, converting the skill
   dir to a submodule (`rm -rf` + `git submodule add` re-clone) wiped the
   `.superpowers/sdd/` reports; they had to be manually backed up and restored. After
   branch-finish you are left with terse commit subjects (durable) and nothing else,
   because the rich reports were never committable and the plan that tied them
   together is gone.

2. **Doc gap.** skills-dev `CLAUDE.md` "Specs and plans" documents only the tracked
   `docs/superpowers/` system. It never mentions `.superpowers/sdd/`. A reader
   post-merge will not know the second system exists, where its artifacts live, or
   that they are disposable.

3. **"Preserve vs disposable" sends mixed signals.** SDD artifacts are *designed*
   disposable (self-ignoring). But when they hold the only detailed build record,
   the natural instinct is to preserve them (as happened above). The convention says
   throw away; the value says keep. Pick one.

4. **Worktree-isolation footgun - and subfolder placement does NOT fix it.**
   `subagent-driven-development/SKILL.md` (around line 98) already warns that
   gitignored briefs under `.superpowers/sdd/` are **invisible to worktree-isolated
   implementers**: a worktree checks out only *tracked* files from its commit, so a
   gitignored brief in the parent tree is not materialized. The current worktrees
   advice places worktrees in `.worktrees/` (a gitignored subfolder *inside* the
   parent repo - `using-git-worktrees/SKILL.md`). **This subfolder placement does not
   solve the ignored-SDD problem:** a worktree is still a checkout of a commit, so it
   contains no gitignored parent files regardless of where the worktree directory
   sits on disk. Physical path-traversal up into `../../.superpowers/` is possible but
   breaks the isolation model (and the agent's cwd/context is the worktree root, so it
   will not naturally look there). The SDD skill's own workaround stands: paste the
   brief inline, or write it to a **tracked** path and commit before dispatch.

## Candidate reconciliations (to decide later, not now)

- **(A) Keep both, document the split.** Add a paragraph to skills-dev `CLAUDE.md`
  clarifying: `docs/superpowers/` = tracked/pruned *planning* docs; `.superpowers/sdd/`
  = disposable *execution* scratch; durable rationale MUST be folded into
  `README.md`/`SKILL.md` before branch-finish, because neither artifact survives. Cheap,
  honest, leaves the footgun in place.
- **(B) Make the SDD record durable.** Stop gitignoring the ledger: commit a single
  distilled `progress.md` per build (then prune it with the plan), so the audit trail
  is real and worktree-visible. Costs some noise in history; fixes 1, 3, and 4.
- **(C) Pick one system, retire the other.** Collapse to a single planning+progress
  artifact with one home and one lifecycle. Most work, least confusion long-term.

## Files that currently encode the conflicting advice

- skills-dev `CLAUDE.md` -> "Specs and plans" (prune-spec; silent on `.superpowers/sdd/`)
- `~/superpowers/.gitignore` -> ignores both `.superpowers/` and `.worktrees/`
- `subagent-driven-development/scripts/sdd-workspace` -> writes the self-ignoring `.gitignore`
- `subagent-driven-development/SKILL.md` -> worktree-invisibility warning (~line 98)
- `using-git-worktrees/SKILL.md` -> `.worktrees/` subfolder placement + ignore check
- possibly `~/.claude/CLAUDE.md` global advice, if it references plan/spec lifecycle

## Next step

A fresh session that picks A / B / C, then edits the docs above to match, and adds a
single cross-reference so the two systems stop being discoverable only by accident.
