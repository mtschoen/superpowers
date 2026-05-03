# Prune Spec/Plan Permanence — Design

**Date:** 2026-05-03
**Branch:** `prune-spec-permanence` (cut from `origin/main`, target `schoen/main`)
**Handoff:** `HANDOFF-prune-spec-permanence.md`

## Goal

Amend five superpowers skills so specs and plans are treated as ephemeral
scaffolding for implementation, not durable design artifacts.

## Context

Schoen's fork has a philosophical disagreement with how upstream superpowers
treats specs and plans. Upstream encodes them as durable artifacts (written to
disk, reviewed, handed off, kept around). Schoen treats them as ephemeral LLM
context — useful while the design is in flux, pruned as work progresses,
deleted when the work is done.

The current skill set fights this constantly: every brainstorm wants to write
`docs/superpowers/specs/...`; every plan execution treats the plan file as a
contract; the spec-compliance reviewer treats the spec as authoritative when
code and spec disagree. This design folds the new philosophy into five skills
via surgical edits, not philosophy-first rewrites.

(Self-reference: this spec file is itself ephemeral. Per the new lifecycle,
when `writing-plans` consumes it, its content gets distilled into the plan's
header and this file is deleted. Eat own dogfood.)

## Architecture: the cross-cutting framing

Three concepts shape every amendment.

### 1. Slogan

> **Good code is self-documenting. The lasting artifacts are real
> documentation and code. Specs and plans are scaffolding.**

This is not "code is gospel" — that framing implies durable doctrine, which
is exactly what specs/plans are *not*. "Self-documenting" says good code
makes its intent obvious without external decoration; that's why the
scaffolding can come down.

### 2. Artifact lifecycle

| Phase | Spec file | Plan file |
|---|---|---|
| During brainstorming | Born; reviewed | Does not exist yet |
| At `writing-plans` start | Read; distilled into plan header | Born |
| End of `writing-plans` | **Deleted** | Drafted, self-reviewed |
| During execution | (gone) | Lives; pruned phase-by-phase |
| At branch finish | (gone) | Insight extracted to real docs; **deleted** |

After branch finish, the only artifacts are the code and any durable docs the
work yielded. Plan history is in git (`git log -- <plan-file>`); not in the
tree.

### 3. Authority and drift

**During implementation, the plan is authoritative.** Drift is a defect to
correct, not a license to ratify. Three bug-handling cases:

- **Bug from faithful execution** (you followed the plan, result is buggy):
  fix the bug — which means deviating from the plan — and flag the deviation
  as a possible plan defect.
- **Bug from divergence** (you drifted from the plan, result is buggy): fix
  the code to match the plan. No flag.
- **Plan describes something impossible** (API doesn't exist, file moved,
  framework incompatibility):
  - *Trivial mismatch* (typo, "behavior" vs "behaviour"): agent's call.
  - *Anything complex or uncertain*: stop and raise with the human partner.

The agent never silently ratifies a bug.

### 4. Commit cadence (lagged pruning)

Each commit's diff should narrate what it accomplished:

- **Per-task commit:** flips that task's step checkboxes from `- [ ]` to
  `- [x]` in the plan file as part of the same commit. Strikethrough is
  visible at the moment of completion.
- **Per-phase boundary:** the *next* commit (typically the start of the next
  phase) opens by deleting the prior phase's now-completed tasks plus any
  preamble that only served them. Pruning lags by one commit so checkbox-flip
  and section-delete don't happen together (which would erase the audit
  trail).
- **At branch finish:** plan file deleted entirely, after insight extraction.

### 5. Phase grouping (optional)

Plans optionally group tasks under `## Phase N: <name>` headers. Phases are
the pruning unit. Skip phase headers for small plans where everything is one
phase. In a no-phase-header plan, mid-execution pruning has no triggers; the
plan gets deleted whole at branch-finish (per-task checkbox flips still
happen).

## Approach

**Surgical edits to each affected skill.** No philosophy-first rewrites; no
new cross-cutting "ephemeral-artifacts" skill; no template restructure beyond
the optional phase header. Justification: the framing change is small and
orthogonal to most existing skill content (which is *how to do the thing in
front of you*, not *how to think about artifacts*). Surgical edits also
minimize merge friction with future upstream pulls.

## Per-skill amendments

Five skills are touched. Each amendment is detailed below with proposed text.

### `brainstorming` (skills/brainstorming/SKILL.md)

**New subsection: "Spec lifecycle"** — placed under "After the Design,"
between "Documentation" and "Spec Self-Review":

```markdown
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
```

**User Review Gate edit** — append a single sentence to the existing message:

> "Spec written and committed to `<path>`. Please review it and let me know
> if you want to make any changes before we start writing out the
> implementation plan. (Reminder: it's a working draft — it'll be distilled
> into the plan header and deleted at the next handoff.)"

### `writing-plans` (skills/writing-plans/SKILL.md)

**Overview edit** — append one sentence to the existing first paragraph:

> The plan is **scaffolding** — thorough enough to guide implementation,
> transient enough to be deleted when the work is done. See "Plan Lifecycle"
> below.

**New section: "Plan Lifecycle"** — placed right after Overview, before
Scope Check:

```markdown
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

**New section: "Step 1: Consume the Spec"** — placed before "File Structure":

```markdown
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

**Plan Document Header edit** — prepend one sentence:

> The header is the distilled spec — the part of the brainstorming intent
> that survives into execution. Once the spec file is deleted, this header
> carries the design rationale forward.

**Task Structure edit** — insert above the existing template:

```markdown
**Optional phase grouping.** When tasks cluster into milestones,
group them under `## Phase N: <name>` headers (see example below).
Phases are the pruning unit during execution — when a phase's tasks
all complete, the *next* commit deletes the whole phase from the
plan. Skip phase headers for small plans where everything is one
phase; in that case no mid-execution pruning happens, and the plan
gets deleted whole at branch-finish.
```

Then the existing task-template fenced block gets a single line prepended
to its content (the phase header + a brief inline comment). Inside the
existing four-backtick fence:

```markdown
## Phase 1: <phase name>     <!-- optional; only when phase grouping helps -->

[Optional preamble for the phase]

### Task N: [Component Name]

[…rest of existing template unchanged…]
```

**Self-Review edit** — add one sentence to the intro:

> **Run this BEFORE deleting the spec file (next step).**

**New section: "Spec Deletion"** — placed between Self-Review and Execution
Handoff:

````markdown
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

### `executing-plans` (skills/executing-plans/SKILL.md)

**New section: "Drift, Divergence, and Self-Documenting Code"** — placed
between "When to Revisit Earlier Steps" and "Remember":

```markdown
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

**Step 2 edit (line 25-31):**

```markdown
### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step. When reality contradicts the plan (drift,
   impossible API, discovered bug), see "Drift, Divergence, and
   Self-Documenting Code" below.
3. Run verifications as specified
4. Mark as completed; commit per the cadence in the same section
```

**Remember edit (line 57-63)** — replace "Follow plan steps exactly" bullet:

```markdown
- Follow plan steps; when they conflict with reality, fix the code
  or flag the deviation — never silently rationalize drift
```

### `subagent-driven-development` (skills/subagent-driven-development/)

**Terminology rename** — "spec compliance" → "plan compliance" everywhere
in SKILL.md (lines 8, 12, 38, 50-83 process diagram, 122, 152-200 example
workflow, 225, 244, 247). The reviewer's job is unchanged; the reference
document is now "the task entry from the plan" rather than "the spec."

**File rename:** `spec-reviewer-prompt.md` → `plan-reviewer-prompt.md`.
Content updates inside:
- Title: `# Spec Compliance Reviewer Prompt Template` → `# Plan Compliance
  Reviewer Prompt Template`
- Intro: `Use this template when dispatching a spec compliance reviewer
  subagent.` → `...plan compliance reviewer subagent.`
- Body: `You are reviewing whether an implementation matches its
  specification.` → `You are reviewing whether an implementation matches
  its assigned task.`
- Output: `✅ Spec compliant` → `✅ Plan compliant`

**`implementer-prompt.md` line 78:** `Did I fully implement everything in
the spec?` → `Did I fully implement everything in the task?`

**`implementer-prompt.md` template additions** — split the existing
`## Context` block into two explicit fields:

```
## Plan Header

[FULL TEXT of the plan's Goal / Architecture / Tech Stack header —
the design rationale that carried over from brainstorming]

## Task Description

[FULL TEXT of task from plan]

## Context

[Scene-setting specific to this task: dependencies on prior tasks,
any task-local context not in the header]
```

**`plan-reviewer-prompt.md` template addition** — add a `## Plan Header`
field above the existing `## What Was Requested`:

```
## Plan Header

[FULL TEXT of plan header — the architectural framing the
implementation was supposed to fit into]

## What Was Requested

[FULL TEXT of task requirements]
```

`code-quality-reviewer-prompt.md` is left alone — its job is readability /
idioms / test quality, mostly task-bounded; it does not need the header.

**New section: "Plan-File Maintenance"** — placed in SKILL.md after
"Handling Implementer Status," before "Prompt Templates":

```markdown
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

### `finishing-a-development-branch` (skills/finishing-a-development-branch/SKILL.md)

**Step 4 intro edit** — replace existing intro with:

```markdown
### Step 4: Execute Choice

**For Options 1 and 2: do Plan Disposal first (see below).** For
Option 3, no disposal — work is paused. For Option 4, the whole
branch is being discarded; the plan goes with it.
```

**New subsection: "Plan Disposal (Options 1 and 2)"** — placed at the start
of Step 4, before the existing "Option 1: Merge Locally":

````markdown
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
````

The existing Option 1 / Option 2 / Option 3 / Option 4 sub-flows remain
unchanged.

## Out of scope

The following are NOT part of this design — they are tracked separately:

- **Worktree-isolation extension** (CLAUDE.md "Parallel Worktree Agents"
  text → SDD's Pre-Dispatch Checklist). Different concern, different
  branch (`extend-sdd-worktree-isolation`).
- **Downstream `local-ci/CLAUDE.md` update** (the frozen-spec rule on
  lines 12-13). Tracked in `~/local-ci/HANDOFF-windows-runner.md`. Only
  done after this branch merges into `schoen/main`.

## Self-reference

This spec is itself ephemeral. When `writing-plans` runs against it, the
content of "Goal," "Architecture," and the slogan above will be distilled
into the plan's header, and this file will be deleted. The plan file will
then guide the surgical edits to each of the five skills, will shrink as
those edits commit, and will itself be deleted at branch-finish — with
this design's rationale folded into nothing more than the resulting
SKILL.md text and the commit history.

That is the lifecycle this design encodes. Apply it to itself.
