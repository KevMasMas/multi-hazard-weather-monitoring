# Workshop 3 evidence register

Current scope: verified historical quality/Gold, incremental replay/state/recovery, announced bounded live validation and an eight-page review PDF. No W3 personal approval or platform submission is inferred.

## Read first

- `evidence/final_artifact_audit.json`: 49 passing tests across three suites, preserved prior artifacts, current source fingerprints, offline restoration, PDF and review-file scan.
- `evidence/gold_airflow_run.json`, `gold_reconciliation.json`, `gold_retry_verification.json`: actual successful Gold run, independent aggregates and unchanged batch retry.
- `evidence/incremental_replay.json`: original first/unchanged second saved passes; partial KOKC coverage is explicit.
- `evidence/incremental_live.json`: announced real query URLs, UTC times, page hashes and zero/903 source counts; raw original bytes remain ignored.
- `evidence/nws_window_review.json`: 902 observations within the requested interval, one before its start, none after its end. All returned records are preserved; analytics must filter timestamps.
- `evidence/incremental_airflow_run.json`: three actual successful replay tasks, DAG paused afterward.
- `evidence/incremental_restart.json` and `incremental_database_audit.json`: persisted hashes across DB restart, 19,039 preserved historical records and 19,942 unique operational rows.
- `evidence/incremental_disabled_schedule.json` and Gold permission-failure receipts: earlier failures retained with corrections, not silently removed.
- `evidence/report_qa.json`: compiled PDF, eight pages, rendered/visually inspected, no overfull TeX boxes.
- The Silver reproduction ZIP restores all 13 frozen inputs offline. Notebook execution used fresh kernels in the existing environment, not a newly installed dependency environment.

Five saved-data candidate associations are intra-NWS and unconfirmed. Five W1 NOAA/GHCN wind rows are reused historical context, not new W3 matches. Live validation produced zero candidates. County allocation, labelled match evaluation and professor clarification remain open.

## SHA-256

| Repository path | SHA-256 |
| --- | --- |
| `airflow/dags/gold_processing_dag.py` | `94D423CDFB60F134E6B4D2497AEC6873A160D29428F520C2C1F92FCC4BEE2AAF` |
| `airflow/dags/incremental_ingestion_dag.py` | `4034B16BE0B5AB306970E231A11BE9CDF5E641EE0F678153EDB5080E1021B53C` |
| `airflow/dags/silver_processing_dag.py` | `532C0D0E68C9AD54B364EFEDA8AE59242931231CDC6DC76EE80A1E86ABCC72A9` |
| `config/workshop3_gold.json` | `00F70BC0FDA4B10C439B2F3C73374277A72C1E7250160D369DA3A2FC572E4685` |
| `config/workshop3_incremental.json` | `63AF45AF08CF9E876E544BF1E202D5CFB11013468B327C9946A2FFF8E8BCDE0C` |
| `config/workshop3_nws_replay.json` | `00219F0DA7791764CF3AD5D18F159D6498DCD5A23437034CF1396641BE03D4DC` |
| `deliveries/03-workshop-3/SUBMISSION_MANIFEST.json` | `7CAA631ED2BED247735EE185883052F088AB047F193C564F1FE0D419B05859D7` |
| `ingest.py` | `B30B7624984781561830E93CF33F07D783C4FEDDFA13335B9FFD950760AB6EA0` |
| `notebooks/03_silver_quality_review.ipynb` | `FF631F091E38AF1C5043B899E70876E4D8A68E14E4D5F22E29320351342A7BB7` |
| `notebooks/04_gold_review.ipynb` | `A7067C216C1FABB9C11A94F217FE02E93681497B56B2D86C1C1B30DFB00B41AD` |
| `scripts/workshop_3/audit_gold_delivery.py` | `C9CC09D07BB09093C2E79BCFD6E7ABE4C76C81F52DB0AB5F0CE5B107571E7716` |
| `scripts/workshop_3/audit_live_window.py` | `A5BF768F8691BA5B453F9395A375F6BA840B593FF1408E92688CCB6F88D3AD90` |
| `scripts/workshop_3/cache_spark_package.py` | `258598D36BA7BDB20B310C3855FFF99090556D2BDD70984E957F67E581ED8323` |
| `scripts/workshop_3/check_report.py` | `A1F5E0A4B018B3E6053B1A00EC91AC5881CBA2352114913AA1C212796F443F92` |
| `scripts/workshop_3/create_gold_notebook.py` | `886DCF840034CF6C7D8195725CA5E03FAF0DE6DFBB7675B23C33955B6AF10840` |
| `scripts/workshop_3/create_quality_notebook.py` | `96CFE50F9F979A0C4D316414387225C5AD7C5EDBF17835AFE2DF6CB7FC7458B5` |
| `scripts/workshop_3/create_report_assets.py` | `95F5690E64B604D13AB240782890D710762FC2FFE33AA704C5B728B551CF0236` |
| `scripts/workshop_3/prepare_gold_samples.py` | `1137ECD8E44E32134C8377497065794492FB0AB33614DE25197274C0BB36A19A` |
| `scripts/workshop_3/record_runtime.py` | `4E68187CD1D346992BBE68E8F2383CFF13D499A01D3E90CE018F7F311561A8DE` |
| `scripts/workshop_3/restore_silver.py` | `DA23675FE05DEBED158EA0299EFA09C6BF39EA0B395F2C09005E123FC8EC51C6` |
| `scripts/workshop_3/run_gold.py` | `E7624A1414210E2DA8155DAC42904C47F05207530A43E3A3B240AA54A01672A3` |
| `scripts/workshop_3/run_tests.py` | `6DE905F48141260AD451C4E42257774F4F40D8ADD170D4581EE8D8676345EC95` |
| `scripts/workshop_3/seal_delivery.py` | `B1BACF66E27EA05E1A25154DF06C25DFE341969B05139DEC374E1ED76A3CC197` |
| `scripts/workshop_3/verify_airflow_gold.py` | `420D1F00803CFFF9C6F4282FEF8E5B427938B934C2ACC9EA92231C3B2E19291E` |
| `scripts/workshop_3/verify_cli.py` | `4E7203B49567BF8F2B882AC1F17B76DAB3A2A3A59210DB9D847E279A5E28A586` |
| `scripts/workshop_3/verify_gold.py` | `2F12BF40F357097180723240A897BD1C1B95549FFCB2D1A6D22E45204A7AE4FA` |
| `scripts/workshop_3/verify_incremental.py` | `84AF521BED9F701CB2321F22151FD78FEEE043F971C59568D62B29898E3F0B5A` |
| `scripts/workshop_3/verify_incremental_airflow.py` | `86A455B9393813CF8DAA48DA74985FEF47314FEBEE45543ADE0CDD92184C10DF` |
| `scripts/workshop_3/verify_live.py` | `6A8E728C873C273AEEA07A87EA8270E91DDD1ECC932CE6BA87F17BEF5A9D7E14` |
| `scripts/workshop_3/verify_restart.py` | `BE6640908E4A5E209C3340BEED499DC8116720A1EB6EE6C91AC4806A65F06C1E` |
| `sql/005_incremental_ingestion.sql` | `111B7C21834325BBFBE0F6A0209F0C8EC91A957C5C1A2EE2520965D048669DE7` |
| `src/multi_hazard_weather_monitoring/event_candidates.py` | `017862A5D2AEEBB136D9066F72D82430D1566A733C141B6A039790CE7710957C` |
| `src/multi_hazard_weather_monitoring/gold.py` | `0FB577A674B3AC30F4DBB0F72EAF0B1A8A826DB7C0CE2ED6F3F6273B290C424E` |
| `src/multi_hazard_weather_monitoring/incremental.py` | `36AA9F527E2CC05220A043A890D157B286B268667A7B1AB7F837E359B4D2A6B6` |
| `tests/test_incremental.py` | `A3877F852A166CDA8CB4A6CB6DA92C9471DB280FBE6FD50FD8A23F7C00CE81A8` |
| `workshop_3/architecture.mmd` | `7F36A302A6A7892CA2E9F505FCB8A609F71EE982BAA63B9A6C68F0F0C60AC291` |
| `workshop_3/evidence/distribution_review.csv` | `A7FF53473A8758F225D5D27B44B134ED5E4FF50F035214D53D821F339B24FED9` |
| `workshop_3/evidence/final_artifact_audit.json` | `C585138D235B966A88775EC9F7AFE380050B769D2E508986E5D26BE740F711B3` |
| `workshop_3/evidence/gold_airflow_failed_permissions.json` | `89D443F52368B0B0502B82355BAD40C407F94E257C4D40C4D8B23700222B62C1` |
| `workshop_3/evidence/gold_airflow_run.json` | `3224F09F2F281B1348A626A82670DBCE9DAFBCA54EAF51E6B0D8AB60F27898F9` |
| `workshop_3/evidence/gold_artifact_audit.json` | `86E6765CE38B302452F7BB7ADD481FF0361572A94568C33E4338CCF2DF9A2D22` |
| `workshop_3/evidence/gold_notebook_execution.json` | `5BA843026AD7C9D1BA36034487A2BAB9E43219EDEF8C599E3B51A3A6B0DF3B81` |
| `workshop_3/evidence/gold_permission_error.json` | `1390E4EE05E81865C9302AB727FCC0A5447F922D400E1F4402760A14C3BAE637` |
| `workshop_3/evidence/gold_reconciliation.json` | `84E0CB0550F63A64823E693882601B4D7C1137E6B64ED274B9B41E2D945CBD2B` |
| `workshop_3/evidence/gold_retry_verification.json` | `1D5262E2A51C211220265DCFFE048DCCC54D6DF55AA0497183D25135E83B71EE` |
| `workshop_3/evidence/gold_samples.json` | `B470E8506D68141E077DC6B66853A847243912A8B6BE2489E4F5B1A4AAC7DCC6` |
| `workshop_3/evidence/incremental_airflow_run.json` | `5DFB404D6FA5930FE22B7437063DC533E84903D48159CADE0975204ADC7219B8` |
| `workshop_3/evidence/incremental_database_audit.json` | `EDB934113E6525D8CA8F0A468577876E264A20878384F72E9DFCE0133F1395FA` |
| `workshop_3/evidence/incremental_disabled_schedule.json` | `A5FA71FFED67D55E310721C0FB9AE0BF2C9465D0601F6AB5741A93955EF42896` |
| `workshop_3/evidence/incremental_live.json` | `086F78B5533EF3D07689D559C7E5CA288CAA91C61DE71A98CA26591320221AB2` |
| `workshop_3/evidence/incremental_replay.json` | `FBDE7A133BC43DCE26BA27140897F204AAD0B8B6BA825B4D7507E6CB021C87CE` |
| `workshop_3/evidence/incremental_restart.json` | `4C1F773162647BCD68A82150E9F01B5CB32A1A190D2991DD2FC4561CF354A10B` |
| `workshop_3/evidence/incremental_tests.json` | `F1EC916D065579777DCB6B39EFF2386229FBEE2D0BF63BF63FF9A124DD209413` |
| `workshop_3/evidence/notebook_execution.json` | `55C61B98F55E5FF1B93007C8FB2571F326DD40E0DC6C776B4D0F272AF1E99969` |
| `workshop_3/evidence/nws_window_review.json` | `19046F010F5D70937026115803D730D1C302C98F8C777F1AA12E0ECB0E856A4C` |
| `workshop_3/evidence/quality_artifact_hashes.json` | `E8F4C99D54B082A7318FB7216CC963AAA8E987005884A5E7638C48EFBBCA8098` |
| `workshop_3/evidence/report_qa.json` | `30BCAF4EB82AD1C99A1D857141750986BCAC3BCF55DBB246D6884B7682D6423E` |
| `workshop_3/evidence/runtime.json` | `CA36D62540F3F278A52E2E88C80657C26F333A1F819E2F5B1D5593EF8CDE3EA3` |
| `workshop_3/evidence/seasonal_review.csv` | `E270E6C83C7F8CF6E72D9F433B0B1C7493229F7A8555C3001481386AC0452861` |
| `workshop_3/evidence/silver_review.json` | `CAAEAFFA6F3C7C656B7C91487DED77A5FA569FECC0A46C9E259B9FFB91C14C25` |
| `workshop_3/evidence/snapshot_inventory.csv` | `6B81F21FDD37FE252714767771F0545AE74A5372EC1C2FE954EA6FE32AA4E9EE` |
| `workshop_3/evidence/source_missingness.csv` | `9BAF6C46340CBE87394DD65A7285C3643B345C717E1258A47821F507AA9A4EA0` |
| `workshop_3/evidence/spark_tests.json` | `012B2FA728C6113BDBB980FC7C1FF7299D72F6774EF6212355983BC3EC77607D` |
| `workshop_3/evidence/workshop2_regression.json` | `4C04596BCAECC77F7C6A5BBE0B2CC0CDD57B83603A87CAEE5AA3EEDAE8719DD0` |
| `workshop_3/GOLD_CONTRACT.md` | `BF5C9DA9A1E7C08A997D2834CBD7A8F67FBAC7CB89F80F1E764C73EFCFF48508` |
| `workshop_3/INCREMENTAL_CONTRACT.md` | `CF0784983DA57D991D3F156331031D5D9DA233CC0285F5AD4304CC687E8DB2D4` |
| `workshop_3/report/assets/Escudo.png` | `E0F1F6EDA8029C428E69579B72DBAD04FF8A7CE56912429363B50A059AD7AB1E` |
| `workshop_3/report/assets/governance_preview.png` | `438676F32A03E71E77348B08CB757A0FD04DAE99CFF6005D8348E44561B87ABC` |
| `workshop_3/report/assets/quality_1.png` | `D94F61675BA20FE0E20B248B6D80A847162F16E53825C970B81F4CE44AB2B201` |
| `workshop_3/report/assets/quality_2.png` | `0D12415F93823C7269E38F730724138F8F82DE4BCE54EC0C6A944C77650FDC55` |
| `workshop_3/report/assets/storytelling_preview.png` | `4B9BBC364B4F7E1D8F90C593276570434E64B4D74FA1AF6E5D7FE50E9B4FAED6` |
| `workshop_3/report/cover.tex` | `15673FD327BDA2CAA50FE7D077DC697D41A646E22851F4CF47A2857F49D50DED` |
| `workshop_3/report/main.tex` | `9E05E45A1BF85534EEF74F412DE26B5E9E04CD134C102FEB5AD11F99C44A8476` |
| `workshop_3/samples/gold/governance_20261121_144319_caeba6938516.parquet` | `C21E050DB77E0F941B99F028740FEDF96FD5C38DF2262AF55F5817190705F4F8` |
| `workshop_3/samples/gold/governance_preview.csv` | `1B606E431B36E169C389F990AADE53FF16F3A584C697EE83050ED8CF63F1C07B` |
| `workshop_3/samples/gold/manifest.json` | `A413FAB0E5CDA49CBD6B814915261D830CDE2D886C25F0D4379B2CA072ADAE3C` |
| `workshop_3/samples/gold/README.md` | `22153A72EE31959C4BE34D146165FE6E22C9B4BD6F302B95CC17CD3EF90DC3F0` |
| `workshop_3/samples/gold/storytelling_20261121_144319_caeba6938516.parquet` | `63C1FA56AD8919F4B2361F5588A43D85614E39763D34C9523A4369BE40A35097` |
| `workshop_3/samples/gold/storytelling_preview.csv` | `7CC062606E5152DDD3A1EA781990F5CD7AC815F1D818D6E4FB171D260FE7B226` |
| `workshop_3/samples/incremental/live_nws_candidates.json` | `37517E5F3DC66819F61F5A7BB8ACE1921282415F10551D2DEFA5C3EB0985B570` |
| `workshop_3/samples/incremental/normalized_preview.json` | `2D6E98952162A25743F99B7846B9F158DB18FD80099D446B6161CAE3C4B1C914` |
| `workshop_3/samples/incremental/nws_alerts_live_excerpt.json` | `EDFBD2AE8361B8590F58B8AE3C08E6E465AF9184466C468FAF64FF6B692CCD08` |
| `workshop_3/samples/incremental/nws_candidates.json` | `3849C005C11919C6DAF0842829E2A24D86806DCBDB22904257989AB5265BE9F8` |
| `workshop_3/samples/incremental/nws_station_observations_live_excerpt.json` | `EDBABE8C50B85CF259A7BD657DB9C6A96A4383EA788DC1363CD3B4C401037A4A` |
| `workshop_3/samples/incremental/README.md` | `F9268A7261A9F73D22B540D2E51AAC841713806AF0413983084FF947A290869A` |
| `workshop_3/Workshop_3_Pipeline_Improvements_and_Gold_Layer_Report.pdf` | `0728EF7BA195E302DF765694521E20E3806D057CF1DAA9E23ECE3D59FA19CDFA` |
| `workshop_3/Workshop_3_Pipeline_Output_Samples.zip` | `74813503B8F210EEECCF656F14279888C5DBBB9FF551113D6FEFEA88F8A26DE9` |
| `workshop_3/Workshop_3_Silver_Reproduction_Inputs.zip` | `B01835F142E7A85F8387421AFBC44CA853C65E8D908E8355523F5C708DCC905F` |
