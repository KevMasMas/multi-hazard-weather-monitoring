# Implementation Plan - Workshop 1

- **Team:** Team 9 - Pablo Garzon and Kevin Rincon
- **Target date:** not yet recorded in the reviewed specification
- **Working branch:** `workflow-1`
- **Base branch/commit:** project foundation commit `602143d`
- **Status:** Four-source evidence, accepted region/time scope, concrete quality-record examples, traceability, draft contracts, shared model/architecture and executed notebook are recorded; PDF export/visual review and final independent submission review remain incomplete
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

- [x] Prior executed notebook evidence: 29/29 code cells, execution counts 1-29, zero error outputs (see 2026-11-05 entries); [ ] rerun after current report/config/notebook edits in the locked environment; [x] Pablo's earlier workstream review is recorded; [ ] Kevin cross-review of current edits.
- [x] Report source-profile dimensions in executed notebook outputs for the four qualifying samples; note sample limitations and distinguish station-page behavior from source-wide policy.
- [x] Record six evidence-backed quality/availability/revision examples with exact source IDs and raw paths (REPORT_DRAFT.md, Section 5, Q-01 through Q-06).
- [x] Investigate five NWS Alert/KOKC candidate pairs with explicit temporal/textual-geographic basis and limitations; Pablo review accepts them for investigation only, not as confirmed matches.

#### Contracts and project definition

- [x] Draft the four-source canonical field mapping and Team 9 domain tables in `workshop_1/mapping.md`; [ ] complete final field-level team review.
- [x] Draft UTC, WGS84, unit/severity, duplicate-key, and raw-reference/content-hash rules in the mapping and ADRs; [ ] close the explicitly listed open field-level decisions.
- [x] Draft four source-specific partition/pagination, key, poll/overlap, watermark/checkpoint and interrupted-run recovery contracts in REPORT_DRAFT.md Section 7 and mirror them in config; proposed schedules remain pending mutual review and implementation.
- [x] Draft a proposed functional user and seven MoSCoW stories (W1-D01; see 2026-11-04 report-draft change-log entry); [ ] confirm user and wording with Kevin/professor.
- [x] Draft and jointly review index inputs/rule/scale/validation approach without claiming empirical validation (ADR 0002 and `PABLO_REVIEW.md`).
- [x] Draft and jointly review six risks and mitigations (W1-D01; see report draft and `PABLO_REVIEW.md`).
- [x] Produce the conceptual ER diagram, labeled architecture overview, and independent field-level mapping table; [ ] complete the final English PDF report and submission review.

### P1 - quality improvements after P0

- [ ] Automate a source-profile summary table from the notebook outputs.
- [x] Add Workshop 1 requirement-to-evidence traceability matrix to REPORT_DRAFT.md Section 11; PDF and final artifact review remain pending.
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

- [x] Four sources are validated with preserved real evidence and official documentation citations; source-specific limitations and license caveats are explicit.
- [ ] Each profile meets the record threshold and required dimensions.
- [ ] Five real quality issues and five defensible candidate pairs are documented, or a requirement conflict is explicitly escalated rather than fabricated.
- [ ] Mapping, ER model, and ingestion contracts cover all four sources.
- [x] English report source, notebook, samples, configuration draft, mapping and repository structure exist; [ ] final PDF export and visual review (explicitly deferred).
- [x] Rubric items point to report sections/artifacts in Section 11; exact evidence IDs are listed in the Evidence Register and quality-example table.

## 9. Merge and submission gate

- [x] Earlier joint review of source scope, candidate pairs, notebook and preliminary CHI is recorded in `PABLO_REVIEW.md`; [ ] Kevin to cross-review current report/config updates and both to repeat final artifact review.
- [x] Previous notebook run used documented inputs (29/29 code cells, zero errors, eleven checksum matches); [ ] rerun after current edits. The current environment lacks `uv`, so the documented runner could not execute here.
- [x] Registered raw evidence is checksum-protected, attributable, and sanitized of captured cookies; [ ] repeat the secret/artifact audit immediately before submission.
- [x] Large-source acquisition and partition instructions are documented in source notes/scripts; no bulk archive is tracked.
- [x] Report and technical documentation are in English.
- [x] Limitations and unresolved questions are explicit.
- [ ] The submitted commit/hash and repository link are recorded in `CHANGE_LOG.md`.

## 10. Required handoff

Every source task must append its exact observation, sample path, documentation URL, query/poll time, HTTP metadata where relevant, profile result, limitation, and handoff to `CHANGE_LOG.md` and `EVIDENCE_REGISTER.md`.
