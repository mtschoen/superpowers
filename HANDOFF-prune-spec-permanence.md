# HANDOFF: prune spec/plan permanence from superpowers skills

**Date started:** 2026-04-26
**Status:** repo cloned, audit done, no edits yet

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

## Repo state

- Cloned from `git@github.com:obra/superpowers.git` to `~/superpowers`
- On `main` at commit `6efe32c` ("Use committed Codex plugin files in
  sync script")
- Remotes:
  - `origin` → `git@github.com:obra/superpowers.git`
  - `mtschoen` → `git@github.com:mtschoen/superpowers.git` (schoen's
    pre-existing fork; added 2026-04-26 in this session)
- No local branch created yet
- No gitea remote configured yet

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

### Bridge to the prune-spec-permanence work

`c384d09` already takes a half-step toward "specs/plans as ephemeral
context": its preferred remediation is *"paste the full task text
inline in the prompt rather than referencing a file path."* That's
the same direction the fork amendments are heading — the plan
travels as conversation context, not as a file the subagent must
locate. Worth citing as prior art within the schoen line when
amending `subagent-driven-development` and `writing-plans`.

## schoen's desired branch model (from this session)

1. Establish a primary fork branch — proposed name `schoen/main` —
   that consolidates `origin/main` plus the two existing fix
   branches above. This becomes the ongoing "where my fork's
   philosophy lives" branch.
2. The spec/plan-permanence amendments (see "Audit" below) happen on
   a **feature branch** cut from `schoen/main` and **PR'd back to
   `schoen/main`** on the github fork. This formalizes the
   philosophical divergence in PR history rather than burying it in
   straight commits to main.
3. Gitea mirror is still desired (`schoen/superpowers` on
   `gitea.llamabox.internal`) but is secondary to the github fork now
   that we know it exists.

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

## Pending operational decisions

1. **Build `schoen/main`.** Cut a new branch off `origin/main` (or
   `mtschoen/main`, equivalent), merge or cherry-pick the two real
   fix commits (`3367249` from `fix/finishing-branch-cleanup-order`
   and `c384d09` from `fix/subagent-driven-dev-worktree-isolation`),
   push to `mtschoen/schoen/main`. Confirm the branch name
   (`schoen/main` is the schoen-stated default; alternatives like
   `mtschoen-main` or `personal-main` if slashes look weird) before
   pushing.
2. **Feature branch for the amendments.** Off `schoen/main`, name
   something like `feat/specs-plans-ephemeral` or
   `feat/prune-spec-permanence`. PR back to `schoen/main` on the
   github fork to record the divergence.
3. **Gitea mirror.** Still desired. Create `schoen/superpowers` on
   `gitea.llamabox.internal` and push `schoen/main`. Secondary to
   the github fork; not blocking.
4. **Runtime override.** How does the modified skill actually replace
   the upstream one inside Claude Code? Three candidates, untried:
   - User-level skill at `~/.claude/skills/<name>/` overriding the
     plugin's
   - Register the fork as a local plugin
   - Direct override of `~/.claude/plugins/cache/...` (gets blown
     away on plugin update — bad)
   This is a separate investigation from the content edits and should
   not block them.

## Downstream consequence

`local-ci/CLAUDE.md` line 12-13 currently reads:

> Specs in `docs/specs/` are frozen once merged; amendments go in
> new dated specs that reference the old ones.

That rule was written under upstream-superpowers influence. After
this fork's amendments land, it should be replaced with living-doc
language. Deferred — see `~/local-ci/HANDOFF-windows-runner.md`.

## Resume-from-here checklist

1. ~~Inventory check.~~ Done 2026-05-03. See "INVENTORY FINAL"
   section above.
2. Confirm `schoen/main` as the primary fork branch name.
3. Build `schoen/main` (consolidate `origin/main` + the two fix
   commits) and push to the github fork. When re-landing `c384d09`,
   merge in the broader CLAUDE.md "Parallel Worktree Agents"
   failure-sign list — see caveat above.
4. Create `schoen/superpowers` on gitea, mirror push.
5. Cut feature branch off `schoen/main` for the amendments.
6. Draft specific wording for each of the 5 amendments. Get schoen's
   approval section by section. Apply, commit.
7. Push feature branch and open PR back to `schoen/main` on github.
8. Separately: solve runtime override (task #12 in parent session).
