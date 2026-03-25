-- sample_dev_data.sql
-- Purpose: create reproducible development samples in DuckDB.
-- Input table assumption: feature_table(entity_id, target, ...features...)

-- -----------------------------------------------------------------------------
-- Strategy A: deterministic fixed-rate sample (about 10%)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE dev_sample_fixed AS
SELECT *
FROM feature_table
WHERE abs(hash(CAST(entity_id AS VARCHAR) || '|seed=20260325')) % 1000 < 100;

-- -----------------------------------------------------------------------------
-- Strategy B: deterministic stratified sample by target
-- target=1 keep 80%, target=0 keep 10%
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE dev_sample_stratified AS
SELECT *
FROM feature_table
WHERE (
    target = 1
    AND abs(hash(CAST(entity_id AS VARCHAR) || '|seed=20260325|bad')) % 1000 < 800
) OR (
    target = 0
    AND abs(hash(CAST(entity_id AS VARCHAR) || '|seed=20260325|good')) % 1000 < 100
);

-- -----------------------------------------------------------------------------
-- Strategy C: keep all bads + downsample goods
-- target=1 keep all
-- target=0 keep about 5%
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE dev_sample_all_bads AS
SELECT *
FROM feature_table
WHERE target = 1
   OR (
        target = 0
        AND abs(hash(CAST(entity_id AS VARCHAR) || '|seed=20260325|goods')) % 1000 < 50
   );

-- Optional profile check:
-- SELECT 'fixed' AS sample_name, COUNT(*) AS n, AVG(target) AS bad_rate FROM dev_sample_fixed
-- UNION ALL
-- SELECT 'stratified' AS sample_name, COUNT(*) AS n, AVG(target) AS bad_rate FROM dev_sample_stratified
-- UNION ALL
-- SELECT 'all_bads' AS sample_name, COUNT(*) AS n, AVG(target) AS bad_rate FROM dev_sample_all_bads;
