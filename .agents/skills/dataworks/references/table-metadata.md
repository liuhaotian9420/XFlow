# PyODPS Table Metadata Reference

Use this reference when the task is: "I already know the table name, fetch its schema / DDL / sample rows and sync them into `tables.md`."

## Scope

This file covers the official PyODPS APIs needed for table introspection:

- `odps.get_table(...)`
- `table.table_schema`
- `table.table_schema.columns`
- `table.table_schema.partitions`
- `table.get_ddl(...)`
- `table.head(...)`

## Official documentation

- Table object API: <https://pyodps.readthedocs.io/en/latest/api-models.html>
- Table basics in Chinese docs: <https://pyodps.readthedocs.io/zh-cn/latest/base-tables.html>

## Practical mapping

### Get the table object

Use:

```python
table = odps.get_table("project_name.table_name")
```

### Read field names and data types

The official docs expose:

- `table.table_schema`
- `table.table_schema.columns`
- `table.table_schema.partitions`

The Chinese docs show `t.table_schema.columns` returning column objects, and each column exposes at least name and type.

Use this for the canonical field list in `tables.md`.

### Read DDL

The official Table API documents:

```python
table.get_ddl(with_comments=True, if_not_exists=False, force_table_ddl=False)
```

Use this when the skill needs a faithful table-definition snapshot.

### Read sample rows

The official Table API documents:

```python
table.head(limit)
```

This returns head records of the table, with a documented maximum of 10000 rows. For this skill, keep sample capture small and stable, such as `5`.

## Decision rules

- Prefer `table.table_schema` for field names and types.
- Prefer `table.get_ddl(...)` when exact DDL is useful or comments matter.
- Prefer `table.head(...)` only for small inspection samples, not full export.
- Keep sample rows optional because some validation flows only need schema + DDL.

## Failure interpretation

- import failure: `pyodps` is missing from the environment
- `get_table(...)` failure: table name, project, endpoint, or permissions are wrong
- `get_ddl(...)` failure: permissions or object type issue
- `head(...)` failure: permissions, data access, or runtime tunnel issue

## Source links used for this reference

- English API models page: <https://pyodps.readthedocs.io/en/latest/api-models.html>
- Chinese base tables page: <https://pyodps.readthedocs.io/zh-cn/latest/base-tables.html>
