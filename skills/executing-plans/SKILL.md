---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** Tell your human partner that Superpowers works much better with access to subagents. The quality of its work will be significantly higher if run on a platform with subagent support (Claude Code, Codex CLI, Codex App, Copilot CLI, and Gemini CLI all qualify; see the per-platform tool refs in `../using-superpowers/references/`). If subagents are available, use superpowers:subagent-driven-development instead of this skill.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create todos for the plan items and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step. When reality contradicts the plan (drift,
   impossible API, discovered bug), see "Drift, Divergence, and
   Self-Documenting Code" below.
3. Run verifications as specified
4. Mark as completed; commit per the cadence in the same section

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

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

## Remember
- Review plan critically first
- Follow plan steps; when they conflict with reality, fix the code or flag the deviation — never silently rationalize drift
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required workflow skills:**
- **superpowers:using-git-worktrees** - Ensures isolated workspace (creates one or verifies existing)
- **superpowers:writing-plans** - Creates the plan this skill executes
- **superpowers:finishing-a-development-branch** - Complete development after all tasks
