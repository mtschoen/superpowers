# Task: Remove the "Discard" option from finishing-a-development-branch

**Date:** 2026-05-29
**Status:** Todo
**Source:** User feedback — `finishing-a-development-branch` presented "Discard this work" as option 4 immediately after a 12-commit feature was completed and verified. Offering destructive deletion deadpan right after success feels dangerous and out of place.

---

## Goal

Drop option 4 (**Discard this work**) from the skill entirely. The skill should present **3** options, not 4:

1. Merge back to `<base-branch>` locally
2. Push and create a Pull Request
3. Keep the branch as-is (handle it later)

**Rationale:** Discarding completed work is almost never the right call at this stage, and surfacing it as a first-class menu item invites accidental data loss. A user who genuinely wants to discard can say so in the free-text write-in (AskUserQuestion always offers "Other") or just cancel the prompt and delete the branch manually. The safe default is to never *suggest* destruction.

---

## File

`skills/finishing-a-development-branch/SKILL.md`

## Edit checklist (Option 4 is referenced in several places — remove all)

- [ ] **Step 3 (Present Options):** change the option block from 4 items to 3; drop the `4. Discard this work` line.
- [ ] **Step 4 intro:** the line "For Options 1 and 2: do Plan Disposal first … For Option 3, no disposal … For Option 4, the whole branch is being discarded; the plan goes with it." — drop the Option 4 clause.
- [ ] **Step 4:** delete the entire `#### Option 4: Discard` subsection (the typed-`discard` confirmation flow).
- [ ] **Step 5 (Cleanup):** change "For Options 1, 2, 4:" → "For Options 1 and 2:" (note: only Option 1 actually triggers branch cleanup; Option 2 keeps the branch). Remove the `git branch -D <feature-branch>` force-delete line and its "Option 4 (discarded …)" comment, keeping only the Option 1 `git branch -d` safe-delete.
- [ ] **Quick Reference table:** delete the `4. Discard` row.
- [ ] **Common Mistakes:** remove the "No confirmation for discard" entry (now moot).
- [ ] **Red Flags:** remove "Delete work without confirmation" (Never) and "Get typed confirmation for Option 4" (Always); reword "Clean up worktree for Options 1 & 4 only" → "Clean up worktree for Option 1 only".
- [ ] Re-read the whole SKILL.md after edits to confirm no dangling "Option 4" / "discard" references remain and the option numbering is internally consistent.

## Verification

- [ ] `grep -ri discard skills/finishing-a-development-branch/` returns nothing (or only unrelated prose).
- [ ] The four-options→three-options change reads cleanly; the Quick Reference table still aligns.
- [ ] If the repo has a skills-lint / dev-check (`dev/superpowers-dev-check.py`), run it.

## Note

This is a personal/fork-local change to a synced skill. If this superpowers install tracks an upstream (obra/superpowers), decide whether to keep the change local or propose it upstream before syncing, so a sync doesn't clobber it.
