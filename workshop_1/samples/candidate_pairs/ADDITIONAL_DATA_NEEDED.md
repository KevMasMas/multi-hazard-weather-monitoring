# Cross-source matching gap

## Follow-up capture completed

The user authorized the one GHCN download on 2026-11-16. It returned HTTP 200;
the exact body and Date header are recorded in the 2026 overlap CSV/metadata.
The daily comparison now yields eight candidate records: TMAX/TMIN for October
31 and November 1, 3 and 4. November 2 fails the declared 70-minute gap threshold;
November 5 is partial. See `daily_coverage.csv` and
`daily_comparison_metadata.json`. The original planning text below describes the
earlier gap and is retained as history. Do not execute another download.

The audit of all committed CSV/GeoJSON samples finds disjoint years:
Storm Events 2024, GHCN 2025, NWS Alerts/observations 2026.
`cross_source_candidate_pairs.csv` therefore has the requested comparison columns
and zero rows. No source pairing is inferred from different years.
The five existing alert/KOKC rows remain **intra-NWS** examples and do not count
toward the user's independent-source requirement. Distinct APIs/products do not
establish independent observing agencies or independent physical-event evidence.

## Additional queries for the team (not executed)

### Preferred: GHCN versus saved KOKC observations

Fetch GHCN USW00013967 for **2026-10-31 through 2026-11-05**, requesting metric
PRCP/TMAX/TMIN and attributes:

```text
https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=USW00013967&startDate=2026-10-31&endDate=2026-11-05&dataTypes=PRCP,TMAX,TMIN&format=csv&units=metric&includeAttributes=true&includeStationName=true
```

Preserve raw body, exact URL, retrieval time, status, headers and SHA-256. The
saved KOKC cursor page starts 2026-10-31T04:55Z; the later pages reach
2026-11-05T11:52Z. Deduplicate by ID/content hash before daily aggregation.
First establish NCEI's daily observation boundary from attributes and station
metadata; do not assume calendar UTC days. The boundary dates are partial and
the pages may have gaps. Sampled instantaneous maxima/minima are not necessarily
official daily extrema. Null/overlapping precipitation accumulation windows
cannot be summed or treated as zero. Five comparable records are not guaranteed
by this query. Multiple elements on one day must not be described as separate
weather episodes. If fewer than five defensible records remain, report the gap.

Historical NWS observations for that window are now outside the documented
seven-day retention. Do not expect today's NWS endpoint to recover missing pages.

### Alternative: Storm Events versus GHCN

Fetch GHCN for **2024-01-01 through 2024-12-31** instead of the saved 2025 year:

```text
https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=USW00013967&startDate=2024-01-01&endDate=2024-12-31&dataTypes=PRCP,TMAX,TMIN&format=csv&units=metric&includeAttributes=true&includeStationName=true
```

Saved nearby flood candidates include EVENT_ID **1210551** (2024-08-11,
Cleveland) and **1201840** (2024-07-21, Lincoln). These are investigation targets,
not matches. The former lies roughly 20 km from the pilot station and the latter
roughly 74 km (haversine from saved point coordinates). Other saved April 27
flash-flood points are still farther away. Use an official station inventory to
select local stations before claiming five event/measurement pairs. Query the
local station for the event day and at least one preceding/following day because
daily reporting boundaries and antecedent rainfall differ from event intervals.
A single Oklahoma City rainfall value cannot validate distant flood reports.

### Storm Events versus NWS Alerts

The saved alert window is 2026-10-31 through 2026-11-03; Storm Events is 2024.
The live recent-alert API cannot supply 2024 alerts. An official archive request
to NCEI for Oklahoma CAP alerts over **2024-04-27T00:00:00Z through
2024-04-29T23:59:59Z** would permit investigation against the saved April flood
records, but archive access and availability must first be verified.
