# Workshop 1 diagrams

Current editable Mermaid sources:

- `workshop-1-core.mmd`: canonical records, raw captures, audit/state and grouping; PK/FK shown.
- `workshop-1-domain.mmd`: source domain subtypes and station/county relations; PK/FK shown.
- `workshop-1-pipeline.mmd`: CLI, orchestration, raw landing, validation, quarantine, database and dashboard.

Paste any file into https://mermaid.live/ to inspect/edit it. The report uses
rendered images under `workshop_1/report/assets/`. These are proposed schemas and
services, not reverse-engineered implemented tables.

Render with Mermaid CLI:

```text
mmdc -i docs/architecture/workshop-1-core.mmd -o workshop_1/report/assets/er-core.png
mmdc -i docs/architecture/workshop-1-domain.mmd -o workshop_1/report/assets/er-domain.png
mmdc -i docs/architecture/workshop-1-pipeline.mmd -o workshop_1/report/assets/er-pipeline.png
```

The earlier `.md` diagrams are retained as design history. Use the `.mmd` files
for the current report. Final SQL constraints need implementation review.
