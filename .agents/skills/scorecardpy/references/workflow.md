# Scorecard Workflow on Large Local Data

This workflow is the default path for large datasets:

1. Build a clean modeling table in DuckDB.
2. Reduce features before pandas.
3. Sample development data in DuckDB.
4. Export only sampled columns to pandas.
5. Run scorecardpy on the sampled dataset.
6. Freeze bins and selected variables.
7. Apply WOE and score logic at full scale in DuckDB.

## 1) Build Modeling Table

Goal: one row per modeling entity (user/account/order/application).

Required columns:
- `entity_id`
- `target` (0/1)
- candidate features

Do in DuckDB:
- deduplicate entity grain
- join labels
- aggregate event features
- normalize null-like values
- remove leakage fields

Use `scripts/build_feature_table.sql` as the template.

## 2) Reduce Feature Complexity

Before scorecardpy, reduce noisy columns:
- drop IDs and timestamps not intended as features
- collapse rare categories into `OTHER`
- drop constant or near-constant columns
- convert booleans to integer flags

Reason: `woebin` cost grows quickly with row count, feature count, and category cardinality.

## 3) Sample in DuckDB

Never default to full export for large tables.

Preferred strategies:
- fixed-size random sample
- stratified sample by target
- keep all bads + downsample goods

For reproducibility, use deterministic hash sampling or fixed seed plus materialized sample tables.

Use `scripts/sample_dev_data.sql`.

## 4) Export Only Development Columns

From DuckDB to pandas, export only:
- `target`
- selected feature columns
- optional `entity_id` for traceability

Avoid `SELECT *` unless table size is already proven small.

## 5) Run scorecardpy

Typical pipeline:
- `var_filter`
- `woebin`
- `woebin_ply`
- logistic model fitting
- `scorecard` and `scorecard_ply`
- `perf_eva` and optional `perf_psi`

Use `scripts/run_scorecardpy.py`.

## 6) Freeze Artifacts

After acceptable bins are approved, freeze:
- bin definitions (`bins.pkl` or equivalent)
- breakpoints and special values (`breaks_list`, `special_values`)
- selected variable list
- model coefficients
- scorecard points mapping

Use `scripts/export_breaks.py` to create stable JSON outputs.

## 7) Deploy in DuckDB

For large-scale scoring, push logic back to DuckDB:
- assign bins with deterministic SQL
- map bins to WOE/points
- aggregate per-row score

Use `scripts/apply_woe_in_duckdb.sql`.

## Reproducibility Checklist

- Record data snapshot date and label window.
- Record modeling grain.
- Record sample strategy and seed/hash rule.
- Version all frozen artifacts.
- Separate development sample logic from full-data scoring logic.
