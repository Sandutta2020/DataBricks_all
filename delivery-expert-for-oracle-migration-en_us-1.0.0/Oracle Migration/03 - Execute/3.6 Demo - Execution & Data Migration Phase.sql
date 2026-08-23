-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">03 - Execute</span>
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
-- MAGIC # Demo: Execution & Data Migration Phase
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this demo, you will be able to:
-- MAGIC - Convert the schema of Oracle tables to Databricks, including all seven HR tables with accurate type mapping and constraints
-- MAGIC - Load data using three complementary ingestion methods: COPY INTO, Auto Loader, and Lakehouse Federation
-- MAGIC - Apply incremental CDC patterns using Auto Loader with MERGE and Change Data Feed
-- MAGIC - Convert PL/SQL code, triggers, and functions to Databricks SQL and Python

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

-- DBTITLE 1,Set Default Catalog and Schema (SQL)
USE CATALOG migration_dev;
USE SCHEMA hr_raw;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Schema and DDL conversion

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### DDL Extraction Workflow
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Extract Schema Metadata using Data Dictionary Views</summary>
-- MAGIC
-- MAGIC Use **Oracle data dictionary views** to extract table and column metadata for programmatic DDL conversion.
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Extract table metadata from Oracle data dictionary
-- MAGIC -- Run in Oracle worksheet
-- MAGIC <br/>
-- MAGIC -- List all tables in a schema with row counts and approximate sizes
-- MAGIC SELECT
-- MAGIC     owner AS schema_name,
-- MAGIC     table_name,
-- MAGIC     num_rows AS row_count,
-- MAGIC     blocks * 8 * 1024 AS size_bytes,
-- MAGIC     last_analyzed
-- MAGIC FROM ALL_TABLES
-- MAGIC WHERE owner = 'HR' -- Replace with your schema name
-- MAGIC ORDER BY table_name;
-- MAGIC <br/>
-- MAGIC -- Extract column details for DDL generation
-- MAGIC SELECT
-- MAGIC     owner AS schema_name,
-- MAGIC     table_name,
-- MAGIC     column_name,
-- MAGIC     column_id AS ordinal_position,
-- MAGIC     data_type,
-- MAGIC     data_length,
-- MAGIC     data_precision,
-- MAGIC     data_scale,
-- MAGIC     nullable
-- MAGIC FROM ALL_TAB_COLUMNS
-- MAGIC WHERE owner = 'HR' -- Replace with your schema name
-- MAGIC ORDER BY table_name, column_id;
-- MAGIC <br/>
-- MAGIC -- Query constraint metadata from Oracle data dictionary
-- MAGIC SELECT
-- MAGIC     constraint_name,
-- MAGIC     table_name,
-- MAGIC     constraint_type,
-- MAGIC     status
-- MAGIC FROM all_constraints
-- MAGIC WHERE owner = 'HR' -- Replace with your schema name
-- MAGIC AND table_name = 'EMPLOYEES'
-- MAGIC ORDER BY constraint_type;
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Extract DDL using DBMS_METADATA.GET_DDL</summary>
-- MAGIC
-- MAGIC Use the `DBMS_METADATA.GET_DDL` function to extract complete DDL statements directly from Oracle objects.
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Extract DDL for a single table
-- MAGIC SELECT DBMS_METADATA.GET_DDL('TABLE', 'EMPLOYEES', 'HR') -- Replace with your schema name
-- MAGIC FROM dual;
-- MAGIC <br/>
-- MAGIC -- Extract DDL for all tables in a schema
-- MAGIC SELECT DBMS_METADATA.GET_DDL('TABLE', table_name, owner)
-- MAGIC FROM ALL_TABLES
-- MAGIC WHERE owner = 'HR'; -- Replace with your schema name
-- MAGIC <br/>
-- MAGIC -- Extract DDL for views in a schema
-- MAGIC SELECT DBMS_METADATA.GET_DDL('VIEW', view_name, owner)
-- MAGIC FROM all_views
-- MAGIC WHERE owner = 'HR'; -- Replace with your schema name
-- MAGIC <br/>
-- MAGIC -- Extract DDL for stored procedures and functions
-- MAGIC SELECT DBMS_METADATA.GET_DDL(object_type, object_name, owner)
-- MAGIC FROM all_objects
-- MAGIC WHERE owner = 'HR' -- Replace with your schema name
-- MAGIC AND object_type IN ('FUNCTION','PROCEDURE');
-- MAGIC </div>
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 12px 16px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 10px;">
-- MAGIC         <span style="font-size: 20px;">ℹ️</span>
-- MAGIC         <div style="font-size: 14px;">
-- MAGIC             <strong style="color: #0d47a1;">DBMS_METADATA.GET_DDL() Output Notes:</strong> The output includes Oracle-specific syntax (e.g., <code>NUMBER</code>, <code>VARCHAR2</code>, <code>DATE</code>) that requires conversion for Databricks. Use the datatype mapping reference to transform these statements.
-- MAGIC         </div>
-- MAGIC     </div>
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

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC ### Lakebridge DDL Transpilation
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Lakebridge Installation and Commands</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="bash">
-- MAGIC # Install Lakebridge (part of Databricks Labs)
-- MAGIC databricks labs install lakebridge
-- MAGIC <br/>
-- MAGIC # Install transpilers (interactive - select 'oracle' as source dialect)
-- MAGIC databricks labs lakebridge install-transpile --interactive true
-- MAGIC # Installs: Bladebridge and Morpheus transpilers
-- MAGIC <br/>
-- MAGIC # Verify installed transpilers and supported dialects
-- MAGIC databricks labs lakebridge describe-transpile
-- MAGIC <br/>
-- MAGIC # Transpile Oracle DDL to Databricks SQL
-- MAGIC databricks labs lakebridge transpile \
-- MAGIC   --source-dialect oracle \
-- MAGIC   --input-source ./oracle-export \
-- MAGIC   --output-folder ./databricks_ddl \
-- MAGIC   --error-file-path ./transpile_errors.log
-- MAGIC <br/>
-- MAGIC # Configure and run data reconciliation (compare source vs target) - covered in the VALIDATE phase
-- MAGIC # databricks labs lakebridge configure-reconcile
-- MAGIC # databricks labs lakebridge reconcile
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
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

-- MAGIC %md
-- MAGIC ### Data Type Mapping Overview
-- MAGIC
-- MAGIC All seven Oracle HR tables are recreated here.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: REGIONS (source)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Oracle: HR.REGIONS
-- MAGIC CREATE TABLE "HR"."REGIONS" (
-- MAGIC     "REGION_ID"   NUMBER        CONSTRAINT "REGION_ID_NN" NOT NULL ENABLE,
-- MAGIC     "REGION_NAME" VARCHAR2(25)
-- MAGIC );
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
-- MAGIC                 var t = document.createElement('textarea'); t.value = code;
-- MAGIC                 document.body.appendChild(t); t.select(); document.execCommand('copy');
-- MAGIC                 document.body.removeChild(t);
-- MAGIC                 this.textContent = '✓ Copied!';
-- MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
-- MAGIC             };
-- MAGIC         });
-- MAGIC     }
-- MAGIC     processCodeBlocks();
-- MAGIC     document.querySelectorAll('details').forEach(d => d.addEventListener('toggle', processCodeBlocks));
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- DBTITLE 1,Create Table: hr_raw.regions
-- NUMBER -> INT  |  VARCHAR2(25) -> STRING
CREATE TABLE IF NOT EXISTS migration_dev.hr_raw.regions (
    region_id   INT     NOT NULL,  -- NUMBER NOT NULL
    region_name STRING             -- VARCHAR2(25)
)
COMMENT 'Migrated from Oracle HR.REGIONS';

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Query both `information_schema.columns` and the Oracle data dictionary via federation to validate that every column landed with the expected type, nullability, and position.

-- COMMAND ----------

-- DBTITLE 1,Validate Schema Parity (SQL)
WITH oracle_cols AS (
    SELECT
        UPPER(column_name) AS column_name,
        column_id::int-1         AS ordinal_position, -- Oracle position starts at 1, Databricks at 0
        data_type
            || CASE
                 WHEN data_precision IS NOT NULL
                   THEN '(' || data_precision
                        || CASE WHEN data_scale > 0 THEN ',' || data_scale ELSE '' END
                        || ')'
                 WHEN data_type IN ('VARCHAR2', 'CHAR', 'NVARCHAR2')
                   THEN '(' || data_length::int || ')'
                 ELSE ''
               END         AS oracle_type,
        CASE nullable WHEN 'N' THEN 'NO' ELSE 'YES' END AS oracle_nullable
    FROM oracle_federation_catalog.SYS.ALL_TAB_COLUMNS
    WHERE owner      = 'HR'
      AND table_name = 'REGIONS'
),
databricks_cols AS (
    SELECT
        UPPER(column_name) AS column_name,
        ordinal_position,
        full_data_type     AS databricks_type,
        is_nullable        AS databricks_nullable
    FROM migration_dev.information_schema.columns
    WHERE table_schema = 'hr_raw'
      AND table_name   = 'regions'
)
SELECT
    d.ordinal_position AS databricks_position,
    o.ordinal_position AS oracle_position,
    d.column_name AS databricks_name,
    o.column_name AS oracle_name,
    o.oracle_type,
    d.databricks_type,
    o.oracle_nullable       AS oracle_nullable,
    d.databricks_nullable   AS databricks_nullable,
    CASE WHEN o.oracle_nullable = d.databricks_nullable THEN '✓' ELSE '△' END AS nullable_match
FROM databricks_cols  d
LEFT JOIN oracle_cols o USING (column_name)
ORDER BY d.ordinal_position;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: COUNTRIES (source)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Oracle: HR.COUNTRIES
-- MAGIC CREATE TABLE "HR"."COUNTRIES" (
-- MAGIC     "COUNTRY_ID"   CHAR(2)      CONSTRAINT "COUNTRY_ID_NN" NOT NULL ENABLE,
-- MAGIC     "COUNTRY_NAME" VARCHAR2(40),
-- MAGIC     "REGION_ID"    NUMBER,
-- MAGIC     CONSTRAINT "COUNTRY_C_ID_PK" PRIMARY KEY ("COUNTRY_ID")
-- MAGIC );
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
-- MAGIC                 var t = document.createElement('textarea'); t.value = code;
-- MAGIC                 document.body.appendChild(t); t.select(); document.execCommand('copy');
-- MAGIC                 document.body.removeChild(t);
-- MAGIC                 this.textContent = '✓ Copied!';
-- MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
-- MAGIC             };
-- MAGIC         });
-- MAGIC     }
-- MAGIC     processCodeBlocks();
-- MAGIC     document.querySelectorAll('details').forEach(d => d.addEventListener('toggle', processCodeBlocks));
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- DBTITLE 1,Create Table: hr_raw.countries
-- CHAR(2) -> STRING  |  PK declared informational (RELY)
CREATE TABLE IF NOT EXISTS migration_dev.hr_raw.countries (
    country_id   STRING NOT NULL,  -- CHAR(2)
    country_name STRING,           -- VARCHAR2(40)
    region_id    INT,              -- NUMBER -> INT (FK to regions)
    CONSTRAINT countries_pk PRIMARY KEY (country_id) RELY
)
COMMENT 'Migrated from Oracle HR.COUNTRIES';

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: LOCATIONS (source)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Oracle: HR.LOCATIONS
-- MAGIC CREATE TABLE "HR"."LOCATIONS" (
-- MAGIC     "LOCATION_ID"    NUMBER(4,0),
-- MAGIC     "STREET_ADDRESS" VARCHAR2(40),
-- MAGIC     "POSTAL_CODE"    VARCHAR2(12),
-- MAGIC     "CITY"           VARCHAR2(30) CONSTRAINT "LOC_CITY_NN" NOT NULL ENABLE,
-- MAGIC     "STATE_PROVINCE" VARCHAR2(25),
-- MAGIC     "COUNTRY_ID"     CHAR(2),
-- MAGIC     CONSTRAINT "LOC_ID_PK" PRIMARY KEY ("LOCATION_ID")
-- MAGIC );
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
-- MAGIC                 var t = document.createElement('textarea'); t.value = code;
-- MAGIC                 document.body.appendChild(t); t.select(); document.execCommand('copy');
-- MAGIC                 document.body.removeChild(t);
-- MAGIC                 this.textContent = '✓ Copied!';
-- MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
-- MAGIC             };
-- MAGIC         });
-- MAGIC     }
-- MAGIC     processCodeBlocks();
-- MAGIC     document.querySelectorAll('details').forEach(d => d.addEventListener('toggle', processCodeBlocks));
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- DBTITLE 1,Create Table: hr_raw.locations
-- NUMBER(4,0) -> INT  |  postal_code kept STRING to preserve leading zeros
CREATE TABLE IF NOT EXISTS migration_dev.hr_raw.locations (
    location_id    INT     NOT NULL,  -- NUMBER(4,0) PK
    street_address STRING,            -- VARCHAR2(40)
    postal_code    STRING,            -- VARCHAR2(12) — STRING preserves leading zeros
    city           STRING   NOT NULL, -- VARCHAR2(30) NOT NULL
    state_province STRING,            -- VARCHAR2(25) nullable
    country_id     STRING,            -- CHAR(2) FK to countries
    CONSTRAINT locations_pk PRIMARY KEY (location_id) RELY
)
COMMENT 'Migrated from Oracle HR.LOCATIONS';

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: JOBS Table (source)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Oracle: HR.JOBS
-- MAGIC CREATE TABLE "HR"."JOBS" (
-- MAGIC     "JOB_ID" VARCHAR2(10), 
-- MAGIC 	"JOB_TITLE" VARCHAR2(35), 
-- MAGIC 	"MIN_SALARY" NUMBER(6,0), 
-- MAGIC 	"MAX_SALARY" NUMBER(6,0)
-- MAGIC )
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

-- DBTITLE 1,Create Table: hr_raw.jobs
-- VARCHAR2(10) -> STRING  |  NUMBER(6,0) -> INT
-- CHECK constraint enforces that min_salary <= max_salary
CREATE TABLE IF NOT EXISTS migration_dev.hr_raw.jobs (
    job_id     STRING NOT NULL,  -- VARCHAR2(10) PK
    job_title  STRING,           -- VARCHAR2(35)
    min_salary INT,              -- NUMBER(6,0)
    max_salary INT,              -- NUMBER(6,0)
    CONSTRAINT jobs_pk PRIMARY KEY (job_id) RELY
)
COMMENT 'Migrated from Oracle HR.JOBS';

ALTER TABLE migration_dev.hr_raw.jobs
ADD CONSTRAINT jobs_salary_range CHECK (min_salary <= max_salary);

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: DEPARTMENTS (source)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Oracle: HR.DEPARTMENTS
-- MAGIC CREATE TABLE "HR"."DEPARTMENTS" (
-- MAGIC     "DEPARTMENT_ID"   NUMBER(4,0),
-- MAGIC     "DEPARTMENT_NAME" VARCHAR2(30) CONSTRAINT "DEPT_NAME_NN" NOT NULL ENABLE,
-- MAGIC     "MANAGER_ID"      NUMBER(6,0),   -- FK to EMPLOYEES (circular dependency)
-- MAGIC     "LOCATION_ID"     NUMBER(4,0),   -- FK to LOCATIONS
-- MAGIC     CONSTRAINT "DEPT_ID_PK" PRIMARY KEY ("DEPARTMENT_ID")
-- MAGIC );
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
-- MAGIC                 var t = document.createElement('textarea'); t.value = code;
-- MAGIC                 document.body.appendChild(t); t.select(); document.execCommand('copy');
-- MAGIC                 document.body.removeChild(t);
-- MAGIC                 this.textContent = '✓ Copied!';
-- MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
-- MAGIC             };
-- MAGIC         });
-- MAGIC     }
-- MAGIC     processCodeBlocks();
-- MAGIC     document.querySelectorAll('details').forEach(d => d.addEventListener('toggle', processCodeBlocks));
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- DBTITLE 1,Create Table: hr_raw.departments
-- Circular FK: departments.manager_id -> employees.employee_id
-- Delta Lake does not enforce FKs; the relationship is documented as a comment.
CREATE TABLE IF NOT EXISTS migration_dev.hr_raw.departments (
    department_id   INT    NOT NULL,  -- NUMBER(4,0) PK
    department_name STRING NOT NULL,  -- VARCHAR2(30) NOT NULL
    manager_id      INT,              -- NUMBER(6,0) nullable FK -> employees
    location_id     INT,              -- NUMBER(4,0) FK -> locations
    CONSTRAINT departments_pk PRIMARY KEY (department_id) RELY
)
COMMENT 'Migrated from Oracle HR.DEPARTMENTS';

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: EMPLOYEES Table (source)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Oracle: HR.EMPLOYEES
-- MAGIC -- Note: some parts omitted for brevity
-- MAGIC CREATE TABLE "HR"."EMPLOYEES" (
-- MAGIC     "EMPLOYEE_ID" NUMBER(6,0), 
-- MAGIC 	"FIRST_NAME" VARCHAR2(20), 
-- MAGIC 	"LAST_NAME" VARCHAR2(25) CONSTRAINT "EMP_LAST_NAME_NN" NOT NULL ENABLE, 
-- MAGIC 	"EMAIL" VARCHAR2(25) CONSTRAINT "EMP_EMAIL_NN" NOT NULL ENABLE, 
-- MAGIC 	"PHONE_NUMBER" VARCHAR2(20), 
-- MAGIC 	"HIRE_DATE" DATE CONSTRAINT "EMP_HIRE_DATE_NN" NOT NULL ENABLE, 
-- MAGIC 	"JOB_ID" VARCHAR2(10) CONSTRAINT "EMP_JOB_NN" NOT NULL ENABLE, 
-- MAGIC 	"SALARY" NUMBER(8,2), 
-- MAGIC 	"COMMISSION_PCT" NUMBER(2,2), 
-- MAGIC 	"MANAGER_ID" NUMBER(6,0), 
-- MAGIC 	"DEPARTMENT_ID" NUMBER(4,0), 
-- MAGIC 	 CONSTRAINT "EMP_SALARY_MIN" CHECK (salary > 0) ENABLE, 
-- MAGIC 	 CONSTRAINT "EMP_EMAIL_UK" UNIQUE ("EMAIL")
-- MAGIC )
-- MAGIC ALTER TABLE "HR"."EMPLOYEES" ADD CONSTRAINT "EMP_EMP_ID_PK" PRIMARY KEY ("EMPLOYEE_ID")
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

-- DBTITLE 1,Create Table: hr_raw.employees
-- Migrate the employees table
-- DECIMAL(8,2) for salary, DECIMAL(2,2) for commission_pct (Oracle NUMBER(2,2))
CREATE TABLE IF NOT EXISTS migration_dev.hr_raw.employees (
    employee_id     INT          NOT NULL,  -- NUMBER(6,0) PK
    first_name      STRING,                 -- VARCHAR2(20)
    last_name       STRING       NOT NULL,  -- VARCHAR2(25) NOT NULL
    email           STRING       NOT NULL,  -- VARCHAR2(25) NOT NULL
    phone_number    STRING,                 -- VARCHAR2(20)
    hire_date       DATE         NOT NULL,  -- DATE NOT NULL
    job_id          STRING       NOT NULL,  -- VARCHAR2(10) NOT NULL FK -> jobs
    salary          DECIMAL(8,2),           -- NUMBER(8,2)
    commission_pct  DECIMAL(2,2),           -- NUMBER(2,2) nullable
    manager_id      INT,                    -- NUMBER(6,0) nullable self-FK
    department_id   INT,                    -- NUMBER(4,0) nullable FK -> departments
    CONSTRAINT emp_emp_id_pk PRIMARY KEY (employee_id) RELY
)
CLUSTER BY (employee_id, department_id)
COMMENT 'Migrated from Oracle HR.EMPLOYEES';

ALTER TABLE migration_dev.hr_raw.employees
ADD CONSTRAINT emp_salary_min CHECK (salary > 0);

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: JOB_HISTORY (source)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Oracle: HR.JOB_HISTORY
-- MAGIC CREATE TABLE "HR"."JOB_HISTORY" (
-- MAGIC     "EMPLOYEE_ID"   NUMBER(6,0) NOT NULL ENABLE,
-- MAGIC     "START_DATE"    DATE        NOT NULL ENABLE,
-- MAGIC     "END_DATE"      DATE        NOT NULL ENABLE,
-- MAGIC     "JOB_ID"        VARCHAR2(10) NOT NULL ENABLE,
-- MAGIC     "DEPARTMENT_ID" NUMBER(4,0),
-- MAGIC     CONSTRAINT "JHIST_EMP_ID_ST_DATE_PK" PRIMARY KEY ("EMPLOYEE_ID", "START_DATE")
-- MAGIC );
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
-- MAGIC                 var t = document.createElement('textarea'); t.value = code;
-- MAGIC                 document.body.appendChild(t); t.select(); document.execCommand('copy');
-- MAGIC                 document.body.removeChild(t);
-- MAGIC                 this.textContent = '✓ Copied!';
-- MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
-- MAGIC             };
-- MAGIC         });
-- MAGIC     }
-- MAGIC     processCodeBlocks();
-- MAGIC     document.querySelectorAll('details').forEach(d => d.addEventListener('toggle', processCodeBlocks));
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- DBTITLE 1,Create Table: hr_raw.job_history
-- Composite PK (employee_id, start_date) — documented as RELY since Delta does not enforce
CREATE TABLE IF NOT EXISTS migration_dev.hr_raw.job_history (
    employee_id   INT    NOT NULL,  -- NUMBER(6,0) FK -> employees
    start_date    DATE   NOT NULL,  -- DATE NOT NULL
    end_date      DATE   NOT NULL,  -- DATE NOT NULL
    job_id        STRING NOT NULL,  -- VARCHAR2(10) FK -> jobs
    department_id INT,              -- NUMBER(4,0) nullable FK -> departments
    CONSTRAINT job_history_pk PRIMARY KEY (employee_id, start_date) RELY
)
COMMENT 'Migrated from Oracle HR.JOB_HISTORY';

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### View conversion
-- MAGIC
-- MAGIC Views are straight-forward to migrate.
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Example HR View (Active Employees with Salary)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Oracle: HR.ACTIVE_EMPLOYEES view
-- MAGIC CREATE OR REPLACE VIEW HR.ACTIVE_EMPLOYEES AS
-- MAGIC SELECT
-- MAGIC     EMPLOYEE_ID,
-- MAGIC     FIRST_NAME,
-- MAGIC     LAST_NAME,
-- MAGIC     EMAIL,
-- MAGIC     JOB_ID,
-- MAGIC     SALARY
-- MAGIC FROM
-- MAGIC     HR.EMPLOYEES
-- MAGIC WHERE
-- MAGIC     SALARY > 0
-- MAGIC     AND JOB_ID IS NOT NULL;
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

-- DBTITLE 1,Active Employees View (SQL)
CREATE OR REPLACE VIEW active_employees AS
SELECT
    employee_id,
    first_name,
    last_name,
    email,
    job_id,
    salary
FROM
    employees
WHERE
    salary > 0
    AND job_id IS NOT NULL;


-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC ## Data Migration
-- MAGIC
-- MAGIC To extract the data, we will use Oracle's SQLcl and stream the output directly to AWS S3 storage.
-- MAGIC
-- MAGIC **Pros:**  
-- MAGIC - Simple and quick: No need for complex ETL tools, intermediate file handling, or complex privilege setup; a single command streams data directly from Oracle to S3.
-- MAGIC
-- MAGIC **Cons:**  
-- MAGIC - Streams through your computer: Data flows through your local machine, which can be a bottleneck for large tables and may expose sensitive data to local network issues.
-- MAGIC
-- MAGIC 1. Install SQLcl
-- MAGIC 1. Start SQLcl: <code>sql -nolog</code>
-- MAGIC 1. Save a named connection <code>conn -save RDS -savepwd DATABRICKS_FEDERATION_SVC/password@rds-host:1521:ORCL</code>
-- MAGIC 1. Exit SQLcl: <code>EXIT</code>
-- MAGIC 1. Create and run the shell script below, that executes a SELECT * query on all tables, and stream the result into S3, into the <code>landing/hr</code> path to make it appear in the external Volume we created earlier.
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 SQLcl: Stream Oracle Data to S3</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="bash">
-- MAGIC #!/bin/bash
-- MAGIC
-- MAGIC # 1. Get the list of all tables from Oracle
-- MAGIC echo "Fetching table list..."
-- MAGIC TABLE_LIST=$(sql -s -name RDS << EOF
-- MAGIC SET FEEDBACK OFF
-- MAGIC SET PAGESIZE 0
-- MAGIC SET HEADING OFF
-- MAGIC SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER='HR';
-- MAGIC EXIT;
-- MAGIC EOF
-- MAGIC )
-- MAGIC
-- MAGIC # 2. Loop through the dynamic list
-- MAGIC for TABLE in $TABLE_LIST
-- MAGIC do
-- MAGIC   FOLDER=$(echo "$TABLE" | tr '[:upper:]' '[:lower:]')
-- MAGIC   echo "Streaming $FOLDER to S3..."
-- MAGIC   sql -s -name RDS << EOF | aws s3 cp - s3://databricks-oracle-migration/landing/hr/${FOLDER}/data.csv
-- MAGIC   SET SQLFORMAT csv
-- MAGIC   SET FEEDBACK OFF
-- MAGIC   SET PAGESIZE 0
-- MAGIC   SELECT * FROM HR.${TABLE};
-- MAGIC   EXIT;
-- MAGIC EOF
-- MAGIC done
-- MAGIC echo "All tables exported!"
-- MAGIC
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
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
-- MAGIC                 this.textContent = 'Copied!';
-- MAGIC                 setTimeout(function() { this.textContent = 'Copy'; }.bind(this), 2000);
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

-- MAGIC %md
-- MAGIC ## Data Ingestion
-- MAGIC
-- MAGIC With all seven tables created in `migration_dev.hr_raw`, we now load the full Oracle HR dataset. The three ingestion methods are used as follows:
-- MAGIC
-- MAGIC | Method | Tables | Best for |
-- MAGIC |---|---|---|
-- MAGIC | **COPY INTO** | `regions`, `jobs` | Batch / one-shot historical load; explicit schema; idempotent reruns |
-- MAGIC | **Auto Loader** | `locations`, `departments`, `employees` | Incremental cloud file ingestion; schema enforcement; streaming or batch trigger |
-- MAGIC | **Lakehouse Federation CRAS** | `countries`, `job_history` | Direct pull from connected Oracle source; no file staging required |
-- MAGIC
-- MAGIC Source files are in `/Volumes/migration_dev/hr_raw/oracle_exports/` (one CSV per table).

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Ingesting Data Using `COPY INTO`
-- MAGIC
-- MAGIC `COPY INTO` is ideal for **batch, one-shot historical loads** from staged files. It is idempotent by default — re-running the same command will not duplicate rows already loaded. Use an explicit `SELECT` subquery to map CSV columns to target column names and cast types precisely.
-- MAGIC
-- MAGIC Key options:
-- MAGIC - `FILEFORMAT = CSV` with `header = true` — skips the header row
-- MAGIC - `inferSchema = false` — forces all CSV columns to be read as strings; casts are applied in the SELECT
-- MAGIC - `force = false` (default) — skips files already processed

-- COMMAND ----------

-- DBTITLE 1,COPY INTO: hr_raw.regions
-- Two columns, four rows — straightforward batch load.
COPY INTO migration_dev.hr_raw.regions
FROM (
    SELECT
        REGION_ID::INT AS region_id,
        REGION_NAME    AS region_name
    FROM '/Volumes/migration_dev/hr_raw/oracle_exports/regions'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false')
COPY_OPTIONS ('force' = 'false');

-- COMMAND ----------

-- DBTITLE 1,View Regions
SELECT * FROM migration_dev.hr_raw.regions;

-- COMMAND ----------

-- DBTITLE 1,COPY INTO: hr_raw.jobs
-- Explicit type casts: job_id stays STRING, salary columns cast to INT.
COPY INTO migration_dev.hr_raw.jobs
FROM (
    SELECT
        JOB_ID          AS job_id,
        JOB_TITLE       AS job_title,
        MIN_SALARY::INT AS min_salary,
        MAX_SALARY::INT AS max_salary
    FROM '/Volumes/migration_dev/hr_raw/oracle_exports/jobs'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false')
COPY_OPTIONS ('force' = 'false');

-- COMMAND ----------

-- DBTITLE 1,Verify: COPY INTO Row Counts
SELECT 'regions' AS table_name, COUNT(*) AS row_count FROM migration_dev.hr_raw.regions
UNION ALL
SELECT 'jobs',                  COUNT(*)              FROM migration_dev.hr_raw.jobs
ORDER BY table_name;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Ingesting Data Using Auto Loader
-- MAGIC
-- MAGIC Auto Loader (`cloudFiles` format) is designed for **incremental file ingestion** — it tracks which files have already been processed using a checkpoint directory and picks up new arrivals automatically. Using `trigger(availableNow=True)` runs it in a single batch-style pass, making it suitable for both initial loads and incremental refreshes.
-- MAGIC
-- MAGIC Best practices shown here:
-- MAGIC - Declare an explicit `StructType` schema (avoids inference overhead and enforces types)
-- MAGIC - For Oracle `DATE` columns stored in `DD-MON-YY` format, read as `STRING` and convert with `to_date(col, "dd-MMM-yy")`
-- MAGIC - Use a dedicated checkpoint directory per table under the volume

-- COMMAND ----------

-- DBTITLE 1,Auto Loader: hr_raw.locations
-- MAGIC %python
-- MAGIC from pyspark.sql.types import StructType, StructField, IntegerType, StringType
-- MAGIC
-- MAGIC schema = StructType([
-- MAGIC     StructField("location_id",    IntegerType(), False),
-- MAGIC     StructField("street_address", StringType(),  True),
-- MAGIC     StructField("postal_code",    StringType(),  True),  # STRING preserves leading zeros
-- MAGIC     StructField("city",           StringType(),  False),
-- MAGIC     StructField("state_province", StringType(),  True),  # nullable
-- MAGIC     StructField("country_id",     StringType(),  True)
-- MAGIC ])
-- MAGIC
-- MAGIC (spark.readStream
-- MAGIC     .format("cloudFiles")
-- MAGIC     .option("cloudFiles.format", "csv")
-- MAGIC     .option("header", "true")
-- MAGIC     .schema(schema)
-- MAGIC     .load("/Volumes/migration_dev/hr_raw/oracle_exports/locations")
-- MAGIC     .writeStream
-- MAGIC     .trigger(availableNow=True)
-- MAGIC     .option("checkpointLocation", "/Volumes/migration_dev/hr_raw/oracle_exports/checkpoints/locations")
-- MAGIC     .toTable("migration_dev.hr_raw.locations")
-- MAGIC     .awaitTermination()
-- MAGIC )

-- COMMAND ----------

-- DBTITLE 1,Auto Loader: hr_raw.departments
-- MAGIC %python
-- MAGIC from pyspark.sql.types import StructType, StructField, IntegerType, StringType
-- MAGIC
-- MAGIC schema = StructType([
-- MAGIC     StructField("department_id",   IntegerType(), False),
-- MAGIC     StructField("department_name", StringType(),  False),
-- MAGIC     StructField("manager_id",      IntegerType(), True),  # nullable — circular FK resolved post-load
-- MAGIC     StructField("location_id",     IntegerType(), True)
-- MAGIC ])
-- MAGIC
-- MAGIC (spark.readStream
-- MAGIC     .format("cloudFiles")
-- MAGIC     .option("cloudFiles.format", "csv")
-- MAGIC     .option("header", "true")
-- MAGIC     .schema(schema)
-- MAGIC     .load("/Volumes/migration_dev/hr_raw/oracle_exports/departments")
-- MAGIC     .writeStream
-- MAGIC     .trigger(availableNow=True)
-- MAGIC     .option("checkpointLocation", "/Volumes/migration_dev/hr_raw/oracle_exports/checkpoints/departments")
-- MAGIC     .toTable("migration_dev.hr_raw.departments")
-- MAGIC     .awaitTermination()
-- MAGIC )

-- COMMAND ----------

-- DBTITLE 1,Auto Loader: hr_raw.employees
-- MAGIC %python
-- MAGIC from pyspark.sql.types import (StructType, StructField, IntegerType,
-- MAGIC                                 StringType, DecimalType)
-- MAGIC from pyspark.sql.functions import to_date, col
-- MAGIC
-- MAGIC # hire_date is read as STRING because Oracle exports it as "DD-MON-YY" (e.g. "17-JUN-03")
-- MAGIC # and converted to DateType using to_date with the matching format pattern.
-- MAGIC schema = StructType([
-- MAGIC     StructField("employee_id",    IntegerType(),        False),
-- MAGIC     StructField("first_name",     StringType(),         True),
-- MAGIC     StructField("last_name",      StringType(),         False),
-- MAGIC     StructField("email",          StringType(),         False),
-- MAGIC     StructField("phone_number",   StringType(),         True),
-- MAGIC     StructField("hire_date",      StringType(),         False),  # converted below
-- MAGIC     StructField("job_id",         StringType(),         False),
-- MAGIC     StructField("salary",         DecimalType(8, 2),    True),
-- MAGIC     StructField("commission_pct", DecimalType(2, 2),    True),   # NUMBER(2,2)
-- MAGIC     StructField("manager_id",     IntegerType(),        True),
-- MAGIC     StructField("department_id",  IntegerType(),        True)
-- MAGIC ])
-- MAGIC
-- MAGIC (spark.readStream
-- MAGIC     .format("cloudFiles")
-- MAGIC     .option("cloudFiles.format", "csv")
-- MAGIC     .option("header", "true")
-- MAGIC     .schema(schema)
-- MAGIC     .load("/Volumes/migration_dev/hr_raw/oracle_exports/employees")
-- MAGIC     .withColumn("hire_date", to_date(col("hire_date"), "dd-MMM-yy"))
-- MAGIC     .writeStream
-- MAGIC     .trigger(availableNow=True)
-- MAGIC     .option("checkpointLocation", "/Volumes/migration_dev/hr_raw/oracle_exports/checkpoints/employees")
-- MAGIC     .toTable("migration_dev.hr_raw.employees")
-- MAGIC     .awaitTermination()
-- MAGIC )

-- COMMAND ----------

-- DBTITLE 1,Verify: Auto Loader Row Counts
SELECT 'locations'   AS table_name, COUNT(*) AS row_count FROM migration_dev.hr_raw.locations
UNION ALL
SELECT 'departments',               COUNT(*)              FROM migration_dev.hr_raw.departments
UNION ALL
SELECT 'employees',                 COUNT(*)              FROM migration_dev.hr_raw.employees
ORDER BY table_name;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Direct Migration with Lakehouse Federation

-- COMMAND ----------

-- DBTITLE 1,Federation INSERT: hr_raw.countries
-- INSERT INTO ... pulls directly from the live Oracle source via
-- the registered foreign catalog — no file staging, no schema declaration needed.
-- Explicit casts ensure correct Databricks types (Oracle NUMBER -> INT).

INSERT INTO migration_dev.hr_raw.countries
SELECT
    country_id,
    country_name,
    CAST(region_id AS INT) AS region_id
FROM oracle_federation_catalog.hr.countries;

-- COMMAND ----------

-- DBTITLE 1,Federation INSERT: hr_raw.job_history
-- Oracle DATE columns are cast explicitly to Databricks DATE.
-- Composite PK (employee_id, start_date) is retained as a RELY constraint in the target DDL.

INSERT INTO migration_dev.hr_raw.job_history
SELECT
    CAST(employee_id   AS INT)    AS employee_id,
    CAST(start_date    AS DATE)   AS start_date,
    CAST(end_date      AS DATE)   AS end_date,
    job_id,
    CAST(department_id AS INT)    AS department_id
FROM oracle_federation_catalog.hr.job_history;

-- COMMAND ----------

-- DBTITLE 1,Verify: Federation Row Counts
SELECT 'countries'   AS table_name, COUNT(*) AS row_count FROM migration_dev.hr_raw.countries
UNION ALL
SELECT 'job_history',               COUNT(*)              FROM migration_dev.hr_raw.job_history
ORDER BY table_name;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Migration Validation
-- MAGIC
-- MAGIC When Lakehouse Federation is used, it becomes very easy to check if all data has been migrated.
-- MAGIC We can compare the count of rows in the migrated and the source database with a single query.

-- COMMAND ----------

-- DBTITLE 1,Validate: All Table Row Counts
-- Compares row counts between the Databricks target (hr_raw) and the live Oracle source
-- via Lakehouse Federation. A mismatch indicates rows lost or duplicated during migration.

WITH databricks AS (
    SELECT 'regions'     AS table_name, COUNT(*) AS row_count FROM migration_dev.hr_raw.regions
    UNION ALL
    SELECT 'countries',                 COUNT(*)              FROM migration_dev.hr_raw.countries
    UNION ALL
    SELECT 'locations',                 COUNT(*)              FROM migration_dev.hr_raw.locations
    UNION ALL
    SELECT 'jobs',                      COUNT(*)              FROM migration_dev.hr_raw.jobs
    UNION ALL
    SELECT 'departments',               COUNT(*)              FROM migration_dev.hr_raw.departments
    UNION ALL
    SELECT 'employees',                 COUNT(*)              FROM migration_dev.hr_raw.employees
    UNION ALL
    SELECT 'job_history',               COUNT(*)              FROM migration_dev.hr_raw.job_history
),
oracle AS (
    SELECT 'regions'     AS table_name, COUNT(*) AS row_count FROM oracle_federation_catalog.hr.regions
    UNION ALL
    SELECT 'countries',                 COUNT(*)              FROM oracle_federation_catalog.hr.countries
    UNION ALL
    SELECT 'locations',                 COUNT(*)              FROM oracle_federation_catalog.hr.locations
    UNION ALL
    SELECT 'jobs',                      COUNT(*)              FROM oracle_federation_catalog.hr.jobs
    UNION ALL
    SELECT 'departments',               COUNT(*)              FROM oracle_federation_catalog.hr.departments
    UNION ALL
    SELECT 'employees',                 COUNT(*)              FROM oracle_federation_catalog.hr.employees
    UNION ALL
    SELECT 'job_history',               COUNT(*)              FROM oracle_federation_catalog.hr.job_history
)
SELECT
    d.table_name,
    o.row_count                                         AS oracle_count,
    d.row_count                                         AS databricks_count,
    d.row_count - o.row_count                           AS delta,
    CASE WHEN d.row_count = o.row_count THEN '✓ OK'
         ELSE '✗ MISMATCH'
    END                                                 AS status
FROM databricks d
JOIN oracle      o USING (table_name)
ORDER BY table_name;

-- COMMAND ----------

-- DBTITLE 1,Validate: Sample Spot Checks
-- Verify hire_date parsed correctly (Oracle DD-MON-YY -> DATE) and compare with federated source
SELECT
    d.employee_id,
    d.first_name AS dbx_first_name,
    d.hire_date  AS dbx_hire_date,
    d.job_id     AS dbx_job_id,
    o.first_name AS oracle_first_name,
    CAST(o.hire_date AS DATE) AS oracle_hire_date,
    o.job_id     AS oracle_job_id
FROM migration_dev.hr_raw.employees d
JOIN oracle_federation_catalog.hr.employees o
  ON d.employee_id = o.employee_id
WHERE d.employee_id = 100;  -- expected: Steven King, 2003-06-17, AD_PRES

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## SQL and Code Conversion
-- MAGIC
-- MAGIC You can run original Oracle queries from Databricks with `remote_query` using Oracle syntax. This works through our federated `CONNECTION`. This method can be used to compare the results of the original and the migrated queries and to check if all data has been moved over.

-- COMMAND ----------

-- DBTITLE 1,remote_query Example (SQL)
SELECT * FROM remote_query(
  'oracle_federation',
  service_name => 'ORCL',
  query => 'SELECT EMPLOYEE_ID, FIRST_NAME, LAST_NAME FROM HR.EMPLOYEES WHERE ROWNUM <= 5'
);

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Type casting and mapping
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- DBTITLE 1,Type Casting Example (SQL)
-- Demonstrates type conversions for strings, numbers, dates, and safe casting with TRY_CAST.
-- Both :: shorthand and CAST() work; NUMBER -> DECIMAL, FLOAT -> DOUBLE, VARCHAR -> STRING.
SELECT 
    employee_id,
    
    employee_id::STRING AS emp_id_string,
    CAST(salary AS STRING) AS salary_string,
    
    salary::INT AS salary_int,
    CAST(salary AS DECIMAL(10,2)) AS salary_decimal,
    
    hire_date::STRING AS hire_date_string,
    CAST('2024-01-15' AS DATE) AS date_from_string,
    
    TRY_CAST(commission_pct AS DOUBLE) AS commission_safe,
    TRY_CAST('invalid' AS INT) AS invalid_cast_null
    
FROM migration_dev.hr_raw.employees
LIMIT 5;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Date and Time Functions

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Date arithmetic (ADD_MONTHS and direct addition)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Adds 90 days for probation end and 6 months for first review date.
-- MAGIC -- Oracle uses direct date arithmetic for days and ADD_MONTHS for month offsets.
-- MAGIC
-- MAGIC SELECT 
-- MAGIC     employee_id,
-- MAGIC     hire_date,
-- MAGIC     hire_date + 90 AS probation_end,
-- MAGIC     ADD_MONTHS(hire_date, 6) AS first_review_date
-- MAGIC FROM HR.EMPLOYEES
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,Date arithmetic with INTERVAL syntax and DATEADD (SQL)
-- Adds 90 days for probation end and 6 months for first review date.
-- Databricks supports both INTERVAL syntax and DATEADD; date parts are unquoted (DAY not 'day').
SELECT 
    employee_id,
    hire_date,
    hire_date + INTERVAL 90 DAYS AS probation_end_interval,
    DATEADD(DAY, 90, hire_date) AS probation_end_dateadd,
    DATEADD(MONTH, 6, hire_date) AS first_review_date
FROM migration_dev.hr_raw.employees
LIMIT 5;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Calculate days between dates</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Calculates how many days each employee spent in a previous role.
-- MAGIC -- Oracle calculates date differences by subtracting dates directly (result in days).
-- MAGIC
-- MAGIC -- Note: DATE - DATE returns number of days.
-- MAGIC -- If TIMESTAMP is involved, cast to DATE to avoid INTERVAL results.
-- MAGIC SELECT 
-- MAGIC     e.employee_id,
-- MAGIC     e.first_name || ' ' || e.last_name AS employee_name,
-- MAGIC     jh.start_date,
-- MAGIC     jh.end_date,
-- MAGIC     jh.end_date - jh.start_date AS days_in_role
-- MAGIC FROM HR.EMPLOYEES e
-- MAGIC JOIN HR.JOB_HISTORY jh ON e.employee_id = jh.employee_id
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,Calculate days between sign-up and first order (SQL)
-- Calculates how many days each employee spent in a previous role.
-- DATEDIFF uses unquoted date part (DAY not 'day'); otherwise identical to Oracle.
SELECT 
    e.employee_id,
    e.first_name || ' ' || e.last_name AS employee_name,
    jh.start_date,
    jh.end_date,
    DATEDIFF(DAY, jh.start_date, jh.end_date) AS days_in_role
FROM migration_dev.hr_raw.employees e
JOIN migration_dev.hr_raw.job_history jh ON e.employee_id = jh.employee_id
ORDER BY days_in_role DESC;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Date parts and truncation</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Extracts date components like month start, day of week, and full month/day names from hire dates.
-- MAGIC -- Oracle uses TRUNC, TO_CHAR, and LAST_DAY for date manipulation.
-- MAGIC
-- MAGIC SELECT 
-- MAGIC     hire_date,
-- MAGIC     TRUNC(hire_date, 'MM') AS month_start,
-- MAGIC     TO_CHAR(hire_date, 'D') AS day_of_week,
-- MAGIC     TO_CHAR(hire_date, 'Month') AS month_name,
-- MAGIC     TO_CHAR(hire_date, 'Day') AS day_name,
-- MAGIC     LAST_DAY(hire_date) AS month_end
-- MAGIC FROM HR.EMPLOYEES
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,Date parts and truncation (SQL)
-- Extracts date components like month start, day of week, and full month/day names from hire dates.
-- MONTHNAME -> DATE_FORMAT(,'MMMM') and DAYNAME -> DATE_FORMAT(,'EEEE'); other functions identical.
SELECT 
    hire_date,
    DATE_TRUNC('month', hire_date) AS month_start,
    DATE_PART('DOW', hire_date) AS day_of_week,
    DATE_FORMAT(hire_date, 'MMMM') AS month_name, -- Replaces MONTHNAME()
    DATE_FORMAT(hire_date, 'EEEE') AS day_name, -- Replaces DAYNAME()
    LAST_DAY(hire_date) AS month_end
FROM migration_dev.hr_raw.employees
LIMIT 5;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### String Functions

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: String manipulation examples</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Builds full employee names using concatenation and extracts phone prefixes.
-- MAGIC -- Oracle uses || for concatenation and SUBSTR/INSTR for string parsing.
-- MAGIC
-- MAGIC SELECT 
-- MAGIC     employee_id,
-- MAGIC     first_name || ' ' || last_name AS full_name,
-- MAGIC     CONCAT(first_name, last_name) AS full_name_concat,
-- MAGIC     UPPER(last_name) AS last_name_upper,
-- MAGIC     SUBSTR(phone_number, 1, 3) AS phone_prefix
-- MAGIC FROM HR.EMPLOYEES
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,String manipulation examples (SQL)
-- Builds full employee names using concatenation and extracts phone prefixes.
-- All string functions (CONCAT, UPPER, SPLIT_PART, LEFT) work identically to Oracle.
SELECT 
    employee_id,
    first_name || ' ' || last_name AS full_name,
    CONCAT(first_name, ' ', last_name) AS full_name_concat,
    UPPER(last_name) AS last_name_upper,
    LEFT(phone_number, 3) AS phone_prefix
FROM migration_dev.hr_raw.employees
LIMIT 5;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Aggregate data into comma-separated list</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Aggregates employee first names into a sorted comma-separated list per department.
-- MAGIC -- Oracle uses LISTAGG with WITHIN GROUP for ordered string aggregation.
-- MAGIC
-- MAGIC SELECT 
-- MAGIC     d.department_name,
-- MAGIC     LISTAGG(e.first_name, ', ') WITHIN GROUP (ORDER BY e.first_name) AS employee_names
-- MAGIC FROM HR.EMPLOYEES e
-- MAGIC JOIN HR.DEPARTMENTS d ON e.department_id = d.department_id
-- MAGIC GROUP BY d.department_name
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,LISTAGG equivalent using ARRAY_JOIN + COLLECT_LIST (SQL)
-- Aggregates employee first names into a sorted comma-separated list per department.
-- LISTAGG -> ARRAY_JOIN(ARRAY_SORT(COLLECT_LIST())); combines three functions to match Oracle behavior.
SELECT 
    d.department_name,
    ARRAY_JOIN(ARRAY_SORT(COLLECT_LIST(e.first_name)), ', ') AS employee_names
FROM migration_dev.hr_raw.employees e
JOIN migration_dev.hr_raw.departments d ON e.department_id = d.department_id
GROUP BY d.department_name;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Extract patterns using Regular Expressions</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Extracts the area code from phone numbers and normalizes phone format.
-- MAGIC -- Oracle uses REGEXP_SUBSTR for extraction and REGEXP_REPLACE for substitution.
-- MAGIC
-- MAGIC SELECT 
-- MAGIC     first_name || ' ' || last_name AS employee_name,
-- MAGIC     phone_number,
-- MAGIC     REGEXP_SUBSTR(phone_number, '[0-9]+') AS area_code,
-- MAGIC     REGEXP_REPLACE(phone_number, '\.', '-') AS phone_dashes
-- MAGIC FROM HR.EMPLOYEES
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,Regex extraction and replacement (SQL)
-- Extracts the area code from phone numbers and normalizes phone format.
-- REGEXP_SUBSTR -> REGEXP_EXTRACT (with group index parameter); REGEXP_REPLACE is identical.
SELECT 
    first_name || ' ' || last_name AS employee_name,
    phone_number,
    REGEXP_EXTRACT(phone_number, '[0-9]+', 0) AS area_code,
    REGEXP_REPLACE(phone_number, '\\.', '-') AS phone_dashes
FROM migration_dev.hr_raw.employees
LIMIT 5;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Aggregate and Window Functions

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: LISTAGG with duplicates</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Collects all job IDs from job history for each employee into a delimited string, including duplicates.
-- MAGIC -- LISTAGG preserves all values in the order they appear.
-- MAGIC SELECT 
-- MAGIC     employee_id,
-- MAGIC     COUNT(*) AS role_count,
-- MAGIC     LISTAGG(job_id, ', ') WITHIN GROUP (ORDER BY start_date) AS all_previous_roles
-- MAGIC FROM HR.JOB_HISTORY
-- MAGIC GROUP BY employee_id
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,ARRAY_AGG with duplicates conversion to COLLECT_LIST (SQL)
-- Collects all job IDs from job history for each employee into a delimited string, including duplicates.
-- LISTAGG -> ARRAY_JOIN(COLLECT_LIST()); preserves all values and duplicates just like Oracle.
SELECT 
    employee_id,
    COUNT(*) AS role_count,
    ARRAY_JOIN(COLLECT_LIST(job_id), ', ') AS all_previous_roles
FROM migration_dev.hr_raw.job_history
GROUP BY employee_id;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: LISTAGG without duplicates</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Collects unique department IDs from job history for each employee, removing duplicates.
-- MAGIC -- LISTAGG(DISTINCT) eliminates duplicates before aggregation.
-- MAGIC SELECT 
-- MAGIC     employee_id,
-- MAGIC     COUNT(*) AS role_count,
-- MAGIC     LISTAGG(DISTINCT department_id, ', ') 
-- MAGIC         WITHIN GROUP (ORDER BY department_id) AS unique_departments
-- MAGIC FROM HR.JOB_HISTORY
-- MAGIC GROUP BY employee_id
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,ARRAY_AGG without duplicates conversion to COLLECT_SET (SQL)
-- Collects unique department IDs from job history for each employee, removing duplicates.
-- LISTAGG(DISTINCT) -> COLLECT_SET(); automatically deduplicates values in the array.
SELECT 
    employee_id,
    COUNT(*) AS role_count,
    COLLECT_SET(department_id) AS unique_departments
FROM migration_dev.hr_raw.job_history
GROUP BY employee_id;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Null handling functions

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: NVL example</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Calculates total compensation with NULL commission replaced by zero, plus median salary.
-- MAGIC -- Oracle uses NVL for NULL handling and MEDIAN for statistical aggregation.
-- MAGIC SELECT 
-- MAGIC     department_id,
-- MAGIC     NVL(SUM(salary * commission_pct), 0) AS total_commission,
-- MAGIC     MEDIAN(salary) AS median_salary
-- MAGIC FROM HR.EMPLOYEES
-- MAGIC GROUP BY department_id;
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

-- DBTITLE 1,ZEROIFNULL -> COALESCE or IFNULL (SQL)
-- Calculates total compensation with NULL commission replaced by zero, plus median salary.
-- NVL -> COALESCE(col,0) or IFNULL(col,0); MEDIAN is supported directly in DBR 14+, PERCENTILE works on all versions.
SELECT 
    department_id,
    COALESCE(SUM(salary * commission_pct), 0) AS total_commission,
    IFNULL(SUM(salary * commission_pct), 0) AS total_commission_v2,
    MEDIAN(salary) AS median_salary,
    PERCENTILE(salary, 0.5) AS median_v2
FROM migration_dev.hr_raw.employees
GROUP BY department_id;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Some more null functions

-- COMMAND ----------

-- DBTITLE 1,Conditional function conversions (SQL)
-- Demonstrates conditional logic including IF, IFNULL, NVL, NVL2, COALESCE, and null-safe equality.
SELECT 
    employee_id,
    salary,
    commission_pct,
    
    IF(salary > 15000, 'High Earner', 'Standard') AS salary_category,
    
    IFNULL(commission_pct, 0) AS commission_ifnull,
    NVL(commission_pct, 0) AS commission_nvl,
    COALESCE(commission_pct, 0) AS commission_coalesce,
    
    NVL2(commission_pct, 'Commission-Based', 'Fixed Salary') AS comp_type,
    
    COALESCE(TRY_CAST(commission_pct AS DOUBLE), 0) AS commission_safe,
    
    commission_pct <=> 0.30 AS is_30pct_nullsafe
    
FROM migration_dev.hr_raw.employees;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Semi-Structured Data (JSON vs VARIANT)
-- MAGIC
-- MAGIC Let's create a sample table for these examples first.
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">Serverless version requirement</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">The <code>VARIANT</code> data type needs at least serverless environment <strong>v2</strong>.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- DBTITLE 1,Create Sample Structured Data
-- Separate analytics table joining core HR columns with semi-structured profile data.

CREATE OR REPLACE TABLE migration_dev.hr_raw.employee_profiles AS
WITH profiles (employee_id, employee_details) AS (
    VALUES
    (100, PARSE_JSON('{"skills":["Leadership","Strategy","Finance"],"certifications":[{"name":"MBA","year":2000},{"name":"PMP","year":2002}],"languages":["English","French"],"performance_rating":4.8}')),
    (103, PARSE_JSON('{"skills":["Python","Java","SQL","Cloud"],"certifications":[{"name":"AWS Solutions Architect","year":2020},{"name":"Databricks Certified","year":2022}],"languages":["English","German"],"performance_rating":4.2}')),
    (108, PARSE_JSON('{"skills":["Accounting","Financial Analysis","SAP"],"certifications":[{"name":"CPA","year":2005},{"name":"CFA","year":2008}],"languages":["English"],"performance_rating":4.3}')),
    (145, PARSE_JSON('{"skills":["Sales Strategy","Negotiation","CRM"],"certifications":[{"name":"Salesforce Admin","year":2019}],"languages":["English","German"],"performance_rating":4.4}')),
    (201, PARSE_JSON('{"skills":["Brand Strategy","Digital Marketing","Leadership"],"certifications":[{"name":"MBA","year":2003}],"languages":["English","Spanish"],"performance_rating":4.3}')),
    (203, PARSE_JSON('{"skills":["Recruiting","HRIS","Training"],"certifications":[{"name":"PHR","year":2015}],"languages":["English"],"performance_rating":3.8}'))
)
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.job_id,
    e.department_id,
    e.salary,
    p.employee_details
FROM migration_dev.hr_raw.employees  e
JOIN profiles                        p USING (employee_id);

SELECT * FROM migration_dev.hr_raw.employee_profiles;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Accessing JSON fields</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Extracts performance rating and first certification from the employee_details JSON.
-- MAGIC -- Navigates through JSON: object -> field, object -> array[0] -> field.
-- MAGIC
-- MAGIC SELECT 
-- MAGIC     first_name || ' ' || last_name AS employee_name,
-- MAGIC     JSON_VALUE(employee_details, '$.performance_rating') AS rating,
-- MAGIC     JSON_VALUE(employee_details, '$.certifications[0].name') AS first_cert,
-- MAGIC     JSON_VALUE(employee_details, '$.certifications[0].year') AS cert_year
-- MAGIC FROM HR.EMPLOYEES
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,VARIANT field access using colon notation (DBR 15.3+) (SQL)
-- Extracts performance rating and first certification from the employee_details VARIANT.
-- Colon notation with array indexing is identical to Oracle (DBR 15.3+).
SELECT 
    first_name || ' ' || last_name AS employee_name,
    employee_details:performance_rating::DOUBLE AS rating,
    employee_details:certifications[0]:name::STRING AS first_cert,
    employee_details:certifications[0]:year::INT AS cert_year
FROM migration_dev.hr_raw.employee_profiles
WHERE employee_details IS NOT NULL;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Accessing nested arrays</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Retrieves the skills array and counts how many skills each employee has.
-- MAGIC -- Uses JSON_TABLE to count array elements (portable and widely supported).
-- MAGIC
-- MAGIC SELECT 
-- MAGIC     first_name || ' ' || last_name AS employee_name,
-- MAGIC     JSON_QUERY(employee_details, '$.skills') AS skills_array,
-- MAGIC     JSON_VALUE(employee_details, '$.skills.size()') AS num_skills,
-- MAGIC     JSON_VALUE(employee_details, '$.skills[0]') AS primary_skill
-- MAGIC FROM HR.EMPLOYEES
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,Access nested arrays within VARIANT (SQL)
-- Retrieves the skills array and counts how many skills each employee has.
-- ARRAY_SIZE -> SIZE; must cast VARIANT to ARRAY first in Databricks.
SELECT 
    first_name || ' ' || last_name AS employee_name,
    employee_details:skills AS skills_array,
    SIZE(CAST(employee_details:skills AS ARRAY<STRING>)) AS num_skills,
    employee_details:skills[0]::STRING AS primary_skill
FROM migration_dev.hr_raw.employee_profiles
WHERE employee_details IS NOT NULL;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Building a new JSON object</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Creates a new JSON object containing employee summary information from column values.
-- MAGIC -- Oracle uses JSON_OBJECT for constructing JSON from relational columns.
-- MAGIC
-- MAGIC SELECT 
-- MAGIC     employee_id,
-- MAGIC     JSON_OBJECT(
-- MAGIC         'employee_id' VALUE employee_id,
-- MAGIC         'name' VALUE first_name || ' ' || last_name,
-- MAGIC         'department_id' VALUE department_id
-- MAGIC     ) AS employee_summary
-- MAGIC FROM HR.EMPLOYEES
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,OBJECT_CONSTRUCT alternatives (SQL)
-- Creates a new structured object containing employee summary information from column values.
-- JSON_OBJECT -> NAMED_STRUCT (returns STRUCT) or TO_JSON(NAMED_STRUCT()) for JSON string.
SELECT 
    employee_id,
    NAMED_STRUCT(
        'employee_id', employee_id,
        'name', first_name || ' ' || last_name,
        'department_id', department_id
    ) AS employee_summary_struct,
    
    TO_JSON(NAMED_STRUCT(
        'employee_id', employee_id,
        'name', first_name || ' ' || last_name,
        'department_id', department_id
    )) AS employee_summary_json
FROM migration_dev.hr_raw.employee_profiles;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Checking if JSON array contains a value</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Checks if employees have specific skills like 'Python' or 'SQL' in their profile.
-- MAGIC -- Oracle uses JSON_EXISTS for checking value presence in JSON arrays.
-- MAGIC
-- MAGIC SELECT 
-- MAGIC     first_name || ' ' || last_name AS employee_name,
-- MAGIC     JSON_QUERY(employee_details, '$.skills') AS skills,
-- MAGIC     CASE WHEN JSON_EXISTS(employee_details, '$.skills[*]?(@ == "Python")') THEN 'Y' ELSE 'N' END AS knows_python,
-- MAGIC     CASE WHEN JSON_EXISTS(employee_details, '$.skills[*]?(@ == "SQL")') THEN 'Y' ELSE 'N' END AS knows_sql
-- MAGIC FROM HR.EMPLOYEES
-- MAGIC WHERE employee_details IS NOT NULL
-- MAGIC FETCH FIRST 5 ROWS ONLY;
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

-- DBTITLE 1,ARRAY_CONTAINS example (SQL)
-- Checks if employees have specific skills like 'Python' or 'SQL' in their profile.
-- ARRAY_CONTAINS argument order is REVERSED: Databricks uses (array, value) not (value, array).
SELECT 
    first_name || ' ' || last_name AS employee_name,
    employee_details:skills AS skills,
    ARRAY_CONTAINS(
        CAST(employee_details:skills AS ARRAY<STRING>),
        'Python'
    ) AS knows_python,
    ARRAY_CONTAINS(
        CAST(employee_details:skills AS ARRAY<STRING>),
        'SQL'
    ) AS knows_sql
FROM migration_dev.hr_raw.employee_profiles
WHERE employee_details IS NOT NULL;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### User-Defined Function (UDF) Conversion

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### SQL UDF Conversion
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: SQL UDF definitions</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql"><pre>-- Creates SQL functions for annual salary calculation and salary band classification.
-- MAGIC -- Uses PL/SQL syntax with IS/BEGIN/END block structure.
-- MAGIC
-- MAGIC CREATE OR REPLACE FUNCTION HR.CALC_ANNUAL_COMPENSATION(
-- MAGIC     base_salary NUMBER,
-- MAGIC     commission_pct NUMBER
-- MAGIC )
-- MAGIC RETURN NUMBER
-- MAGIC IS
-- MAGIC BEGIN
-- MAGIC     RETURN base_salary * 12 * (1 + NVL(commission_pct, 0));
-- MAGIC END;
-- MAGIC
-- MAGIC CREATE OR REPLACE FUNCTION HR.GET_SALARY_BAND(
-- MAGIC     salary NUMBER
-- MAGIC )
-- MAGIC RETURN VARCHAR2
-- MAGIC IS
-- MAGIC BEGIN
-- MAGIC     RETURN CASE 
-- MAGIC         WHEN salary >= 15000 THEN 'Executive'
-- MAGIC         WHEN salary >= 10000 THEN 'Senior'
-- MAGIC         WHEN salary >= 6000 THEN 'Mid-Level'
-- MAGIC         ELSE 'Junior'
-- MAGIC     END;
-- MAGIC END;</pre></div>
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

-- DBTITLE 1,SQL UDF definitions (SQL)
-- Creates SQL functions for annual salary calculation and salary band classification.
-- Uses RETURN keyword instead of $$ delimiters; FLOAT -> DOUBLE, NUMBER -> DECIMAL for types.
CREATE OR REPLACE FUNCTION migration_dev.hr_raw.calc_annual_compensation(
    base_salary DOUBLE,
    commission_pct DOUBLE
)
RETURNS DOUBLE
RETURN base_salary * 12 * (1 + COALESCE(commission_pct, 0));

CREATE OR REPLACE FUNCTION migration_dev.hr_raw.get_salary_band(
    salary DOUBLE
)
RETURNS STRING
RETURN CASE 
    WHEN salary >= 15000 THEN 'Executive'
    WHEN salary >= 10000 THEN 'Senior'
    WHEN salary >= 6000 THEN 'Mid-Level'
    ELSE 'Junior'
END;

-- COMMAND ----------

-- DBTITLE 1,Call SQL UDFs (SQL)
-- Calculates annual compensation and salary band for each employee using custom UDFs.
-- References UDF with catalog.schema.function_name format (three-level namespace).
SELECT 
    first_name || ' ' || last_name AS employee_name,
    salary,
    commission_pct,
    migration_dev.hr_raw.calc_annual_compensation(
        salary, 
        commission_pct
    ) AS annual_compensation,
    migration_dev.hr_raw.get_salary_band(salary) AS salary_band
FROM migration_dev.hr_raw.employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Trigger and Stored Procedure Conversion
-- MAGIC
-- MAGIC Stored Procedures exist in Databricks too, since DBR 17.0, easing the migration procedure. However, re-implementing an Oracle stored procedure as a Databricks Lakeflow Job, potentially including multiple source files / queries, might be a better fit to the Lakehouse platform.
-- MAGIC
-- MAGIC Oracle triggers fire procedural logic in response to DML events. The `UPDATE_JOB_HISTORY` trigger records an employee's previous job into `JOB_HISTORY` whenever `job_id` or `department_id` changes.
-- MAGIC
-- MAGIC Delta Lake does not support triggers; instead, **Change Data Feed (CDF)** captures row-level before/after images, and a **Lakeflow Spark Declarative Pipeline** with `AUTO CDC INTO` can replicate the same history pattern as a continuous stream.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle's <code>add_job_history</code> procedure and its trigger</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC CREATE OR REPLACE PROCEDURE add_job_history
-- MAGIC   (  p_emp_id          job_history.employee_id%type
-- MAGIC    , p_start_date      job_history.start_date%type
-- MAGIC    , p_end_date        job_history.end_date%type
-- MAGIC    , p_job_id          job_history.job_id%type
-- MAGIC    , p_department_id   job_history.department_id%type 
-- MAGIC    )
-- MAGIC IS
-- MAGIC BEGIN
-- MAGIC   INSERT INTO job_history (employee_id, start_date, end_date, 
-- MAGIC                            job_id, department_id)
-- MAGIC     VALUES(p_emp_id, p_start_date, p_end_date, p_job_id, p_department_id);
-- MAGIC END add_job_history;
-- MAGIC /
-- MAGIC
-- MAGIC CREATE OR REPLACE TRIGGER update_job_history
-- MAGIC   AFTER UPDATE OF job_id, department_id ON employees
-- MAGIC   FOR EACH ROW
-- MAGIC BEGIN
-- MAGIC   add_job_history(:old.employee_id, :old.hire_date, sysdate, 
-- MAGIC                   :old.job_id, :old.department_id);
-- MAGIC END;
-- MAGIC /
-- MAGIC
-- MAGIC COMMIT;
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

-- MAGIC %md
-- MAGIC The Oracle `update_job_history` trigger fires on every `UPDATE` of `job_id` or `department_id` in `EMPLOYEES`. Below, we demonstrate the equivalent pattern in Databricks using **jobs** as the source table and **jobs_history** as the audit target — the same technique applies to any table.
-- MAGIC
-- MAGIC Steps:
-- MAGIC 1. Enable Change Data Feed on `hr_raw.jobs`
-- MAGIC 2. Simulate a salary band update (the event that would fire an Oracle trigger)
-- MAGIC 3. Inspect the CDF to see the before-image
-- MAGIC 4. Insert the before-image into `hr_raw.jobs_history`
-- MAGIC 5. Verify the audit record

-- COMMAND ----------

-- DBTITLE 1,Step 1: Enable Change Data Feed on employees (SQL)
ALTER TABLE migration_dev.hr_raw.employees
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);

-- COMMAND ----------

-- DBTITLE 1,Step 2: Simulate an Employee Job Change (SQL)
UPDATE migration_dev.hr_raw.employees
SET job_id = 'FI_MGR', department_id = 100
WHERE employee_id = 101;

-- COMMAND ----------

-- DBTITLE 1,Step 3: Inspect CDF — Read the Before-Image (SQL)
SELECT employee_id, first_name, hire_date, job_id, department_id,
       _change_type, _commit_version, _commit_timestamp
FROM table_changes('migration_dev.hr_raw.employees', 3)
WHERE _commit_timestamp >= current_timestamp() - INTERVAL 5 MINUTES
ORDER BY _commit_version, _change_type;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Confirm `job_history` is empty

-- COMMAND ----------

-- DBTITLE 1,Step 4: Replicate Trigger Logic — INSERT into job_history (SQL)
-- start_date: end_date of the employee's most recent job_history row, or hire_date
-- if this is their first job change — so repeated job changes remain accurate.
INSERT INTO migration_dev.hr_raw.job_history (employee_id, start_date, end_date, job_id, department_id)
SELECT
    cdf.employee_id,
    COALESCE(
        (SELECT MAX(jh.end_date)
         FROM   migration_dev.hr_raw.job_history jh
         WHERE  jh.employee_id = cdf.employee_id),
        cdf.hire_date
    )                        AS start_date,
    cdf._commit_timestamp    AS end_date,
    cdf.job_id,
    cdf.department_id
FROM table_changes('migration_dev.hr_raw.employees', 3) AS cdf
WHERE cdf._change_type = 'update_preimage'
  AND cdf._commit_timestamp >= current_timestamp() - INTERVAL 5 MINUTES
  AND cdf.employee_id = 101;

-- COMMAND ----------

-- DBTITLE 1,Step 5: Verify — Job History Captured from CDF (SQL)
SELECT jh.employee_id, e.first_name, e.last_name,
       jh.start_date, CAST(jh.end_date AS DATE) AS end_date,
       jh.job_id AS previous_job, jh.department_id AS previous_dept,
       e.job_id  AS current_job,  e.department_id  AS current_dept
FROM migration_dev.hr_raw.job_history AS jh
JOIN migration_dev.hr_raw.employees   AS e ON jh.employee_id = e.employee_id
WHERE jh.employee_id = 101
ORDER BY jh.start_date DESC;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC For production use, implement trigger replacement as a **Lakeflow Spark Declarative Pipeline**. The Python approach suits custom filtering or enrichment logic; <code>AUTO CDC INTO</code> with <code>STORED AS SCD TYPE 2</code> consolidates the trigger and history table into a single dimension.
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Lakeflow SDP — Python streaming pipeline (replaces trigger with CDF)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="python">
-- MAGIC from pyspark import pipelines as dp
-- MAGIC from pyspark.sql.functions import col
-- MAGIC
-- MAGIC @dp.table(
-- MAGIC     name="job_history_from_cdf",
-- MAGIC     comment="Replaces Oracle UPDATE_JOB_HISTORY trigger via CDF streaming"
-- MAGIC )
-- MAGIC def job_history_from_cdf():
-- MAGIC     return (
-- MAGIC         spark.readStream
-- MAGIC              .format("delta")
-- MAGIC              .option("readChangeFeed", "true")
-- MAGIC              .table("migration_dev.hr.employees")
-- MAGIC         .filter(col("_change_type") == "update_preimage")
-- MAGIC         .select(
-- MAGIC             col("employee_id"),
-- MAGIC             col("hire_date").alias("start_date"),
-- MAGIC             col("_commit_timestamp").alias("end_date"),
-- MAGIC             col("job_id"),
-- MAGIC             col("department_id")
-- MAGIC         )
-- MAGIC     )
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Lakeflow SDP — Python AUTO CDC SCD Type 2 (consolidates full table history into one dimension)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="python">
-- MAGIC from pyspark import pipelines as dp
-- MAGIC from pyspark.sql.functions import col, expr
-- MAGIC
-- MAGIC # Define a streaming view that reads the Change Data Feed
-- MAGIC @dp.view
-- MAGIC def employees_cdf():
-- MAGIC     return (
-- MAGIC         spark.readStream
-- MAGIC              .option("readChangeFeed", "true")
-- MAGIC              .table("migration_dev.hr.employees")
-- MAGIC     )
-- MAGIC
-- MAGIC # Create the target streaming table
-- MAGIC dp.create_streaming_table(
-- MAGIC     name="employees_scd2",
-- MAGIC     comment="SCD Type 2 employee dimension — replaces Oracle trigger pattern"
-- MAGIC )
-- MAGIC
-- MAGIC # Apply CDC changes into the SCD2 target
-- MAGIC dp.create_auto_cdc_flow(
-- MAGIC     target="employees_scd2",
-- MAGIC     source="employees_cdf",
-- MAGIC     keys=["employee_id"],
-- MAGIC     sequence_by=col("_commit_version"),
-- MAGIC     except_column_list=["_change_type", "_commit_version", "_commit_timestamp"],
-- MAGIC     stored_as_scd_type="2"
-- MAGIC )
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
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

-- MAGIC %md
-- MAGIC ### QUALIFY Clause
-- MAGIC
-- MAGIC Databricks SQL uses `QUALIFY` to filter the results of window functions. In Oracle, this would be implemented as a subquery or a CTE.

-- COMMAND ----------

-- DBTITLE 1,QUALIFY in Databricks SQL (SQL)
-- Retrieves the highest-paid employee in each department using QUALIFY.
SELECT 
    employee_id,
    first_name || ' ' || last_name AS employee_name,
    department_id,
    salary
FROM migration_dev.hr_raw.employees
QUALIFY ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) = 1
ORDER BY department_id;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
