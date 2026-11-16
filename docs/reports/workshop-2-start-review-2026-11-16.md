# Workshop 2 start review

Reviewed on 2026-11-16. Working branch: `workflow-2`. No implementation or weather
request was performed in this review. Permanent ownership remains solely in
`WORK_BOARD.md`; task detail remains in the Workshop 2 implementation plan.

## Current academic evidence

The public professor repository was checked directly. The current Workshop 2 PDF
has SHA-256 `48012A30DF3709607717929B5CA0F2C94694B76BAF8669E4321AF9283132AE77`,
identical to the reviewed local copy. It still states 2026-I and Public Opinion
and Sentiment Analysis. The CourseProject PDF hash is
`EE4361C937AACE4776890EAF4D0FBE838BB8687C0700E8E4875A385106DD2E01`, also identical
to the local copy. Its Workshop 2 milestone is Docker, database schema and
historical ingestion, with normalization, validation, missing-value handling and
quarantine. The common project requires at least five historical years where
available; the team's accepted target remains 2010-2025.

Sources:
- https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/CourseProject.pdf
- https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_2.pdf
- https://github.com/EngAndres/ud-public/tree/main/courses/data-analysis-programming/practices/airflow_etl

## What the current professor practice actually does

The practice uses Airflow 2.10.4 with LocalExecutor, PostgreSQL 16, initialization,
webserver and scheduler services, persisted volumes and a database health check.
These versions are observed teaching references, not a newly accepted project
dependency selection.

`earthquake_ingestion.py` extracts a deterministic Airflow interval, saves raw
JSON and triggers curation using TriggerDagRunOperator.
`earthquake_curation.py` selects files for that interval, uses Pandas and
PostgresHook, and transactionally closes/opens changed record versions in a
zipper table. `earthquake_analysis.py` computes weekly statistics and exports
Parquet; that analytical stage is not the first historical-ingestion objective.

The current practice uses PythonOperator, not TaskFlow decorators, and explicit
DAG triggering, not FileSensor. The Workshop 2 PDF requests TaskFlow and
FileSensor. These differences must remain visible in the architecture decision.
Neither the earthquake schema nor automatic dropping of invalid rows should be
copied into the weather project. Weather rejects need quarantine and audit.
Keep original CSV/gzip bytes rather than relabeling converted JSON as raw.

## Execution order

1. Verify Docker CLI/daemon access and record the architecture ADR: services,
   raw landing, canonical storage, optional curated Parquet and recovery.
2. Build pinned dependencies, Compose, environment examples and migrations.
   Keep Airflow metadata separate from weather application tables.
3. Complete an offline vertical slice using saved NOAA and GHCN evidence:
   immutable raw reference -> parser -> normalization -> validation -> canonical
   domain rows or rejected_record -> committed metrics and partition state.
4. Implement common historical/status CLI modes and unit/integration tests.
   A second run of the same partition must not increase canonical counts;
   simulated failure must not advance the successful checkpoint.
5. Integrate the same functions into Airflow. Prefer thin DAG tasks calling the
   application code, passing paths/manifests rather than large XCom payloads.
   TaskFlow is a proposed compatible choice; FileSensor and required Parquet
   counts remain conditional until the PDF conflict is resolved.
6. Plan station/year coverage and bounded multi-year partitions. Saved pilot
   evidence cannot prove statewide or multi-year completion. Obtain explicit
   authorization before new weather downloads and cache every response.
7. Run the multi-year workload, reconcile counts, rerun, and rehearse restart and
   recovery. Record actual coverage and missing partitions; do not invent totals.
8. Produce the executed historical review notebook, English PDF/LaTeX report,
   Mermaid architecture, runbook, evidence and final submission reference.

## Conditional deliverables and completion boundary

If the standalone Workshop 2 PDF applies, its additional deliverables include
two functional TaskFlow DAGs, a Silver FileSensor, at least three Bronze JSON and
three Silver Parquet outputs across runs, Parquet exploration notebook, Airflow
UI evidence, `workshop_2/` PDF and updated README. Output files must be genuine
run products, not copies manufactured to meet a count. Any JSON derivative must
retain a link to the unchanged native capture. NLP and scraping conflict with
Team 9 and require clarification, not implementation by analogy.

NWS operational polling, cross-source event matching, CHI computation and the
dashboard belong to later milestones. Their tables/interfaces may be prepared,
but their implementation is not needed to demonstrate the historical core.

## Local preflight and limits

The branch was verified as `workflow-2` and the working tree was clean before
this planning update. `ingest.py` still returns `not_implemented`; source package
boundaries remain stubs. Docker was not resolved by `Get-Command docker` in this
session; this does not prove Docker Desktop is absent. Verify installation,
PATH and daemon access before claiming container validation. No runtime service,
adapter, database load, test result or delivery completion is claimed here.
