# ADR 0006 - Workshop 2 executed historical slice and evidence

- Date: 2026-11-16, America/Bogota
- Status: implementation decision documented for team review; not personal approval
- Prior decision: ADR 0005 (Airflow, native Bronze, relational Silver/Parquet)

## Context

Kevin requested completion of the Workshop 2 deliverables before 21:45. The
published workshop describes a conflicting public-opinion domain; the course
project and Team 9 assignment require weather sources. The runtime supports
Airflow/PostGIS, and the first saved-capture DAG runs were already verified.

## Decision

Execute 2021-2025 as the five-year delivery slice: Storm Events rows whose state
is Oklahoma and GHCN-Daily station USW00013967. Preserve native nationwide gzip
responses and station CSVs with URL, UTC time, size and SHA-256 before deriving
the registered Oklahoma subsets. Do not redefine the semester's 2010-2025 target
or present one station as statewide coverage.

Keep source acquisition as a separate explicit, cached command. Historical
TaskFlow DAGs replay registered inputs on a manual schedule; a direct trigger
passes one exact file to Silver's FileSensor. Keep the data layout under `data/`
and explain its correspondence to the handout's datalake layer names.

Use LocalExecutor rather than a Celery worker/broker. Include a triggerer service
for stack compatibility, although the current sensor uses reschedule mode.
Pin Arrow 18.1 for Python 3.12; Python 3.14 uses Arrow 26/NumPy 2. Validate the
Docker dependency set with `pip check`.

## Alternatives and consequences

Downloading all sixteen baseline years and every Oklahoma station would increase
coverage, but is not represented as achieved. Copying samples to create nominal
file counts would not demonstrate actual runs and is rejected. The three
packaged batches originate from separate actual source/year runs.

The report must retain open station inventory/county assignment work, source
domain discrepancy and real failed task history. Technical verification cannot
establish professor clarification, student approval, a pushed commit or upload.
