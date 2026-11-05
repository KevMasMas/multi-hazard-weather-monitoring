# Workshop 1 Conceptual ER Model

- **Status:** Accepted conceptual model for Workshop 1
- **Date:** 2026-11-05
- **Station/geography owner:** Pablo Garzon
- **Canonical integration owner:** Kevin Rincon
- **Implementation:** Workshop 2 migrations after field-level review

This model separates immutable raw captures, source-specific records,
analytical regions, and inferred event groups. It is conceptual: names and
cardinalities guide the first SQL design but do not claim implemented tables.

```mermaid
erDiagram
    SOURCE ||--o{ RAW_CAPTURE : supplies
    SOURCE ||--o{ STATION : catalogs
    RAW_CAPTURE ||--o{ STORM_EVENT : contains
    RAW_CAPTURE ||--o{ ALERT_VERSION : contains
    RAW_CAPTURE ||--o{ DAILY_STATION_MEASUREMENT : contains
    RAW_CAPTURE ||--o{ STATION_OBSERVATION_VERSION : contains
    RAW_CAPTURE ||--o{ REJECTED_RECORD : quarantines

    REGION ||--o{ STATION_REGION_ASSIGNMENT : contains
    STATION ||--o{ STATION_REGION_ASSIGNMENT : assigned_to
    REGION ||--o{ REGION_SOURCE_GEOGRAPHY : maps
    SOURCE_GEOGRAPHY ||--o{ REGION_SOURCE_GEOGRAPHY : allocated_to

    STATION ||--o{ DAILY_STATION_MEASUREMENT : reports
    STATION ||--o{ STATION_OBSERVATION_VERSION : reports

    SOURCE_GEOGRAPHY ||--o{ STORM_EVENT_GEOGRAPHY : locates
    STORM_EVENT ||--o{ STORM_EVENT_GEOGRAPHY : has
    SOURCE_GEOGRAPHY ||--o{ ALERT_GEOGRAPHY : covers
    ALERT_VERSION ||--o{ ALERT_GEOGRAPHY : has

    EVENT_GROUP ||--o{ EVENT_GROUP_MEMBER : groups
    STORM_EVENT ||--o{ EVENT_GROUP_MEMBER : candidate_member
    ALERT_VERSION ||--o{ EVENT_GROUP_MEMBER : candidate_member
    STATION_OBSERVATION_VERSION ||--o{ EVENT_GROUP_MEMBER : candidate_member

    REGION {
        uuid region_id PK
        string region_type
        string state_fips
        string county_fips
        geometry geometry
        date valid_from
        date valid_to
    }
    SOURCE_GEOGRAPHY {
        uuid source_geography_id PK
        uuid source_id FK
        string geography_type
        string source_code
        geometry geometry
        string raw_reference
    }
    STATION {
        uuid station_id PK
        uuid source_id FK
        string source_station_code
        string provider
        geometry geometry
        date valid_from
        date valid_to
    }
    RAW_CAPTURE {
        uuid raw_capture_id PK
        uuid source_id FK
        datetime retrieved_at_utc
        string sha256
        string raw_reference
        integer http_status
    }
    STORM_EVENT {
        uuid storm_event_id PK
        uuid raw_capture_id FK
        string source_event_id
        string event_type
        datetime begin_at_utc
        datetime end_at_utc
        string content_hash
    }
    ALERT_VERSION {
        uuid alert_version_id PK
        uuid raw_capture_id FK
        string source_alert_id
        datetime effective_at_utc
        datetime expires_at_utc
        string severity
        string message_type
        string content_hash
    }
    DAILY_STATION_MEASUREMENT {
        uuid measurement_id PK
        uuid raw_capture_id FK
        uuid station_id FK
        date observation_date
        string element_code
        number value
        string unit
        string attributes
    }
    STATION_OBSERVATION_VERSION {
        uuid observation_version_id PK
        uuid raw_capture_id FK
        uuid station_id FK
        string source_observation_id
        datetime observed_at_utc
        string content_hash
    }
    EVENT_GROUP {
        uuid event_group_id PK
        string matching_rule_version
        string review_status
    }
    EVENT_GROUP_MEMBER {
        uuid event_group_member_id PK
        uuid event_group_id FK
        string member_type
        uuid member_id
        number match_score
        string match_status
    }
```

## Modeling rules

- `RAW_CAPTURE` is immutable and content-addressed; normalized rows retain its
  reference.
- Source identities and content versions are separate so same-ID revisions are
  auditable.
- `REGION` stores Oklahoma counties; source zones/polygons remain in
  `SOURCE_GEOGRAPHY` with many-to-many allocation.
- Daily GHCN dates remain dates. NWS/Storm Events instants are normalized to UTC
  while original time fields remain in raw evidence.
- `EVENT_GROUP_MEMBER` is an inferred relationship with a rule version and
  review status. Candidate pairs never become confirmed merely because they
  share time/geography.
- Invalid records retain raw provenance and a rejection reason.

## Open SQL-level decisions

- Exact PostgreSQL/PostGIS types, indexes and constraints.
- Hazard-specific domain tables and severity/value representation.
- Polymorphic event-group membership implementation versus separate link
  tables.
- Boundary/crosswalk data source and versioning mechanism.
- Final uniqueness constraints after multi-year duplicate profiling.
