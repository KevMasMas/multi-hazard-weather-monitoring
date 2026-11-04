# Team Work Board

This is the single operational entry point for Team 9. Read this file to know the current state, who owns each workstream, and what must happen next.

## Current state

| Item | State |
| --- | --- |
| Repository foundation | Committed and pushed as `602143d` on `workflow-1` |
| Git author | Corrected to `KevMasMas <kevindavidrincon01@gmail.com>` |
| Workshop 1 implementation | Not started |
| Weather-source queries | None performed |
| Selected US region | Undecided; must be supported by evidence |
| Compound Hazard Index formula | Undecided; only a preliminary proposal belongs in Workshop 1 |
| Immediate goal | Review the foundation together, then start Workshop 1 source validation |

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
