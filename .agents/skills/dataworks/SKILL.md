---
name: sql-export-agent
description: Execute a single ODPS SQL file, export the result to Excel, and optionally persist it to DuckDB with lifecycle cleanup.
---

## Watermark

- Every time this skill is used, overwrite `water.json` in this skill directory.
- Use `../_common/scripts/write_watermark.py` to write the file.
- Required JSON shape:
  - `skill`: `sql-export-agent`
  - `version`: watermark version, default `v1`
  - `input_files`: input file names/paths used for this run, or `[]`
  - `actions`: concise completed actions for this run
- Include the executed SQL file in `input_files` when available.
- Do this before the final answer for the skill, and overwrite rather than append.

# SQL Export Agent

## Purpose

Turn one `.sql` file into a controlled execution workflow that an agent can run safely and repeatedly:

1. read SQL from disk
2. execute it in ODPS
3. materialize the result as a pandas DataFrame
4. export to `.xlsx`
5. optionally cache the same result into DuckDB
6. enforce local DuckDB table lifecycle cleanup

This skill is for **single-file SQL execution and export**, not for arbitrary multi-step SQL orchestration.

## Directory index

```text
.
├── SKILL.md
├── references/  
│   └── duckdb.md
└── scripts/
    ├── run_sql_export.py
    ├── example.env
    └── example_command.sh
```

## Read these first

- `references/tables.md`: expected source/target table notes, naming assumptions, business table context
- `references/duckdb.md`: local cache behavior, DuckDB usage rules, lifecycle metadata conventions
- `references/pythonodps.md`: PyODPS installation, ODPS client construction, SQL execution, result retrieval, and DataWorks Tunnel caveats

## What this skill does

Given a SQL file path, the workflow:

- loads environment variables with `dotenv`
- creates an ODPS client from CLI args or env vars
- reads the SQL text from file
- submits the SQL asynchronously with `odps.run_sql(...)`
- prints the Logview URL immediately
- waits for task success
- opens an Arrow reader with tunnel mode
- converts the full result to pandas with multiprocessing
- stops if the DataFrame is empty
- writes Excel output under `save_path`
- optionally writes the same data into a DuckDB table
- before DuckDB write, drops expired cached tables recorded in lifecycle metadata

## Inputs

### Required

- `file_path`: path to one SQL file

### Optional

- `save_path`: output directory for Excel files, default `./files`
- `file_name`: target Excel file name; if omitted, derive from SQL file name
- `access-id`: ODPS access ID
- `access-key`: ODPS access key
- `project`: ODPS project
- `endpoint`: ODPS endpoint
- `duckdb-path`: DuckDB database path, default `warehouse.db`
- `duckdb-table`: table name for local persistence
- `lifecycle`: retention days for the DuckDB table, default `30`

### Environment variables supported

- `ALIBABA_CLOUD_ACCESS_KEY_ID`
- `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
- `ALIBABA_CLOUD_PROJECT_JINGYING`
- `ALIBABA_CLOUD_REGION_ENDPOINT`

## Outputs

### Always attempted

- one Excel file: `{save_path}/{base_name}.xlsx`

### Conditionally attempted

- one DuckDB table in `duckdb-path` when `duckdb-table` is provided
- one lifecycle metadata record in `__table_lifecycle`

## Execution contract for agents

An agent using this skill should follow this exact order:

1. verify `file_path` exists and is a file
2. verify ODPS credentials are present through args or env
3. read SQL text exactly as-is from disk
4. execute the SQL in ODPS
5. wait for success before reading results
6. fetch into pandas
7. if DataFrame is empty, stop and report “No data returned. Skipping exports.”
8. determine `base_name`
9. export Excel
10. if `duckdb-table` is set:
   - validate table name
   - validate `lifecycle > 0`
   - cleanup expired tables
   - write `CREATE OR REPLACE TABLE`
   - upsert lifecycle metadata

Do not reorder these steps.

## Safety boundaries

### 1. DuckDB table names are restricted

Only allow identifiers matching:

```regex
[A-Za-z_][A-Za-z0-9_]*
```

Reject names with spaces, hyphens, dots, quotes, schema prefixes, or SQL fragments.

### 2. Empty result means no export

If the query returns an empty DataFrame, do **not** create Excel or DuckDB outputs.

### 3. Lifecycle must be positive

If `duckdb-table` is provided, `lifecycle` must be greater than `0`.

### 4. Scope is one SQL file

This skill is intentionally scoped to **one** SQL file at a time. The directory-processing branch is not active and should not be assumed available.

### 5. This skill is execution-oriented, not SQL-authoring-oriented

The skill executes an existing SQL file. It should not silently rewrite SQL logic unless the caller explicitly asks for SQL modification.

## Decision rules for agents

Use this skill when:

- the task is “run this SQL file”
- the task is “export SQL result to Excel”
- the task is “cache SQL result locally in DuckDB”
- the user wants a reproducible ODPS → pandas → Excel / DuckDB workflow

Do **not** use this skill when:

- the input is raw SQL text with no file context and the surrounding workflow expects editing/review first
- the task requires batch execution of a whole SQL folder
- the task requires writing back to ODPS tables rather than local export
- the task requires Excel formatting beyond plain `to_excel(...)`
- the task requires DuckDB schema migrations, indexing strategy, or advanced incremental merge logic

## Failure modes to surface clearly

Agents should report the exact stage that failed:

- SQL file read failure
- ODPS authentication/config failure
- ODPS execution failure
- result fetch / reader failure
- Excel write failure
- DuckDB connection or write failure
- invalid DuckDB table name
- invalid lifecycle value

Avoid vague summaries like “execution failed”. Name the failing stage.

## Expected references usage


### `references/duckdb.md`
Use this to understand:

- why DuckDB is being used
- the meaning of `__table_lifecycle`
- retention and cleanup expectations
- local analytical reuse patterns after export

### `references/pythonodps.md`
Use this to understand:

- how the `pyodps` package maps to `from odps import ODPS`
- which constructor fields and environment values are required
- how `run_sql`, `wait_for_success`, `get_logview_address`, and `open_reader` fit together
- why `tunnel=True` matters for export workflows in DataWorks environments
- common package / endpoint / Tunnel / pandas materialization failure modes

## Expected scripts usage

### `scripts/run_sql_export.py`
Canonical implementation of the workflow described in this skill.

### `scripts/example.env`
Minimal environment-variable template for ODPS credentials.

### `scripts/example_command.sh`
Example CLI invocations for:

- Excel-only export
- Excel + DuckDB export
- custom output file naming

## Minimal invocation patterns

### Excel only

```bash
python scripts/run_sql_export.py path/to/query.sql --save_path ./files
```

### Excel + DuckDB cache

```bash
python scripts/run_sql_export.py path/to/query.sql \
  --save_path ./files \
  --duckdb-path ./warehouse.db \
  --duckdb-table tmp_result \
  --lifecycle 30
```

### Explicit output file name

```bash
python scripts/run_sql_export.py path/to/query.sql \
  --save_path ./files \
  --file_name monthly_report.xlsx
```

## Agent-facing checklist

Before execution:

- confirm the input is a file
- confirm ODPS credentials are resolvable
- confirm output directory exists or can be created by the caller
- confirm DuckDB table name is safe if DuckDB output is requested

After execution:

- report Logview availability
- report row count and column names if available
- report Excel output path
- report DuckDB output path/table if used
- report lifecycle expiry time if DuckDB was used

## Non-goals

This skill does not define:

- SQL linting or templating
- SQL semantic validation against business logic
- Excel styling or pivot generation
- multi-file dependency scheduling
- incremental CDC loading into DuckDB
- data quality assertions beyond empty/non-empty result detection

## Implementation notes distilled from the Python flow

- SQL execution is asynchronous at submission time, but the workflow becomes blocking before result retrieval
- result loading uses Arrow reader + pandas conversion with `multiprocessing.cpu_count()` parallelism
- the current implementation prints status and errors instead of raising a structured result object
- DuckDB cache cleanup is metadata-driven via `__table_lifecycle`
- table writes are `CREATE OR REPLACE`, so this is overwrite semantics, not append semantics

## Recommended extension path

If this skill grows later, extend in this order:

1. structured return object instead of print-only logging
2. optional row-limit support that is truly enforced at fetch/export stage
3. output-directory creation and validation
4. batch SQL directory mode behind an explicit flag
5. optional data quality checks before export
6. richer DuckDB modes such as append/merge with explicit keys
