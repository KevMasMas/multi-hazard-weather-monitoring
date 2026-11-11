# Change Log - Workshop 1

## Entry template

Use `deliveries/_templates/CHANGE_LOG.md` and include source-query timestamps and evidence paths when source validation begins.

## Entries

### [2026-11-11 America/Bogota] - W1-D05 - Execute the current notebook

- **Objective:** refresh current notebook execution evidence.
- **Status:** execution completed; final report/PDF and submission review remain pending.
- **Branch or commit:** `workflow-1`; uncommitted changes.
- **Requirements addressed:** executed source-profile notebook.
- **Files created:** `FINAL_REVIEW.md`.
- **Files modified:** notebook and this change log.
- **Implementation or documentation completed:** executed all notebook cells using the existing project virtual environment.
- **Decisions and rationale:** use the available environment directly when the wrapper cannot find `uv`.
- **Verification and exact result:** nbconvert exited 0; 29/29 code cells executed; zero stored error outputs.
- **Evidence location:** notebook outputs and `FINAL_REVIEW.md`.
- **Errors found and correction:** wrapper failed because `uv` is unavailable; direct project Python execution succeeded. Runtime emitted non-fatal Windows kernel warnings.
- **Risks or limitations:** lock synchronization and fresh-clone reproduction were not verified; PDF remains pending.
- **Input received from:** Kevin requested completion of Workshop 1.
- **Handoff to:** final technical/report review and PDF preparation.
- **Recovery or rollback:** regenerate outputs from preserved samples with the recorded command; source samples are unchanged.


### [2026-11-05 America/Bogota] - W1-D03/W1-D05 - reconcile stale Workshop 1 status claims

- **Objective:** remove outdated source status statements, clarify the accepted Oklahoma decision versus unmeasured multi-year completeness, and align the plan with existing review evidence.
- **Status:** [x] NOAA/NWS Alerts source notes and report now reflect captured profiles; [x] prior Pablo review is correctly recorded for region and candidate pairs; [x] plan identifies the previous notebook run separately from the required rerun after edits; [!] cross-review and fresh execution remain pending.
- **Branch or commit:** `workflow-1`; no commit created.
- **Files modified:** `docs/sources/noaa-storm-events.md`, `docs/sources/nws-alerts.md`, `deliveries/01-workshop-1/REPORT_DRAFT.md`, `IMPLEMENTATION_PLAN.md`, `CHANGE_LOG.md`, and `docs/reports/workshop-1-compliance-review.md`.
- **Implementation or documentation completed:** corrected source-note statuses that incorrectly said samples/profiles were missing; corrected the report table to state that Oklahoma is accepted while full statewide history remains unproven; marked documented English report/limitations and the already-recorded region/pair reviews accurately in the plan; clarified Kevin's current review handoff.
- **Verification and exact result:** reviewed all modified status statements against the evidence register, Pablo review, current report, notebook state and accepted ADRs. `git diff --check` passed. No source data, live endpoint or notebook computations were changed in this cleanup.
- **Evidence location:** NOAA sample/profile and status in `docs/sources/noaa-storm-events.md`; Alerts sample/profile and empty-poll limitation in `docs/sources/nws-alerts.md`; region and candidate approvals in `deliveries/01-workshop-1/PABLO_REVIEW.md` and ADR 0001; current compliance matrix in `docs/reports/workshop-1-compliance-review.md`.
- **Decisions and rationale:** accepted Oklahoma scope is distinct from statewide multi-year station coverage, which remains unmeasured. A prior review cannot stand in for Kevin's review of newly edited contracts and report content. A saved prior notebook run cannot stand in for re-execution after current edits.
- **Errors found and correction:** status text said NOAA live evidence was not captured and NWS field profiling was pending despite preserved samples and executed profiles; those stale claims were corrected. No additional data-quality issue was inferred.
- **Risks or limitations:** strict acceptance of the five sample quality conditions remains for cross-review because several describe documented source limitations rather than provider defects. Exact 2010-2025 statewide volumes remain unmeasured. Final PDF remains deferred.
- **Input received from:** Pablo asked to complete all remaining work that can be performed, excluding the PDF.
- **Handoff to:** Kevin to review current source contracts, Q examples, volume screens and report. Re-run the notebook in the locked environment after `uv` becomes available.
- **Recovery or rollback:** restore earlier source-note wording only if corresponding source evidence changes; preserve all raw samples and prior review history. Re-run the notebook with the repository script when the locked runtime is available and update its outputs/change log with exact results.



### [2026-11-05 America/Bogota] - W1-S05/W1-D05 - reconcile source contracts and notebook handoff

- **Objective:** reconcile configuration with source-specific report contracts, state concrete incremental overlap proposals, and remove obsolete or machine-specific notebook text/output.
- **Status:** [x] NOAA/GHCN/Alerts/station configuration fields now align with the report proposal; [x] notebook status and stale saved project-root output updated; [x] YAML and whitespace checks passed; [!] rerun of the edited notebook is pending because `uv` is unavailable; [!] Kevin's cross-review remains pending.
- **Branch or commit:** `workflow-1`; no commit created.
- **Files modified:** `config/sources.yaml`, `deliveries/01-workshop-1/REPORT_DRAFT.md`, `IMPLEMENTATION_PLAN.md`, `CHANGE_LOG.md`, `WORK_BOARD.md`, and `notebooks/01_source_profiling.ipynb`.
- **Implementation or documentation completed:** NOAA config now distinguishes yearly archive partition from row-level `BEGIN_YEARMONTH`; GHCN config distinguishes raw wide key `(STATION, DATE)` from normalized key `(STATION, DATE, element_code)` and no longer treats a historical date as a live watermark. NWS Alerts now records hourly full-snapshot polling, no record watermark, ID/content-hash revision detection and no deletion inference from absence. NWS station observations propose hourly polling with a one-hour overlap plus daily seven-day reconciliation, bounded by documented retention and subject to request-cost review. Notebook markdown now identifies the prior run and says rerun/review are still needed; replacement-character mojibake was removed from markdown; the saved code-cell output no longer exposes Kevin's old local absolute path.
- **Verification and exact result:** `yaml.safe_load` parsed `config/sources.yaml` and returned exactly `noaa_storm_events`, `ghcn_daily`, `nws_alerts`, and `nws_station_observations`; `nws_alerts.watermark_field` is null and station overlap is `PT1H`. `git diff --check` passed. The documented execution script was previously attempted and exited at line 20 with `uv is not installed or available on PATH`; no full rerun is claimed. Existing notebook outputs still show 29 code cells with execution counts 1-29 and zero stored error outputs, but those outputs predate this documentation/config edit.
- **Evidence location:** aligned details in `config/sources.yaml`, `REPORT_DRAFT.md` Section 7, and notebook cells 0, 4, and 49.
- **Decisions and rationale:** hourly polling is a proposal, not a source-mandated schedule. The one-hour station overlap exceeds the documented up-to-20-minute arrival delay; a daily seven-day reconciliation is proposed to catch later revisions within retention. The Alerts endpoint is treated as a full current-state snapshot because the captured active polls were empty and do not support a validated event watermark. Historical keys are named by transformation stage to avoid ambiguity.
- **Errors found and correction:** previous configuration did not distinguish NOAA archive-year from `BEGIN_YEARMONTH`, conflated the GHCN raw/normalized key, and declared an Alerts record watermark inconsistent with full-snapshot polling; all were corrected in the draft. Notebook output contained a contributor-specific local path and outdated status; the saved text was updated. Full notebook execution remains blocked by missing `uv` in the current environment.
- **Risks or limitations:** contract schedules and overlaps still need Kevin's review; query support/cost for seven-day station reconciliation must be demonstrated before implementation. Current notebook output counts do not prove a fresh run after edits. No live weather request or bulk download was performed.
- **Input received from:** Pablo requested all remaining work that can be completed, excluding the PDF.
- **Handoff to:** Kevin to cross-review source proposals; both students to approve the contracts. Re-run the documented locked-environment notebook when `uv` is available.
- **Recovery or rollback:** revert only the config/report/notebook prose changes if cross-review selects different contracts. Preserve raw samples. To verify the final notebook, install the locked `uv` version using `scripts/workshop_1/README.md` and rerun the documented PowerShell script, then confirm 29/29 cells, zero errors and checksum assertions.



### [2026-11-05 America/Bogota] - W1-S04/W1-S05/W1-D01/W1-D03/W1-D04 - close evidence-backed report gaps (PDF deferred)

- **Objective:** complete the remaining Workshop 1 work that can be supported from the preserved samples and official-source notes, excluding final PDF generation as requested.
- **Status:** [x] added six record-level quality/availability/revision examples with stable source references; [x] added source-qualified hazard measures/units and monitoring context; [x] added one explicitly labeled volume screen per historical source; [x] documented four draft source contracts with partition/poll overlap, keys, checkpoint and failure-recovery rules; [x] added requirement-to-evidence traceability and updated ownership/review notes; [!] Kevin cross-review, statewide station inventory/multi-year counts, clean-clone review, and final PDF/visual inspection remain pending.
- **Branch or commit:** `workflow-1`; no commit created. Working tree was clean before these edits; changes remain uncommitted.
- **Files modified:** `WORK_BOARD.md`, `deliveries/01-workshop-1/EVIDENCE_REGISTER.md`, `IMPLEMENTATION_PLAN.md`, `PABLO_REVIEW.md`, `REPORT_DRAFT.md`, and this `CHANGE_LOG.md`.
- **Implementation or documentation completed:** Q-01 to Q-06 table cites GHCN station/date/flag, NOAA event ID, NWS alert ID, same-ID KDEN revision, adjacent KOKC observation IDs and a KOKC optional-field null. Q-01 through Q-05 satisfy the five-example minimum; Q-06 is supplemental. Report now distinguishes categorical alert severity, event-specific NOAA magnitude, station metric values/units and GHCN daily units. Proposed NOAA annual partitions, GHCN station-year partitions, NWS Alerts full-active-state polling, and NWS station rolling overlap include idempotency keys and interruption recovery. An evidence matrix maps rubric topics to report sections and registered artifacts. Report volume screens: NOAA selected-filter 2024 count 2,317, multiplied linearly by 16 to 37,072 only as a rough screening extrapolation; GHCN 365 observed rows at one station in 2025, or 5,840 single-station rows under a complete-year straight-line assumption. Neither is a measured full-scope volume. The report and board explicitly defer PDF export.
- **Verification and exact result:** manually parsed raw CSV/GeoJSON evidence. Confirmed GHCN `USW00013967` / `2025-01-05` has PRCP `0.0` and attribute `T,,W,2400`; NOAA `EVENT_ID=1155350` is Heavy Snow / zone `CIMARRON` with blank begin coordinates; NWS alert `urn:oid:2.49.0.1.840.0.86cd7f91116ab184a79b0a23e06189d945720161.001.1` has null geometry and seven affected zone URLs; the shared KDEN observation URL timestamped `2026-11-04T01:53:00+00:00` changed temperature from null/QC Z to 4.4 degC/QC V; adjacent KOKC observations `2026-11-03T21:52:00Z` and `2026-11-03T22:55:00Z` are 63 minutes apart. `git diff --check` initially reported trailing spaces on the report status line; removed them and will rerun. Existing notebook artifact was inspected in prior audit as 52 cells / 29 code cells, counts 1-29, zero error outputs, eleven checksum matches. Attempted the documented notebook runner, but it stopped at line 20 because `uv` is not installed/on PATH in this environment; system Python lacks `seaborn`, so no substitute execution was claimed.
- **Evidence location:** quality rows reference `workshop_1/samples/region_comparison/ghcn_okc_usw00013967_2025.csv`, `workshop_1/samples/noaa_storm_events/details_sample.csv`, `workshop_1/samples/nws_alerts/recent_7d_page_1.geojson`, KDEN poll 1/2 GeoJSON, and `workshop_1/samples/region_comparison/nws_kokc_observations_snapshot.geojson`; broader profile evidence in `notebooks/01_source_profiling.ipynb` and `deliveries/01-workshop-1/EVIDENCE_REGISTER.md`.
- **Decisions and rationale:** source schedules/overlaps and volume figures are labeled proposals/screens, not verified source guarantees or measured totals. Empty NWS active polls are not treated as proof of alert-level change semantics. The sample includes the exact five quality examples without presenting normal documented optionality as an agency defect. The five alert/KOKC pairs remain candidates because spatial containment was not computed. PDF remains deferred per Pablo's instruction.
- **Errors found and correction:** report initially had trailing Markdown hard-break spaces, removed. Notebook runner could not execute because the documented `uv` dependency manager is missing; this is an environment blocker, not a notebook failure. No live weather calls or bulk downloads were made.
- **Risks or limitations:** NOAA extrapolation is a one-year linear screen across a changing event distribution; GHCN row screen covers only one station-year and cannot estimate the county/state inventory. Station source/provider attribution and multi-station completeness remain open. Hourly polling and overlap windows are proposed, not team-approved schedules. Quality cases are five samples; not all represent data defects. Final source cross-review, clean-clone review, final PDF and visual inspection remain outstanding.
- **Input received from:** Pablo requested completion of all remaining Workshop 1 work except the final PDF.
- **Handoff to:** Kevin for source-contract, volume-screen and quality-case cross-review; both students for artifact review. Pablo can generate the PDF only after the user/team is ready for that step.
- **Recovery or rollback:** revert only this entry and the listed documentation changes if source review changes the contract; do not remove or rewrite raw evidence. To rerun the notebook, install the locked `uv` version (`scripts/workshop_1/README.md`) and execute `scripts/workshop_1/execute_source_profiling_notebook.ps1`; verify 29/29 cells, zero errors and checksum assertions before refreshing saved outputs.


### [2026-11-05 America/Bogota] - W1-S02/W1-D03 - align repository scaffolding with Workshop 1

- **Objective:** reconcile the repository root and Workshop 1 artifacts with the professor's explicit repository-setup checklist while keeping later workshop implementation out of scope.
- **Status:** [x] required root scaffolding, configuration draft, independent mapping, architecture overview, and source-status log added; [!] final report and remaining rubric evidence are not complete.
- **Branch or commit:** `workflow-1`; no commit created.
- **Requirements addressed:** Workshop 1 repository setup, four-entry `config/sources.yaml`, required CLI stub, canonical mapping artifact, labeled architecture overview, source-status tracking, and stable future-workshop boundaries.
- **Files created:** `ingest.py`, `config/sources.yaml`, `src/multi_hazard_weather_monitoring/` package boundaries, area READMEs under `dashboard/`, `sql/`, `tests/` and `tests/fixtures/`, `workshop_1/mapping.md`, `docs/architecture/workshop-1-overview.md`, `docs/sources/SOURCE_STATUS.md`, and `docs/reports/workshop-1-compliance-review.md`.
- **Files modified:** `README.md`, `WORK_BOARD.md`, `deliveries/README.md`, `deliveries/01-workshop-1/IMPLEMENTATION_PLAN.md`, `docs/references/academic-materials.md`, `docs/reports/academic-material-review.md`, and this change log.
- **Implementation or documentation completed:** replaced empty-directory-only placeholders with explicit package and milestone boundaries; added all four assigned sources with URL, format, schedule state, watermark field, duplicate key and change-detection proposal; separated the high-level pipeline diagram from the conceptual ER model; created the professor-requested standalone source-to-canonical mapping; updated outdated notebook execution counts and indexed the Workshop 2-4 PDFs published on 2026-11-05.
- **Verification and exact result:** `ingest.py` compiled and `python ingest.py --mode status` returned JSON with `status=not_implemented` and `milestone=workshop_1_scaffold`; `config/sources.yaml` parsed successfully and contains exactly four source entries; all 17 checked professor-required scaffold paths exist; `git diff --check` passed apart from informational CRLF-to-LF warnings.
- **Evidence location:** repository root, `config/sources.yaml`, `workshop_1/mapping.md`, `docs/architecture/`, and the professor-issued `Workshop_1.pdf` repository-setup section.
- **Decisions and rationale:** scaffolding is present now because Workshop 1 explicitly requires it. Docker, SQL schema, adapters, scheduling, tests and dashboard behavior remain unimplemented and are labeled with their correct later milestones. Proposed hourly incremental schedules remain drafts pending final contract review.
- **Errors found and correction:** directories existed only as `.gitkeep` placeholders, so `rg --files` and a fresh-clone reviewer could not understand their intended boundaries. Required explanatory/package files were added without deleting existing files. The academic index also still implied that Workshops 2-4 were unpublished; it now records their 2026-11-05 publication without claiming they were fully reviewed.
- **Risks or limitations:** structural compliance is not delivery completion. The final English PDF, exact quality-problem example records, requirement-to-evidence matrix, license/attribution closure, source-volume estimates, final ingestion-contract decisions, and final review remain pending.
- **Input received from:** Kevin's request to organize the project and verify it against the professor's requirements.
- **Handoff to:** Kevin for NOAA/Alerts contract and traceability closure; Pablo for GHCN/station contract and final report review; both for the final Workshop 1 merge gate.
- **Recovery or rollback:** revert this additive scaffold/mapping documentation set together. Preserved samples and notebook evidence are unchanged.

### [2026-11-05 America/Bogota] - W1-P03/W1-P04 - add class-level DataFrame inspection

- **Objective:** make the GHCN-Daily and KOKC sections visibly demonstrate the basic Pandas workflow covered in the current semester through 2026-11-05, without introducing later EDA or modelling topics.
- **Status:** [x] basic DataFrame inspection and simple aggregation added; [x] notebook executed from top to bottom; [!] teammate review remains part of the submission gate.
- **Branch or commit:** `workflow-1`; no commit created.
- **Requirements addressed:** W1-P03/W1-P04 source profiling, reproducible notebook evidence, and course-level explanation of how captured CSV/GeoJSON data becomes a Pandas DataFrame.
- **Files modified:** `notebooks/01_source_profiling.ipynb` and this change log.
- **Implementation or documentation completed:** added explicit `head()`, `shape`, column listing, `info()`, `describe()`, and null-count outputs for GHCN and flattened KOKC observations; added a simple monthly GHCN `groupby()` summary plus KOKC condition and observation-date counts. Existing provenance, source-specific QC, polling comparison, and limitation cells were preserved.
- **Verification and exact result:** the notebook contains 52 cells, including 29 code cells; all 29 code cells have execution counts and there are zero error outputs. The GHCN frame is 365 rows by 12 columns with zero missing values in the captured fields. The flattened KOKC frame is 200 rows by 59 columns; the focused eight-column view exposes 200 missing relative-humidity values, 199 missing wind-gust values, and one missing wind-speed value in this bounded sample. No live weather request was made.
- **Evidence location:** executed outputs in `notebooks/01_source_profiling.ipynb`; preserved inputs under `workshop_1/samples/region_comparison/`.
- **Decisions and rationale:** the notebook now follows the current class boundary: loading/displaying DataFrames, types, descriptive statistics, null counts, `value_counts()`, and `groupby()`. Correlation, regression, imputation, outlier treatment, feature engineering, and advanced visualization were deliberately excluded because they are not required for this correction and must not be inferred merely from legacy repository notebooks.
- **Errors found and correction:** the first execution attempt failed because the sandbox denied `uv` access to its interpreter cache. The same locked project script was rerun with the required filesystem permission and completed successfully. The Windows ZMQ runtime emitted non-fatal local-kernel transport warnings; execution still completed with zero notebook errors.
- **Risks or limitations:** descriptive values apply only to the registered one-station samples. Missing optional station measurements are observations to investigate, not automatically defects. The monthly GHCN table is descriptive and does not establish a historical baseline or statewide coverage.
- **Input received from:** Kevin's clarification that the notebook should use only material covered in the current semester through 2026-11-05 and should visibly read and inspect each source as a basic DataFrame.
- **Handoff to:** Pablo to review and explain the GHCN/KOKC inspection; Kevin to confirm that the source-profile narrative remains consistent with the final report.
- **Recovery or rollback:** revert this notebook/log change together; the preserved source samples remain unchanged and can regenerate the prior or current notebook outputs.

### [2026-11-05 America/Bogota] - W1-S01/W1-S03/W1-D02/W1-D04 - accept scope/time and close Pablo's Workshop 1 review

- **Objective:** record the team's final region and temporal decisions and complete Pablo's Workshop 1 design/review responsibilities without fabricating production coverage or personal authorship.
- **Status:** [x] Oklahoma/counties accepted; [x] 2010-2025 baseline and rolling 24-hour current window accepted; [x] station/geographic contract accepted; [x] Pablo workstream review recorded; [x] CHI accepted as a preliminary Workshop 1 proposal; [!] production station inventory, shared canonical model/architecture, final PDF and later empirical validation remain.
- **Branch or commit:** `workflow-1`; no commit created.
- **Requirements addressed:** W1-S01 region/time scope, Pablo-owned W1-S03 station/region design, W1-D02 preliminary indicator review, W1-D04 report review, and mutual-review gates.
- **Files created:** `docs/decisions/0003-temporal-scope.md`, `docs/decisions/0004-oklahoma-geographic-and-station-contract.md`, `docs/architecture/workshop-1-er-model.md`, and `deliveries/01-workshop-1/PABLO_REVIEW.md`.
- **Files modified:** ADRs 0001/0002, `PROJECT_CONTEXT.md`, `WORK_BOARD.md`, `IMPLEMENTATION_PLAN.md`, `EVIDENCE_REGISTER.md`, `REPORT_DRAFT.md`, station-source research, region-comparison report, notebook narrative, and this change log.
- **Implementation or documentation completed:** promoted Oklahoma/counties from preferred to accepted; selected 16 complete baseline years (`2010-01-01` through `2025-12-31`); defined current as a rolling 24-hour interval at hourly UTC boundaries with separate seven-day audit/recovery context; defined monthly seasonal comparison; completed deterministic station eligibility/primary selection; defined county/zone/polygon/station allocation rules and source-geography entities; completed the first conceptual four-source ER model; recorded joint review of source contracts, candidate pairs, notebook and CHI proposal.
- **Verification and exact result:** reviewed all-four-source Oklahoma evidence, the Oklahoma-vs-Denver comparison, 27/27 clean notebook execution, eleven checksum assertions, two-poll KOKC results, five unconfirmed candidate pairs, and CHI ADR. Documentation now distinguishes accepted decisions from future measurements. The final notebook rerun after narrative updates completed 27/27 code cells with zero error outputs. `git diff --check` passes.
- **Evidence location:** ADRs 0001-0004; `PABLO_REVIEW.md`; `docs/reports/region-comparison-oklahoma-vs-denver.md`; executed notebook and evidence register.
- **Decisions and rationale:** 2010-2025 provides 16 complete, annually partitionable years and excludes incomplete 2026; a 24-hour current window is operationally interpretable; seven days remains context rather than being mislabeled current. County analytics retain source zones/polygons through versioned many-to-many relations. One pilot station never represents the entire state.
- **Errors found and correction:** outdated candidate/pending wording remained across report, notebook and status files after the team decision; it was replaced without rewriting older chronological change-log entries. No historical log claim was retroactively changed.
- **Risks or limitations:** acceptance does not prove 16-year completeness for every station, implement crosswalks, validate CHI parameters, confirm candidate event matches, or constitute professor approval. Those gates remain explicit.
- **Input received from:** Kevin's instruction, with Pablo present, confirming Oklahoma and asking the assistant to select the best temporal window and complete Pablo's documented Workshop 1 workstream.
- **Handoff to:** Pablo for Workshop 2 GHCN/station inventory and orchestration; Kevin for canonical database/NOAA/Alerts integration; both for schema, architecture, final report/PDF and submission commit.
- **Recovery or rollback:** supersede accepted ADRs with a new numbered decision if later evidence changes scope; do not erase the decision history. Revert only this additive review/decision block if the team states that the communicated approval was inaccurate.

### [2026-11-05 America/Bogota] - W1-S04 - investigate five alert/observation candidate pairs

- **Objective:** satisfy the five-pair investigation with temporal and geographic evidence instead of pairing unrelated historical/current records.
- **Status:** [x] one additional official KOKC cursor page preserved; [x] deterministic five-pair derivation created; [x] notebook/report/evidence register updated and executed; [!] candidates require Pablo review and remain unconfirmed.
- **Branch or commit:** `workflow-1`; no commit created.
- **Requirements addressed:** W1-S04 five cross-source candidate pairs, reproducibility, and explicit time/geography/severity/identifier differences.
- **Files created:** `scripts/workshop_1/build_candidate_event_pairs.py`; `workshop_1/samples/candidate_pairs/README.md`, `source_metadata.yaml`, raw KOKC page/metadata/headers, and `nws_alerts_kokc_candidate_pairs.csv`.
- **Files modified:** the station-capture script/README, `notebooks/01_source_profiling.ipynb`, `EVIDENCE_REGISTER.md`, `IMPLEMENTATION_PLAN.md`, `WORK_BOARD.md`, `REPORT_DRAFT.md`, station research note, and this change log.
- **Implementation or documentation completed:** extended the capture script to follow a supplied official cursor; preserved the next KOKC page; implemented a deterministic candidate rule requiring Oklahoma County area text and a station timestamp inside the alert interval; selected the earliest unused observation after effective time; exposed source IDs, timestamps, delay, severity, measurements/units, basis, and unconfirmed status.
- **Verification and exact result:** KOKC cursor request returned HTTP 200, 500 unique features, zero missing geometries, range `2026-10-31T04:55:00Z` to `2026-11-03T21:50:00Z`, 2,056,851 bytes, and SHA-256 `A13720F4E561AC3B20E56DD15F9D43224A1EF1ABE84D37E58DF5BF5FE38BA5CD`. Derived CSV has five rows and SHA-256 `09429FE22925B3B1B2F1CCF72BD3F374920548A42290A9733A11A14F366FA275`. Delays after alert effective time are 60, 240, 660, 660, and 480 seconds. Final notebook rerun executed 27/27 code cells with zero errors and asserts five `candidate_not_confirmed` rows plus both new checksums.
- **Evidence location:** `W1-NWS-ALERTS-PROFILE-001`, `W1-NWS-KOKC-PAGE-002`, and `workshop_1/samples/candidate_pairs/`.
- **Decisions and rationale:** pair NWS Alerts with temporally overlapping KOKC observations because current evidence does not temporally overlap Storm Events/GHCN years. Do not call the rows confirmed matches: county text is broader than a station point, and three warning messages belong to one broader episode.
- **Errors found and correction:** the first attempt to hash copied files passed `*` to `Get-FileHash -LiteralPath`, which is invalid; files had copied successfully and were then hashed individually. No evidence body was changed.
- **Risks or limitations:** textual area matching is not polygon containment; KOKC cannot represent the full county; alert updates are records, not independent weather episodes; current endpoint retention limits retrospective analysis.
- **Input received from:** Kevin's instruction to continue with all remaining Workshop 1 work.
- **Handoff to:** Pablo to inspect the five IDs, timing, station values, and candidate wording; both students to approve matching rules for later automated integration.
- **Recovery or rollback:** regenerate the CSV from the registered alert page and committed KOKC cursor page using the documented script; verify both registered SHA-256 values before accepting output.

### [2026-11-05 America/Bogota] - W1-D05 - create the locked notebook environment and execute all profiles

- **Objective:** remove the final local-environment blocker and execute the all-four-source Oklahoma profiling notebook from top to bottom with reproducible dependencies.
- **Status:** [x] isolated environment and exact dependency lock created; [x] notebook executed twice after correction; [x] all checks and cells passed; [!] Pablo must review outputs before the submission gate is complete.
- **Branch or commit:** `workflow-1`; no commit created.
- **Requirements addressed:** W1-D05 clean notebook execution, reproducible setup, evidence integrity, and review-ready stored outputs.
- **Files created:** `requirements-workshop1.in`, `requirements-workshop1.lock`, and `scripts/workshop_1/execute_source_profiling_notebook.ps1`. The local `.venv` is ignored and is not submission content.
- **Files modified:** `notebooks/01_source_profiling.ipynb`, `scripts/workshop_1/README.md`, `REPORT_DRAFT.md`, `IMPLEMENTATION_PLAN.md`, `WORK_BOARD.md`, and this change log.
- **Implementation or documentation completed:** installed `uv 0.13.7`; created an isolated CPython 3.12 environment; locked 59 direct/transitive packages; added an execution script that discovers uv, uses the lock, runs from the repository root, stops on failure, and writes reviewed outputs in place; corrected a stale KDEN-specific coordinate-quality rule exposed by the first Oklahoma execution.
- **Verification and exact result:** final notebook has 49 cells and 27 code cells; all 27 executed sequentially with counts 1-27 and zero error outputs. The initial execution passed nine registered checksums; the final W1-S04 rerun passes eleven after adding the KOKC cursor page and candidate-pair CSV. Summary rows are NOAA 250, active NWS polls 0/0, recent NWS Alerts 238, GHCN-Daily 365, and KOKC station polls 200/200. The KOKC comparison reports 3,627.404123 seconds, 197 shared IDs, three entering and three leaving IDs, zero changed shared payloads, and 197 unchanged payloads. Verified runtime: CPython 3.12.16, pandas 3.1.1, NumPy 2.5.4, Matplotlib 3.11.2, Seaborn 0.13.2, PyYAML 6.0.3, and nbformat 5.11.1. `git diff --check` passes.
- **Evidence location:** executed `notebooks/01_source_profiling.ipynb`; direct and exact dependencies at repository root; execution procedure in `scripts/workshop_1/README.md`.
- **Decisions and rationale:** keep the Workshop 1 environment separate from future production dependencies; commit the lock and executed notebook but not `.venv`; require teammate review even after a technically successful execution.
- **Errors found and correction:** the first `uv` Python resolution created a valid CPython directory but a broken minor-version junction, so compilation used the exact managed interpreter and the execution script now discovers the concrete CPython 3.12 directory. A sandboxed rerun could not write uv's profile cache; the authorized rerun succeeded. The first executed quality table carried a KDEN assumption that any coordinate-count entry meant variation; KOKC has one coordinate pair, so the row is now emitted only when more than one pair exists. The notebook was rerun after correction.
- **Risks or limitations:** the uv cache and interpreter are user-local; a fresh machine must install uv and recreate `.venv`. Successful execution verifies reproducibility of the captured samples, not the correctness of unresolved cross-source matches, region approval, model, or index parameters.
- **Input received from:** Kevin's instruction to continue completing all remaining work.
- **Handoff to:** Pablo for notebook-output and report review; both students for the five candidate event-pair investigation and shared design decisions.
- **Recovery or rollback:** delete the ignored `.venv` if local recovery is needed, reinstall uv, and rerun `execute_source_profiling_notebook.ps1`; the committed lock reconstructs the exact package set.

### [2026-11-05 America/Bogota] - W1-P04/W1-S01 - complete the KOKC two-poll comparison

- **Objective:** replace the mixed-region station profile with reproducible two-poll KOKC evidence for the preferred Oklahoma scope and integrate it into the Workshop 1 notebook and documentation.
- **Status:** [x] reusable capture/comparison scripts added and validated; [x] second KOKC poll preserved after the one-hour minimum; [x] exact ID/payload comparison documented; [x] notebook paths moved to Oklahoma and stale Denver outputs removed; [!] clean top-to-bottom notebook execution and Pablo review remain pending.
- **Branch or commit:** `workflow-1`; no commit created.
- **Requirements addressed:** W1-P04 common-region evidence, W1-S01 all-four-source regional alignment, notebook evidence integrity, and reproducible source-validation procedure.
- **Files created:** `scripts/workshop_1/capture_nws_station_observations.ps1`, `compare_nws_station_polls.ps1`, and `README.md`; `workshop_1/samples/region_comparison/nws_kokc_observations_poll_2.geojson`, its metadata JSON, and sanitized response-headers JSON.
- **Files modified:** `notebooks/01_source_profiling.ipynb`, the region-comparison README/metadata, `EVIDENCE_REGISTER.md`, `REPORT_DRAFT.md`, `IMPLEMENTATION_PLAN.md`, `WORK_BOARD.md`, `PROJECT_CONTEXT.md`, ADR 0001, the region-comparison report, the station-source research note, the repository README, and this change log.
- **Implementation or documentation completed:** added a Windows PowerShell 5.1/PowerShell 7 compatible station-capture script with identifying User-Agent, exact body preservation, sanitized headers, metadata, counts, timestamps, pagination and checksum; added a duplicate-aware comparator for IDs and compact payloads; moved the notebook's GHCN/station paths and integrity checks from Denver to Oklahoma; cleared five stale stored output blocks that described KDEN/Denver.
- **Verification and exact result:** capture at `2026-11-05T12:39:36.9519380Z` returned HTTP 200 `application/geo+json`, 200 features and unique IDs, zero missing geometries, oldest observation `2026-11-03T23:10:00Z`, newest `2026-11-05T11:52:00Z`, and `pagination.next`. Raw size is 779,027 bytes and SHA-256 is `7857DD85FB4F35E33FA4A0EEFB0F07E6634E457D96F6A0D4C30560B5CDD07D79`. The interval from the first local capture time is 3,627.404123 seconds. The pages share 197 IDs; three occur only in each page; all 197 shared payloads are unchanged. Both scripts have zero parser errors. The comparator also reproduced the earlier KDEN result exactly: 96 shared IDs, 95 unchanged, one changed same-ID/same-timestamp payload.
- **Evidence location:** `W1-REGION-NWS-KOKC-001` and `W1-REGION-NWS-KOKC-002` in `EVIDENCE_REGISTER.md`; exact metadata in `workshop_1/samples/region_comparison/`; procedure in `scripts/workshop_1/README.md`.
- **Decisions and rationale:** use KOKC/`USW00013967` for the notebook's preferred-region station profile while retaining KDEN evidence as a tested alternative and revision example. Treat records entering/leaving a bounded page as rolling-window behavior, not deletion. Retain ID plus content-hash comparison even though no KOKC shared payload changed because KDEN proves same-ID changes can occur.
- **Errors found and correction:** the first live request failed with `Host desconocido` under the restricted network and succeeded once authorized. The first local copy command used an invalid PowerShell `Select-Object -Single` parameter; no files were copied, and rerunning with `-First 1` preserved and verified the intended artifacts. The notebook previously contained stored Denver outputs under newly changed Oklahoma paths; all five stale output blocks were cleared.
- **Risks or limitations:** the first KOKC snapshot lacks persisted HTTP headers/status; only poll 2 has them. Two bounded pages at one Oklahoma station do not establish statewide station coverage or general revision/deletion behavior. The notebook has not yet been executed after switching to Oklahoma evidence.
- **Input received from:** Kevin's instruction to continue completing and documenting the remaining Workshop 1 work.
- **Handoff to:** Pablo to review the preferred-region station selection and comparison; both students to execute/review the combined notebook and select a reproducible multi-station coverage rule.
- **Recovery or rollback:** restore poll 2 from ignored raw path `data/raw/nws_station_observations/poll_2_KOKC_20261105T123936Z.geojson` and verify its SHA-256. Never replace the evidence with a later rolling response; register a new poll instead.

### [2026-11-05 America/Bogota] - W1-D02 - draft the preliminary Compound Hazard Index

- **Objective:** define a transparent, parameterized, and reviewable Compound Hazard Index proposal without implementing or claiming validation during Workshop 1.
- **Status:** [x] Component model, formula, missingness/freshness rules, alternatives, and validation plan drafted; [!] Pablo review, accepted source-field mappings, historical coverage measurement, parameter sensitivity, and empirical validation remain pending.
- **Branch or commit:** `workflow-1`; no commit created.
- **Requirements addressed:** W1-D02 and the preliminary-index portion of the Workshop 1 project definition.
- **Files created:** `docs/decisions/0002-compound-hazard-index-proposal.md`.
- **Files modified:** `REPORT_DRAFT.md`, `IMPLEMENTATION_PLAN.md`, `WORK_BOARD.md`, `PROJECT_CONTEXT.md`, and this change log.
- **Implementation or documentation completed:** proposed county/24-hour/versioned output grain; five hazard components (flood, wind, heat, cold, winter); seasonal empirical-percentile normalization; weighted base plus bounded pairwise interaction; `[0, 100]` output; strict null/staleness behavior; separate coverage reporting; historical/current display requirements; and a held-out-period/sensitivity validation plan.
- **Verification and exact result:** checked the proposal against the project requirements already recorded in `PROJECT_CONTEXT.md`: it is per region, parameterized, historical-versus-current, exposes severity/component evidence, and remains explicitly non-predictive. The initial review parameters are five equal weights of `0.20` and `beta = 0.20`; they are labeled proposals rather than results. The formula is bounded because both the weighted base and pair term are bounded and the final value is capped before scaling to `[0, 100]`.
- **Evidence location:** design rationale and formula in ADR 0002; report-ready summary in `REPORT_DRAFT.md`. This is a design proposal and therefore does not create empirical evidence IDs.
- **Decisions and rationale:** keep component scores visible; add a limited interaction bonus so the index represents compound conditions; suppress the total when required evidence is unavailable; never lower apparent hazard by multiplying by data coverage. Avoid interpretation bands and learned weights until historical distributions and sensitivity are evaluated.
- **Errors found and correction:** none. No code or source data were changed.
- **Risks or limitations:** final field/unit mappings, categorical alert mapping, station/county aggregation, interaction pairs, time grain, baseline years, weights, and validation thresholds are unresolved. The assigned current NWS access paths may not permit full historical reconstruction of alerts and station observations.
- **Input received from:** Kevin's instruction to continue with the next documented task while waiting for the one-hour KOKC poll interval.
- **Handoff to:** Pablo to review component semantics, station/geographic aggregation, and missingness communication; Kevin to connect accepted NOAA/Alerts mappings; both students to approve parameters only after coverage and sensitivity evidence.
- **Recovery or rollback:** revert ADR 0002 and its report/plan references if team review selects a different formulation. No raw evidence or implementation depends on this proposal yet.

### [2026-11-05 America/Bogota] - W1-S01 - compare Oklahoma and Denver and repair evidence portability

- **Objective:** determine which candidate region better supports the four assigned sources, preserve the comparison evidence, and ensure registered checksums survive a clean Windows checkout.
- **Status:** [x] Oklahoma-versus-Denver comparison and recommendation documented; [x] Oklahoma City GHCN/KOKC coverage captures registered; [x] evidence line-ending policy repaired; [!] Pablo approval, second KOKC poll, final common-region notebook profile, and accepted ADR remain pending.
- **Branch or commit:** `workflow-1`; no commit created.
- **Requirements addressed:** W1-S01 candidate-region comparison, Kevin review of Pablo's regional coverage concern, evidence integrity, and notebook correctness.
- **Files created:** `.gitattributes`; `docs/reports/region-comparison-oklahoma-vs-denver.md`; `workshop_1/samples/region_comparison/README.md`, `source_metadata.yaml`, `ghcn_okc_usw00013967_2025.csv`, and `nws_kokc_observations_snapshot.geojson`.
- **Files modified:** eight previously registered CSV/GeoJSON evidence bodies were restored to their registered LF byte representation; `docs/decisions/0001-oklahoma-county-scope-candidate.md`, `PROJECT_CONTEXT.md`, `WORK_BOARD.md`, `IMPLEMENTATION_PLAN.md`, `EVIDENCE_REGISTER.md`, `REPORT_DRAFT.md`, and `notebooks/01_source_profiling.ipynb` were updated.
- **Implementation or documentation completed:** compared Oklahoma statewide, Colorado statewide, and a Denver-name subset using the same 14-event-family filter and official 2024 Storm Events archive; captured one qualifying Oklahoma City GHCN year and one KOKC 200-feature station page; documented Oklahoma/counties as the preferred but not accepted scope; added explicit Git attributes so raw evidence bytes are not rewritten by `core.autocrlf`; corrected the station notebook pagination check to read `station_observation_payload` instead of the unrelated `nws` variable.
- **Verification and exact result:** Oklahoma produced 2,317 relevant 2024 Storm Events rows, 14 event types, and 150 county/zone identifiers; Colorado produced 1,350 rows, 11 types, and 120 identifiers; the Denver-name subset produced 21 rows across six types. GHCN station `USW00013967` produced 365 rows from 2025-01-01 through 2025-12-31 with zero null PRCP/TMAX/TMIN values; SHA-256 is `D8EE9E0AFBFE25897C17BABE4A88DC0E12D4FECE8B74C26E8D817D5309FFB5AE`. KOKC produced 200 unique features spanning 37.05 hours, zero missing geometries, and a next-page cursor; SHA-256 is `391C49B75E7E05C225FE0EB63BB7BB822004169FFBB0F8FF6DDA006F236B0E68`. All eight earlier registered sample hashes were rechecked against their sidecars/register and matched after byte restoration.
- **Evidence location:** `W1-REGION-GHCN-OK-001` and `W1-REGION-NWS-KOKC-001`; full comparison in `docs/reports/region-comparison-oklahoma-vs-denver.md`; exact capture metadata in `workshop_1/samples/region_comparison/source_metadata.yaml`.
- **Decisions and rationale:** recommend Oklahoma because it aligns the existing alert and Storm Events evidence, has a substantially broader one-year hazard mix, and now meets the minimum record profile for both station sources. Do not mark the ADR accepted until Pablo reviews it. Retain Denver evidence because it proves same-ID station payload revision behavior.
- **Errors found and correction:** `core.autocrlf=true` changed registered evidence bytes after checkout, making notebook checksum assertions fail. Added `.gitattributes` with `-text` for evidence CSV/GeoJSON files and restored exact registered bytes. The notebook also referenced the wrong payload variable in its KDEN pagination assertion; corrected it without claiming a full notebook execution.
- **Risks or limitations:** one GHCN and one KOKC station do not establish statewide representativeness; HTTP status/headers were not persisted for the two comparison captures; the KOKC evidence has only one poll; the historical screen covers one year; county/zone/polygon crosswalks and five candidate cross-source event pairs remain open.
- **Input received from:** Kevin's request to document every action and decide whether Oklahoma or Denver is the better project scope.
- **Handoff to:** Pablo to review the comparison and approve or challenge Oklahoma/counties; Kevin to capture a second KOKC poll if the final common-region evidence requires it; both students to agree the crosswalk, time windows, and index proposal.
- **Recovery or rollback:** verify the two new evidence hashes against `source_metadata.yaml`; verify the eight restored sample hashes against their existing sidecars/register. Revert the recommendation documents if team review selects another scope, but retain raw captures and the `.gitattributes` integrity rule.

### [2026-11-04 America/Bogota] - W1-D01/W1-D04 - project definition and report source draft

- **Objective:** complete Pablo's draft user, MoSCoW stories, risks, source interpretation, station-region proposal, and English report manuscript using the shared evidence and current official source documentation.
- **Status:** [x] Project-definition sections and report source draft prepared; [!] no final region, accepted shared architecture/model, cross-source pair review, Kevin approval, full notebook run, or final PDF yet.
- **Branch or commit:** `workflow-1`; no commit created.
- **Requirements addressed:** W1-D01 draft sections, W1-D04 English report-source assembly, Pablo's station/region draft under W1-S03, and official attribution/update terms for W1-P01/W1-P02.
- **Files created:** `deliveries/01-workshop-1/REPORT_DRAFT.md`.
- **Files modified:** `deliveries/01-workshop-1/source-research-ghcn-nws-stations.md`, `deliveries/01-workshop-1/EVIDENCE_REGISTER.md`, `deliveries/01-workshop-1/IMPLEMENTATION_PLAN.md`, and `WORK_BOARD.md`.
- **Implementation or documentation completed:** added a proposed functional user, seven prioritized user stories (Must/Should/Could/Won't), risk/mitigation table, scope exclusions, station/region relationship sketch, all-four-source evidence summary, source observations and limits, draft mappings/contracts, report completion gate, and official citations. Added NCEI's daily update/weekly reconstruction and 45-60 day archive-quality timing; added NWS use/attribution caveats, seven-day station retention, and the current documented MADIS null max/min issue outside the Central time zone.
- **Verification and exact result:** official primary pages reviewed 2026-11-04: NCEI GHCN-Daily metadata/product page and NWS API/disclaimer. The cited GHCN v3 DOI is `10.7289/V5D21VHZ`; NCEI's page specifies subset/access-date citation and related article citation. NWS says its API is open/free with an identifying User-Agent and its disclaimer restricts endorsement claims. Report facts use existing register/research evidence and do not claim a shared region or event match. `git diff --check` passes; no PDF was generated, no notebook execution or automated tests were run in this entry.
- **Decisions and rationale:** left Oklahoma and Denver as candidates; station-region mapping and functional user remain proposals. The report is a Markdown source draft because required shared decisions and review are not available for final PDF claims.
- **Risks or limitations:** the source observations come from two different candidate areas, so no regional comparison across four sources is demonstrated; five cross-source pairs and Kevin's source review are still open. Attribution for any identified third-party station provider needs checking once the final station set is selected.
- **Input received from:** user's instruction to finish the remaining part of Pablo's work.
- **Handoff to:** Kevin to review user stories, source interpretation, report statements, candidate station-region relation, and attribution; both students to decide region, model, index scope, and cross-source findings.
- **Recovery or rollback:** all material is additive. Revert the report draft and these source-document updates if shared review changes scope; raw evidence remains preserved separately and checksum-verified.


### [2026-11-04 America/Bogota] - W1-P03/W1-P04 - complete first-pass evidence and source profiling

- **Objective:** complete Pablo's source-validation work using Kevin's notebook structure: provide a qualifying GHCN-Daily sample, perform the required second NWS station-observation poll, profile both sources, and record provisional mappings and update contracts.
- **Status:** [x] GHCN-Daily 365-row sample and profile; [x] NWS station observations two-poll evidence and comparison; [x] Pablo sections integrated into the shared notebook; [!] full notebook top-to-bottom execution, attribution confirmation, regional validation, and Kevin review remain pending.
- **Branch or commit:** `workflow-1`; no commit created.
- **Requirements addressed:** W1-P03, W1-P04, Pablo's source-to-canonical mapping and ingestion-contract drafts under W1-S02/W1-S05.
- **Files created:** `workshop_1/samples/nws_kden_observations_poll2.geojson` (200 features; 807,067 bytes) and adjacent metadata sidecar.
- **Files modified:** `notebooks/01_source_profiling.ipynb`, `deliveries/01-workshop-1/source-research-ghcn-nws-stations.md`, `deliveries/01-workshop-1/EVIDENCE_REGISTER.md`, `deliveries/01-workshop-1/IMPLEMENTATION_PLAN.md`, `WORK_BOARD.md`, `PROJECT_CONTEXT.md`, and `docs/plans/semester-roadmap.md`.
- **Implementation or documentation completed:** added poll 2 to evidence inventory and checksum validation; added a reproducible ID/payload comparison, station-source quality observations, GHCN and NWS station mappings, and draft source-specific update contracts. Kept Denver labeled as a test candidate, not the accepted project region.
- **Verification and exact result:** poll 2 was retrieved 2026-11-04 20:04:29 America/Bogota (2026-11-05 01:04:29 UTC), HTTP 200, `application/geo+json`, 200 features, SHA-256 `83099d933716e406dde6541fa0aa1a16fa9eae28da11797ed4d5d595de1aa870`. The interval from poll 1 was 80,124.882 seconds. The bounded pages shared 96 IDs; 104 IDs were only on page 2 and 104 from page 1 were not on page 2; 95 shared payloads were unchanged and one same-ID/same-timestamp payload changed. The changed observation included revised QC/value fields and cloud metadata. Notebook structure passed nbformat validation with 49 cells and includes the poll-2 body and metadata in its integrity inventory. SHA-256 checks matched all four GHCN/NWS sample sidecars. No top-to-bottom execution is claimed.
- **Evidence location:** `P-GHCN-01`, `P-NWS-01`, and `P-NWS-02` in the evidence register; research and profile notes in `source-research-ghcn-nws-stations.md`.
- **Decisions and rationale:** retained source IDs but added full-feature content comparison because one same-ID payload changed. Did not infer deletions from absence in a later bounded page. Kept GHCN daily measurements in a source-specific domain proposal instead of forcing them into event rows.
- **Errors found and correction:** a first network connectivity attempt failed under the default restricted environment. An authorized escalation permitted the source query. An initial connectivity check returned status/size only and did not persist the body; it was not counted as evidence. A subsequent single capture was saved with response metadata and checksum.
- **Risks or limitations:** both NWS pages are bounded and rolling; Denver is not an agreed region; the two polls do not establish the service-wide revision/deletion policy. The notebook was not run fully in this Python environment; plotting dependencies `matplotlib` and `seaborn` are unavailable. No package installation was attempted. GHCN revision cadence, regional coverage, and attribution terms still need validation.
- **Input received from:** user's instruction to complete Pablo's part based on Kevin's work.
- **Handoff to:** Kevin for review of source mappings, content-hash update strategy, and station coordinate variation; both students for shared region, domain-model, and report decisions.
- **Recovery or rollback:** restore captured poll bytes from `workshop_1/samples/nws_kden_observations_poll2.geojson`; verify SHA-256 against its metadata sidecar and evidence-register row. Polling again later would produce a different rolling response and is not a byte-identical recovery.


### [2026-11-03 America/Bogota] - Pablo first empirical source samples

- **Objective:** validate Pablo's two assigned sources at one candidate location and produce reviewable raw evidence and initial profiles.
- **Status:** [x] Captured and profiled 365 GHCN-Daily rows and 200 NWS observations; [!] second NWS poll, regional coverage analysis, shared-region decision, attribution confirmation, and Kevin review remain pending.
- **Branch or commit:** `workflow-1`; no new commit created.
- **Requirements addressed:** first empirical access and sample/profile work for GHCN-Daily/NCEI and NWS station observations.
- **Files created:** `notebooks/01_source_profiling.ipynb` (partial two-source notebook); `workshop_1/samples/ghcn_daily_denver_2025-06_to_09.csv` (93-row scoping response), its metadata sidecar, `workshop_1/samples/ghcn_daily_usw00003017_2025.csv` (365 rows), its metadata sidecar, `workshop_1/samples/nws_kden_observations_poll1.geojson` (200 features), its metadata sidecar.
- **Files modified:** `README.md`, `PROJECT_CONTEXT.md`, `docs/plans/semester-roadmap.md`, `deliveries/01-workshop-1/source-research-ghcn-nws-stations.md`, `EVIDENCE_REGISTER.md`, `IMPLEMENTATION_PLAN.md`, this log, and the notebook after execution to store cell outputs.
- **Decisions and rationale:** use Denver/KDEN/USW00003017 only as a candidate test location; the airport names and nearby coordinates support testing a station crosswalk, but do not select the team's final region. Save a full calendar year for GHCN to exceed the record threshold. Save one bounded NWS page; compare a second poll only after the required one-hour minimum.
- **Verification and exact result:** NCEI returned HTTP 200 CSV with 365 rows for 2025, 365 unique dates, zero duplicate station-date keys, zero nulls in the requested PRCP/TMAX/TMIN values, and no nonblank quality flags; PRCP included 47 trace (`T`) flags with numeric 0.0 and source flags W (238) / 1 (127). NWS returned HTTP 200 GeoJSON with 200 features, 200 distinct IDs, 200 parseable descending timestamps, valid point coordinates for all features, and no duplicate IDs. Profiled nested-value null counts, units, timestamps, coordinates, and response pagination in the research note. Executed all five notebook code cells in order using IPython, saved their outputs, and validated notebook structure with `nbformat`; `git diff --check` passes. No automated tests were requested or run.
- **Evidence location:** evidence IDs P-GHCN-00, P-GHCN-01, and P-NWS-01 in `EVIDENCE_REGISTER.md`; SHA-256 values and exact request/response metadata are recorded there and in sidecars. Sample-level detailed results are in `source-research-ghcn-nws-stations.md`.
- **Errors found and correction:** initial NCEI scoping response contained 93 records, below the 200-record threshold, so a separate full-year request was captured with 365. Direct PowerShell curl could not connect through the host's configured local proxy; the requests were completed via the Node fetch runtime. Standard Jupyter `nbconvert` execution was blocked when Windows denied `SetFileSecurity` on its connection file; ran the notebook's code cells sequentially in an in-process IPython shell and saved the resulting outputs. Removed the response's NWS tracking `Set-Cookie` header from the metadata sidecar; the raw GeoJSON body is unchanged.
- **Risks or limitations:** the NWS response is one page and the returned response includes `pagination.next`; only one poll exists so far. Observed nulls may represent optional/conditional values and must not be labeled confirmed defects without QA interpretation. Denver is not team-approved; no event matches or cross-source overlap have been claimed.
- **Input received from:** user's instruction to do as much of Pablo's Workshop 1 part as possible.
- **Handoff to:** Kevin for review of the candidate station crosswalk, profile, and mapping; both students to choose the region and validate the proposed contracts. The NWS second poll is due no earlier than 2026-11-03 22:49:04 America/Bogota.
- **Recovery or rollback:** preserve raw sample bodies as captured and verify against their sidecar SHA-256 values. If a later query differs, add a new evidence item instead of replacing these samples; retain the candidate-location caveat until the shared region decision.

### [2026-11-03 America/Bogota] - Pablo source documentation review

- **Objective:** prepare Pablo's Workshop 1 workstream for GHCN-Daily/NCEI and NWS station observations using official documentation only.
- **Status:** [x] Documentary research and draft mappings/contracts recorded; [!] empirical validation, samples, profiles, license/attribution confirmation, and reviewer approval remain pending.
- **Branch or commit:** `workflow-1`; no new commit created.
- **Requirements addressed:** initial source documentation review and preliminary field-mapping/ingestion-contract work for Pablo's two assigned sources.
- **Files created:** `source-research-ghcn-nws-stations.md` (renamed from its initial working filename to use a neutral artifact name).
- **Files modified:** this change log; `EVIDENCE_REGISTER.md`.
- **Decisions and rationale:** separated official documentation facts from proposed contracts and unresolved empirical questions; retained both the NCEI service and GHCN-Daily file layouts as alternatives pending a documented source-format choice.
- **Verification and exact result:** reviewed official NOAA/NCEI GHCN-Daily README, NCEI Access Data Service documentation/product metadata, and NWS API documentation. No live weather endpoint was queried and no sample/profile/test was produced.
- **Evidence location:** official documentation links and the source-by-source notes in `source-research-ghcn-nws-stations.md`; no raw source evidence captured.
- **Errors found and correction:** repository status initially described the evidence register as empty because no APIs had been queried. Clarified below that desk research exists while empirical evidence remains empty.
- **Risks or limitations:** documentation cannot establish actual response fields, station coverage in the selected region, revisions, data-quality findings, useful polling cadence, or observed service behavior. License/attribution wording needs explicit confirmation for report use.
- **Input received from:** Pablo's request to complete his Workshop 1 part.
- **Handoff to:** Kevin for review; both students for shared region, representation, model, and attribution decisions. Empirical validation follows only after the team's authorization and scope selection.
- **Recovery or rollback:** this is an additive research note; revise its proposal sections if samples or authoritative instructions contradict them, preserving this log entry as history.

### [2026-11-03 America/Bogota] - Planning baseline - Workshop not started

- **Objective:** translate the official Workshop 1 specification into a two-person, evidence-gated implementation plan.
- **Status:** [x] Planning draft prepared; [!] no Workshop 1 requirement has been executed or validated.
- **Branch or commit:** planning was included in foundation commit `602143d` on `workflow-1`.
- **Requirements addressed:** planning and allocation only.
- **Files created:** `IMPLEMENTATION_PLAN.md`, `CHANGE_LOG.md`, and `EVIDENCE_REGISTER.md`.
- **Implementation or documentation completed:** requirement checklist and proposed Kevin/Pablo source ownership.
- **Decisions and rationale:** each student owns one historical and one incremental source to balance work and avoid knowledge silos; all scope, model, matching, and index decisions remain shared.
- **Verification and exact result:** plan checked against the local Workshop 1 PDF; no API or dataset was queried.
- **Evidence location:** `docs/reports/academic-material-review.md` and the local professor-issued PDF outside this repository.
- **Errors found and correction:** none during planning.
- **Risks or limitations:** target date and later workshop specifications are not present in the reviewed material; ownership still requires team approval.
- **Input received from:** project foundation review.
- **Handoff to:** Kevin and Pablo after accepting `deliveries/00-project-foundation/`.
- **Recovery or rollback:** revise the plan when official instructions change; retain this entry as historical planning context.

### [2026-11-04 America/Bogota] - Planning organization - Task ownership clarified

- **Objective:** make the Workshop 1 execution order and individual responsibility immediately understandable.
- **Status:** [x] Planning structure clarified; [!] source validation remains not started.
- **Branch or commit:** local organization changes after `602143d` on `workflow-1`.
- **Requirements addressed:** source ownership, review responsibility, dependencies, evidence handoff, and final integration.
- **Files modified:** `WORK_BOARD.md` and this Workshop 1 implementation plan/change log.
- **Implementation or documentation completed:** created stable task IDs grouped into foundation closure, official research, evidence collection, four-source integration, and delivery preparation.
- **Decisions and rationale:** Kevin keeps NOAA Storm Events/NWS Alerts; Pablo keeps GHCN/NWS observations; shared model and indicator decisions require mutual approval.
- **Verification and exact result:** no source query or data validation was performed; this change is documentation-only.
- **Evidence location:** `WORK_BOARD.md`.
- **Errors found and correction:** responsibility was repeated in multiple documents without a single current task sequence; `WORK_BOARD.md` is now the only operational assignment source.
- **Risks or limitations:** the allocation still needs Pablo's confirmation and official Workshop 1 dates are not recorded.
- **Input received from:** user request for a clearer, less disorganized project structure.
- **Handoff to:** Kevin and Pablo for Step 0 review before source research begins.
- **Recovery or rollback:** revert the organization commit; foundation commit `602143d` remains unchanged.

### [2026-11-04 America/Bogota] - W1-K01/W1-K03 - NOAA source preparation and first evidence sample

- **Objective:** document NOAA Storm Events access and capture a reproducible source sample large enough to begin the required Workshop 1 profile.
- **Status:** [x] Official 2024 bulk archive and 250-row sample captured; [!] full notebook profile and Pablo's review remain pending.
- **Branch or commit:** `docs/w1-noaa-source-preparation`; uncommitted at entry time.
- **Requirements addressed:** W1-K01 documentation research and the evidence-capture portion of W1-K03.
- **Files created or changed:** `docs/sources/noaa-storm-events.md`, `docs/decisions/0001-oklahoma-county-scope-candidate.md`, `notebooks/references/noaa/`, `scripts/workshop_1/extract_noaa_storm_events_sample.ps1`, `workshop_1/samples/noaa_storm_events/`, `WORK_BOARD.md`, and `EVIDENCE_REGISTER.md`.
- **Implementation or documentation completed:** preserved the NOAA tutorial as reference; documented official access paths, revision behavior, evidence rules, and profiling requirements; downloaded the official 2024 details archive; generated a deterministic Oklahoma compound-hazard subset.
- **Decisions and rationale:** Oklahoma/counties and 2010-2025 are proposals only. The sample uses one complete year (2024) so profiling can start without claiming that the final multi-year window or region is accepted.
- **Verification and exact result:** raw archive 12,693,243 bytes, SHA-256 `2070B83ECCAB041B36360AB73645B9A249C3EEFC5B92B5B3FC0CBBA4D9FCC09C`; decompressed source 69,801 rows and 51 columns; filter produced 2,317 candidate rows across 14 requested event types and 150 distinct county/zone identifiers; 1,681 candidate rows use zone geography and have missing begin coordinates; committed stratified sample contains 250 rows, 51 columns, all 14 event types, 250 distinct `EVENT_ID` values, and zero exact duplicate rows; sample SHA-256 `987F5C641B6B85BF89477A823B52757D50D2C5376895FD53056A9AFE9F79403A`.
- **Evidence location:** `workshop_1/samples/noaa_storm_events/` with evidence ID `W1-NOAA-SE-001`; untouched archive is local under ignored `data/raw/` storage.
- **Errors found and correction:** the first PowerShell decompression command used a missing path property and produced an empty derived CSV. That file was rejected, the path handling was corrected, and the sample was regenerated and revalidated before registration.
- **Risks or limitations:** the committed CSV is a parsed and re-serialized subset, not the byte-identical source response; the untouched gzip archive is intentionally not committed; one year cannot validate the proposed 2010-2025 baseline; HTTP headers other than status were not captured.
- **Input received from:** Kevin's NOAA tutorial notebook and official NOAA/NCEI documentation.
- **Handoff to:** Kevin to build the NOAA section of `notebooks/01_source_profiling.ipynb`; Pablo to review the evidence and candidate-region assumptions.
- **Recovery or rollback:** delete only the generated sample artifacts and rerun `scripts/workshop_1/extract_noaa_storm_events_sample.ps1` from the checksum-verified local archive; do not modify the original gzip file.

### [2026-11-04 America/Bogota] - W1-K02/W1-K04 - NWS Alerts first poll

- **Objective:** document the incremental alert contract and preserve the first of two required Oklahoma active-alert polls.
- **Status:** [x] Documentation and poll 1 captured; [!] poll 2, change comparison, alert-level profile, and review remain pending.
- **Branch or commit:** `docs/w1-noaa-source-preparation`; uncommitted at entry time.
- **Requirements addressed:** W1-K02 documentation and the first-capture portion of W1-K04.
- **Files created or changed:** `docs/sources/nws-alerts.md`, `scripts/workshop_1/capture_nws_alerts.ps1`, `workshop_1/samples/nws_alerts/`, `WORK_BOARD.md`, and `EVIDENCE_REGISTER.md`.
- **Implementation or documentation completed:** added a parameterized capture script with the required identifying User-Agent and GeoJSON Accept header; preserved the exact response and registered selected response metadata.
- **Decisions and rationale:** queried `alerts/active?area=OK` to stay aligned with the proposed region and incremental current-state requirement; did not widen the query merely to obtain more records.
- **Verification and exact result:** at 2026-11-04 19:14:33 UTC (14:14:33 America/Bogota), NWS returned HTTP 200 and `application/geo+json`; response was 221 bytes with a valid FeatureCollection and zero features; SHA-256 `1D0E2E7AA61FB7F1C43913FB4A7A58BB6FA31922516D6CC4E50166009CCED27D`; raw and committed-copy checksums matched.
- **Evidence location:** `workshop_1/samples/nws_alerts/poll_1.geojson` and `poll_1_metadata.yaml`, evidence ID `W1-NWS-ALERTS-001`; raw response and full header capture remain in ignored `data/raw/nws_alerts/` storage.
- **Errors found and correction:** no request or parsing error occurred. The zero-feature response is preserved as observed rather than treated as a failure.
- **Risks or limitations:** an empty active response cannot profile alert fields, compare identifiers, or demonstrate update behavior. The second poll may also be empty; if so, the team must report the limitation and use a separately labeled recent-alert sample only if the Workshop requirement permits it.
- **Input received from:** official NWS API and Alerts Web Service documentation.
- **Handoff to:** Kevin to run poll 2 no earlier than 2026-11-04 20:14:34 UTC and compare both responses; Pablo to review the contract and evidence.
- **Recovery or rollback:** preserve poll 1. If the committed copy is lost, restore it byte-for-byte from the ignored raw path and verify the registered SHA-256 before use.

### [2026-11-04 America/Bogota] - W1-K04 - Windows PowerShell compatibility correction

- **Objective:** allow Kevin to execute the NWS capture script from the Windows PowerShell console available on his machine.
- **Status:** [x] Script and instructions corrected; [!] poll 2 remains pending until Kevin reruns the command.
- **Branch or commit:** `docs/w1-noaa-source-preparation`; uncommitted at entry time.
- **Requirements addressed:** reproducibility of W1-K04 evidence capture.
- **Files modified:** `scripts/workshop_1/capture_nws_alerts.ps1`, `workshop_1/samples/nws_alerts/README.md`, and `docs/sources/nws-alerts.md`.
- **Implementation or documentation completed:** replaced the PowerShell 7-only `Get-Date -AsUTC` option with `[DateTime]::UtcNow`, enabled TLS 1.2 for Windows PowerShell 5.1, and documented direct script invocation plus a process-scoped execution-policy fallback.
- **Verification and exact result:** script parsed successfully after the change; no additional NWS request was made during the compatibility correction.
- **Errors found and correction:** the documented `pwsh` command failed because PowerShell 7 was not installed or not on `PATH`; instructions now work from the already-open Windows PowerShell session.
- **Risks or limitations:** Windows execution policy may still block unsigned local scripts; the documented `-ExecutionPolicy Bypass` applies only to the child process and does not change the machine policy.
- **Input received from:** Kevin's exact `CommandNotFoundException` output.
- **Handoff to:** Kevin to run poll 2 using the corrected command.
- **Recovery or rollback:** revert this compatibility entry only if PowerShell 7 becomes an explicit project prerequisite.

### [2026-11-04 America/Bogota] - W1-K04 - NWS Alerts second poll and comparison

- **Objective:** validate the second active-alert capture, prove the required interval, and compare it with poll 1.
- **Status:** [x] Two-poll capture and empty-state comparison completed; [!] recent-alert field sample, full profile, and reviewer acceptance remain pending.
- **Branch or commit:** `docs/w1-noaa-source-preparation`; uncommitted at entry time.
- **Requirements addressed:** two-poll and comparison portion of W1-K04.
- **Files created or changed:** `workshop_1/samples/nws_alerts/poll_2.geojson`, `poll_2_metadata.yaml`, `poll_comparison.yaml`, `docs/sources/nws-alerts.md`, `WORK_BOARD.md`, and `EVIDENCE_REGISTER.md`.
- **Implementation or documentation completed:** preserved the exact second GeoJSON body, registered selected response headers and checksum, and documented collection- and feature-level comparison results.
- **Decisions and rationale:** retained both empty responses as valid current-state evidence; did not widen or rewrite the polls to manufacture active alert records.
- **Verification and exact result:** poll 2 occurred at 2026-11-04 20:49:29 UTC, 5,696 seconds (1 hour 34 minutes 56 seconds) after poll 1; HTTP 200, `application/geo+json`, 221 bytes, zero features, SHA-256 `5932B237B6751B92C46BFB5B6BD6A2F444522F4614B12D6DD1E72FC65C56716C`; raw and committed-copy checksums matched. Both polls had zero features; the collection `updated` timestamp and document hash changed.
- **Evidence location:** evidence ID `W1-NWS-ALERTS-002` in `workshop_1/samples/nws_alerts/`; comparison in `poll_comparison.yaml`.
- **Errors found and correction:** no capture error was found. The Windows PowerShell compatibility correction allowed Kevin to produce poll 2 successfully.
- **Risks or limitations:** no alert-level identifiers, geometry, severity, revisions, expirations, or content changes can be profiled from two empty collections.
- **Input received from:** Kevin's locally executed poll 2 raw response and headers.
- **Handoff to:** Kevin to capture a separately labeled recent seven-day Oklahoma alert response and add both NWS and NOAA sections to the profiling notebook; Pablo to review the two-poll evidence.
- **Recovery or rollback:** restore `poll_2.geojson` byte-for-byte from its ignored raw path and verify the registered SHA-256 if the committed evidence copy is lost.

### [2026-11-04 America/Bogota] - W1-K04 - NWS recent-window profiling evidence

- **Objective:** obtain enough real NWS Alert records for field profiling after both active-state polls returned empty collections.
- **Status:** [x] Complete observed pagination chain and preliminary aggregates captured; [!] executed notebook profile and reviewer acceptance remain pending.
- **Branch or commit:** `docs/w1-noaa-source-preparation`; uncommitted at entry time.
- **Requirements addressed:** record-threshold and field-evidence portion of W1-K04; this evidence does not replace the two polls.
- **Files created or changed:** `scripts/workshop_1/capture_nws_recent_alerts.ps1`, `workshop_1/samples/nws_alerts/recent_7d_*`, source notes, work board, and evidence register.
- **Implementation or documentation completed:** preserved both exact GeoJSON pages, followed the supplied cursor to termination, added a reusable paginated capture script, and recorded preliminary field distributions and missingness.
- **Decisions and rationale:** retained the full 238-record collection instead of truncating to 200; kept recent-window evidence separately labeled from active-state incremental polls.
- **Verification and exact result:** page 1 contained 238 features with 238 distinct feature and property IDs; page 2 contained zero features and no next cursor. Page checksums were `70AD394CF9E7399ACCB5CEA7B0A3B8E55526F01C314E68136439EA8442E966C3` and `4CB866FDD600EAC1EBDFFEF103B4F8B27E84D15EB8221914167420D158261574`. Observed event counts were 136 Severe Thunderstorm Warnings, 42 Special Weather Statements, 32 Tornado Watches, 18 Tornado Warnings, 6 Dense Fog Advisories, and 4 Wind Advisories. Geometry was null in 42 records, `ends` in 42, and `instruction` in 79.
- **Evidence location:** `workshop_1/samples/nws_alerts/`, evidence ID `W1-NWS-ALERTS-PROFILE-001`.
- **Errors found and correction:** the first page exposed a next cursor even though it contained fewer than the advertised 500-result limit; the cursor was followed instead of assuming completeness, and the resulting empty terminal page was preserved.
- **Risks or limitations:** page-1 response headers and HTTP status were not persisted by the manual command; the body was validated as GeoJSON. Null geometry may be expected when affected zones provide geography and must not yet be labeled a defect.
- **Input received from:** Kevin's manual recent-alert capture and the official pagination cursor returned by NWS.
- **Handoff to:** Kevin to reproduce these aggregates in `notebooks/01_source_profiling.ipynb`; Pablo to review field interpretation and geographic mapping.
- **Recovery or rollback:** restore exact page copies from ignored raw storage and verify both registered hashes; rerunning the endpoint later produces a different time window and is not a byte-identical recovery.

### [2026-11-04 America/Bogota] - W1-K03/W1-K04 - Kevin source-profiling notebook sections

- **Objective:** create the required Workshop 1 notebook and implement reproducible profiling sections for NOAA Storm Events and NWS Alerts following the course EDA structure.
- **Status:** [x] Notebook structure and Kevin-owned source code created; [!] execution outputs, Pablo's GHCN/station sections, cross-source pairs, and reviewer acceptance remain pending.
- **Branch or commit:** `docs/w1-noaa-source-preparation`; uncommitted at entry time.
- **Requirements addressed:** required `notebooks/01_source_profiling.ipynb`, evidence loading, integrity validation, source schema/missingness/identifier/time/geography profiles, incremental comparison, preliminary quality observations, and source-to-canonical mapping.
- **Files created or changed:** `notebooks/01_source_profiling.ipynb`, `WORK_BOARD.md`, and this change log.
- **Implementation or documentation completed:** added 39 cells: 18 Markdown and 21 code cells. The notebook locates the repository without absolute paths, validates five registered checksums, profiles 250 NOAA records and 238 recent NWS alerts, compares the two active polls, generates plots and preliminary quality observations, and records limitations and handoff requirements.
- **Decisions and rationale:** the notebook reads preserved local evidence and performs no live requests; raw frames remain unchanged and all parsing occurs on copies. Course curation steps such as imputation, outlier removal, and feature engineering are intentionally excluded from Workshop 1 source validation.
- **Verification and exact result:** notebook JSON parsed successfully as nbformat 4.5 with 39 cells, zero stored outputs, and zero execution counts. A real Python/Jupyter runtime is not installed in the current local environment, so code execution has not yet been claimed.
- **Evidence location:** `notebooks/01_source_profiling.ipynb` plus the registered NOAA and NWS sample paths it reads.
- **Errors found and correction:** the initial execution-summary label could imply that an unexecuted profile was complete; it was renamed to `section_implemented`, and completion language now appears only after cells execute successfully.
- **Risks or limitations:** syntax and runtime behavior still require execution in Colab or a documented Python environment; the notebook remains incomplete without Pablo's two sources and the shared cross-source analysis.
- **Input received from:** the professor's `eda_data_curation.ipynb`, `eda_visualizations.ipynb`, Workshop 1 specification, and Team 9 evidence register.
- **Handoff to:** Kevin to run all current cells and save real outputs; Pablo to add GHCN-Daily and NWS Station Observations using the same pattern.
- **Recovery or rollback:** restore the notebook from Git after its first commit; source evidence remains unchanged and can regenerate all outputs.
