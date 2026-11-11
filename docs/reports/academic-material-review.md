# Academic Material Review

## Review scope

Reviewed on 2026-11-03 from professor repository commit `387ec69a66294158f012253e5ee12c7a30bf94ac` (`Project update DAP`) and the local copies of `CourseProject.pdf`, `TeamsDistribution.pdf`, `Workshop_1.pdf`, and `Airflow-PostgreSQL-ETL.pdf`.

Update observed on 2026-11-05: professor repository commit
`5a6ec8d` added `Workshop_2.pdf`, `Workshop_3.pdf`, and `Workshop_4.pdf`.
The three PDFs were reviewed in full on 2026-11-10. They are labeled 2026-I and
describe a Public Opinion and Sentiment Analysis project that conflicts with the
2026-II natural-hazard contract. The conflict, hashes, reusable guidance and
professor-clarification questions are recorded in
`docs/reports/workshops-2-4-specification-review.md`.

The team repository was also inspected and had no commits or tracked files before this foundation branch.

## Authoritative requirements

The three project PDFs are the primary requirements and evaluation sources:

- The course project document defines the shared four-workshop lifecycle, common CLI, conceptual model, infrastructure expectations, final deliverables, and rubric.
- The team-assignment document identifies Team 9, its two members, US scope, assigned sources, Compound Hazard Index, and the main spatial/temporal correlation challenge.
- Workshop 1 defines the evidence threshold, profiling and mapping work, required artifacts, and its 20-point rubric.

The README, slides, notebooks, Airflow guide, and practice support learning and implementation, but they do not override the project PDFs.

## Material developed in the course repository

### Course and programming foundations

- `README.md` and `CourseDescription.pdf`: goals, syllabus, grading, English-submission rule, and bibliography.
- `IntroductionToDataScience.pdf`: data systems, databases, data lake versus warehouse, metadata, and analysis processes.
- `ProgrammingLanguagesForDataAnalysis.pdf`: Python, R, SQL, and Rust ecosystems and their roles in a modern data stack.
- `DataManipulationPython.pdf` and `python_intro.ipynb`: Python fundamentals, NumPy, Pandas, data loading, datetime handling, missing values, merges, and group-by operations.
- `r_intro.ipynb` and `rust_weather.ipynb`: descriptive weather analysis in R and Rust. These are educational alternatives, not mandatory languages for this project.

### Data engineering and quality

- `OpenData-ETLs-Enhanced.pdf`: open-data standards and licensing, REST APIs, authentication, API errors, rate limits, ETL/ELT, data-quality dimensions, retries and resilience, orchestration, observability, incremental loads, late data, partitioning, and scaling.
- `ExploratoryDataAnalysis.pdf` and `DataEngineeringAndVisualization.pdf`: EDA, descriptive statistics, data-quality dimensions, missing data, outliers, feature engineering, curation pipelines, visualization, and dashboard design.
- `eda_data_curation.ipynb`: executable examples of schema inspection, null profiling, ranges, duplicates, impossible values, outlier detection/treatment, imputation, feature engineering, and feature selection.
- `eda_ydata_profiling.ipynb`: automated profiling as a supporting technique. It cannot replace the explicit evidence and analysis required by Workshop 1.

### Analysis and communication

- `DataAnalysis.pdf`: descriptive statistics, distributions, missing data, outlier detection, normalization, correlation, and regression.
- `DataVisualization.pdf` and `eda_visualizations.ipynb`: plot selection, temporal and relationship charts, visual storytelling, dashboard design, and Plotly Dash.
- `NaturalLanguageProcessing.pdf` and `nlp.ipynb`: NLP, scraping, sentiment, RAG, embeddings, and transformers. This material is not currently central to Team 9's defined deliverables.

### Airflow and PostgreSQL practice

The guide and `practices/airflow_etl/` implement a teaching pipeline for USGS earthquakes:

1. Docker Compose starts PostgreSQL, Airflow initialization, webserver, and scheduler.
2. A bronze DAG polls an API for a deterministic Airflow data interval and writes timestamped raw JSON.
3. A curation DAG selects files by interval, validates/standardizes data, and upserts into PostgreSQL.
4. An analysis DAG waits for curation, computes 24-hour statistics, and writes Parquet.

Useful patterns for this project are deterministic data intervals, raw/curated separation, timestamped provenance, retry configuration, database hooks, primary-key upserts, idempotent reruns, orchestration dependencies, and operational verification.

Important limits of the example:

- It is earthquake-specific and is not a Team 9 design template.
- It uses learning credentials and runtime package installation; production-quality project configuration should improve on both.
- It passes an API payload through XCom even though the guide itself warns that large payloads should be stored externally and only paths passed.
- The curation example drops invalid rows, while the project contract requires rejected-record quarantine and audit metrics.
- The guide demonstrates Airflow, but the project specification permits an equivalent documented scheduler.
- Any schedule or code discrepancy between the PDF and repository files must be resolved deliberately rather than copied blindly.

## Relevance by workshop

| Workshop | Most relevant material | Correct use |
| --- | --- | --- |
| 1 | Project PDFs; Open Data/ETL slides; Python/Pandas; EDA/data-curation notebook | Source characterization, evidence profiling, canonical mapping, contracts, scope, risks, and architecture proposal |
| 2 | Airflow/PostgreSQL guide and practice; Open Data/ETL; Pandas; EDA/curation | Docker architecture, raw landing, schema, validation, missing values, quarantine, idempotent historical ingestion |
| 3 | Airflow data intervals and dependencies; API resilience; incremental/late-data material | Watermarks, overlap windows, retries, scheduling, change detection, deduplication, and recovery |
| 4 | Data Analysis; EDA; Data Visualization; dashboard material and visualization notebook | Baselines, temporal/geographic comparison, index communication, Plotly Dash, and visual design |
| Final | Course project final checklist and all above material | Reproducibility, tests, data health, report, live demonstration, and defense |

## Requirements versus examples

The following are required because the project documents say so: four validated sources, common CLI modes, canonical model concepts, raw provenance, validation and quarantine, idempotency, watermarks, cross-source integration, historical/current analysis, Compound Hazard Index, Docker Compose, relational storage, scheduler/orchestrator, Plotly Dash, tests, logging, English documentation, and reproducibility.

The following remain choices or examples: exact US region, exact hazard components, Airflow versus an equivalent scheduler, PostgreSQL/PostGIS versus a justified SQLite/GeoPackage alternative, bronze/silver/gold naming, Pandas versus Polars for a given step, and the precise indicator formula.

## Gaps and open work

- The initial 2026-11-03 review contained only the detailed Workshop 1 specification. Workshop 2-4 PDFs published on 2026-11-05 were reviewed on 2026-11-10 and conflict with the 2026-II Team 9 contract; implementation plans therefore separate safe compatibility work from conditional 2026-I requirements.
- The exact US region and index definition are not specified and must be selected from validated source coverage and manageable volume.
- No Team 9 source behavior, samples, profiles, data-quality issues, record overlap, or index validation has been established yet.
- The project needs a source-status log because operational sources can revise records and interfaces.
