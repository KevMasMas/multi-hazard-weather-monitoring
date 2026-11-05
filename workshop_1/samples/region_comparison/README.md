# Oklahoma Region-Comparison Evidence

This directory contains small, unmodified responses used only to compare the
Oklahoma and Denver candidates for Workshop 1 decision `W1-S01`.

## Files

- `ghcn_okc_usw00013967_2025.csv`: 365 daily rows for Oklahoma City Will
  Rogers World Airport (`USW00013967`) from the NCEI daily-summaries service.
- `nws_kokc_observations_snapshot.geojson`: one bounded 200-feature page from
  the NWS KOKC station-observations endpoint.
- `nws_kokc_observations_poll_2.geojson`: the second bounded 200-feature KOKC
  page, captured 3,627.404123 seconds after the first local capture time.
- `nws_kokc_observations_poll_2.metadata.json` and
  `nws_kokc_observations_poll_2.response_headers.json`: exact request/result
  metadata and sanitized response headers for poll 2.
- `source_metadata.yaml`: request scope, observed profile facts, checksums, and
  limitations for both captures.

These files show that the Oklahoma candidate can meet the Workshop 1 minimum
profile size for Pablo's two sources. The KOKC pages share 197 IDs; all 197
shared payloads are unchanged, while three IDs entered and three left the
bounded rolling page. Absence from the later page is not treated as deletion.
The existing KDEN polls remain valid evidence of one observed same-ID payload
revision in the tested alternative region.

The full comparison and recommendation are documented in
`docs/reports/region-comparison-oklahoma-vs-denver.md`.
