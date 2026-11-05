# Source Research - GHCN-Daily and NWS Station Observations

- **Prepared:** 2026-11-03
- **Owner:** Pablo Garzon
- **Reviewer:** Kevin Rincon
- **Status:** official documentation, qualifying GHCN sample, two NWS polls, first profiles, and preliminary contracts recorded; Kevin and shared review remain pending
- **Scope:** GHCN-Daily/NCEI (historical) and NWS station observations (incremental)

This note separates official documentation, empirical observations from the captured sample, proposals, and open validation items. Two NWS station-observation polls are preserved more than one hour apart; the comparison is limited to the bounded 200-feature pages.

Denver is used below as a **candidate test location only** because the GHCN-Daily and NWS station identifiers returned matching Denver International Airport names and nearby coordinates. The team has not selected or approved Denver as the project's final region.

## 1. GHCN-Daily through NCEI

### Documented facts

- NCEI describes GHCN-Daily as integrated station-based daily climate observations. Coverage and record length vary by station; some stations report precipitation only. See the [GHCN-Daily product page](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily) and [dataset metadata](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc%3AC00861).
- The official [GHCN-Daily README](https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt) documents station metadata and multiple distribution layouts. Its `.dly` representation is fixed-width, has one station per file, and encodes one month per line. The README also describes yearly CSV subsets and daily full/difference distributions. These are alternatives to investigate, not a selected delivery contract.
- The core GHCN elements include PRCP (tenths of mm), SNOW (mm), SNWD (mm), and TMAX/TMIN (tenths of degrees C). The README defines measurement, quality, and source flags; these must be preserved for interpretation rather than discarded.
- The [NCEI Access Data Service documentation](https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation) documents HTTP GET at `/access/services/data/v1`, dataset selection, station/date/data-type filters, CSV/JSON and other formats, optional station metadata/attributes, and supported metric/standard unit conversion for applicable datasets.
- NCEI says GHCNd is updated daily, reconstructed weekly, and that U.S. observations can be replaced by archive-quality sources typically 45-60 days after a month closes. It notes values or flags can still change after archive integration, though U.S. data changes are rare after 60 days. A queried 2025 partition is therefore not assumed immutable.
- NCEI provides a required dataset citation (GHCN-Daily Version 3, DOI 10.7289/V5D21VHZ, subset and access date) and a related journal citation. Its metadata states downloads are generally free and supplies use/distribution liability language; the page does not name a separate open-source license. Cite and describe the source, retain caveats, and avoid claiming a specific license beyond what the metadata says.

### Revised Workshop 1 inspection path

1. The current profile uses NCEI daily summaries in CSV; compare it with the official GHCN-Daily file distributions only if a later task needs that alternative. Do not mix formats in one profile without documenting the transformation.
2. The 2025 response and request metadata are preserved; avoid downloading the full archive.
3. Regional station/date/element coverage, historical revisions, and attribution still require team-level validation. The current profile is limited to one station/year.

### Preliminary mapping proposal (subject to a real sample)

| Source concept | Canonical proposal | Rule or question |
| --- | --- | --- |
| Station identifier | `station_id` and source reference | Preserve original identifier exactly; confirm exact field and whether it is stable in selected representation. |
| Observation date | `observed_at` / observation date | Daily record is not necessarily an instantaneous event. Define a date-valued daily observation representation and UTC policy with the shared model; do not invent an observation time. |
| Element (e.g., PRCP, TMAX, TMIN) | GHCN measurement type in a source-specific domain table | Keep original element code; do not treat every daily climate measurement as a discrete hazard event or collapse unlike measures into one severity. |
| Integer measurement | `value` plus `unit` | Preserve raw integer and source unit; convert only in a documented derived field. |
| Measurement/quality/source flags | domain quality and provenance fields | Preserve raw codes; profile and define acceptance/flag policy from the official code tables and observed data. |
| Station latitude/longitude/elevation/name | station dimension/reference | Station metadata may change; retain source metadata snapshot/provenance and defer region crosswalk choice until shared region decision. |
| Source payload / file row | `raw_reference`, `content_hash` | Keep raw evidence immutable; define deterministic row identity after choosing representation. |

### Draft historical ingestion contract

- **Partition proposal:** by requested date range and/or station, subject to testing NCEI service limits and comparing the yearly-file route. Avoid fetching all stations/years by default.
- **Candidate record key:** `(source_id, station_id, observation_date, element_code)` for a daily measurement. Confirm against actual representation and revision behavior before acceptance.
- **Idempotency proposal:** hash the canonicalized source record while retaining raw bytes separately; an unchanged key with changed value/flags should be recorded as a revision, not silently ignored.
- **Recovery proposal:** persist raw partition and its checksum before parsing; commit normalized records, rejects, run status, and partition state atomically. Advance any partition watermark only after commit; resume from the last committed partition.
- **Still to validate empirically:** exact query behavior across a selected region, regional volumes, partition sizes, and how frequently the chosen station/year values change in practice. The general NCEI update and reconstruction schedule is documented, but no second historical response has been compared.

### First empirical sample and profile

- **Request:** NCEI Access Data Service `GET`, dataset `daily-summaries`, station `USW00003017`, dates `2025-01-01` through `2025-12-31`, data types `PRCP,TMAX,TMIN`, CSV, metric units, station name/location and measurement attributes requested.
- **Retrieved:** 2026-11-03 21:49:48 America/Bogota (2026-11-04 02:49:48 UTC); HTTP 200; response `text/csv;charset=utf-8`.
- **Evidence:** `workshop_1/samples/ghcn_daily_usw00003017_2025.csv` (50,062 bytes; SHA-256 `96daedb1c41d9f3d42426ae5cc86a7dd133388ee2ca1bcd89067dc61ee2756c9`) with request/response metadata in the adjacent `.metadata.json` file.
- **Profile result:** 365 rows, 12 columns, one station, 365 unique dates from 2025-01-01 to 2025-12-31, and zero duplicate station-date rows. `STATION`, `NAME`, coordinates, elevation, date, and the three requested measurements had zero nulls in these rows. Coordinates were constant at latitude 39.84657 and longitude -104.65623; elevation was 1647.2 m.
- **Observed value ranges in returned metric units:** PRCP 0.0-36.3 mm (mean 1.072 mm); TMAX -12.1-37.8 C (mean 19.655 C); TMIN -25.5-23.3 C (mean 3.618 C). These describe this one station/year only.
- **Observed flags:** no nonblank quality flags in these three fields. All 365 PRCP rows had a measurement/source attribute string; 47 rows carried measurement flag `T` with numeric PRCP `0.0` (trace precipitation), and the source flag was `W` on 238 rows and `1` on 127 rows. These are provenance/interpretation details to retain, not asserted source defects.
- **Observed candidate data-quality concern:** a downstream parser that drops attributes would lose the distinction between 47 trace-precipitation records and ordinary numeric zero. Preserve and profile flags before defining missing/zero rules.
- **Limitations:** this is a single station and one year, not a regional coverage/volume estimate or a revision/update test. The NCEI service's license/attribution wording still needs confirmation for the report.

An initial NCEI scoping response for 2025-06-01 through 2025-09-01 returned 93 rows (not enough by itself for the 200-record threshold). It is retained as `workshop_1/samples/ghcn_daily_denver_2025-06_to_09.csv` with its own metadata and is not counted as the qualifying profile.

## 2. NWS Station Observations

### Documented facts

- The official [NWS API documentation](https://www.weather.gov/documentation/services-web-api) identifies `/points/{latitude},{longitude}` as a way to discover nearby observation stations, `/stations/{stationId}/observations` for recent station observations, and `/stations/{stationId}/observations/latest` for the latest single observation.
- NWS says observations are retained for seven days in this real-time service. The station list is ordered by distance from the WFO gridpoint; station data quality can vary by provider, and most stations are not maintained by NWS (ASOS is an exception).
- NWS requires a descriptive `User-Agent`; its documentation asks developers to identify the application and recommends contact information. The service is described as open data/free to use, with reasonable rate limits that are not publicly specified. Do not treat an undocumented numeric rate as verified.
- The official documentation says station observations may be delayed for upstream MADIS quality-control processing. It also records upstream known issues; these notices motivate measurement/null checks but are not findings about this team's captured response.
- NWS API timestamps are documented as ISO 8601. Its developer FAQ describes cache-aware behavior and `Cache-Control` / `Last-Modified` headers generally; whether those headers provide a useful change signal for the selected observation endpoint must be checked empirically.

### Revised Workshop 1 inspection path

1. KDEN was used as a candidate test station based on the captured station identity and Denver crosswalk; it does not imply a final region selection.
2. Two responses and their request/response metadata are preserved, each with a descriptive `User-Agent`.
3. The two bounded pages are compared by observation ID and full-feature payload; see the empirical comparison below.
4. The profile covers units, null/QC availability, timestamps, point coordinates, duplicate IDs, and page pagination. Provider coverage and longer-term retention/revision behavior remain open.

### Preliminary mapping proposal (subject to a real sample)

| Source concept | Canonical proposal | Rule or question |
| --- | --- | --- |
| Station ID and source URL | `station_id`, `source_id`, `raw_reference` | Preserve station ID and request URL exactly. Confirm any observation-level identifier from the response. |
| Observation timestamp | `observed_at` (UTC) | Parse offset-aware ISO 8601; reject/quarantine invalid timestamps. Keep retrieval time separately from observation time. |
| Station coordinates | WGS84 point / station dimension | Confirm coordinate source and validity; do not equate station location with hazard impact footprint. |
| Measurement properties | NWS observation domain table | Preserve the original property name, value, and unit code together. Select canonical measures only after inspecting the response and shared hazard scope. |
| Text/weather description and quality metadata | source-specific attributes | Preserve raw details; define normalization only after seeing actual fields and provider variation. |
| Feature identifier / request time / response headers | source provenance | Determine duplicate key/change detection empirically; hash original response for revision audit. |

### Draft incremental ingestion contract

- **Discovery:** use the selected region's coordinates with the `/points` station-discovery link, or a justified station inventory. Cache the discovery result with retrieval time; periodically recheck station/region mapping.
- **Polling:** query a bounded set of selected station IDs. Choose a cadence only after considering assignment expectations, service terms, observed data delay, and rate-limit behavior. A small, documented initial cadence is a proposal, not a verified requirement.
- **Candidate identity:** `(station_id, observed_at, source_property)` pending confirmation that the actual response has no better stable identifier.
- **Change detection:** retain raw response hash and observation-level hashes. Re-fetch with normal cache semantics; compare records and headers. Do not use random query parameters to defeat caching.
- **Watermark/recovery:** use per-station last successful retrieval/observation cursor with a bounded overlap window selected after measuring delays. Commit observations, rejects, raw reference, and cursor atomically; advance only after commit. Re-read the overlap on restart and upsert deterministically.
- **Retention limitation:** the documented seven-day history makes delayed recovery beyond the retention period a risk. Assess whether an approved local archive from the first poll is sufficient for the project and make that limitation explicit.
- **Still to validate empirically:** station/provider coverage in an accepted region, whether the observed payload revision is representative, useful cache validators, and safe polling cadence. The API documentation gives general open-data terms, User-Agent rules, retention, and attribution caveats; provider-specific third-party reuse terms must be checked when providers are identified.

### First empirical poll and profile

- **Request:** NWS API `GET https://api.weather.gov/stations/KDEN/observations?limit=200`, `Accept: application/geo+json`, descriptive `User-Agent: Team 9 Multi-Hazard Weather Monitoring Workshop 1 (student course project; contact not supplied)`.
- **Retrieved:** 2026-11-03 21:49:04 America/Bogota (2026-11-04 02:49:04 UTC); HTTP 200; content type `application/geo+json`; cache-control `public, max-age=300, s-maxage=120`.
- **Evidence:** `workshop_1/samples/nws_kden_observations_poll1.geojson` (832,833 bytes after standard HTTP content decoding; SHA-256 `ed3b125abeb90803b649f0e81d0146667517f8f16d6c35ad0448882b09c080b7`) with request/response metadata in the adjacent `.metadata.json` file. The metadata sidecar omits the response `Set-Cookie` tracking header.
- **Profile result:** 200 GeoJSON features, all `Feature`, all station ID `KDEN`; 200 unique IDs, each ID's URL timestamp matched its `properties.timestamp`. All 200 timestamps parsed as ISO-8601 offsets and were descending from 2026-11-02 11:30 UTC to 2026-11-04 02:35 UTC. No invalid/missing feature point coordinates; two distinct point coordinate pairs appeared: `[-104.66, 39.83]` (164 records) and `[-104.67, 39.86]` (36 records).
- **Observed missingness / availability findings:** `barometricPressure.value` was null in 200/200; `maxTemperatureLast24Hours.value` and `minTemperatureLast24Hours.value` were each null in 200/200; `precipitationLast3Hours.value` was null in 198/200; `precipitationLastHour.value` in 191/200; `precipitationLast6Hours.value` in 196/200; and `windGust.value` in 128/200. `temperature.value` was null in 3/200 and `windSpeed.value` in 24/200. These are sample-level missingness findings, not proof of a defect: some observation elements are conditional/optional and QC codes also appear. Preserve null and QC state; do not impute or drop silently.
- **Units observed:** temperature/dew point in `wmoUnit:degC`; wind direction in `wmoUnit:degree_(angle)`; wind speed/gust in `wmoUnit:km_h-1`; precipitation in `wmoUnit:mm`; pressure in `wmoUnit:Pa`; visibility in `wmoUnit:m`; relative humidity in `wmoUnit:percent`. Value/QC availability varied even where the unit code existed.
- **Other profile observations:** 200 valid point geometries; the same station identifier had two coordinate pairs (`[-104.66, 39.83]` and `[-104.67, 39.86]`). Timestamps had 1-67 minute intervals between adjacent records (120 of 199 intervals were not exactly five minutes). These are observed location/cadence variations requiring provider and metadata interpretation, not established defects. The response included a `pagination.next` URL, so this was a bounded first page, not all retained observations.
- **Second poll:** retrieved 2026-11-04 20:04:29 America/Bogota (2026-11-05 01:04:29 UTC); HTTP 200, `application/geo+json`, 807,067 bytes after standard content decoding; 200 features; SHA-256 `83099d933716e406dde6541fa0aa1a16fa9eae28da11797ed4d5d595de1aa870`. Exact request and response headers are recorded in the adjacent metadata sidecar.
- **Poll comparison:** 80,124.882 seconds elapsed. The bounded pages shared 96 observation IDs; 104 IDs appeared only in poll 2 and 104 from poll 1 were not present on poll 2's page. Of the 96 shared IDs, 95 payloads were unchanged and one payload changed while keeping the same ID and timestamp (`2026-11-04T01:53:00+00:00`). That record gained temperature `4.4 degC`, relative humidity `79.13634713827%`, wind chill `1.0636423271394444 degC`, cloud layer/icon/text description, and updated QC state. This supports content-hash comparison for change detection, but does not establish whether the cause was late QC, correction, or another upstream update.
- **Attribution and use:** NWS describes API data as open and free for any purpose. NWS web content is public domain unless specifically annotated otherwise; do not claim NWS endorsement, present altered data as official, or assume third-party material is covered by the same rule. Cite source, retrieval time, and station/provider where available.
- **Limitations:** these are two bounded pages, not full snapshots; absence from the later page is not proof of deletion because the rolling observation window advanced. Poll 2 did not expose a cache-control header in the captured client metadata; that single absence does not establish endpoint-wide validator behavior. The joint review accepted the content-hash rule and Oklahoma scope, not a service-wide revision claim.

### Draft station-observation update contract (revised from two polls)

- Keep the observation `id` as the provisional natural identifier and compute a deterministic hash of the full source feature so a same-ID payload change is detectable.
- Preserve both raw response bodies, retrieval timestamps, request parameters, relevant response headers, and body hashes before parsing.
- Upsert by station and observation ID while retaining changed payload versions or an auditable revision record; the observed same-ID change means an ID-only ignore strategy can miss changes.
- Do not interpret a record absent from the next bounded page as deleted. The page window advanced; use explicit source semantics or retention-aware policy before inferring deletions.
- Keep the NWS seven-day documented retention as a recovery limit; capture each successful poll before advancing a per-station watermark. A candidate overlap window should be selected from measured upstream delays and team cadence, and must fit within retention.
- These remain draft rules pending Kevin's review and a longer observation study; two polls do not prove a universal revision policy.

### GHCN-Daily source-specific contract

- Retain the daily-summary representation used for the qualifying 2025 sample; keep the .dly/yearly distribution as a future alternative rather than mixing it into this profile.
- Provisional natural key: `(STATION, DATE, element)`; preserve measurement/source/quality attributes and the station metadata snapshot.
- Preserve the original response and checksum; persist raw partition before parsing, then atomically commit normalized values, rejects, run status, and partition state.
- Treat `PRCP` trace flag `T` separately from ordinary numeric zero; do not infer measurement absence from numeric value alone.
- Revisions and service update cadence remain unmeasured. Re-fetching a historical partition and comparing content is a future validation step, not an observed behavior.

### Official citations and use notes

- GHCN-Daily Version 3 citation supplied by NCEI: Menne et al. (2012), *Global Historical Climatology Network - Daily (GHCN-Daily), Version 3*, specify the subset used, NOAA National Climatic Data Center, DOI `10.7289/V5D21VHZ`, and access date. NCEI also asks publications using the dataset to cite Menne et al. (2012), *An Overview of the Global Historical Climatology Network-Daily Database*, DOI `10.1175/JTECH-D-11-00103.1`.
- NWS API documentation describes API data as open and free to use, requires an identifying `User-Agent`, and documents seven-day station-observation retention. NWS's disclaimer says web information is public domain unless specifically annotated otherwise and prohibits implying endorsement or presenting modified material as official. The project should preserve provenance and disclose transformations; the disclaimer is not a blanket license for third-party provider data.
- Primary references: [GHCN-Daily dataset metadata](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc%3AC00861), [GHCN-Daily product page](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily), [NWS API documentation](https://www.weather.gov/documentation/services-web-api), and [NWS disclaimer](https://www.weather.gov/disclaimer). Reviewed 2026-11-04.

## 3. Questions for Kevin and shared review

- Review both candidate keys and revision handling; confirm that source identifiers and raw evidence remain available in the eventual shared mapping.
- Jointly choose the region, station-to-region rule, and historical/current windows before gathering samples.
- Decide whether both historical sources should use their assigned source APIs or whether the GHCN-Daily file distribution is the defensible profiling path; record the reason and preserve the actual format.
- Kevin should review the recorded NCEI citation/liability wording and NWS public-domain/third-party caveats for the final report; check any selected station provider separately.
- Reconcile the proposed station and measurement domain tables with NOAA Storm Events and NWS Alerts in the shared ER diagram; these proposals are not approved schema decisions.

## 4. Evidence status

Official documentation, first profiles for both assigned sources, and two preserved KDEN station-observation polls are recorded. Accepted-region evidence contains 365 Oklahoma City GHCN rows and two KOKC pages separated by 3,627.404123 seconds. The KOKC pages shared 197 unchanged IDs, while three entered and three left the bounded page; this does not imply deletion or a service-wide policy. An additional cursor page supports five deterministic unconfirmed candidate pairs. The notebook executes top to bottom with Oklahoma evidence. ADRs 0001, 0003 and 0004 plus `PABLO_REVIEW.md` record the accepted scope, time and station/geographic rule. Full multi-station coverage and production schema remain implementation work.
