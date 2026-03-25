# DuckDB Cache Rules for SQL Export Agent

This skill uses DuckDB as a local cache for ODPS query results.

Scope of DuckDB usage in this skill:
- Optional persistence after successful ODPS query and Excel export.
- Overwrite semantics (`CREATE OR REPLACE TABLE`), not append/merge.
- Lifecycle-based cleanup via metadata table `__table_lifecycle`.

## Why DuckDB Here

- Fast local query and reuse of exported result sets.
- Easy sharing of cached analytical snapshots through a single `.db` file.
- Useful fallback when repeated ODPS pulls are expensive.

## Lifecycle Metadata Contract

The script manages a metadata table named `__table_lifecycle`.

Expected columns:
- `table_name` (`VARCHAR`) primary key
- `created_at` (`TIMESTAMP`)
- `expires_at` (`TIMESTAMP`)
- `lifecycle_days` (`INTEGER`)

Behavior:
1. Before writing a new cache table, drop expired tables listed in metadata.
2. Remove expired metadata records.
3. After writing the new table, upsert metadata with fresh `created_at` and `expires_at`.

This keeps local cache bounded without external schedulers.

## Table Naming Safety

Only allow DuckDB table names matching:

```regex
[A-Za-z_][A-Za-z0-9_]*
```

Reject:
- schema-qualified names (for example `main.tmp_result`)
- quoted names
- names with spaces/hyphens/dots
- SQL fragments

Reason: table name is used in SQL DDL, so strict validation avoids injection and accidental misuse.

## Write Semantics

Cache write should be:
- deterministic
- idempotent for same input
- full overwrite

Recommended SQL pattern:

```sql
CREATE OR REPLACE TABLE <table_name> AS
SELECT * FROM df;
```

## Operational Notes

- Keep `lifecycle > 0` whenever DuckDB write is requested.
- Store db path explicitly (for example `./warehouse.db`) in run commands to avoid accidental writes to unknown working directories.
- If result DataFrame is empty, skip DuckDB write.
- Report final cache location and expiration timestamp in run logs.

## Troubleshooting

1. `Catalog Error: Table ... does not exist` during cleanup
- Cause: stale metadata entry or manual table deletion.
- Action: continue cleanup and remove stale metadata.

2. `Parser Error` during `CREATE OR REPLACE`
- Cause: invalid `duckdb-table` name.
- Action: enforce strict regex validation before SQL execution.

3. Locked database file
- Cause: another process has write lock.
- Action: retry after closing other DuckDB clients or switch to a different `duckdb-path`.
