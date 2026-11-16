# Workshop 1 Compliance Review

- **Review date:** 2026-11-16 (supersedes the 2026-11-05 status)
- **Authoritative inputs:** `CourseProject.pdf`, `TeamsDistribution.pdf`, and `Workshop_1.pdf`
- **Repository branch:** `workflow-1`
- **Conclusion:** PDF exists and six quality claims/eight daily comparison rows are reproducible. Same-event rubric interpretation and current student/submission review remain open; no blanket compliance or approval is claimed.

## Executive assessment

The repository now follows the professor's required Workshop 1 layout and keeps
future implementation clearly separated. The executed notebook, four-source
samples, mapping, ER model, architecture overview, configuration draft and CLI
stub are present. The thirteen-page PDF and Overleaf package exist. The active
report source is `workshop_1/report/content.tex`; `REPORT_DRAFT.md` is superseded.
The acceptance plan separates artifacts, numerical verification and review.
Actual historical loading/statewide inventory belong to later implementation;
sample-derived volume screens remain qualified estimates in Workshop 1.

## Requirement matrix

| Professor requirement | Status | Repository evidence | Remaining gate |
| --- | --- | --- | --- |
| Define the compound-weather problem, region, historical window and current situation | Present | Report section 1; ADRs 0001-0004 | Current student content review; retain source-qualified units. |
| Two historical and two periodically updated sources | Present with scope limits | Evidence register and samples for NOAA, GHCN, NWS Alerts and NWS observations | Statewide GHCN/station coverage and exact multi-year volume remain unmeasured; source-specific attribution caveats are in report. |
| Real unmodified responses retained as evidence | Present with documented qualifications | `workshop_1/samples/`; evidence register; local ignored raw landing | Repeat evidence/secret audit before submission; acquisition and partition instructions now exist. |
| At least 200 records per source, or full source if smaller | Present | NOAA 250; GHCN 365; NWS Alerts 238 recent records plus two active polls; KOKC 200-feature pages | Reviewer must confirm the registered evidence and scope caveats. |
| Profile nulls, ranges, duplicates, time, coordinates and units | Present in executed notebook | `notebooks/01_source_profiling.ipynb`; source notes and report | Final cross-review; sample findings must not be generalized to statewide coverage. |
| Five concrete data-quality problems with example records | Q1-Q5 proposed, Q6 additional; six source claims verified | Report section 4.1; offline audit JSON | Five integration concerns have records and handling proposals. They are not five proved provider errors; cadence/optional-field interpretations remain qualified. |
| Five candidate same-real-world-event record pairs | Numerical/provenance part verified; semantic acceptance open | Report section 4.2; eight daily CSV rows; audit JSON | Four dates times two elements; NWS side is a derived aggregate. Assumed daily boundaries and unverified station equivalence prevent an unconditional same-event compliance claim. No independent-event count inferred. |
| Canonical mapping and domain tables | Draft present | `workshop_1/mapping.md`; conceptual ER model | Final field-level team review and close listed open rules. |
| Historical and incremental contracts per source | Proposals present for all four | Report section 6, source notes and `config/sources.yaml` | Current team review of proposed schedules/overlaps; implementation remains later work. |
| Functional user and at least six MoSCoW stories | Six present | Report section 2 | Current wording review; no stakeholder interview claimed. |
| Preliminary indicator and historical validation approach | Proposal present; earlier scoped decision recorded | Report section 7; ADR 0002 | No validated weights, thresholds or prediction accuracy claimed. |
| At least five risks and mitigations | Seven present | Report section 9 | Current content/citation review. |
| Labeled high-level architecture | Present, embedded and visually inspected | Report section 8; Mermaid; ADR 0005 | Airflow/layers selected at Kevin's request; no new Pablo approval or running service inferred. |
| Required repository structure | Present | `src/`, `ingest.py`, `config/`, `data/raw/`, `sql/`, `dashboard/`, `tests/`, `notebooks/`, `docs/`, `workshop_1/`, `.env.example`, `.gitignore`, `README.md` | Do not mistake scaffolding for later-workshop implementation. |
| Executed source-profile notebook with outputs | Present | 31/31 code cells executed, zero stored errors | Fresh-clone locked setup and current teammate review remain separate gates. |
| Single English PDF report | Generated and visually inspected | `workshop_1/report/Workshop_1_Report.pdf`, thirteen pages; portable ZIP | Student content review and actual platform upload not recorded. |
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

## Evidence checks and interpretation

`scripts/workshop_1/audit_submission_evidence.py` runs offline. It verifies nine
captured-file hashes, asserts the six quality-record claims, reproduces the eight
rows against the saved CSV and checks their provenance/difference fields.
`submission_evidence_audit.json` records results, input hashes and limitations.

Workshop 1 page 3 requires five concrete data-quality problems with record
examples and five candidate pairs believed to describe the same real-world event.
It does not require proof of eight independent events. Conversely, eight rows
alone do not establish that its same-event condition is met.

| Example | Verified evidence and proposed problem | Interpretation limit |
| --- | --- | --- |
| Q1 | PRCP 0.0 with `T,,W,2400`, 2025-01-05: trace flag affects meaning. | Not a corrupt numeric reading; preserve flags. |
| Q2 | NOAA 1155350: missing begin coordinates for zone-based Heavy Snow. | Zone exists; no fabricated point or assertion of absent geography. |
| Q3 | Wind Advisory: null polygon but seven affected-zone URLs. | Alternative geography is present; do not label it locationless. |
| Q4 | Same KDEN ID changes from null/QC Z to 4.4 degC/QC V. | Cause and provider-wide revision guarantee are unknown. |
| Q5 | Adjacent returned KOKC observations are 63 minutes apart. | Observed sampling gap, not proof of a broken five-minute promise or lost record. |
| Q6 | Optional 24-hour extrema are null in the cited KOKC record. | Additional availability example, not zero or necessarily a defect. |

The daily comparison's required difference categories are present: daily versus
instantaneous timing (no invented exact GHCN event time), saved station points,
values/deltas in degC, and distinct source/derived identifiers with raw extreme
observation IDs. The 48-reading/70-minute screen is a proposed sampling rule,
not an official completeness guarantee. The guide's same-event interpretation
therefore remains an explicit review item; a stronger saved-evidence association
or professor clarification may be needed. No additional weather request was made.

## Remaining review actions (ownership stays in WORK_BOARD.md)

### Kevin

1. Cross-review the NOAA/Alerts proposals and citations. Their hourly/partition contracts and rough volume screen are documented; exact multi-year totals and a separately stated NOAA license remain unverified.
2. Cross-review the new quality records, volume screens, contract proposals, traceability matrix, and final report claims.
3. Review the final canonical mapping and report claims against the notebook.

### Pablo

1. Cross-review the GHCN and station-observation profile/contract additions; full regional station inventory and multi-year coverage are still unmeasured.
2. Review the exact GHCN/station quality example rows and report traceability.
3. Review the existing PDF; its export is already complete.

### Both

1. Cross-review the five concrete quality examples with exact source references.
2. Review the four-source mapping, draft ingestion contracts and architecture.
3. Review the generated PDF, reproduce the locked environment, audit secrets/artifacts and record the actual submission reference. Earlier workstream decisions do not approve the new daily comparisons or revised report.

## Explicitly not required yet

Workshop 1 does not require implemented Docker services, PostgreSQL migrations,
historical or incremental adapters, Airflow scheduling, automated production
tests, CHI computation or a working dashboard. Their directories are scaffolds
for later workshops and must not be presented as completed functionality.
