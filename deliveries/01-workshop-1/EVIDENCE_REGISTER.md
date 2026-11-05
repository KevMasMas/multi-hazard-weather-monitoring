# Evidence Register - Workshop 1

Status: first NOAA historical sample, both NWS Alerts polls, and a complete
238-alert recent-window profiling sample captured. Executed notebook profiles
and reviewer acceptance remain pending.

## Evidence rules

- Preserve source responses exactly as received.
- Record retrieval time in America/Bogota and source-native/UTC timestamps where applicable.
- Record the official documentation URL, request method, parameters without secrets, response format, HTTP status, and relevant headers.
- Store only small reviewable samples under `workshop_1/samples/`; document a reproducible download method for larger evidence.
- Give every evidence item a stable identifier and reference it from the notebook, mapping, report, and change log.
- Never edit a raw sample to make it easier to profile. Derived/redacted artifacts must have a different filename and documented transformation.

## Register

| ID | Source | Evidence type | Retrieved at | Raw path | Documentation | Owner | Integrity/checksum | Status/notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W1-NOAA-SE-001 | NOAA Storm Events details | Official 2024 bulk archive plus deterministic stratified 250-row derived subset | 2026-11-04 13:56:42 America/Bogota | `workshop_1/samples/noaa_storm_events/details_sample.csv` | [Bulk CSV specification](https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/Storm-Data-Bulk-csv-Format.pdf) | Kevin | Sample SHA-256 `987F5C641B6B85BF89477A823B52757D50D2C5376895FD53056A9AFE9F79403A`; raw checksum in metadata | Captured; 250 rows, 51 columns, 14 event types, 250 distinct event IDs, zero exact duplicate rows; full profile and reviewer acceptance pending |
| W1-NWS-ALERTS-001 | NWS Alerts API | First active-alert poll for Oklahoma; complete response | 2026-11-04 14:14:33 America/Bogota | `workshop_1/samples/nws_alerts/poll_1.geojson` | [NWS API documentation](https://www.weather.gov/documentation/services-web-api) | Kevin | SHA-256 `1D0E2E7AA61FB7F1C43913FB4A7A58BB6FA31922516D6CC4E50166009CCED27D` | HTTP 200 GeoJSON; valid empty FeatureCollection with 0 active alerts; second poll and alert-level profiling pending |
| W1-NWS-ALERTS-002 | NWS Alerts API | Second active-alert poll for Oklahoma; complete response | 2026-11-04 15:49:29 America/Bogota | `workshop_1/samples/nws_alerts/poll_2.geojson` | [NWS API documentation](https://www.weather.gov/documentation/services-web-api) | Kevin | SHA-256 `5932B237B6751B92C46BFB5B6BD6A2F444522F4614B12D6DD1E72FC65C56716C` | HTTP 200 GeoJSON; valid empty FeatureCollection with 0 active alerts; interval from poll 1 was 5,696 seconds; comparison complete, field profile pending |
| W1-NWS-ALERTS-PROFILE-001 | NWS Alerts API | Complete observed recent-window pagination chain for Oklahoma | 2026-11-04 16:43:09 America/Bogota | `workshop_1/samples/nws_alerts/recent_7d_page_1.geojson`, `recent_7d_page_2.geojson` | [NWS API documentation](https://www.weather.gov/documentation/services-web-api) | Kevin | Page 1 SHA-256 `70AD394CF9E7399ACCB5CEA7B0A3B8E55526F01C314E68136439EA8442E966C3`; page 2 SHA-256 `4CB866FDD600EAC1EBDFFEF103B4F8B27E84D15EB8221914167420D158261574` | 238 features and IDs; page 2 empty with no next cursor; preliminary profile recorded, executed notebook and review pending |

## Incremental comparison register

| Source | First poll | Second poll | Evidence IDs | Observed change | Revision/deletion notes | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| NWS Alerts | 2026-11-04 14:14:33 America/Bogota | 2026-11-04 15:49:29 America/Bogota | `W1-NWS-ALERTS-001`, `W1-NWS-ALERTS-002` | Both polls contained 0 active alerts; collection `updated` timestamp and document hash changed | No alert-level revision/deletion behavior was observable | Kevin |
| NWS station observations | Pending | Pending | - | Not observed | Not evaluated | Pablo |
