# Delivery Records

This directory keeps the historical execution record for each course milestone. It adapts the strongest practices from the team's HiLeS project while keeping all technical documentation in English.

For current assignments and next actions, use `WORK_BOARD.md` at the repository root. Delivery folders define detailed requirements and preserve evidence; they are not competing task boards.

## Folder convention

```text
deliveries/
├── 00-project-foundation/
├── 01-workshop-1/
├── 02-workshop-2/          created after its official specification is reviewed
├── 03-workshop-3/          created after its official specification is reviewed
├── 04-workshop-4/          created after its official specification is reviewed
├── 05-final-project/       created for final integration
└── _templates/
```

The professor repository published Workshop 2-4 specifications on 2026-11-05.
Do not pre-fill future workshop claims or open their active delivery folders while
Workshop 1 is being closed. Create each folder after reviewing its specification
and beginning that milestone.

## Required documents

Every active delivery contains:

- `IMPLEMENTATION_PLAN.md`: scope, priorities, responsibilities, dependencies, acceptance criteria, and merge gate.
- `CHANGE_LOG.md`: append-only, dated evidence of actual work.

Add when applicable:

- `DEMO_GUIDE.md`: repeatable preparation, sequence, expected results, evidence, contingency, and final checklist.
- `EVIDENCE_REGISTER.md`: indexed source samples, screenshots, reports, test outputs, or other milestone evidence.
- milestone-specific artifacts explicitly required by the professor.

## Status markers

- `[ ]` pending and not verified.
- `[x]` completed with evidence recorded in the change log.
- `[!]` blocked or only partially validated; the limitation must be stated.
- `[-]` explicitly removed from scope with a reason.

## Working rules

1. Start a milestone by copying the templates and recording the branch/base commit.
2. Define a non-negotiable objective and the minimum demonstrable result before assigning tasks.
3. Divide work by owner and reviewer; both students must understand every accepted component.
4. Keep P0 requirements separate from P1 improvements and out-of-scope work.
5. Append evidence as work happens. Do not rewrite an old observation to make it look successful.
6. A checked item must cite a dated change-log entry or an indexed evidence item.
7. Finish with a clean-session review and explicit approval before integration.

`docs/` remains the home of current architecture, accepted decisions, and reusable guidance. Delivery folders remain historical even when the implementation later changes.
