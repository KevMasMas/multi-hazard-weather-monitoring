# Implementation Plan - Workshop 2

- **Team:** Team 9 - Pablo Garzon and Kevin Rincon
- **Target date:** TBD - no submission date appears in the reviewed specification
- **Proposed working branch:** `feat/workshop-2-historical-ingestion`
- **Proposed base:** `workflow-1` / `3304d4b` after Workshop 1 closure
- **Status:** proposed; implementation not started
- **Primary specification:** [CourseProject.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/CourseProject.pdf), Semester 2026-II
- **Secondary/conflicting specification:** [Workshop_2.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_2.pdf), labeled Semester 2026-I
- **Conflict review:** `docs/reports/workshops-2-4-specification-review.md`

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

The full 2010-2025 baseline remains the target historical scope. A smaller
partition may be used for the first demonstrable run only if the report labels it
as a test and separately proves the multi-partition path.

## 4. Non-negotiable principles

- Preserve raw responses before parsing; never rewrite the original body.
- Keep NOAA and GHCN extraction separate from canonical normalization/storage.
- Derive cleaning rules from Workshop 1 evidence; do not add generic imputation.
- Quarantine invalid rows with reasons; never silently drop them.
- Commit canonical rows, rejects, run metrics and partition state atomically.
- Use configuration/environment variables; never commit credentials.
- Do not download the full historical baseline repeatedly during development.
- Do not claim Bronze/Silver, Airflow or Parquet as mandatory until the conflict
  is clarified; document the selected architecture in an ADR.

## 5. Prioritized scope

### P0 - required compatibility core

- [ ] **W2-00 - Clarification gate:** send the six specification-conflict questions to the professor and record the response or the explicit decision to proceed under the 2026-II contract.
- [ ] **W2-01 - Architecture ADR:** select PostgreSQL/PostGIS, scheduler, raw/curated boundaries, optional Parquet role, service layout, ports, volumes and recovery model.
- [ ] **W2-02 - Reproducible environment:** create version-pinned project dependencies, Dockerfiles, Compose health checks, persistent volumes and `.env.example` variables.
- [ ] **W2-03 - Database migrations:** implement canonical/support/domain/geography tables, constraints, indexes, data dictionary and migration verification.
- [ ] **W2-04 - Raw landing:** persist body, retrieval/request metadata, source/partition, content type, byte count and SHA-256 before transformation.
- [ ] **W2-05 - NOAA historical adapter:** implement annual archive discovery/cache, deterministic partitioning, parsing, source key/content hash and resumable checkpoints.
- [ ] **W2-06 - GHCN historical adapter:** generate the Oklahoma station inventory, apply ADR 0004 coverage rules, ingest station-year partitions and preserve measurement/QC/source flags.
- [ ] **W2-07 - Canonical validation:** enforce types, UTC/date semantics, WGS84 ranges, units, required keys, missing-value policy and quarantine reasons.
- [ ] **W2-08 - CLI integration:** replace the Workshop 1 stub for `historical` and `status` while preserving the common CLI contract.
- [ ] **W2-09 - Idempotency and recovery:** prove same-partition reruns, mid-run failure rollback/resume and no state advancement before commit.
- [ ] **W2-10 - Tests:** add fixture-based unit tests for both adapters and integration tests for migrations, validation, quarantine and idempotency.
- [ ] **W2-11 - Evidence notebook:** create `notebooks/02_historical_ingestion_review.ipynb` to inspect persisted counts, nulls, rejects, partitions and provenance.
- [ ] **W2-12 - Documentation:** produce the English Workshop 2 report, architecture diagram, runbook, evidence register, README commands and exact verification results.

### Conditional scope from the 2026-I PDF

- [ ] Use Airflow TaskFlow DAGs and a FileSensor only if confirmed or selected by ADR.
- [ ] Add Bronze/Silver nomenclature and at least three persisted outputs per layer only if confirmed.
- [ ] Add Silver Parquet files as curated/export artifacts without replacing the required canonical relational database.
- [ ] Document local Airflow UI evidence at `localhost:8080` if Airflow is selected.

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

### Kevin - NOAA and canonical database workstream

**Reviewer:** Pablo

- [ ] Lead W2-02/W2-03 database, migrations, constraints and CLI integration.
- [ ] Implement W2-04 raw-capture contract shared by all adapters.
- [ ] Implement W2-05 NOAA annual historical adapter and cache/partition logic.
- [ ] Define NOAA canonical/domain mapping, validation and duplicate keys.
- [ ] Add NOAA and database tests plus exact run metrics.

### Pablo - GHCN and orchestration workstream

**Reviewer:** Kevin

- [ ] Lead scheduler/Compose integration and service runbook after W2-01.
- [ ] Implement W2-06 Oklahoma station inventory and GHCN station-year adapter.
- [ ] Implement station/region persistence and GHCN measurement/QC normalization.
- [ ] Add GHCN tests and evidence notebook sections.
- [ ] Assemble architecture/report evidence and demonstration screenshots.

### Shared decisions and integration

- [ ] Send/record W2-00 clarification and accept W2-01 ADR together.
- [ ] Review schema, data dictionary, missing-value rules and quarantine taxonomy.
- [ ] Pair on the first end-to-end historical run and destructive-failure simulation.
- [ ] Cross-review every acceptance result and approve the submission commit.

## 7. Dependencies and handoffs

1. Close Workshop 1 PDF/cross-review and freeze accepted mapping/contracts.
2. Resolve or explicitly record the W2-00 specification conflict.
3. Accept W2-01 before adding infrastructure files.
4. Migrations and raw-capture storage precede source adapters.
5. Each adapter hands raw fixtures, normalized records, rejects and run metrics to
   the shared validation/idempotency tests.
6. Workshop 2 hands Workshop 3 a stable database, raw-capture API, run audit,
   source keys, content-hash rules and `status` command.

## 8. Acceptance criteria

- [ ] A fresh clone follows README instructions without undocumented manual steps.
- [ ] Required services become healthy and persistent data survives restart.
- [ ] Both historical sources load through the common CLI for a bounded test range.
- [ ] Raw capture checksum and normalized/raw references are queryable for sampled rows.
- [ ] Invalid fixture rows enter quarantine with stable reason codes.
- [ ] A repeated historical run produces zero duplicate business keys and unchanged counts.
- [ ] A simulated halfway failure leaves no partial committed partition or advanced state.
- [ ] Tests run without live APIs and their exact pass/fail counts are logged.
- [ ] Notebook/report counts reconcile with database and ingestion-run metrics.
- [ ] English report, citations, limitations and repository commit are recorded.

## 9. Merge gate

- [ ] The non-owner reviewed the complete diff and can explain both adapters.
- [ ] Automated tests, migration checks and the clean historical rerun passed.
- [ ] Evidence and limitations are recorded in this delivery's `CHANGE_LOG.md`.
- [ ] Architecture/schema decisions were promoted to `docs/decisions/`.
- [ ] Generated database volumes, bulk data, secrets and unrelated files are absent.
- [ ] The professor conflict response or adopted precedence is recorded.

## 10. Required contributor handoff

Every completed task must add a `CHANGE_LOG.md` entry with its task ID, commit,
exact command/result, evidence location, limitations and rollback instructions.
No task becomes complete solely because code exists.
