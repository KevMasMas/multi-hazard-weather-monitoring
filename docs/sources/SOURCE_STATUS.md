# Source Status Log

This log satisfies the Team 9 requirement to track operational source changes.
It records only observed or officially documented status; absence of an issue is
not a guarantee of future availability.

| Reviewed (UTC) | Source | Observed status | Evidence | Follow-up |
| --- | --- | --- | --- | --- |
| 2026-11-04 | NOAA Storm Events | 2024 archive downloaded and checksum-verified; deterministic Oklahoma sample produced. | `W1-NOAA-SE-001` | Recheck archive checksum before multi-year historical ingestion because published archives can be revised. |
| 2026-11-04 | NWS Alerts | Two Oklahoma active polls returned HTTP 200 with zero features; separate recent-window pagination returned 238 features. | `W1-NWS-ALERTS-001`, `W1-NWS-ALERTS-002`, `W1-NWS-ALERTS-PROFILE-001` | Do not interpret an empty active response as an outage; revalidate pagination and headers during Workshop 3. |
| 2026-11-04 | GHCN-Daily / NCEI | CSV access validated for pilot station/year samples. | Workshop 1 evidence register | Validate statewide station coverage and partition volume before historical implementation. |
| 2026-11-05 | NWS Station Observations | KOKC bounded pages returned data and pagination; KDEN retained evidence contains one same-ID content revision. | Workshop 1 evidence register and notebook | Preserve content hashes and revalidate retention/pagination behavior during Workshop 3. |

Update this table when an endpoint, schema, availability rule, attribution rule,
or observed behavior changes. Link every empirical entry to preserved evidence.
