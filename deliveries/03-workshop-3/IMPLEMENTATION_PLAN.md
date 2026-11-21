# Implementation Plan - Workshop 3

**Latest verification, 2026-11-21:** the real Gold DAG succeeded with 625
governance and 607 storytelling rows from 19,039 unique records. Eight new tests
and 29 W2 regressions passed; both notebooks execute without errors (7/5 cells).
Independent Pandas reconciliation and unchanged same-batch replay are recorded
in `workshop_3/EVIDENCE_REGISTER.md`. W3-G02..G05 are supported by the current
Gold change-log entry. Incremental integration, final PDF and human review remain
open. The earlier first-slice status below is historical.

**Executed first slice, 2026-11-20:** `notebooks/03_silver_quality_review.ipynb`
ran seven code cells with zero errors. Thirteen checksum-verified successful
exports reconcile 22,553 snapshot rows to 19,039 business records. Missingness,
sample skewness/excess kurtosis, IQR/Z-score comparison, positive-precipitation
and monthly context are recorded under `workshop_3/evidence/`. The all-day PRCP
IQR is zero, so that rule is explicitly unavailable for that population.
At that first-slice checkpoint, Gold and incremental integration were unimplemented;
the latest verification above supersedes its Gold status. Actual branch:
`feat/workshop-3-quality-gold`, based on `f35c75c`.

## Current technical review - 2026-11-21

This checkpoint supersedes earlier pending-status prose above. The incremental
core and English PDF are now prepared for team review. Evidence: the 2026-11-21
incremental/report closure entry in `CHANGE_LOG.md`, `workshop_3/EVIDENCE_REGISTER.md`
and `workshop_3/evidence/incremental_*.json`.

Twelve incremental tests, 29 historical regressions and eight Spark tests pass.
Saved replay ingested 238 alerts and 700 observations; the second pass was fully
unchanged. Announced live validation returned zero active OK alerts and 903 KOKC
observations, with complete returned chains and unchanged captured-byte replays.
Three actual replay DAG tasks succeeded. State/revision hashes survived a real
PostgreSQL restart. The DAG was left paused; automatic network mode is disabled.
The eight-page report, two executed notebooks and exact offline Silver archive
are reviewable. No commit/push or W3 human approval is claimed.

Remaining integration boundaries: W3-07 county/station allocation and labelled
match evaluation remain open; the implemented polygon/time rule makes only
unconfirmed intra-NWS associations. Exact classroom formula comparison and the
professor's cross-semester/domain discrepancy remain unresolved. CHI/dashboard
and broader baseline/station coverage remain later work.

## Current direction - 2026-11-20

Kevin requested classroom-aligned distribution analysis and preparation of
dashboard questions. Adopt the local Workshop 3 handout's technical Gold/PySpark,
governance, storytelling and two-notebook deliverables as implementation targets,
adapted explicitly to weather. Retain the 2026-II project's incremental/integration
workstream; Gold does not replace it. Earlier conditional-Gold wording below is
planning history, superseded by this target, not evidence of professor clarification.

### Analysis and dashboard preparation

- [ ] Audit Silver file selection before analysis: reconcile repeated exports and
  revisions by source/key and deterministic successful-run precedence. Never count
  repeated partition snapshots as independent weather observations.
- [ ] Profile PRCP, TMAX and TMIN separately by source/station/unit and time period:
  sample size, missingness, mean/median, quantiles, spread, histogram and boxplot.
  Describe skewness and excess kurtosis with the estimator/convention, missing-value
  treatment and sample size. Constant or insufficient samples produce an explicit
  unavailable statistic, not an invented zero.
- [ ] Choose the outlier-review method per variable from observed distribution and
  course examples. Use 1.5-IQR as a robust initial candidate for skewed data;
  compare Z-score only when its mean/standard-deviation interpretation is justified.
  Z-score 3 and IQR 1.5 are proposed starting thresholds, not automatic instructor
  requirements or proof of an erroneous observation. Document sensitivity and
  the zero-IQR/zero-standard-deviation cases.
- [ ] For precipitation, report the zero proportion and distinguish all-day versus
  wet-day distributions; define the wet-day threshold explicitly. For temperature,
  inspect seasonality before calling a pooled extreme anomalous. Preserve extremes
  and raw values; separate physical-invalidity quarantine from statistical flags.
- [ ] Record observation -> evidence -> selected rule -> justification -> result.
  No cleaning change is accepted solely because skewness/kurtosis is high. Confirm
  exact classroom formula conventions against available slides/notebooks before
  claiming they reproduce the professor's method. Current remote slide retrieval
  failed; no exact lesson wording is claimed by this plan.
- [ ] Implement the scheduled Gold DAG with local-mode PySpark, two typed outputs
  (governance/storytelling), provenance and verified multi-Parquet consolidation.
  Notebook exploration uses Pandas; reusable Gold calculations use PySpark.
- [ ] Define dashboard questions and corresponding Gold fields before UI work.
  Plotly Dash is the course-project application; this milestone prepares its data
  and narrative rather than claiming a finished dashboard.

| Analysis | Weather question / proposed view | Evidence boundary |
| --- | --- | --- |
| Descriptive | What was recorded? Monthly event counts/types and station distributions. | Distinguish reported events from daily measurements; show coverage and units. |
| Diagnostic / exploratory | Which periods, types or locations accompany an observed peak? Filtered comparisons and associations. | Association does not establish cause; verify station/county allocation. |
| Predictive | What might happen next? | No forecast is implemented or required by this direction. A forecast needs a separate approved target, temporal validation and uncertainty; historical trends/CHI are not predictions. |
| Prescriptive / decision support | What should a user inspect first? Quality/freshness flags and documented monitoring priorities. | Proposed monitoring support, not optimized interventions or official safety instructions. |

Do not fabricate a panel for every analysis type. The current project objective
is monitoring/correlation. Descriptive and exploratory diagnostic views are the
initial implementable narrative; predictive/prescriptive capability must be
labelled as absent or proposed unless separately justified and validated.

- **Team:** Team 9 - Pablo Garzon and Kevin Rincon
- **Target date:** TBD - no submission date appears in the reviewed specification
- **Working branch:** `feat/workshop-3-quality-gold`
- **Base:** Workshop 2 technical commit `f35c75c`; final personal approval/upload is separate
- **Status:** Gold, incremental core and report technically verified; human review and listed integration boundaries remain open
- **Primary specification:** [CourseProject.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/CourseProject.pdf), Semester 2026-II
- **Secondary/conflicting specification:** [Workshop_3.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_3.pdf), labeled Semester 2026-I
- **Conflict review:** `docs/reports/workshops-2-4-specification-review.md`

## 1. Requirement interpretation

The authoritative 2026-II contract assigns Workshop 3 to incremental ingestion
and integration: NWS Alerts and NWS station observations, scheduled polling,
watermarks/state, new/changed detection, retries, deduplication, idempotency,
failure recovery and cross-source event identification.

The published Workshop 3 PDF requires PySpark Silver-to-Gold processing,
governance KPIs and storytelling. Adopt its technical deliverables with weather
aggregations under Kevin's current instruction. Keep the project-level
incremental workstream; Gold does not replace it. NLP/sentiment is excluded for
Team 9, and no professor clarification is implied.

## 2. Non-negotiable objective

Run the two NWS sources repeatedly without losing, duplicating or silently
overwriting records. The system must preserve every raw poll, distinguish new,
unchanged and changed source records, advance state only after successful commit,
recover safely from failure, and create auditable candidate event groups using
versioned temporal/geographic rules.
Also consolidate reviewed Silver exports with local PySpark into traceable
governance/storytelling Gold datasets, with quality findings and dashboard
questions grounded in observed data rather than invented model results.

## 3. Minimum demonstrable result

1. `python ingest.py --mode incremental --source <source> --scope <scope>` polls a configured NWS source through
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
8. A scheduled local Spark Gold DAG publishes actual governance/storytelling
   Parquet summaries with verified input lineage and independent reconciliation.
9. The quality and Gold-preview notebooks execute from fresh kernels; the report
   distinguishes implemented historical context from pending live integration.

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

- [x] **W3-00 - Requirement interpretation:** adopt weather-compatible Gold/PySpark tasks under Kevin's instruction and retain the incremental workstream; no written professor clarification is claimed.
- [x] **W3-01 - State model:** finalize `ingestion_state`, source cursor/snapshot metadata, per-station state, overlap/reconciliation configuration and state transitions.
- [x] **W3-02 - Alerts adapter:** implement raw snapshot capture, pagination when applicable, feature normalization, stable ID/content hash comparison and preserved lifecycle fields; absence never implies deletion.
- [x] **W3-03 - Station adapter:** implement configured station polling, pagination, measurement/QC normalization, same-ID revision versions and retention-aware reconciliation.
- [x] **W3-04 - Scheduler:** implement separate tasks/DAGs, retries, exponential backoff, timeouts, concurrency limits, User-Agent/config handling and audit logging.
- [x] **W3-05 - Change classification:** persist deterministic `new`, `unchanged`, `changed`, `invalid` and source-state outcomes with run metrics.
- [x] **W3-06 - Deduplication:** enforce source/version uniqueness across reruns and overlapping windows.
- [ ] **W3-07 - Event identification:** implement versioned temporal/geographic candidate rules, county/station allocation and human-review status using Workshop 1 pairs as fixtures, not truth labels. Polygon/time candidates and status are implemented; reviewed county allocation and labelled evaluation remain pending.
- [x] **W3-08 - Recovery:** test empty response, timeout, HTTP error, partial parse, database failure, schema drift, late record and restart paths.
- [x] **W3-09 - CLI/status:** implement `incremental` and expand `status` with source freshness, state, last run and failure/row metrics.
- [x] **W3-10 - Tests:** add fixture-driven unit/integration tests for polling, pagination, revisions, overlaps, state commits, deduplication and event matching.
- [x] **W3-11 - Evidence/report:** create an incremental-run notebook/report, source-status updates, exact demo evidence and English PDF.

### Gold implementation target from the handout

- [x] **W3-G01 - Quality evidence:** execute the Silver review notebook; seven code cells, no errors. See the 2026-11-20 quality change-log entry and `workshop_3/evidence/notebook_execution.json`.
- [x] **W3-G02 - Spark consolidation:** enforce registered hashes/schema, reconcile revisions/replays, preserve units/time grain and prove unique business records.
- [x] **W3-G03 - Two Gold outputs:** implement governance and monthly weather storytelling, with explicit metric denominators/methods/availability and provenance.
- [x] **W3-G04 - Runtime/DAG:** configure Java/PySpark in Docker and execute the scheduled TaskFlow Gold DAG with real outputs and retry evidence.
- [x] **W3-G05 - Independent verification:** compare Spark aggregates with Pandas, exercise synthetic fixture failures, execute a Gold preview notebook and preserve actual output samples.
- [x] **W3-G06 - Report:** assemble the English workshop PDF, quality findings, before/after justification, class/guide correspondence and dashboard story mapping.

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

- [x] Both actual Gold Parquet outputs come from a successful Docker/Airflow Spark run; input/output hashes and task states reconcile.
- [x] Consolidation prevents repeated snapshot counts; conflicting revisions fail before publication.
- [x] Exact quartiles, sample skewness/excess kurtosis and monthly aggregates reconcile independently with Pandas; zero-scale statistics remain explicitly unavailable.
- [x] Both notebooks execute without errors; Gold samples and dashboard field/story mapping are documented.
- [x] Both incremental sources run through the common CLI and scheduler.
- [x] Empty responses are successful empty states when valid, not fabricated failures.
- [x] Repeating unchanged fixtures creates zero duplicate records/versions.
- [x] Same-ID changed fixtures create auditable versions and correct run metrics.
- [x] Overlap/reconciliation tests include late and revised observations.
- [x] Forced failure preserves the previous successful state; retry fills the interval once.
- [x] Pagination and bounded rolling-page behavior are tested without deletion inference.
- [x] Candidate matches store evidence, rule version and unconfirmed/reviewed status.
- [x] `status` reports freshness, state age, counts, rejects and failures per source.
- [x] Automated tests and documented demonstration results reconcile with database counts.
- [x] English report, source-status log and citations are recorded. Commit/push remain student actions and are not inferred.

## 9. Merge gate

- [ ] The non-owner reviewed the complete diff and can explain both incremental adapters.
- [x] New/unchanged/changed/late/invalid/empty/failure fixture scenarios passed.
- [x] Repeated and recovery runs proved idempotency and commit-safe state.
- [x] Event-matching limitations and evaluation evidence are explicit.
- [x] Durable state/matching decisions were promoted to `docs/decisions/`.
- [ ] No secrets, raw bulk data, local scheduler state or generated database volumes are tracked.
- [ ] Weather-adapted PySpark/Gold scope and outstanding source-domain discrepancy are explicit; professor response is cited only if received.

## 10. Required contributor handoff

Every completed task must add a `CHANGE_LOG.md` entry with task ID, commit,
exact fixture/live verification, state before/after, row/version metrics, evidence,
limitations and rollback/replay instructions.
