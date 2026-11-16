# Workshop 1 clean reproduction

Verified on 2026-11-16 with CPython 3.12.16, a fresh local Git clone and a new
virtual environment without system packages. All 59 pinned packages matched;
`pip check` passed; the explicitly selected clean kernel executed all 32 code
cells with zero errors. See `clean_environment_verification.json` for the exact
tested source revision and hashes. Dependency installation needs package-index
access; notebook/audit execution uses saved local samples only.

The first clone exposed old NOAA sample line-ending normalization in Git. Commit
`cce9ade` stores the registered original CRLF bytes. Do not edit samples or change
expected hashes to work around a checksum failure.

## Windows PowerShell procedure

Start from a fresh clone and CPython 3.12 available as `python` (or use its full
executable path). These commands install an explicit environment-local kernel;
they do not rely on a globally registered Jupyter kernel.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-workshop1.lock
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m ipykernel install --prefix .venv --name weather-w1
$env:JUPYTER_PATH = (Resolve-Path .venv/share/jupyter).Path
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=weather-w1 --ExecutePreprocessor.timeout=300 notebooks/01_source_profiling.ipynb
.\.venv\Scripts\python.exe scripts/workshop_1/build_historical_event_pairs.py
.\.venv\Scripts\python.exe scripts/workshop_1/compare_daily_sources.py
.\.venv\Scripts\python.exe scripts/workshop_1/audit_submission_evidence.py
.\.venv\Scripts\python.exe scripts/workshop_1/review_artifacts.py
```

Do not use `--fetch`: the saved evidence suffices. `--extract` is only for
reconstructing the small NOAA wind subset from the ignored original bulk archive;
normal clones use the committed subset and do not need that archive.

The tested run isolated Jupyter config/IPython directories as well. Kernel and
virtual-environment paths in the JSON receipt are local test paths, not portable
project configuration. On another machine create its own environment.
