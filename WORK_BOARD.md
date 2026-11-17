# Team Work Board

This is the single operational entry point for Team 9. Read this file to know the current state, who owns each workstream, and what must happen next.

## Current state

**Delivery preparation, 2026-11-16:** the Workshop 2 PDF, three genuine sample
pairs and executed notebook are prepared for final team review. Ten actual
Airflow source/year batches cover 2021-2025: 13,561 Oklahoma Storm Events and
5,478 GHCN measurements (one station). All 29 tests pass without skips.
A historical CLI rerun, container restart and three subsequent DAG replays
preserved canonical counts with zero duplicates. Kevin supplied the actual UI
screenshot. See `workshop_2/EVIDENCE_REGISTER.md` and the current change log.

**Kevin next:** review the PDF and database/source limitations, select the commit,
then perform commit/push and Moodle upload. **Pablo next:** cross-review DAGs,
sample notebook/ZIP and the documented scope. Record approval only when received.
The 2010-2020 years, broader station inventory, county assignments and later
workshops remain open; the 2026-I handout discrepancy is not resolved.

| Item | State |
| --- | --- |
| Repository foundation | Committed and pushed as `602143d` on `workflow-1` |
| Git author | Corrected to `KevMasMas <kevindavidrincon01@gmail.com>` |
| Workshop 1 implementation | Final technical review and clean reproduction passed: five qualified wind-record pairs, Q1-Q5 quality concerns plus Q6-Q7, 32 cells/zero errors, 59 lock pins, scoped artifact scan. Kevin communicated both students' approval in TEAM_APPROVAL.md. Platform submission/reference still unrecorded |
| Weather-source queries | NOAA 2024 archive retrieved; two empty NWS active polls plus a complete observed 238-alert recent pagination chain captured |
| Selected US region | Accepted: Oklahoma study area with counties as analytical regions (ADR 0001) |
| Architecture selection | Airflow/LocalExecutor, native capture lineage, canonical PostGIS and Silver Parquet executed; Gold remains planned (ADRs 0005/0006) |
| Temporal scope | Accepted: 2010-2025 complete-year baseline; rolling 24-hour current window; separate seven-day context (ADR 0003) |
| Compound Hazard Index formula | Accepted as the Workshop 1 preliminary five-component proposal; empirical validation remains for Workshop 4 |
| Pablo review | `PABLO_REVIEW.md` is historical and limited in scope; Kevin separately communicated both students' approval of the final Workshop 1 report/mapping/design in `TEAM_APPROVAL.md` |
| Workshops 2-4 planning | Workshop 2 five-year slice and artifacts prepared; Workshops 3-4 remain planning only |
| Workshop 2 foundation review | 29 passing tests; real schema/domain/revision/replay and two-source Airflow execution verified; wider station/county scope remains open |
| Workshop 2 delivery target | Kevin's Moodle checklist: Technical Architecture/Pipeline PDF, Pipeline Output Samples, GitHub link. G0-G6 targets two TaskFlow DAGs, exact-batch FileSensor, canonical DB and genuine JSON/Parquet evidence; planning does not establish execution |
| Specification conflict | Airflow and Bronze/Silver/Gold selected as the classroom workflow (ADR 0005); public-opinion/NLP/scraping wording and incompatible later-workshop details still require clarification |
| Immediate goal | Kevin/Pablo review PDF, samples and notebook; select local commit, push and upload manually. No final approval/upload claimed |

## Permanent ownership

The ownership split stays stable across the semester so each person can follow their sources from validation to the final dashboard.

| Person | Primary source ownership | System leadership | Reviewer responsibility |
| --- | --- | --- | --- |
| Kevin Rincon | NOAA Storm Events and NWS Alerts | Canonical database model, CLI integration, analytical views, index implementation, reproducibility gate | Review Pablo's GHCN and station work |
| Pablo Garzon | GHCN-Daily/NCEI and NWS station observations | Raw landing/orchestration, station-to-region processing, geographic aggregation, dashboard and presentation assembly | Review Kevin's Storm Events and alerts work |

Ownership means preparing the work and its evidence. It does not mean working alone: the other person must review it and be able to explain it during the individual defense.

## Shared decisions

Neither person may decide these alone:

- Exact US region and aggregation unit.
- Historical and current-condition time windows.
- Canonical event and domain tables.
- Cross-source matching rules.
- Compound Hazard Index components, weights, scale, and limitations.
- Architecture and scheduler selection.
- Final report claims and submission commit.

Record accepted decisions in `docs/decisions/` after both members approve them.

## What happens next

### Step 0 - close the foundation review

| ID | Task | Owner | Reviewer | Output |
| --- | --- | --- | --- | --- |
| F-01 | Read `PROJECT_CONTEXT.md` and confirm the academic requirements | Kevin | Pablo | Corrections or approval in the foundation change log |
| F-02 | Confirm the permanent ownership table above | Pablo | Kevin | Written approval or revised allocation |
| F-03 | Review repository structure and ignored files | Kevin | Pablo | Completed foundation review checklist |
| F-04 | Agree on the branch strategy after the initial empty repository | Both | Both | Recorded decision before starting implementation |

Do not start weather-source queries until Step 0 is reviewed by both members.

### Step 1 - start Workshop 1 in parallel

| ID | Task | Owner | Reviewer | Required output |
| --- | --- | --- | --- | --- |
| W1-K01 | Research NOAA Storm Events official documentation, access, license, fields, coverage, and revision behavior | Kevin | Pablo | Documentation notes and source-contract draft |
| W1-K02 | Research NWS Alerts official documentation, identifiers, geometry, update behavior, headers, and User-Agent rule | Kevin | Pablo | Documentation notes and incremental-contract draft |
| W1-P01 | Research GHCN-Daily/NCEI official documentation, access, license, fields, coverage, and update behavior | Pablo | Kevin | Documentation notes and source-contract draft |
| W1-P02 | Research NWS station-observation documentation, stations, units, timestamps, identifiers, and revisions | Pablo | Kevin | Documentation notes and incremental-contract draft |

Official documentation research comes before live requests.

### Step 2 - collect and profile evidence

| ID | Task | Owner | Reviewer | Required output |
| --- | --- | --- | --- | --- |
| W1-K03 | Capture an unmodified NOAA Storm Events sample and profile at least 200 records | Kevin | Pablo | Evidence entry, raw sample, profiling output |
| W1-K04 | Poll NWS Alerts twice at the required interval and profile at least 200 records or the full response | Kevin | Pablo | Two evidence entries and change comparison |
| W1-P03 | Capture an unmodified GHCN-Daily sample and profile at least 200 records | Pablo | Kevin | Evidence entry, raw sample, profiling output |
| W1-P04 | Poll NWS station observations twice and profile at least 200 records or the full response | Pablo | Kevin | Two evidence entries and change comparison |

Every observation must be indexed in `deliveries/01-workshop-1/EVIDENCE_REGISTER.md`. Large downloads remain outside Git.

### Step 3 - integrate the four sources

| ID | Task | Owner | Reviewer | Required output |
| --- | --- | --- | --- | --- |
| W1-S01 | Compare candidate US regions using coverage from all four sources | Both | Both | Accepted region decision record |
| W1-S02 | Consolidate field mappings, units, UTC, WGS84, duplicate keys, and raw references | Kevin drafts | Pablo reviews | Canonical mapping table |
| W1-S03 | Design regional entities, station/zone/county relationships, and geographic joins | Pablo drafts | Kevin reviews | First ER diagram and geographic rules |
| W1-S04 | Investigate five real data-quality problems and five candidate cross-source pairs | Both | Both | Evidence-backed examples; never fabricated |
| W1-S05 | Define historical partitions, watermarks, overlap windows, polling, and failure recovery | Each drafts own sources | Cross-review | Four accepted ingestion contracts |

### Step 4 - prepare the delivery

| ID | Task | Owner | Reviewer | Required output |
| --- | --- | --- | --- | --- |
| W1-D01 | Draft functional user, six MoSCoW user stories, risks, exclusions, and limitations | Pablo | Kevin | Project-definition sections |
| W1-D02 | Draft preliminary Compound Hazard Index inputs, scale, and historical validation approach | Kevin | Pablo | Clearly labeled proposal, not a validated result |
| W1-D03 | Assemble the architecture diagram and requirement-to-evidence matrix | Kevin | Pablo | Reviewed diagram and traceability table |
| W1-D04 | Assemble the English report and verify citations | Pablo | Kevin | Report source ready for PDF generation |
| W1-D05 | Run the notebook from top to bottom and review all artifacts from a clean clone | Both | Both | Submission checklist and recorded commit hash |

## Milestone queue

Workshop 2 is active at the compatible offline core by user instruction. The
specification conflict and Workshop 1 acceptance caveat remain recorded; neither
is silently treated as resolved. Workshops 3-4 remain planning only.

| Gate/ID | Planned next action | Owner | Reviewer | Start condition |
| --- | --- | --- | --- | --- |
| XW-01 | Send the Workshop 2-4 specification-conflict questions to the professor and record the response | Both | Both | Can happen now |
| W2-00 | Execute delivery-first plan G0-G6 and finalize runtime architecture details | Kevin drafts | Pablo | Workshop 1 review recorded; compatible technical path explicitly selected, no professor clarification inferred |
| W2-K | Implement NOAA historical adapter, canonical DB/migrations and CLI | Kevin | Pablo | W2-00 accepted |
| W2-P | Implement GHCN historical adapter, raw landing and orchestration | Pablo | Kevin | W2-00 accepted |
| W3-K | Implement NWS Alerts polling, change detection and event grouping | Kevin | Pablo | Workshop 2 accepted |
| W3-P | Implement station polling, state/overlap and scheduling | Pablo | Kevin | Workshop 2 accepted |
| W4-K | Implement historical/current analytical views and CHI | Kevin | Pablo | Workshop 3 accepted |
| W4-P | Implement county/data-health presentation and Dash application | Pablo | Kevin | Workshop 3 accepted |

Detailed P0/P1/out-of-scope tasks, evidence gates and acceptance criteria are in
the corresponding proposed delivery plans. This table is the operational order.

## Semester ownership after Workshop 1

| Milestone | Kevin | Pablo | Shared gate |
| --- | --- | --- | --- |
| Workshop 2 | NOAA historical adapter; canonical DB, migrations, and CLI | GHCN historical adapter; raw landing and orchestration | Validation, quarantine, idempotency, clean historical rerun |
| Workshop 3 | NWS Alerts polling, change hashes, and source status | Station polling, scheduling, and watermark operations | Event matching, retries, failure recovery, integration tests |
| Workshop 4 | Compound Hazard Index calculation and analytical views | Geographic aggregation and Plotly Dash experience | Sensitivity analysis, limitations, and data-health panel |
| Final | Reproducibility audit, automated quality gate, release checklist | Final report, presentation assets, and demo coordination | Fresh-clone rehearsal and individual defense preparation |

## How each person works

1. Create a short-lived branch from the agreed base: `docs/...`, `feat/...`, `fix/...`, or `test/...`.
2. Work only on assigned task IDs and coordinate before editing shared files.
3. Add a dated entry to the active delivery `CHANGE_LOG.md`.
4. Record exact verification results and evidence paths; do not write only "works."
5. Ask the other member for review.
6. Merge only after review, evidence, and applicable checks pass.

## Definition of done

A task is done only when:

- its requirement and task ID are identified;
- its output is stored in the correct folder;
- evidence or tests are recorded with exact results;
- limitations and unresolved questions are explicit;
- the reviewer can explain the work;
- the change log and work board reflect the real state;
- no secrets or bulk raw data are tracked.

## Where information belongs

| Information | Location |
| --- | --- |
| What to do now and who owns it | `WORK_BOARD.md` |
| Stable project requirements and constraints | `PROJECT_CONTEXT.md` |
| Detailed current-delivery requirements and acceptance criteria | `deliveries/<delivery>/IMPLEMENTATION_PLAN.md` |
| Work actually performed and verification results | `deliveries/<delivery>/CHANGE_LOG.md` |
| Raw-evidence index | `deliveries/<delivery>/EVIDENCE_REGISTER.md` |
| Semester sequence | `docs/plans/semester-roadmap.md` |
| Accepted architecture/data decisions | `docs/decisions/` |
| Academic and workflow research | `docs/reports/` |

If responsibility or current status appears elsewhere and conflicts with this board, update the board and the relevant delivery log together.
