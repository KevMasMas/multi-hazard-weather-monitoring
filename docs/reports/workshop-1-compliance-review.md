# Workshop 1 Compliance Review

- **Review date:** 2026-11-05
- **Authoritative inputs:** `CourseProject.pdf`, `TeamsDistribution.pdf`, and `Workshop_1.pdf`
- **Repository branch:** `workflow-1`
- **Conclusion:** structurally aligned, not yet submission-ready

## Executive assessment

The repository now follows the professor's required Workshop 1 layout and keeps
future implementation clearly separated. The executed notebook, four-source
samples, mapping, ER model, architecture overview, configuration draft and CLI
stub are present. Remaining gaps are mainly evidence closure and the final English
report, not folder organization.

## Requirement matrix

| Professor requirement | Status | Repository evidence | Remaining gate |
| --- | --- | --- | --- |
| Define the compound-weather problem, region, historical window and current situation | Partial | `REPORT_DRAFT.md`; ADRs 0001-0004 | Expand the physical/severity explanation and finish citations. |
| Two historical and two periodically updated sources | Present | Evidence register and samples for NOAA, GHCN, NWS Alerts and NWS observations | Close source-level license, volume and update-policy gaps. |
| Real unmodified responses retained as evidence | Present with documented qualifications | `workshop_1/samples/`; evidence register; local ignored raw landing | Final evidence audit and download instructions for large files. |
| At least 200 records per source, or full source if smaller | Present | NOAA 250; GHCN 365; NWS Alerts 238 recent records plus two active polls; KOKC 200-feature pages | Reviewer must confirm the registered evidence and scope caveats. |
| Profile nulls, ranges, duplicates, time, coordinates and units | Partial | Executed `notebooks/01_source_profiling.ipynb` | Convert every required dimension into an explicit four-source checklist/table. |
| Five concrete data-quality problems with example records | Partial | Notebook and report list observed candidates | Add exact source record/raw references for five defensible examples and distinguish semantics from defects. |
| Five candidate cross-source pairs | Present | `workshop_1/samples/candidate_pairs/` and notebook | Keep them labeled unconfirmed unless stronger evidence is found. |
| Canonical mapping and domain tables | Draft present | `workshop_1/mapping.md`; conceptual ER model | Final field-level team review and close listed open rules. |
| Historical and incremental contracts per source | Partial | Source notes, report draft and `config/sources.yaml` | Finalize partition volume, polling cadence, overlap window, duplicate key and halfway-failure recovery for all four sources. |
| Functional user and at least six MoSCoW stories | Draft present | `REPORT_DRAFT.md` | Final wording and report review. |
| Preliminary indicator and historical validation approach | Draft accepted for Workshop 1 | ADR 0002 and report draft | Preserve as preliminary; empirical validation belongs to Workshop 4. |
| At least five risks and mitigations | Draft present | `REPORT_DRAFT.md` | Citation and final review only. |
| Labeled high-level architecture | Present | `docs/architecture/workshop-1-overview.md` | Final report embedding/render review. |
| Required repository structure | Present | `src/`, `ingest.py`, `config/`, `data/raw/`, `sql/`, `dashboard/`, `tests/`, `notebooks/`, `docs/`, `workshop_1/`, `.env.example`, `.gitignore`, `README.md` | Do not mistake scaffolding for later-workshop implementation. |
| Executed source-profile notebook with outputs | Present | 52 cells; 29/29 code cells executed; zero error outputs | Final teammate review after any report-driven edits. |
| Single English PDF report | Missing | English `REPORT_DRAFT.md` exists | Complete, render, visually inspect and submit the PDF. |
| Citations, attribution and no secrets | Partial | Official links and `.env.example`; no credentials intentionally stored | Run final license/citation and secret audit. |

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

1. Close NOAA Storm Events and NWS Alerts contract gaps: license/attribution,
   estimated historical volume, final partition/poll/overlap proposal, duplicate
   key and failure recovery.
2. Build the requirement-to-evidence matrix used by the final report.
3. Review the final canonical mapping and report claims against the notebook.

### Pablo

1. Close GHCN and station-observation contract gaps: regional coverage method,
   license/attribution, revision behavior, pagination/retention and proposed
   polling/overlap values.
2. Add exact references for the GHCN/station quality examples.
3. Assemble and review the final English report source.

### Both

1. Approve five concrete quality examples with exact source references.
2. Review the four-source mapping, ingestion contracts and architecture.
3. Produce and inspect the PDF, run the notebook from top to bottom, audit
   secrets/artifacts and record the submission commit.

## Explicitly not required yet

Workshop 1 does not require implemented Docker services, PostgreSQL migrations,
historical or incremental adapters, Airflow scheduling, automated production
tests, CHI computation or a working dashboard. Their directories are scaffolds
for later workshops and must not be presented as completed functionality.
