# Workshop 2 evidence register

Current executed slice: 2021-2025; Oklahoma Storm Events and one GHCN station.
Personal approval, selected commit, push and platform upload are not inferred.

## Documentation revision

Current PDF: 12 pages, including Appendix A with literal layer excerpts. The current documentation audit is `evidence/report_revision_audit.json`. Earlier nine-page PDF/package audits remain preserved historical records; pipeline samples, notebook and run results are unchanged. Git remote `workflow-2` was checked: 5810ba5 is pushed; this new documentation revision is local and requires another commit/push.

## Evidence boundaries

- `historical_acquisition.json`: original NOAA gzip/NCEI CSV responses, request URLs, UTC captures, native/input SHA-256 and subset derivation.
- `historical_airflow_runs.json`: ten actual successful source/year DAG pairs, real tasks and output metrics.
- `delivery_database.json`: 19,039 canonical rows, zero duplicate keys and five-year/date coverage.
- `after_restart_database.json`, `persistence_verification.json`, `replay_airflow_runs.json`: persisted state and three successful unchanged replays.
- `wsl_test_results.json`: current 29-test receipt and tested-file hashes; synthetic integration fixtures remain separate from weather evidence.
- `notebook_execution.json`: fresh kernel in the existing Python environment, not a newly installed isolated environment.
- `user_screenshot.json`: contributor-supplied unchanged UI overview; earlier failures remain visible.
- `package_verification.json` / `final_artifact_audit.json`: actual ZIP/hash/receipt/W1-preservation checks.
- Earlier `airflow_verification.json` / `database_verification.json` are historical bounded-pilot receipts, not the current five-year totals.

Full original archives/bulk outputs stay in ignored storage. Three reviewable registered CSV inputs, original DAG JSON/Parquet and lineage manifests are packaged. The NOAA CSV is a documented subset, not an original nationwide response.

## Artifact and receipt hashes

| Repository path | SHA-256 |
| --- | --- |
| `workshop_2/report/Workshop_2_Report.pdf` | `4C15B1D5769DEB06CFAC704E4CFFE4E3D15CB4D72955F70BBDA6D81897A7CC2B` |
| `workshop_2/Workshop_2_Pipeline_Output_Samples.zip` | `1A7CB0BCC62D484E4DC019D276539A897ED286BE5434AE7597768DC291C33171` |
| `notebooks/02_historical_ingestion_review.ipynb` | `4FFD7E5B6D5E9856B58FF1299CB4640354C56301B52E828111F6300C1B98FE41` |
| `workshop_2/samples/manifest.json` | `D2AEE0B5420BA9C12E6B21EB842D945ABB6BEA6D1064CFA7AE373F28CF3BDBDF` |
| `workshop_2/report/main.tex` | `E7031B9255210AC666A7A31BAC5A1C327E2AB36E59DB5861E16AA31F90A8D90C` |
| `workshop_2/evidence/after_restart_database.json` | `C012C6C40789A114516951A23A2723A94D974981CD14197F1E91EDA0C9986B16` |
| `workshop_2/evidence/airflow_verification.json` | `9A09B99AE62092DEFB6150B7898773334028FF6D69254EBAEF32CDA8C7560E78` |
| `workshop_2/evidence/compose_ps.json` | `384F7246A0E05795798F3F8CDE0D05338B09C0FA77AFA4ACCF5DF64F9E6D8FA4` |
| `workshop_2/evidence/database_verification.json` | `467270BBC2B7F051A4D04AE80F854E4670902CB32AF16F45250E1E3E2A0E6C04` |
| `workshop_2/evidence/delivery_database.json` | `DA74EE8F5BEAA2FD9504F0A5B6B6596A6A56C698AE45D026745D64CF8D979A07` |
| `workshop_2/evidence/final_artifact_audit.json` | `657D89638FED6DB8BC80E5F51D49BF8BFAE45FAA22FCCF53F462A1C1426C3D5A` |
| `workshop_2/evidence/historical_acquisition.json` | `C8D7A3F96E8BE8F98CCD521BBA94B7227126DAECB52BA7D67C571D865EEEDD1F` |
| `workshop_2/evidence/historical_airflow_runs.json` | `18C17F1EBFDA7751BECBC1B77A9FABAD84D1435A02373565B08A40B33CCF1EEF` |
| `workshop_2/evidence/isolated_notebook_execution.json` | `1CB0554B5F7B33F3F5412D6AB321416807E6D10060AB99D856BAF1817B8F37A5` |
| `workshop_2/evidence/notebook_execution.json` | `6BA656B06DB6A048891D1F09167454496FC4549FEDD5B5E1FA71ED3DC316E642` |
| `workshop_2/evidence/package_verification.json` | `42CF88A4F2184B9252D5E46BC202D3B20C5132DAFC6AA185FBDE7D5E13A75168` |
| `workshop_2/evidence/persistence_verification.json` | `0541846C6294CB3873C72FD39F7349676617BDF11842001C788AC9E6BC3B18A1` |
| `workshop_2/evidence/replay_airflow_runs.json` | `AAC1786620550AAFE19DF27924D923E474422581CBFFB997F7A6EFFAD9412405` |
| `workshop_2/evidence/report_analysis.json` | `1BCE50B39D93A3CE07A62407ED972CCC60E09420A5E39D5051BF9A5D12F6E769` |
| `workshop_2/evidence/user_screenshot.json` | `7E3C2B2F6F47A7ABF5D109CDDC29C305EEF31213AB2B95C7DEAFB8B9F7631F77` |
| `workshop_2/evidence/wsl_test_results.json` | `767B63530FF65514623CD980D3EB01EF81751CABC1F7DAA7FCAC64142AAF9FDA` |
| `workshop_2/report/layer_appendix.tex` | `85CE21031CCAAD0244BD486870642B36AF0EEE956A11086FFC9322AB6449BF93` |
| `workshop_2/report/assets/bronze_excerpt.json` | `CC3501B2835E602372605A2980AE992E254FB5A90359C0E100A21A214BAE4702` |
| `workshop_2/report/assets/silver_head.txt` | `64D9CF8AC3156AFE45B0C9879E4B57104F16239E11CF9F174004DF906B3CBFC4` |
| `workshop_2/report/assets/silver_info.txt` | `42D3E4343493443B6D09C855C7576A54EF346821C0170072F686B23A3AA3D8C1` |
| `workshop_2/evidence/layer_excerpt_provenance.json` | `A46B98C64B365E18B6B9AF89B41A5278C17B9953F6B333E063826F0AA4262D28` |
| `workshop_2/evidence/report_revision_audit.json` | `650CB04B92390FE8C94EB70BFC7DFE086913306190C460F7E7C8954B9EE45376` |

## Sample hashes

Full per-file hashes and sizes: `samples/manifest.json`. ZIP members are independently indexed by `PACKAGE_MANIFEST.json` inside the archive.

## Open items

Remaining semester years (2010-2020), broader station inventory and reviewed county assignments remain open. Professor clarification of the conflicting source-domain wording is unrecorded. Kevin and Pablo must review and select the submission commit, then perform push/upload.
