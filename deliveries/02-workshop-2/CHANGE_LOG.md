# Change Log - Workshop 2

Append entries; do not silently rewrite historical observations.

## Entries

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
