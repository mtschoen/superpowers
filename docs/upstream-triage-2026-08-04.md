# Upstream triage - 2026-08-04 (post v6.2.0 merge)

State snapshot after merging upstream v6.2.0 into schoen/main (merge commit
87beafc, plus cherry-picks e628249 / 54063c8). Parked until Fable quota is
available for PR-preparation sessions. Each PR needs its own session, a
duplicate search refresh, and human review of the full diff per upstream's
CLAUDE.md.

## Absorbed upstream - no action

- Worktree-cleanup-before-branch-delete ordering: our closed PR
  obra/superpowers#1072, absorbed via obra's #1933 refactor.
- Discard menu option: upstream's menu now excludes it (explicit-typed-request
  escape hatch only), matching our 3fb5b20 rationale.
- Ephemeral SDD workspace: upstream's plan-scoped `.superpowers/sdd/<plan>`
  (deleted at plan end) converges with our ephemeral-scaffolding position for
  SDD state.

## Blocked by existing open PRs - do not duplicate

- Parallel dispatch with worktree isolation: obra/superpowers#1534
  (xuefei-wang, 2026-05) and #1213 (zyrill, 2026-04) argue our position.
  v6.2.0 kept the hardline "never parallel" wording, so obra has not accepted
  it yet. Best move: comment on #1534 with our field evidence
  (isolation-failure signs, gitlink pitfall, permission-allowlist gotcha)
  rather than a third PR.

## Live PR candidates

1. `fix(tests/codex-plugin-sync): hermetic line-ending handling` (e628249).
   Still novel upstream as of v6.2.0 (their test has no autocrlf handling).
2. `fix(tests/opencode): register plugin via copy when symlinks unavailable`
   (54063c8). Check against open #2004 (OpenCode v2 plugin API port) first -
   it may moot this.
3. Windows worktree-removal cwd-lock doc note (the "Device or resource busy"
   gotcha re-added in 87beafc to finishing-a-development-branch). Small doc
   fix, no duplicate found.
4. Upstream tests fail on Windows, pre-existing on byte-identical upstream
   files (verified 2026-08-04 on chonkers): 23 assertions in
   tests/codex-plugin-sync/test-sync-to-codex-plugin.sh (sync preview exits
   1), 4 in tests/claude-code/test-sdd-workspace.sh (review-package diff
   path, linked-worktree workspace resolution). Diagnose root cause, then
   file an issue or fix PR.

## Held

- llamabox `feat/hermes-support` (worktree /home/schoen/superpowers-hermes):
  superseded by upstream's in-flight `hermes-harness-rebase` branch (working
  pre_llm_call bootstrap + full test suite). Drop ours once upstream lands
  theirs. Related open PR: #881.

## Fork-permanent divergences (keep, never upstream)

- Plans/specs as ephemeral scaffolding (brainstorming, writing-plans,
  executing-plans, finishing-a-development-branch plan-disposal step);
  upstream commits specs/plans permanently under docs/.
- Plan-compliance verdict language throughout SDD (upstream keeps "spec"
  framing in places).
- docs-update step in finishing-a-development-branch (references our custom
  skill).
- Parallel Dispatch (Worktree Isolation) section in SDD + softened red flag
  (unless #1534 lands upstream).
- dev/ tooling, tracked .claude/settings.json, `+probe1` version suffix.

## Open design debt

- docs/sdd-artifact-conventions-reconciliation.md: still accurate post-merge;
  sharper now that Finish rm -rf's the plan workspace (point 1) and worktree
  invisibility of git-ignored briefs (point 4) is exactly what the Parallel
  Dispatch checklist warns about.
