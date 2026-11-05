# Change Log - Workshop 1

## Entry template

Use `deliveries/_templates/CHANGE_LOG.md` and include source-query timestamps and evidence paths when source validation begins.

## Entries

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
