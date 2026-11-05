# Workshop 1 Evidence Scripts

Run these commands from the repository root with Windows PowerShell 5.1 or
PowerShell 7. The scripts preserve live responses under ignored `data/raw/`
storage. A reviewed, checksum-registered copy must be placed under
`workshop_1/samples/` before it becomes submission evidence.

## NWS station observations

Capture a bounded 200-feature KOKC page:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/workshop_1/capture_nws_station_observations.ps1 `
  -StationId KOKC `
  -PollLabel poll_2
```

The script records the raw GeoJSON body, response headers without
`Set-Cookie`, retrieval metadata, HTTP status, feature counts, timestamp range,
pagination presence, bytes, and SHA-256. The default identifying User-Agent is
documented in the script and can be overridden with `-UserAgent`.

Compare two preserved pages:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/workshop_1/compare_nws_station_polls.ps1 `
  -FirstPollPath workshop_1/samples/region_comparison/nws_kokc_observations_snapshot.geojson `
  -SecondPollPath workshop_1/samples/region_comparison/nws_kokc_observations_poll_2.geojson
```

The comparison reports shared, entering, and leaving IDs plus unchanged and
changed shared payloads. Records that leave a bounded rolling page are not
classified as deletions.

To preserve the next page returned by `pagination.next`, pass the cursor value
without manually rebuilding the URL:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/workshop_1/capture_nws_station_observations.ps1 `
  -StationId KOKC `
  -PollLabel page_2 `
  -Cursor "CURSOR_FROM_PAGINATION_NEXT"
```

## Existing source scripts

- `capture_nws_alerts.ps1`: one active-alert poll for a two-letter state area.
- `capture_nws_recent_alerts.ps1`: recent alert pagination evidence.
- `extract_noaa_storm_events_sample.ps1`: deterministic Oklahoma subset from
  the locally preserved official archive.

Never overwrite an existing evidence item with a later response. Use a new poll
label and register the capture in the Workshop 1 evidence register and change
log.

## Execute the profiling notebook

After `requirements-workshop1.lock` has been generated and reviewed:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/workshop_1/execute_source_profiling_notebook.ps1
```

The script creates or reuses the ignored repository `.venv`, synchronizes the
exact locked dependencies, and executes the notebook in place from the
repository root. A failed assertion or cell stops execution. Stored outputs may
be committed only after manual review against the evidence register.

The verified 2026-11-05 execution used `uv 0.13.7`, CPython `3.12.16`, and the
exact versions in `requirements-workshop1.lock`. The lock can be regenerated
from the direct dependency list with:

```powershell
uv pip compile requirements-workshop1.in -o requirements-workshop1.lock --python-version 3.12
```
