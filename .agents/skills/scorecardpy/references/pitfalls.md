# Common Pitfalls and Fixes

## 1) pandas Memory Explosion

Symptom:
- notebook/kernel crashes or severe swap thrashing

Root cause:
- full-table export from DuckDB to pandas

Fix:
- sample in DuckDB first
- export only target and selected features

## 2) Unstable Bins Across Iterations

Symptom:
- breakpoints keep changing for the same variable

Root cause:
- unstable sampling
- repeated uncontrolled auto-binning

Fix:
- deterministic sample
- persist dev sample table
- freeze and reuse breaks after approval

## 3) Very Slow `woebin`

Symptom:
- binning takes too long

Root cause:
- too many rows/features
- high-cardinality categoricals

Fix:
- shrink sample for iteration
- pre-collapse categories in DuckDB
- pre-drop weak/invalid columns

## 4) Bad Class Underrepresented

Symptom:
- bins on minority class are noisy or degenerate

Root cause:
- naive random sampling on highly imbalanced data

Fix:
- stratified sampling
- keep all bads plus sampled goods

## 5) Data Leakage in Features

Symptom:
- unrealistically high train performance, poor OOT performance

Root cause:
- post-outcome or policy-decision variables included

Fix:
- remove leakage columns before modeling
- enforce feature cutoff date rules

## 6) Train/OOT Confusion

Symptom:
- inflated evaluation or contradictory monitoring metrics

Root cause:
- mixed period/split definitions

Fix:
- document split fields and date windows explicitly
- materialize train/test/oot tables separately

## 7) Categorical Mapping Mismatch in Deployment

Symptom:
- missing WOE/points for categories in production

Root cause:
- no fallback bin (`OTHER`/`MISSING`) in SQL mapping

Fix:
- always define fallback logic
- monitor unmatched category rates

## 8) Silent Preprocessing Drift

Symptom:
- model performance declines without obvious reason

Root cause:
- dev and deployment feature engineering differ

Fix:
- keep feature SQL versioned
- run periodic parity checks between dev and prod pipelines

## Quick Prevention Checklist

- freeze sample definition
- freeze bins and special values
- separate development and deployment logic
- keep deterministic SQL scoring path
- monitor drift and mapping coverage over time
