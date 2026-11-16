# Workshop 2 course-material review (2026-11-16)

## Provenance and scope

Read the public `EngAndres/ud-public` `main` branch at `7a54da476f500bdd80a48feccbbab048925bc155` on 2026-11-16. The latest commit touching `courses/data-analysis-programming/` is `3f7010d` (2026-11-16); the previous relevant workshop upload is `5a6ec8d` (2026-11-05). This review interprets the professor's materials for Team 9's weather project. It does not claim a pipeline run.

## Relevant recent changes

| Commit | Observed course change | Consequence for Team 9 |
| --- | --- | --- |
| `3f7010d` | Revised all three earthquake Airflow DAGs and added two Gold Parquet example files. | Use the newer interval, trigger, transaction and versioning patterns as references. The example outputs are not Team 9 evidence. |
| `5a6ec8d` | Added Workshop 2, 3 and 4 handouts, all labeled 2026-I public opinion/sentiment. | Apply compatible pipeline requirements while retaining the 2026-II weather domain and recording the specification conflict. |
| `387ec69` | Added the 2026-II CourseProject, TeamDistribution and Workshop 1 PDFs. | The weather-domain source and milestone contract is explicit. |
| `90be38e` | Updated Open Data/ETL slides. | Use raw landing, validation and orchestration concepts, not the example's domain schema. |
| `86710d7` and `814b66a` | Added the current `practices/airflow_etl` exercise and Airflow/PostgreSQL guide. | These are teaching references for the local stack and pipeline stages. |

## What the current practice actually demonstrates

- `practices/airflow_etl/docker-compose.yml`: Airflow 2.10.4 LocalExecutor, PostgreSQL 16, Airflow init/webserver/scheduler, bind-mounted DAG and Bronze/Gold directories, PostgreSQL health check. The practice stores Airflow metadata and application data in separate databases on one server.
- `earthquake_ingestion.py`: a daily deterministic interval, API response saved to Bronze JSON, then `TriggerDagRunOperator` starts curation. The revised schedule is `0 0 * * *`, with catchup enabled.
- `earthquake_curation.py`: processes only Bronze files in the requested interval, stages records, closes changed versions and inserts new current versions in a single database transaction; current rows have a unique identifier. It fails when an expected file is absent.
- `earthquake_analysis.py`: reads current database rows for an explicit weekly interval and writes a dated Gold Parquet aggregate. The two committed example Parquet files demonstrate the practice, not a Silver layer for this team.
- The practice uses `PythonOperator` and `TriggerDagRunOperator`. It has **no TaskFlow decorators or FileSensor**, despite the separate Workshop 2 handout requesting both. It also drops invalid earthquake rows; Team 9 must quarantine invalid weather rows under its 2026-II contract.

## Related classes and design translation

The Airflow/PostgreSQL guide explains Compose startup, metadata versus application database, deterministic intervals, raw landing, SQL curation and Parquet output. The Open Data/ETL, Data Engineering/Visualization and Exploratory Data Analysis slides cover ETL/ELT, schema drift, late data, idempotency, observability, missing values, outlier review and curation. These support the following implementation choices:

1. Keep NOAA archive CSV/gzip and GHCN CSV bytes unchanged as Bronze evidence. A JSON manifest may describe a capture, but must not be called the raw response.
2. Use bounded NOAA year and GHCN station/year partitions, not a daily network request pattern copied from the USGS example.
3. Use the accepted Airflow architecture with thin tasks calling reusable Python modules. Pass a path/manifest between tasks instead of large weather payloads through XCom.
4. Store validated canonical/domain rows and rejects transactionally in PostgreSQL/PostGIS; preserve raw hash, source ID, partition and run IDs. Publish Silver Parquet exports with those references only after a successful database commit.
5. Use stable partition identifiers and content hashes so repeated runs do not duplicate records; advance state only after success. Preserve revisions instead of overwriting unexplained source changes.
6. Apply source-specific missingness rules from Workshop 1. Keep NOAA missing points as null with zone geography, preserve GHCN trace/QC flags, and quarantine records with invalid required fields. Do not copy generic mean imputation, NLP cleanup or silent row dropping.
7. The Workshop 2 handout's TaskFlow and FileSensor requirements remain a visible discrepancy with the latest practice. If implemented for compatibility, the sensor must identify a specific unprocessed manifest and avoid repeated processing of old files. The practice's direct trigger is a useful alternative design, not evidence that the handout changed.

## Current evidence boundary

No Team 9 Docker service, DAG execution, database load, Bronze run file, Silver Parquet or Airflow screenshot was produced by this read-only source review. The latest practice commit does not resolve the 2026-I/2026-II domain conflict. The next implementation step is the offline historical slice from saved Workshop 1 samples, followed by the Docker/Airflow stack when available.

## Primary sources

- [Course tree](https://github.com/EngAndres/ud-public/tree/main/courses/data-analysis-programming)
- [Current practice](https://github.com/EngAndres/ud-public/tree/main/courses/data-analysis-programming/practices/airflow_etl)
- [Practice Compose](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/practices/airflow_etl/docker-compose.yml)
- [Bronze DAG](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/practices/airflow_etl/airflow/dags/earthquake_ingestion.py)
- [Curation DAG](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/practices/airflow_etl/airflow/dags/earthquake_curation.py)
- [Analysis DAG](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/practices/airflow_etl/airflow/dags/earthquake_analysis.py)
- [Airflow/PostgreSQL guide](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/guides/Airflow-PostgreSQL-ETL.pdf)
- [Open Data/ETL slides](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/slides/OpenData-ETLs-Enhanced.pdf)
- [Data Engineering/Visualization slides](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/slides/DataEngineeringAndVisualization.pdf)
- [EDA/curation slides](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/slides/ExploratoryDataAnalysis.pdf)
