# SQL Area

Numbered files 001-004 are executed Workshop 2 migrations. The migration runner
applies pending files transactionally and records their hashes in
`schema_migration`; do not edit a migration that has already been applied.
Add a new numbered migration for a schema change.

- `001_historical_schema.sql`: source/capture/run/state, canonical records,
  generated WGS84 point geometry, constraints and quarantine.
- `002_historical_domains_and_revisions.sql`: domain tables, immutable accepted
  revisions, per-run sightings, station/location and geography structures.
- `003_capture_revision_links.sql`: pins each sighting to its exact revision.
- `004_pipeline_batch_identity.sql`: unique successful-batch identity for retry.
- `005_incremental_ingestion.sql`: W3 NWS poll/state, records/revisions/sightings,
  quarantine, unconfirmed candidate relationships and operational integration view.
- `bootstrap/create_airflow_database.sql`: separate idempotent Airflow metadata
  database creation, not an application migration.

See `DATA_DICTIONARY.md` and `docs/architecture/workshop-2-er.mmd` for the current
model. Region/assignment tables are intentionally empty pending a reviewed
geographic crosswalk. Workshop 1 diagrams remain the earlier conceptual design.
Historical PySpark Gold is verified separately under `workshop_3/`; incremental
state semantics are in `workshop_3/INCREMENTAL_CONTRACT.md`. CHI remains future work.
