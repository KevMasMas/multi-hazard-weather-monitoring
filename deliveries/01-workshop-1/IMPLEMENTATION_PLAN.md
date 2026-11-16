# Implementation Plan - Workshop 1

- **Team:** Team 9 - Pablo Garzon and Kevin Rincon
- **Target date:** Moodle notice supplied by Kevin: 2026-11-16, 12:00-15:15 America/Bogota; no upload is recorded
- **Working branch:** `workflow-1`
- **Base branch/commit:** project foundation commit `602143d`
- **Status:** technical review and clean reproduction complete: five qualified wind-record candidates, five primary quality concerns plus two observations, 59 lock pins and 32 error-free code cells. Kevin explicitly communicated approval by both students (`TEAM_APPROVAL.md`). Actual platform submission remains unrecorded.
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
- [x] Draft/review the preliminary CHI proposal; team approval of the Workshop 1 design recorded. Empirical acceptance of final parameters remains Workshop 4 work.

#### Historical sources

- [x] Profile NOAA Storm Events sample and document access, fields, observed coverage, identifier, archive revisions, citation/attribution caveat, and yearly partition proposal (2026-11-05; one-year screen only, exact license not identified).
- [x] Capture/profile qualifying GHCN-Daily sample and document volume/key/partition/revision/citation proposals; current report/mapping review complete. Statewide inventory remains later implementation work.
- [x] Preserve unmodified samples and record explicitly labeled volume screens (2026-11-05); complete regional station inventory and measured multi-year totals remain open and are not inferred from the pilot.

#### Incremental sources

- [x] Document NWS Alerts access, fields, geometry, IDs, timestamps, User-Agent, two-poll result and recent-alert profile; alert-level changes were not observable because both active polls were empty.
- [x] Capture and compare two qualifying NWS station-observation pages at least one hour apart for KDEN and for the preferred KOKC common region (see 2026-11-04 and 2026-11-05 change-log entries); [ ] complete multi-station/provider coverage and service-wide revision-policy review.
- [x] Poll both incremental sources twice at least one hour apart and record exact bounded-response differences; the empty active-alert polls cannot validate alert-level change semantics.

#### Profiling and data quality

- [x] Fresh clone/isolated locked environment executed 32/32 code cells with zero errors; [x] technical review and scoped artifact scan completed; [x] Kevin communicated both students' content approval (`TEAM_APPROVAL.md`).
- [x] Report source-profile dimensions in executed notebook outputs for the four qualifying samples; note sample limitations and distinguish station-page behavior from source-wide policy.
- [x] Verify Q1-Q7 against saved records; technical review accepts Q1-Q5 as five engineering quality concerns, with Q6-Q7 additional. They are not seven proven provider defects.
- [x] Eight daily temperature rows reproduced as supplemental comparisons, with limits explicitly reviewed. Five qualified Storm Events/GHCN wind-record pairs are the primary overlap examples; old intra-NWS rows excluded. Team report/method approval recorded without confirming ground truth.

#### Contracts and project definition

- [x] Draft the four-source field mapping/domain tables; [x] technical consistency review and communicated team approval complete for the Workshop 1 proposal.
- [x] Draft UTC, WGS84, unit/severity, duplicate-key, and raw-reference/content-hash rules in the mapping and ADRs; [ ] close the explicitly listed open field-level decisions.
- [x] Draft four contracts in current report section 6/config/source notes; technical and team proposal review complete, production schedule/recovery validation remains later work.
- [x] Current report section 2 contains the proposed functional user and six MoSCoW stories; team report approval recorded. No stakeholder interview or professor approval is claimed.
- [x] Draft and jointly review index inputs/rule/scale/validation approach without claiming empirical validation (ADR 0002 and `PABLO_REVIEW.md`).
- [x] Current report section 9 contains seven risks with mitigations; earlier workstream integration review is recorded in `PABLO_REVIEW.md`, not approval of all later edits.
- [x] Produce ER, architecture, mapping and visually inspected PDF; team content review explicitly recorded. Actual platform submission remains open.
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
| A02 | Q1-Q5 are five verified quality/integration problems; Q6-Q7 are additional availability observations. | Technical review considers them valid engineering quality problems under the guide; audit asserts all seven facts. Q5 now uses actual non-V QC; the old cadence gap is Q7. No provider fault or invalid measurement is inferred. Student review remains personal. |
| A03 | Five primary Storm Events/GHCN wind-record pairs have explicit airport, date, magnitude and identifier evidence. | Technical candidate-example review passes with disclosed limits: five Storm IDs, three GHCN daily records/dates, no five-independent-episode claim, null PGTM, possible common ASOS lineage. Eight temperature comparisons are supplementary; intra-NWS examples excluded. No exact-gust or professor acceptance claimed. |
| A04 | Mapping, core/domain ERs and configuration cover all four sources. | Technical review and explicit communicated team approval complete for the proposal; SQL/crosswalk implementation later. |
| A05 | Four contract proposals include keys, partition/polling, checkpoints and recovery. | Technical review and team report/design approval recorded with provider-policy unknowns preserved; production validation later. |
| A06 | English PDF, LaTeX/Overleaf package, literal snippets, six stories, seven risks, preliminary CHI and architecture. | Fourteen-page PDF visually inspected and ZIP checked; team approval bound to current report/mapping hashes. Actual upload not recorded. |
| A07 | Source-profile notebook executed with outputs. | Fresh clone at `cce9ade`, new non-system CPython environment, 59 exact lock pins, explicit clean kernel: 32/32 cells, zero errors; receipt stored. The NOAA Git newline defect was fixed and rerun. |
| A08 | Required scaffolding, configuration, samples, citations and GitHub entry points. | Current-tree/ZIP pattern and forbidden-path audit passes with its documented scope. Scaffolds are not implemented services. |
| A09 | Submission reference and review provenance. | `TEAM_APPROVAL.md` records Kevin's explicit statement that both reviewed and approved the current PDF/mapping/decisions, with artifact hashes; not an individual signature or professor grade. Actual upload/final submitted reference not recorded. |

Technical evidence/consistency/reproduction review is complete with the stated
qualifications; team content approval is explicitly recorded. Actual submission
recording remains open, and professor acceptance is not guaranteed by this review.

## 9. Merge and submission gate

- [x] Earlier integration decisions stay scoped to `PABLO_REVIEW.md`; current report/mapping/shared-design team approval is independently recorded in `TEAM_APPROVAL.md`, as explicitly communicated by Kevin.
- [x] Clean reproduction: 59 exact pinned versions, isolated kernel and 32/32 code cells with zero errors; receipt stored. The NOAA Git newline mismatch was corrected and rerun successfully.
- [x] Current source/ZIP secret-pattern and forbidden-artifact audit passed with its scope recorded; no universal absence-of-secrets or remote-history audit claimed.
- [x] Large-source acquisition and partition instructions are documented in source notes/scripts; no bulk archive is tracked.
- [x] Report and technical documentation are in English.
- [x] Limitations and unresolved questions are explicit.
- [ ] The submitted commit/hash and repository link are recorded in `CHANGE_LOG.md`.

## 10. Required handoff

Every source task must append its exact observation, sample path, documentation URL, query/poll time, HTTP metadata where relevant, profile result, limitation, and handoff to `CHANGE_LOG.md` and `EVIDENCE_REGISTER.md`.
