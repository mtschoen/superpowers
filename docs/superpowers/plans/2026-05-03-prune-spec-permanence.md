# Prune Spec/Plan Permanence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply surgical edits to five superpowers skills so specs and plans are treated as ephemeral scaffolding rather than durable artifacts.

**Architecture:** Each affected SKILL.md (and two SDD prompt template files) gets targeted insertions/edits per the design at `docs/superpowers/specs/2026-05-03-prune-spec-permanence-design.md`. Existing structure preserved — no philosophy-first rewrites, no template restructure beyond an optional phase header. Slogan: "Good code is self-documenting; the lasting artifacts are real documentation and code." Lifecycle: spec consumed at writing-plans handoff, plan pruned phase-by-phase during execution, plan deleted at branch finish (with durable insight extracted to real docs).

**Tech Stack:** Markdown. Edits via `Edit` tool. Verification via `grep -n`. Git commits per task.

**Spec:** `docs/superpowers/specs/2026-05-03-prune-spec-permanence-design.md` (will be deleted in Task 7 — catch-up for what amended `writing-plans` would have done at handoff)

---

## File Structure

| File | Responsibility | Action |
|---|---|---|
| `skills/brainstorming/SKILL.md` | Spec authoring + handoff | Add "Spec lifecycle" subsection; soften Review Gate message |
| `skills/writing-plans/SKILL.md` | Plan production | Add Plan Lifecycle section; spec consumption + deletion steps; optional phase grouping |
| `skills/executing-plans/SKILL.md` | Plan execution | Add "Drift, Divergence, and Self-Documenting Code" section; reference from Step 2 + Remember |
| `skills/subagent-driven-development/SKILL.md` | SDD loop | Rename "spec compliance" → "plan compliance"; add Plan-File Maintenance section |
| `skills/subagent-driven-development/spec-reviewer-prompt.md` | Reviewer template | Rename file → `plan-reviewer-prompt.md`; update content; add Plan Header field |
| `skills/subagent-driven-development/implementer-prompt.md` | Implementer template | Add Plan Header field; "spec" → "task" |
| `skills/finishing-a-development-branch/SKILL.md` | Branch finishing | Add Plan Disposal subsection in Step 4 |
| `docs/superpowers/specs/2026-05-03-prune-spec-permanence-design.md` | This work's design doc | Delete in Task 7 (lifecycle catch-up) |

---

## Phase 2: Cleanup

### Task 7: Smoke verification + spec deletion

This task closes out Phase 1 by deleting the previous phase from the plan file (the lagged-pruning rule, now in effect since the skills are amended), running cross-skill smoke checks, and deleting the spec file (the catch-up for what amended `writing-plans` would have done at handoff).

**Files:**
- Modify: `docs/superpowers/plans/2026-05-03-prune-spec-permanence.md` (delete Phase 1 section)
- Delete: `docs/superpowers/specs/2026-05-03-prune-spec-permanence-design.md`

- [ ] **Step 1: Cross-skill smoke check**

Run:

```bash
# Verify all amendments landed
grep -n "Spec lifecycle:" skills/brainstorming/SKILL.md
grep -n "## Plan Lifecycle" skills/writing-plans/SKILL.md
grep -n "## Drift, Divergence, and Self-Documenting Code" skills/executing-plans/SKILL.md
grep -n "## Plan-File Maintenance" skills/subagent-driven-development/SKILL.md
grep -n "#### Plan Disposal" skills/finishing-a-development-branch/SKILL.md
grep -n "Plan Compliance Reviewer Prompt Template" skills/subagent-driven-development/plan-reviewer-prompt.md
grep -n "## Plan Header" skills/subagent-driven-development/implementer-prompt.md

# Confirm old terminology is fully gone
grep -rn "spec compliance" skills/ || echo "no occurrences"
grep -rn "Spec compliance" skills/ || echo "no occurrences"
grep -rn "spec-reviewer-prompt" skills/ || echo "no occurrences"
ls skills/subagent-driven-development/spec-reviewer-prompt.md 2>&1 | grep "No such"

# Markdown fence balance across affected files
for f in skills/brainstorming/SKILL.md skills/writing-plans/SKILL.md skills/executing-plans/SKILL.md skills/subagent-driven-development/SKILL.md skills/finishing-a-development-branch/SKILL.md skills/subagent-driven-development/plan-reviewer-prompt.md skills/subagent-driven-development/implementer-prompt.md; do
  echo -n "$f: "
  awk '/^```/ {n++} END {if (n%2==0) print "fences balanced"; else print "FENCE MISMATCH: " n " fences"}' "$f"
done
```

Expected:
- First seven greps return one matching line each
- "no occurrences" or empty results for the cleanup greps
- "No such" for the deleted file
- All seven files report `fences balanced`

If any check fails, stop and investigate. Do not proceed to Step 2.

- [ ] **Step 2: Delete the spec file**

```bash
git rm docs/superpowers/specs/2026-05-03-prune-spec-permanence-design.md
```

This is the catch-up that amended `writing-plans` would have performed at handoff. The design content has lived inside this plan since `writing-plans` ran; the spec file is now redundant.

- [ ] **Step 3: Prune Phase 1 from this plan**

Open `docs/superpowers/plans/2026-05-03-prune-spec-permanence.md`. Delete the entire `## Phase 1: Skill Amendments` section — from its `## Phase 1:` header through the last task in it (Task 6's commit step), stopping just before `## Phase 2: Cleanup`. Keep:
- The plan header (Goal / Architecture / Tech Stack / Spec)
- The File Structure table
- The `## Phase 2: Cleanup` section onward

Per the lagged-pruning rule (now in effect since the skills are amended), this commit is the boundary that sweeps the now-complete Phase 1 out of the plan.

- [ ] **Step 4: Commit Phase 1 prune + spec deletion + Task 7 progress**

```bash
git add -A docs/superpowers/
git commit -m "chore: prune Phase 1 from plan, dispose spec

Phase 1 (skill amendments) is complete; per the new lagged-pruning
rule encoded in those amendments, the next commit deletes the prior
phase. Also delete the spec file — the new writing-plans rule says
the spec dissolves at handoff; this is the catch-up since this plan
was produced under upstream writing-plans (which left the spec
behind)."
```

- [ ] **Step 5: Hand off to `finishing-a-development-branch`**

Per the `executing-plans` Step 3 / SDD final step, invoke the (now-amended) `finishing-a-development-branch` skill. It will:

1. Verify tests pass (no tests in this repo for skill markdown; the smoke checks above are the equivalent — confirm again if needed)
2. Determine base branch (`schoen/main` or `origin/main` depending on intent)
3. Present 4 options
4. For Options 1 or 2: invoke the new Plan Disposal subsection (extract durable insight, delete the plan file)
5. Execute the chosen option

The Plan Disposal step is where this plan's own lifecycle terminates — the plan file gets deleted, with any durable insight folded into real docs (likely none for this work, since the amendments themselves are now the documentation).
