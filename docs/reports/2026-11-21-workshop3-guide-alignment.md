# Workshop 3 guide alignment review — 2026-11-21

The user selected the supplied Workshop 3 handout as authoritative despite its
2026-I cover. Four audited gaps were addressed in a local feature branch:

1. Source-bound NOAA Oklahoma 2021 narrative Silver from the registered CSV:
   1,324 rows, 632 event narratives and 692 episode fallbacks. The checked
   sample has original text, cleaned tokens, length, VADER 3.3.2 lexical score,
   source key/line and native SHA-256. It has no labelled accuracy evaluation.
2. Historical Bronze now verifies a quality profile in its DAG; historical
   Silver mirrors numeric Parquet and adds a narrative publication task. These
   revised DAG paths have not been rerun inside Airflow.
3. Gold enumerates all hash-verified numeric Parquet files in `datalake_silver/`,
   joins checked narrative Silver, and writes `datalake_gold/`. The locally run
   output has 650 governance and 607 storytelling rows from 19,039 canonical
   records; 1,324 text records reconcile independently. The earlier 625-row
   Airflow success belongs to the earlier implementation.
4. Three Workshop 2 checkout hashes were corrected after proving that their
   recorded hashes equal CRLF reconstruction of the current LF bytes. Workshop 3
   notebook and output hashes must reflect the final regenerated files.

The two updated notebooks ran in fresh kernels with eight and six code cells,
respectively, and zero errors. The updated PDF rendered as nine pages and was
visually inspected. Local narrative/folder guard tests passed. Native Windows
Spark fixture tests hit Hadoop/Python worker constraints, while the full revised
local PySpark data run and independent Pandas reconciliation succeeded. Human
approval, commit, push and Moodle submission are not recorded.

Remaining after this scoped work: actual Airflow run of the revised tasks, wider
narrative source coverage if the team authorizes acquisition, and the existing
county/match/CHI/dashboard milestones. Lexical tone is not hazard severity.
