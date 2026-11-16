# Implementation Plan - Workshop 1

- **Team:** Team 9 - Pablo Garzon and Kevin Rincon
- **Target date:** Moodle notice supplied by Kevin: 2026-11-16, 12:00-15:15 America/Bogota; no upload is recorded
- **Working branch:** `workflow-1`
- **Base branch/commit:** project foundation commit `602143d`
- **Status:** thirteen-page PDF generated and visually inspected; four-source profiles and six quality examples present; eight reproducible daily comparisons over four days. Same-event interpretation, current student review, clean-environment reproduction and submission recording remain open. See acceptance matrix below.
- **Official specification:** `Workshop_1.pdf`

## 1. Requirement interpretation

Workshop 1 is an evidence-producing source-validation and data-contract milestone. Reading documentation is insufficient: all four assigned sources must be queried for real when this workshop is authorized, their unmodified responses preserved, and factual conclusions tied to evidence.

### Pablo workstream preparation (2026-11-03)

The desk review, qualifying GHCN-Daily samples, KDEN/KOKC station polls, profiles, mappings, and source-specific contracts are recorded in the research note and evidence register. Oklahoma/counties and the 2010-2025/24-hour temporal scope are accepted in ADRs 0001 and 0003. ADR 0004 accepts Pablo's station/geographic rule while keeping the full statewide inventory as later implementation work. Pablo's review is recorded in `PABLO_REVIEW.md`.

## 2. Non-negotiable objective

Prove that a justified US regional scope can be supported by NOAA Storm Events, GHCN-Daily/NCEI, NWS Alerts, and NWS station observations, then define a coherent canonical contract for later implementation.

## 3. Minimum demonstrable result

1. Four source samples and profiles that satisfy the professor's evidence threshold.
2. A justified region/time scope covered by all four sources.
3. A field-to-canonical mapping and first ER diagram.
4. Historical and incremental ingestion contracts with failure-recovery reasoning.
5. A project definition with functional user, prioritized stories, preliminary index, risks, limitations, and architecture.
6. A complete English report and reproducible executed notebook.

## 4. Non-negotiable principles

- Use official source documentation and free/open access.
- Respect terms, rate limits, caching, and the NWS User-Agent requirement.
- Preserve raw samples unmodified and never commit secrets or bulk archives.
- Profile at least 200 records per source, or the complete source if smaller.
- Do not manufacture five quality issues or five matching pairs; report honestly if candidate overlap cannot be established and escalate the requirement.
- Separate observed source behavior from proposed ingestion behavior.
- Do not present the preliminary index as validated prediction.

## 5. Prioritized scope

### P0 - professor-required

#### Hazard and scope

- [x] Explain compound weather hazards, source-specific severity measures/units, and monitoring value (2026-11-05 report update; source severity remains non-comparable by design).
- [x] Compare Oklahoma and Denver/Colorado using all-four-source coverage and manageable volume; Pablo review and accepted Oklahoma scope are recorded in ADR 0001 and PABLO_REVIEW.md.
- [x] Select and justify Oklahoma/counties, the 2010-2025 complete-year baseline, rolling 24-hour current window, and separate seven-day operational context (ADRs 0001 and 0003; 2026-11-05 review entry).
- [x] Draft the preliminary Compound Hazard Index components, formula, missingness policy, and validation plan (see 2026-11-05 W1-D02 change-log entry); [ ] obtain Pablo review and accept final parameters later.

#### Historical sources

- [x] Profile NOAA Storm Events sample and document access, fields, observed coverage, identifier, archive revisions, citation/attribution caveat, and yearly partition proposal (2026-11-05; one-year screen only, exact license not identified).
- [x] Capture/profile qualifying GHCN-Daily sample; document station-year volume screen, key/partition proposal, NCEI update/citation/liability statements (2026-11-05); statewide station coverage and Kevin cross-review remain open.
- [x] Preserve unmodified samples and record explicitly labeled volume screens (2026-11-05); complete regional station inventory and measured multi-year totals remain open and are not inferred from the pilot.

#### Incremental sources

- [x] Document NWS Alerts access, fields, geometry, IDs, timestamps, User-Agent, two-poll result and recent-alert profile; alert-level changes were not observable because both active polls were empty.
- [x] Capture and compare two qualifying NWS station-observation pages at least one hour apart for KDEN and for the preferred KOKC common region (see 2026-11-04 and 2026-11-05 change-log entries); [ ] complete multi-station/provider coverage and service-wide revision-policy review.
- [x] Poll both incremental sources twice at least one hour apart and record exact bounded-response differences; the empty active-alert polls cannot validate alert-level change semantics.

#### Profiling and data quality

- [x] Current notebook executed 31/31 code cells without errors using the existing virtual environment after the overlap changes; [x] Pablo's earlier workstream review is recorded; [ ] Kevin cross-review of current edits and fresh-clone lock reproduction.
- [x] Report source-profile dimensions in executed notebook outputs for the four qualifying samples; note sample limitations and distinguish station-page behavior from source-wide policy.
- [x] Verify six quality/integration/availability observations against saved records (report section 4.1, Q1-Q6; `submission_evidence_audit.json`). Q1-Q5 are the five proposed problems; Q6 is additional. They are not six proven provider defects; final interpretation remains subject to review.
- [x] Eight GHCN/KOKC daily temperature candidate records are reproduced from cached evidence on four eligible days after the authorized GHCN follow-up; five intra-NWS examples remain excluded. [ ] Both students to review daily-boundary/station-equivalence assumptions and the interpretation of multiple elements per day. See the latest change-log entry.

#### Contracts and project definition

- [x] Draft the four-source canonical field mapping and Team 9 domain tables in `workshop_1/mapping.md`; [ ] complete final field-level team review.
- [x] Draft UTC, WGS84, unit/severity, duplicate-key, and raw-reference/content-hash rules in the mapping and ADRs; [ ] close the explicitly listed open field-level decisions.
- [x] Draft four source-specific partition/pagination, key, poll/overlap, watermark/checkpoint and interrupted-run recovery contracts in REPORT_DRAFT.md Section 7 and mirror them in config; proposed schedules remain pending mutual review and implementation.
- [x] Current report section 2 contains the proposed functional user and six MoSCoW stories; [ ] review current wording. No stakeholder interview or professor approval is recorded.
- [x] Draft and jointly review index inputs/rule/scale/validation approach without claiming empirical validation (ADR 0002 and `PABLO_REVIEW.md`).
- [x] Current report section 9 contains seven risks with mitigations; earlier workstream integration review is recorded in `PABLO_REVIEW.md`, not approval of all later edits.
- [x] Produce the conceptual ER diagram, labeled architecture overview, independent mapping table and visually inspected English PDF; [ ] complete current student content/submission review.
- [x] Revise the unsubmitted architecture to select Apache Airflow and explicitly map Bronze native captures, Silver canonical storage/Parquet and planned Gold outputs (ADR 0005; 2026-11-16 architecture correction log). This does not implement Workshop 2.

### P1 - quality improvements after P0

- [ ] Automate a source-profile summary table from the notebook outputs.
- [x] Current requirement-to-evidence matrix is in `docs/reports/workshop-1-compliance-review.md`; report section 10 indexes submission artifacts. The legacy draft is not the current submission source.
- [ ] Add schema-drift snapshots or checks only if supported by actual source evidence.

### Out of scope

- Production historical or incremental ingestion.
- Database/Docker/Airflow implementation.
- Final Compound Hazard Index implementation or dashboard.
- Claims that the selected sources predict hazards.

## 6. Work allocation

`WORK_BOARD.md` is the only current assignment board. The Workshop 1 split is:

| Owner | Sources | Primary deliverables | Reviewer |
| --- | --- | --- | --- |
| Kevin | NOAA Storm Events; NWS Alerts | Documentation research, evidence, profiles, mappings, duplicate keys, ingestion contracts, alert/event correlation constraints | Pablo |
| Pablo | GHCN-Daily/NCEI; NWS station observations | Documentation research, evidence, profiles, mappings, duplicate keys, ingestion contracts, station/region and historical-baseline constraints | Kevin |
| Both | Cross-source integration | Region, time windows, canonical model, ER diagram, matching candidates, functional user, stories, index proposal, risks, architecture, notebook and report | Mutual approval |

Use the Workshop 1 task IDs listed under Steps 1-4 of `WORK_BOARD.md` in branches, change-log entries, reviews, and commits.

## 7. Dependencies and handoffs

- Foundation delivery accepted before creating the workshop branch.
- Official documentation review precedes live source access.
- Source evidence precedes scope and contract acceptance.
- Individual source mappings are handed to the shared model review.
- Shared decisions require both students' approval and, where necessary, professor confirmation.

## 8. Acceptance criteria

`Present` means an artifact exists; `verified` means the named check ran.
Neither means student/professor approval or a guaranteed rubric score. A checked
drafting task above is not blanket acceptance of this milestone.

| ID | Criterion and current evidence | Verification / remaining gate |
| --- | --- | --- |
| A01 | Four qualifying profiles: NOAA 250 rows, GHCN 365, recent NWS Alerts 238, KOKC 200 per poll; notebook includes nulls, ranges, IDs, time, geography and units. | Counts and stored execution checked; small/empty captures are additional evidence, not substitutes. Statewide completeness is not proved. |
| A02 | Five proposed concrete problems Q1-Q5 and extra Q6 have exact saved-record evidence and handling rules. | Offline audit verifies all six claims. These are integration/semantic/availability/revision concerns, not six established source errors. Review the five-problem interpretation; do not infer provider faults or a missing-observation cause. |
| A03 | Eight daily GHCN/KOKC comparisons reproduce with time, position, magnitude/unit and identifier differences. | Numerical/count/provenance checks pass: four days, TMAX/TMIN each. **Same-real-world-event interpretation remains open**: KOKC side is a derived aggregate, daily boundary assumed, station equivalence unverified. Eight rows are not eight independent events. Escalation alone does not satisfy this criterion. |
| A04 | Mapping, core/domain ERs and source configuration cover all four sources. | Artifacts present; current field-level team review pending. Production SQL/crosswalk implementation is later work. |
| A05 | Four historical/incremental contract proposals include keys, partitions/polling, checkpoints and failure recovery. | Present in report section 6/config/source notes; retain documented unknown provider policies. Current team review pending, production validation later. |
| A06 | English PDF, LaTeX/Overleaf package, literal snippets, six stories, seven risks, preliminary CHI and architecture. | PDF generated and visually inspected, thirteen pages; source/ZIP consistency checked. Student content review pending. |
| A07 | Source-profile notebook executed with outputs. | 31/31 code cells, zero stored errors in existing environment; fresh-clone lock reproduction remains an internal gate, not an invented extra professor artifact. |
| A08 | Required repository scaffolding, configuration, samples, citations and GitHub entry points. | Present; repeat final secret/artifact review before submission. Scaffolds are not implemented services. |
| A09 | Submission reference and review provenance. | Earlier decisions/review records apply only to their recorded scope. No approval of the new pairs/report is inferred; no upload or final submitted commit is recorded. |

The remaining academic uncertainty is A03, plus final interpretation/review of
A02. Do not mark Workshop 1 fully compliant merely because all files exist.

## 9. Merge and submission gate

- [x] Earlier integration decisions are recorded in `PABLO_REVIEW.md`, limited to its historical source scope, intra-NWS investigation rows, earlier notebook and preliminary CHI; [ ] current report/config/daily-comparison review by both students. The record does not approve later edits.
- [x] Current notebook rerun completed: 31/31 code cells, zero errors, saved-input checksum assertions and reproduced cross-source table. [ ] Fresh-clone reproduction against the lock; the existing environment run does not establish this.
- [x] Registered raw evidence is checksum-protected, attributable, and sanitized of captured cookies; [ ] repeat the secret/artifact audit immediately before submission.
- [x] Large-source acquisition and partition instructions are documented in source notes/scripts; no bulk archive is tracked.
- [x] Report and technical documentation are in English.
- [x] Limitations and unresolved questions are explicit.
- [ ] The submitted commit/hash and repository link are recorded in `CHANGE_LOG.md`.

## 10. Required handoff

Every source task must append its exact observation, sample path, documentation URL, query/poll time, HTTP metadata where relevant, profile result, limitation, and handoff to `CHANGE_LOG.md` and `EVIDENCE_REGISTER.md`.
