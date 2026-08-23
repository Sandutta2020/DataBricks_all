-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">04 - Activate</span>
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

-- MAGIC %md-sandbox
-- MAGIC # Demo: Activation Phase
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this demo, you will be able to:
-- MAGIC - Validate migrated data
-- MAGIC - Use common data testing frameworks
-- MAGIC - Get usage and billing information
-- MAGIC - Monitor jobs and pipelines
-- MAGIC - Validate cutover execution

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
-- MAGIC ## Testing and Data Validation

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Row Count Extraction
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Detailed count for a schema</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC SELECT
-- MAGIC     owner AS schema_name,
-- MAGIC     table_name,
-- MAGIC     num_rows,
-- MAGIC     last_analyzed
-- MAGIC FROM ALL_TABLES
-- MAGIC WHERE owner = 'HR'
-- MAGIC ORDER BY num_rows DESC;
-- MAGIC </div>
-- MAGIC </details>
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Detailed count for specific table</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Detailed count for specific table
-- MAGIC SELECT COUNT(*) AS total_rows
-- MAGIC FROM HR.DEPARTMENTS;
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Export row counts (Autonomous Database)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Note: num_rows relies on DBMS_STATS and may be stale. Exact COUNT(*) validation is recommended during freeze.
-- MAGIC -- Export row counts to Object Storage as Parquet using DBMS_CLOUD
-- MAGIC BEGIN
-- MAGIC   DBMS_CLOUD.EXPORT_DATA(
-- MAGIC     credential_name => 'DEF_CRED_NAME',
-- MAGIC     file_uri_list   => 'some-bucket-url',
-- MAGIC     format          => json_object('type' value 'parquet'),
-- MAGIC     query           => 'SELECT owner AS schema_name, table_name, num_rows, last_analyzed, SYSTIMESTAMP AS extracted_at FROM ALL_TABLES WHERE owner = ''HR'''
-- MAGIC   );
-- MAGIC END;
-- MAGIC /
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
-- MAGIC
-- MAGIC <script>
-- MAGIC (function() {
-- MAGIC     function processCodeBlocks() {
-- MAGIC         document.querySelectorAll('.code-block').forEach(function(block) {
-- MAGIC             if (block.getAttribute('data-processed')) return;
-- MAGIC             block.setAttribute('data-processed', 'true');
-- MAGIC             var lang = block.getAttribute('data-language') || 'sql';
-- MAGIC             var code = block.textContent.trim();
-- MAGIC             var id = 'code-' + Math.random().toString(36).substr(2, 9);
-- MAGIC             block.innerHTML = 
-- MAGIC                 '<div style="position:relative;margin:16px 0;">' +
-- MAGIC                     '<button class="copy-btn" style="position:absolute;top:8px;right:8px;padding:4px 12px;font-size:12px;background:#ddd;color:#333;border:1px solid #ccc;border-radius:4px;cursor:pointer;z-index:10;">Copy</button>' +
-- MAGIC                     '<pre style="background:#f8f8f8;border-radius:8px;padding:16px;padding-top:40px;overflow-x:auto;margin:0;border:1px solid #e0e0e0;"><code id="' + id + '" class="language-' + lang + '" style="font-family:Consolas,Monaco,monospace;font-size:14px;"></code></pre>' +
-- MAGIC                 '</div>';
-- MAGIC             var codeEl = document.getElementById(id);
-- MAGIC             codeEl.textContent = code;
-- MAGIC             Prism.highlightElement(codeEl);
-- MAGIC             block.querySelector('.copy-btn').onclick = function() {
-- MAGIC                 var t = document.createElement('textarea');
-- MAGIC                 t.value = code;
-- MAGIC                 document.body.appendChild(t);
-- MAGIC                 t.select();
-- MAGIC                 document.execCommand('copy');
-- MAGIC                 document.body.removeChild(t);
-- MAGIC                 this.textContent = '✓ Copied!';
-- MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
-- MAGIC             };
-- MAGIC         });
-- MAGIC     }
-- MAGIC     processCodeBlocks();
-- MAGIC     document.querySelectorAll('details').forEach(function(details) {
-- MAGIC         details.addEventListener('toggle', processCodeBlocks);
-- MAGIC     });
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- DBTITLE 1,Load baseline (SQL)
-- Compare row counts directly via Lakehouse Federation (no export needed)
-- This avoids the need to export and stage row-count files from Oracle
CREATE OR REPLACE TEMP VIEW oracle_baseline AS
SELECT 'EMPLOYEES'    AS table_name, COUNT(*) AS row_count FROM oracle_federation_catalog.hr.employees
UNION ALL
SELECT 'DEPARTMENTS',               COUNT(*)              FROM oracle_federation_catalog.hr.departments
UNION ALL
SELECT 'JOBS',                      COUNT(*)              FROM oracle_federation_catalog.hr.jobs
UNION ALL
SELECT 'JOB_HISTORY',               COUNT(*)              FROM oracle_federation_catalog.hr.job_history
UNION ALL
SELECT 'LOCATIONS',                 COUNT(*)              FROM oracle_federation_catalog.hr.locations
UNION ALL
SELECT 'COUNTRIES',                 COUNT(*)              FROM oracle_federation_catalog.hr.countries
UNION ALL
SELECT 'REGIONS',                   COUNT(*)              FROM oracle_federation_catalog.hr.regions;

-- COMMAND ----------

-- DBTITLE 1,Compare Against Oracle Baseline (SQL)
-- Compare all tables against the oracle baseline
SELECT 
    b.table_name,
    b.row_count       AS oracle_count,
    d.databricks_count,
    d.databricks_count - b.row_count AS difference,
    CASE WHEN d.databricks_count = b.row_count THEN '✓' ELSE '✗' END AS status
FROM oracle_baseline b
JOIN (
    SELECT 'EMPLOYEES'    AS table_name, COUNT(*) AS databricks_count FROM migration_dev.hr_raw.employees
    UNION ALL
    SELECT 'DEPARTMENTS',               COUNT(*)                      FROM migration_dev.hr_raw.departments
    UNION ALL
    SELECT 'JOBS',                      COUNT(*)                      FROM migration_dev.hr_raw.jobs
    UNION ALL
    SELECT 'JOB_HISTORY',               COUNT(*)                      FROM migration_dev.hr_raw.job_history
    UNION ALL
    SELECT 'LOCATIONS',                 COUNT(*)                      FROM migration_dev.hr_raw.locations
    UNION ALL
    SELECT 'COUNTRIES',                 COUNT(*)                      FROM migration_dev.hr_raw.countries
    UNION ALL
    SELECT 'REGIONS',                   COUNT(*)                      FROM migration_dev.hr_raw.regions
) d ON b.table_name = d.table_name
ORDER BY table_name;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Aggregation Validation

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Extract aggregation baselines</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Aggregation baseline for employees
-- MAGIC SELECT 
-- MAGIC     'employees' AS table_name,
-- MAGIC     COUNT(*) AS row_count,
-- MAGIC     SUM(salary) AS sum_salary,
-- MAGIC     AVG(salary) AS avg_salary,
-- MAGIC     MIN(salary) AS min_salary,
-- MAGIC     MAX(salary) AS max_salary,
-- MAGIC     STDDEV(salary) AS stddev_salary,
-- MAGIC     COUNT(commission_pct) AS non_null_commission
-- MAGIC FROM HR.EMPLOYEES;
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Null count validation</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Null count validation
-- MAGIC SELECT 
-- MAGIC     COUNT(*) AS total_rows,
-- MAGIC     COUNT(manager_id) AS non_null_manager_id,
-- MAGIC     COUNT(*) - COUNT(manager_id) AS null_manager_id,
-- MAGIC     COUNT(commission_pct) AS non_null_commission_pct,
-- MAGIC     COUNT(*) - COUNT(commission_pct) AS null_commission_pct
-- MAGIC FROM HR.EMPLOYEES;
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #009688; background: #e0f2f1; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">💡</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #00695c; font-size: 1.1em;">Export for Comparison</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">With Lakehouse Federation, these aggregate baselines can be queried directly from Databricks without exporting. Use <code>SELECT ... FROM oracle_federation_catalog.hr.employees</code> to run the same queries and compare inline.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #F57C00; background: #FFF3E0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #E65100; font-size: 1.1em;">Oracle NUMBER vs Delta DECIMAL — Expect Small Aggregate Differences</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Oracle <code>NUMBER</code> has arbitrary precision; Delta stores numeric columns as <code>DECIMAL(38, N)</code>. Across hundreds of millions of rows, SUM/AVG comparisons will often show tiny rounding differences — this is expected and not a data loss issue. Set a tolerance threshold (e.g. &lt; 0.01% relative difference) rather than requiring exact equality for aggregate checks.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
-- MAGIC
-- MAGIC <script>
-- MAGIC (function() {
-- MAGIC     function processCodeBlocks() {
-- MAGIC         document.querySelectorAll('.code-block').forEach(function(block) {
-- MAGIC             if (block.getAttribute('data-processed')) return;
-- MAGIC             block.setAttribute('data-processed', 'true');
-- MAGIC             var lang = block.getAttribute('data-language') || 'sql';
-- MAGIC             var code = block.textContent.trim();
-- MAGIC             var id = 'code-' + Math.random().toString(36).substr(2, 9);
-- MAGIC             block.innerHTML = 
-- MAGIC                 '<div style="position:relative;margin:16px 0;">' +
-- MAGIC                     '<button class="copy-btn" style="position:absolute;top:8px;right:8px;padding:4px 12px;font-size:12px;background:#ddd;color:#333;border:1px solid #ccc;border-radius:4px;cursor:pointer;z-index:10;">Copy</button>' +
-- MAGIC                     '<pre style="background:#f8f8f8;border-radius:8px;padding:16px;padding-top:40px;overflow-x:auto;margin:0;border:1px solid #e0e0e0;"><code id="' + id + '" class="language-' + lang + '" style="font-family:Consolas,Monaco,monospace;font-size:14px;"></code></pre>' +
-- MAGIC                 '</div>';
-- MAGIC             var codeEl = document.getElementById(id);
-- MAGIC             codeEl.textContent = code;
-- MAGIC             Prism.highlightElement(codeEl);
-- MAGIC             block.querySelector('.copy-btn').onclick = function() {
-- MAGIC                 var t = document.createElement('textarea');
-- MAGIC                 t.value = code;
-- MAGIC                 document.body.appendChild(t);
-- MAGIC                 t.select();
-- MAGIC                 document.execCommand('copy');
-- MAGIC                 document.body.removeChild(t);
-- MAGIC                 this.textContent = '✓ Copied!';
-- MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
-- MAGIC             };
-- MAGIC         });
-- MAGIC     }
-- MAGIC     processCodeBlocks();
-- MAGIC     document.querySelectorAll('details').forEach(function(details) {
-- MAGIC         details.addEventListener('toggle', processCodeBlocks);
-- MAGIC     });
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- DBTITLE 1,Aggregation Validation (SQL)
-- Collect table aggregates for validation
SELECT 
    'employees' AS table_name,
    COUNT(*) AS row_count,
    ROUND(SUM(salary), 2) AS sum_salary,
    ROUND(AVG(salary), 4) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    ROUND(STDDEV(salary), 4) AS stddev_salary,
    COUNT(commission_pct) AS non_null_commission
FROM migration_dev.hr_raw.employees;

-- COMMAND ----------

-- DBTITLE 1,Null Count Validation (SQL)
-- Validate NULLs
SELECT 
    COUNT(*) AS total_rows,
    COUNT(manager_id) AS non_null_manager_id,
    COUNT(*) - COUNT(manager_id) AS null_manager_id,
    COUNT(commission_pct) AS non_null_commission_pct,
    COUNT(*) - COUNT(commission_pct) AS null_commission_pct,
    -- Validate nullable columns didn't lose data
    ROUND(100.0 * COUNT(manager_id) / COUNT(*), 2) AS pct_manager_populated
FROM migration_dev.hr_raw.employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Testing Frameworks

-- COMMAND ----------

-- DBTITLE 1,Test Data Setup (Python)
-- MAGIC %python
-- MAGIC from pyspark.sql.types import StructType, StructField, StringType, DecimalType
-- MAGIC from decimal import Decimal
-- MAGIC
-- MAGIC # Schema matching actual employees table types
-- MAGIC expected_schema = StructType([
-- MAGIC     StructField("employee_id",  DecimalType(6, 0),  False),
-- MAGIC     StructField("first_name",   StringType(),        True),
-- MAGIC     StructField("last_name",    StringType(),        False),
-- MAGIC     StructField("salary",       DecimalType(8, 2),   True),
-- MAGIC     StructField("job_id",       StringType(),        False)
-- MAGIC ])
-- MAGIC
-- MAGIC expected_data = [
-- MAGIC     (Decimal("100"), "Steven",  "King",    Decimal("24000.00"), "AD_PRES"),
-- MAGIC     (Decimal("101"), "Neena",   "Kochhar", Decimal("17000.00"), "AD_VP"),
-- MAGIC     (Decimal("102"), "Lex",     "De Haan", Decimal("17000.00"), "AD_VP")
-- MAGIC ]
-- MAGIC
-- MAGIC expected_df = spark.createDataFrame(expected_data, expected_schema)

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Chispa Example
-- MAGIC
-- MAGIC First, install Chispa, then demonstrate its usage on a small example

-- COMMAND ----------

-- DBTITLE 1,Install Chispa
-- MAGIC %python
-- MAGIC %pip install chispa

-- COMMAND ----------

-- DBTITLE 1,Validate DataFrame with Chispa (Python)
-- MAGIC %python
-- MAGIC from chispa.dataframe_comparer import assert_df_equality
-- MAGIC
-- MAGIC # In practice, load actual_df from the migrated table:
-- MAGIC # actual_df = spark.table("migration_dev.hr_raw.employees").select("employee_id","first_name","last_name","salary","job_id").limit(3)
-- MAGIC actual_df = spark.createDataFrame(expected_data, expected_schema)
-- MAGIC
-- MAGIC # Schema comparison (ignore nullable differences common in migrations)
-- MAGIC try:
-- MAGIC     assert_df_equality(actual_df, expected_df, ignore_nullable=True, ignore_row_order=True)
-- MAGIC     print("✓ DataFrame equality check passed")
-- MAGIC except Exception as e:
-- MAGIC     print(f"✗ DataFrame mismatch:\n{e}")
-- MAGIC
-- MAGIC # Example validation function for pytest integration
-- MAGIC def test_validate_employees_schema():
-- MAGIC     """Validate employees schema matches expected structure."""
-- MAGIC     actual_df = spark.table("migration_dev.hr_raw.employees")
-- MAGIC     expected_columns = {"employee_id", "first_name", "last_name", "email",
-- MAGIC                         "hire_date", "salary", "job_id", "department_id"}
-- MAGIC     actual_columns = set(actual_df.columns)
-- MAGIC     missing = expected_columns - actual_columns
-- MAGIC     extra = actual_columns - expected_columns
-- MAGIC     assert len(missing) == 0, f"Missing columns: {missing}"
-- MAGIC     print(f"✓ Schema validation passed. Extra columns (OK): {extra if extra else 'None'}")
-- MAGIC
-- MAGIC test_validate_employees_schema()

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### PySpark Built-In Testing

-- COMMAND ----------

-- DBTITLE 1,Validate DataFrame with Native PySpark (Python)
-- MAGIC %python
-- MAGIC from pyspark.testing import assertDataFrameEqual
-- MAGIC
-- MAGIC # In practice, load actual_df from the migrated table:
-- MAGIC # actual_df = spark.table("migration_dev.hr_raw.employees").select("employee_id","first_name","last_name","salary","job_id").limit(3)
-- MAGIC actual_df = spark.createDataFrame(expected_data, expected_schema)
-- MAGIC
-- MAGIC # DataFrame comparison (PySpark 3.5+)
-- MAGIC try:
-- MAGIC     assertDataFrameEqual(actual_df, expected_df, checkRowOrder=False)
-- MAGIC     print("✓ DataFrame equality check passed")
-- MAGIC except Exception as e:
-- MAGIC     print(f"✗ DataFrame mismatch:\n{e}")
-- MAGIC
-- MAGIC # Example validation function for pytest integration
-- MAGIC def validate_employees_schema():
-- MAGIC     """Validate employees schema matches expected structure."""
-- MAGIC     actual_df = spark.table("migration_dev.hr_raw.employees")
-- MAGIC     expected_columns = {"employee_id", "first_name", "last_name", "email",
-- MAGIC                         "hire_date", "salary", "job_id", "department_id"}
-- MAGIC     actual_columns = set(actual_df.columns)
-- MAGIC     missing = expected_columns - actual_columns
-- MAGIC     extra = actual_columns - expected_columns
-- MAGIC     assert len(missing) == 0, f"Missing columns: {missing}"
-- MAGIC     print(f"✓ Schema validation passed. Extra columns (OK): {extra if extra else 'None'}")
-- MAGIC
-- MAGIC validate_employees_schema()

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Delta Table Constraints
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #1565C0; background: #E3F2FD; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">🔑</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0D47A1; font-size: 1.1em;">PK / FK Enforcement: a key architectural difference</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Delta Lake supports only <strong>CHECK constraints</strong> (enforced on INSERT/UPDATE) and informational <strong>PRIMARY KEY / FOREIGN KEY</strong> declarations (defined but <em>not enforced</em>). Referential integrity that Oracle enforced declaratively must be re-implemented as ETL validation logic — for example, running a LEFT JOIN anti-pattern to detect orphaned rows before a MERGE. Use <code>COUNT(DISTINCT pk_col) = COUNT(*)</code> checks as a post-load substitute for PK uniqueness enforcement.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- DBTITLE 1,Add Constraints (SQL)
-- These are enforced on INSERT and UPDATE operations

-- Constraint: salary must be positive
ALTER TABLE migration_dev.hr_raw.employees
ADD CONSTRAINT salary_positive CHECK (salary IS NULL OR salary > 0);

-- Constraint: hire_date must be within valid range
ALTER TABLE migration_dev.hr_raw.employees
ADD CONSTRAINT hire_date_valid CHECK (hire_date IS NULL OR hire_date >= '1987-01-01');

-- COMMAND ----------

-- DBTITLE 1,Describe Table (SQL)
DESCRIBE DETAIL migration_dev.hr_raw.employees;

-- COMMAND ----------

-- DBTITLE 1,Show Table Properties (SQL)
SHOW TBLPROPERTIES migration_dev.hr_raw.employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Comprehensive Validation Report

-- COMMAND ----------

-- DBTITLE 1,Validation Report (SQL)
-- Comprehensive validation report: Databricks vs Oracle baseline
-- Requires oracle_baseline view from Cell 6 (live row counts via Lakehouse Federation)

WITH databricks_metrics AS (
    SELECT 
        'employees' AS table_name,
        COUNT(*) AS row_count,
        ROUND(SUM(salary), 2) AS sum_numeric,
        COUNT(*) - COUNT(manager_id) AS null_count,
        COUNT(DISTINCT employee_id) AS distinct_pk
    FROM migration_dev.hr_raw.employees
    
    UNION ALL
    
    SELECT 
        'departments' AS table_name,
        COUNT(*) AS row_count,
        NULL AS sum_numeric,
        COUNT(*) - COUNT(manager_id) AS null_count,
        COUNT(DISTINCT department_id) AS distinct_pk
    FROM migration_dev.hr_raw.departments

    -- additional tables added with UNION ALL

)
SELECT 
    d.table_name,
    b.row_count                                            AS oracle_rows,
    d.row_count                                            AS databricks_rows,
    d.row_count - b.row_count                             AS row_diff,
    CASE WHEN d.row_count = b.row_count THEN '✓' ELSE '✗' END AS row_check,
    CASE WHEN d.row_count = d.distinct_pk
         THEN '✓' ELSE '✗ DUPLICATE PKs' END              AS pk_check
FROM databricks_metrics d
LEFT JOIN oracle_baseline b ON UPPER(d.table_name) = b.table_name
ORDER BY d.table_name;

-- COMMAND ----------

-- DBTITLE 1,Validation Template (Python)
-- MAGIC %python
-- MAGIC # Template for side-by-side Oracle vs Databricks validation
-- MAGIC # Populate oracle_baselines from oracle_baseline temp view (or run inline via federation)
-- MAGIC
-- MAGIC oracle_baselines = {
-- MAGIC     "employees": {
-- MAGIC         "row_count": 107,              # from oracle_federation_catalog.hr.employees
-- MAGIC         "sum_salary": 691416.00,       # SUM(salary) from Oracle
-- MAGIC         "null_manager_id": 1,          # CEO has no manager
-- MAGIC         "distinct_employee_id": 107
-- MAGIC     },
-- MAGIC     # additional tables
-- MAGIC }
-- MAGIC
-- MAGIC TOLERANCE_PCT = 0.01  # Accept up to 0.01% relative difference in aggregates
-- MAGIC                       # due to Oracle NUMBER -> DECIMAL(38,N) precision change
-- MAGIC
-- MAGIC def compare_table(table_name: str, baselines: dict):
-- MAGIC     """Compare Databricks table against Oracle baselines."""
-- MAGIC     from pyspark.sql import functions as F
-- MAGIC     df = spark.table(f"migration_dev.hr_raw.{table_name}")
-- MAGIC
-- MAGIC     db_row_count = df.count()
-- MAGIC     oracle_row_count = baselines.get("row_count")
-- MAGIC
-- MAGIC     if oracle_row_count is not None:
-- MAGIC         row_diff = db_row_count - oracle_row_count
-- MAGIC         row_ok = row_diff == 0
-- MAGIC         print(f"{table_name}:")
-- MAGIC         print(f"  Oracle rows:     {oracle_row_count:,}")
-- MAGIC         print(f"  Databricks rows: {db_row_count:,}")
-- MAGIC         print(f"  Row check:       {'✓ MATCH' if row_ok else f'✗ DIFF: {row_diff:+d}'}")
-- MAGIC     else:
-- MAGIC         print(f"{table_name}: Oracle baseline not populated")
-- MAGIC         return
-- MAGIC
-- MAGIC     # Aggregate comparison with tolerance
-- MAGIC     oracle_sum = baselines.get("sum_salary")
-- MAGIC     if oracle_sum:
-- MAGIC         db_sum = df.agg(F.round(F.sum("salary"), 2)).collect()[0][0]
-- MAGIC         rel_diff_pct = abs(float(db_sum or 0) - oracle_sum) / abs(oracle_sum) * 100
-- MAGIC         agg_ok = rel_diff_pct < TOLERANCE_PCT
-- MAGIC         print(f"  Oracle sum:      {oracle_sum:,.2f}")
-- MAGIC         print(f"  Databricks sum:  {db_sum:,.2f}")
-- MAGIC         print(f"  Sum diff:        {rel_diff_pct:.6f}% ({'✓' if agg_ok else '✗ EXCEEDS TOLERANCE'})")
-- MAGIC
-- MAGIC # Run comparison (populate baselines first, or query oracle_baseline view)
-- MAGIC compare_table("employees", oracle_baselines.get("employees", {}))

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Observability and Monitoring

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Monitoring Job Execution

-- COMMAND ----------

-- DBTITLE 1,Gather Job Metrics (SQL)
-- Compare against Oracle DBA_SCHEDULER_JOB_RUN_DETAILS baseline metrics
SELECT 
    j.name AS job_name,
    jrt.run_id,
    jrt.result_state AS result,
    jrt.run_type,
    jrt.trigger_type,
    jrt.period_start_time AS start_time,
    jrt.period_end_time AS end_time,
    jrt.run_duration_seconds AS duration_seconds,
    jrt.termination_code
FROM system.lakeflow.job_run_timeline jrt
JOIN system.lakeflow.jobs j ON jrt.job_id = j.job_id
WHERE jrt.period_start_time >= current_date() - INTERVAL 30 DAYS
ORDER BY jrt.period_start_time DESC
LIMIT 50;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC The next query aggregates per-run details into job-level success/failure totals — matching the rollup format of Oracle's `DBA_SCHEDULER_JOB_RUN_DETAILS`.

-- COMMAND ----------

-- DBTITLE 1,Gather Job Metrics II (SQL)
-- Aggregates match Oracle scheduler job metrics format
SELECT 
    j.name AS job_name,
    COUNT(DISTINCT jrt.run_id) AS total_runs,
    SUM(CASE WHEN jrt.result_state = 'SUCCESS' THEN 1 ELSE 0 END) AS successful_runs,
    SUM(CASE WHEN jrt.result_state = 'FAILED' THEN 1 ELSE 0 END) AS failed_runs,
    ROUND(100.0 * SUM(CASE WHEN jrt.result_state = 'SUCCESS' THEN 1 ELSE 0 END) / NULLIF(COUNT(DISTINCT jrt.run_id), 0), 2) AS success_rate_pct,
    ROUND(AVG(TIMESTAMPDIFF(SECOND, jrt.period_start_time, jrt.period_end_time)), 2) AS avg_duration_seconds,
    MIN(TIMESTAMPDIFF(SECOND, jrt.period_start_time, jrt.period_end_time)) AS min_duration_seconds,
    MAX(TIMESTAMPDIFF(SECOND, jrt.period_start_time, jrt.period_end_time)) AS max_duration_seconds
FROM system.lakeflow.job_run_timeline jrt
JOIN system.lakeflow.jobs j ON jrt.job_id = j.job_id
WHERE jrt.period_start_time >= current_date() - INTERVAL 30 DAYS
  AND jrt.result_state IS NOT NULL
GROUP BY j.name
ORDER BY total_runs DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Data Lineage Monitoring

-- COMMAND ----------

-- DBTITLE 1,Find Upstream and Downstream Dependencies (SQL)
-- Identifies upstream and downstream dependencies
SELECT 
    source_table_full_name,
    target_table_full_name,
    entity_type,
    entity_id,
    event_time,
    event_date
FROM system.access.table_lineage
WHERE (
    source_table_full_name LIKE 'migration_dev.hr%'
    OR target_table_full_name LIKE 'migration_dev.hr%'
)
AND event_date >= current_date() - INTERVAL 7 DAYS
ORDER BY event_time DESC
LIMIT 50;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Usage Monitoring

-- COMMAND ----------

-- DBTITLE 1,Find Most Frequently Accessed Tables (SQL)
-- Identify most frequently accessed tables (helps prioritize cutover)
-- Using audit logs for comprehensive access tracking

SELECT 
    request_params.full_name_arg AS table_name,
    COUNT(*) AS access_count,
    COUNT(DISTINCT user_identity.email) AS unique_users,
    COUNT(DISTINCT source_ip_address) AS unique_sources,
    SUM(CASE WHEN action_name = 'getTable' THEN 1 ELSE 0 END) AS metadata_reads,
    SUM(CASE WHEN action_name = 'commandSubmit' THEN 1 ELSE 0 END) AS query_executions
FROM system.access.audit
WHERE request_params.full_name_arg LIKE 'migration_dev.hr%'
  AND event_date >= current_date() - INTERVAL 30 DAYS
  AND action_name IN ('getTable', 'commandSubmit', 'generateTemporaryTableCredential')
GROUP BY request_params.full_name_arg
ORDER BY access_count DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Billing Monitoring and Cost Optimization

-- COMMAND ----------

-- DBTITLE 1,Daily Usage Summary by SKU (SQL)
SELECT 
    usage_date,
    sku_name,
    billing_origin_product,
    usage_unit,
    SUM(usage_quantity) AS total_usage
FROM system.billing.usage
WHERE usage_date >= current_date() - INTERVAL 30 DAYS
GROUP BY usage_date, sku_name, billing_origin_product, usage_unit
ORDER BY usage_date DESC, total_usage DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Break down DBU consumption by job to identify the most resource-intensive migrated pipelines and target them for optimization.

-- COMMAND ----------

-- DBTITLE 1,Usage Attributed to Jobs (SQL)
SELECT 
    usage_date,
    usage_metadata.job_name AS job_name,
    usage_metadata.job_id AS job_id,
    sku_name,
    SUM(usage_quantity) AS total_dbus
FROM system.billing.usage
WHERE usage_metadata.job_id IS NOT NULL
  AND usage_date >= current_date() - INTERVAL 90 DAYS
GROUP BY usage_date, usage_metadata.job_name, usage_metadata.job_id, sku_name
ORDER BY total_dbus DESC;


-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Extracting Monitoring Baselines from Oracle
-- MAGIC
-- MAGIC Extract important performance baselines for SLA comparison between the two platforms. This is possible through Lakehouse Federation, as well.

-- COMMAND ----------

-- DBTITLE 1,Query Performance Baselines (SQL)
SELECT 
    parsing_schema_name,
    module,
    COUNT(*) AS query_count,
    AVG(elapsed_time_delta) / 1000000 AS avg_duration_seconds,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY elapsed_time_delta) / 1000000 AS p50_seconds,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY elapsed_time_delta) / 1000000 AS p95_seconds,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY elapsed_time_delta) / 1000000 AS p99_seconds,
    AVG(physical_read_bytes_delta) / (1024*1024*1024) AS avg_gb_scanned
FROM oracle_federation_catalog.sys.DBA_HIST_SQLSTAT
JOIN oracle_federation_catalog.sys.DBA_HIST_SNAPSHOT s ON DBA_HIST_SQLSTAT.snap_id = s.snap_id
WHERE s.begin_interval_time >= now() - INTERVAL 30 DAYS
  AND parsing_schema_name = 'HR'
GROUP BY parsing_schema_name, module
ORDER BY query_count DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Extract Oracle Scheduler job duration statistics to establish the execution-time baseline for post-migration SLA comparison.

-- COMMAND ----------

-- DBTITLE 1,Job Execution Baselines (SQL)
SELECT 
    job_name,
    owner AS schema_name,
    COUNT(*) AS execution_count,
    AVG(EXTRACT(DAY FROM run_duration) * 86400 + EXTRACT(HOUR FROM run_duration) * 3600 + EXTRACT(MINUTE FROM run_duration) * 60 + EXTRACT(SECOND FROM run_duration)) AS avg_duration_seconds,
    SUM(CASE WHEN status = 'SUCCEEDED' THEN 1 ELSE 0 END) AS success_count,
    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS failure_count
FROM oracle_federation_catalog.sys.DBA_SCHEDULER_JOB_RUN_DETAILS
WHERE log_date >= now() - INTERVAL 30 DAYS
  AND owner = 'HR'
GROUP BY job_name, owner
ORDER BY execution_count DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Building Operational Dashboards

-- COMMAND ----------

-- DBTITLE 1,Example Migration Validation Coverage Dashboard Metrics (SQL)
WITH row_counts AS (
    SELECT 'employees'   AS table_name, COUNT(*) AS row_count FROM migration_dev.hr_raw.employees
    UNION ALL
    SELECT 'departments',               COUNT(*)              FROM migration_dev.hr_raw.departments
    UNION ALL
    SELECT 'jobs',                      COUNT(*)              FROM migration_dev.hr_raw.jobs
)
SELECT
    t.table_name,
    rc.row_count,
    t.last_altered AS last_updated,
    CASE
        WHEN t.last_altered >= current_timestamp() - INTERVAL 24 HOURS THEN 'FRESH'
        WHEN t.last_altered >= current_timestamp() - INTERVAL 7 DAYS  THEN 'STALE'
        ELSE 'OUTDATED'
    END AS freshness_status
FROM migration_dev.information_schema.tables t
JOIN row_counts rc ON t.table_name = rc.table_name
WHERE t.table_schema = 'hr_raw'
ORDER BY t.table_name;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Performance Tuning Before Cutover

-- COMMAND ----------

-- DBTITLE 1,Enable Liquid Clustering on frequently filtered tables (SQL)
-- Cluster employees by hire_date and department_id (common filter columns)
-- Already done on setup
-- ALTER TABLE migration_dev.hr_raw.employees
-- CLUSTER BY (hire_date, department_id);

-- View clustering status
DESCRIBE DETAIL migration_dev.hr_raw.employees;

-- COMMAND ----------

-- DBTITLE 1,Run OPTIMIZE to compact small files and apply clustering (SQL)
OPTIMIZE migration_dev.hr_raw.employees;

-- Verify file compaction
DESCRIBE HISTORY migration_dev.hr_raw.employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### When to Run ANALYZE Manually
-- MAGIC
-- MAGIC If **Predictive Optimization** is enabled on the catalog, it runs `ANALYZE`, `OPTIMIZE`, and `VACUUM` automatically — running them manually here is redundant during normal operations. Run manually when:
-- MAGIC - You need statistics immediately after a bulk load (before the next Predictive Optimization cycle)
-- MAGIC - The table is excluded from Predictive Optimization (e.g. external tables)
-- MAGIC - You are benchmarking query plans and need up-to-date stats right now
-- MAGIC
-- MAGIC Check whether Predictive Optimization is active on your catalog before scheduling explicit `ANALYZE` jobs.

-- COMMAND ----------

-- DBTITLE 1,Compute table statistics for query optimization (SQL)
ANALYZE TABLE migration_dev.hr_raw.employees COMPUTE STATISTICS FOR ALL COLUMNS;
ANALYZE TABLE migration_dev.hr_raw.departments COMPUTE STATISTICS FOR ALL COLUMNS;

-- COMMAND ----------

-- DBTITLE 1,Check predictive optimization history (SQL)
SELECT 
    table_name,
    operation_type,
    operation_status,
    operation_metrics,
    start_time,
    end_time,
    TIMESTAMPDIFF(SECOND, start_time, end_time) AS duration_seconds
FROM system.storage.predictive_optimization_operations_history
WHERE table_name LIKE '%hr_%'
  AND start_time >= current_date() - INTERVAL 90 DAYS
ORDER BY start_time DESC
LIMIT 20;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Cutover Execution

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Delta Catch-Up Synchronization

-- COMMAND ----------

-- DBTITLE 1,Verify Last Sync Timestamp Before Catch-Up (SQL)
-- Check latest hire_date loaded and current row count as a data-driven sync baseline
SELECT 
    'employees' AS table_name,
    MAX(hire_date) AS latest_hire_date,
    COUNT(*) AS current_row_count
FROM migration_dev.hr_raw.employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC With the sync baseline confirmed, trigger the final catch-up MERGE to bring Databricks fully in sync with Oracle before cutover.

-- COMMAND ----------

-- DBTITLE 1,Trigger Final Delta Catch-Up (Example Using MERGE) (SQL)
-- Trigger final delta catch-up using Lakehouse Federation as source
-- No separate export or staging step required

-- Option 1: If using Lakeflow Pipeline, trigger update via API or UI

-- Option 2: Manual MERGE for final deltas using Lakehouse Federation
MERGE INTO migration_dev.hr_raw.employees AS target
USING oracle_federation_catalog.hr.employees AS source
ON target.employee_id = source.employee_id
WHEN MATCHED AND (
    source.salary != target.salary OR
    source.job_id != target.job_id OR
    source.department_id != target.department_id
) THEN
    UPDATE SET *
WHEN NOT MATCHED THEN
    INSERT *;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC After the MERGE completes, verify row counts and aggregate sums match Oracle exactly. Both numbers must agree before cutting over consumers.

-- COMMAND ----------

-- DBTITLE 1,Final Reconciliation Check After Delta Catch-Up (SQL)
-- These counts should match Oracle exactly after catch-up
WITH databricks_counts AS (
    SELECT 
        'employees' AS table_name,
        COUNT(*) AS row_count,
        ROUND(SUM(salary), 2) AS sum_salary
    FROM migration_dev.hr_raw.employees
    UNION ALL
    SELECT 
        'departments' AS table_name,
        COUNT(*) AS row_count,
        NULL AS sum_salary
    FROM migration_dev.hr_raw.departments
),
oracle_counts AS (
    SELECT 
        'employees' AS table_name,
        COUNT(*) AS row_count,
        ROUND(SUM(salary), 2) AS sum_salary
    FROM oracle_federation_catalog.hr.employees
    UNION ALL
    SELECT 
        'departments' AS table_name,
        COUNT(*) AS row_count,
        NULL AS sum_salary
    FROM oracle_federation_catalog.hr.departments
)
SELECT 
    d.table_name,
    d.row_count AS databricks_count,
    o.row_count AS oracle_count,
    d.sum_salary AS databricks_sum_salary,
    o.sum_salary AS oracle_sum_salary,
    d.row_count - o.row_count AS row_diff,
    CASE WHEN d.row_count = o.row_count THEN '✓' ELSE '✗' END AS row_count_match,
    CASE WHEN d.sum_salary = o.sum_salary OR d.sum_salary IS NULL THEN '✓' ELSE '✗' END AS sum_salary_match
FROM databricks_counts d
JOIN oracle_counts o ON d.table_name = o.table_name;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Cutover Checklist
-- MAGIC
-- MAGIC Before declaring cutover complete:
-- MAGIC
-- MAGIC | Step | Check | Owner |
-- MAGIC |------|-------|-------|
-- MAGIC | Row counts match Oracle exactly | Run reconciliation query above | Data Eng |
-- MAGIC | Aggregate sums within tolerance (< 0.01%) | Run `compare_table()` for all tables | Data Eng |
-- MAGIC | Identity/sequence high watermarks advanced | Verify via `DESCRIBE DETAIL` | DBA |
-- MAGIC | Downstream connections re-pointed | JDBC URLs, DSNs, service accounts updated | App Team |
-- MAGIC | Oracle jobs frozen / scheduler disabled | Confirm no new writes to Oracle source | DBA |
-- MAGIC | Rollback decision point agreed | Define max acceptable downtime window; keep Oracle read-only for N days | Mgmt |
-- MAGIC
-- MAGIC **Rollback procedure:** If critical validation fails post-cutover, re-enable Oracle as primary and replay any Databricks writes back using the Delta change data feed (`table_changes()`) before cutting over again.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Post-Cutover Validation

-- COMMAND ----------

-- DBTITLE 1,Post-Cutover Dashboard Validation Queries (SQL)
-- Run these against Databricks and compare with expected results
-- Salary distribution by department and location (common dashboard metric)
SELECT 
    d.department_name,
    l.city,
    l.country_id,
    COUNT(e.employee_id) AS employee_count,
    ROUND(SUM(e.salary), 2)   AS total_salary,
    ROUND(AVG(e.salary), 2)   AS avg_salary,
    MIN(e.salary)             AS min_salary,
    MAX(e.salary)             AS max_salary
FROM migration_dev.hr_raw.employees e
JOIN migration_dev.hr_raw.departments d ON e.department_id = d.department_id
JOIN migration_dev.hr_raw.locations l   ON d.location_id   = l.location_id
GROUP BY d.department_name, l.city, l.country_id
ORDER BY total_salary DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Verify the monthly headcount and salary report matches the Oracle output — a common business report used for cutover acceptance sign-off.

-- COMMAND ----------

-- DBTITLE 1,Validate Scheduled Report Query (SQL)
-- This should match the Oracle report output
-- Monthly headcount and salary report by job
SELECT 
    j.job_title,
    COUNT(e.employee_id)        AS headcount,
    ROUND(AVG(e.salary), 2)    AS avg_salary,
    MIN(e.salary)              AS min_salary,
    MAX(e.salary)              AS max_salary,
    ROUND(
        100.0 * COUNT(e.employee_id)
        / SUM(COUNT(e.employee_id)) OVER (), 2
    ) AS pct_headcount
FROM migration_dev.hr_raw.employees e
JOIN migration_dev.hr_raw.jobs j ON e.job_id = j.job_id
GROUP BY j.job_title
ORDER BY headcount DESC;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
