-- apply_woe_in_duckdb.sql
-- Purpose: example SQL pattern for full-scale WOE scoring in DuckDB.
-- Replace placeholder bin rules with frozen artifacts from export_breaks.py.

-- Input assumptions:
--   scored_input(entity_id, target, feature_num_1, feature_cat_1, ...)
-- Output:
--   scored_output(entity_id, score, feature-level WOE columns)

CREATE OR REPLACE TABLE scored_output AS
WITH binned AS (
    SELECT
        entity_id,
        target,

        -- Numeric variable binning example
        CASE
            WHEN feature_num_1 IS NULL THEN 'MISSING'
            WHEN feature_num_1 < 100 THEN '(-inf,100)'
            WHEN feature_num_1 < 300 THEN '[100,300)'
            ELSE '[300,inf)'
        END AS feature_num_1_bin,

        -- Categorical variable binning example
        CASE
            WHEN feature_cat_1 IS NULL OR TRIM(feature_cat_1) = '' THEN 'MISSING'
            WHEN feature_cat_1 IN ('A', 'B') THEN 'A_or_B'
            WHEN feature_cat_1 IN ('C') THEN 'C'
            ELSE 'OTHER'
        END AS feature_cat_1_bin
    FROM scored_input
),
woe_mapped AS (
    SELECT
        entity_id,
        target,
        feature_num_1_bin,
        feature_cat_1_bin,

        -- Replace with frozen WOE values from training artifacts
        CASE feature_num_1_bin
            WHEN 'MISSING' THEN 0.115
            WHEN '(-inf,100)' THEN -0.420
            WHEN '[100,300)' THEN -0.050
            WHEN '[300,inf)' THEN 0.210
            ELSE 0.000
        END AS feature_num_1_woe,

        CASE feature_cat_1_bin
            WHEN 'MISSING' THEN 0.090
            WHEN 'A_or_B' THEN -0.180
            WHEN 'C' THEN 0.060
            WHEN 'OTHER' THEN 0.020
            ELSE 0.000
        END AS feature_cat_1_woe
    FROM binned
),
scored AS (
    SELECT
        entity_id,
        target,
        feature_num_1_bin,
        feature_cat_1_bin,
        feature_num_1_woe,
        feature_cat_1_woe,

        -- Example logistic-style linear score (placeholder coefficients)
        -2.100
        + 1.250 * feature_num_1_woe
        + 0.860 * feature_cat_1_woe AS logit_score
    FROM woe_mapped
)
SELECT
    *,
    1.0 / (1.0 + exp(-logit_score)) AS pd_score
FROM scored;

-- Optional checks:
-- SELECT COUNT(*) AS n, AVG(pd_score) AS avg_pd FROM scored_output;
-- SELECT feature_num_1_bin, COUNT(*) FROM scored_output GROUP BY 1 ORDER BY 2 DESC;
