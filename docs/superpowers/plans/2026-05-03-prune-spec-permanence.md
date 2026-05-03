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

## Phase 1: Skill Amendments

[Six tasks, one per affected skill or prompt-template group. Tasks are independent — order does not matter for correctness, but they're numbered in the order they appear in the spec for readability.]

### Task 1: `brainstorming` — Spec lifecycle subsection + Review Gate softening

**Files:**
- Modify: `skills/brainstorming/SKILL.md`

- [ ] **Step 1: Read the current file**

Read `skills/brainstorming/SKILL.md` in full. Confirm:
- "Documentation:" subsection exists around line 109
- "Spec Self-Review:" subsection exists around line 116
- "User Review Gate:" subsection exists around line 126

- [ ] **Step 2: Insert "Spec lifecycle" subsection between "Documentation" and "Spec Self-Review"**

Use the `Edit` tool. Find this exact block:

```
- Commit the design document to git

**Spec Self-Review:**
```

Replace with:

```
- Commit the design document to git

**Spec lifecycle:**

The spec file is a working draft, not a durable design doc. Its job
is to anchor the brainstorm-to-plan handoff so you and your human
partner can review the design before plan-writing starts.

When `writing-plans` runs, it will:
- Distill this spec's intent into the plan's `Goal:` / `Architecture:`
  / `Tech Stack:` header
- Delete this spec file from the tree

The spec exists for the duration of brainstorming + plan-writing.
After that, the plan is the only artifact, and the plan itself is
destined to be deleted when work completes — at branch-finish time,
any durable insight is folded into proper documentation (README,
ARCHITECTURE.md, inline doc comments) and the plan goes away. **The
lasting artifacts are real documentation and code. Specs and plans
are scaffolding.**

If the design needs revision later (during plan-writing or
execution), edit the plan — the spec is gone by then.

**Spec Self-Review:**
```

- [ ] **Step 3: Update User Review Gate message**

Find this exact line:

```
> "Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start writing out the implementation plan."
```

Replace with:

```
> "Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start writing out the implementation plan. (Reminder: it's a working draft — it'll be distilled into the plan header and deleted at the next handoff.)"
```

- [ ] **Step 4: Verify both edits**

Run:

```bash
grep -n "Spec lifecycle:" skills/brainstorming/SKILL.md
grep -n "Reminder: it's a working draft" skills/brainstorming/SKILL.md
```

Expected: each command returns exactly one matching line.

- [ ] **Step 5: Commit**

```bash
git add skills/brainstorming/SKILL.md
git commit -m "feat(brainstorming): spec lifecycle as ephemeral scaffolding

Add 'Spec lifecycle' subsection establishing that the spec is a
working draft destined for distillation+deletion at writing-plans
handoff. Soften User Review Gate message with transience reminder."
```

---

### Task 2: `writing-plans` — Lifecycle, spec consumption, phase grouping, spec deletion

**Files:**
- Modify: `skills/writing-plans/SKILL.md`

- [ ] **Step 1: Read the current file**

Read `skills/writing-plans/SKILL.md` in full. Confirm structure: Overview → Scope Check → File Structure → Bite-Sized Task Granularity → Plan Document Header → Task Structure → No Placeholders → Remember → Self-Review → Execution Handoff.

- [ ] **Step 2: Append a sentence to the Overview's first paragraph**

Find this exact block (the end of the Overview's first paragraph):

```
Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.
```

Replace with:

```
Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

The plan is **scaffolding** — thorough enough to guide implementation, transient enough to be deleted when the work is done. See "Plan Lifecycle" below.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.
```

- [ ] **Step 3: Insert "Plan Lifecycle" section after Overview, before Scope Check**

Find the line `## Scope Check`. Insert this content immediately before it:

```
## Plan Lifecycle

A plan is scaffolding for implementation, not durable documentation.
Three moments matter:

**Birth:** This skill absorbs the brainstorming spec — the spec's
intent is distilled into the plan's header (`Goal:` / `Architecture:`
/ `Tech Stack:`) — and the spec file is deleted. From this point
forward, the plan is the only artifact.

**During execution:** Each commit that completes tasks flips those
tasks' checkboxes from `- [ ]` to `- [x]`. The *next* commit
(typically the start of the next phase) opens by deleting the prior
phase's now-completed tasks plus any preamble that only served them.
Pruning lags the work by one commit so each commit's diff narrates
what it accomplished.

**Death:** At branch-finish time, the plan is deleted. Before
deletion, any durable insight (new abstractions, novel testing
patterns, tricky tradeoffs, architectural decisions) is folded into
proper documentation — README, ARCHITECTURE.md, inline doc comments,
type docs. **The lasting artifacts are real documentation and code.
Specs and plans are scaffolding.**

Once the plan is deleted, its history is in git, not in the tree.
`git log -- <plan-file>` is the audit trail. Don't keep the plan
around 'just in case' — real documentation handles that role.

**Once this skill starts, the plan is authoritative.** If self-review
reveals a gap or an error, fix the plan (or the header). Don't update
the spec — it's dying.

```

(Note the trailing blank line so the new section is separated from `## Scope Check`.)

- [ ] **Step 4: Insert "Step 1: Consume the Spec" section before File Structure**

Find the line `## File Structure`. Insert this content immediately before it:

```
## Step 1: Consume the Spec

Before drafting tasks:

1. Read the spec file (`docs/superpowers/specs/<path>` from
   brainstorming).
2. Distill its intent into the plan's header (`Goal:` /
   `Architecture:` / `Tech Stack:`) — see "Plan Document Header"
   below.
3. Leave the spec file in place for now. Self-review still reads it.
   Deletion happens after self-review (see "Spec Deletion" below).

```

- [ ] **Step 5: Prepend a framing sentence to "Plan Document Header"**

Find this exact block:

```
## Plan Document Header

**Every plan MUST start with this header:**
```

Replace with:

```
## Plan Document Header

The header is the distilled spec — the part of the brainstorming
intent that survives into execution. Once the spec file is deleted,
this header carries the design rationale forward.

**Every plan MUST start with this header:**
```

- [ ] **Step 6: Insert "Optional phase grouping" prose before the Task Structure example**

Find this exact line:

```
## Task Structure
```

Replace the `## Task Structure` heading and the line(s) immediately following it through the start of the existing fenced code block. Specifically, find:

```
## Task Structure

````markdown
### Task N: [Component Name]
```

Replace with:

```
## Task Structure

**Optional phase grouping.** When tasks cluster into milestones,
group them under `## Phase N: <name>` headers (see example below).
Phases are the pruning unit during execution — when a phase's tasks
all complete, the *next* commit deletes the whole phase from the
plan. Skip phase headers for small plans where everything is one
phase; in that case no mid-execution pruning happens, and the plan
gets deleted whole at branch-finish.

````markdown
## Phase 1: <phase name>     <!-- optional; only when phase grouping helps -->

[Optional preamble for the phase]

### Task N: [Component Name]
```

(This adds the `## Phase 1:` header and the optional-preamble line at the top of the existing example fenced block; the rest of the example template is unchanged.)

- [ ] **Step 7: Add "Run this BEFORE deleting the spec file" sentence to Self-Review intro**

Find this exact block:

```
## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.
```

Replace with:

```
## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch. **Run this BEFORE deleting the spec file (next step).**
```

- [ ] **Step 8: Insert "Spec Deletion" section before Execution Handoff**

Find the line `## Execution Handoff`. Insert this content immediately before it:

````
## Spec Deletion

After self-review passes, delete the spec file:

```bash
git rm docs/superpowers/specs/<spec-file>.md
git add docs/superpowers/plans/<plan-file>.md
git commit -m "plan: <feature> (consume spec)"
```

Commit the spec removal alongside the new plan. The spec's content
now lives in the plan's header. The git history records that the
spec ever existed.

````

(Note the four-backtick outer fence so the inner ```bash block doesn't terminate it. The trailing blank line separates the new section from `## Execution Handoff`.)

- [ ] **Step 9: Verify all changes**

Run:

```bash
grep -n "Plan Lifecycle$" skills/writing-plans/SKILL.md
grep -n "## Step 1: Consume the Spec" skills/writing-plans/SKILL.md
grep -n "header is the distilled spec" skills/writing-plans/SKILL.md
grep -n "Optional phase grouping" skills/writing-plans/SKILL.md
grep -n "Run this BEFORE deleting the spec file" skills/writing-plans/SKILL.md
grep -n "## Spec Deletion" skills/writing-plans/SKILL.md
grep -n "thorough enough to guide implementation, transient enough" skills/writing-plans/SKILL.md
```

Expected: each grep returns exactly one matching line.

- [ ] **Step 10: Commit**

```bash
git add skills/writing-plans/SKILL.md
git commit -m "feat(writing-plans): plan lifecycle as ephemeral scaffolding

Add Plan Lifecycle section, Step 1 Consume the Spec, Spec Deletion
step, optional phase grouping in Task Structure. Plan now consumes
the brainstorming spec, distills into header, and deletes spec at
end of skill. Plan itself is destined for deletion at branch finish."
```

---

### Task 3: `executing-plans` — Drift, Divergence, and Self-Documenting Code

**Files:**
- Modify: `skills/executing-plans/SKILL.md`

- [ ] **Step 1: Read the current file**

Read `skills/executing-plans/SKILL.md` in full. Confirm structure: Overview → The Process (Step 1/2/3) → When to Stop → When to Revisit → Remember → Integration.

- [ ] **Step 2: Edit Step 2 to reference the new Drift section**

Find this exact block:

```
### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed
```

Replace with:

```
### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step. When reality contradicts the plan (drift,
   impossible API, discovered bug), see "Drift, Divergence, and
   Self-Documenting Code" below.
3. Run verifications as specified
4. Mark as completed; commit per the cadence in the same section
```

- [ ] **Step 3: Insert "Drift, Divergence, and Self-Documenting Code" section before "Remember"**

Find the line `## Remember`. Insert this content immediately before it:

```
## Drift, Divergence, and Self-Documenting Code

The plan is authoritative during execution — it's the contract you're
implementing against. But execution is not blind transcription. When
the plan and the working code disagree, *something is wrong*; drift
is a defect to correct, not a license to ratify whatever's in the
tree.

**Slogan:** Good code is self-documenting. The lasting artifacts are
real documentation and code. The plan is scaffolding — by the time
work is done, the code should read clearly without it.

### Bug-handling cases

**Bug from faithful execution.** You followed the plan exactly and
the result is buggy. The plan has a defect. Fix the bug — which
means deviating from the plan — and flag the deviation to your human
partner ("the plan said X but X produces Y; I did Z instead — does
that look right?"). Don't silently carry buggy code forward and
don't silently ratify the bug by updating the plan to match.

**Bug from divergence.** You drifted from the plan, and the result
is buggy. The plan was right. Fix the code to match the plan. No
flag needed — this is just discipline.

**Plan describes something impossible.** The plan calls for an API
or behavior that doesn't survive contact with reality.
- *Trivial mismatch* (typo, spelling, "behavior" vs "behaviour"):
  agent's call. Use your best judgment, fix it, move on.
- *Anything complex or uncertain* (semantically different API,
  architectural impossibility): stop and raise it with your human
  partner.

### Commit cadence

The plan file is part of the work history, and its pruning rhythm
encodes when each piece of work happened.

**Per-task commit:** When a task's steps are complete, flip its
steps' checkboxes from `- [ ]` to `- [x]` in the plan file as part
of that commit. The diff shows the strikethrough at the moment of
completion.

**Per-phase boundary:** When all tasks in a phase are complete, the
*next* commit (typically the start of the next phase) opens by
deleting the now-completed phase from the plan, including any
preamble that only served it. Pruning lags by one commit so each
commit's diff narrates what it accomplished.

**At branch-finish:** the plan file gets deleted entirely — see
`finishing-a-development-branch` for the disposal step.

### Done means done

Before declaring work complete:

- All checkboxes flipped (no leftover `- [ ]`)
- All drift resolved (fix the code or flag a deviation — never
  silently rationalize)
- Code reads clearly enough to stand without the plan — that's the
  self-documenting test

```

- [ ] **Step 4: Update "Remember" bullet about following plan steps**

Find this exact line:

```
- Follow plan steps exactly
```

Replace with:

```
- Follow plan steps; when they conflict with reality, fix the code or flag the deviation — never silently rationalize drift
```

- [ ] **Step 5: Verify changes**

Run:

```bash
grep -n "Drift, Divergence, and Self-Documenting Code" skills/executing-plans/SKILL.md
grep -n "self-documenting test" skills/executing-plans/SKILL.md
grep -n "never silently rationalize drift" skills/executing-plans/SKILL.md
grep -c "Follow plan steps exactly" skills/executing-plans/SKILL.md
```

Expected:
- First three return one matching line each
- Fourth returns `0` (the old phrasing should be gone)

- [ ] **Step 6: Commit**

```bash
git add skills/executing-plans/SKILL.md
git commit -m "feat(executing-plans): drift handling + commit cadence

Add 'Drift, Divergence, and Self-Documenting Code' section. Plan is
authoritative during execution but drift is a defect; bugs from
faithful execution get fixed and flagged; trivial reality mismatches
are agent's call; complex ones escalate. Commit cadence: per-task
checkbox flips, lagged per-phase pruning, branch-finish deletion."
```

---

### Task 4: `subagent-driven-development` SKILL.md — terminology rename + Plan-File Maintenance

**Files:**
- Modify: `skills/subagent-driven-development/SKILL.md`

- [ ] **Step 1: Read the current file**

Read `skills/subagent-driven-development/SKILL.md` in full. Note line numbers of "spec compliance" / "spec reviewer" / "Spec reviewer" occurrences.

- [ ] **Step 2: Rename "spec compliance" → "plan compliance" everywhere**

Use `Edit` with `replace_all: true`. Apply each of these renames:

| Old | New |
|---|---|
| `spec compliance review` | `plan compliance review` |
| `spec compliance` | `plan compliance` |
| `Spec compliance` | `Plan compliance` |

Be careful not to touch the diagram references to `./spec-reviewer-prompt.md` (those are handled in the next step).

- [ ] **Step 3: Rename file path references and diagram nodes**

Apply each of these renames using `Edit` with `replace_all: true`:

| Old | New |
|---|---|
| `./spec-reviewer-prompt.md` | `./plan-reviewer-prompt.md` |
| `Dispatch spec reviewer subagent` | `Dispatch plan reviewer subagent` |
| `Spec reviewer subagent confirms code matches spec?` | `Plan reviewer subagent confirms code matches plan?` |
| `Implementer subagent fixes spec gaps` | `Implementer subagent fixes plan gaps` |
| `Spec reviewer:` | `Plan reviewer:` |

- [ ] **Step 4: Update phrase about "spec compliance prevents over/under-building"**

Find this exact line:

```
- Spec compliance prevents over/under-building
```

Replace with:

```
- Plan compliance prevents over/under-building
```

(This may already be handled by the bulk rename in Step 2; if so, skip.)

- [ ] **Step 5: Update "Core principle" line**

Find this exact line:

```
**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration
```

Replace with:

```
**Core principle:** Fresh subagent per task + two-stage review (plan then quality) = high quality, fast iteration
```

- [ ] **Step 6: Insert "Plan-File Maintenance" section between "Handling Implementer Status" and "Prompt Templates"**

Find the line `## Prompt Templates`. Insert this content immediately before it:

```
## Plan-File Maintenance

The plan file is part of the work history. The controller is
responsible for keeping it in sync; implementer subagents touch it
only on explicit instruction. (The existing red flag *"Make subagent
read plan file (provide full text instead)"* still applies — the
implementer never reads the plan to understand its task.)

**Per-task commit:** When dispatching an implementer, include in the
prompt: *"After your work commit, also flip these checkboxes in
`<plan-file-path>` from `- [ ]` to `- [x]`: <list of step lines for
this task>."* The implementer's commit will contain code + checkbox
flips together. The diff narrates "task N: done."

**Phase boundary commit:** When dispatching the first implementer of
a new phase (after the previous phase's last task was reviewed and
approved), include in the prompt: *"Before your work, delete lines
`<X-Y>` of `<plan-file-path>` (the now-complete prior phase plus its
preamble). Then proceed."* That implementer's single commit then
does three things: delete the old phase, do the new task's work,
flip the new task's checkboxes.

**Why pruning lags by one commit:** each commit's diff should
narrate what it accomplished — newly-completed tasks show as
strikethrough, then the next phase opens by sweeping them out. If
checkbox-flip and section-delete were in the same commit, the diff
would show "minus task X, plus nothing" with no record of what
finished.

**Subagent context:** Implementer and plan-compliance reviewer
subagents receive the plan header (Goal / Architecture / Tech Stack)
in addition to the task text — the header is the design rationale
that survived from brainstorming, and subagents need it to make
consistent architectural choices. The existing red flag against
making subagents *locate and read* the plan file still applies; the
controller pastes the header into the prompt.

**Branch finish:** `finishing-a-development-branch` deletes the
plan file entirely after any durable insight is folded into real
docs. Don't preempt that step.

**See also:** `executing-plans` "Drift, Divergence, and
Self-Documenting Code" — the drift-handling rules apply identically
here. The controller should reject implementer work that ratifies
drift instead of fixing it or flagging it as a possible plan defect.

```

- [ ] **Step 7: Verify changes**

Run:

```bash
grep -c "spec compliance" skills/subagent-driven-development/SKILL.md
grep -c "Spec reviewer" skills/subagent-driven-development/SKILL.md
grep -c "spec-reviewer-prompt.md" skills/subagent-driven-development/SKILL.md
grep -n "## Plan-File Maintenance" skills/subagent-driven-development/SKILL.md
grep -n "plan compliance" skills/subagent-driven-development/SKILL.md
grep -n "plan-reviewer-prompt.md" skills/subagent-driven-development/SKILL.md
```

Expected:
- First three return `0` (old terminology is gone)
- Fourth returns one matching line (new section)
- Fifth and sixth return multiple matching lines

- [ ] **Step 8: Commit**

```bash
git add skills/subagent-driven-development/SKILL.md
git commit -m "feat(subagent-driven-development): plan compliance + plan-file maintenance

Rename 'spec compliance' → 'plan compliance' everywhere (the spec is
gone by the time SDD runs; the reference doc is the plan). Rename
file references for spec-reviewer-prompt.md → plan-reviewer-prompt.md.
Add Plan-File Maintenance section: controller manages plan-file
edits via implementer-prompt instructions; lagged-pruning rhythm;
subagents receive plan header for architectural context."
```

---

### Task 5: SDD prompt template files — rename + content updates

**Files:**
- Move: `skills/subagent-driven-development/spec-reviewer-prompt.md` → `skills/subagent-driven-development/plan-reviewer-prompt.md`
- Modify (the renamed file): `skills/subagent-driven-development/plan-reviewer-prompt.md`
- Modify: `skills/subagent-driven-development/implementer-prompt.md`

- [ ] **Step 1: Read both current files**

Read `skills/subagent-driven-development/spec-reviewer-prompt.md` and `skills/subagent-driven-development/implementer-prompt.md` in full.

- [ ] **Step 2: Rename `spec-reviewer-prompt.md` → `plan-reviewer-prompt.md`**

```bash
git mv skills/subagent-driven-development/spec-reviewer-prompt.md skills/subagent-driven-development/plan-reviewer-prompt.md
```

- [ ] **Step 3: Update title and intro of the renamed file**

Find this exact block at the top of `skills/subagent-driven-development/plan-reviewer-prompt.md`:

```
# Spec Compliance Reviewer Prompt Template

Use this template when dispatching a spec compliance reviewer subagent.

**Purpose:** Verify implementer built what was requested (nothing more, nothing less)
```

Replace with:

```
# Plan Compliance Reviewer Prompt Template

Use this template when dispatching a plan compliance reviewer subagent.

**Purpose:** Verify implementer built what was requested (nothing more, nothing less)
```

- [ ] **Step 4: Update the prompt body in the renamed file**

Find this exact line:

```
    description: "Review spec compliance for Task N"
```

Replace with:

```
    description: "Review plan compliance for Task N"
```

Find this exact line:

```
    You are reviewing whether an implementation matches its specification.
```

Replace with:

```
    You are reviewing whether an implementation matches its assigned task.
```

- [ ] **Step 5: Add Plan Header field above What Was Requested in the renamed file**

Find this exact block:

```
    ## What Was Requested

    [FULL TEXT of task requirements]
```

Replace with:

```
    ## Plan Header

    [FULL TEXT of plan header — the architectural framing the
    implementation was supposed to fit into]

    ## What Was Requested

    [FULL TEXT of task requirements]
```

- [ ] **Step 6: Update Output Format in the renamed file**

Find this exact line:

```
    - ✅ Spec compliant (if everything matches after code inspection)
```

Replace with:

```
    - ✅ Plan compliant (if everything matches after code inspection)
```

- [ ] **Step 7: Add Plan Header field to `implementer-prompt.md`**

Find this exact block:

```
    ## Task Description

    [FULL TEXT of task from plan - paste it here, don't make subagent read file]

    ## Context

    [Scene-setting: where this fits, dependencies, architectural context]
```

Replace with:

```
    ## Plan Header

    [FULL TEXT of the plan's Goal / Architecture / Tech Stack header —
    the design rationale that carried over from brainstorming]

    ## Task Description

    [FULL TEXT of task from plan - paste it here, don't make subagent read file]

    ## Context

    [Scene-setting specific to this task: dependencies on prior tasks,
    any task-local context not in the header]
```

- [ ] **Step 8: Update self-review question in `implementer-prompt.md`**

Find this exact line:

```
    - Did I fully implement everything in the spec?
```

Replace with:

```
    - Did I fully implement everything in the task?
```

- [ ] **Step 9: Verify changes**

Run:

```bash
ls skills/subagent-driven-development/plan-reviewer-prompt.md
ls skills/subagent-driven-development/spec-reviewer-prompt.md 2>&1 | grep "No such"
grep -n "Plan Compliance Reviewer Prompt Template" skills/subagent-driven-development/plan-reviewer-prompt.md
grep -n "matches its assigned task" skills/subagent-driven-development/plan-reviewer-prompt.md
grep -n "## Plan Header" skills/subagent-driven-development/plan-reviewer-prompt.md
grep -n "✅ Plan compliant" skills/subagent-driven-development/plan-reviewer-prompt.md
grep -n "## Plan Header" skills/subagent-driven-development/implementer-prompt.md
grep -c "in the spec?" skills/subagent-driven-development/implementer-prompt.md
```

Expected:
- First confirms file exists
- Second confirms old file gone (returns "No such")
- Next four return one match each
- Last returns one match (Plan Header in implementer)
- Final `grep -c` returns `0` (old "in the spec?" phrasing gone)

- [ ] **Step 10: Commit**

```bash
git add -A skills/subagent-driven-development/
git commit -m "feat(subagent-driven-development): plan compliance prompts + plan header context

Rename spec-reviewer-prompt.md → plan-reviewer-prompt.md; update
title, intro, body, output. Add Plan Header field to both implementer
and plan-reviewer templates so subagents receive the architectural
framing distilled from brainstorming. Update implementer self-review
question 'in the spec' → 'in the task'."
```

---

### Task 6: `finishing-a-development-branch` — Plan Disposal subsection

**Files:**
- Modify: `skills/finishing-a-development-branch/SKILL.md`

- [ ] **Step 1: Read the current file**

Read `skills/finishing-a-development-branch/SKILL.md` in full. Confirm Step 4 begins with `### Step 4: Execute Choice` and the first sub-flow is `#### Option 1: Merge Locally`.

- [ ] **Step 2: Edit Step 4 intro**

Find this exact block:

```
### Step 4: Execute Choice

#### Option 1: Merge Locally
```

Replace with the content in the four-backtick-fenced block below. (The outer four-backtick fence is just for this plan document — the actual replacement text starts at `### Step 4: Execute Choice` and ends at `#### Option 1: Merge Locally`. Inner triple-backtick fences are part of the replacement text.)

````
### Step 4: Execute Choice

**For Options 1 and 2: do Plan Disposal first (see below).** For
Option 3, no disposal — work is paused. For Option 4, the whole
branch is being discarded; the plan goes with it.

#### Plan Disposal (Options 1 and 2)

Before merging or pushing, dispose of the plan file.

**1. Extract durable insight, if any.** Most plans are nearly empty
by this point — phases were pruned during execution and only the
header plus the final phase's struck-through tasks remain. Review
the branch's work — the code diff (`git diff <base>..HEAD`), the
commit messages, and whatever's left in the plan — and ask: does
this work expose anything that should outlast the scaffolding?

Examples of insight worth folding into proper docs:
- A new abstraction or pattern → README / ARCHITECTURE.md
- A non-obvious testing approach → test-suite README or test file
  comments
- A subtle invariant or constraint → inline doc comment near the
  code that enforces it
- An architectural decision with non-obvious tradeoffs → an
  ADR-style note (if the project uses them) or ARCHITECTURE.md

Most work yields nothing in this category. That's normal. Don't
fabricate insight to justify the step.

**2. Delete the plan file.**

If insight was folded in:

```bash
git rm docs/superpowers/plans/<plan-file>.md
git add <docs touched in step 1>
git commit -m "docs: <feature> (dispose plan, fold insight into <doc>)"
```

If no docs were touched:

```bash
git rm docs/superpowers/plans/<plan-file>.md
git commit -m "chore: remove implementation plan for <feature>"
```

Then proceed to your chosen option below.

#### Option 1: Merge Locally
````

- [ ] **Step 3: Verify changes**

Run:

```bash
grep -n "#### Plan Disposal" skills/finishing-a-development-branch/SKILL.md
grep -n "Extract durable insight" skills/finishing-a-development-branch/SKILL.md
grep -n "fold insight into" skills/finishing-a-development-branch/SKILL.md
```

Expected: each grep returns one matching line.

Also verify the file still parses as valid markdown by reading it and confirming no broken fenced code blocks:

```bash
awk '/^```/ {n++} END {if (n%2==0) print "fences balanced"; else print "FENCE MISMATCH: " n " fences"}' skills/finishing-a-development-branch/SKILL.md
```

Expected: `fences balanced`

- [ ] **Step 4: Commit**

```bash
git add skills/finishing-a-development-branch/SKILL.md
git commit -m "feat(finishing-a-development-branch): plan disposal step

Add Plan Disposal subsection at start of Step 4 (applies to Options
1 and 2): extract any durable insight into proper docs (README,
ARCHITECTURE.md, inline comments), then delete the plan file.
Establishes the 'lasting artifacts are real documentation and code'
principle at the natural disposal moment."
```

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
