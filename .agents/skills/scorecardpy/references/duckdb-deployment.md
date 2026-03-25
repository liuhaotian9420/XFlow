# DuckDB Deployment of Bins, WOE, and Scores

After binning is approved on the development sample, run full-data scoring in DuckDB for scale and reproducibility.

## Deployment Modes

1. pandas deployment
- Acceptable only for modest full datasets.

2. DuckDB SQL deployment
- Preferred for large local datasets.
- Deterministic, auditable, and fast for batch scoring.

## Recommended Artifacts to Export

- `breaks_list.json`
- `special_values.json`
- `bins` summary (bin label, interval/category set, WOE, points)
- selected variable list
- score scaling parameters (if points scaling is used)

## SQL Design Patterns

### Pattern A: Inline CASE WHEN

Pros:
- No extra mapping tables.
- Simple for a small number of variables.

Cons:
- Harder to maintain for many variables.

### Pattern B: Mapping Table Join

Pros:
- Centralized governance and versioning.
- Easier to audit and update.

Cons:
- Requires robust bin key design.

## Determinism and Governance

- Version deployment SQL with artifact version tags.
- Include effective date and sample version in metadata.
- Keep train-time and production-time preprocessing aligned.
- Reject scoring if required feature columns are missing.

## Validation Checks

- Compare score distributions between pandas dev run and DuckDB deployment sample.
- Recompute a small sample in both pipelines and diff row-level scores.
- Monitor missing rate and out-of-range frequency in production.
- Track PSI by period for drift alerts.

## Minimal Deployment Flow

1. Load frozen bin artifacts.
2. Build SQL bin assignment expressions.
3. Map bins to WOE or points.
4. Aggregate to final score.
5. Persist scored table with version metadata.

Use `scripts/apply_woe_in_duckdb.sql` as baseline template.
