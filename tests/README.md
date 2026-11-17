# Test Area

Automated tests begin with the implemented ingestion components in Workshop 2.
Tests must use small recorded fixtures, not live weather-service requests.

- `fixtures/`: sanitized and reviewable recorded inputs.
- Current unit tests: source parsing, registered capture hashes, native gzip,
  atomic landing, canonical validation, tamper detection and transaction boundaries.
- Current integration tests: migrations, quarantine, immutable revisions/export,
  idempotency, retry batch identity and rollback/checkpoint recovery.
- Watermarks for current NWS ingestion remain Workshop 3.

Latest real WSL result: **29 tests passed, zero failures/errors/skips**, recorded
in `workshop_2/evidence/wsl_test_results.json`. Eight tests use real PostGIS;
the remaining 21 tests are offline. Test fixtures are synthetic where labelled.

Workshop 2 portable command (Windows Python or Ubuntu WSL):

```text
python scripts/workshop_2/run_tests.py
```

It sets the project import paths explicitly. Plain `unittest discover` without
`PYTHONPATH=src` may fail to import the package. Real PostGIS tests are optional:
set `WORKSHOP2_TEST_DATABASE_URL` to a development database with schema/PostGIS
permissions. Tests use a fresh UUID schema and clean it up; without that URL,
database tests are skipped, not counted as successful integration checks.
See `docs/WSL_SETUP.md`. Synthetic invalid inputs are test fixtures, not observed
weather measurements.
