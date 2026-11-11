# Workshop 1 Final Review

## Verification on 2026-11-11

The current source-profile notebook was executed with the existing project virtual
environment using:

```powershell
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 notebooks\01_source_profiling.ipynb
```

Execution completed successfully. All 29 code cells executed and no notebook error
outputs were stored. This verifies the current notebook against preserved local
evidence. No live weather request was made. Dependency synchronization against
the lock was not performed because `uv` was unavailable; a fresh-clone environment
reproduction remains a separate check.

## Remaining submission gates

- Final technical review of mapping, quality examples and source contracts.
- English PDF generation and visual inspection, including rendered diagrams.
- Fresh-clone reproduction and final artifact/secret review.
- Student review and submission commit/reference recording.

Assistant verification must not be presented as personal approval by either
student. Candidate pairs remain unconfirmed and historical volume screens remain
estimates.
