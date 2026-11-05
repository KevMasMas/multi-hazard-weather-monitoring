# Preliminary Canonical Mapping

- **Status:** Workshop 1 draft
- **Study area:** Oklahoma, aggregated by county
- **Time rules:** instants normalize to UTC; GHCN daily dates remain calendar dates
- **Coordinate rules:** preserve source geometry and normalize analytical geometry to WGS84 decimal degrees

This is the independent mapping artifact required by Workshop 1. It summarizes
the executed notebook and accepted conceptual model without claiming that the
Workshop 2 database schema exists.

## Required canonical event fields

| Canonical field | NOAA Storm Events | GHCN-Daily | NWS Alerts | NWS station observations | Draft rule |
| --- | --- | --- | --- | --- | --- |
| `event_id` | `EVENT_ID` | `STATION` + `DATE` + element code | `properties.id` (cross-check feature `id`) | `properties.@id` | Namespace by source; never assume identifiers are globally unique. |
| `source` | Constant `noaa_storm_events` | Constant `ghcn_daily` | Constant `nws_alerts` | Constant `nws_station_observations` | Reference the source catalog entry. |
| `event_type` | `EVENT_TYPE` | Element code such as `PRCP`, `TMAX`, `TMIN` | `properties.event` | Measurement/observation type | Preserve the original classification and map separately to CHI components. |
| `timestamp` | `BEGIN_DATE_TIME` plus `CZ_TIMEZONE` | `DATE` | `properties.effective`; retain `sent`, `onset`, `ends`, `expires` | `properties.timestamp` | Convert instants to UTC; do not invent an intraday time for GHCN. |
| `latitude` | `BEGIN_LAT`; may be absent for zone events | Station latitude | Geometry centroid is not substituted for the original polygon; derived regional allocation is separate | Feature point latitude | Preserve missingness and original geometry. |
| `longitude` | `BEGIN_LON`; may be absent for zone events | Station longitude | Same rule as latitude | Feature point longitude | WGS84 decimal degrees after validation. |
| `severity` | Hazard-specific magnitude/impact fields | Measurement `value` | `properties.severity` | Measurement `value` | Severity is domain-specific; retain its unit and do not force incomparable values into one scale. |
| `raw_reference` | Archive name, `EVENT_ID`, raw checksum | Request/partition path, station/date, checksum | Raw response path, alert ID, checksum | Raw response path, observation ID, checksum | Every normalized record retains immutable capture provenance and a content hash. |

## Source-specific fields and domain tables

### `storm_event`

| Field | Source field | Rule |
| --- | --- | --- |
| `episode_id` | `EPISODE_ID` | Preserve source identifier. |
| `event_type` | `EVENT_TYPE` | Preserve NOAA category. |
| `begin_at` / `end_at` | begin/end date-time fields and `CZ_TIMEZONE` | Convert with an explicit timezone mapping and retain original strings. |
| `magnitude` / `magnitude_type` | `MAGNITUDE`, `MAGNITUDE_TYPE` | Keep nullable and unit/type-qualified. |
| `damage_property` / `damage_crops` | `DAMAGE_PROPERTY`, `DAMAGE_CROPS` | Preserve raw text; parsing rules require later validation. |
| `deaths` / `injuries` | direct + indirect fields | Preserve separate source measures. |
| `source_geography` | `CZ_TYPE`, state/county/zone identifiers and coordinates | Apply ADR 0004; do not invent a point for zone records. |

### `daily_station_measurement`

| Field | Source field | Rule |
| --- | --- | --- |
| `station_id` | `STATION` | Preserve GHCN station identifier. |
| `observation_date` | `DATE` | Calendar date, not a fabricated UTC instant. |
| `element_code` | `PRCP`, `TMAX`, `TMIN` | Normalize wide source columns to measurement rows during Workshop 2. |
| `value` | corresponding element value | Preserve requested metric output. |
| `attributes` | `<ELEMENT>_ATTRIBUTES` | Keep measurement, quality and source flags; trace precipitation is not ordinary zero. |
| `station_geometry` | `LATITUDE`, `LONGITUDE`, `ELEVATION` | Validate ranges and retain elevation unit metadata. |

### `alert_version`

| Field | Source field | Rule |
| --- | --- | --- |
| `source_alert_id` | `properties.id` | Stable identity candidate; compare content hash for revisions. |
| `message_type` | `properties.messageType` | Preserve CAP message semantics. |
| `severity` / `certainty` / `urgency` | matching CAP fields | Preserve categorical values separately. |
| `effective_at` / `expires_at` | `effective`, `onset`, `ends`, `expires` | Parse as offset-aware instants and normalize to UTC. |
| `source_geography` | feature geometry, `affectedZones`, UGC/geocode | Apply polygon/county or versioned zone/county mapping from ADR 0004. |
| `content_hash` | canonical serialization of the feature | Detect same-ID changes without replacing raw evidence. |

### `station_observation_version`

| Field | Source field | Rule |
| --- | --- | --- |
| `source_observation_id` | `properties.@id` | Use with source namespace; do not infer deletion from a rolling page. |
| `station_id` | `properties.stationId` | Preserve NWS identifier; link to GHCN only with reviewed evidence. |
| `observed_at` | `properties.timestamp` | Normalize to UTC and retain retrieval time separately. |
| `measurements` | each `{value, unitCode, qualityControl}` property | Preserve value, unit and QC together; null optional elements remain null. |
| `geometry` | feature point | Preserve per-observation point and validate coordinate range. |
| `content_hash` | canonical serialization of the feature | Required because the retained KDEN evidence includes a same-ID payload revision. |

## Supporting entities

- `source`, `raw_capture`, `ingestion_run`, `ingestion_state`, and `rejected_record` support provenance and recovery.
- `region`, `source_geography`, `region_source_geography`, `station`, and `station_region_assignment` implement the accepted county/station contract.
- `event_group` and `event_group_member` store versioned, reviewable cross-source match decisions.
- CHI component tables or analytical views belong to Workshop 4 and are not implemented here.

## Open field-level decisions

- Final NOAA timezone lookup and multi-year uniqueness constraints.
- Final severity representation for source records that do not expose a single comparable severity value.
- Exact alert polygon allocation weights and versioned county/zone boundary source.
- Final station crosswalk and element/unit conversion dictionary after statewide coverage profiling.
- SQL types, constraints and indexes after Workshop 2 implementation review.
