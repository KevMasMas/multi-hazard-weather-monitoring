# ADR 0005 - Apache Airflow and weather data layers

- **Date:** 2026-11-16
- **Status:** selected for the Workshop 1 design revision at Kevin's request;
  joint implementation review remains pending
- **Scope:** architecture proposal, not implemented infrastructure

## Context

The course guide teaches Bronze native responses, PostgreSQL Silver and Parquet
Gold. The standalone Workshop 2 handout instead requests Parquet Silver. The
2026-II course project requires canonical relational storage and a database-backed
dashboard. Kevin confirmed the class used the Airflow/layer guide and requested
updating the unsubmitted Workshop 1 before continuing Workshop 2.

## Decision

Select Apache Airflow and PostgreSQL/PostGIS. Retain native response bytes and
capture metadata in Bronze (`data/raw/` for bulk captures). Silver consists of
validated canonical/domain records and traceable Parquet exports. Publish exports
after database commit; their later implementation must make retries safe and
retain source, capture, partition and run references. Quarantine invalid records.
Gold will hold later analytical aggregates and CHI outputs; the dashboard reads
database analytical views and health metrics. The shared CLI remains the course
entry point; DAGs call the same application functions.

## Alternatives

- An equivalent scheduler is permitted by the general project but does not
  match the selected classroom workflow as closely.
- PostgreSQL-only Silver follows the guide but omits the handout's Parquet
  output. File-only Silver would omit the canonical database contract.
- Converting all originals into JSON would lose native raw evidence semantics.

## Consequences and limits

The Workshop 1 report and diagram must name these layers and selected tools,
while preserving samples, hashes, profiling and model mappings. No DAG, exported
Parquet file or Gold metric is claimed to exist from this design decision. The
standalone handout's NLP/scraping domain discrepancy remains documented.

## References

- https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/guides/Airflow-PostgreSQL-ETL.pdf
- https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/CourseProject.pdf
- https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_2.pdf
