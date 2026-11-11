# Implementation Plan - Workshop 3

- **Team:** Team 9 - Pablo Garzon and Kevin Rincon
- **Target date:** TBD - no submission date appears in the reviewed specification
- **Proposed working branch:** `feat/workshop-3-incremental-integration`
- **Proposed base:** accepted Workshop 2 delivery commit
- **Status:** proposed; implementation not started
- **Primary specification:** [CourseProject.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/CourseProject.pdf), Semester 2026-II
- **Secondary/conflicting specification:** [Workshop_3.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_3.pdf), labeled Semester 2026-I
- **Conflict review:** `docs/reports/workshops-2-4-specification-review.md`

## 1. Requirement interpretation

The authoritative 2026-II contract assigns Workshop 3 to incremental ingestion
and integration: NWS Alerts and NWS station observations, scheduled polling,
watermarks/state, new/changed detection, retries, deduplication, idempotency,
failure recovery and cross-source event identification.

The new Workshop 3 PDF instead requires PySpark Silver-to-Gold processing,
governance KPIs and sentiment storytelling. Pipeline improvement and grounded
data-quality metrics are reusable ideas. NLP, sentiment and replacing incremental
integration with a Gold-only milestone are conditional until clarified.

## 2. Non-negotiable objective

Run the two NWS sources repeatedly without losing, duplicating or silently
overwriting records. The system must preserve every raw poll, distinguish new,
unchanged and changed source records, advance state only after successful commit,
recover safely from failure, and create auditable candidate event groups using
versioned temporal/geographic rules.

## 3. Minimum demonstrable result

1. `python ingest.py --mode incremental` polls both configured NWS sources through
   source-specific adapters and records a run even when a response is empty.
2. First, repeated unchanged and revised fixture runs demonstrate new/unchanged/
   changed classification without duplicate canonical records.
3. Source state and overlap/reconciliation windows advance only after commit.
4. A forced failure leaves the previous successful state intact and a retry
   completes without gaps or duplicate versions.
5. Scheduled execution uses the accepted orchestrator with retries, timeouts,
   backoff and observable failure state.
6. Candidate alert/station or alert/storm relationships retain matching-rule
   version, evidence and review status; no candidate is automatically “confirmed.”
7. `python ingest.py --mode status` reports last success, state age, row/version
   counts, rejects and recent failure.

## 4. Non-negotiable principles

- Treat NWS Alerts active responses as current-state snapshots unless a supported
  record watermark is empirically validated.
- Do not infer deletion from absence in a rolling/bounded response.
- Preserve source identifier and content hash so same-ID revisions remain auditable.
- Use per-source/per-station state and overlap windows; advance only after commit.
- Keep retrieval time separate from source event/observation time.
- Use recorded fixtures for automated tests; live calls belong only to authorized,
  rate-conscious validation/demo runs.
- Store event-group matches as rule-versioned inferences with review status.
- Do not implement sentiment/NLP fields for Team 9.

## 5. Prioritized scope

### P0 - required compatibility core

- [ ] **W3-00 - Clarification gate:** carry forward the professor response and confirm whether any PySpark/Gold deliverable is additionally required.
- [ ] **W3-01 - State model:** finalize `ingestion_state`, source cursor/snapshot metadata, per-station state, overlap/reconciliation configuration and state transitions.
- [ ] **W3-02 - Alerts adapter:** implement raw snapshot capture, pagination when applicable, feature normalization, stable ID/content hash comparison and active-state transitions.
- [ ] **W3-03 - Station adapter:** implement configured station polling, pagination, measurement/QC normalization, same-ID revision versions and retention-aware reconciliation.
- [ ] **W3-04 - Scheduler:** implement separate tasks/DAGs, retries, exponential backoff, timeouts, concurrency limits, User-Agent/config handling and audit logging.
- [ ] **W3-05 - Change classification:** persist deterministic `new`, `unchanged`, `changed`, `invalid` and source-state outcomes with run metrics.
- [ ] **W3-06 - Deduplication:** enforce source/version uniqueness across reruns and overlapping windows.
- [ ] **W3-07 - Event identification:** implement versioned temporal/geographic candidate rules, county/station allocation and human-review status using Workshop 1 pairs as fixtures, not truth labels.
- [ ] **W3-08 - Recovery:** test empty response, timeout, HTTP error, partial parse, database failure, schema drift, late record and restart paths.
- [ ] **W3-09 - CLI/status:** implement `incremental` and expand `status` with source freshness, state, last run and failure/row metrics.
- [ ] **W3-10 - Tests:** add fixture-driven unit/integration tests for polling, pagination, revisions, overlaps, state commits, deduplication and event matching.
- [ ] **W3-11 - Evidence/report:** create an incremental-run notebook/report, source-status updates, exact demo evidence and English PDF.

### Conditional scope from the 2026-I PDF

- [ ] Improve historical/curation pipelines when incremental evidence reveals actual schema/quality issues.
- [ ] Add PySpark local-mode processing of accumulated Parquet only if confirmed.
- [ ] Produce governance and analytical Gold Parquet datasets only if confirmed, mapping weather KPIs/user stories instead of sentiment.
- [ ] If Gold is required, define weather-specific summaries: completeness/freshness, source volume, duplicate/revision rates, regional hazard components and current/historical inputs.

### P1 - improvement after P0 is stable

- [ ] Add replay from raw captures for a chosen run/time window without network access.
- [ ] Add dead-letter/retry queue visibility and stale-state alerts.
- [ ] Evaluate matching thresholds against manually reviewed positive/negative pairs.
- [ ] Add operational metrics export for dashboard/data-health use.

### Out of scope

- Final CHI computation, baseline sensitivity and dashboard visual design: Workshop 4.
- Treating Workshop 1 candidate pairs as confirmed ground truth.
- Scraping, language detection, sentiment, keywords or NLP storytelling.
- Advancing a watermark/state after a failed transaction.

## 6. Work allocation

### Kevin - NWS Alerts and event-integration workstream

**Reviewer:** Pablo

- [ ] Lead W3-02 Alerts snapshot/version adapter and source-status semantics.
- [ ] Implement shared content-hash/change-classification and deduplication rules.
- [ ] Lead W3-07 event grouping, rule versioning and review/evaluation fixtures.
- [ ] Extend CLI `incremental`/`status` integration and Alerts tests.
- [ ] Document Alerts limitations, empty-state behavior and candidate-match evidence.

### Pablo - station polling and orchestration workstream

**Reviewer:** Kevin

- [ ] Lead W3-01 per-station state/overlap/reconciliation implementation.
- [ ] Implement W3-03 NWS station adapter, pagination and measurement/QC versions.
- [ ] Lead W3-04 scheduling, retries, timeouts and operational run evidence.
- [ ] Implement station-to-region allocation and station fixture tests.
- [ ] Assemble incremental notebook/report and demonstration sequence.

### Shared decisions and integration

- [ ] Accept state machine, polling frequency, overlap/reconciliation and failure policy.
- [ ] Review match features, thresholds, uncertainty and evaluation sample.
- [ ] Pair on forced-failure/recovery and repeated-run demonstrations.
- [ ] Decide conditional Gold/PySpark scope only after professor clarification.

## 7. Dependencies and handoffs

1. Workshop 2 must provide stable migrations, raw capture, source adapters,
   transactions, run audit and fixture infrastructure.
2. W3-01 precedes incremental adapters and scheduler state updates.
3. W3-02/W3-03 must pass source-specific fixture tests before live validation.
4. Change classification/deduplication precede event grouping.
5. Workshop 3 hands Workshop 4 database views/data contracts for current state,
   revisions, regional allocation, event groups and data-health metrics.

## 8. Acceptance criteria

- [ ] Both incremental sources run through the common CLI and scheduler.
- [ ] Empty responses are successful empty states when valid, not fabricated failures.
- [ ] Repeating unchanged fixtures creates zero duplicate records/versions.
- [ ] Same-ID changed fixtures create auditable versions and correct run metrics.
- [ ] Overlap/reconciliation tests include late and revised observations.
- [ ] Forced failure preserves the previous successful state; retry fills the interval once.
- [ ] Pagination and bounded rolling-page behavior are tested without deletion inference.
- [ ] Candidate matches store evidence, rule version and unconfirmed/reviewed status.
- [ ] `status` reports freshness, state age, counts, rejects and failures per source.
- [ ] Automated tests and documented demonstration results reconcile with database counts.
- [ ] English report, source-status log, citations and commit are recorded.

## 9. Merge gate

- [ ] The non-owner reviewed the complete diff and can explain both incremental adapters.
- [ ] New/unchanged/changed/late/invalid/empty/failure fixture scenarios passed.
- [ ] Repeated and recovery runs proved idempotency and commit-safe state.
- [ ] Event-matching limitations and evaluation evidence are explicit.
- [ ] Durable state/matching decisions were promoted to `docs/decisions/`.
- [ ] No secrets, raw bulk data, local scheduler state or generated database volumes are tracked.
- [ ] Conditional PySpark/Gold scope matches the recorded professor response.

## 10. Required contributor handoff

Every completed task must add a `CHANGE_LOG.md` entry with task ID, commit,
exact fixture/live verification, state before/after, row/version metrics, evidence,
limitations and rollback/replay instructions.
