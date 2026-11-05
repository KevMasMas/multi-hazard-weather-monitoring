# Region Comparison: Oklahoma vs. Denver

- **Workshop gate:** W1-S01
- **Date:** 2026-11-05
- **Status:** Reviewed and accepted; Oklahoma/counties selected
- **Prepared by:** Kevin Rincon

## Question

Should Team 9 use Oklahoma or Denver as the common study area for the
Multi-Hazard Weather Impact Monitoring project?

The project needs a scope that supports all four assigned sources, multiple
hazard families, meaningful regional aggregation, and a manageable semester
implementation. Denver is a city-scale candidate represented by the KDEN and
`USW00003017` samples. Oklahoma is a state-scale candidate with counties as the
proposed analytical regions.

## Evidence reviewed

The comparison uses only captured official-source evidence:

1. the NOAA Storm Events 2024 details archive already registered as
   `W1-NOAA-SE-001`;
2. Oklahoma NWS Alerts evidence `W1-NWS-ALERTS-001`,
   `W1-NWS-ALERTS-002`, and `W1-NWS-ALERTS-PROFILE-001`;
3. Pablo's Denver GHCN and KDEN evidence `P-GHCN-01`, `P-NWS-01`, and
   `P-NWS-02`;
4. the Oklahoma City coverage captures `W1-REGION-GHCN-OK-001` and
   `W1-REGION-NWS-KOKC-001`.

The Storm Events comparison applies the same 14-event-family filter used by
the registered Oklahoma sample to the same official 2024 archive. “Denver” is
approximated by records whose NOAA `CZ_NAME` contains `DENVER`; this is a
screening comparison, not a final geographic crosswalk.

## Observed comparison

| Criterion | Oklahoma candidate | Colorado / Denver candidate | Interpretation |
| --- | ---: | ---: | --- |
| Filtered 2024 Storm Events | 2,317 statewide | 1,350 Colorado statewide; 21 Denver-name records | Oklahoma offers a much larger historical event base. |
| Represented filtered event types | 14 statewide | 11 Colorado statewide; 6 Denver-name records | Oklahoma covers every selected hazard family in the one-year screen. |
| County/zone identifiers | 150 statewide | 120 Colorado statewide | Both require geographic reconciliation; Oklahoma still supports county aggregation. |
| Records missing begin coordinates | 1,681 | 992 Colorado statewide | Both need zone/county handling; neither can rely only on point coordinates. |
| Heat signal in the filtered screen | 912 Heat and 567 Excessive Heat records | No Heat or Excessive Heat records in the Colorado 2024 filtered screen | Oklahoma gives the index a stronger hot-weather component in this screen. |
| Other major observed families | 536 Thunderstorm Wind, 87 Flash Flood, 78 Cold/Wind Chill, 59 High Wind | 439 Heavy Snow, 290 Thunderstorm Wind, 273 Winter Weather, 155 High Wind | Denver/Colorado is more winter-heavy; Oklahoma is broader for a compound-hazard study. |
| GHCN-Daily qualifying sample | `USW00013967`: 365 rows, 2025, zero null PRCP/TMAX/TMIN values | `USW00003017`: 365 rows, 2025, zero null requested values | Both candidates meet the 200-record profiling threshold at one station. |
| NWS station observations | KOKC: two 200-feature polls separated by 3,627.404123 seconds; 197 shared payloads, all unchanged | KDEN: two 200-feature polls and one observed same-ID revision | Both have two-poll evidence. The different observed outcomes show why IDs and content hashes are both required. |
| NWS Alerts | Oklahoma: two active polls plus a complete observed 238-feature recent-window chain | No registered Denver alert sample | Existing alert evidence already aligns with Oklahoma. |

## Recommendation

Use **Oklahoma as the study area and counties as the primary analytical
regions**, while retaining NWS forecast zones and source geometries for an
explicit crosswalk or spatial-allocation rule.

Oklahoma is the stronger choice because it already aligns Kevin's two sources,
shows substantially greater and more varied Storm Events evidence, includes
both heat and cold/convective/flood/winter components, and now has qualifying
GHCN-Daily and KOKC station-observation coverage. Selecting Denver would require
recollecting Kevin's evidence and would leave a narrower, more winter-weighted
hazard profile in the one-year screen.

The team accepted Oklahoma/counties in the joint Kevin/Pablo working session on
2026-11-05. ADR 0001 records the decision; Denver evidence remains preserved as
an evaluated alternative and source-update example.

## Consequences and remaining validation

- Keep the historical-window candidate at 2010-2025 until volume and
  completeness are profiled across all selected Oklahoma stations and years.
- Select more than one Oklahoma GHCN/NWS station using a reproducible coverage
  rule; one Oklahoma City airport station is not statewide representation.
- Review the completed KOKC two-poll comparison and select additional Oklahoma
  stations through a reproducible coverage rule.
- Design and review a county/forecast-zone/alert-polygon/station crosswalk.
- Do not discard the KDEN captures: they remain valid evidence of same-ID
  payload revision behavior and a documented alternative considered.
- The five candidate cross-source event pairs still require temporally aligned
  Oklahoma evidence; this comparison does not claim those matches.

## Reproducibility notes

The exact Oklahoma comparison bodies and SHA-256 values are stored in
`workshop_1/samples/region_comparison/`. The NOAA archive URL, checksum, filter,
and extraction script are stored under
`workshop_1/samples/noaa_storm_events/`. All counts above are observations from
those captured artifacts; they are not forecasts or claims about every year.
