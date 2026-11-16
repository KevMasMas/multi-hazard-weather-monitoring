-- Workshop 2 initial historical model. Apply inside one migration transaction.
-- This file has not yet been run against PostgreSQL in this workspace.
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS source_catalog (
    source_id text PRIMARY KEY,
    source_url text NOT NULL,
    source_format text NOT NULL,
    attribution text NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_capture (
    capture_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id text NOT NULL REFERENCES source_catalog(source_id),
    partition_key text NOT NULL,
    raw_path text NOT NULL,
    content_type text NOT NULL,
    byte_count bigint NOT NULL CHECK (byte_count >= 0),
    sha256 char(64) NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
    origin_reference text NOT NULL,
    retrieved_at_utc timestamptz,
    UNIQUE (source_id, partition_key, sha256)
);

CREATE TABLE IF NOT EXISTS ingestion_run (
    run_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id text NOT NULL REFERENCES source_catalog(source_id),
    partition_key text NOT NULL,
    capture_id bigint REFERENCES raw_capture(capture_id),
    started_at_utc timestamptz NOT NULL DEFAULT now(),
    finished_at_utc timestamptz,
    status text NOT NULL CHECK (status IN ('running', 'succeeded', 'failed')),
    rows_read integer NOT NULL DEFAULT 0 CHECK (rows_read >= 0),
    rows_accepted integer NOT NULL DEFAULT 0 CHECK (rows_accepted >= 0),
    rows_rejected integer NOT NULL DEFAULT 0 CHECK (rows_rejected >= 0),
    rows_unchanged integer NOT NULL DEFAULT 0 CHECK (rows_unchanged >= 0)
);

CREATE INDEX IF NOT EXISTS ingestion_run_source_partition_idx
    ON ingestion_run (source_id, partition_key, started_at_utc DESC);

CREATE TABLE IF NOT EXISTS historical_record (
    record_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id text NOT NULL REFERENCES source_catalog(source_id),
    source_key text NOT NULL,
    event_type text NOT NULL,
    observed_at_utc timestamptz,
    observed_date date,
    latitude double precision,
    longitude double precision,
    point_geom geometry(Point, 4326) GENERATED ALWAYS AS (
        CASE WHEN latitude IS NULL THEN NULL
             ELSE ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
        END
    ) STORED,
    severity_value double precision,
    severity_unit text,
    geography_reference text,
    quality_attributes text,
    source_content_sha256 char(64) NOT NULL,
    capture_id bigint NOT NULL REFERENCES raw_capture(capture_id),
    source_line integer NOT NULL CHECK (source_line >= 2),
    last_run_id bigint NOT NULL REFERENCES ingestion_run(run_id),
    CONSTRAINT historical_record_time_grain CHECK (
        (observed_at_utc IS NOT NULL) <> (observed_date IS NOT NULL)
    ),
    CONSTRAINT historical_record_coordinate_pair CHECK (
        (latitude IS NULL) = (longitude IS NULL)
    ),
    CONSTRAINT historical_record_latitude CHECK (latitude IS NULL OR latitude BETWEEN -90 AND 90),
    CONSTRAINT historical_record_longitude CHECK (longitude IS NULL OR longitude BETWEEN -180 AND 180),
    UNIQUE (source_id, source_key)
);

CREATE INDEX IF NOT EXISTS historical_record_time_idx
    ON historical_record (observed_at_utc, observed_date);
CREATE INDEX IF NOT EXISTS historical_record_geom_idx
    ON historical_record USING gist (point_geom);

CREATE TABLE IF NOT EXISTS rejected_record (
    rejected_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id bigint NOT NULL REFERENCES ingestion_run(run_id),
    capture_id bigint NOT NULL REFERENCES raw_capture(capture_id),
    source_line integer NOT NULL CHECK (source_line >= 2),
    element_code text,
    reason_code text NOT NULL,
    raw_fields jsonb NOT NULL,
    UNIQUE (run_id, source_line, element_code, reason_code)
);

CREATE TABLE IF NOT EXISTS ingestion_state (
    source_id text NOT NULL REFERENCES source_catalog(source_id),
    partition_key text NOT NULL,
    last_successful_run_id bigint NOT NULL REFERENCES ingestion_run(run_id),
    last_successful_at_utc timestamptz NOT NULL,
    PRIMARY KEY (source_id, partition_key)
);
