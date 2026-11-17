# Workshop 2 data dictionary

Source of truth: executed migrations 001-004. SQL files define complete constraints
and indexes. This document explains the stored semantics; it does not imply that
all planned geographic relationships have been populated.

## Canonical and provenance tables

| Table / key | Important fields and meaning |
| --- | --- |
| `source_catalog` / `source_id` (text PK) | Source URL, declared format and attribution. |
| `raw_capture` / `capture_id` (bigint PK) | FK source; partition, relative raw path, content type, bytes, SHA-256 and origin. `(source_id,partition_key,sha256)` unique. Native HTTP capture time/headers for acquired W2 inputs are in `historical_acquisition.json`; legacy DB `retrieved_at_utc` can remain null. |
| `ingestion_run` / `run_id` (bigint PK) | Source/capture FKs; partition, status, UTC start/finish and read/accepted/rejected/unchanged counts. Optional unique `batch_key` identifies a committed Bronze batch for retry. Accepted includes inserts or changed source records, not necessarily newly discovered events. |
| `ingestion_state` / `(source_id,partition_key)` | Last successful run FK and commit-time UTC checkpoint. Historical partition state is not an NWS per-record watermark. |
| `historical_record` / `record_id` (bigint PK) | FK source, capture and last accepted run. Composite unique `(source_id,source_key)`. Holds latest canonical fields listed below. |
| `historical_record_revision` / `revision_id` (bigint PK) | Record/run/capture FKs, source row hash, normalized JSON snapshot, raw JSON and recorded UTC time. Unique `(record_id,run_id)`. Legacy raw payload may be filled from unchanged evidence without inventing a past response. |
| `record_capture_link` / `(record_id,run_id)` | Record/run/capture/revision FKs, CSV line and unchanged flag. Identifies the exact accepted revision observed by each successful run, including unchanged replays. |
| `rejected_record` / `rejected_id` (bigint PK) | Run/capture FKs, original CSV line/element, stable reason and raw JSON fields. Invalid inputs remain traceable. |
| `schema_migration` | Applied SQL filename/checksum and application time. Applied-file changes fail verification. |

## Canonical fields and Parquet

| Fields | Type / meaning |
| --- | --- |
| `source`, `source_key` | Source identity and source business key. Event ID for NOAA; station/date/element for GHCN. |
| `event_type` | NOAA source event type, or GHCN element PRCP/TMAX/TMIN. |
| `observed_at_utc` | Nullable timestamptz / Arrow timestamp(us, UTC). Populated for Storm Events; converted from supported source `CST-6`. |
| `observed_date` | Nullable date / Arrow date32. Populated for GHCN; no invented time-of-day. Exactly one of instant/date is populated. |
| `latitude`, `longitude` | Nullable double pair in WGS84. Range checked; both missing is retained. |
| `point_geom` | PostGIS generated point SRID 4326; null when no source point. Not serialized into the current Parquet schema. |
| `severity_value`, `severity_unit` | Nullable finite double plus explicit unit: kn for wind, in for hail, mm for PRCP, degC for TMAX/TMIN. Different units are never aggregated together. |
| `magnitude_type` | Nullable original wind measurement/estimate category, not a physical unit. |
| `quality_attributes` | Nullable unchanged GHCN provider attribute string; QC/trace/source flags remain available for review. |
| `geography_reference` | Source county/zone description retained in canonical DB; detailed typed identity is in `source_geography`. |
| `source_content_sha256` | Canonical JSON encoding hash of the original CSV row, including source attributes. |
| `capture_sha256` | Hash of registered input CSV bytes represented by the export; NOAA's nationwide archive hash is separately linked in acquisition evidence. |
| `record_id`, `run_id`, `capture_id`, `revision_id`, `source_line` | int64 lineage columns. A source line counts header as line 1; parsed data begins at line 2. |

The Parquet schema has 18 columns, `silver-v1` metadata, source/partition/run and
immutable lineage. A GHCN daily row can produce three measurement records.
Parquet row count equals accepted plus unchanged records for its successful run.
Rejected rows are available in database quarantine, not silently represented as
accepted Parquet values. Statistical IQR review flags in the notebook do not
alter the stored schema or remove weather extremes.

## Domain and geography tables

| Table / key | Relationships and scope |
| --- | --- |
| `storm_event` / `record_id` PK/FK | Source event ID, episode ID, geography FK, original magnitude category, raw property/crop damage, impacts JSON and full original fields. Damage suffix strings are retained; numeric currency conversion is not implemented by this slice. |
| `source_geography` / `geography_id` | Unique source/state/type/code. `C` is a county, `Z` is a forecast zone; codes are not interchangeable. Names and source classification are preserved. |
| `station` / `station_id` | Source FK, source station ID/name. Composite unique `(source_id,source_station_id)`. Current data has one GHCN station. |
| `station_location_observation` / `(station_id,capture_id)` | Capture-specific location and raw elevation. Missing new coordinates do not silently inherit an older point. |
| `daily_station_measurement` / `record_id` PK/FK | Station FK, observation date, element, numeric value/unit, original attributes/fields. Unique station/date/element. |
| `region` / `county_fips` | County name and boundary version. Empty until boundary/crosswalk evidence is reviewed. |
| `station_region_assignment` / `(station_id,county_fips,valid_from)` | Station/region FKs, validity interval, method and evidence. Empty; no current-point inference is presented as a verified historical county assignment. |

`canonical_event` is a read-only compatibility view over canonical records; its
name does not make every daily measurement a confirmed weather event.
