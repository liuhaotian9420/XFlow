---
name: sql-export-agent
description: Execute a single ODPS SQL file, export the result to Excel, optionally persist it to DuckDB, and maintain DataWorks table metadata notes. Use when Codex needs to run an existing `.sql` file in MaxCompute / ODPS, export query results, cache them locally, extract table usage from SQL snippets, or when a known ODPS table name needs its field names, data types, DDL, and sample rows synced into `references/tables.md`.
---

## Watermark

- Every time this skill is used, overwrite `water.json` in this skill directory.
- Use `../_common/scripts/write_watermark.py` to write the file.
- Required JSON shape:
  - `skill`: `sql-export-agent`
  - `version`: watermark version, default `v1`
  - `input_files`: input file names/paths used for this run, or `[]`
  - `actions`: concise completed actions for this run
- Include the executed SQL file, synced table name, or fixture path in `input_files` when available.
- Do this before the final answer for the skill, and overwrite rather than append.

# SQL Export Agent

## Purpose

Own a narrow, repeatable DataWorks workflow:

1. execute one existing ODPS SQL file
2. export the result to Excel
3. optionally cache the same result into DuckDB
4. extract table usage from local SQL snippets
5. sync known ODPS table metadata into [references/tables.md](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/references/tables.md)
6. bootstrap `references/tables.md` from an existing ground-truth markdown file

Do not treat this skill as a generic SQL authoring or multi-job orchestration skill.

## Dependency boundary

- Python runtime with `pyodps`
- `pandas`
- `python-dotenv`
- `duckdb` for local cache mode
- Live ODPS credentials only when calling ODPS directly
- No live credentials are required for the mock metadata sync path

## Directory index

```text
.
├─ SKILL.md
├─ references/
│  ├─ duckdb.md
│  ├─ pythonodps.md
│  ├─ table-metadata.md
│  ├─ tables.md
│  ├─ by_table
│     └─ index.md
│  └─ prompts/
│     └─ table_extraction.md
├─ scripts/
│  ├─ example.env
│  ├─ example.sql
│  ├─ example_command.sh
│  ├─ extract_tables_from_sql_snippets.py
│  ├─ bootstrap_tables_reference.py
│  ├─ run_sql_export.py
│  └─ sync_table_metadata.py
└─ tests/
   ├─ fixtures/
   │  └─ mock_table_metadata.json
   └─ smoke_sync_table_metadata.py
```

## Read these first

- [references/pythonodps.md](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/references/pythonodps.md): ODPS client construction, SQL execution, result retrieval
- [references/table-metadata.md](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/references/table-metadata.md): official PyODPS APIs for schema, DDL, and head rows
- [references/duckdb.md](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/references/duckdb.md): local cache behavior
- [references/tables.md](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/references/tables.md): accumulated table notes that this skill updates

## Inputs

### SQL export path

Required:

- `file_path`: path to one `.sql` file

Optional:

- `save_path`
- `file_name`
- `access-id`
- `access-key`
- `project`
- `endpoint`
- `duckdb-path`
- `duckdb-table`
- `lifecycle`

### SQL snippet extraction path

Required:

- `--input-dir`: directory containing `.sql`, `.txt`, or `.ipynb` snippets

Optional:

- `--output`: target markdown path, default `references/tables.md`
- `--include-ext`

### Known table metadata sync path

Use exactly one of:

- `--table-name <project.table_or_schema.table>`
- `--mock-metadata-json <fixture.json>`

Optional:

- `--tables-md`: markdown file to update, default `references/tables.md`
- `--sample-limit`: head row count, default `5`, max `10`
- `--skip-ddl`
- `--skip-head`
- `--print-only`
- ODPS credentials through args or env when `--table-name` is used

### Ground-truth bootstrap path

Required:

- `--source-md`: an existing markdown file containing trusted table sections

Optional:

- `--target-md`: output markdown path, default `references/tables.md`
- `--replace`: overwrite target instead of merge

### Environment variables supported

- `ODPS_ACCESS_KEY_ID`
- `ODPS_ACCESS_KEY_SECRET`
- `ODPS_PROJECT`
- `ODPS_ENDPOINT`
- `ALIBABA_CLOUD_ACCESS_KEY_ID`
- `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
- `ALIBABA_CLOUD_PROJECT_JINGYING`
- `ALIBABA_CLOUD_REGION_ENDPOINT`

## Outputs and side effects

### SQL export path

- creates one Excel file under `save_path`
- optionally creates or replaces one DuckDB table
- optionally updates `__table_lifecycle`

### SQL snippet extraction path

- creates or overwrites `references/tables.md` with SQL-derived table usage notes

### Known table metadata sync path

- creates or updates one `## <table_name>` section in `references/tables.md`
- writes field names, data types, column comments, optional sample rows, and optional DDL
- preserves other table sections in the same markdown file

### Ground-truth bootstrap path

- creates or updates `references/tables.md` from an existing trusted markdown source
- preserves trusted `原始字段` / `字段加工` sections as the seed layer before live ODPS enrichment

## Failure modes

Report the failing stage explicitly.

- SQL file read failure
- ODPS authentication/config failure
- ODPS execution failure
- result fetch / reader failure
- Excel write failure
- DuckDB connection or write failure
- invalid DuckDB table name
- invalid lifecycle value
- table metadata input failure
- table metadata fetch failure
- tables.md update failure
- ground-truth bootstrap failure

## Decision rules

Use this skill when:

- the task is "run this SQL file in ODPS"
- the task is "export this SQL result to Excel"
- the task is "cache this SQL result in DuckDB"
- the task is "extract which physical tables and fields appear in these SQL snippets"
- the task is "I know the table name, fetch its schema / DDL / sample rows and append them into `tables.md`"
- the task is "seed this skill's `tables.md` from another trusted `tables.md`"

Do not use this skill when:

- the user needs a new SQL script authored from scratch
- the task needs batch scheduling of many SQL files with dependencies
- the task needs writes back into ODPS tables as the primary output
- the task needs advanced DuckDB schema migration or merge logic

## Canonical workflows

### 1. Run one SQL file and export Excel

1. verify `file_path` exists
2. resolve ODPS credentials
3. read SQL exactly as-is
4. execute SQL
5. wait for success
6. fetch rows into pandas
7. stop early on empty result
8. write Excel
9. optionally write DuckDB

### 2. Extract table usage from SQL snippets

1. point `extract_tables_from_sql_snippets.py` at a snippets directory
2. generate `references/tables.md`
3. if physical schema is also needed, run the metadata sync workflow afterward for specific tables

### 3. Sync known table metadata into `tables.md`

1. resolve metadata source: live ODPS or mock JSON
2. collect columns from `table.table_schema`
3. optionally collect DDL from `table.get_ddl(...)`
4. optionally collect sample rows from `table.head(...)`
5. upsert the table section into `references/tables.md`
6. report the updated file path and synchronized table name

Do not silently rewrite unrelated sections in `tables.md`.

### 4. Bootstrap `tables.md` from a trusted source markdown

1. read the source markdown
2. extract the `# tables` content
3. merge or replace into `references/tables.md`
4. preserve existing target content unless `--replace` is explicitly used
5. report source and target paths

## Scripts index

### [scripts/run_sql_export.py](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/scripts/run_sql_export.py)

Canonical ODPS SQL -> pandas -> Excel / DuckDB execution path.

### [scripts/extract_tables_from_sql_snippets.py](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/scripts/extract_tables_from_sql_snippets.py)

Offline SQL parser that extracts source tables, raw fields, and transformed expressions from snippet files.

### [scripts/sync_table_metadata.py](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/scripts/sync_table_metadata.py)

Known-table metadata synchronizer. It fetches field names, data types, comments, optional sample rows, and optional DDL, then upserts the result into `references/tables.md`.

Mock mode exists specifically for local validation and contract testing.

### [scripts/bootstrap_tables_reference.py](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/scripts/bootstrap_tables_reference.py)

Seed `references/tables.md` from an existing trusted markdown source, such as the SQL generator skill's `tables.md`. Use this when table names and raw fields are already known ground truth and should become the baseline for later ODPS metadata sync.

## References index

### [references/pythonodps.md](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/references/pythonodps.md)

Use for SQL execution and result export.

### [references/table-metadata.md](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/references/table-metadata.md)

Use for table metadata sync. This file maps the workflow to official PyODPS APIs:

- `odps.get_table(...)`
- `table.table_schema.columns`
- `table.table_schema.partitions`
- `table.get_ddl(...)`
- `table.head(...)`

### [references/tables.md](C:/Users/haotian.liu/Documents/GitHub/xyf-competition-mvp/.agents/skills/dataworks/references/tables.md)

Target artifact for extracted table notes and synchronized table metadata.

This file can also be bootstrapped from another skill's trusted `tables.md`.

## Minimal runnable paths

### Local smoke path without ODPS credentials

```bash
python .agents/skills/dataworks/scripts/sync_table_metadata.py \
  --mock-metadata-json .agents/skills/dataworks/tests/fixtures/mock_table_metadata.json \
  --tables-md .agents/skills/dataworks/tests/tmp_tables.md
```

Expected success criteria:

- exit code `0`
- target markdown file exists
- markdown contains the target table heading
- markdown contains field names, data types, sample row section, and DDL section

### Live ODPS metadata sync

```bash
python .agents/skills/dataworks/scripts/sync_table_metadata.py \
  --table-name your_project.your_table \
  --tables-md .agents/skills/dataworks/references/tables.md \
  --sample-limit 5
```

Expected success criteria:

- exit code `0`
- `references/tables.md` contains `## your_project.your_table`
- field list reflects `table.table_schema`
- sample row section is present unless `--skip-head`
- DDL section is present unless `--skip-ddl`

### Bootstrap from trusted markdown

```bash
python .agents/skills/dataworks/scripts/bootstrap_tables_reference.py \
  --source-md .agents/skills/sql-generator/references/tables.md \
  --target-md .agents/skills/dataworks/references/tables.md
```

Expected success criteria:

- exit code `0`
- target markdown contains trusted table sections from the source file
- later metadata sync can continue appending DDL and sample rows per table

### Live SQL export

```bash
python .agents/skills/dataworks/scripts/run_sql_export.py path/to/query.sql --save_path ./files
```

## Negative-path checks

At least one of these should be testable:

- metadata sync with neither `--table-name` nor `--mock-metadata-json`
- metadata sync with malformed mock JSON
- metadata sync with `--sample-limit 0`
- bootstrap with missing `--source-md`
- SQL export with missing SQL file
- SQL export with missing credentials
- DuckDB export with unsafe `--duckdb-table`

## Agent checklist

Before execution:

- choose the right workflow: export, snippet extraction, or metadata sync
- verify required inputs are present
- prefer mock mode when only local verification is needed
- keep live ODPS calls explicit

After execution:

- report output artifact path
- report updated table name when `tables.md` changed
- report row count / columns for SQL export when available
- report skipped sections such as DDL or head rows when intentionally disabled
- when bootstrapping, state that source markdown is treated as the trusted seed layer

## Non-goals

This skill does not define:

- SQL linting or SQL generation
- multi-file SQL dependency orchestration
- semantic business interpretation of column meaning beyond what is explicitly fetched
- advanced Excel formatting
- advanced DuckDB merge or CDC behavior
