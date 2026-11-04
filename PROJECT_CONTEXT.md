# Project Context

## Purpose

This file is the durable context for Team 9's semester project. Update it when the professor changes a requirement or the team approves a material technical decision. Do not record unverified results as facts.

## Identity

- Course: Data Analysis Programming
- Semester: 2026-II
- Institution: Universidad Distrital Francisco Jose de Caldas
- Team: 9 (the only two-person team)
- Students: Pablo Garzon (20232020341) and Kevin Rincon (20232020356)
- Assigned system: Multi-Hazard Weather Impact Monitoring
- Required analytical output: Compound Hazard Index per region
- Required geographic family: a region of the United States because the assigned NOAA/NWS sources are US services

## Objective

Design and implement a reproducible, multi-source data ingestion and analysis system that combines historical and periodically updated weather information, detects new or changed records, correlates multiple hazard types in time and space, and communicates current conditions relative to a historical baseline.

The system is for monitoring and correlation. It must not be presented as a hazard-prediction system.

## Assigned sources

The following sources are assigned starting points and must be validated during Workshop 1 before the team commits to detailed contracts:

| Role | Source | Expected access pattern | Official starting point |
| --- | --- | --- | --- |
| Historical 1 | NOAA Storm Events Database | Bulk yearly compressed CSV archives; multiple event types | <https://www.ncei.noaa.gov/stormevents/> |
| Historical 2 | GHCN-Daily through NCEI | NCEI Access Data Service; daily summaries in JSON or CSV | <https://www.ncei.noaa.gov/access/services/data/v1> |
| Incremental 1 | NWS Alerts API | Active alerts; GeoJSON/CAP; descriptive User-Agent required | <https://www.weather.gov/documentation/services-web-api> |
| Incremental 2 | NWS Station Observations | Latest or recent station observations through the NWS API | <https://www.weather.gov/documentation/services-web-api> |

No API availability, rate limit, license, field behavior, record volume, or cross-source overlap is considered verified merely because it appears in this file or in the assignment document. Workshop 1 requires empirical validation with real responses; that work has not started in this foundation branch.

## Common technical contract

The course project specification requires the final system to provide:

- At least two historical sources with different formats or access methods and several years of data where available.
- At least two continuously or periodically updated sources.
- A raw landing zone that preserves responses as received for provenance and reprocessing.
- Canonical normalization, validation, documented missing-value handling, deduplication, event identification, cross-source integration, and rejected-record quarantine.
- Watermark-based incremental ingestion, new/changed record detection, idempotency, pagination or partitioning where needed, rate-limit handling, retries, and safe recovery.
- Temporal and geographic analysis, historical-versus-current comparison, a parameterized Compound Hazard Index, and a monitoring dashboard.
- Configuration outside code, structured logging, automated tests, and reproducible setup.

Required command-line contract:

```text
python ingest.py --mode historical [--start YYYY-MM-DD --end YYYY-MM-DD]
python ingest.py --mode incremental
python ingest.py --mode status
```

The final infrastructure runs locally with Docker Compose and includes a relational database, ingestion application, scheduler/orchestrator, and Plotly Dash dashboard. PostgreSQL with PostGIS is recommended. SQLite/GeoPackage requires justification. Apache Airflow is an example orchestrator, not the only allowed scheduler.

## Canonical conceptual model

The common conceptual model includes:

- `source`: source catalog, URL, format, and license.
- `ingestion_run`: auditable execution status and row metrics.
- `ingestion_state`: per-source watermark and last successful run.
- `event`: canonical source record with source, event type, UTC timestamp, WGS84 coordinates, severity with units, original reference, and content hash.
- `event_group`: links records believed to describe the same real-world event.
- `rejected_record`: quarantined payload and rejection reason.
- Domain tables: hazard-specific attributes that reference canonical events.

The exact Team 9 domain tables, regional entity model, station-to-region mapping, alert geometry handling, and event-grouping rules remain open decisions.

## Workshop sequence

### Workshop 1 - source validation and data contract

Define the hazard and scope; validate four sources with real evidence; profile at least 200 records per source (or the full source if smaller); identify at least five concrete data-quality problems; examine at least five candidate cross-source event pairs; draft canonical mappings, domain tables, ingestion contracts, user stories, risks, indicator proposal, and architecture. Required artifacts include a PDF report, `notebooks/01_source_profiling.ipynb`, small raw samples, a mapping table, a first ER diagram, and repository setup.

### Workshop 2 - architecture and historical ingestion

Build the Docker stack, database schema, and historical ingestion with normalization, validation, missing-value handling, idempotency, and quarantine.

### Workshop 3 - incremental ingestion and integration

Implement watermarks, scheduled polling, retries, new/changed detection, deduplication, and event identification/integration across sources.

### Workshop 4 - analytics and dashboard

Implement temporal and geographic analysis, historical-versus-current comparison, the Compound Hazard Index, and the Plotly Dash monitoring dashboard.

### Final delivery

Integrate all workshops, prove reproducibility and idempotency, complete automated tests and data-health reporting, submit the English report and presentation, demonstrate the product live, and tag the final commit `v1.0-final`.

## Final evaluation priorities

The final rubric assigns the greatest weight to historical ingestion (15), incremental ingestion (15), and temporal/geographic analysis plus historical/current comparison (15). Data modeling, data quality, event integration, dashboard communication, and engineering quality each carry 10 points; the indicator carries 5 points. Individual understanding can adjust each team member's grade.

## Current constraints

- Do not implement Workshop 1 on the project-foundation branch.
- Do not query weather APIs during foundation work.
- Do not invent source behavior, data samples, quality findings, volumes, overlap, results, or validations.
- Do not treat an academic example as a mandatory design unless a project specification requires it.
- Keep technical documentation, code, identifiers, commits, and pull-request descriptions in English.
- Preserve existing files and avoid committing secrets or bulk/raw data.
- Work on feature branches and review changes before integration into `main`.

## Documentation and delivery model

- `deliveries/` is the historical record of each graded milestone. Each active delivery contains an implementation plan and a chronological change log. Runnable milestones also receive a demo guide.
- `docs/` contains current, durable knowledge: semester plans, academic reviews, references, and accepted design decisions.
- `PROJECT_CONTEXT.md` contains requirements and constraints that must survive across deliveries.
- Plans describe intended work; change logs describe work actually performed. A checked plan item must point to evidence in the corresponding change log.
- Delivery documents must distinguish verified software behavior, live-source evidence, manual observations, and remaining external validation.

## Open decisions

The following decisions must be made from evidence during Workshop 1:

1. Exact US region and regional aggregation unit (state, county, NWS forecast zone, or another justified unit).
2. Historical time window and meaning of "current situation."
3. Hazard components and event types included in the Compound Hazard Index.
4. Severity units, normalization rules, seasonal baseline, weighting, output scale, and validation method for the index.
5. Stable source identifiers, update semantics, deletion/revision behavior, watermark, overlap window, and polling frequency per incremental source.
6. Crosswalks among stations, alert polygons/zones/counties, Storm Events locations, and the chosen region model.
7. Domain tables, duplicate keys, cross-source event-matching criteria, and treatment of records that cannot be geocoded precisely.
8. Final scheduler choice. Airflow is strongly supported by course material but is not mandatory if an equivalent scheduler is justified.

## Authoritative references

### Project documents

- [CourseProject.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/CourseProject.pdf)
- [TeamsDistribution.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/TeamsDistribution.pdf)
- [Workshop_1.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_1.pdf)

### Most relevant course material

- [Course repository and syllabus](https://github.com/EngAndres/ud-public/tree/main/courses/data-analysis-programming)
- [Open Data and ETLs slides](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/slides/OpenData-ETLs-Enhanced.pdf)
- [Python data manipulation slides](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/slides/DataManipulationPython.pdf)
- [Exploratory data analysis slides](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/slides/ExploratoryDataAnalysis.pdf)
- [Data visualization slides](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/slides/DataVisualization.pdf)
- [Airflow/PostgreSQL ETL guide](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/guides/Airflow-PostgreSQL-ETL.pdf)
- [Airflow ETL practice](https://github.com/EngAndres/ud-public/tree/main/courses/data-analysis-programming/practices/airflow_etl)
- [EDA and data curation notebook](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/notebooks/eda_data_curation.ipynb)
- [Visualization notebook](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/notebooks/eda_visualizations.ipynb)

See `docs/reports/academic-material-review.md` for relevance and limitations.
