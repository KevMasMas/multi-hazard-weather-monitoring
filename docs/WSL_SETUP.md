# Workshop 2 on Ubuntu WSL 2

## Verified state on 2026-11-16 (after runtime recovery)

Ubuntu starts with Linux `6.18.33.2-microsoft-standard-WSL2`, user `kevin`,
Python 3.14.4. The portable offline test runner executes there. Docker Desktop's
Windows client existed, but initially the Linux-engine pipe was unavailable and Ubuntu's
Docker command initially requested WSL integration. After Kevin started Desktop
from Windows Start, Docker Server 29.7.2 and Compose 5.4.0 became available in
Ubuntu. PostGIS `16-3.7` is healthy; real tests and saved-data CLI/rerun passed.
The observed Desktop server identifies 4.87.0, which supersedes earlier
installation-only version reports. No second Linux Docker Engine was installed.

Docker Desktop on Windows: use **Settings > General > Use WSL 2 based engine**,
then **Resources > WSL Integration > Ubuntu > Apply & restart**. This follows
https://docs.docker.com/desktop/features/wsl/ . Do not install a second Docker
Engine in Ubuntu while using Desktop integration.

## Run from Ubuntu

```bash
cd '/mnt/d/usuarios/Monitores/Desktop/Documentos Kevin/Universidad/Programacion para analisis de datos/Multi-Hazard Weather Impact Monitoring'
git branch --show-current
docker version                   # must include Server, not only Client
docker compose version
python3 scripts/workshop_2/run_tests.py
```

Do not activate Windows `.venv/Scripts/activate` inside WSL. Create a separate
Linux environment. `python3.14-venv` was installed in Ubuntu because ensurepip was
initially unavailable. The minimal CLI and real DB tests passed with system
Python 3.14.4 and `psycopg2-binary==2.9.11`; the earlier 2.9.10 pin has no CPython
3.14 Linux wheel. A runtime-only setup is:

```bash
python3 -m venv .venv-wsl
source .venv-wsl/bin/activate
python -m pip install -r requirements-workshop2-runtime.txt
python -m pip check
python scripts/workshop_2/run_tests.py
```

The full data-science dependency lock is still a Python 3.12 reference and was
not installed/tested on Linux 3.14 in this work. For the full notebook environment,
if `uv` is available, create/select 3.12 explicitly:

```bash
uv venv --python 3.12 .venv-wsl
source .venv-wsl/bin/activate
uv pip install -r requirements-workshop2.in
python -m pip check              # if pip is installed; otherwise uv pip check
python scripts/workshop_2/run_tests.py
```

`uv` availability and dependency install in WSL are not yet verified here. An
existing Linux Python 3.12 can instead create this venv and use its pip. The
project ignores `.venv-wsl/`; do not copy or commit virtual environments.

## Real database gate (executed successfully for saved pilot data)

After Docker reports Server:

```bash
docker compose config --quiet
docker compose up -d --wait postgres
docker compose ps
# Local development defaults; match any overrides in your untracked .env.
export DATABASE_URL='postgresql://weather:weather@127.0.0.1:55432/weather_monitoring'
export WORKSHOP2_TEST_DATABASE_URL="$DATABASE_URL"
python scripts/workshop_2/run_tests.py
python ingest.py --mode historical --start 2024-01-01 --end 2025-12-31
python ingest.py --mode historical --start 2024-01-01 --end 2025-12-31
python ingest.py --mode status
python scripts/workshop_2/verify_database.py
```

### pgAdmin on Windows

Register the project server using host `127.0.0.1`, port `55432`, maintenance
database `weather_monitoring`, username `weather`, and the password configured
by `POSTGRES_PASSWORD` (local development default: `weather`). Clear a previously
saved password if necessary. Expand Databases > weather_monitoring > Schemas >
public > Tables after connecting.

Windows has a separate PostgreSQL service on port 5432. Connecting pgAdmin to
`localhost:5432` can therefore authenticate against that service instead of the
project container. The container publishes only `127.0.0.1:55432`; connections
between Compose services still use `postgres:5432`. No Windows PostgreSQL
service needs to be stopped. A password-authenticated host connection on
2026-11-16 returned database `weather_monitoring`, user `weather`, and 1,345
rows in `historical_record`. This verifies connectivity, not workshop acceptance.

The optional integration tests create/drop only a random `w2_test_<uuid>` schema
in the configured development database; they do not remove public application
tables. They require CREATE SCHEMA and PostGIS permissions. They verify real
load/quarantine, rerun counts and rollback/checkpoint behavior. Without the test
URL they are reported as skipped, never passed database validation.

`verify_database.py` retains `workshop_2/evidence/database_verification.json`:
250 NOAA records and 1,095 GHCN measurement records; second invocation has
zero accepted/duplicates and all records unchanged. Integration tests pass real
quarantine and rollback cases in UUID schemas. The running service/volume is
left available for the next milestone; no reset or volume removal was performed.

The first Desktop launch from this application's process context failed with
`sailor-ingest.sock` access error. Manual Windows Start launch resolved it; no
socket was deleted. This is an observed recovery, not proof of its root cause.

The initial 2024/2025 pilot above is historical. Current verification covers
2021-2025, ten real DAG pairs, 19,039 canonical records, a successful container
restart and 29 passing tests. Domain/revision migrations and Parquet exports
are executed. Station coverage is still one station, and the 2010-2025 semester
target is incomplete. See the delivery index and evidence register.

Start the full runtime with:

```bash
docker compose up -d --build --wait airflow-webserver airflow-scheduler airflow-triggerer
python scripts/workshop_2/restore_sample_inputs.py
```

For Arrow exports install `requirements-workshop2-pipeline.txt` in the Linux
runtime environment. Python-version markers retain Arrow 18.1 with the Airflow
Python 3.12 stack and Arrow 26/NumPy 2 for Python 3.14. The full review environment
is defined by `requirements-workshop2.in` for Python 3.12.
