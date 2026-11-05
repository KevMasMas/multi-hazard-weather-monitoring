# NWS Alerts Evidence

This folder stores small, exact copies of the two Workshop 1 alert polls and
their versioned metadata. Bulk or repeated operational responses belong under
ignored `data/raw/nws_alerts/` storage.

Capture the first poll with:

From an open PowerShell console at the repository root:

```powershell
& .\scripts\workshop_1\capture_nws_alerts.ps1 -PollLabel poll_1
```

Wait at least one hour and capture the second poll with:

```powershell
& .\scripts\workshop_1\capture_nws_alerts.ps1 -PollLabel poll_2
```

The script supports Windows PowerShell 5.1 and PowerShell 7. If local execution
policy blocks the script, start a one-time child process without changing the
machine policy:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\scripts\workshop_1\capture_nws_alerts.ps1" -PollLabel poll_2
```

Do not overwrite either raw response. Register exact timestamps, checksums, and
paths in `deliveries/01-workshop-1/EVIDENCE_REGISTER.md`.

## Current evidence

`poll_1.geojson` was captured successfully on 2026-11-04 at 19:14:33 UTC
(14:14:33 America/Bogota). It is a valid HTTP 200 GeoJSON FeatureCollection,
but Oklahoma had zero active alerts at that instant. The empty collection is a
real observation and must not be replaced or edited.

`poll_2.geojson` was captured successfully on 2026-11-04 at 20:49:29 UTC
(15:49:29 America/Bogota), 1 hour 34 minutes 56 seconds after poll 1. It also
contained zero active alerts. `poll_comparison.yaml` records the exact comparison.

The two-poll requirement is now evidenced, but alert-level profiling remains
blocked by the empty collections. Capture a separately labeled recent-alert
response from the API's seven-day window for profiling; do not replace either
active-state poll.

## Recent-window profiling evidence

`recent_7d_page_1.geojson` and `recent_7d_page_2.geojson` preserve the complete
observed pagination chain for the separately labeled profiling request. Page 1
contains 238 alerts; following its cursor produced an empty page 2 without a
next cursor. See `recent_7d_metadata.yaml` for integrity data and
`recent_7d_preliminary_profile.md` for observed aggregates.

Future captures should use the Windows PowerShell-compatible script:

```powershell
& .\scripts\workshop_1\capture_nws_recent_alerts.ps1
```

