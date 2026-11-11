# Workshops 2-4 Specification Review

- **Review date:** 2026-11-10
- **Professor repository commit checked:** `5a6ec8d` (`Update classes`, 2026-11-05)
- **Project:** Team 9 - Multi-Hazard Weather Impact Monitoring
- **Status:** reviewed; specification conflict requires professor clarification

## Reviewed files

| File | Pages | SHA-256 | Stated semester and topic |
| --- | ---: | --- | --- |
| `Workshop_2.pdf` | 7 | `48012A30DF3709607717929B5CA0F2C94694B76BAF8669E4321AF9283132AE77` | 2026-I; Public Opinion and Sentiment Analysis; Bronze/Silver pipeline |
| `Workshop_3.pdf` | 7 | `9D5A0447E60B93D1DE66479DA8F0D54100D58A9EF8870F43BC28C6CE1CD3BEF2` | 2026-I; Silver-to-Gold, governance KPIs and storytelling |
| `Workshop_4.pdf` | 7 | `BD03749B03A49846A66E99279B7E742311B577B177DF585DDD376702F010F0A5` | 2026-I; two Plotly Dash applications backed by Gold Parquet |

The PDFs were downloaded from the official professor repository and reviewed
page by page, including title, deliverable and submission pages.

## Authoritative conflict

The 2026-II `CourseProject.pdf`, `TeamsDistribution.pdf`, and `Workshop_1.pdf`
define Team 9 as a four-source natural-hazard system. Their milestone sequence is:

1. Workshop 2: Docker architecture, relational schema and historical ingestion.
2. Workshop 3: incremental ingestion, watermarks, deduplication and event identification.
3. Workshop 4: temporal/geographic analytics, historical/current comparison, Compound Hazard Index and monitoring dashboard.

The newly published Workshop 2-4 PDFs instead describe a different 2026-I
project with one API, one web-scraping source, NLP preprocessing, sentiment,
Bronze/Silver/Gold Parquet layers, PySpark and two dashboards. They do not mention
the natural-hazard canonical model, NOAA/NWS sources or the Compound Hazard Index.

| Topic | 2026-II natural-hazard contract | New Workshop 2-4 PDFs | Planning treatment |
| --- | --- | --- | --- |
| Domain | Natural hazards and source/event integration | Public opinion and sentiment | 2026-II domain wins. |
| Sources | Two historical plus two periodically updated sources | One API plus one scraper | Team 9 keeps NOAA, GHCN and NWS sources. |
| Workshop 2 | Historical ingestion into relational canonical model | Bronze JSON and Silver Parquet for both sources | Implement the historical/database core; keep compatible Airflow/Parquet items conditional. |
| Workshop 3 | Incremental ingestion and event identification | PySpark Gold and NLP summaries | Implement incremental/event integration first; Gold/PySpark is conditional. |
| Workshop 4 | CHI, historical/current analysis and monitoring dashboard | Governance and sentiment dashboards | Implement Team 9 analytics and database-backed monitoring; a second app is conditional. |
| Dashboard source | Database or analytical views | Gold Parquet only | Do not select one until the professor resolves the conflict. |
| Scheduler | Airflow or equivalent documented scheduler | Airflow TaskFlow and FileSensor required | Airflow is the safest provisional choice, but the final decision remains an ADR. |

## Planning decision

Professor-issued 2026-II project documents remain the primary requirements for
Team 9. The new PDFs are used only for compatible engineering expectations such
as Docker reproducibility, Airflow task structure, persisted raw evidence,
Parquet exploration, data-quality reporting, dashboard quality and English PDF
documentation. Incompatible NLP/sentiment/scraping claims are not converted into
Team 9 requirements without written clarification.

Implementation plans therefore distinguish:

- **P0 compatibility core:** required by the 2026-II project and safe to start.
- **Conditional scope:** present only in the mismatched 2026-I PDFs.
- **Out of scope:** work that belongs to another workshop or contradicts Team 9.

## Questions for the professor

1. Are `Workshop_2.pdf`, `Workshop_3.pdf`, and `Workshop_4.pdf` intended for the
   2026-II natural-hazard projects despite their 2026-I public-opinion wording?
2. Must Team 9 implement Bronze/Silver/Gold Parquet in addition to the required
   relational canonical database?
3. Is Apache Airflow mandatory, or does the 2026-II “Airflow or equivalent” rule
   remain authoritative?
4. Is PySpark mandatory for Workshop 3 even though the 2026-II milestone assigns
   incremental ingestion and event identification to that workshop?
5. Must Team 9 build two independent dashboards, or one monitoring dashboard
   with analytical and data-health views?
6. Should dashboards read Gold Parquet exclusively, or the database/analytical
   views required by the 2026-II course project?

## Safe work that can begin before clarification

- Close Workshop 1 review/PDF gates and freeze accepted contracts.
- Design Docker Compose with PostgreSQL/PostGIS and an ingestion service.
- Select Airflow provisionally because it satisfies both document families.
- Define raw-capture, canonical, quarantine and ingestion-state schemas.
- Implement/test NOAA and GHCN historical adapters behind stable interfaces.
- Keep storage boundaries flexible so optional Parquet layers can be added
  without replacing the relational source of truth.
- Design NWS incremental adapters and dashboard views without claiming them
  implemented before their workshops.

No new weather API request, pipeline execution or implementation result was
produced during this specification review.
