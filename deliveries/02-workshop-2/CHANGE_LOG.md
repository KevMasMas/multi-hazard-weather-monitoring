# Change Log - Workshop 2

Append entries; do not silently rewrite historical observations.

## Entries

### [2026-11-16 America/Bogota] - Documentation review - Literal layer evidence and precise contracts

- **Objective/status:** address Kevin's pasted review priorities without source calls, data/migration changes or new pipeline runs; revised PDF compiled and inspected.
- **Branch/commit:** `workflow-2`, base `5810ba5b6f4587b57697d57a345a668b1a8fc47b`; `git ls-remote --heads origin workflow-2` confirms that base is pushed. New documentation changes remain local; no commit/push performed.
- **Files changed:** report main/PDF/README; generated `layer_appendix.tex`, `assets/bronze_excerpt.json`, `silver_head.txt`, `silver_info.txt`; offline excerpt/audit scripts; new `layer_excerpt_provenance.json` and `report_revision_audit.json`; root README, evidence register, submission manifest and active board/plan/log.
- **Content:** first two actual Bronze records, with only documented narrative prefixes omitted; complete input hashes; literal recorded Pandas head/info; exact task/schedule/trigger/logging behavior; explicit separate acquisition CLI with no DAG acquisition parameter; source/year native versus batch timestamp naming; course-to-schema/layer mapping; complete-interval CLI semantics and justification; neutral delivery/screenshot wording. No written professor clarification was found in the repository search, so the existing interpretation remains qualified.
- **Verification/results:** all sample hashes, notebook hash and nine executed code cells/zero errors remain unchanged. Existing 29-test receipt fingerprints match tested files. Saved database counts remain 13,561 NOAA and 5,478 GHCN with no duplicate groups. ZIP unchanged, CRC/member hashes valid, three JSON and three Parquet from distinct actual runs. W1 submission hashes match. Recompiled PDF: 12 pages, zero overfull-box errors; Poppler contact sheet and appendix page inspected. Existing run/test/package receipts were preserved; new documentation audit records the current build.
- **Errors/corrections:** first new build had two small text/table overflows; widened schedule column and split notebook-source prose, then recompiled with no overfull warnings. Underfull spacing notices remain nonfatal.
- **Evidence:** `workshop_2/EVIDENCE_REGISTER.md`, `evidence/layer_excerpt_provenance.json`, `evidence/report_revision_audit.json`, updated delivery `SUBMISSION_MANIFEST.json`.
- **Limits:** existing results were revalidated, not rerun. No new source/API query, runtime validation or teacher approval is claimed. Wider semester coverage/station/county scope remains as documented. Git verification used its remote ref protocol, not a weather API.
- **Input/handoff:** Kevin supplied the review instructions in the attached text. Review the new PDF, commit the documentation revision and push `workflow-2` manually before using the updated branch link.
- **Recovery:** regenerate excerpts from unchanged files and rebuild LaTeX. Keep earlier receipts and native data; do not replace historical run results with documentation-audit results.

### [2026-11-16 America/Bogota] - W2-01..W2-14 - Five-year slice and delivery artifacts

- **Objective:** prepare the requested PDF, genuine pipeline output samples and repository handoff before Kevin's 21:45 review deadline.
- **Status:** technical artifacts generated and verified; team approval, submission commit, push/upload and wider station/county/2010-2020 coverage remain open. W2-06 is one-station coverage, not completed Oklahoma inventory.
- **Branch/commit:** `workflow-2`, local working tree based on `f7d7c55`; no commit or push performed. Earlier teammate work and Workshop 1 artifacts preserved.
- **Files changed:** explicit acquisition/API verification/sample restore/packaging/notebook/audit tools under `scripts/workshop_2/`; capture registry and NOAA hail units; `config/workshop2_saved_captures.json`; Compose triggerer; 001-004 schema documentation; executed notebook; three selected actual Bronze/Parquet/CSV/lineage sets; report LaTeX/assets/PDF; sample ZIP; evidence/register/manifest; ADR 0006, Mermaid architecture, README/WSL/board/plan/demo documentation. `.gitattributes` preserves exact packaged CSV/JSON bytes across Git checkouts, and `.gitignore` permits only the selected sample Parquet outputs.
- **Implementation:** cached official NOAA details gzip files for 2021-2025, filtered Oklahoma rows without changing field values, and captured metric GHCN station-year CSVs. Native responses retain URLs, UTC capture times, hashes and headers before derivation. Registered the new inputs separately without modifying the Workshop 1 evidence register.
- **Decisions:** retain manual bounded historical DAGs and explicit network acquisition; keep original gzip versus derived Oklahoma CSV/JSON distinctions visible. One station is not statewide coverage. Retain weather extremes, daily dates, source QC attributes and missing points. Include triggerer for handout compatibility while using LocalExecutor/reschedule. Original failed runs remain in Airflow.
- **Verification/exact results:** ten real source/year Bronze/Silver pairs succeeded, including all sensors; database has 13,561 NOAA + 5,478 GHCN = 19,039 canonical rows, zero duplicate business-key groups, 365 dates per non-leap GHCN year and 366 in 2024. CLI replay returned all rows unchanged. Restarted only project containers; source counts and all ten original Parquet hashes persisted. Three further real DAG replays succeeded with zero accepted/rejected and all rows unchanged. All 29 WSL tests passed, zero errors/failures/skips; tested-file fingerprints verified. Notebook executed nine code cells with zero error outputs in Python 3.12.16/Pandas 3.1.1/Arrow 18.1.0. Its extracted ZIP copy also executed from an isolated directory with a fresh kernel, using the existing dependency environment (not a newly installed environment).
- **PDF/package evidence:** nine-page PDF compiled with Tectonic and rendered with Poppler; all pages reviewed in a contact sheet and key figures inspected at larger size. No overfull-box or out-of-page warnings remain; underfull spacing notices are nonfatal. ZIP has three actual JSON and three actual Parquet outputs, CSV inputs, lineage, manifest, executed notebook and current receipts; CRC/member hashes checked. Kevin supplied the unchanged actual UI screenshot; recorded counts include the two earlier failed Silver runs.
- **Evidence locations:** `workshop_2/EVIDENCE_REGISTER.md`, `samples/manifest.json`, `evidence/historical_acquisition.json`, `historical_airflow_runs.json`, `delivery_database.json`, `after_restart_database.json`, `replay_airflow_runs.json`, `persistence_verification.json`, `wsl_test_results.json`, `notebook_execution.json`, `isolated_notebook_execution.json`, `package_verification.json`, `final_artifact_audit.json`; delivery hashes in `SUBMISSION_MANIFEST.json`.
- **Errors/corrections:** a date-selection unit test was incorrectly coupled to the growing production config; replaced with explicit interval fixtures, then all tests passed. First LaTeX attempts encountered unused missing TikZ libraries, a fragile caption path and uncached fonts; removed unused libraries, fixed the caption and allowed Tectonic font retrieval. Added xurl and adjusted table/figure layout to remove overflow and an isolated figure page. Audit normalization handles PDF ligatures. The venv lacks pip; used the available external installer for dependency checks. Browser automation was unavailable; the UI image is contributor-supplied, not an invented screenshot.
- **Risks/limitations:** 2010-2020 years, wider station inventory and reviewed county assignments remain open. No monetary conversion, NLP, live-source acquisition on every DAG trigger, NWS incremental service or CHI is claimed. No professor clarification or Workshop 2 personal approval is recorded. Secret checks are scoped recognized-token/private-key pattern checks, not an absolute guarantee.
- **Input received:** Kevin requested completing the delivery and supplied the Airflow screenshot; live historical acquisition was announced before requests under that instruction.
- **Handoff:** Kevin/Pablo review the concrete PDF, notebook, ZIP and limitations; select a commit, then Kevin commits/pushes/uploads. Final ownership remains in `WORK_BOARD.md`.
- **Recovery:** preserve volumes/native evidence. Restore three packaged CSV inputs offline, then use the demo guide to rerun real batches; hashes reject modified inputs. Reacquisition is explicit and cached; future provider revisions must not silently replace submitted evidence. Use new numbered SQL migrations rather than editing applied ones.

### [2026-11-16 America/Bogota] - G3 pilot - Real Airflow Bronze/Silver verification

- **Objective/status:** execute the saved-data pipeline; both source flows completed successfully after correcting an actual Arrow import failure.
- **Branch/commit:** `workflow-2`, local uncommitted work; no commit/push.
- **Files:** `requirements-workshop2-pipeline.txt`, `Dockerfile`, board/plan/Workshop 2 README, `workshop_2/evidence/airflow_verification.json` and refreshed `wsl_test_results.json`. Generated outputs are in ignored `data/bronze/` and `data/curated/silver/`.
- **Decision:** Python <3.14 uses Arrow 18.1, preserving the Airflow image's pandas/NumPy compatibility; Python >=3.14 uses Arrow 26 and NumPy >=2. Build now requires `pip check`.
- **Verification:** Docker rebuild passed `pip check`; 28 WSL tests passed, zero failures/errors/skips. Local REST API reports Bronze and Silver success for `w2_fixed_20261117T015304` and `w2_ghcn_20261117T015321`, including successful exact-file sensors. Parquet rows: NOAA 250, GHCN 1,095; all unchanged, zero accepted/rejected in these replays. Native/Bronze/Parquet provenance is in manifests; Bronze and Parquet hashes were checked against files before recording the receipt.
- **Errors/corrections:** earlier Silver runs failed because Arrow 26 requires NumPy 2 while the image has 1.26. Upgrading NumPy conflicts with bundled pandas 2.1.4, so the final fix retains the compatible Arrow version. Earlier failed runs remain visible, not relabelled as successes. A REST request during restart failed before the verified runs. Browser access was unavailable; no GUI screenshot or inspection is claimed.
- **Limitations:** two partitions do not establish five-year/statewide historical coverage, three deliverable samples, full restart/recovery acceptance, or a completed workshop. Outputs are not packaged yet. WSL's 3.14 tests do not replace Airflow's real 3.12 execution; both were checked separately.
- **Input/handoff:** Kevin requested testing the open local Airflow instance. No weather API calls, personal approvals or submission were performed. Next: complete bounded output evidence, historical coverage and notebook/PDF/ZIP.
- **Recovery:** keep the Postgres/log volumes; rebuild with Compose after dependency changes. Rerun using saved inputs; canonical storage is idempotent. Review actual child Silver state independently of Bronze success.

### [2026-11-16 America/Bogota] - Local pgAdmin connection verification

- **Objective/status:** resolve the reported `weather` authentication failure on localhost:5432; verified the project's distinct published port.
- **Branch/commit:** `workflow-2`, uncommitted local work; no push.
- **Files changed:** `docs/WSL_SETUP.md` now uses host port 55432 and includes pgAdmin instructions. Compose and `.env.example` already publish that port in the current working tree.
- **Decision:** use `127.0.0.1:55432` from Windows/WSL, retaining `postgres:5432` inside Compose; preserve the separate native PostgreSQL installation and existing volume.
- **Verification/evidence:** `docker compose ps` reported healthy PostgreSQL with `127.0.0.1:55432->5432/tcp`. A psycopg2 password-authenticated connection through that host port returned `weather_monitoring`, user `weather`, and 1,345 historical records. No weather-service request was made.
- **Error/correction:** localhost:5432 targets the separate Windows service; the setup example incorrectly retained that host port and is corrected.
- **Limitations/input/handoff:** Kevin reported the pgAdmin error. The agent verified database connectivity; Kevin must reopen the saved pgAdmin connection with the documented port/password. No GUI success or workshop approval is claimed.
- **Recovery:** clear pgAdmin's saved password and reconnect using the configured local password. Do not reset volumes or stop native PostgreSQL services.

### [2026-11-16 America/Bogota] - G0/G1/G2 partial - Review pull and execute WSL/PostGIS pilot

- **Objective:** review `f7d7c55`, retain fixes and continue the saved-data historical path using Kevin's selected WSL runtime.
- **Status:** runtime/expanded validation and actual minimal PostGIS pilot verified; full domain/geography/history/Airflow/Parquet/report remain open.
- **Branch/commit:** `workflow-2` at `f7d7c55`, clean at start; no commit/push.
- **Requirements:** reproducibility, canonical validation, transactional reject/state/metrics integrity, real DB evidence and truthful output scope.
- **Files:** validator, transaction lock/timestamps, portable test/receipt runner, real DB tests and verification script, runtime dependency pin, WSL setup, test/readme/plan/board/review, ignore rule and JSON receipts; no approved Workshop 1 artifact changed.
- **Implementation/decisions:** preserve R1-R3 fixes and native captures; validate identity/provenance/time/coordinates/units before SQL. Serialize source loads with advisory transaction lock; do not count missing zone points as invalid. Three real DB tests use/clean only generated UUID schemas. Keep a separate Linux Python environment.
- **Verification:** Ubuntu WSL 2 works; user manual Desktop launch restored Docker Server 29.7.2/Compose 5.4.0. Compose config/up --wait passed, PostGIS 16-3.7 healthy. Isolated Linux Python 3.14.4 with driver 2.9.11 passed pip check. Final suite: 20 passed, zero skips/failures. First real load: NOAA 250/GHCN 1,095 accepted; rerun zero accepted/1,345 unchanged and zero duplicates. CLI historical/status executed. Real quarantine/rerun, mid-run rollback and prior checkpoint preservation tests pass.
- **Evidence:** dated WSL/database review, `workshop_2/evidence/wsl_test_results.json`, `database_verification.json`, tests/code and WSL runbook.
- **Errors/corrections:** plain discovery import path fixed by runner. App-context Desktop startup gave socket-access error; user manual Windows Start launch worked with no socket removal/reset. Ubuntu lacked ensurepip: installed venv package. 2.9.10 wheel unavailable on 3.14: changed runtime to 2.9.11. An intermediate host-shell interpolation emptied the DB test URL; explicit assignment reran all real tests and replaced receipt. Documentation patch contexts re-read/corrected after rejection.
- **Risks/limits:** current canonical rows upsert; final domain/geography/revision history pending. Advisory locking not stress-tested; full Python 3.12 notebook lock not tested on Linux 3.14. Pilot is saved 2024/2025 samples, not statewide multi-year/DAG coverage. Service/volume left running; no live weather query, personal approval or completed Workshop 2 claimed.
- **Input:** Kevin requested review/corrections/continuation and WSL; reported socket error and confirmed successful manual launch.
- **Handoff:** domain/geography/revision completion, then Airflow TaskFlow/FileSensor, Parquet and output notebook/PDF/sample package. Ownership stays on single board.
- **Recovery:** regenerate pilot/receipts from registered local samples; recreate Linux venv from pinned runtime. Do not remove volume to prove reruns. Integration cleanup only drops its own UUID schema; preserve Workshop 1.

### [2026-11-16 America/Bogota] - G0/G2 partial - Docker diagnosis and PostGIS Compose draft

- **Objective/status:** respond to installed Docker and prepare a local PostGIS service for the first real Workshop 2 migration; configuration drafted, daemon/database execution pending.
- **Branch/commit:** `workflow-2` with existing uncommitted G1/G2 changes; no commit or push.
- **Files changed:** `docker-compose.yml`, `.env.example`, `workshop_2/README.md`, Workshop 2 plan, current board and this log.
- **Decisions:** use the PostGIS project's documented `postgis/postgis:16-3.7` image, PostgreSQL 16 with a named volume, health check and host port 5432 by default. Keep schema application in the historical CLI and local credentials overrideable through untracked `.env`.
- **Verification/evidence:** Docker CLI 29.9.3 and Compose v5.7.0 found at the per-user Docker Desktop path; `docker compose config --quiet` passed. `docker version` displayed Client only and failed to connect to `dockerDesktopLinuxEngine`; `wsl --version` and `wsl --status` reported a missing path. Docker Desktop process launched but backend did not start. `git diff --check` showed no whitespace errors. Image tag checked against the official PostGIS Docker repository documentation.
- **Errors/corrections:** initial `docker` lookup failed because the per-user executable directory is not on this shell's PATH. Direct executable invocation resolved the CLI lookup. The user reported Docker Desktop asks to install/update WSL 2; engine startup remains dependent on that Windows setup/restart.
- **Limitations/input/handoff:** no image pull, database service, migration, ingestion, Airflow or Parquet run is claimed. User should run `wsl --install` or `wsl --update` in administrator PowerShell as appropriate, restart if prompted, reopen Docker Desktop and confirm `docker version` displays Server. Afterward execute Compose and database checks. The Compose file currently defines PostGIS only; application/Airflow services remain for later gates.
- **Recovery:** the named database volume is untouched because no daemon connection occurred. Review the Compose file and environment values before first service start; do not remove any pre-existing Docker volumes.


### [2026-11-16 America/Bogota] - G2 partial - Draft transactional historical CLI

- **Objective/status:** connect registered saved captures to the historical/status CLI and a per-partition PostgreSQL transaction; implementation and offline boundary tests added, real database execution pending.
- **Branch/commit:** `workflow-2` at `7f28e28` before uncommitted changes; no push.
- **Files changed:** `ingest.py`, `config/workshop2_saved_captures.json`, `requirements-workshop2.in`, `src/multi_hazard_weather_monitoring/storage/postgres_historical.py`, `tests/test_workshop2_transaction.py`, Workshop 2 README, plan, board and this log; concurrent G1 correction files remain uncommitted.
- **Decisions:** select only complete saved-capture date intervals; verify all selected bodies against the Workshop 1 hash register before schema/data writes; link raw capture, run, accepted/unchanged rows, rejects and successful state. Commit once per partition and roll back on an exception. Keep 2026 overlap evidence separate from the 2010-2025 baseline.
- **Verification/evidence:** `python -m compileall -q ingest.py src/multi_hazard_weather_monitoring` passed. Ten focused tests passed (`python -m unittest tests.test_workshop2_foundation tests.test_workshop2_transaction -q` with `PYTHONPATH=src` and authorized filesystem access), including complete-interval selection, source mismatch and injected state-write rollback. `python ingest.py --help` displayed the CLI; historical command with 2024-2025 dates returned `DATABASE_URL is required`, confirming the database path was not executed. `git diff --check` found no whitespace error. No live weather request was made.
- **Errors/corrections:** the initial sandboxed test run failed in Python's temporary-directory creation with Windows access denied; running the same ten tests with ordinary authorized filesystem access passed. The first patch for the CLI was rejected as a duplicate file operation and reapplied as an update; no partial CLI rewrite remained.
- **Limitations/input/handoff:** user confirmed Docker is not installed and asked what to download; official Docker Desktop for Windows with WSL 2 instructions were supplied. There is no Compose service, database migration result, actual historical load, rerun result, Silver Parquet or DAG evidence yet. Generic schema lacks final source-specific domain tables and full regional model. The offline fake cannot establish PostgreSQL semantics. Next: install/start Docker, add Compose/PostGIS, execute migration and load/rerun/rollback checks, then build DAG/output evidence.
- **Recovery:** saved Workshop 1 evidence is unchanged. Raw landing under ignored `data/raw/` can be reconstructed from registered samples. Revert the uncommitted CLI/loader if the schema contract changes before first migration.

### [2026-11-16 America/Bogota] - G1 partial - Correct reviewed foundation defects

- **Objective/status:** review the latest Workshop 2 planning/review commit and fix confirmed R1-R3 defects; initial R4 validator and partial R5/R6 corrections completed, full G1/G2 acceptance pending.
- **Branch/commit:** `workflow-2` at `7f28e28` before these uncommitted changes; no push.
- **Files changed:** historical source parser, raw landing, offline review script, initial validation module, SQL draft, six focused tests, Workshop 2 plan/board/README, foundation correction review and this log.
- **Decisions:** distinguish NOAA `MAGNITUDE_TYPE` from physical wind unit `kn`; require registered input hashes before landing; close temporary files before cleanup and publish manifests atomically; reject conflicting origin metadata; preserve native gzip; keep source-aware validation separate from parsing. `UNIQUE NULLS NOT DISTINCT` is selected for nullable rejection keys in PostgreSQL 16.
- **Verification/evidence:** six focused `unittest` cases passed after using an authorized workspace temporary directory. Saved-input review reproduced three captures and 1,363 accepted parsed records, with unchanged summary SHA-256 `47491AE61A721B82B10B6AAAAA470B6DB58EF10D14298C2D9126035AE265FC9E`; synthetic altered input, negative PRCP, fsync failure, gzip and conflicting origin were tested. No weather API was called.
- **Errors/corrections:** first test attempt failed with Windows access denied creating temporary directories, including under `data/raw/`; authorized execution passed all six tests. The failure arose before the target code paths and is not reported as a pipeline failure.
- **Limitations/input/handoff:** user requested review and the next implementation step. Docker and `psql` were not found on PATH, the common Docker Desktop path or uninstall registry in this session; no database, DAG or Parquet run is claimed. Full validation, source metadata/provenance, transactional loader and container setup remain.
- **Recovery:** revert this focused change if the source-unit contract is superseded; existing Workshop 1 captures and approved artifacts were not edited. Re-run the offline command and the six tests before proceeding to G2.

### [2026-11-16 America/Bogota] - W2-00/W2-12 planning - Bind work to Moodle deliverables

- **Objective:** turn the supplied checklist into an ordered plan for all deliverables without confusing offline audit with a functional pipeline.
- **Status:** delivery/implementation/acceptance plan updated; no code defect, service, DAG, output or PDF marked complete.
- **Branch/commit:** `workflow-2` at `c2380c9`; earlier uncommitted pull-review documentation preserved. No commit or push.
- **Requirements:** Technical Architecture and Pipeline Report PDF, Pipeline Output Samples and GitHub link, supported by code/notebook/run evidence.
- **Files changed:** implementation plan, Workshop 2 README, current board and this log.
- **Documentation completed:** mapped each item to artifacts/checks; added G0-G6, W2-13/W2-14, two TaskFlow DAGs/exact-file FileSensor, native CSV plus labelled JSON view, canonical DB/Parquet lineage and genuine sample-run requirements.
- **Decisions/rationale:** adopt compatible technical handout requirements now; preserve the domain discrepancy. No unrelated NLP/scraper or false native-JSON claim. Three copied files are not three run outputs; 2026 smoke data is not 2010-2025 coverage. Supporting notebook/DAGs are not extra Moodle items.
- **Verification:** plan has all three items, G0-G6 and W2-00 through W2-14. Existing guide/PDF review and R1-R6 findings used; no execution checkbox closed by planning. Docker not found on PATH/default queried paths; process/uninstall-registry query returned no entry in this session. Kevin explicitly reports Docker installed and needing launch/PATH configuration; runtime remains unverified.
- **Evidence:** user-supplied checklist, plan section 3, submission index and prior pull-review report.
- **Errors/corrections:** prior plan left technical TaskFlow/FileSensor/Parquet work conditional and lacked a direct package map. Made these explicit implementation targets, narrowed README verification claims and corrected a board patch context after inspecting its current wording.
- **Risks/limits:** runtime access and R1-R6 unresolved; multi-year coverage and actual successful runs need evidence. Native CSV/derived JSON is a transparent weather adaptation, not professor clarification. No team approval or upload inferred for Workshop 2.
- **Input:** Kevin supplied the three-item notice/requested completion-ready plans and confirmed Docker installed. Moodle was not independently authenticated.
- **Handoff:** G0/G1 can progress independently; execute G2-G6 with actual results before checking completion. Ownership stays on the single board.
- **Recovery:** revise proposals if corrected instructions arrive; retain dated evidence, source work and approved Workshop 1 files. No weather query, database run, output package or PDF build occurred.

### [2026-11-16 America/Bogota] - Pull review - Pablo's historical foundation

- **Objective:** review pulled Workshop 2 work against the course contract, current guide/practice and actual execution.
- **Status:** review complete; useful partial foundation, confirmed defects and completion gaps recorded; no production fix or acceptance claimed.
- **Branch or commit:** `workflow-2` at `c2380c9`, including Pablo's `c507a19` and merge `39844db`; clean before review.
- **Requirements addressed:** historical parsing, raw evidence, units, validation, provenance, recoverability, canonical schema and Airflow/layer expectations.
- **Files changed:** new dated pull-review report; review reference in the plan and board; this log. Existing source/schema code and Workshop 1 approved artifacts preserved.
- **Implementation/documentation completed:** classified the three-file offline audit as preparation, mapped strengths and R1-R6 issues, recorded current academic hashes and ordered next actions.
- **Decisions/rationale:** keep the modular foundation; correct physical units, enforce registered capture identity and repair Windows cleanup before extending it into a claimed pipeline. Treat absent canonical validation/DB/domain/DAG/Parquet as unfinished work, not passed tests.
- **Verification/exact result:** real offline command reproduced 250 NOAA, 1,095 GHCN 2025 and 18 GHCN overlap records (1,363 total, zero parser rejects). Repeated synthetic landing reused one body; actual NOAA 1155308 emitted unit MG. Synthetic altered input was processed without expected-hash validation; synthetic negative PRCP was accepted; injected fsync failure yielded PermissionError and left one temporary file. Synthetic gzip was labelled csv; changed origin replaced its manifest field. These probes did not alter weather samples. Six inherited Workshop 1 manifest hashes match. Current guide, Compose, three DAGs and Workshop 2 PDF checked against official GitHub. Docker/psql not found on session PATH; no SQL/container result claimed.
- **Evidence:** `docs/reports/workshop-2-pull-review-2026-11-16.md`, exact source locations and primary references there; original offline summary remains unchanged semantically.
- **Errors/corrections:** no production code corrected in this review. Current-unit interpretation checked against NOAA bulk specification; nullable UNIQUE behavior checked against PostgreSQL 16 docs. Runtime data examples and synthetic fixtures are distinguished.
- **Risks/limits:** parser accepted counts are not canonical quality acceptance, raw file reuse is not DB idempotency, DDL is unexecuted and the guide/handout trigger/format differences remain visible. No teacher/student approval, full multi-year coverage or source availability was inferred.
- **Input:** Kevin requested review of the teammate pull and alignment with professor guide/classes before continuing Workshop 2.
- **Handoff:** implement/test R1-R3, canonical validation and transaction/storage path, then Docker/Airflow and real Silver/report evidence; ownership remains on the single board.
- **Recovery:** review is documentation only. Rerun the offline command from preserved samples; retain confirmed issue evidence and update dispositions only when actual fixes/checks pass. No weather query, commit or push performed by this review.

### [2026-11-16 America/Bogota] - W2 integration - Inherit completed Workshop 1 evidence

- **Objective/status:** pull the four latest remote Workshop 1 commits and integrate the local Workshop 2 foundation; local merge completed, remote push not performed.
- **Branch/commit:** protected local Workshop 2 work in `c507a19`, fetched origin and merged `origin/workflow-1` at `6fea29b` into `workflow-2` as `39844db`. Both remote workflow branches pointed at `6fea29b` when fetched.
- **Files changed:** inherited Workshop 1 wind-pair evidence, 14-page report, notebook/receipts and raw-sample byte policy; Workshop 2 parser, raw-landing, SQL and offline summary retained. Current navigation/status corrections are a follow-up local edit.
- **Decision:** use the new five historical wind candidates as Workshop 1's primary overlap evidence. Preserve all approved Workshop 1 artifact bytes; treat the recorded team approval and clean reproduction as scoped evidence. Continue Workshop 2 from its existing source-specific adapters.
- **Verification/evidence:** merge resolved automatically with no conflicts. After merge, `review_offline_captures.py` again produced three captures and 1363 parsed records with NOAA SHA-256 `987F5C64...`, matching the registered source; the summary did not change. Current Workshop 1 manifest hashes match six of six artifacts, notebook has 32/32 executed cells with zero stored errors, and PDF has 14 pages. Raw sample files under `data/raw/` remain ignored.
- **Errors/corrections:** initial sandboxed `git fetch` could not write `.git/FETCH_HEAD`; authorized Git execution fetched successfully. Stale Workshop 1 navigation text was corrected separately; no approved PDF/sample/mapping was edited.
- **Limitations/input/handoff:** user requested pull, full Workshop 1 audit and merge. Moodle upload is unrecorded; Docker, database, DAGs, Silver Parquet and Workshop 2 report remain open. Local branch is ahead of remote by integration commits; no push.
- **Recovery:** local history retains `c507a19` and the four remote Workshop 1 commits; the merge is reviewable with `git log --graph`. Do not discard unpushed work.

### [2026-11-16 America/Bogota] - W2-03 partial - Initial historical schema

- **Objective/status:** draft relational tables for capture provenance, runs, canonical historical records, rejects and successful partition state; SQL written, migration execution pending.
- **Branch/commit:** `workflow-2` at `273f279` before uncommitted work.
- **Files changed:** `sql/001_historical_schema.sql`, this log.
- **Decisions:** keep GHCN daily date distinct from NOAA UTC event timestamp; enforce paired WGS84 coordinates and stable `(source_id, source_key)` uniqueness; link each record/reject to raw capture and run; use PostGIS Point(4326) for available coordinates. Partition state references only a successful run when application code writes it.
- **Verification/evidence:** reviewed DDL structure and ran `git diff --check`. PostgreSQL/PostGIS and Docker were unavailable in this session; no migration or integration result is claimed.
- **Errors/corrections:** none observed at the SQL review stage.
- **Limitations/input/handoff:** domain-specific NOAA/GHCN tables, schema migration runner, transactional upsert/rejection/state update, and live database validation remain open. User requested continued Workshop 2 implementation.
- **Recovery:** revise the draft before first application; once deployed, use a versioned follow-up migration rather than editing applied SQL.

### [2026-11-16 America/Bogota] - W2-04 partial - Content-addressed offline raw landing

- **Objective/status:** connect saved historical captures to a byte-preserving Bronze landing and reproduce a bounded parser audit; completed for the three saved samples, live acquisition and pipeline persistence pending.
- **Branch/commit:** `workflow-2` at `273f279` before uncommitted work.
- **Files changed:** `src/multi_hazard_weather_monitoring/storage/raw_landing.py`, `scripts/workshop_2/review_offline_captures.py`, `workshop_2/README.md`, `workshop_2/samples/offline_capture_review.json`, root README, board, plan and this log.
- **Decisions:** store original CSV bytes by source, partition and SHA-256 under ignored `data/raw/`; write deterministic JSON manifests separately. The summary is explicitly labeled an offline parser review, not a DAG-generated Bronze JSON or Silver Parquet sample. The original Workshop 1 evidence is unchanged.
- **Verification/evidence:** ran `python scripts/workshop_2/review_offline_captures.py` twice. Each run reported three captures and 1363 parsed records: NOAA 250, GHCN 2025 1095 measurements and GHCN 2026 overlap 18. All three had zero rejected rows and distinct keys equal to row counts. Landing hashes match registered source hashes `987F5C64...`, `D8EE9E0A...` and `7456D668...`. Summary SHA-256 `47491AE61A721B82B10B6AAAAA470B6DB58EF10D14298C2D9126035AE265FC9E`; raw captures/manifests are Git-ignored. Re-ran after making manifest paths relative to the raw root; summary hash remained unchanged. Python compilation and `git diff --check` passed.
- **Errors/corrections:** none in the two saved-sample runs. These checks do not establish database-level idempotency or failure recovery.
- **Limitations/input/handoff:** user asked to continue Workshop 2. The raw landing receives already saved evidence rather than new HTTP responses; original retrieval metadata remains in Workshop 1 sidecars. Database transaction, state, DAG execution, Parquet, three DAG-produced files per layer and final PDF remain open.
- **Recovery:** rerun the script from the repository root to reconstruct ignored raw landing and the small summary; no source download is required.

### [2026-11-16 America/Bogota] - W2-05/W2-06 partial - Offline historical parsers

- **Objective/status:** begin the source-specific historical path from saved Workshop 1 evidence; parsers complete for current samples, full adapters and storage pending.
- **Branch/commit:** `workflow-2` at `273f279` before uncommitted changes.
- **Files changed:** `src/multi_hazard_weather_monitoring/sources/historical_samples.py`, Workshop 2 plan, board and this log.
- **Decisions:** retain NOAA event time with the source's explicit `CST-6` offset; retain GHCN as a daily measurement without inventing a UTC instant. Preserve flags, nullable coordinates, source keys, source row hashes and original parsed fields. Unsupported NOAA timezone and invalid identifiers/coordinates yield rejected records with reasons.
- **Verification/evidence:** ran the parsers offline against the saved 250-row NOAA sample, 365-day GHCN 2025 capture and 6-day GHCN 2026 overlap capture. Results respectively: 250/0 rejected/250 distinct source keys; 1095/0/1095; 18/0/18. Minimal malformed inputs returned `missing_event_id` and `nonfinite_number`. `git diff --check` passed. No live weather request, database write or Parquet export was performed.
- **Errors/corrections:** none in this sample parser run. The sample does not cover every NOAA timezone or malformed fixture.
- **Limitations/input/handoff:** user authorized moving Workshop 2 forward and requested alignment with the current course practice. Annual discovery, station inventory, raw byte landing, canonical validation, quarantine persistence, database transaction, DAGs and pipeline output samples remain next. This code is not an end-to-end pipeline.
- **Recovery:** revert this source module and its documentation entry if a different source contract is accepted; Workshop 1 evidence files were not modified.

### [2026-11-16 America/Bogota] - W2-00/W2-01 - Review current professor pipeline and classes

- **Objective/status:** inspect recent course changes and translate the current practice into the weather architecture; research complete, implementation still pending.
- **Branch/commit:** `workflow-2` at `273f279` before these uncommitted documentation edits.
- **Files changed:** `docs/reports/workshop-2-course-material-review-2026-11-16.md`, Workshop 2 plan and change log.
- **Decisions:** retain native CSV/gzip Bronze evidence and canonical PostgreSQL/PostGIS Silver; use deterministic partitions, transactional curation, explicit rejects and traceable Parquet exports. Treat the example DAG as a pattern, not a copied weather implementation.
- **Verification/evidence:** read public `main` head `7a54da476f500bdd80a48feccbbab048925bc155`; latest course commit `3f7010d` (2026-11-16) revised all three earthquake DAGs and added two Gold Parquet examples. Read current Compose and DAGs, commit diff, Airflow/PostgreSQL guide and ETL/curation slides. No weather request, container run or pipeline output was performed.
- **Errors/corrections:** ordinary web browsing could not open the GitHub tree; a read-only sparse Git clone verified the files. The current practice has no TaskFlow or FileSensor, so the separate handout cannot be presented as implemented by the practice.
- **Limitations/input/handoff:** the handout still describes the 2026-I public-opinion project. User requested review of recent professor materials. Next: implement the saved-sample offline historical path, then Docker/Airflow execution and real output evidence. No professor clarification or team approval is inferred.
- **Recovery:** this entry is documentary; revise architecture choices if corrected course instructions arrive.

### [2026-11-16 America/Bogota] - Handoff - Workshop 1 acceptance audit

- **Objective/status:** inherit the evidence/status corrections without losing Workshop 2 planning; completed, no Workshop 2 implementation.
- **Branch/commit:** focused Workshop 1 audit commit `9b011dd`, fast-forwarded into `workflow-2`; no push or submission.
- **Files/requirements:** inherited acceptance A01-A09, current PDF/compliance review, offline quality/pair audit and evidence hashes; restored existing Workshop 2 plan/log/start-review and combined board updates.
- **Decision/rationale:** same-event interpretation remains open despite eight reproduced daily rows; previous workstream review is not new approval. Workshop 2 planning must not silently mark Workshop 1 accepted.
- **Verification/evidence:** Q1-Q6 assertions, nine captured checksums and eight-row reproduction pass. Thirteen-page PDF and matching ZIP verified. Three stashed planning files were compared byte-for-byte after newline normalization before this handoff annotation; no unmerged paths remain.
- **Errors/correction:** stash restoration conflicted in the board's adjacent status rows. Resolved by retaining the corrected Workshop 1/Pablo status and the existing Workshop 2 planning/next-action rows. The initial subprocess Git lookup was inaccessible; explicit bundled Git verified preservation successfully.
- **Limitations/input/handoff:** Kevin requested a Workshop 1 acceptance audit, not new personal approvals, source downloads or Workshop 2 implementation. A02 interpretation review, A03 same-event semantics, current student review and submission reference remain open.
- **Recovery:** focused commit is reversible; the previous planning content is preserved with its new handoff annotation. Do not discard the uncommitted Workshop 2 planning files.

### [2026-11-16 America/Bogota] - Handoff - Inherit the unsubmitted Workshop 1 architecture correction

- **Objective/status:** preserve Workshop 2 planning while correcting Workshop 1, then resume on `workflow-2`; completed without implementation.
- **Branch/commit:** Workshop 1 correction `009e628`, fast-forwarded into `workflow-2`; no remote push. Pre-existing planning changes restored from the task-specific stash without conflicts.
- **Requirements/files:** inherited ADR 0005, report/diagram and architecture documentation; updated this log, plan architecture reference and current board clarification.
- **Decision/rationale:** use the explicitly selected Airflow/medallion workflow; retain native raw evidence and canonical PostgreSQL storage with Silver Parquet exports. NLP/scraping discrepancy remains separate.
- **Verification/evidence:** focused commit exists on both local branches; revised PDF remains thirteen pages, rendered and inspected; ZIP inputs/assets match byte-for-byte. Samples and executed notebook unchanged. Final branch is `workflow-2` with prior planning files restored; no weather requests.
- **Errors/limitations:** no Git conflict; infrastructure and deployment configuration remain unimplemented and technical details still need review. No final student approval, push or submission is claimed.
- **Input/handoff:** Kevin requested the return to Workshop 1 and subsequent return to Workshop 2; continue W2-01/W2-02 using ADR 0005.
- **Recovery:** the focused architecture commit is reversible. Preserve the restored uncommitted Workshop 2 planning files before any later branch operations.

### [2026-11-16 America/Bogota] - W2-00 - Reverify requirements and start sequence

- **Objective:** explain the complete Workshop 2 path using current professor files and the actual repository state.
- **Status:** review and execution sequence recorded; implementation not started; specification discrepancy remains open.
- **Branch or commit:** `workflow-2`, created by Kevin; uncommitted planning changes only.
- **Requirements addressed:** architecture/historical milestone, source scope, academic precedence, conditional DAG/output requirements and demonstrable completion.
- **Files changed:** implementation plan metadata, `WORK_BOARD.md`, this log and `docs/reports/workshop-2-start-review-2026-11-16.md`.
- **Implementation or documentation completed:** recorded current source hashes, real practice operators/services, ordered offline-first build sequence, multi-year requirement and preflight limits.
- **Decisions and rationale:** reuse the practice's interval/raw/database/orchestration patterns; preserve native captures and quarantine invalid records. Treat TaskFlow/FileSensor/JSON layer wording explicitly rather than claiming the practice and PDF match.
- **Verification and exact result:** current public Workshop 2 and CourseProject hashes match local copies; all seven Workshop 2 pages read and historical milestone checked. Current Compose and all three practice DAGs inspected. Branch is `workflow-2`; tree was clean before documentation edits. `ingest.py` remains a stub. Docker CLI not found on session PATH; no daemon/container validation claimed.
- **Evidence location:** dated start review and prior specification-conflict review.
- **Errors found and correction:** web reader could not retrieve GitHub; direct read-only official GitHub access succeeded after network escalation. No weather endpoint was called.
- **Risks or limitations:** professor clarification, Docker access, architecture acceptance and multi-year coverage remain pending.
- **Input received from:** Kevin confirmed the new branch and requested the professor-aligned sequence to finish Workshop 2.
- **Handoff to:** start W2-01/W2-02 preflight and design; use saved samples for the first end-to-end path before bounded authorized acquisition.
- **Recovery or rollback:** revise the proposed sequence if corrected instructions arrive; retain this dated evidence and preserve Workshop 1 artifacts.

### [2026-11-10 America/Bogota] - Planning - Initial Workshop 2 plan

- **Objective:** translate the 2026-II historical-ingestion milestone and the conflicting Workshop 2 PDF into a reviewable, evidence-gated Team 9 plan.
- **Status:** [x] Plan created; [!] implementation has not started and specification clarification is pending.
- **Branch or commit:** planning performed on `workflow-1` at base `3304d4b`; no implementation commit created.
- **Requirements addressed:** planning metadata, requirement interpretation, minimum demonstration, P0/P1/out-of-scope work, ownership, dependencies, acceptance and merge gate.
- **Files created:** `deliveries/02-workshop-2/IMPLEMENTATION_PLAN.md`, this change log, `docs/reports/workshops-2-4-specification-review.md`, and `docs/reports/project-status-2026-11-10.md`.
- **Files modified:** `PROJECT_CONTEXT.md`, `WORK_BOARD.md`, `README.md`, `docs/plans/semester-roadmap.md`, `docs/reports/academic-material-review.md`, `docs/references/academic-materials.md`, and `deliveries/README.md`; Workshop 3-4 plans maintain their own planning entries.
- **Implementation or documentation completed:** assigned NOAA/database/CLI leadership to Kevin and GHCN/orchestration/evidence leadership to Pablo; separated safe historical/database work from conditional Bronze/Silver requirements.
- **Decisions and rationale:** the 2026-II natural-hazard contract takes precedence until the professor resolves the 2026-I public-opinion wording. Airflow is a provisional compatibility choice, not yet an accepted ADR.
- **Verification and exact result:** reviewed all seven pages of `Workshop_2.pdf`, its rendered title/deliverable/submission pages, the 2026-II course contract, Team 9 context and current repository state. Structural validation found 10/10 required plan sections in each plan, 13 Workshop 2, 12 Workshop 3 and 14 Workshop 4 P0 task IDs, zero pre-checked implementation tasks, 15/15 required change-log fields in each new log, and 8/8 required planning files present. `git diff --check` passed with only informational CRLF-to-LF warnings. No code, service or ingestion execution is claimed.
- **Evidence location:** `docs/reports/workshops-2-4-specification-review.md` and the implementation plan.
- **Errors found and correction:** the published PDF refers to API plus scraping, NLP and forced Bronze JSON, which do not describe Team 9. These were moved to incompatible/conditional scope instead of being copied as requirements. The first PowerShell change-log checker used an ambiguous variable interpolation before `:` and failed to parse; the check was corrected with formatted strings and then passed for all three logs.
- **Risks or limitations:** target date and professor clarification are absent; exact infrastructure may change after clarification and architecture review.
- **Input received from:** Kevin requested implementation plans for every newly published workshop.
- **Handoff to:** both students to review the plan and send the clarification questions; Workshop 2 implementation starts only after the Workshop 1 closure gate.
- **Recovery or rollback:** revise the proposed plan and retain this entry if the professor supplies a corrected 2026-II PDF; do not rewrite this historical observation.
