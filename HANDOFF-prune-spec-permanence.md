# HANDOFF: prune spec/plan permanence from superpowers skills

**Date started:** 2026-04-26
**Last updated:** 2026-05-03
**Status:** branch scaffolding complete; skill amendments not yet drafted

## Why we forked

schoen has a philosophical disagreement with how upstream superpowers
treats specs and plans. Upstream encodes them as durable artifacts
(written to disk, reviewed, handed off, kept around). schoen treats
them as **ephemeral LLM context** — useful while the design is in
flux, pruned as work progresses, deleted when the code and tests are
solid enough to be self-documenting. Code is gospel, not the spec.

The current skill set fights this constantly. Every brainstorm wants to
write `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`; every
plan execution treats the plan file as a contract; spec-compliance
reviewers treat the spec as authoritative when code and spec disagree.

This fork exists to bend those skills toward the schoen workflow.

## Repo state (as of 2026-05-03)

- Worktree at `/home/schoen/superpowers`. Currently checked out on
  `prune-spec-permanence` (the feature branch this doc lives on).
- Remotes (all three configured):
  - `origin` → `git@github.com:obra/superpowers.git`
  - `mtschoen` → `git@github.com:mtschoen/superpowers.git` (schoen's
    github fork)
  - `gitea` → `gitea@llamabox:schoen/superpowers.git` (was a pull
    mirror of obra; converted to regular repo 2026-05-03)
- Branches built and pushed to both `mtschoen` and `gitea`:
  - `schoen/main` — `origin/main` + merges of the two fix branches
    (one merge commit per fix)
  - `dev-probes` — probe markers (`5.0.7+probe1` version bump,
    `PLUGIN_UPDATE_WORKFLOW_MARKER_2026_04_26` injection in
    brainstorming description) + `dev/` directory containing the
    fork's bootstrap scripts (`superpowers-dev-check.py`,
    `superpowers-dev-fixit.py`)
  - `prune-spec-permanence` — single commit holding this handoff doc
- All three feature branches branched off `origin/main`. The plan is
  to merge all four (the two fix branches + dev-probes +
  prune-spec-permanence) into `schoen/main` once the spec-permanence
  amendments are done.

## schoen's existing fork (mtschoen/superpowers) — INVENTORY FINAL 2026-05-03

Cross-checked against the chonkers session (the host where these
commits originated) on 2026-05-03. Confirmed: the two branches below
are the **complete** inventory of pre-existing schoen mods. No
drafted-but-not-pushed amendments, no stash entries, no orphan
branches, no user-level skill overrides that touch superpowers core.

| Branch | Real commit | What it does |
|---|---|---|
| `mtschoen/fix/finishing-branch-cleanup-order` | `3367249` | `fix(finishing-a-development-branch): order branch deletion after worktree removal` |
| `mtschoen/fix/subagent-driven-dev-worktree-isolation` | `c384d09` | `fix(subagent-driven-dev): add worktree isolation pre-dispatch checklist` |

Each branch carries one real commit plus a merge-from-upstream sitting
on top. Their merge-base equals current `origin/main`, so they
consolidate cleanly. Both are already fetched on this host under
`mtschoen/<branch>` — no cross-fetch needed.

`mtschoen/main` itself is just tracking `origin/main` — no mods on it.

### `3367249` — what it actually fixes

Author: Matt Schoen, 2026-04-06. Validated against a real cleanup of
12 stale `worktree-agent-*` branches on Windows 11. Three distinct
bugs in `skills/finishing-a-development-branch/SKILL.md`:

1. **Branch-delete-before-worktree-remove.** `git branch -d/-D` ran
   before `git worktree remove`. Git refuses to delete a branch
   checked out by a worktree (`error: cannot delete branch '<feature>'
   used by worktree at '<path>'`); the skill continued silently and
   left the branch behind.
2. **Stale `.git/worktrees/` registrations.** When a worktree
   directory was deleted out of band (cleanup script, OS reclaim),
   `git worktree remove` errored, the registration lingered, and
   that lingering registration blocked future `git branch -d` of the
   same branch. Fixed with `git worktree prune -v` as fallback +
   defensive final prune.
3. **`grep $(git branch --show-current)` matched the base branch.**
   Step 4 already ran `git checkout <base>` so `--show-current`
   returned `main`/`master`, not the feature branch. Replaced with
   `awk` against column 3 of `git worktree list`, anchored to
   `[<feature-branch>]`.

Plus a Windows-specific operational note: invoke from the parent
repo, not from inside the worktree being cleaned up — Windows holds
a filesystem lock on a process's own cwd.

When re-landing, preserve the per-bug framing in the commit message;
it's load-bearing for understanding why the rewrite is the shape it is.

### `c384d09` — what it actually fixes (and an important caveat)

Author: Matt Schoen, 2026-04-09. Adds a "Pre-Dispatch Checklist
(Worktree Isolation)" section to `skills/subagent-driven-development/SKILL.md`,
narrowly addressing the failure mode where untracked files in the
parent are invisible to the subagent's worktree (because worktrees
check out from a git commit).

**Caveat — never actually loaded.** The chonkers session confirmed
(via diff between skills-on-disk and skills-installed-in-cache) that
this SKILL.md amendment was never synced into the Windows host's
plugin cache. In practice, the user has been protected from worktree
isolation failures by the `## Parallel Worktree Agents` section of
`~/.claude/CLAUDE.md`, which is broader and lists more failure signs
than the SKILL.md amendment.

**When folding c384d09 into `schoen/main`, treat the CLAUDE.md text
as authoritative** and the SKILL.md amendment as a partial
transcription. The merged version should incorporate the full
failure-sign list from CLAUDE.md, not just the untracked-files
subcase.

**STATUS 2026-05-03:** c384d09 has been merged into `schoen/main`
verbatim — the broader CLAUDE.md content has NOT been folded in yet.
This is queued as part of the spec-permanence amendment work
(specifically the `subagent-driven-development` amendment), since the
two will likely overlap in the same SKILL.md section.

### Bridge to the prune-spec-permanence work

`c384d09` already takes a half-step toward "specs/plans as ephemeral
context": its preferred remediation is *"paste the full task text
inline in the prompt rather than referencing a file path."* That's
the same direction the fork amendments are heading — the plan
travels as conversation context, not as a file the subagent must
locate. Worth citing as prior art within the schoen line when
amending `subagent-driven-development` and `writing-plans`.

## Branch model (built 2026-05-03)

`schoen/main` is the primary fork branch — `origin/main` plus
`--no-ff` merges of each contributing branch. All feature branches
(the two fix branches, `dev-probes`, `prune-spec-permanence`) are cut
from `origin/main` and merge into `schoen/main` once their work is
done. This is a fan-in pattern: every feature branches off a known
upstream commit and converges via a visible merge commit, so the
philosophical divergence is recorded in PR history rather than buried
in linear commits to main.

`dev-probes` is intended as a permanent feature of `schoen/main` —
the probe markers and `dev/` bootstrap scripts ship with the fork so
the dev install can be set up on any machine where the fork is
cloned.

The github fork (`mtschoen/superpowers`) is the canonical home for
PRs into `schoen/main`. The gitea repo (`schoen/superpowers` on
`gitea.llamabox.internal`) carries the same branches as a
local-network mirror; default `git pull`/`git push` for these
branches goes to gitea (low-latency), explicit `git push mtschoen
<branch>` to surface work on github.

## License + legal (verified 2026-04-26)

- MIT License, © 2025 Jesse Vincent. Forking, modifying, distributing
  (even publicly, even commercially) is allowed. Only requirement:
  keep `LICENSE` in any redistribution.
- No CLA, no `CONTRIBUTING.md`, no contributor agreement.
- `CODE_OF_CONDUCT.md` only governs upstream-community participation,
  doesn't constrain a fork.
- README has a sponsorship ask — soft, not legally binding.
- **If publishing this fork publicly later:** rename to avoid brand
  collision with the upstream "Superpowers" plugin on Anthropic's
  marketplace. Not a legal requirement, just courteous.

## Audit: where spec/plan permanence is encoded

Five skills need amendment. Other skills (`using-superpowers`,
`writing-skills`, `using-git-worktrees`, etc.) do not take a position
on spec permanence and can be left alone.

| Skill | What it currently encodes | What needs to change |
|---|---|---|
| `brainstorming` | Spec is the deliverable; written to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`, reviewed, handed to writing-plans. No retirement story. | Reframe spec as ephemeral context. Edit in place as understanding evolves. Explicit retirement step at the end of the lifecycle (prune completed sections; delete when code is solid). |
| `writing-plans` | Plan is the durable contract for the engineer/subagent. Saved to `docs/superpowers/plans/YYYY-MM-DD-<feature>.md`. No retirement. | Same framing. Plan is meant to be deleted once executed. |
| `executing-plans` | "Load plan, follow exactly." Plan is sacred during execution. | Permit (encourage) editing the plan as understanding evolves during execution. Code wins when they disagree. |
| `subagent-driven-development` | Spec-compliance reviewer treats spec as authority. Drift between code and spec always resolves toward spec. | Resolution can go either way. The spec is not authoritative over working code. Update `spec-reviewer-prompt.md` to match. |
| `finishing-a-development-branch` | No step to prune or delete the spec/plan. | Add a "prune or delete spec/plan" step as part of completion. |

Search confirmed: no upstream skill uses words like "living",
"prune", "retire", or "delete the spec" — there is genuinely no
existing language to lean on.

## Proposed scope (NOT YET DRAFTED OR APPROVED)

The five edits above. Once drafted, schoen reviews wording before
anything is committed. No implementation skills should be invoked
during this work — this is editing skill markdown, not building
software.

## Operational decisions (resolved 2026-05-03)

1. ~~**Build `schoen/main`.**~~ Done. Two `--no-ff` merge commits on
   top of `origin/main` (one per fix branch). Pushed to mtschoen and
   gitea.
2. ~~**Feature branch for the amendments.**~~ Done. Branch is
   `prune-spec-permanence` (cut from `origin/main`, not
   `schoen/main`, so it can have its own history that merges into
   `schoen/main` separately from the dev-probes and fix branches).
3. ~~**Gitea repo.**~~ Done. `schoen/superpowers` on
   `gitea.llamabox.internal` was already a pull-mirror of obra; now
   converted to a regular repo and carries all four feature branches.
4. ~~**Runtime override.**~~ Resolved before this session started.
   The fork loads as `superpowers@superpowers-dev` via manual
   registration in `~/.claude/plugins/installed_plugins.json`, with
   `superpowers@claude-plugins-official` disabled in
   `~/.claude/settings.json`. Maintained by the `dev/` bootstrap
   scripts now living on the `dev-probes` branch. The three
   originally-considered candidates (user-level skill override, local
   plugin registration, cache override) were all ruled out — see the
   `project_local_dev_setup.md` memory file for full rationale.

## Downstream consequence

`local-ci/CLAUDE.md` line 12-13 currently reads:

> Specs in `docs/specs/` are frozen once merged; amendments go in
> new dated specs that reference the old ones.

That rule was written under upstream-superpowers influence. After
this fork's amendments land, it should be replaced with living-doc
language. Deferred — see `~/local-ci/HANDOFF-windows-runner.md`.

## Resume-from-here checklist

All branch scaffolding is done. What remains:

1. **Draft the 5 skill amendments.** See "Audit" table above. Each
   amendment needs section-by-section approval from schoen before
   committing — wording is load-bearing for skills, and the project's
   CLAUDE.md explicitly warns that "compliance" rewrites of skill
   content will be rejected upstream. Work happens on the
   `prune-spec-permanence` branch (currently checked out).
2. **Fold the broader CLAUDE.md "Parallel Worktree Agents" content
   into the `subagent-driven-development` amendment** — see the
   c384d09 caveat above. The current SKILL.md only addresses one
   subcase; the broader failure-sign list lives in
   `~/.claude/CLAUDE.md` and should be incorporated when amending
   that skill.
3. **Push branch and open PR** back to `schoen/main` on github once
   amendments are approved and committed. Branch is already pushed
   to both remotes; PR creation is a github-side action.
4. **Separately: update `local-ci/CLAUDE.md`** per the "Downstream
   consequence" section above — replace the frozen-spec rule with
   living-doc language. Tracked in `~/local-ci/HANDOFF-windows-runner.md`.
