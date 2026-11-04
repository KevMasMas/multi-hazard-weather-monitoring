# Two-Person Work Plan

Status: initial proposal for team approval. Ownership means primary implementation responsibility, not exclusive knowledge.

The active assignment checklist lives in the corresponding `deliveries/<milestone>/IMPLEMENTATION_PLAN.md`. This document only defines stable semester-level ownership and collaboration rules.

## Stable source ownership

| Source/workstream | Primary | Reviewer and backup |
| --- | --- | --- |
| NOAA Storm Events historical source | Kevin | Pablo |
| GHCN-Daily/NCEI historical source | Pablo | Kevin |
| NWS Alerts incremental source | Kevin | Pablo |
| NWS station observations incremental source | Pablo | Kevin |
| Canonical model and source integration | Pair decision | Both approve |
| Compound Hazard Index | Pair decision | Both approve |

This split gives each person one historical and one incremental source and forces integration through a shared contract.

## Milestone leadership

| Milestone | Kevin lead | Pablo lead | Shared review gate |
| --- | --- | --- | --- |
| Foundation | Git workflow, repository rules, context consistency | Academic review, requirement traceability, scope questions | Foundation diff and initial integration approach |
| Workshop 1 | NOAA Storm Events and NWS Alerts evidence; mapping contribution | GHCN-Daily and NWS observations evidence; profiling contribution | Region, user, contracts, ER model, index proposal, report |
| Workshop 2 | Canonical database model, migrations, CLI integration | Historical adapters, raw landing, orchestration setup | Validation, quarantine, idempotency, clean-run evidence |
| Workshop 3 | Alerts polling, content-change handling, source audit/status | Station polling, Airflow/scheduler jobs, watermark operations | Event matching, retries, failure recovery, integration tests |
| Workshop 4 | Index calculation and analytical views | Geospatial aggregation and dashboard experience | Sensitivity analysis, limitations, data-health panel |
| Final | Reproducibility audit, test/quality gate, release checklist | Report assembly, presentation assets, demo coordination | Fresh-clone rehearsal and individual technical defense |

## Weekly collaboration rhythm

1. Planning: choose a small deliverable, owner, reviewer, evidence required, and due date.
2. Implementation: work in separate short-lived branches; keep changes reviewable.
3. Review: the non-owner reviews source assumptions, tests, documentation, and reproducibility.
4. Integration: merge only after the agreed checks pass and update the relevant report.
5. Knowledge transfer: each person explains the other's merged change and alternates live-demo steps.

## Definition of done for a task

- The requirement or decision is linked.
- Code or documentation is in its intended area and is in English.
- Relevant automated checks pass, or the absence of a runnable check is stated.
- External observations have preserved evidence and source citations.
- No secrets or bulk raw data are tracked.
- The reviewer can explain the change and its limitations.
- The plan/report reflects what actually happened and what remains open.

## Avoiding merge conflicts

- One primary editor per document during a task.
- Separate source adapters and fixture directories by source.
- Coordinate before editing shared schemas, CLI entry points, Compose files, or indicator formulas.
- Rebase or merge the latest accepted base before final review; never overwrite another member's uncommitted work.
