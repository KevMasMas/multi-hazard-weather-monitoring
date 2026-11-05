# Workshop 1 Architecture Overview

- **Status:** accepted high-level Workshop 1 proposal
- **Implementation:** Workshops 2-4

The professor's reference architecture is adapted to four weather sources while
keeping historical and incremental extraction separate. Boxes describe planned
responsibilities; they do not claim implemented services.

```mermaid
flowchart LR
    subgraph Historical[Historical sources]
        NOAA[NOAA Storm Events\nyearly CSV archives]
        GHCN[GHCN-Daily / NCEI\nstation-date CSV]
    end

    subgraph Incremental[Periodically updated sources]
        Alerts[NWS Alerts\nGeoJSON polling]
        Stations[NWS Station Observations\nGeoJSON polling]
    end

    NOAA --> Raw[Immutable raw landing\nbody + metadata + SHA-256]
    GHCN --> Raw
    Alerts --> Raw
    Stations --> Raw

    Raw --> Adapters[Source adapters\nparse and preserve source fields]
    Adapters --> Validate[Normalize, validate, deduplicate]
    Validate -->|valid| DB[(PostgreSQL/PostGIS\ncanonical + domain tables)]
    Validate -->|invalid| Rejects[(Rejected records\nreason + raw reference)]

    DB --> Match[Temporal/geographic\nevent matching]
    DB --> Analytics[Historical/current views\nand CHI components]
    Match --> Analytics
    Analytics --> Dash[Plotly Dash\nmap, trends, CHI, data health]

    Scheduler[Airflow or justified scheduler] -. triggers .-> Adapters
    State[(Ingestion state\nwatermarks + last success)] <--> Scheduler
    State <--> DB
```

## Workshop boundaries

- **Workshop 1:** validate sources, preserve samples, define contracts, mapping and this architecture.
- **Workshop 2:** implement Docker, raw landing, database, historical adapters, validation and quarantine.
- **Workshop 3:** implement incremental polling, watermarks, retries, scheduling and event matching.
- **Workshop 4:** implement analytical views, historical/current comparison, CHI and dashboard.

The conceptual entity relationships are detailed in
`docs/architecture/workshop-1-er-model.md` and the field mapping is maintained in
`workshop_1/mapping.md`.
