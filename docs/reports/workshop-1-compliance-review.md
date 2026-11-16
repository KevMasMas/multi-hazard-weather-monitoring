# Workshop 1 Compliance Review

- **Review date:** 2026-11-16 (supersedes the 2026-11-05 status)
- **Authoritative inputs:** `CourseProject.pdf`, `TeamsDistribution.pdf`, and `Workshop_1.pdf`
- **Repository branch:** `workflow-1`
- **Conclusion:** technical review completed with five qualified historical wind pairs, five primary quality concerns, clean locked execution and scoped artifact scan. Kevin explicitly communicated both students' approval in `TEAM_APPROVAL.md`; professor acceptance and platform submission are not inferred.

## Executive assessment

The repository now follows the professor's required Workshop 1 layout and keeps
future implementation clearly separated. The executed notebook, four-source
samples, mapping, ER model, architecture overview, configuration draft and CLI
stub are present. The fourteen-page PDF and Overleaf package exist. The active
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
| Five concrete data-quality problems with example records | Technical review accepts Q1-Q5; Q6-Q7 additional; seven claims asserted | Report section 4.1; audit JSON | Valid engineering integration/quality concerns, not five provider errors. Q5 is QC S versus selected V, not a claim of invalid data. |
| Five candidate same-real-world-event record pairs | Five primary wind candidates technically reviewed with qualifications | Report section 4.2; historical wind CSV; audit JSON | Five distinct Storm IDs explicitly name KOKC, paired with three original daily GHCN records for that airport/date. Multiple pairs can share an episode and station lineage. No exact peak timestamp or professor acceptance inferred. |
| Canonical mapping and domain tables | Draft present | `workshop_1/mapping.md`; conceptual ER model | Final field-level team review and close listed open rules. |
| Historical and incremental contracts per source | Proposals present for all four | Report section 6, source notes and `config/sources.yaml` | Current team review of proposed schedules/overlaps; implementation remains later work. |
| Functional user and at least six MoSCoW stories | Six present | Report section 2 | Current wording review; no stakeholder interview claimed. |
| Preliminary indicator and historical validation approach | Proposal present; earlier scoped decision recorded | Report section 7; ADR 0002 | No validated weights, thresholds or prediction accuracy claimed. |
| At least five risks and mitigations | Seven present | Report section 9 | Current content/citation review. |
| Labeled high-level architecture | Present, embedded and visually inspected | Report section 8; Mermaid; ADR 0005 | Airflow/layers selected at Kevin's request; no new Pablo approval or running service inferred. |
| Required repository structure | Present | `src/`, `ingest.py`, `config/`, `data/raw/`, `sql/`, `dashboard/`, `tests/`, `notebooks/`, `docs/`, `workshop_1/`, `.env.example`, `.gitignore`, `README.md` | Do not mistake scaffolding for later-workshop implementation. |
| Executed source-profile notebook with outputs | Fresh-clone locked execution passed | 59 exact pins, isolated kernel, 32/32 code cells, zero errors; JSON receipt | Current personal teammate review remains separate. NOAA Git newline defect fixed and clean run repeated. |
| Single English PDF report | Generated, visually inspected and team approval recorded | `workshop_1/report/Workshop_1_Report.pdf`, fourteen pages; portable ZIP; `TEAM_APPROVAL.md` | Actual platform upload/professor acceptance not recorded. |
| Citations, attribution and no secrets | Technical attribution review and bounded current-tree/ZIP scan passed | Official references, documented license unknowns and `final_artifact_audit.json` | No universal absence-of-secrets or remote-history guarantee; professor/platform acceptance not inferred. |

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
prior captured-file hashes, asserts seven quality-record claims, reproduces five
primary wind candidates and eight supplemental daily rows, and checks provenance/differences.
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
| Q5 | KOKC 2026-10-31T20:52Z temperature 16.7 degC has QC S, not selected V. | Preserve value/QC; V-only selection does not prove S invalid. |
| Q6 | Optional 24-hour extrema are null in the cited KOKC record. | Additional availability example, not zero or necessarily a defect. |
| Q7 | Adjacent returned KOKC observations are 63 minutes apart. | Extra sampling observation, not proof of a broken cadence promise or lost record. |

The supplementary daily comparison's difference categories are present: daily versus
instantaneous timing (no invented exact GHCN event time), saved station points,
values/deltas in degC, and distinct source/derived identifiers with raw extreme
observation IDs. The 48-reading/70-minute screen is a proposed sampling rule,
not an official completeness guarantee. The guide's same-event interpretation
is not claimed for those eight rows. The new five primary wind candidates use
explicit Storm Events airport narratives and the newly captured original GHCN
wind summaries instead. One bounded announced GHCN request was made; no NWS
request or NOAA redownload. The technical review considers these candidate
examples defensible with date/peak-time and shared-lineage limitations preserved.

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
3. Team content approval is now explicitly recorded in `TEAM_APPROVAL.md`; select the final delivery reference and upload. Locked clean execution and scoped artifact checks are separate evidence, not inferred personal approval.

## Explicitly not required yet

Workshop 1 does not require implemented Docker services, PostgreSQL migrations,
historical or incremental adapters, Airflow scheduling, automated production
tests, CHI computation or a working dashboard. Their directories are scaffolds
for later workshops and must not be presented as completed functionality.
