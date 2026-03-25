#!/usr/bin/env bash

# Excel only
python scripts/run_sql_export.py path/to/query.sql \
  --save_path ./files

# Excel + DuckDB cache
python scripts/run_sql_export.py path/to/query.sql \
  --save_path ./files \
  --duckdb-path ./warehouse.db \
  --duckdb-table tmp_result \
  --lifecycle 30

# Explicit output file name
python scripts/run_sql_export.py path/to/query.sql \
  --save_path ./files \
  --file_name monthly_report.xlsx

# Explicit ODPS credentials from CLI
python scripts/run_sql_export.py path/to/query.sql \
  --save_path ./files \
  --access-id "$ALIBABA_CLOUD_ACCESS_KEY_ID" \
  --access-key "$ALIBABA_CLOUD_ACCESS_KEY_SECRET" \
  --project "$ALIBABA_CLOUD_PROJECT_JINGYING" \
  --endpoint "$ALIBABA_CLOUD_REGION_ENDPOINT"
