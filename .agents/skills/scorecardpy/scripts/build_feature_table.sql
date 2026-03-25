-- build_feature_table.sql
-- Purpose: build a modeling table in DuckDB with one row per entity.
-- Replace placeholder names before use.

CREATE OR REPLACE TABLE feature_table AS
WITH base AS (
    SELECT
        s.entity_id,
        CAST(s.snapshot_date AS DATE) AS snapshot_date,
        CAST(l.target AS INTEGER) AS target,
        s.feature_num_1,
        s.feature_num_2,
        s.feature_cat_1,
        s.feature_cat_2,
        s.event_ts
    FROM source_events s
    INNER JOIN labels l
        ON s.entity_id = l.entity_id
    WHERE s.snapshot_date BETWEEN DATE '2025-01-01' AND DATE '2025-12-31'
),
dedup AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY entity_id, snapshot_date
            ORDER BY event_ts DESC
        ) AS rn
    FROM base
),
cleaned AS (
    SELECT
        entity_id,
        snapshot_date,
        target,
        CAST(feature_num_1 AS DOUBLE) AS feature_num_1,
        CAST(feature_num_2 AS DOUBLE) AS feature_num_2,
        COALESCE(NULLIF(TRIM(feature_cat_1), ''), 'MISSING') AS feature_cat_1,
        COALESCE(NULLIF(TRIM(feature_cat_2), ''), 'MISSING') AS feature_cat_2
    FROM dedup
    WHERE rn = 1
)
SELECT
    entity_id,
    snapshot_date,
    target,
    feature_num_1,
    feature_num_2,
    feature_cat_1,
    feature_cat_2
FROM cleaned;

-- Optional quick checks:
-- SELECT COUNT(*) AS n_rows, AVG(target) AS bad_rate FROM feature_table;
-- DESCRIBE feature_table;
