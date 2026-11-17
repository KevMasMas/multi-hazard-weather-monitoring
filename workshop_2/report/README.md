# Technical Architecture and Pipeline Report

`Workshop_2_Report.pdf` is the review/delivery build. Upload this folder to
Overleaf and select `main.tex` (pdfLaTeX), or build locally with:

```bash
tectonic --keep-logs main.tex
```

Compilation creates `main.pdf`; copy that successful build to the delivery name.
Keep `cover.tex`, `results.tex` and `assets/` alongside the main source.
The cover follows the supplied Workshop 1 style with the same two students.
The body follows the Workshop 2 handout's architecture, preprocessing, Docker,
DAGs, results and challenges sections. Tables flow without forced section pages.

`results.tex` and analysis figures are generated offline by
`scripts/workshop_2/build_report_evidence.py` from actual saved receipts/Parquet.
The real Airflow overview was supplied by Kevin; its unchanged hash and evidence
limits are in `workshop_2/evidence/user_screenshot.json`.
The task-state figure is explicitly labelled as an API rendering, not a screenshot.

Mermaid sources are in `docs/architecture/workshop-2-pipeline.mmd` and
`workshop-2-er.mmd`. The report's architecture is a local TikZ diagram, so Overleaf
does not need an external Mermaid renderer or network data access.

The executed slice is 2021-2025, with one GHCN station. The semester 2010-2025
target and statewide station/county work are not presented as complete.
Final personal approval, commit/push and Moodle upload are not inferred.
