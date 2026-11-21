# Incremental source and state contract

Implementation: `src/multi_hazard_weather_monitoring/incremental.py` and
`event_candidates.py`; additive migration `sql/005_incremental_ingestion.sql`.
Team policy is in `config/workshop3_incremental.json`. No applied W2 migration
was edited. Personal review of this W3 decision remains pending.

## Queries and retention

- Alerts: active snapshots for `area=OK`. Keep stable feature URI, original
  CAP identifier, sent/effective/onset/expiry, severity/category, zones, polygon
  and references in preserved raw revisions. No provider record watermark is
  asserted. The complete-query timestamp is the coverage watermark.
- Observations: configured KOKC station, explicit start/end, limit 500 and the
  returned pagination chain. Initial query covers the preceding seven days;
  subsequent hourly queries overlap the last complete query by one hour.
  At least every 24 hours, reconcile the entire seven-day retention window.
  These intervals are implementation choices, not an asserted NWS requirement.
- A gap older than retention is flagged in `pages[0].window`; it is not recovered
  through a fictional API archive. Coverage means a complete returned chain for
  the requested interval, not proof every expected observation is present.
  Offline audit of the live capture found 902 timestamps inside the requested
  interval and one before its start; none follows the end. Preserve all returned
  bytes/records and apply explicit analysis-time filters. Cause is unverified;
  see `evidence/nws_window_review.json`.
- NWS requires an identifying User-Agent; its rate threshold is not public.
  The official service documents seven-day observation retention and caching.
  Reference: <https://www.weather.gov/documentation/services-web-api> (checked
  2026-11-21). Numeric limits are not invented.

## Persistence and change semantics

Raw bytes are content-addressed, immutable and ignored under `data/raw/`.
Poll metadata retains URL, retrieval UTC, path, byte count and SHA-256.
Feature identity is `(source, namespace, source URI)`; content identity is
SHA-256 of sorted, compact feature JSON. This detects content changes rather
than attributing an unsupported source revision counter.

`incremental_record` retains latest accepted fields and geometry.
`incremental_revision` retains original and normalized fields for every observed
content transition, including reversions. `incremental_sighting` traces unchanged
records to page hash/index/poll. Each actual poll has counters; an unchanged
database replay is a new receipt, not a new business record or source revision.

One source/scope transaction writes records, revisions, sightings, rejects, run
metrics and state. A source/namespace/scope advisory lock prevents concurrent
overwrite; an older query timestamp cannot replace a newer committed snapshot.
Failure rolls back record/state changes and writes a separate failure receipt.
Invalid envelopes or incomplete pagination fail the poll. Invalid features are
quarantined with reasons; a poll with rejects does not advance coverage state.
Duplicate IDs within one poll are conservatively quarantined, rather than letting
ambiguous page order choose a version. Missing IDs never imply deletion.

`replay`, `test` and `live` namespaces do not mix. The operational
`integrated_weather_record` view combines historical records and live NWS records;
it excludes replay/test. It preserves daily versus instantaneous time grain.
NWS data does not enter the frozen historical Gold batch automatically.

## Quantities and quality

Supported temperatures become degrees C; supported wind quantities become m/s;
precipitation in metres becomes mm. Preserve source value, unit code and QC code
alongside the conversion. Missing remains missing. Unsupported units have an
explicit unsupported status and no invented converted value. Physical-invalidity
checks quarantine invalid coordinates, negative wind/precipitation, impossible
relative humidity, nonpositive pressure and temperature below absolute zero.
Provider QC codes remain uninterpreted review evidence, not a blanket validity
certificate. Alert categorical severity is not a numeric observation magnitude.

## Polling, retries and activation

HTTPS requests are restricted to `api.weather.gov`; each page has a 30-second
timeout and at most four attempts. Retry transient HTTP 429/5xx and connection
timeouts with bounded exponential delay, honoring Retry-After. A Retry-After
above five minutes fails for a later scheduled retry rather than retrying early.
Cycles, untrusted next URLs and a 20-page bound fail; no partial-success watermark.
Raw pages acquired before failure are retained and referenced in its receipt.

The DAG has two source tasks followed by candidate grouping, one active run,
two task retries with exponential backoff and 15-minute source-task timeouts.
Network defaults to disabled; automatic hourly scheduling is enabled only when
`NWS_POLL_MODE=live` and a local identifying User-Agent are configured, containers
are recreated and the DAG is unpaused. It was left paused after replay validation.
The bounded live CLI validation is evidence of two source queries, not an uptime
or scheduled-frequency compliance claim.

## Candidate inference

`nws_polygon_validity_v1`: one nearest-in-time observation per alert whose station
point satisfies PostGIS `ST_Covers` and whose timestamp is inside effective/expiry.
No missing-polygon county fallback or arbitrary nearest-station assignment is
invented. Persist rule version, both IDs/content hashes, evidence and unconfirmed
status. Five saved-data associations are **intra-NWS**, not independent-source
matches, independent episodes or confirmed impacts. Live validation produced none
because the active-alert response was empty. No precision/recall claim is made.

The five W1 NOAA/GHCN wind candidate rows are checksum-verified, indexed historical
context. They remain candidates with daily-timing and reporting-lineage caveats;
they are not newly discovered W3 matches. Reviewed county allocation, current
historical-source overlap and labelled event-match evaluation remain open.

## Observed verification

- First saved replay: 238 new alerts, 700 new observations, zero rejects.
- Second pass: 238/700 unchanged, zero additional records/revisions.
- Alerts' saved chain is complete. KOKC saved pages are partial/non-contiguous:
  they do not advance a coverage watermark.
- Announced live queries on 2026-11-21: zero active OK alerts and 903 KOKC records;
  complete returned chains, zero rejects. Captured-response replays are unchanged.
- Twelve synthetic/fault and isolated-PostGIS tests pass, including a forced
  exception after the record update but before revision/state commit. These
  fixtures are software evidence, never real weather events.

Exact times, counts, page hashes, test-source fingerprints and DAG state are in
`evidence/incremental_*.json`. Original live bytes remain in ignored local storage;
committed live excerpts are explicitly parsed derivatives.
