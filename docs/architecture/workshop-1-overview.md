# Workshop 1 Architecture Overview

The revised report renders `workshop-1-pipeline.mmd`: it explicitly includes
Apache Airflow, CLI, Bronze raw landing, validation/quarantine, Silver canonical
storage and Parquet exports, run/state audit, planned Gold analytics and dashboard.
That Mermaid file is the single editable architecture figure.

- **Status:** accepted high-level Workshop 1 proposal
- **Implementation:** Workshops 2-4

The professor's reference architecture is adapted to four weather sources while
keeping historical and incremental extraction separate. Boxes describe planned
responsibilities; they do not claim implemented services.

## Selected layers

| Layer/component | Planned responsibility |
| --- | --- |
| Bronze | Preserve native NOAA/GHCN CSV or gzip and NWS JSON/GeoJSON, metadata and SHA-256; `data/raw/` remains the raw landing area. |
| Silver | Normalize and validate source records, retain units/QC, load PostgreSQL/PostGIS canonical/domain tables and publish traceable Parquet exports after successful commit. |
| Quarantine | Retain rejected payload references and reason codes outside accepted Silver records. |
| Gold | Later temporal/geographic aggregates, historical/current comparison and CHI outputs; provide database analytical views for the dashboard. |
| Apache Airflow and CLI | Orchestrate shared ingestion functions with auditable intervals, retries and checkpoints; pass paths/manifests rather than bulk data. |

The [course guide](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/guides/Airflow-PostgreSQL-ETL.pdf)
demonstrates PostgreSQL Silver and Parquet Gold. The standalone Workshop 2 PDF
requests Parquet Silver. The team's proposed Silver exports support that file
artifact alongside the canonical database. A native CSV response is not changed
into JSON and described as unmodified evidence. Parquet is a storage format;
its role as Silver or Gold depends on the content, not the extension.

Architecture selection is recorded in ADR 0005. Docker services, DAG details and
actual layer outputs will be implemented and verified in Workshop 2; Gold
analytics and dashboard remain later work. The older public-opinion/NLP wording
is still not a weather-domain requirement.

## Workshop boundaries

- **Workshop 1:** validate sources, preserve samples, define contracts, mapping and this architecture.
- **Workshop 2:** implement Docker/Airflow, Bronze landing, historical adapters, Silver database/Parquet, validation and quarantine.
- **Workshop 3:** implement incremental polling, watermarks, retries, scheduling and event matching.
- **Workshop 4:** implement analytical views, historical/current comparison, CHI and dashboard.

The conceptual entity relationships are detailed in
`docs/architecture/workshop-1-er-model.md` and the field mapping is maintained in
`workshop_1/mapping.md`.
