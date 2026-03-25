# scorecardpy Usage Notes

Use scorecardpy as a methodology layer on sampled development data, not as a large-scale compute engine.

## Core Function Roles

- `var_filter(df, y=...)`
  - Drop unusable variables by missingness, identical rate, and IV heuristics.
- `woebin(df, y=...)`
  - Build bins and WOE maps.
  - Usually the most expensive step.
- `woebin_ply(df, bins)`
  - Apply binning rules and produce WOE-transformed columns.
- `scorecard(bins, model, xcolumns)`
  - Convert model coefficients and WOE maps to points card.
- `scorecard_ply(df, card)`
  - Compute per-row score.
- `perf_eva(...)`
  - Evaluate ROC/KS/Lift style performance.
- `perf_psi(...)`
  - Stability check between samples/time periods.

## Recommended Modeling Order

1. Filter variables (`var_filter`).
2. Build bins (`woebin`), optionally with constraints.
3. Transform to WOE (`woebin_ply`).
4. Fit logistic model on WOE features.
5. Generate scorecard and score outputs.
6. Evaluate on train/test/OOT splits.

## Parameter Guidance

- `woebin(..., bin_num_limit=...)`
  - Lower values reduce complexity and overfitting risk.
- `positive='1'` or equivalent
  - Keep positive label definition explicit and consistent.
- `special_values`
  - Use for business-defined missing/sentinel values.
- `breaks_list`
  - Use to freeze or partially override auto bins.

## Practical Limits

- Too many rows: binning becomes slow and memory-heavy.
- Too many variables: unstable bins and longer cycles.
- High-cardinality categoricals: large bin search space.

Mitigation:
- Reduce columns in DuckDB first.
- Collapse sparse categories before scorecardpy.
- Use sampled dev data and freeze artifacts once approved.

## Artifact Expectations

Persist at least:
- selected variable list
- bin outputs (`bins` object)
- breaks/special values export
- trained model object
- scorecard mapping object
- evaluation summary metrics

## Troubleshooting

- If bins vary every run:
  - stabilize sample and seed
  - avoid uncontrolled re-binning
- If `woebin` is slow:
  - shrink sample
  - remove high-cardinality columns
  - provide partial `breaks_list` where known

For operationalization details, see `references/duckdb-deployment.md`.
