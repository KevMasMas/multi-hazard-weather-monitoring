# Evidence Register - Workshop 1

Status: four-source evidence is captured. Primary overlap examples are five qualified wind-record candidates over three dates, with repeated daily summaries disclosed. Eight temperature rows are supplemental and intra-NWS rows excluded. Clean lock execution passed: 59 packages, 32 cells, zero errors. Technical/artifact reviews complete; Kevin explicitly communicated both students' approval in TEAM_APPROVAL.md. Actual submission unrecorded.

## Latest wind overlap and clean verification (2026-11-16)

One bounded GHCN capture, announced before execution, returned HTTP 200 at
`2026-11-16T23:27:14.985010+00:00` (18:27:14 America/Bogota), 6,318 bytes,
35 rows/18 columns, no retries. The exact URL and selected response headers are
in the sidecar. No NWS query or NOAA redownload. Five measured-wind records
explicitly naming KOKC were extracted from the previously saved checksum-verified
2024 NOAA archive, preserving all source columns in a labelled parsed subset.

| Artifact under `workshop_1/samples/candidate_pairs/` | SHA-256 |
| --- | --- |
| `ghcn_kokc_wind_2024.csv` | `CD9E68A7FB43343E3E64D3633DF45AF08D21F97E5B6ED9D43B75E4CF82D0CCC2` |
| `ghcn_kokc_wind_2024.metadata.json` | `6B7BAEA6849429C3835AFF950E1A841853C8E17BFF77A2A0D9B04899DC5B2A7E` |
| `noaa_kokc_wind_events_2024.csv` | `0441358E52A43CA55D64EA62EF55EF155E4377137270543A8B1FFB47B83964BA` |
| `noaa_kokc_wind_events_2024.metadata.json` | `76AC5680F08EA1C5451C2D624C3FA559B1CAC509840BB03268596EB54F32ED60` |
| `historical_wind_candidate_pairs.csv` | `809E5FF7E35FA4C7065907F50D03F568195ED97C367A0DA457FDCCA90014426E` |
| `submission_evidence_audit.json` (current seven-quality/wind/daily audit) | `5AFE50CDDEC8060D8F44F1EB9A4D4FC07E2DB71E5370F63A7E5C116043EE31C3` |
| `daily_comparison_metadata.json` (QC label clarified to `qc_not_selected`) | `030077CC01FF247F49B89CAC96DC00C45F407D7289A854521DA778758B6DBEE7` |

The guide's five-candidate-record interpretation is technically addressed by
five distinct Storm IDs and three GHCN daily wind records. Three May 6 gusts
share a summary; products may share ASOS lineage. No exact gust/time equivalence,
five independent episodes, independent sensor validation or professor acceptance
claimed. Four Storm points are near the returned station; the zone-based High
Wind row keeps null coordinates and uses only its explicit airport narrative.

Clean reproduction receipt: `deliveries/01-workshop-1/clean_environment_verification.json`.
Receipt SHA-256: `BF5A9EB8D60FE51DF06E4B197E07505D8323D7AA9225817040D5F9C137F09BA7`.
Clean-executed notebook SHA-256: `04FB9E0E24DAE05DC0FB756CC9843BEF45181258FB485BE32E930717946703A0`.
The first clone exposed that the old NOAA subset Git blob used LF while the
registered original had CRLF. Commit `cce9ade` preserves the original bytes with
the same registered `987F...` SHA-256. The new isolated environment then passed
all 32 code cells and 59 exact lock pins. No sample value or registered source
hash was changed to hide the failure. Current notebook outputs are from that run.
`TEAM_APPROVAL.md` binds the current PDF/mapping hashes to Kevin's explicitly
communicated team approval; `SUBMISSION_MANIFEST.json` indexes final local
delivery hashes. Neither record represents platform submission or a grade.

Offline reproduction: `build_historical_event_pairs.py`,
`compare_daily_sources.py` (no `--fetch`), `audit_submission_evidence.py`, notebook.

## Earlier submission evidence audit (before wind follow-up; hashes superseded above)

Offline command: `python scripts/workshop_1/audit_submission_evidence.py`.
Nine registered captured-file SHA-256 values match; Q1-Q6 record claims pass;
eight daily comparison rows reproduce exactly and cover four dates with two
elements each. The audit records eleven input file hashes, including the derived
pair CSV and saved station metadata. No source response was modified or fetched.

- Artifact: `workshop_1/samples/candidate_pairs/submission_evidence_audit.json`
- SHA-256: `93BFC7307F516F194B216E3576598B2BE7DD155CE8044F1672B3BB6744D1247A`
- Contents: exact example paths/IDs/values, interpretations, sampling exclusions,
  difference-field/provenance checks and explicit unresolved same-event status.

Q1-Q5 are proposed integration-quality concerns; Q6 is extra optional-field
availability. These are not six proven provider defects. The NWS daily side is a
derived aggregate, not an original daily event record. Numerical reproducibility
and an eight-row count do not certify the guide's same-real-world-event condition.
No independent-event count or new student/professor approval is recorded.

## Current follow-up: authorized GHCN overlap capture (2026-11-16)

This entry supersedes the zero-row overlap status below, which is retained as
review history. Kevin explicitly authorized one GHCN download. A single GET
returned HTTP 200 at `2026-11-16T21:42:06.174020+00:00` (16:42:06 America/Bogota),
6,791 bytes, six rows and 301 columns; no retry or further weather request was
made. The exact URL, request time, response Date/Content-Type and body checksum
are in the adjacent metadata sidecar. This small overlap capture supplements,
rather than replaces, the existing full-year GHCN profiling sample.

Request: `https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=USW00013967&startDate=2026-10-31&endDate=2026-11-05&format=csv&units=metric&includeAttributes=true&includeStationName=true`

| Artifact under `workshop_1/samples/` | Evidence / SHA-256 |
| --- | --- |
| `region_comparison/ghcn_okc_usw00013967_2026_overlap.csv` | W1-GHCN-OVERLAP-001; unchanged response; `7456D668D4253550881435F5E9BFC95371965B7EBE72F1F8E060872F4A2D8D55` |
| `region_comparison/ghcn_okc_usw00013967_2026_overlap.metadata.json` | Capture provenance; `95FCAB6ABE20B1CEBDF66537BF551DA6EFFBDD84B864A557B34547927A63852F` |
| `candidate_pairs/cross_source_candidate_pairs.csv` | Eight daily temperature candidate records, four days; `743F284C5D6971B85794BF8B3A309383F7439999A8096CD1CF14F176895DBEB0` |
| `candidate_pairs/daily_coverage.csv` | Six-day sampling screen; `18AD89BE7FCB545F331203E87F3937AA5755981FDB30357792E29AE4575E43AF` |
| `candidate_pairs/daily_comparison_metadata.json` | Input hashes, QC exclusions and assumptions; `C7D4EA295BAE98BBBBED92898E9CAC662FAF9ABB711981A7AA133A94693FCA5A` |
| `candidate_pairs/cross_source_overlap_audit.json` | Updated saved-source coverage; `9EEFEEE748FDF0D4D42C4B1D6ACB36A03B7DAAF4FC2EFE7DB4DE1A9346C113D4` |

Offline reproduction: run `scripts/workshop_1/compare_daily_sources.py` without
`--fetch`, then `scripts/workshop_1/review_saved_evidence.py`. The notebook also
rebuilds and compares the pair table with the saved CSV. All 31 code cells executed
without errors. Prior samples and four response excerpts remain unchanged.

TMAX/TMIN candidates use October 31 and November 1, 3 and 4. November 2 fails the
proposed 70-minute maximum-gap screen; November 5 is partial. One observation
with temperature QC other than `V` is excluded. The 48-reading/70-minute rule is
a review sampling criterion, not proof of a complete daily record. Fixed CST
daily boundaries and station equivalence remain assumptions. The new response
omits coordinates; distances use the saved 2025 station metadata, explicitly
qualified in the report. PRCP is not aggregated. Eight element/day comparisons
are not eight independent weather episodes or confirmed matches.

## Evidence rules

## Earlier review correction: before the authorized follow-up capture

Current notebook: **31 executed code cells, zero errors**. All fourteen existing
CSV/GeoJSON sample hashes (including the old derived pair CSV) were found to
match the registered values during this review. Raw sample bodies are unchanged.
The old five NWS alert/KOKC pairs are now classified as **intra-NWS** and excluded
from the independent-source requirement. The full saved-file date audit finds
Storm Events in 2024, GHCN in 2025 and NWS in 2026, so the independent-source
requirement remains pending. See `ADDITIONAL_DATA_NEEDED.md` for unexecuted queries.

| New derived artifact | Rows / meaning | SHA-256 |
| --- | --- | --- |
| `workshop_1/samples/candidate_pairs/cross_source_candidate_pairs.csv` | Zero rows; required comparison schema; no invented matches | `883FC1E955AFC888296210C19AFEA87D64969AF8E60CB8ED035175F9FC06EF21` |
| `workshop_1/samples/candidate_pairs/cross_source_overlap_audit.json` | Coverage of all nonempty saved CSV/GeoJSON sources | `50172F9EE174A3DAB8AB56056FC42EE636C2418899667F469B79CBD3D7B95F63` |
| `workshop_1/samples/response_snippets/storm_events.txt` | Literal header/row from derived NOAA sample | `B962E2B23718EF8AB95A880290D228148EE010E638BE5B6E438696E9A0C8A064` |
| `workshop_1/samples/response_snippets/ghcn_daily.txt` | Literal response CSV header/row | `EEF40C41952A4EE6C79073B1B62387099AB0845B3727CD1BBBA85E12D7A8C7C5` |
| `workshop_1/samples/response_snippets/nws_alert.txt` | First alert selected key/value substrings, unchanged | `76FEBC633E4A00984A8A0C74DA28315029009C3513D42A271118D45C9BC5FB04` |
| `workshop_1/samples/response_snippets/nws_observation.txt` | First observation selected key/value substrings, unchanged | `9E26C7116C87E5935974A59BF46EC2C5C4A21329E55240ABDD65620A42AF8ADF` |
| `workshop_1/samples/response_snippets/manifest.json` | Original paths/hashes, requests, capture timestamps and excerpt hashes | `73F9054343F9B8856396F7650814704B09547ADD1E4F8E1FC1195F5CD774D30D` |

Derived artifacts are reproducible with `scripts/workshop_1/review_saved_evidence.py`.
JSON excerpts mark omitted fields with a standalone `...`; their selected lexical
values are unchanged, but the abbreviated excerpt is not a valid full JSON document.
No new API response is represented by these files.

## Preservation rules

- Preserve source responses exactly as received.
- Record retrieval time in America/Bogota and source-native/UTC timestamps where applicable.
- Record the official documentation URL, request method, parameters without secrets, response format, HTTP status, and relevant headers.
- Store only small reviewable samples under `workshop_1/samples/`; document a reproducible download method for larger evidence.
- Give every evidence item a stable identifier and reference it from the notebook, mapping, report, and change log.
- Never edit a raw sample to make it easier to profile. Derived/redacted artifacts must have a different filename and documented transformation.

## Register

| ID | Source | Evidence type | Retrieved at | Raw path | Documentation | Owner | Integrity/checksum | Status/notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W1-NOAA-SE-001 | NOAA Storm Events details | Official 2024 bulk archive plus deterministic stratified 250-row derived subset | 2026-11-04 13:56:42 America/Bogota | `workshop_1/samples/noaa_storm_events/details_sample.csv` | [Bulk CSV specification](https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/Storm-Data-Bulk-csv-Format.pdf) | Kevin | Sample SHA-256 `987F5C641B6B85BF89477A823B52757D50D2C5376895FD53056A9AFE9F79403A`; raw checksum in metadata | Captured; 250 rows, 51 columns, 14 event types, 250 distinct event IDs, zero exact duplicate rows; full notebook profile recorded; source-specific cross-review pending |
| W1-NWS-ALERTS-001 | NWS Alerts API | First active-alert poll for Oklahoma; complete response | 2026-11-04 14:14:33 America/Bogota | `workshop_1/samples/nws_alerts/poll_1.geojson` | [NWS API documentation](https://www.weather.gov/documentation/services-web-api) | Kevin | SHA-256 `1D0E2E7AA61FB7F1C43913FB4A7A58BB6FA31922516D6CC4E50166009CCED27D` | HTTP 200 GeoJSON; valid empty FeatureCollection with 0 active alerts; second poll and alert-level profiling pending |
| W1-NWS-ALERTS-002 | NWS Alerts API | Second active-alert poll for Oklahoma; complete response | 2026-11-04 15:49:29 America/Bogota | `workshop_1/samples/nws_alerts/poll_2.geojson` | [NWS API documentation](https://www.weather.gov/documentation/services-web-api) | Kevin | SHA-256 `5932B237B6751B92C46BFB5B6BD6A2F444522F4614B12D6DD1E72FC65C56716C` | HTTP 200 GeoJSON; valid empty FeatureCollection with 0 active alerts; interval from poll 1 was 5,696 seconds; comparison and field profile recorded; source-specific cross-review pending |
| W1-NWS-ALERTS-PROFILE-001 | NWS Alerts API | Complete observed recent-window pagination chain for Oklahoma | 2026-11-04 16:43:09 America/Bogota | `workshop_1/samples/nws_alerts/recent_7d_page_1.geojson`, `workshop_1/samples/nws_alerts/recent_7d_page_2.geojson` | [NWS API documentation](https://www.weather.gov/documentation/services-web-api) | Kevin | Page 1 SHA-256 `70AD394CF9E7399ACCB5CEA7B0A3B8E55526F01C314E68136439EA8442E966C3`; page 2 SHA-256 `4CB866FDD600EAC1EBDFFEF103B4F8B27E84D15EB8221914167420D158261574` | 238 features and IDs; page 2 empty with no next cursor; profile recorded in executed notebook; source-specific cross-review pending |
| P-GHCN-01 | GHCN-Daily via NCEI daily-summaries service | CSV response, one station, 2025, PRCP/TMAX/TMIN | 2026-11-03 21:49:48 -05:00 | `workshop_1/samples/ghcn_daily_usw00003017_2025.csv` | [GHCN-Daily README](https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt); [NCEI Access Data Service](https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation) | Pablo | 50,062 bytes; SHA-256 `96daedb1c41d9f3d42426ae5cc86a7dd133388ee2ca1bcd89067dc61ee2756c9` | HTTP 200; 365 rows; profile in `source-research-ghcn-nws-stations.md`; one-station candidate only |
| P-GHCN-00 | GHCN-Daily via NCEI daily-summaries service | Exploratory partial CSV response, one station, 2025-06-01 to 2025-09-01 | 2026-11-03 21:49:04 -05:00 | `workshop_1/samples/ghcn_daily_denver_2025-06_to_09.csv` | [NCEI Access Data Service](https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation) | Pablo | 12,887 bytes; SHA-256 `9e5f1fed70c5b4ef8194a346a8ea03648b64d12ba57fd90d261d4a807adce901` | HTTP 200; 93 rows; retained as scoping evidence, below 200-record profile threshold |
| P-NWS-01 | NWS station observations | GeoJSON first page, KDEN, `limit=200` | 2026-11-03 21:49:04 -05:00 | `workshop_1/samples/nws_kden_observations_poll1.geojson` | [NWS API documentation](https://www.weather.gov/documentation/services-web-api) | Pablo | 832,833 bytes after standard HTTP content decoding; SHA-256 `ed3b125abeb90803b649f0e81d0146667517f8f16d6c35ad0448882b09c080b7` | HTTP 200; 200 features; first page had `pagination.next`; paired with P-NWS-02 |
| P-NWS-02 | NWS station observations | GeoJSON first page, KDEN, `limit=200` | 2026-11-04 20:04:29 -05:00 | `workshop_1/samples/nws_kden_observations_poll2.geojson` | [NWS API documentation](https://www.weather.gov/documentation/services-web-api) | Pablo | 807,067 bytes after standard HTTP content decoding; SHA-256 `83099d933716e406dde6541fa0aa1a16fa9eae28da11797ed4d5d595de1aa870` | HTTP 200; 200 features; first page had `pagination.next`; 96 IDs shared with poll 1 and one same-ID/same-timestamp payload changed. Full request/response metadata is in adjacent JSON sidecar |
| W1-REGION-GHCN-OK-001 | GHCN-Daily via NCEI daily-summaries service | Oklahoma City coverage capture, station `USW00013967`, 2025, PRCP/TMAX/TMIN | 2026-11-05 06:38:49 America/Bogota (local file capture time) | `workshop_1/samples/region_comparison/ghcn_okc_usw00013967_2025.csv` | [NCEI Access Data Service](https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation) | Kevin | 54,843 bytes; SHA-256 `D8EE9E0AFBFE25897C17BABE4A88DC0E12D4FECE8B74C26E8D817D5309FFB5AE` | 365 rows and 12 columns; 2025-01-01 through 2025-12-31; zero null PRCP/TMAX/TMIN values; scope-comparison evidence, not statewide representativeness |
| W1-REGION-NWS-KOKC-001 | NWS station observations | Oklahoma City coverage snapshot, KOKC first page, `limit=200` | 2026-11-05 06:39:09 America/Bogota (local file capture time) | `workshop_1/samples/region_comparison/nws_kokc_observations_snapshot.geojson` | [NWS API documentation](https://www.weather.gov/documentation/services-web-api) | Kevin | 779,031 bytes; SHA-256 `391C49B75E7E05C225FE0EB63BB7BB822004169FFBB0F8FF6DDA006F236B0E68` | 200 unique features; 37.05-hour observation span; zero missing geometries; `pagination.next` present; paired with W1-REGION-NWS-KOKC-002 |
| W1-REGION-NWS-KOKC-002 | NWS station observations | Second Oklahoma City KOKC first page, `limit=200` | 2026-11-05 07:39:36 America/Bogota | `workshop_1/samples/region_comparison/nws_kokc_observations_poll_2.geojson` | [NWS API documentation](https://www.weather.gov/documentation/services-web-api) | Kevin | 779,027 bytes; SHA-256 `7857DD85FB4F35E33FA4A0EEFB0F07E6634E457D96F6A0D4C30560B5CDD07D79` | HTTP 200 `application/geo+json`; 200 unique features; zero missing geometries; `pagination.next` present; paired with W1-REGION-NWS-KOKC-001 |
| W1-NWS-KOKC-PAGE-002 | NWS station observations | Cursor page used for candidate-pair investigation | 2026-11-05 07:52:29 America/Bogota | `workshop_1/samples/candidate_pairs/nws_kokc_observations_page_2.geojson` | [NWS API documentation](https://www.weather.gov/documentation/services-web-api) | Kevin | 2,056,851 bytes; SHA-256 `A13720F4E561AC3B20E56DD15F9D43224A1EF1ABE84D37E58DF5BF5FE38BA5CD` | HTTP 200; 500 unique features; 2026-10-31T04:55Z to 2026-11-03T21:50Z; derived five-pair CSV SHA-256 `09429FE22925B3B1B2F1CCF72BD3F374920548A42290A9733A11A14F366FA275`; candidates are not confirmed matches |

## Incremental comparison register

| Source | First poll | Second poll | Evidence IDs | Observed change | Revision/deletion notes | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| NWS Alerts | 2026-11-04 14:14:33 America/Bogota | 2026-11-04 15:49:29 America/Bogota | `W1-NWS-ALERTS-001`, `W1-NWS-ALERTS-002` | Both polls contained 0 active alerts; collection `updated` timestamp and document hash changed | No alert-level revision/deletion behavior was observable | Kevin |
| NWS station observations | 2026-11-03 21:49:04 -05:00 | 2026-11-04 20:04:29 -05:00 | `P-NWS-01`, `P-NWS-02` | 80,124.882 seconds elapsed; 96 shared IDs, 104 appeared only on page 2, 104 from page 1 were not on page 2; 95 shared payloads unchanged and one same-ID/same-timestamp payload changed | Bounded pages are rolling; absence from page 2 is not evidence of deletion. One shared payload changed, cause and endpoint-wide policy unknown. | Pablo |
| NWS station observations - KOKC common region | 2026-11-05 06:39:09 America/Bogota | 2026-11-05 07:39:36 America/Bogota | `W1-REGION-NWS-KOKC-001`, `W1-REGION-NWS-KOKC-002` | 3,627.404123 seconds elapsed; 197 shared IDs, three appeared only on each page; all 197 shared payloads were unchanged | Bounded pages are rolling; absence from page 2 is not evidence of deletion. No shared-payload revision was observed in this interval. | Kevin; reviewed in joint session |

## Documentary research (not empirical evidence)

| Source | Owner | Official documentation reviewed | What remains pending |
| --- | --- | --- | --- |
| NOAA Storm Events | Kevin | See `docs/sources/noaa-storm-events.md` and evidence item W1-NOAA-SE-001 | Full profile, selected-region coverage, mapping and reviewer acceptance. |
| NWS Alerts | Kevin | See `docs/sources/nws-alerts.md` and evidence items W1-NWS-ALERTS-001/002/PROFILE-001 | Alert-level field profile, mapping, cross-source review and reviewer acceptance. |
| GHCN-Daily/NCEI | Pablo | GHCN-Daily README, NCEI Access Data Service documentation, product metadata, and sample P-GHCN-01; see `source-research-ghcn-nws-stations.md` | Use NCEI-specified GHCN-Daily v3 and article citations; NCEI metadata notes free electronic downloads and liability but does not identify a separate license. Validate full accepted-region station inventory and obtain Kevin cross-review; these cannot be inferred from a single-station sample. |
| NWS station observations | Pablo | NWS API documentation, developer FAQ, and samples P-NWS-01/02; see `source-research-ghcn-nws-stations.md` | Region-specific station/provider attribution and Kevin cross-review remain open; KDEN/KOKC poll evidence is documented, but does not establish statewide coverage. |
