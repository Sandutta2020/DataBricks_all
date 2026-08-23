-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">00 - Foundations</span>
-- MAGIC     </div>
-- MAGIC     <div style="display: flex; align-items: center; gap: 8px;">
-- MAGIC         <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="24" height="24" />
-- MAGIC         <span style="color: #999; font-size: 16px;">-></span>
-- MAGIC         <img src="https://cdn.simpleicons.org/databricks/FF3621" width="24" height="24"/>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
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
-- MAGIC   </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Demo: Lakehouse Federation with Oracle
-- MAGIC
-- MAGIC This demo shows how to set up Lakehouse Federation to access an Oracle database from our Unity Catalog metastore.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this lesson, you will be able to:
-- MAGIC - Set up a user in Oracle
-- MAGIC - Create a connection object
-- MAGIC - Reach Oracle data in a foreign catalog

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
-- MAGIC ## Prerequisites
-- MAGIC
-- MAGIC - Databricks workspace with Unity Catalog enabled
-- MAGIC - Oracle account with a user that has appropriate privileges
-- MAGIC - Network connectivity between Databricks and Oracle (if Private Link or IP allowlisting are enabled)
-- MAGIC - The _human resources_ Oracle sample dataset installed into the `HR` schema in Oracle
-- MAGIC
-- MAGIC If you do not have the HR dataset already, install it from <a href="https://github.com/oracle-samples/db-sample-schemas/releases" target="_blank">Oracle's GitHub repository.</a>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## Step 1: Create a user in Oracle
-- MAGIC
-- MAGIC We will create a user for Lakehouse Federation specifically. This user will have a 0 quota, since the connection will be read-only.
-- MAGIC
-- MAGIC <details style="margin: 16px 0; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
-- MAGIC   <summary style="padding: 12px 16px; background: #f5f5f5; cursor: pointer; font-weight: 600; font-size: 1em;">
-- MAGIC     <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle:</span> Create Service User (click to expand)
-- MAGIC   </summary>
-- MAGIC   <div style="padding: 16px; background: #fafafa;">
-- MAGIC     <p style="margin: 0 0 12px 0; color: #333;">Create a Dedicated Oracle Service User for Databricks Lakehouse Federation:</p>
-- MAGIC     <div class="code-block" data-language="sql">
-- MAGIC -- Run in Oracle to create your service user
-- MAGIC CREATE USER DATABRICKS_FEDERATION_SVC
-- MAGIC IDENTIFIED BY "DbxFederation123!"
-- MAGIC DEFAULT TABLESPACE USERS
-- MAGIC TEMPORARY TABLESPACE TEMP
-- MAGIC QUOTA 0 ON USERS;
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC </details>
-- MAGIC
-- MAGIC <details style="margin: 16px 0; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
-- MAGIC   <summary style="padding: 12px 16px; background: #f5f5f5; cursor: pointer; font-weight: 600; font-size: 1em;">
-- MAGIC     <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle:</span> Grant Session Privilege to the Service User (click to expand)
-- MAGIC   </summary>
-- MAGIC   <div style="padding: 16px; background: #fafafa;">
-- MAGIC     <p style="margin: 0 0 12px 0; color: #333;">Grant the necessary privilege to allow the user to establish a session and connect to the Oracle database (adjust names as needed):</p>
-- MAGIC     <div class="code-block" data-language="sql">
-- MAGIC -- Allow login
-- MAGIC GRANT CREATE SESSION TO DATABRICKS_FEDERATION_SVC;
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC </details>
-- MAGIC
-- MAGIC Give the SVC the required privileges. There are two options for this. The first option is giving it access to **ALL** data, including metadata such as procedure codes and grants. This option can be incredibly helpful for migration: with this, you can e.g. check table schemas from within Databricks, and compare the results from the two systems in one query.
-- MAGIC
-- MAGIC <details style="margin: 16px 0; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
-- MAGIC   <summary style="padding: 12px 16px; background: #f5f5f5; cursor: pointer; font-weight: 600; font-size: 1em;">
-- MAGIC     <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle:</span> Option 1: SVC with High Privileges (click to expand)
-- MAGIC   </summary>
-- MAGIC   <div style="padding: 16px; background: #fafafa;">
-- MAGIC     <p style="margin: 0 0 12px 0; color: #333;">In this option, we give the SVC high privileges. This will be very useful during the migration, as it allows running metadata queries and comparing data from within Databricks.</p>
-- MAGIC     <div class="code-block" data-language="sql">
-- MAGIC -- Grant read access on all tables and metadata
-- MAGIC GRANT SELECT ANY TABLE TO DATABRICKS_FEDERATION_SVC;
-- MAGIC GRANT SELECT ANY DICTIONARY TO DATABRICKS_FEDERATION_SVC;
-- MAGIC GRANT SELECT ANY SEQUENCE TO DATABRICKS_FEDERATION_SVC;
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC </details>
-- MAGIC
-- MAGIC <details style="margin: 16px 0; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
-- MAGIC   <summary style="padding: 12px 16px; background: #f5f5f5; cursor: pointer; font-weight: 600; font-size: 1em;">
-- MAGIC     <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle:</span> Option 2: Give SVC  Limited Privileges (click to expand)
-- MAGIC   </summary>
-- MAGIC     <div style="padding: 16px; background: #fafafa;">
-- MAGIC     <p style="margin: 0 0 12px 0; color: #333;">This option limits federation to read some tables from the HR schema, being safer than the alternative.</p>
-- MAGIC     <div class="code-block" data-language="sql">
-- MAGIC -- Grant read access on HR tables
-- MAGIC GRANT SELECT ON hr.countries TO DATABRICKS_FEDERATION_SVC;
-- MAGIC GRANT SELECT ON hr.departments TO DATABRICKS_FEDERATION_SVC;
-- MAGIC GRANT SELECT ON hr.employees TO DATABRICKS_FEDERATION_SVC;
-- MAGIC GRANT SELECT ON hr.job_history TO DATABRICKS_FEDERATION_SVC;
-- MAGIC GRANT SELECT ON hr.jobs TO DATABRICKS_FEDERATION_SVC;
-- MAGIC GRANT SELECT ON hr.locations TO DATABRICKS_FEDERATION_SVC;
-- MAGIC GRANT SELECT ON hr.regions TO DATABRICKS_FEDERATION_SVC;
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC </details>
-- MAGIC
-- MAGIC
-- MAGIC <details style="margin: 16px 0; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
-- MAGIC   <summary style="padding: 12px 16px; background: #f5f5f5; cursor: pointer; font-weight: 600; font-size: 1em;">
-- MAGIC     <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle:</span> Verify User Setup (click to expand)
-- MAGIC   </summary>
-- MAGIC   <div style="padding: 16px; background: #fafafa;">
-- MAGIC     <p style="margin: 0 0 12px 0; color: #333;">Verify the service user is configured correctly:</p>
-- MAGIC     <div class="code-block" data-language="sql">
-- MAGIC -- Describe the Oracle user
-- MAGIC SELECT username,
-- MAGIC        account_status,
-- MAGIC        default_tablespace,
-- MAGIC        temporary_tablespace
-- MAGIC FROM dba_users
-- MAGIC WHERE username = 'DATABRICKS_FEDERATION_SVC';
-- MAGIC
-- MAGIC -- Show system privileges granted to the user
-- MAGIC SELECT privilege
-- MAGIC FROM dba_sys_privs
-- MAGIC WHERE grantee = 'DATABRICKS_FEDERATION_SVC';
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC </details>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
-- MAGIC
-- MAGIC <script>
-- MAGIC (function() {
-- MAGIC     document.querySelectorAll('.code-block').forEach(function(block) {
-- MAGIC         if (block.getAttribute('data-processed')) return;
-- MAGIC         block.setAttribute('data-processed', 'true');
-- MAGIC         var lang = block.getAttribute('data-language') || 'sql';
-- MAGIC         var label = lang === 'bash' ? 'Terminal' : 'Oracle';
-- MAGIC         var code = block.textContent.trim();
-- MAGIC         var id = 'code-' + Math.random().toString(36).substr(2, 9);
-- MAGIC         block.innerHTML = 
-- MAGIC             '<div style="position:relative;margin:16px 0;">' +
-- MAGIC                 '<div style="position:absolute;top:8px;left:12px;font-size:11px;color:#666;font-weight:600;text-transform:uppercase;">' + label + '</div>' +
-- MAGIC                 '<button class="copy-btn" style="position:absolute;top:8px;right:8px;padding:4px 12px;font-size:12px;background:#ddd;color:#333;border:1px solid #ccc;border-radius:4px;cursor:pointer;z-index:10;">Copy</button>' +
-- MAGIC                 '<pre style="background:#f8f8f8;border-radius:8px;padding:16px;padding-top:32px;overflow-x:auto;margin:0;border:1px solid #e0e0e0;"><code id="' + id + '" class="language-' + lang + '" style="font-family:Consolas,Monaco,monospace;font-size:13px;"></code></pre>' +
-- MAGIC             '</div>';
-- MAGIC         var codeEl = document.getElementById(id);
-- MAGIC         codeEl.textContent = code;
-- MAGIC         Prism.highlightElement(codeEl);
-- MAGIC         block.querySelector('.copy-btn').onclick = function() {
-- MAGIC             var t = document.createElement('textarea');
-- MAGIC             t.value = code;
-- MAGIC             document.body.appendChild(t);
-- MAGIC             t.select();
-- MAGIC             document.execCommand('copy');
-- MAGIC             document.body.removeChild(t);
-- MAGIC             this.textContent = '✓ Copied!';
-- MAGIC             setTimeout(() => this.textContent = 'Copy', 2000);
-- MAGIC         };
-- MAGIC     });
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## Step 2: Create a Connection to Oracle
-- MAGIC
-- MAGIC Create a connection object that defines how Databricks will authenticate to the Oracle database using JDBC credentials.
-- MAGIC
-- MAGIC **Prerequisites:**
-- MAGIC
-- MAGIC - **Host**: Oracle database host (e.g., `YOUR-ORACLE-HOST.amazonaws.com`)
-- MAGIC - **Port**: Oracle listener port (typically `1521`)
-- MAGIC - **User**: The Oracle service user created in Step 1 (e.g., `DATABRICKS_FEDERATION_SVC`)
-- MAGIC - **Database / Service Name**: Oracle service name (e.g., `ORCL`)
-- MAGIC - **Password**: Password for the Oracle service user
-- MAGIC
-- MAGIC <div style="background:#e7f3fe;border-left:4px solid #2196F3;padding:16px;border-radius:4px;margin:16px 0;">
-- MAGIC <strong>💡 Tip:</strong> Run this query in Oracle to list available service names:
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Run in Oracle to list available database services
-- MAGIC SELECT name
-- MAGIC FROM V$SERVICES;
-- MAGIC </div>
-- MAGIC You may see multiple services such as SYS$BACKGROUND, SYS$USERS, or application services like ORCL_A.
-- MAGIC For JDBC connections and Lakehouse Federation, use the main database service (e.g., ORCL or ORCL_A), not the internal SYS$ services.
-- MAGIC </div>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
-- MAGIC
-- MAGIC <script>
-- MAGIC (function() {
-- MAGIC     document.querySelectorAll('.code-block').forEach(function(block) {
-- MAGIC         if (block.getAttribute('data-processed')) return;
-- MAGIC         block.setAttribute('data-processed', 'true');
-- MAGIC         var lang = block.getAttribute('data-language') || 'sql';
-- MAGIC         var code = block.textContent.trim();
-- MAGIC         var id = 'code-' + Math.random().toString(36).substr(2, 9);
-- MAGIC         block.innerHTML = 
-- MAGIC             '<div style="position:relative;margin:16px 0;">' +
-- MAGIC                 '<div style="position:absolute;top:8px;left:12px;font-size:11px;color:#666;font-weight:600;text-transform:uppercase;">Oracle</div>' +
-- MAGIC                 '<button class="copy-btn" style="position:absolute;top:8px;right:8px;padding:4px 12px;font-size:12px;background:#ddd;color:#333;border:1px solid #ccc;border-radius:4px;cursor:pointer;z-index:10;">Copy</button>' +
-- MAGIC                 '<pre style="background:#f8f8f8;border-radius:8px;padding:16px;padding-top:32px;overflow-x:auto;margin:0;border:1px solid #e0e0e0;"><code id="' + id + '" class="language-' + lang + '" style="font-family:Consolas,Monaco,monospace;font-size:14px;"></code></pre>' +
-- MAGIC             '</div>';
-- MAGIC         var codeEl = document.getElementById(id);
-- MAGIC         codeEl.textContent = code;
-- MAGIC         Prism.highlightElement(codeEl);
-- MAGIC         block.querySelector('.copy-btn').onclick = function() {
-- MAGIC             var t = document.createElement('textarea');
-- MAGIC             t.value = code;
-- MAGIC             document.body.appendChild(t);
-- MAGIC             t.select();
-- MAGIC             document.execCommand('copy');
-- MAGIC             document.body.removeChild(t);
-- MAGIC             this.textContent = '✓ Copied!';
-- MAGIC             setTimeout(() => this.textContent = 'Copy', 2000);
-- MAGIC         };
-- MAGIC     });
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">Security Note</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">
-- MAGIC                 In production environments, use Databricks secrets to store credentials securely. Replace the Oracle password value with a secret reference: <code>secret('scope', 'password')</code>
-- MAGIC             </p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- DBTITLE 1,Create Connection
-- Create connection
DROP CONNECTION IF EXISTS oracle_federation;

CREATE CONNECTION oracle_federation
TYPE oracle
OPTIONS (
  host 'core-de-oracle-import-test.ckmlzxlvr0pu.eu-central-1.rds.amazonaws.com',
  port '1521',
  user 'DATABRICKS_FEDERATION_SVC',
  password secret('oracle_migration', 'oracle_password')
);

-- COMMAND ----------

-- DBTITLE 1,Describe Connection
-- Describe the connection object
DESCRIBE CONNECTION EXTENDED oracle_federation;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Let's test the connection with a query that will be executed on Oracle

-- COMMAND ----------

-- DBTITLE 1,Test Connection
SELECT * FROM remote_query(
  'oracle_federation',
  service_name => 'ORCL',
  query => "SELECT 'hello' FROM DUAL;")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Step 3: Create a Foreign Catalog
-- MAGIC
-- MAGIC Create a foreign catalog that mirrors the Oracle database structure in Unity Catalog:

-- COMMAND ----------

-- DBTITLE 1,Create Foreign Catalog
-- Create foreign catalog
DROP CATALOG IF EXISTS oracle_federation_catalog;

CREATE FOREIGN CATALOG oracle_federation_catalog
USING CONNECTION oracle_federation
OPTIONS (
  service_name 'ORCL'
);

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Step 4: Explore the Federated Catalog
-- MAGIC
-- MAGIC Once the foreign catalog is created, you can explore the Oracle schemas and tables directly from Databricks:

-- COMMAND ----------

-- DBTITLE 1,Show Schemas
-- List schemas in the federated catalog
SHOW SCHEMAS IN oracle_federation_catalog;

-- COMMAND ----------

-- DBTITLE 1,Show Tables
-- List tables in a specific schema
SHOW TABLES IN oracle_federation_catalog.hr;

-- COMMAND ----------

-- DBTITLE 1,Describe Table
-- Describe a federated table
DESCRIBE TABLE oracle_federation_catalog.hr.employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Step 5: Query Federated Data
-- MAGIC
-- MAGIC Query Oracle tables directly from Databricks without moving data:

-- COMMAND ----------

-- DBTITLE 1,Query Federated Data
-- Query an Oracle table from Databricks
SELECT * FROM oracle_federation_catalog.hr.employees;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Step 6: Query Pushdown
-- MAGIC
-- MAGIC Lakehouse Federation optimizes queries by pushing down predicates, projections, and aggregations to Oracle where possible. This minimizes data transfer and leverages Oracle's compute for filtering and aggregations before results are returned to Databricks.
-- MAGIC
-- MAGIC The following cell will generate the physical plan for the query below. You will see that Databricks:
-- MAGIC - Reads only the required columns
-- MAGIC - Pushes the filter down to Oracle
-- MAGIC
-- MAGIC This reduces the amount of data transferred.

-- COMMAND ----------

-- DBTITLE 1,Query Pushdown Example
EXPLAIN SELECT first_name, last_name
FROM oracle_federation_catalog.hr.employees
WHERE STARTSWITH(FIRST_NAME, 'K')

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">💡</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Supported Pushdowns</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">
-- MAGIC                 <a href="https://docs.databricks.com/aws/en/query-federation/oracle#supported-pushdowns" target="_blank">You can find the supported pushdowns here.</a>
-- MAGIC             </p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Cleanup
-- MAGIC
-- MAGIC Remove the demo resources when no longer needed:

-- COMMAND ----------

-- DBTITLE 1,Drop Demo Objects
-- Cleanup Unity Catalog resources (run in Databricks)

-- DROP CATALOG IF EXISTS oracle_federation_catalog;
-- DROP CONNECTION IF EXISTS oracle_federation;

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
