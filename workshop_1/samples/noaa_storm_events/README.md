# NOAA Storm Events Sample Evidence

This folder will contain the small, reviewable Workshop 1 evidence for task
W1-K03. It must not contain full yearly archives.

Captured evidence files:

| File | Purpose | Commit policy |
| --- | --- | --- |
| `details_sample.csv` | Deterministic 250-row source subset with all 51 source columns | Commit |
| `sample_query.sql` | Exact deterministic query | Commit |
| `source_metadata.yaml` | Retrieval time, paths, versions, dimensions, and checksum | Commit |

The sample seeds up to 25 rows from each requested event type and fills any
remaining slots chronologically. This prevents the 250-row evidence file from
excluding less frequent hazard families.

The untouched 2024 `.csv.gz` archive is stored below `data/raw/` and is ignored
by Git. The committed sample is a derived subset: values and columns were not
normalized, but PowerShell parsed and re-serialized the selected CSV rows. Its
provenance, dimensions, checksums, tool version, and limitations are recorded
in `source_metadata.yaml`.

If the ignored raw archive is absent, recreate its directory and download the
exact registered NOAA revision first:

```powershell
New-Item -ItemType Directory -Force -Path data/raw/noaa_storm_events/details/year=2024
Invoke-WebRequest `
  -Uri "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_d2024_c20260728.csv.gz" `
  -OutFile "data/raw/noaa_storm_events/details/year=2024/StormEvents_details-ftp_v1.0_d2024_c20260728.csv.gz"
```

Verify that the raw SHA-256 matches `source_metadata.yaml`; stop if it does not.
Then reproduce the subset with:

```powershell
pwsh -File scripts/workshop_1/extract_noaa_storm_events_sample.ps1
```

This is enough to begin the required profile. It does not complete W1-K03 until
`notebooks/01_source_profiling.ipynb` records the full profiling dimensions and
Pablo reviews the evidence.

The proposed Oklahoma filter is for evidence collection and feasibility testing;
it is not the final region decision. That decision requires coverage evidence
from NOAA Storm Events, GHCN-Daily, NWS Alerts, and NWS station observations and
approval by both team members.

