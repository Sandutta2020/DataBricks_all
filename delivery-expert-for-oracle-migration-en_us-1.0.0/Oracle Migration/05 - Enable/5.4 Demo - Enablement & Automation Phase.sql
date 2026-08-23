-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">05 - Enable</span>
-- MAGIC     </div>
-- MAGIC     <div style="display: flex; align-items: center; gap: 8px;">
-- MAGIC         <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="24" height="24" />
-- MAGIC         <span style="color: #999; font-size: 16px;">-></span>
-- MAGIC         <img src="https://cdn.simpleicons.org/databricks/FF3621" width="24" height="24"/>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img
-- MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
-- MAGIC     alt="Databricks Learning"
-- MAGIC   >
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div style="
-- MAGIC   border-left: 4px solid #f44336;
-- MAGIC   background: #ffebee;
-- MAGIC   padding: 14px 18px;
-- MAGIC   border-radius: 4px;
-- MAGIC   margin: 16px 0;
-- MAGIC ">
-- MAGIC   <strong style="display:block; color:#c62828; margin-bottom:6px; font-size: 1.1em;">Important Prerequisites</strong>
-- MAGIC   <div style="color:#333;">
-- MAGIC This notebook is not supported for execution on Databricks Academy provided Vocareum workspaces.
-- MAGIC
-- MAGIC Please go through this guided notebook as a study guide and lecture for Oracle Migration.
-- MAGIC
-- MAGIC The material is intended to be run in your own sandbox environments if you would like. Databricks Academy does not provide Oracle access (on-prem, cloud-hosted, or OCI), a Databricks account with admin level access, or an AWS account for this notebook.
-- MAGIC
-- MAGIC Please view the PREREQUISITES file for more information.
-- MAGIC
-- MAGIC **However, the provided LAB notebooks at the end of each section can be run in a Databricks Academy provided Vocareum workspace and allow you to practice the concepts.**
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Demo: Enablement & Automation Phase

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this demo, you will be able to:
-- MAGIC
-- MAGIC - Query `system.billing.usage` to analyze DBU consumption by team and cost center using custom tags
-- MAGIC - Use `system.query.history` to right-size SQL Warehouses based on real workload data
-- MAGIC - Create dynamic views that combine row and column security
-- MAGIC - Implement row filters and column masks in Unity Catalog to protect HR employee data
-- MAGIC - Apply Attribute-Based Access Control (ABAC) policies using governed tags for centralized governance
-- MAGIC - Audit Unity Catalog privileges and monitor consumer query patterns using system tables

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## Compute Requirements
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC   <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC     <span style="font-size: 24px;">🚨</span>
-- MAGIC     <div>
-- MAGIC       <strong style="color: #1565c0; font-size: 1.1em;">REQUIRED – SQL WAREHOUSE OR SERVERLESS COMPUTE</strong>
-- MAGIC       <p style="margin: 8px 0 0 0; color: #333;">This notebook runs on both <strong>SQL Warehouse</strong> and <strong>Serverless compute</strong>. Select your preferred compute resource before executing any cells.</p>
-- MAGIC       <p style="margin: 8px 0 0 0; color: #333;"><strong>Testing configuration:</strong> This demo was tested using SQL Warehouse</strong> and Serverless compute <strong>version 4</strong>. For more details on Serverless versions, see the <a href="https://docs.databricks.com/aws/en/compute/serverless/dependencies" style="color: #1565c0; text-decoration: none; font-weight: 500;">Databricks documentation</a>.</p>
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Platform Operations and Cost Management

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 1. Querying DBU Consumption by Custom Tags
-- MAGIC
-- MAGIC Query `system.billing.usage` with custom tag breakdowns to support team-level chargeback reporting.

-- COMMAND ----------

-- DBTITLE 1,Query DBU consumption by custom tags for chargeback reporting (SQL)
-- DBU Consumption by Custom Tags
SELECT 
    custom_tags['org'] AS org,
    custom_tags['dev'] AS dev,
    sku_name,
    DATE_TRUNC('month', usage_start_time) AS usage_month,
    SUM(usage_quantity) AS total_dbus,
    COUNT(DISTINCT usage_date) AS active_days
-- Replace custom_tags key names with the tag keys your organisation uses
FROM system.billing.usage
WHERE usage_start_time >= CURRENT_DATE - INTERVAL 90 DAYS
  AND custom_tags IS NOT NULL
GROUP BY ALL
ORDER BY usage_month DESC, total_dbus DESC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 2. Warehouse Utilization Analysis
-- MAGIC
-- MAGIC Use `system.query.history` to measure query volume and latency per warehouse and identify right-sizing candidates.

-- COMMAND ----------

-- DBTITLE 1,Analyze SQL Warehouse utilization for right-sizing decisions (SQL)
-- Warehouse Right-Sizing Analysis
SELECT 
    w.warehouse_name,
    w.warehouse_type,
    w.warehouse_size,
    COUNT(*) AS query_count,
    ROUND(AVG(total_duration_ms) / 1000, 2) AS avg_duration_sec,
    ROUND(PERCENTILE(total_duration_ms, 0.95) / 1000, 2) AS p95_duration_sec,
    ROUND(AVG(waiting_for_compute_duration_ms) / 1000, 2) AS avg_queue_sec,
    ROUND(AVG(waiting_at_capacity_duration_ms) / 1000, 2) AS avg_capacity_wait_sec
FROM system.query.history h
JOIN system.compute.warehouses w 
    ON h.compute.warehouse_id = w.warehouse_id
WHERE h.start_time >= CURRENT_DATE - INTERVAL 7 DAYS
  AND h.compute.warehouse_id IS NOT NULL
GROUP BY w.warehouse_name, w.warehouse_type, w.warehouse_size
HAVING COUNT(*) > 10
ORDER BY avg_queue_sec DESC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 3. Workspace-Level Budget Tracking
-- MAGIC
-- MAGIC Calculate monthly DBU burn rate per team and compare against a budget ceiling to flag overspending early.

-- COMMAND ----------

-- DBTITLE 1,Track spending against budget targets (SQL)
-- Team Budget Burn Rate
WITH monthly_spend AS (
    SELECT 
        custom_tags['org'] AS team,
        DATE_TRUNC('month', usage_start_time) AS usage_month,
        SUM(usage_quantity) AS total_dbus
    FROM system.billing.usage
    WHERE usage_start_time >= DATE_TRUNC('month', CURRENT_DATE)
    GROUP BY ALL
),
budgets AS (
    -- Replace team names and budget values with your organisation's actual figures
    SELECT 'cns' AS team,       50000 AS monthly_budget UNION ALL
    SELECT 'edu',               30000                   UNION ALL
    SELECT 'finance-reporting', 20000
)
SELECT 
    COALESCE(m.team, 'untagged') AS team,
    m.total_dbus,
    b.monthly_budget,
    ROUND(100.0 * m.total_dbus / b.monthly_budget, 1) AS pct_consumed
FROM monthly_spend m
LEFT JOIN budgets b ON m.team = b.team
ORDER BY pct_consumed DESC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Security and Fine-Grained Access

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 1. Row-Level Security with Row Filters

-- COMMAND ----------

-- DBTITLE 1,Create a row filter function (SQL)
-- Restrict HR location data by region based on user group membership
CREATE OR REPLACE FUNCTION migration_dev.hr_raw.region_filter(country_id STRING)
RETURNS BOOLEAN
RETURN (
    -- Admins see all locations
    is_account_group_member('data_admins')
    OR
    -- Regional HR teams see only their region's countries
    (is_account_group_member('hr_apac')  AND country_id IN ('IN', 'AU', 'SG', 'JP', 'CN'))
    OR
    (is_account_group_member('hr_emea')  AND country_id IN ('UK', 'DE', 'FR', 'IT', 'CH', 'NL'))
    OR
    (is_account_group_member('hr_amer')  AND country_id IN ('US', 'CA', 'MX', 'BR'))
    OR
    -- Default: all other workspace users see US locations only
    country_id = 'US'
);

-- COMMAND ----------

-- DBTITLE 1,Applying a Row Filter (SQL)
-- Apply the row filter to the locations table
ALTER TABLE migration_dev.hr_raw.locations
SET ROW FILTER migration_dev.hr_raw.region_filter ON (country_id);

-- Verify the filter is applied
DESCRIBE EXTENDED migration_dev.hr_raw.locations;

-- COMMAND ----------

-- DBTITLE 1,Testing a Row Filter (SQL)
-- Only locations from permitted countries are returned (should only see US without group membership)
SELECT 
    l.location_id,
    l.city,
    l.state_province,
    l.country_id,
    c.country_name,
    r.region_name
FROM migration_dev.hr_raw.locations l
JOIN migration_dev.hr_raw.countries c ON l.country_id = c.country_id
JOIN migration_dev.hr_raw.regions   r ON c.region_id  = r.region_id
ORDER BY r.region_name, c.country_name, l.city;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 2. Column-Level Security with Column Masks

-- COMMAND ----------

-- DBTITLE 1,Create a column mask function (SQL)
-- Create Email Column Mask Function
CREATE OR REPLACE FUNCTION migration_dev.hr_raw.mask_email(email STRING)
RETURNS STRING
RETURN (
    CASE 
        WHEN is_account_group_member('data_admins')  THEN email
        WHEN is_account_group_member('hr_managers')  THEN email
        ELSE mask(email)  -- Returns: Xxxxx.xxxxx
    END
);

-- COMMAND ----------

-- DBTITLE 1,Show column mask
-- Show the column mask
DESCRIBE DETAIL migration_dev.hr_raw.employees

-- COMMAND ----------

-- DBTITLE 1,Apply a column mask (SQL)
-- Drop all check constraints from employees table
ALTER TABLE migration_dev.hr_raw.employees DROP CONSTRAINT IF EXISTS emp_salary_min;
ALTER TABLE migration_dev.hr_raw.employees DROP CONSTRAINT IF EXISTS hire_date_valid;
ALTER TABLE migration_dev.hr_raw.employees DROP CONSTRAINT IF EXISTS salary_positive;

-- Apply Email Mask to Employees Table
ALTER TABLE migration_dev.hr_raw.employees
ALTER COLUMN email SET MASK migration_dev.hr_raw.mask_email;

-- Verify mask is applied
DESCRIBE EXTENDED migration_dev.hr_raw.employees;

-- COMMAND ----------

-- DBTITLE 1,Test column masking (SQL)
-- Test the masking (results depend on your group membership)
SELECT 
    employee_id,
    first_name,
    last_name,
    email,        -- masked for non-admins / non-hr_managers
    phone_number
FROM migration_dev.hr_raw.employees
LIMIT 10;

-- COMMAND ----------

-- DBTITLE 1,Remove column masks when no longer needed (SQL)
-- Drop Email Column Mask
ALTER TABLE migration_dev.hr_raw.employees
ALTER COLUMN email DROP MASK;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 3. Attribute-Based Access Control (ABAC)

-- COMMAND ----------

-- DBTITLE 1,Remove any previously applied row filter (SQL)
-- Remove any previously applied row filter prior to enabling ABAC
ALTER TABLE migration_dev.hr_raw.employees DROP ROW FILTER;
ALTER TABLE migration_dev.hr_raw.employees ALTER COLUMN phone_number DROP MASK;


-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Step 1: Apply Tag to Column
-- MAGIC
-- MAGIC Apply the `class.phone_number` governed tag to the column that will drive row-level access in the ABAC policy.

-- COMMAND ----------

-- DBTITLE 1,Set Tags (SQL)
-- Apply system governed tags to PII columns in the employees table
ALTER TABLE migration_dev.hr_raw.employees
ALTER COLUMN PHONE_NUMBER SET TAGS ('class.phone_number');

ALTER TABLE migration_dev.hr_raw.employees
ALTER COLUMN FIRST_NAME   SET TAGS ('class.name');

ALTER TABLE migration_dev.hr_raw.employees
ALTER COLUMN LAST_NAME    SET TAGS ('class.name');

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Step 2: Audit Applied Tags

-- COMMAND ----------

-- DBTITLE 1,Verify tags are applied (SQL)
-- Audit Column Tags
SELECT 
    catalog_name,
    schema_name,
    table_name, 
    column_name,
    tag_name,
    tag_value
FROM migration_dev.information_schema.column_tags
WHERE schema_name = 'hr_raw'
ORDER BY table_name, column_name;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Step 3: Create a Mask UDF
-- MAGIC
-- MAGIC This UDF will return the masked phone number of an employee.

-- COMMAND ----------

-- DBTITLE 1,Create a UDF for ABAC Column Masking (SQL)
-- ABAC column mask for phone numbers

CREATE OR REPLACE FUNCTION migration_dev.hr_raw.phone_filter(phone_number STRING)
RETURNS STRING
RETURN 
    CASE 
        WHEN phone_number IS NULL THEN NULL
        ELSE CONCAT('***', RIGHT(phone_number, 3))
    END;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Step 4: Create the ABAC Policy
-- MAGIC
-- MAGIC Create a policy that implements our function as a row filter, on all tables in the `migration-dev` catalog, for everyone except members of the `platform-team` group.

-- COMMAND ----------

-- DBTITLE 1,Create an ABAC policy (SQL)
-- ABAC column mask policy for hiding phone numbers

CREATE OR REPLACE POLICY mask_phone_number_policy
ON CATALOG migration_dev
COMMENT 'Hide phone numbers'
COLUMN MASK migration_dev.hr_raw.phone_filter
TO `account users` EXCEPT `platform-team`
FOR TABLES
MATCH COLUMNS
  has_tag('class.phone_number') AS phone_col
ON COLUMN phone_col;

-- COMMAND ----------

-- DBTITLE 1,Test the ABAC policy (SQL)
-- Since we are not 'platform-team', we will see masked phone numbers
SELECT * FROM migration_dev.hr_raw.employees;

-- COMMAND ----------

-- DBTITLE 1,Remove tags when no longer needed (SQL)
-- Remove governed tags when no longer needed
ALTER TABLE migration_dev.hr_raw.employees
ALTER COLUMN PHONE_NUMBER UNSET TAGS ('class.phone_number');

ALTER TABLE migration_dev.hr_raw.employees
ALTER COLUMN FIRST_NAME   UNSET TAGS ('class.name');

ALTER TABLE migration_dev.hr_raw.employees
ALTER COLUMN LAST_NAME    UNSET TAGS ('class.name');

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 4. Dynamic Views for Secure Data Sharing

-- COMMAND ----------

-- DBTITLE 1,Creating a Dynamic View (SQL)
-- Dynamic view combining row filtering and column masking
CREATE OR REPLACE VIEW migration_dev.hr_raw.v_employees_secure AS
SELECT 
    employee_id,
    first_name,
    last_name,
    CASE
        WHEN is_account_group_member('data_admins') THEN salary
        WHEN is_account_group_member('hr_managers') THEN salary
        ELSE NULL
    END AS salary,
    job_id,
    department_id,
    hire_date
FROM migration_dev.hr_raw.employees
-- Row filtering: admins and managers see all employees;
-- Other employees do not see executive leadership (dept. ID 90)
WHERE 
    is_account_group_member('data_admins')
    OR is_account_group_member('hr_managers')
    OR department_id <> 90;

-- COMMAND ----------

-- DBTITLE 1,Testing a Dynamic View (SQL)
-- Test the view (results vary by group membership)
SELECT * FROM migration_dev.hr_raw.v_employees_secure LIMIT 10;

-- COMMAND ----------

-- DBTITLE 1,Clean up (SQL)
-- Clean up
DROP VIEW IF EXISTS migration_dev.hr_raw.v_employees_secure;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 5. Documenting Grants and Inheritance

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Unity Catalog Privilege Audit
-- MAGIC
-- MAGIC Enumerate all effective grants across catalog, schema, and table levels in Unity Catalog for documentation.

-- COMMAND ----------

-- DBTITLE 1,Query effective grants in Unity Catalog (SQL)
-- Comprehensive privilege audit across all object types in migration_dev
SELECT grantor, grantee, 'CATALOG' AS object_type, catalog_name, NULL AS schema_name, NULL AS object_name, privilege_type, is_grantable, inherited_from
FROM migration_dev.information_schema.catalog_privileges

UNION ALL

SELECT grantor, grantee, 'SCHEMA', catalog_name, schema_name, NULL, privilege_type, is_grantable, inherited_from
FROM migration_dev.information_schema.schema_privileges

UNION ALL

SELECT grantor, grantee, 'TABLE', table_catalog, table_schema, table_name, privilege_type, is_grantable, inherited_from
FROM migration_dev.information_schema.table_privileges

UNION ALL

SELECT grantor, grantee, 'VOLUME', volume_catalog, volume_schema, volume_name, privilege_type, is_grantable, inherited_from
FROM migration_dev.information_schema.volume_privileges

ORDER BY schema_name NULLS FIRST, object_type, object_name, grantee;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Consumer Integration

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 1. BI Query Performance Monitoring
-- MAGIC
-- MAGIC Use `system.query.history` to measure warehouse query latency and track active user growth week-over-week.

-- COMMAND ----------

-- DBTITLE 1,Monitor BI query performance against SLA targets (SQL)
-- Identify queries exceeding latency thresholds
SELECT 
    executed_by,
    compute.warehouse_id AS warehouse_id,
    COUNT(*) AS query_count,
    ROUND(AVG(total_duration_ms) / 1000, 2) AS avg_latency_sec,
    ROUND(PERCENTILE(total_duration_ms, 0.95) / 1000, 2) AS p95_latency_sec,
    SUM(CASE WHEN total_duration_ms > 30000 THEN 1 ELSE 0 END) AS queries_over_30s
FROM system.query.history
WHERE start_time >= CURRENT_DATE - INTERVAL 7 DAYS
  AND statement_type = 'SELECT'
  AND compute.warehouse_id IS NOT NULL
GROUP BY executed_by, compute.warehouse_id
HAVING COUNT(*) > 10
ORDER BY avg_latency_sec DESC;

-- COMMAND ----------

-- DBTITLE 1,Monitor platform adoption metrics (SQL)
-- Track user growth and query patterns over time
SELECT 
    DATE_TRUNC('week', start_time) AS week,
    COUNT(DISTINCT executed_by) AS unique_users,
    COUNT(*) AS total_queries,
    ROUND(AVG(total_duration_ms) / 1000, 2) AS avg_query_duration_sec
FROM system.query.history
WHERE start_time >= CURRENT_DATE - INTERVAL 90 DAYS
  AND statement_type IN ('SELECT', 'SHOW', 'DESCRIBE')
GROUP BY DATE_TRUNC('week', start_time)
ORDER BY week DESC;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
