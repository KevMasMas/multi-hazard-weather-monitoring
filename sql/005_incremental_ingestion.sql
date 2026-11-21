-- Additive W3 model. Saved replay and operational records have separate namespaces.
CREATE TABLE incremental_poll (
    poll_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id text NOT NULL REFERENCES source_catalog(source_id),
    scope text NOT NULL,
    namespace text NOT NULL CHECK (namespace IN ('replay', 'live', 'test')),
    queried_at_utc timestamptz NOT NULL,
    completed_at_utc timestamptz NOT NULL DEFAULT clock_timestamp(),
    status text NOT NULL CHECK (status IN ('succeeded', 'failed')),
    coverage_complete boolean NOT NULL,
    pages jsonb NOT NULL,
    rows_read integer NOT NULL DEFAULT 0,
    rows_new integer NOT NULL DEFAULT 0,
    rows_changed integer NOT NULL DEFAULT 0,
    rows_unchanged integer NOT NULL DEFAULT 0,
    rows_rejected integer NOT NULL DEFAULT 0,
    error_code text,
    CHECK (rows_read = rows_new + rows_changed + rows_unchanged + rows_rejected)
);
CREATE TABLE incremental_record (
    record_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id text NOT NULL REFERENCES source_catalog(source_id),
    namespace text NOT NULL CHECK (namespace IN ('replay', 'live', 'test')),
    source_key text NOT NULL,
    observed_at_utc timestamptz NOT NULL,
    event_type text NOT NULL,
    geometry geometry(Geometry,4326),
    normalized_fields jsonb NOT NULL,
    source_content_sha256 char(64) NOT NULL,
    last_poll_id bigint NOT NULL REFERENCES incremental_poll(poll_id),
    UNIQUE (source_id, namespace, source_key)
);
CREATE INDEX incremental_record_geometry_idx ON incremental_record USING gist(geometry);
CREATE TABLE incremental_revision (
    revision_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    record_id bigint NOT NULL REFERENCES incremental_record(record_id),
    poll_id bigint NOT NULL REFERENCES incremental_poll(poll_id),
    source_content_sha256 char(64) NOT NULL,
    raw_fields jsonb NOT NULL,
    normalized_fields jsonb NOT NULL,
    UNIQUE(record_id,poll_id)
);
CREATE TABLE incremental_sighting (
    poll_id bigint NOT NULL REFERENCES incremental_poll(poll_id),
    record_id bigint NOT NULL REFERENCES incremental_record(record_id),
    page_sha256 char(64) NOT NULL,
    feature_index integer NOT NULL,
    classification text NOT NULL CHECK(classification IN ('new','changed','unchanged')),
    PRIMARY KEY(poll_id,record_id)
);
CREATE TABLE incremental_reject (
    poll_id bigint NOT NULL REFERENCES incremental_poll(poll_id),
    page_sha256 char(64) NOT NULL,
    feature_index integer NOT NULL,
    reason_code text NOT NULL,
    raw_fields jsonb NOT NULL,
    PRIMARY KEY(poll_id,page_sha256,feature_index)
);
CREATE TABLE incremental_state (
    source_id text NOT NULL REFERENCES source_catalog(source_id),
    namespace text NOT NULL,
    scope text NOT NULL,
    last_successful_query_at_utc timestamptz NOT NULL,
    last_poll_id bigint NOT NULL REFERENCES incremental_poll(poll_id),
    PRIMARY KEY(source_id,namespace,scope)
);
CREATE TABLE event_candidate (
    candidate_key char(64) PRIMARY KEY,
    rule_version text NOT NULL,
    namespace text NOT NULL,
    left_source text NOT NULL,
    left_key text NOT NULL,
    right_source text NOT NULL,
    right_key text NOT NULL,
    evidence jsonb NOT NULL,
    review_status text NOT NULL DEFAULT 'candidate_not_confirmed'
        CHECK(review_status IN ('candidate_not_confirmed','accepted','rejected')),
    generated_at_utc timestamptz NOT NULL DEFAULT clock_timestamp()
);
-- Daily historical measurements and instantaneous NWS records retain their grain.
-- Replay is deliberately excluded from the operational integration view.
CREATE VIEW integrated_weather_record AS
SELECT source_id,source_key,observed_at_utc,observed_date,event_type,
       point_geom::geometry AS geometry,'historical'::text AS record_kind
FROM historical_record
UNION ALL
SELECT source_id,source_key,observed_at_utc,NULL::date,event_type,geometry,'live'
FROM incremental_record WHERE namespace='live';
