# Project Status Review - 2026-11-10

- **Branch reviewed:** `workflow-1`
- **Starting commit:** `3304d4b` (`complete Workshop 1 evidence and source contracts`)
- **Working tree before planning:** clean
- **Active delivery:** Workshop 1 closure
- **Later deliveries:** Workshops 2-4 planned, not implemented

## Overall status

The project has a strong Workshop 1 evidence base and a clear two-person working
model. All four assigned sources have preserved samples and executed profiles;
Oklahoma/counties and the temporal scope are accepted; source contracts, mapping,
architecture and preliminary CHI design exist. The repository is ready for review,
but Workshop 1 is not submission-complete because the final independent review,
fresh locked notebook execution, PDF and submission commit remain open.

The later-workshop planning gap is now closed: each workshop has a proposed
implementation plan, ownership split, dependencies, acceptance criteria and merge
gate. No later-workshop code or completion claim has been added.

## Workshop status

| Delivery | Current state | Main evidence | Remaining gate |
| --- | --- | --- | --- |
| Foundation | Committed | Context, working agreement, templates | No immediate action unless workflow changes. |
| Workshop 1 | Substantially complete, closing | Four-source evidence, 52-cell notebook, mapping, ER/architecture, report draft, contracts | Kevin cross-review, fresh locked rerun, final English PDF, clean-clone/submission commit. |
| Workshop 2 | Proposed plan only | `deliveries/02-workshop-2/IMPLEMENTATION_PLAN.md` | Workshop 1 closure plus specification clarification/precedence decision. |
| Workshop 3 | Proposed plan only | `deliveries/03-workshop-3/IMPLEMENTATION_PLAN.md` | Accepted Workshop 2 storage/state foundation. |
| Workshop 4 | Proposed plan only | `deliveries/04-workshop-4/IMPLEMENTATION_PLAN.md` | Accepted Workshop 3 current-state/event-integration contracts. |
| Final | Roadmap only | Course-project contract and semester roadmap | Create delivery folder after Workshop 4 planning is validated. |

## Workshop 1 remaining work

1. Kevin reviews the current NOAA/Alerts and GHCN/station contract changes,
   quality examples, volume screens, mapping and report claims.
2. Run the edited notebook in the locked environment and record the new execution
   counts, checksum assertions and zero-error result. Existing saved outputs predate
   the latest prose/config changes and cannot substitute for the final rerun.
3. Reconcile the remaining unchecked acceptance items in the Workshop 1 plan with
   the actual evidence; do not check them without a log/evidence link.
4. Generate the English PDF only after content review, render every page and correct
   layout/citation problems.
5. Perform clean-clone, secret/artifact and Git diff review; record repository URL,
   accepted commit and submission evidence.

## Cross-workshop dependency chain

```text
Workshop 1 contracts/evidence
        |
        v
Workshop 2 historical DB + raw capture + validation + idempotency
        |
        v
Workshop 3 incremental state + revisions + scheduling + event grouping
        |
        v
Workshop 4 baseline/current views + CHI + data health + Dash
        |
        v
Final reproducibility, report, presentation and defense
```

## Immediate safe actions

1. Send the six clarification questions in
   `docs/reports/workshops-2-4-specification-review.md` to the professor.
2. Close Workshop 1 without adding new source scope.
3. Review the Workshop 2 plan and draft the architecture ADR alternatives; do not
   implement infrastructure until the activation gate is accepted.
4. Confirm whether the team will use short-lived milestone branches as required by
   `AGENTS.md` or record an explicit reviewed exception.
5. Add target dates when the professor/course platform publishes them.

## Current risks

- **Specification mismatch:** the published Workshop 2-4 PDFs describe a 2026-I
  public-opinion project; blindly implementing them would misalign Team 9.
- **Workshop overlap:** starting incremental/dashboard code before historical
  storage contracts stabilize would create rework.
- **Evidence freshness:** final Workshop 1 notebook outputs require a fresh locked
  rerun after recent edits.
- **Coverage uncertainty:** full Oklahoma station inventory and exact multi-year
  volume remain implementation evidence, not Workshop 1 facts.
- **Schedule uncertainty:** no target dates or later-workshop point rubrics were
  found in the reviewed PDFs.

## Planning conclusion

The repository is organized and ready for team review. The correct next step is
not to implement all three workshops in parallel; it is to close Workshop 1,
resolve the document conflict, accept the Workshop 2 architecture, and then follow
the dependency chain with evidence at every gate.
