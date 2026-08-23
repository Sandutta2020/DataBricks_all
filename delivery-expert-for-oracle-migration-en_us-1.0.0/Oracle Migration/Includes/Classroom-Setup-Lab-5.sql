-- Databricks notebook source
-- MAGIC %run ./Classroom-Setup-Common

-- COMMAND ----------

DROP SCHEMA IF EXISTS lab_5 CASCADE;
CREATE SCHEMA IF NOT EXISTS lab_5;
USE SCHEMA lab_5;

-- COMMAND ----------

-- system_billing.usage
-- Mirrors: system.billing.usage
-- Generates hourly records for the last 4 months for all eight warehouses.
-- Patterns:
--   - Business hours (07:00-18:00 weekdays): active, higher DBU
--   - Off-peak: very low or zero for well-configured warehouses
--   - mkt_dashboard (auto_stop=120) and eng_ml (auto_stop=240): remain active off-peak
--   - engineering month-over-month growth factor applied (~5% MoM increase)
-- Note: usage_metadata and product_features use named_struct to match production column patterns.

CREATE OR REPLACE TABLE system_billing_usage AS
WITH
hours AS (
  SELECT explode(sequence(
    DATE_TRUNC('MONTH', CURRENT_TIMESTAMP() - INTERVAL 4 MONTHS),
    DATE_TRUNC('HOUR', CURRENT_TIMESTAMP()),
    INTERVAL 1 HOUR
  )) AS ts
),
warehouses AS (
  SELECT * FROM (VALUES
    -- (warehouse_id, workspace_id, sku_name, custom_tags,
    --  peak_dbu, offpeak_dbu, peak_active_pct, offpeak_active_pct, apply_growth)
    ('wh_fin_01', 2001000000001L, 'PREMIUM_SERVERLESS_SQL_COMPUTE_AP_SYDNEY',
     map('bu','finance','environment','prod','project','financial-reporting','cost-center','fin-001'),
     2.1, 0.0, 0.75, 0.0, FALSE),

    ('wh_fin_02', 2001000000001L, 'PREMIUM_SERVERLESS_SQL_COMPUTE_AP_SYDNEY',
     map('bu','finance','environment','dev','project','finance-analytics','cost-center','fin-001'),
     1.2, 0.0, 0.55, 0.0, FALSE),

    -- mkt_01: CLASSIC MEDIUM, auto_stop=120 - stays active off-peak
    ('wh_mkt_01', 2001000000002L, 'PREMIUM_SQL_CLASSIC_COMPUTE_AP_SYDNEY',
     map('bu','marketing'),
     14.0, 14.0, 0.90, 0.80, FALSE),

    -- mkt_02: no tags
    ('wh_mkt_02', 2001000000002L, 'PREMIUM_SERVERLESS_SQL_COMPUTE_AP_SYDNEY',
     map(),
     3.5, 0.0, 0.65, 0.0, FALSE),

    ('wh_eng_01', 2001000000003L, 'PREMIUM_SERVERLESS_SQL_COMPUTE_AP_SYDNEY',
     map('bu','engineering','environment','dev','project','data-platform','cost-center','eng-003'),
     2.5, 0.0, 0.70, 0.0, TRUE),

    ('wh_eng_02', 2001000000003L, 'PREMIUM_SERVERLESS_SQL_COMPUTE_AP_SYDNEY',
     map('bu','engineering','environment','prod','project','data-platform','cost-center','eng-003'),
     8.5, 1.5, 0.88, 0.20, TRUE),

    -- eng_ml: CLASSIC LARGE, auto_stop=240, no tags - the major cost offender
    ('wh_eng_03', 2001000000003L, 'PREMIUM_SQL_CLASSIC_COMPUTE_AP_SYDNEY',
     map(),
     68.0, 68.0, 0.92, 0.88, TRUE),

    ('wh_shr_01', 2001000000004L, 'PREMIUM_SERVERLESS_SQL_COMPUTE_AP_SYDNEY',
     map('bu','shared','environment','prod','project','executive-reporting','cost-center','shr-004'),
     2.0, 0.0, 0.60, 0.0, FALSE)
  ) t(warehouse_id, workspace_id, sku_name, custom_tags,
      peak_dbu, offpeak_dbu, peak_active_pct, offpeak_active_pct, apply_growth)
),
base AS (
  SELECT
    h.ts                                   AS usage_start_time,
    h.ts + INTERVAL 1 HOUR                AS usage_end_time,
    CAST(h.ts AS DATE)                     AS usage_date,
    HOUR(h.ts)                             AS hr,
    DAYOFWEEK(h.ts)                        AS dow,  -- 1=Sun, 7=Sat
    MONTH(h.ts)                            AS mo,
    w.*,
    -- is_business_hours: Mon-Fri 07:00-18:00
    CASE
      WHEN DAYOFWEEK(h.ts) BETWEEN 2 AND 6
       AND HOUR(h.ts) BETWEEN 7 AND 17 THEN TRUE
      ELSE FALSE
    END AS is_biz,
    -- deterministic "noise" using hour and day-of-month to vary usage (avoids RAND for reproducibility)
    0.75 + 0.50 * ((DAYOFMONTH(h.ts) + HOUR(h.ts)) % 7) / 7.0 AS noise_factor,
    -- engineering month-over-month growth (~5% MoM compounding)
    CASE WHEN apply_growth THEN
      CASE MONTH(h.ts)
        WHEN 1  THEN 1.00
        WHEN 2  THEN 1.05
        WHEN 3  THEN 1.10
        WHEN 4  THEN 1.16
        WHEN 5  THEN 1.22
        WHEN 6  THEN 1.28
        WHEN 7  THEN 1.34
        WHEN 8  THEN 1.41
        WHEN 9  THEN 1.48
        WHEN 10 THEN 1.55
        WHEN 11 THEN 1.63
        WHEN 12 THEN 1.71
      END
    ELSE 1.0 END AS growth_factor
  FROM hours h
  CROSS JOIN warehouses w
),
computed AS (
  SELECT
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890' AS account_id,
    workspace_id,
    MD5(CONCAT(warehouse_id, CAST(usage_start_time AS STRING))) AS record_id,
    sku_name,
    'AWS'                  AS cloud,
    usage_start_time,
    usage_end_time,
    usage_date,
    usage_date + INTERVAL 1 DAY  AS ingestion_date,
    custom_tags,
    'DBU'                  AS usage_unit,
    ROUND(
      CASE
        WHEN is_biz AND (hr + dow + DAYOFMONTH(usage_date)) % 100 < CAST(peak_active_pct   * 100 AS INT)
          THEN peak_dbu   * noise_factor * growth_factor
        WHEN NOT is_biz AND (hr + dow + DAYOFMONTH(usage_date)) % 100 < CAST(offpeak_active_pct * 100 AS INT)
          THEN offpeak_dbu * noise_factor * growth_factor
        ELSE 0.0
      END, 4
    ) AS usage_quantity,
    named_struct(
      'warehouse_id',  warehouse_id,
      'notebook_path', CAST(NULL AS STRING),
      'job_id',        CAST(NULL AS STRING),
      'node_type',     CASE WHEN sku_name LIKE '%SERVERLESS%' THEN 'db.serverless' ELSE 'i3.xlarge' END
    ) AS usage_metadata,
    named_struct(
      'run_as',   CAST(NULL AS STRING),
      'owned_by', CAST(NULL AS STRING)
    ) AS identity_metadata,
    'SQL'          AS billing_origin_product,
    named_struct(
      'is_serverless', sku_name LIKE '%SERVERLESS%',
      'sql_tier',      CAST(NULL AS STRING)
    ) AS product_features,
    'COMPUTE_TIME' AS usage_type,
    'ORIGINAL'     AS record_type
  FROM base
)
SELECT * FROM computed
WHERE usage_quantity > 0;

-- COMMAND ----------

-- MAGIC %run ./Oracle-HR-Schema-Setup

-- COMMAND ----------

SELECT "lab_5" AS `Created Schema`,
       "OK" AS Status;
