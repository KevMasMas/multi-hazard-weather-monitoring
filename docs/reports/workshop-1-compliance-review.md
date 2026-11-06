# Workshop 1 Compliance Review

- **Review date:** 2026-11-05
- **Authoritative inputs:** `CourseProject.pdf`, `TeamsDistribution.pdf`, and `Workshop_1.pdf`
- **Repository branch:** `workflow-1`
- **Conclusion:** evidence and report draft substantially closed for Workshop 1; final PDF and independent source cross-review remain outstanding

## Executive assessment

The repository now follows the professor's required Workshop 1 layout and keeps
future implementation clearly separated. The executed notebook, four-source
samples, mapping, ER model, architecture overview, configuration draft and CLI
stub are present. The report source now includes record-level quality examples, a rubric traceability matrix, source-qualified hazard measures, and four draft source contracts. Remaining gates are final mutual review, exact multi-year regional volume/coverage evidence, a clean notebook rerun in the locked environment, and the final English PDF.

## Requirement matrix

| Professor requirement | Status | Repository evidence | Remaining gate |
| --- | --- | --- | --- |
| Define the compound-weather problem, region, historical window and current situation | Draft present | `REPORT_DRAFT.md` Sections 2-4; ADRs 0001-0004 | Kevin cross-review of report claims; retain source-qualified severity units. |
| Two historical and two periodically updated sources | Present with scope limits | Evidence register and samples for NOAA, GHCN, NWS Alerts and NWS observations | Statewide GHCN/station coverage and exact multi-year volume remain unmeasured; source-specific attribution caveats are in report. |
| Real unmodified responses retained as evidence | Present with documented qualifications | `workshop_1/samples/`; evidence register; local ignored raw landing | Repeat evidence/secret audit before submission; acquisition and partition instructions now exist. |
| At least 200 records per source, or full source if smaller | Present | NOAA 250; GHCN 365; NWS Alerts 238 recent records plus two active polls; KOKC 200-feature pages | Reviewer must confirm the registered evidence and scope caveats. |
| Profile nulls, ranges, duplicates, time, coordinates and units | Present in executed notebook | `notebooks/01_source_profiling.ipynb`; source notes and report | Final cross-review; sample findings must not be generalized to statewide coverage. |
| Five concrete data-quality problems with example records | Present, evidence-qualified | `REPORT_DRAFT.md` Section 5 Q-01 to Q-05 and referenced raw samples | Kevin to cross-review; examples include source limitations/revision behavior and are not all provider defects. |
| Five candidate cross-source pairs | Present | `workshop_1/samples/candidate_pairs/` and notebook | Keep them labeled unconfirmed unless stronger evidence is found. |
| Canonical mapping and domain tables | Draft present | `workshop_1/mapping.md`; conceptual ER model | Final field-level team review and close listed open rules. |
| Historical and incremental contracts per source | Draft present for all four | `REPORT_DRAFT.md` Section 7, source notes and `config/sources.yaml` | Proposed schedules/overlaps and rough volume screens need mutual review; implementation remains later work. |
| Functional user and at least six MoSCoW stories | Draft present | `REPORT_DRAFT.md` | Final wording and report review. |
| Preliminary indicator and historical validation approach | Draft accepted for Workshop 1 | ADR 0002 and report draft | Preserve as preliminary; empirical validation belongs to Workshop 4. |
| At least five risks and mitigations | Draft present | `REPORT_DRAFT.md` | Citation and final review only. |
| Labeled high-level architecture | Present | `docs/architecture/workshop-1-overview.md` | Final report embedding/render review. |
| Required repository structure | Present | `src/`, `ingest.py`, `config/`, `data/raw/`, `sql/`, `dashboard/`, `tests/`, `notebooks/`, `docs/`, `workshop_1/`, `.env.example`, `.gitignore`, `README.md` | Do not mistake scaffolding for later-workshop implementation. |
| Executed source-profile notebook with outputs | Present | 52 cells; 29/29 code cells executed; zero error outputs | Final teammate review after any report-driven edits. |
| Single English PDF report | Missing | English `REPORT_DRAFT.md` exists | Complete, render, visually inspect and submit the PDF. |
| Citations, attribution and no secrets | Mostly documented; final audit pending | Official primary-source references, source-specific caveats and `.env.example` | NOAA evidence did not identify a separate dataset license; rerun full attribution/secret audit before submission. |

## Required structure now present

```text
config/sources.yaml
dashboard/README.md
data/raw/.gitkeep
docs/architecture/
docs/sources/SOURCE_STATUS.md
ingest.py
notebooks/01_source_profiling.ipynb
sql/README.md
src/multi_hazard_weather_monitoring/
tests/fixtures/README.md
workshop_1/mapping.md
workshop_1/samples/
```

## Immediate ownership

### Kevin

1. Cross-review the NOAA/Alerts proposals and citations. Their hourly/partition contracts and rough volume screen are documented; exact multi-year totals and a separately stated NOAA license remain unverified.
2. Cross-review the new quality records, volume screens, contract proposals, traceability matrix, and final report claims.
3. Review the final canonical mapping and report claims against the notebook.

### Pablo

1. Cross-review the GHCN and station-observation profile/contract additions; full regional station inventory and multi-year coverage are still unmeasured.
2. Review the exact GHCN/station quality example rows and report traceability.
3. Coordinate final report source review before PDF export.

### Both

1. Cross-review the five concrete quality examples with exact source references.
2. Review the four-source mapping, draft ingestion contracts and architecture.
3. When authorized, produce and inspect the PDF; rerun the notebook in the locked environment, audit secrets/artifacts and record the submission commit.

## Explicitly not required yet

Workshop 1 does not require implemented Docker services, PostgreSQL migrations,
historical or incremental adapters, Airflow scheduling, automated production
tests, CHI computation or a working dashboard. Their directories are scaffolds
for later workshops and must not be presented as completed functionality.
