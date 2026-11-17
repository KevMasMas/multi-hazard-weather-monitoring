# Workshop 2 work in progress

## Submission index

Kevin's Moodle notice lists three items. These are targets, not existing final
artifacts. Execution gates G0-G6 are in the Workshop 2 implementation plan.

| Moodle item | Planned location | Current state |
| --- | --- | --- |
| Technical Architecture and Pipeline Report (PDF) | `report/Workshop_2_Report.pdf`; portable LaTeX in `report/` | Pending real implementation/results and visual review. |
| Pipeline Output Samples | `Workshop_2_Pipeline_Output_Samples.zip`, from sample folders/manifest/README | Pending at least 3 genuine JSON batches and 3 Parquet outputs, provenance and executed review notebook. |
| GitHub link | Reviewed `workflow-2` commit | Foundation present; final delivery reference not selected. |

DAGs, Compose, notebook and run evidence support those three items through the
repository and sample package. No fabricated output or approval is counted.
JSON views derived from weather CSV must be labelled as derivatives; original
bodies stay preserved and checksum-linked.

## What exists now

The report PDF, Docker/Airflow run evidence, database load and Silver Parquet
outputs are not available yet. This folder currently contains a bounded,
reproducible offline review of three historical Workshop 1 CSV captures and a
draft historical/status PostgreSQL CLI whose database path is unexecuted.

From the repository root, run:

```powershell
python scripts/workshop_2/review_offline_captures.py
```

The command reads three saved capture bodies, checks their registered hashes, lands unchanged bytes
under the ignored `data/raw/` directory, writes a deterministic JSON manifest
beside each body, parses NOAA and GHCN records, checks duplicate source keys,
and writes `samples/offline_capture_review.json`. The JSON file is an audit
summary, **not** one of the Bronze JSON files or Silver Parquet files requested
by the standalone Workshop 2 handout. It is not an Airflow DAG run. The source
CSV captures remain the evidence and were not changed.

The pull review found missing expected-hash enforcement, a magnitude category
used as a unit and Windows failure cleanup. These are corrected with focused
tests; initial validation and native gzip landing were added. Database/schema
execution and full provenance remain open. Parser counts do not prove completed
Silver processing. See the dated pull and foundation correction reviews.

## Historical database command (pending Docker verification)

The saved-capture configuration is `config/workshop2_saved_captures.json`.
`--start` and `--end` must fully contain a saved capture's stated interval;
the command does not filter rows out of a capture. The 2026 overlap capture
is a separate smoke sample outside the accepted 2010-2025 baseline.

After installing Docker Desktop with WSL 2 and starting its Linux engine,
launch the repository's PostGIS service. Install `requirements-workshop2.in`
and set `DATABASE_URL` to the host-published port. The service password and
port are local development defaults; override them in an untracked `.env` if
needed. These commands remain an unverified runbook until the WSL 2 engine
starts on this machine:

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin;$env:PATH"
docker version  # Confirm that both Client and Server are displayed.
docker compose up -d postgres
docker compose ps
python -m pip install -r requirements-workshop2.in
$env:DATABASE_URL = 'postgresql://weather:weather@localhost:5432/weather_monitoring'
python ingest.py --mode historical --start 2024-01-01 --end 2025-12-31
python ingest.py --mode status
```

The first historical run applies `sql/001_historical_schema.sql`. A repeat
should report unchanged records; this has not yet been tested on PostgreSQL.
The CLI uses the registered Workshop 1 input hashes, lands the native CSV
bytes, and commits each partition's accepted rows, rejects, metrics and state
in one transaction. The local unit tests only exercise the transaction call
order and rollback boundary with a fake connection.

## Next implementation order

1. Fix/test the foundation and resolve Docker CLI/daemon access.
2. Execute schema and transactional historical/status CLI with saved evidence.
3. Build real Bronze/Silver TaskFlow DAGs, exact-batch FileSensor and Parquet export.
4. Run bounded historical partitions and collect genuine outputs/counts/hashes.
5. Execute the review notebook, finish PDF/ZIP, audit and record team content review.

The current implementation and academic limitations are tracked in
`../deliveries/02-workshop-2/IMPLEMENTATION_PLAN.md` and `CHANGE_LOG.md`.
The initial unexecuted PostgreSQL/PostGIS schema is in
`../sql/001_historical_schema.sql`.
