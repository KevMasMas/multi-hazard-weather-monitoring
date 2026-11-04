# Implementation Plan - Workshop 1

- **Team:** Team 9 - Pablo Garzon and Kevin Rincon
- **Target date:** not yet recorded in the reviewed specification
- **Working branch:** to be agreed after the foundation review
- **Base branch/commit:** foundation commit `602143d`
- **Status:** planned; no source query, sample, profile, or validation has started
- **Official specification:** `Workshop_1.pdf`

## 1. Requirement interpretation

Workshop 1 is an evidence-producing source-validation and data-contract milestone. Reading documentation is insufficient: all four assigned sources must be queried for real when this workshop is authorized, their unmodified responses preserved, and factual conclusions tied to evidence.

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

- [ ] Explain compound weather hazards, component severity measures, units, and monitoring value.
- [ ] Compare candidate US regions using all-four-source coverage and manageable volume.
- [ ] Select and justify the regional unit, historical window, and definition of current conditions.

#### Historical sources

- [ ] Validate NOAA Storm Events access, format, fields, coverage, update/revision policy, license, attribution, identifiers, and partition strategy.
- [ ] Validate GHCN-Daily/NCEI access, format, fields, coverage, update policy, license, attribution, identifiers, and partition strategy.
- [ ] Preserve unmodified samples and estimate full historical rows/size without unnecessary bulk downloads.

#### Incremental sources

- [ ] Validate NWS Alerts access, fields, geometry, identifiers, revisions/deletions, headers/timestamps, and User-Agent requirements.
- [ ] Validate NWS station observations access, station coverage, fields, units, identifiers, revisions, and timestamp behavior.
- [ ] Poll each incremental source twice at least one hour apart, or as otherwise justified by the specification, and record exact differences.

#### Profiling and data quality

- [ ] Execute `notebooks/01_source_profiling.ipynb` top to bottom with outputs.
- [ ] Report null percentages, ranges, duplicated identifiers, timestamp/time-zone formats, coordinate validity, and unit consistency for each source.
- [ ] Record at least five concrete data-quality problems with example records across the sources.
- [ ] Investigate at least five candidate same-event pairs and explain differences in time, position, severity, or identifier.

#### Contracts and project definition

- [ ] Map every source to canonical event fields and define Team 9 domain tables.
- [ ] Define UTC, WGS84, unit-conversion, severity, duplicate-key, and raw-reference/content-hash rules.
- [ ] Draft partitioning/pagination, watermark, polling, overlap-window, and halfway-failure recovery per source.
- [ ] Define functional user and at least six MoSCoW-prioritized user stories covering monitoring, analysis, and trust.
- [ ] Draft index inputs/rule/scale/validation approach without claiming validation.
- [ ] Record at least five risks and mitigations.
- [ ] Produce a labeled architecture overview, first ER diagram, mapping table, and English PDF report.

### P1 - quality improvements after P0

- [ ] Automate a source-profile summary table from the notebook outputs.
- [ ] Add a requirement-to-evidence matrix for the report rubric.
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

- [ ] Four sources are validated with preserved, cited real evidence.
- [ ] Each profile meets the record threshold and required dimensions.
- [ ] Five real quality issues and five defensible candidate pairs are documented, or a requirement conflict is explicitly escalated rather than fabricated.
- [ ] Mapping, ER model, and ingestion contracts cover all four sources.
- [ ] Required report, notebook, samples, configuration draft, and repository structure exist.
- [ ] Every rubric item points to a report section and evidence item.

## 9. Merge and submission gate

- [ ] Both students review every source contract and shared decision.
- [ ] Notebook runs top to bottom in a clean environment using documented inputs.
- [ ] Raw evidence is unmodified, small, attributable, and contains no secret.
- [ ] Large-source download instructions are documented instead of committing bulk data.
- [ ] Report and technical documentation are in English.
- [ ] Limitations and unresolved questions are explicit.
- [ ] The submitted commit/hash and repository link are recorded in `CHANGE_LOG.md`.

## 10. Required handoff

Every source task must append its exact observation, sample path, documentation URL, query/poll time, HTTP metadata where relevant, profile result, limitation, and handoff to `CHANGE_LOG.md` and `EVIDENCE_REGISTER.md`.
