ALTER TABLE ingestion_run ADD COLUMN IF NOT EXISTS batch_key char(64);
CREATE UNIQUE INDEX IF NOT EXISTS ingestion_run_batch_key_unique
    ON ingestion_run(batch_key) WHERE batch_key IS NOT NULL;
