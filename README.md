# Multi-Hazard Weather Impact Monitoring

Semester project for **Data Analysis Programming (2026-II)**, Universidad Distrital
Francisco Jose de Caldas. Team 9: Kevin David Rincon Valencia (20232020356) and
Pablo Garzon Gomez (20232020341).

We are building an Oklahoma county-level monitoring system from NOAA Storm
Events, GHCN-Daily, NWS Alerts and NWS station observations. The planned analytical
output is a Compound Hazard Index. The accepted semester target is 2010-2025,
with a rolling 24-hour current window and separate seven-day context.

## Current delivery: Workshop 2

Start with the [delivery index](workshop_2/README.md), [PDF](workshop_2/report/Workshop_2_Report.pdf),
[sample ZIP](workshop_2/Workshop_2_Pipeline_Output_Samples.zip),
[executed Pandas notebook](notebooks/02_historical_ingestion_review.ipynb) and
[demonstration guide](deliveries/02-workshop-2/DEMO_GUIDE.md).

The executed 2021-2025 slice contains 13,561 Oklahoma Storm Events records and
5,478 daily measurements from GHCN station USW00013967. Ten real Airflow
Bronze/Silver batches, exact-file FileSensor, Parquet exports, unchanged replay
and restart persistence are verified. All 29 tests pass, including real DB checks.
The notebook executes nine code cells without errors.

The PDF/ZIP are prepared for team review. Personal approval, commit/push and
Moodle upload are not inferred. The full 2010-2025 target, broader station
inventory/county assignments, NWS incremental ingestion and CHI remain open.
The published Workshop 2 handout's 2026-I public-opinion wording is a documented
discrepancy; no professor clarification is claimed.

## Run from Ubuntu WSL

With Docker Desktop showing Engine running and Ubuntu integration enabled:

```bash
python scripts/workshop_2/restore_sample_inputs.py
docker compose up -d --build --wait airflow-webserver airflow-scheduler airflow-triggerer
```

Open <http://localhost:8080> (local classroom defaults: `airflow` / `airflow`).
Enable both DAGs and trigger only `weather_bronze_ingestion` with
`{"partition":"OK_2021"}`. It triggers Silver automatically. Other packaged
offline partitions are `USW00013967_2021_full` and `USW00013967_2022_full`.
Restoring samples makes no weather request. Full acquisition is an explicit,
cached command described in the demo guide.

Windows pgAdmin: host `127.0.0.1`, port **55432**, database
`weather_monitoring`, user/password `weather` for local defaults.
Internal Compose connections use `postgres:5432`. Overrides belong in ignored
`.env`; see [WSL setup](docs/WSL_SETUP.md).

The historical/status CLI uses a configured `DATABASE_URL` and complete
registered capture intervals:

```bash
python ingest.py --mode historical --start 2021-01-01 --end 2025-12-31
python ingest.py --mode status
```

Missing inputs or mismatching hashes fail explicitly. Incremental mode remains
Workshop 3. Python 3.12 dependencies are in `requirements-workshop2.in`.
`--start` and `--end` select fully contained registered capture intervals; they
do not trim rows to a subrange. This preserves input hashes, CSV line references
and atomic partition checkpoints. A request containing no complete registered
capture fails rather than silently constructing an unregistered partial file.

## Repository structure

| Area | Purpose |
| --- | --- |
| `airflow/dags/` | Thin Bronze/Silver TaskFlow DAGs |
| `src/` | Shared source parsing, validation, storage and export |
| `sql/` | Checksummed migrations and database bootstrap |
| `config/` | Source contracts and registered capture selection |
| `scripts/workshop_2/` | Explicit acquisition, verification and packaging commands |
| `data/` | Ignored bulk raw, Bronze and curated outputs |
| `notebooks/` | Executed profiling and output exploration |
| `workshop_1/` | Preserved Workshop 1 report, mapping and evidence |
| `workshop_2/` | PDF/LaTeX, small deliverable samples and execution receipts |
| `deliveries/` | Per-workshop plans, change logs and demo guide |
| `docs/` | Decisions, references, architecture and dated reviews |
| `tests/` | Offline and isolated real-PostGIS checks |
| `dashboard/` | Planned later-workshop dashboard |

Only the three selected sample Parquet files are exempted from the bulk-data
ignore rules. Database/log volumes, environments and real credentials are not
committed.

## Team workflow and earlier delivery

[WORK_BOARD.md](WORK_BOARD.md) is the only current assignment board.
Kevin leads NOAA/database/CLI; Pablo leads GHCN/orchestration, with reciprocal
review. Read [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) for requirements,
[AGENTS.md](AGENTS.md) for working rules and the active delivery change log for
verified work. Current branch: `workflow-2`; Kevin performs commit/push after review.

[Workshop 1](workshop_1/README.md) remains preserved, including its approved report,
[source notebook](notebooks/01_source_profiling.ipynb), [mapping](workshop_1/mapping.md)
and separate approval record. That approval does not extend to Workshop 2.

## Academic references

- [Course materials](https://github.com/EngAndres/ud-public/tree/main/courses/data-analysis-programming)
- [CourseProject.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/CourseProject.pdf)
- [TeamsDistribution.pdf](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/TeamsDistribution.pdf)
- [Workshop 1](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_1.pdf)
- [Workshop 2](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_2.pdf)
- [Workshop 3](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_3.pdf)
- [Workshop 4](https://github.com/EngAndres/ud-public/blob/main/courses/data-analysis-programming/project/Workshop_4.pdf)
- [Airflow practice](https://github.com/EngAndres/ud-public/tree/main/courses/data-analysis-programming/practices/airflow_etl)

Professor-issued requirements outrank repository notes. Record semester/domain
conflicts explicitly and never treat a teaching example as a new requirement.
