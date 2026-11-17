-- Add historical domain/provenance storage without replacing the pilot tables.
CREATE TABLE IF NOT EXISTS historical_record_revision (
    revision_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    record_id bigint NOT NULL REFERENCES historical_record(record_id),
    run_id bigint NOT NULL REFERENCES ingestion_run(run_id),
    capture_id bigint NOT NULL REFERENCES raw_capture(capture_id),
    source_content_sha256 char(64) NOT NULL,
    recorded_at_utc timestamptz NOT NULL DEFAULT clock_timestamp(),
    normalized_fields jsonb NOT NULL,
    raw_fields jsonb,
    UNIQUE (record_id, run_id)
);

-- Legacy rows retain their actual earlier capture/run; original bytes remain
-- available there even before their parsed fields have been materialized here.
INSERT INTO historical_record_revision
    (record_id, run_id, capture_id, source_content_sha256, recorded_at_utc,
     normalized_fields, raw_fields)
SELECT h.record_id, h.last_run_id, h.capture_id, h.source_content_sha256,
       coalesce(r.finished_at_utc, r.started_at_utc), to_jsonb(h), NULL
FROM historical_record h JOIN ingestion_run r ON r.run_id=h.last_run_id
ON CONFLICT (record_id, run_id) DO NOTHING;

CREATE TABLE IF NOT EXISTS record_capture_link (
    record_id bigint NOT NULL REFERENCES historical_record(record_id),
    run_id bigint NOT NULL REFERENCES ingestion_run(run_id),
    capture_id bigint NOT NULL REFERENCES raw_capture(capture_id),
    source_line integer NOT NULL CHECK (source_line >= 2),
    unchanged boolean NOT NULL,
    PRIMARY KEY (record_id, run_id)
);

CREATE TABLE IF NOT EXISTS source_geography (
    geography_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id text NOT NULL REFERENCES source_catalog(source_id),
    state_code text NOT NULL,
    geography_type text NOT NULL,
    geography_code text NOT NULL,
    geography_name text,
    UNIQUE (source_id, state_code, geography_type, geography_code)
);

CREATE TABLE IF NOT EXISTS storm_event (
    record_id bigint PRIMARY KEY REFERENCES historical_record(record_id),
    source_event_id text NOT NULL,
    episode_id text,
    geography_id bigint REFERENCES source_geography(geography_id),
    magnitude_type text,
    damage_property_raw text,
    damage_crops_raw text,
    impact_fields jsonb NOT NULL,
    source_fields jsonb NOT NULL
);

CREATE TABLE IF NOT EXISTS station (
    station_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id text NOT NULL REFERENCES source_catalog(source_id),
    source_station_id text NOT NULL,
    station_name text,
    UNIQUE (source_id, source_station_id)
);

-- Locations belong to a source capture; a missing new point does not silently
-- become a measurement made at an older station position.
CREATE TABLE IF NOT EXISTS station_location_observation (
    station_id bigint NOT NULL REFERENCES station(station_id),
    capture_id bigint NOT NULL REFERENCES raw_capture(capture_id),
    latitude double precision,
    longitude double precision,
    elevation_raw text,
    PRIMARY KEY (station_id, capture_id),
    CHECK ((latitude IS NULL) = (longitude IS NULL)),
    CHECK (latitude IS NULL OR latitude BETWEEN -90 AND 90),
    CHECK (longitude IS NULL OR longitude BETWEEN -180 AND 180)
);

CREATE TABLE IF NOT EXISTS daily_station_measurement (
    record_id bigint PRIMARY KEY REFERENCES historical_record(record_id),
    station_id bigint NOT NULL REFERENCES station(station_id),
    observation_date date NOT NULL,
    element_code text NOT NULL,
    value double precision NOT NULL,
    unit text NOT NULL,
    attributes text,
    source_fields jsonb NOT NULL,
    UNIQUE (station_id, observation_date, element_code)
);

-- County allocation requires a reviewed boundary/crosswalk data source.
-- These empty structures are preparation, not a fabricated county inventory.
CREATE TABLE IF NOT EXISTS region (
    county_fips char(5) PRIMARY KEY CHECK (county_fips ~ '^[0-9]{5}$'),
    region_name text NOT NULL,
    boundary_version text NOT NULL
);
CREATE TABLE IF NOT EXISTS station_region_assignment (
    station_id bigint NOT NULL REFERENCES station(station_id),
    county_fips char(5) NOT NULL REFERENCES region(county_fips),
    valid_from date NOT NULL,
    valid_to date,
    assignment_method text NOT NULL,
    evidence_reference text NOT NULL,
    PRIMARY KEY (station_id, county_fips, valid_from),
    CHECK (valid_to IS NULL OR valid_to >= valid_from)
);

CREATE OR REPLACE VIEW canonical_event AS
SELECT record_id AS event_id, source_id AS source, source_key AS source_record_id,
       event_type, observed_at_utc AS timestamp_utc, observed_date,
       latitude, longitude, severity_value, severity_unit,
       capture_id, source_content_sha256, last_run_id
FROM historical_record;
