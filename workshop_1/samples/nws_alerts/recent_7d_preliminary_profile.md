# NWS Recent Alerts - Preliminary Profile

Evidence ID: `W1-NWS-ALERTS-PROFILE-001`

This profile describes the complete observed pagination chain for
`GET /alerts?area=OK` captured on 2026-11-04. It supports field profiling and
does not replace the two active-state polls.

## Integrity and completeness

- Page 1: 238 features, 1,418,905 bytes.
- Page 2: 0 features, 213 bytes, no next cursor.
- Total: 238 features.
- Distinct feature IDs: 238.
- Distinct `properties.id` values: 238.
- Identifier duplicates observed: 0.
- Null geometries: 42; Polygon geometries: 196.

The first page exposed a `pagination.next` URL. Following it produced an empty
second page without another cursor, closing the observed pagination chain.

## Temporal range

- Earliest `sent`: 2026-10-31 02:11:00 UTC.
- Latest `sent`: 2026-11-03 09:56:00 UTC.
- All 238 records contained `sent`, `effective`, `onset`, and `expires`.
- `ends` was null in 42 records.

## Event distribution

| Event | Count |
| --- | ---: |
| Severe Thunderstorm Warning | 136 |
| Special Weather Statement | 42 |
| Tornado Watch | 32 |
| Tornado Warning | 18 |
| Dense Fog Advisory | 6 |
| Wind Advisory | 4 |

## Update semantics observed

| Message type | Count |
| --- | ---: |
| Alert | 109 |
| Update | 84 |
| Cancel | 45 |

References were present in 129 records and absent in 109. Reference-list
lengths ranged from one to five where present. This makes `messageType`,
`references`, alert identifiers, and content hashes required inputs to the
incremental contract; exact update-chain rules still require notebook analysis.

## Severity and geography

| Severity | Count |
| --- | ---: |
| Extreme | 32 |
| Severe | 110 |
| Moderate | 51 |
| Minor | 45 |

All records were `Actual` and category `Met`. Geometry was null in 42 records,
but every record exposed one or more `affectedZones`. A null polygon must not be
treated as missing geographic scope without checking `affectedZones`, `geocode`,
and `areaDesc`.

Issuing offices included NWS Norman, Tulsa, Amarillo, and Shreveport. Offices
outside Oklahoma can legitimately issue products affecting Oklahoma; this is
an observed integration consideration, not automatically a quality defect.

## Missingness observations

- `instruction` was null in 79 records.
- `ends` was null in 42 records.
- `geometry` was null in 42 records.
- No nulls were observed in identifiers, event, message type, severity,
  certainty, urgency, sent/effective/onset/expires, area description, headline,
  or description.

These findings are preliminary. The executed project notebook must reproduce
the aggregates, show examples, and decide which observations qualify among the
five required concrete data-quality issues.

