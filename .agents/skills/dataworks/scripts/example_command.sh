#!/usr/bin/env bash

# Excel only export
python .agents/skills/dataworks/scripts/run_sql_export.py \
  .agents/skills/dataworks/scripts/example.sql \
  --save_path ./.agents/skills/dataworks/scripts/files

# Excel + DuckDB cache
python .agents/skills/dataworks/scripts/run_sql_export.py \
  .agents/skills/dataworks/scripts/example.sql \
  --save_path ./.agents/skills/dataworks/scripts/files \
  --duckdb-path ./.agents/skills/dataworks/scripts/warehouse.db \
  --duckdb-table tmp_result \
  --lifecycle 30

# Extract table usage from local SQL snippets
python .agents/skills/dataworks/scripts/extract_tables_from_sql_snippets.py \
  --input-dir ./.agents/skills/dataworks/references/sql_snippets/sql代码 \
  --output ./.agents/skills/dataworks/references/tables.md

# Bootstrap from trusted ground-truth tables markdown
python .agents/skills/dataworks/scripts/bootstrap_tables_reference.py \
  --source-md ./.agents/skills/sql-generator/references/tables.md \
  --target-md ./.agents/skills/dataworks/references/tables.md

# Sync a known ODPS table into tables.md
python .agents/skills/dataworks/scripts/sync_table_metadata.py \
  --table-name your_project.your_table \
  --tables-md ./.agents/skills/dataworks/references/tables.md \
  --sample-limit 5

# Local smoke test without ODPS credentials
python .agents/skills/dataworks/scripts/sync_table_metadata.py \
  --mock-metadata-json ./.agents/skills/dataworks/tests/fixtures/mock_table_metadata.json \
  --tables-md ./.agents/skills/dataworks/tests/tmp_tables.md
