# Implementation Plan - Workshop 2

**Documentation review, 2026-11-16:** the 12-page revised report adds literal
layer content, course-to-schema/layer naming tables, exact task/schedule/error
behavior and neutral delivery wording. Current checks are in
`workshop_2/evidence/report_revision_audit.json`; earlier pipeline results are
preserved. Base `5810ba5` is pushed; these new edits are local.

**Latest verification, 2026-11-16:** ten actual Airflow Bronze/Silver batches
processed 2021-2025: 13,561 Oklahoma events and 5,478 GHCN measurements from one
station. Canonical rerun/restart checks show zero duplicates. All 29 tests pass;
the notebook executes nine code cells with no errors. PDF/ZIP and technical
evidence are prepared for review. See the current change-log entry and
`workshop_2/EVIDENCE_REGISTER.md`.

G0/G1 and the bounded G2/G3 core are demonstrated. G4 meets the five-year slice
and three real samples; the full 2010-2025 target, statewide station inventory and
county assignments remain open. G5 artifacts are prepared; final content approval,
selected commit/push and upload (G6) require actual human actions.

- **Team:** Team 9 - Pablo Garzon and Kevin Rincon
- **Target date:** 2026-11-16, ready for team review before 21:45 America/Bogota; Kevin reports a 22:00 delivery deadline. This is user-supplied timing, not a newly verified platform response.
- **Working branch:** `workflow-2` (created by Kevin from the Workshop 1 branch)
- **Base:** inherited Workshop 1 work; exact submission reference remains a separate review item
- **Status:** technical delivery artifacts prepared for review; wider historical/station/geography scope and G6 remain open.
- **Primary specification:** [CourseProject.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/CourseProject.pdf), Semester 2026-II
- **Secondary/conflicting specification:** [Workshop_2.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_2.pdf), labeled Semester 2026-I
- **Conflict review:** `docs/reports/workshops-2-4-specification-review.md`
- **Current execution sequence:** `docs/reports/workshop-2-start-review-2026-11-16.md`
- **Pulled-code review:** `docs/reports/workshop-2-pull-review-2026-11-16.md` at `c2380c9`: offline counts reproduced; R1 units, R2 registered input hashes and R3 Windows failure cleanup must be corrected before using the foundation as a validated pipeline. R4 canonical validation, native-format/provenance and SQL/domain execution remain open. No issue is marked fixed by the review alone.
- **Foundation correction review:** `docs/reports/workshop-2-foundation-fix-review-2026-11-16.md` records R1-R3 fixes, initial R4 validation, partial R5 and static R6, with six passing focused tests. The earlier pulled-code review remains historical evidence, not the current defect status.
- **Current course-material review:** `docs/reports/workshop-2-course-material-review-2026-11-16.md` (public `main` at `7a54da4`, latest course change `3f7010d`)
- **Inherited architecture:** ADR 0005 and Workshop 1 correction commit `009e628` select Apache Airflow, native Bronze captures, Silver PostgreSQL/PostGIS plus Parquet exports and later Gold analytics. The executed deployment is now documented in ADR 0006 and the demo guide; wider scope and team review remain open.

## 1. Requirement interpretation

The authoritative 2026-II contract assigns Workshop 2 to technical architecture,
Docker, relational schema and historical ingestion for NOAA Storm Events and
GHCN-Daily. The result must normalize and validate records, handle missing values,
quarantine rejects, preserve raw provenance and remain idempotent.

The new Workshop 2 PDF instead requires Airflow TaskFlow DAGs, Bronze JSON,
FileSensor-triggered Silver Parquet and public-opinion preprocessing. Airflow,
Docker, persisted raw files, Parquet exploration and evidence of successful runs
are compatible techniques. Scraping, NLP/text cleaning and forcing every raw
weather source into JSON are not adopted without professor clarification.
The professor's revised 2026-11-16 earthquake practice uses PythonOperator and
TriggerDagRunOperator, not TaskFlow/FileSensor; it is a teaching example, not a
revision of the Workshop 2 handout. Retain this distinction during implementation.

For this implementation, adopt the compatible technical handout requirements:
two TaskFlow DAGs, a Silver FileSensor, genuine JSON/Parquet output examples and
Docker/Airflow evidence. This is the team's implementation target, not a claim
that the professor clarified the domain conflict. The 2026-II weather sources,
canonical database and provenance remain authoritative; no NLP/scraper is added.
No communication to the professor is sent or claimed by this plan.

## 2. Non-negotiable objective

From a clean clone, start the local stack and load the accepted Oklahoma
historical scope from both NOAA Storm Events and GHCN-Daily into an auditable
canonical relational model. A safe rerun must create no duplicates, invalid rows
must remain traceable in quarantine, and every stored row must link to immutable
raw evidence and an ingestion run.

## 3. Minimum demonstrable result

1. `docker compose up` starts PostgreSQL/PostGIS, the ingestion application and
   the selected scheduler/orchestrator.
2. Database migrations create source, run, state, raw-capture, canonical event,
   historical domain, geography and rejected-record structures.
3. `python ingest.py --mode historical --start YYYY-MM-DD --end YYYY-MM-DD`
   processes at least one reproducible partition from both NOAA and GHCN.
4. The run records rows read, accepted, rejected and unchanged, with source/raw
   checksums and UTC run timestamps.
5. Repeating the same partition produces identical canonical counts and no
   duplicate business keys.
6. `python ingest.py --mode status` reports the last historical runs and counts.
7. Automated tests and a notebook inspect the stored/curated output without a
   live network dependency.
8. Bronze and Silver DAGs complete real Docker/Airflow runs; at least three
   genuine JSON batch outputs and three traceable Silver Parquet outputs are
   preserved, indexed and explained. A repeated partition is tested separately
   for idempotency; copying one result to three filenames does not count.

The course project requires at least five historical years where available;
the full 2010-2025 baseline remains the team's target historical scope. A smaller
partition may be used for the first demonstrable run only if the report labels it
as a test and separately proves the multi-partition path.

### Actual submission items

The following is the Moodle checklist supplied by Kevin, not an independently
authenticated platform response. Report and sample ZIP names below now identify generated, verified artifacts; they are not empty placeholders.

| Moodle item | Planned artifact | Acceptance evidence |
| --- | --- | --- |
| Technical Architecture and Pipeline Report (PDF) | `workshop_2/report/Workshop_2_Report.pdf`; portable LaTeX source alongside it | Executed architecture, preprocessing rules, services/volumes, DAGs, real results/screenshots, challenges and citations; rendered layout reviewed. |
| Pipeline Output Samples | `workshop_2/Workshop_2_Pipeline_Output_Samples.zip`, built from `workshop_2/samples/` and documented provenance | At least 3 real Bronze JSON batches and 3 Silver Parquet outputs from distinct actual runs/partitions, plus native-source references, manifest, review notebook and concise sample README. |
| GitHub link | Reviewed `workflow-2` commit, with exact hash recorded when selected | All code/configuration/run instructions and reviewable evidence committed; no credentials, local volumes or bulk landing files. User performs push unless separately authorized. |

The notebook, DAGs and Compose are implementation/support evidence inside the
repository and sample package, not invented extra Moodle submission items.

### Execution gates (in order)

| Gate | Work | Exit condition |
| --- | --- | --- |
| G0 | Resolve Docker executable/daemon access; inspect current version and Compose support. | `docker version` and `docker compose version` run; installation/PATH/runtime state recorded, not assumed. |
| G1 | Correct R1-R3 (units, expected source hashes, failure cleanup); add W2-07 canonical validation and stable rejection codes. | Meaningful valid/invalid/altered-input/failure fixtures pass; no weather API needed. |
| G2 | Finalize native-format capture contract, provenance, domain schema and transactional storage/CLI. | Migration executes in PostGIS; both sources load from saved evidence; rejects/metrics/state commit together; rerun and rollback checks pass. |
| G3 | Build pinned Docker/Airflow stack and two thin DAGs using the same application code. | Services healthy; Bronze/Silver real runs succeed; exact-file FileSensor and persistence/retry behavior demonstrated. |
| G4 | Produce actual in-scope historical outputs, including multiple partitions/years. | Both sources covered; at least 3 authentic JSON and Parquet sample artifacts; hashes/counts reconcile. Five-year minimum where available and target 2010-2025 coverage measured before full historical-scope closure. |
| G5 | Execute notebook, package samples and complete the English LaTeX PDF/runbook. | Clean reproduction, sample ZIP provenance/content checks, visual PDF inspection and final artifact/secret review pass. |
| G6 | Team content review and delivery reference. | Explicit review record plus actual selected commit; platform upload and push recorded only if performed. |

G0 and G1 can progress independently. G2-G4 require the real container runtime;
an offline imitation cannot close Docker/Airflow/SQL evidence. The saved 2026
overlap sample is a labelled smoke-test fixture outside the 2010-2025 baseline,
not proof of accepted historical coverage. New acquisition is bounded/cached and
announced before weather requests; no download is authorized by a checked plan box.

### Planned DAG and layer contract

- **Bronze:** TaskFlow extraction/capture tasks preserve native bytes and publish
  a batch JSON atomically. For CSV sources, JSON contains a labelled parsed view
  and source metadata/raw references; it is derived, not falsely an original JSON
  response. The original CSV/gzip remains available by hash. Request/run/partition
  IDs and UTC times identify real runs.
- **Silver:** a separate TaskFlow DAG starts from a specific manifest path/run
  reference, uses FileSensor in `reschedule` mode with bounded timeout, validates
  and loads canonical/domain rows or rejects, then publishes Parquet after DB
  commit. The sensor never accepts an arbitrary old file. Bronze may trigger this
  DAG with a path via TriggerDagRunOperator, matching the current practice while
  retaining the handout's sensor. Only paths/IDs travel through XCom.
- **Retry semantics:** same input/partition must not duplicate canonical records;
  partial JSON/Parquet is not published as ready; export retries recover after a
  committed DB transaction. Manifest processing status and output lineage prevent
  old batches from being processed again as new data.
- **Scope:** manual/bounded historical runs first; no unbounded catchup or NWS
  operational polling. Gold/CHI/dashboard appear as planned components in the
  architecture; their implementation remains Workshops 3-4.

### Planned output layout

```text
docker-compose.yml
Dockerfile
airflow/dags/bronze_ingestion_dag.py
airflow/dags/silver_processing_dag.py
src/multi_hazard_weather_monitoring/...
sql/...
notebooks/02_historical_ingestion_review.ipynb
workshop_2/
  README.md
  report/main.tex, cover.tex, assets/, Workshop_2_Report.pdf
  samples/README.md, manifest.json, bronze/*.json, silver/*.parquet
  evidence/run_metrics.csv, sanitized_logs/, screenshots/
  Workshop_2_Pipeline_Output_Samples.zip
```

This is a target layout, not a statement that these files currently exist.
Bulk native captures stay in ignored storage; small deliverable samples retain
native inputs or documented download/replay references. Each sample manifest
includes source/partition/run, native hash, output hash/size/schema version,
accepted/rejected/unchanged metrics and reproduction command. Outlier/missing
policies come from Workshop 1; extremes are not deleted just because of IQR.

## 4. Non-negotiable principles

- Preserve raw responses before parsing; never rewrite the original body.
- Keep NOAA and GHCN extraction separate from canonical normalization/storage.
- Derive cleaning rules from Workshop 1 evidence; do not add generic imputation.
- Quarantine invalid rows with reasons; never silently drop them.
- Commit canonical rows, rejects, run metrics and partition state atomically.
- Use configuration/environment variables; never commit credentials.
- Do not download the full historical baseline repeatedly during development.
- Implement the selected Airflow/JSON/Parquet workflow transparently while
  retaining the canonical DB/native evidence; do not misrepresent it as a
  professor clarification or adopt unrelated public-opinion processing.

## 5. Prioritized scope

### P0 - required compatibility core

Checked implementation items below are supported by the 2026-11-16 delivery
change-log entry, actual receipts and final artifacts; they do not imply G6
approval. W2-14 packaging is prepared, while its human review/reference remains open.

- [x] **W2-00 - Requirement interpretation:** record Kevin's three-item Moodle checklist and the selected weather-compatible technical path above. [ ] Professor response only if/when received; none is claimed or sent automatically. Domain-incompatible NLP/scraping is not a prerequisite to compatible implementation.
- [x] **W2-01 - Architecture ADR (implemented, review pending):** select PostgreSQL/PostGIS, scheduler, raw/curated boundaries, optional Parquet role, service layout, ports, volumes and recovery model.
- [x] **W2-02 - Reproducible environment:** create version-pinned project dependencies, Dockerfiles, Compose health checks, persistent volumes and `.env.example` variables.
- [x] **W2-03 - Database migrations (core executed; reviewed county allocation open):** implement canonical/support/domain/geography tables, constraints, indexes, data dictionary and migration verification.
- [x] **W2-04 - Raw landing:** persist body, retrieval/request metadata, source/partition, content type, byte count and SHA-256 before transformation.
- [x] **W2-05 - NOAA historical adapter:** implement annual archive discovery/cache, deterministic partitioning, parsing, source key/content hash and resumable checkpoints.
- [ ] **W2-06 - GHCN historical adapter (one-station path executed; inventory open):** generate the Oklahoma station inventory, apply ADR 0004 coverage rules, ingest station-year partitions and preserve measurement/QC/source flags.
- [x] **W2-07 - Canonical validation:** enforce types, UTC/date semantics, WGS84 ranges, units, required keys, missing-value policy and quarantine reasons.
- [x] **W2-08 - CLI integration:** replace the Workshop 1 stub for `historical` and `status` while preserving the common CLI contract.
- [x] **W2-09 - Idempotency and recovery:** prove same-partition reruns, mid-run failure rollback/resume and no state advancement before commit.
- [x] **W2-10 - Tests:** add fixture-based unit tests for both adapters and integration tests for migrations, validation, quarantine and idempotency.
- [x] **W2-11 - Evidence notebook:** create `notebooks/02_historical_ingestion_review.ipynb` to inspect persisted counts, nulls, rejects, partitions and provenance.
- [x] **W2-12 - Documentation:** produce the English Workshop 2 report, architecture diagram, runbook, evidence register, README commands and exact verification results.
- [x] **W2-13 - Actual DAG/output evidence:** implement Bronze/Silver TaskFlow DAGs and exact-batch FileSensor, execute them in Docker, preserve at least three real JSON/Parquet outputs and reconcile sample manifest/counts.
- [ ] **W2-14 - Packaging and content review:** execute the Silver/database review notebook, build the samples ZIP and visually inspected PDF, audit artifacts/secrets, then record real team approval and selected delivery reference.

### Selected compatible handout scope (implemented for the bounded slice)

- [x] Two TaskFlow DAGs with an exact-batch Silver FileSensor, retries and logs.
- [x] At least three genuine batch JSON outputs and three traceable Silver Parquet outputs; preserve/label native CSV versus derived JSON.
- [x] Canonical PostgreSQL/PostGIS remains alongside Silver Parquet, as selected in ADR 0005.
- [x] Local Airflow UI evidence at `localhost:8080`, real DAG success and output inspection.

### P1 - improvement after P0 is stable

- [ ] Add partition manifests and replay tooling for selected source/year/station ranges.
- [ ] Add schema-drift snapshots and database constraint coverage reporting.
- [ ] Add performance measurements only after correctness and bounded test data are stable.
- [ ] Add a small make/task wrapper for common developer commands.

### Out of scope

- NWS Alerts and NWS station incremental ingestion: Workshop 3.
- Cross-source event grouping beyond schema preparation: Workshop 3.
- Compound Hazard Index, historical/current analytics and dashboard: Workshop 4.
- NLP, sentiment, web scraping and public-opinion fields: not part of Team 9.
- Unbounded full-history downloads during tests or CI.

## 6. Work allocation

### Kevin - NOAA and canonical database review handoff

**Reviewer:** Pablo

- [ ] Review the executed database/migrations/CLI and confirm the reported limitations.
- [ ] Review native/derived capture hashes and the packaged source lineage.
- [ ] Review the five NOAA annual partitions and cache/replay commands.
- [ ] Confirm canonical/domain mapping, units, missingness and duplicate-key decisions.
- [ ] Review the 29-test receipt and actual NOAA/database metrics.

### Pablo - GHCN and orchestration review handoff

**Reviewer:** Kevin

- [ ] Review the running scheduler/Compose setup and service runbook.
- [ ] Review the five-year one-station GHCN adapter; retain wider inventory as open.
- [ ] Review station/QC storage and confirm county assignments are not fabricated.
- [ ] Review the GHCN tests and nine-cell executed notebook.
- [ ] Review the assembled PDF, actual screenshot and sample ZIP.

### Shared decisions and integration

- [ ] Send/record W2-00 clarification and accept W2-01 ADR together.
- [ ] Review schema, data dictionary, missing-value rules and quarantine taxonomy.
- [ ] Pair on the first end-to-end historical run and destructive-failure simulation.
- [ ] Cross-review every acceptance result and approve the submission commit.

## 7. Dependencies and handoffs

1. Close Workshop 1 PDF/cross-review and freeze accepted mapping/contracts.
2. Use the explicitly recorded W2-00 delivery interpretation; preserve the documented domain discrepancy without blocking compatible work.
3. Accept W2-01 before adding infrastructure files.
4. Migrations and raw-capture storage precede source adapters.
5. Each adapter hands raw fixtures, normalized records, rejects and run metrics to
   the shared validation/idempotency tests.
6. Workshop 2 hands Workshop 3 a stable database, raw-capture API, run audit,
   source keys, content-hash rules and `status` command.

## 8. Acceptance criteria

- [ ] A fresh clone follows README instructions without undocumented manual steps.
- [x] Required services become healthy and persistent data survives restart.
- [x] Both historical sources load through the common CLI for a bounded test range.
- [x] Raw capture checksum and normalized/raw references are queryable for sampled rows.
- [x] Invalid fixture rows enter quarantine with stable reason codes.
- [x] A repeated historical run produces zero duplicate business keys and unchanged counts.
- [x] A simulated halfway failure leaves no partial committed partition or advanced state.
- [x] Tests run without live APIs and their exact pass/fail counts are logged.
- [x] Executed slice: 29 passing WSL tests, 19,039 canonical rows, ten successful source/year DAG pairs and unchanged rerun/restart evidence. Does not close the full semester scope or human approval.
- [x] Notebook/report counts reconcile with database and ingestion-run metrics.
- [ ] English report, citations, limitations and repository commit are recorded.
- [x] Two real DAGs and the exact-batch sensor are demonstrable in Docker, with persisted outputs and authentic UI/log evidence.
- [x] Sample ZIP contains at least three real JSON batches/three Parquet outputs, the review notebook and verifiable native/output provenance; no copied files used to manufacture counts.
- [ ] The three Moodle items map directly to reviewed local artifacts and an actual selected `workflow-2` commit; team approval/upload are not inferred.

## 9. Merge gate

- [ ] The non-owner reviewed the complete diff and can explain both adapters.
- [x] Automated tests, migration checks and the clean historical rerun passed.
- [x] Evidence and limitations are recorded in this delivery's `CHANGE_LOG.md`.
- [x] Architecture/schema decisions were promoted to `docs/decisions/`.
- [ ] Generated database volumes, bulk data, secrets and unrelated files are absent.
- [x] The professor conflict response or adopted precedence is recorded.

## 10. Required contributor handoff

Every completed task must add a `CHANGE_LOG.md` entry with its task ID, commit,
exact command/result, evidence location, limitations and rollback instructions.
No task becomes complete solely because code exists.
