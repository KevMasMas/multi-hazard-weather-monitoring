# NWS Alerts - Workshop 1 Source Notes

**Owner:** Kevin Rincon  
**Reviewer:** Pablo Garzon  
**Task IDs:** W1-K02 (documentation), W1-K04 (two polls and profile)  
**Status:** documentation and two active-state polls captured; field sample and profile pending

## Role in Team 9

NWS Alerts is Kevin's incremental source. It provides current watches, warnings,
advisories, and related alert products. It complements NOAA Storm Events; it
does not replace the historical source.

## Official references

- [NWS API Web Service](https://www.weather.gov/documentation/services-web-api)
- [NWS Alerts Web Service](https://www.weather.gov/documentation/services-web-alerts)
- [NWS OpenAPI specification](https://api.weather.gov/openapi.json)
- [Alerts geolocation guide](https://www.weather.gov/documentation/services-web-alerts)

## Workshop endpoint

The proposed Oklahoma feasibility request is:

```text
GET https://api.weather.gov/alerts/active?area=OK
Accept: application/geo+json
User-Agent: multi-hazard-weather-monitoring/0.1 (github.com/KevMasMas/multi-hazard-weather-monitoring)
```

NWS requires an identifying `User-Agent`. The API applies reasonable rate
limits, and the alerts documentation recommends no more than one request every
30 seconds. Team 9 needs only the two Workshop 1 polls, separated by at least
one hour according to the course specification.

## Capture contract

Each poll must preserve:

- the exact GeoJSON response body;
- request URL, headers, status, content type, and retrieval time in UTC;
- response headers relevant to caching or revision behavior;
- byte size and SHA-256 checksum;
- feature count, distinct feature IDs, and missing-geometry count;
- the exact script and version used.

The raw response and response headers remain under ignored `data/raw/` storage.
If the response is reviewably small, an exact copy may be placed under
`workshop_1/samples/nws_alerts/` and registered as evidence.

Run the capture script directly from either Windows PowerShell 5.1 or
PowerShell 7:

```powershell
& .\scripts\workshop_1\capture_nws_alerts.ps1 -PollLabel poll_1
```

## Fields to profile

Inspect at least:

- feature `id` and `properties.id`;
- `status`, `messageType`, `category`, `event`, `sender`, and `senderName`;
- `sent`, `effective`, `onset`, `expires`, and `ends`;
- `urgency`, `severity`, and `certainty`;
- `areaDesc`, `geocode`, `affectedZones`, and GeoJSON `geometry`;
- `references`, `parameters`, `headline`, `description`, and `instruction`.

Observed nulls, identifier behavior, update chains, and geometry behavior must be
reported from the two real captures, not inferred from the schema alone.

## Incremental comparison

After the second poll, compare alerts by stable feature identifier and content
hash. Classify records as:

- new in poll 2;
- unchanged;
- same identifier with changed content;
- no longer active in poll 2.

An alert missing from the second active response is not necessarily deleted; it
may have expired or otherwise become inactive. Preserve both raw polls before
interpreting the change.

## First observed poll

Evidence `W1-NWS-ALERTS-001` captured Oklahoma active alerts on 2026-11-04 at
19:14:33 UTC. The API returned HTTP 200 and `application/geo+json`, with a valid
FeatureCollection containing zero features. This proves successful access and
an empty current state only; it does not validate alert-level fields or update
behavior. The response must remain part of the evidence set.

## Second observed poll and comparison

Evidence `W1-NWS-ALERTS-002` was captured 5,696 seconds after the first poll,
satisfying the required one-hour interval. It also returned HTTP 200 GeoJSON
with zero features. The collection-level `updated` timestamp changed from
19:13:19 UTC to 20:45:06 UTC, and the response checksum changed accordingly,
but no alert-level addition, removal, or modification could be observed.

The two polls prove reproducible access and an unchanged empty active state.
They do not provide the records needed to profile alert fields.

The separately labeled evidence `W1-NWS-ALERTS-PROFILE-001` therefore captured
the recent `/alerts?area=OK` collection. Its complete observed pagination chain
contains 238 unique alerts. This satisfies the record threshold for source
profiling but does not replace the two active-state observations.

## Limitations to retain

- `/alerts/active` is a current-state feed, not a historical archive.
- The general `/alerts` endpoint contains only the past seven days.
- A state response may contain fewer than 200 active alerts. In that case,
  profile the full response rather than widening the region merely to reach a
  target count.
- Alert geography can use polygons, affected zones, and UGC codes; a null
  geometry does not imply that the alert lacks geographic scope.

