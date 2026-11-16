# Course material review - 16 November 2026

Official course commit checked: `3f7010d`, 2026-11-16.

The updated `r_intro.ipynb` includes `str()`, `summary()`, a histogram, a boxplot
and regression examples. The notebook's boxplot currently plots `Humidity3pm`
while its labels refer to maximum temperature; our plots use labels matching the
actual variables instead of copying that mismatch.

Source: https://github.com/EngAndres/ud-public/blob/3f7010d/courses/data-analysis-programming/notebooks/r_intro.ipynb

For Workshop 1, a TMAX histogram and separate temperature/precipitation boxplots
help inspect ranges and possible unusual values in the GHCN sample. Values beyond
the whiskers are retained; extreme weather is relevant evidence, not an automatic
reason for removal.

Regression/model training and the updated Airflow analysis/curation DAGs are
references for later workshops. No model or pipeline was added to Workshop 1.

The Moodle notice supplied by the team requests a PDF report, notebook, mapping
table and GitHub link. Its stated window is 16 November 2026, 12:00–15:15 Bogotá.
The authenticated Moodle resource was not independently retrieved; this review
uses the notice copied into the chat.
