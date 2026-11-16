# Workshop 1 submission

Moodle requests these four items:

| Item | File |
| --- | --- |
| Project Definition Report (PDF) | [`report/Workshop_1_Report.pdf`](report/Workshop_1_Report.pdf); LaTeX source in `report/`. First version for review. |
| Source Profile Notebook | `../notebooks/01_source_profiling.ipynb` |
| Canonical Mapping Table | `mapping.md` |
| GitHub link | https://github.com/KevMasMas/multi-hazard-weather-monitoring/tree/workflow-1 |

The supplied Moodle notice gives 16 November 2026, 12:00–15:15 America/Bogota as
the submission window. No upload is recorded here.

`samples/` holds source evidence. Plans, report draft and work history are in
`../deliveries/01-workshop-1/`. Bulk data is kept outside Git.

One authorized GHCN overlap capture now supports eight TMAX/TMIN candidate
records over four days. Coverage, QC and daily-boundary assumptions are recorded
in `samples/candidate_pairs/`; the retained intra-NWS examples do not count.
The primary overlap evidence is now five Storm Events/GHCN wind-record candidate
pairs (`samples/candidate_pairs/historical_wind_candidate_pairs.csv`): five Storm
IDs, three original GHCN daily records, explicit airport narratives. These are
technically defensible candidates with all differences/limitations disclosed,
not five independent episodes or confirmed exact gusts. The eight temperature
rows are supplemental. Q1-Q5 are primary quality concerns and Q6-Q7 additional.
The notebook passed a fresh isolated 59-package locked environment: 32 cells,
zero errors. Current artifact audit passed within its recorded scope.
See `../docs/reports/workshop-1-compliance-review.md` and acceptance criteria
A01-A09 in the Workshop 1 implementation plan. No new team approval is implied.
Deliver the reviewed commit on `workflow-1` and record its hash after committing.
No final tag is claimed; `v1.0-final` belongs to the semester's final project.
