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

## Conversion rules for implementation

These rules are proposals grounded in the NOAA bulk specification and NWS
unitCode fields. Preserve the raw value, unit and conversion version alongside
each derived value. Unknown codes must be flagged for review, never guessed.

| Input | Canonical rule | Missing/invalid handling |
| --- | --- | --- |
| Storm Events DAMAGE_PROPERTY / DAMAGE_CROPS | Trim whitespace; accept nonnegative decimal plus K, M or B suffix (case-insensitive): multiply by 10^3, 10^6 or 10^9 USD. `10.00K` means 10,000 USD as a rule example, not a claimed sample record. Bare numbers are USD only after field-level verification. | Blank stays null; unknown suffix, negative or malformed value is flagged. Zero is retained as reported, not proof of a measured zero loss. No inflation adjustment. |
| NOAA CZ_TIMEZONE | Read explicit fixed offset from the source code: CST-6 means UTC = local + 6 hours; EST-5 adds 5; MST-7 adds 7. Preserve date rollover. NOAA describes local standard time. | Do not apply America/Chicago daylight-saving rules automatically. Unknown/missing code remains unresolved with a reason. Keep the original local string/code. |
| NWS wmoUnit:degC / degF / K | Common temperature is degC: identity; (F - 32) * 5/9; K - 273.15. | Null stays null; retain QC. |
| NWS wmoUnit:km_h-1 / m_s-1 / kn | Common speed is m/s: divide by 3.6; identity; multiply by 0.5144444444. | Unknown dimension/unit is flagged. |
| NWS wmoUnit:m / km | Visibility in metres: identity / multiply by 1000. | Do not mix visibility with precipitation despite shared length dimension. |
| NWS precipitation wmoUnit:mm / m / in | Accumulation in mm: identity / multiply by 1000 / multiply by 25.4. | Retain accumulation duration; do not sum overlapping windows or infer zero from null. |
| NWS wmoUnit:Pa / hPa | Pressure in hPa: divide by 100 / identity. | Retain pressure type (station versus sea-level). |
| NWS wmoUnit:percent / degree_(angle) | Preserve percent humidity and degrees for direction. | Never combine these as an ordinary severity scale. |
| GHCN metric response | PRCP in mm and TMAX/TMIN in degC; preserve attributes and daily boundary. | Do not reapply native .dly scaling to the service's metric response. |

NWS unit rows above define supported conversion branches; only codes actually
present in a response may select a branch. The exact code dictionary must be
checked against the official NWS specification during implementation.

References: [NOAA bulk specification](https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/Storm-Data-Bulk-csv-Format.pdf),
[NWS API](https://www.weather.gov/documentation/services-web-api),
[NCEI Access service](https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation).

### NWS Alerts operational watermark

`ingestion_state.last_successful_query_at_utc` is the UTC timestamp of the last
successful query, committed only with its ingested snapshot. It is an operational
checkpoint, not a source-side `updated_since` cursor. Each record preserves
`sent` and `effective`; the active endpoint provides no validated record watermark.
On failure keep the prior checkpoint and retry a full active snapshot.

## Open field-level decisions

- Final NOAA timezone lookup and multi-year uniqueness constraints.
- Final severity representation for source records that do not expose a single comparable severity value.
- Exact alert polygon allocation weights and versioned county/zone boundary source.
- Final station crosswalk and element/unit conversion dictionary after statewide coverage profiling.
- SQL types, constraints and indexes after Workshop 2 implementation review.
