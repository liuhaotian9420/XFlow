# Sampling Guide for Scorecard Development

Large-table scorecard modeling should sample in DuckDB first, then run scorecardpy on the sampled data.

## Strategy Selection

1. Fixed-size random sample
- Use when class balance is acceptable.
- Fast for early iteration.

2. Stratified sample by target
- Use when positive class is rare.
- Preserve class ratio or target custom ratio.

3. Keep all bads + downsample goods
- Practical default for severe imbalance.
- Improves bad-sample coverage for binning stability.

## Reproducibility Rules

- Prefer deterministic hash sampling over non-deterministic `random()`.
- Persist sampled tables if multiple binning iterations are expected.
- Save sample SQL and business date filters with artifacts.

Deterministic example pattern:

```sql
abs(hash(cast(entity_id as varchar) || '|seed=20260325')) % 1000 < 50
```

This yields an approximate 5% stable sample.

## Sample Size Heuristics

- Start with 100k to 500k rows for fast iteration.
- Increase only when bins or coefficients are unstable.
- Ensure enough bad samples per key variable (rule of thumb: several hundred minimum).

## Class Imbalance Notes

- If bad rate is below 2%, naive random sample may miss important bad patterns.
- Prefer:
  - all bads
  - goods sampled at a bounded ratio (for example 3:1 to 10:1 goods:bads)

If you rebalance for development, document that calibration or cutoff tuning must consider true production class distribution.

## Quality Checks After Sampling

- Check total rows and bad rate.
- Compare sampled vs source distribution for major features.
- Check missingness profile for key variables.
- Check time coverage if data is time-dependent.

## Common Mistakes

- Sampling in pandas after full export (memory risk).
- Using unstable random seeds across reruns.
- Mixing train and OOT data in one sample silently.
- Oversampling bads without documenting downstream calibration impact.

## Script Mapping

- See `scripts/sample_dev_data.sql` for reusable SQL templates.
- Use `references/pitfalls.md` for troubleshooting unstable bins and sample drift.
