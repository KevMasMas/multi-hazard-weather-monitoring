# Architecture diagrams

## Workshop 2 - implemented historical slice

- `workshop-2-pipeline.mmd`: acquisition, persistent raw/Bronze, exact-file sensor,
  quarantine, canonical database, revision-based Parquet and planned consumers.
- `workshop-2-er.mmd`: actual migrated entities and key fields. Unique source keys
  are composite with source ID; consult SQL for the complete constraint groups.
  Region/assignment structures are present but empty, pending reviewed geography.

Paste into <https://mermaid.live/> to edit. The Workshop 2 PDF uses a portable
TikZ architecture figure and key-field table; these Mermaid files provide editable
source counterparts. They do not imply completed Gold/CHI/dashboard work.

## Workshop 1 - preserved conceptual design

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
