# Change Log - Workshop 1

## Entry template

Use `deliveries/_templates/CHANGE_LOG.md` and include source-query timestamps and evidence paths when source validation begins.

## Entries

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
