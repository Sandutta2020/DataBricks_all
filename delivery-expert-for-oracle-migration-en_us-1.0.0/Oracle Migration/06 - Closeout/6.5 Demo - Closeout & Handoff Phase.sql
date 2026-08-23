-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">06 - Closeout</span>
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
-- MAGIC # Demo: Closeout & Handoff Phase

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this demo, you will be able to:
-- MAGIC
-- MAGIC - Monitor job health, billing, and audit activity using Databricks system tables
-- MAGIC - Export Databricks metrics for integration with enterprise monitoring platforms (e.g., Splunk, Datadog)
-- MAGIC - Set up SQL Alerts for job failure notifications
-- MAGIC - Validate table migration and readiness before Oracle decommissioning
-- MAGIC - Audit and archive Oracle access and privilege data during system retirement

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
-- MAGIC ## Observability and Cost Monitoring

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 1. System Tables for Observability
-- MAGIC
-- MAGIC The queries below demonstrate monitoring job health, billing, and audit activity using Databricks system tables.

-- COMMAND ----------

-- DBTITLE 1,Query job run failures from system tables (SQL)
-- Job Run Health: failures in the last 7 days
SELECT
    j.name,
    r.run_id,
    r.result_state,
    ROUND((UNIX_TIMESTAMP(r.period_end_time) - UNIX_TIMESTAMP(r.period_start_time)) / 60, 1) AS duration_min,
    r.period_start_time
FROM system.lakeflow.job_run_timeline r
JOIN system.lakeflow.jobs j ON r.job_id = j.job_id
WHERE r.period_start_time >= CURRENT_TIMESTAMP - INTERVAL 7 DAYS
  AND r.result_state <> 'SUCCEEDED'
ORDER BY r.period_start_time DESC
LIMIT 10

-- COMMAND ----------

-- DBTITLE 1,Query Unity Catalog audit log for privilege changes (SQL)
-- Audit: Unity Catalog privilege changes in the last 7 days
SELECT
    event_time,
    user_identity.email     AS changed_by,
    request_params.changes  AS changes,
    response.status_code    AS status
FROM system.access.audit
WHERE event_time >= CURRENT_TIMESTAMP - INTERVAL 7 DAYS
  AND service_name = 'unityCatalog'
  AND action_name IN ('updatePermissions', 'updateSchema', 'createTable', 'deleteTable')
ORDER BY event_time DESC
LIMIT 50

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### 2. Enterprise Monitoring Integration
-- MAGIC
-- MAGIC Export Databricks metrics to your SIEM or APM platform. The query below produces a JSON-friendly payload that can be forwarded via webhook or Databricks SQL endpoint.
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Example: Forward billing metrics to Splunk / Datadog via webhook</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Stage hourly billing snapshot as JSON for SIEM ingestion
-- MAGIC SELECT TO_JSON(STRUCT(
-- MAGIC     DATE_TRUNC('hour', usage_start_time)  AS hour,
-- MAGIC     custom_tags['team']                   AS team,
-- MAGIC     sku_name,
-- MAGIC     SUM(usage_quantity)                   AS dbus
-- MAGIC )) AS metric_payload
-- MAGIC FROM system.billing.usage
-- MAGIC WHERE usage_start_time >= CURRENT_TIMESTAMP - INTERVAL 1 HOUR
-- MAGIC   AND custom_tags IS NOT NULL
-- MAGIC GROUP BY ALL
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
-- MAGIC                 this.textContent = '\u2713 Copied!';
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
-- MAGIC ### 3. Notification Destinations and SQL Alerts
-- MAGIC
-- MAGIC Attach a SQL Alert to the query below to receive notifications when job failures exceed a threshold.

-- COMMAND ----------

-- DBTITLE 1,SQL Alert query for job failure count (SQL)
-- SQL Alert query: count failed job runs in the last hour
-- Attach this query to a SQL Alert (Databricks > SQL > Alerts > Create alert)
-- Trigger condition: value > 0
-- Notification destination: PagerDuty / Slack / Email
SELECT COALESCE(COUNT(*), 0) AS failure_count
FROM system.lakeflow.job_run_timeline r
WHERE r.result_state = 'ERROR'
  AND r.period_end_time >= CURRENT_TIMESTAMP - INTERVAL 1 HOUR

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Decommissioning and Retirement

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### 1. Pre-Decommission Validation
-- MAGIC
-- MAGIC Before switching Oracle to read-only, verify all source tables have been created in the target schema.

-- COMMAND ----------

-- DBTITLE 1,List migrated tables in target schema (SQL)
-- List all tables in the target schema to verify migration completeness before decommission
SELECT
    t.table_catalog,
    t.table_schema,
    t.table_name,
    t.table_type
FROM system.information_schema.tables t
WHERE t.table_schema = 'hr_raw'
ORDER BY t.table_name


-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### 2. Archive and Backup
-- MAGIC
-- MAGIC Before shutting down Oracle, extract metadata and access history. Run the following queries in Oracle as a privileged user.
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Monitor read-only access attempts during wind-down (run in Oracle)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Identify sessions still connecting to Oracle during the read-only period
-- MAGIC -- Run daily; investigate any non-admin connections
-- MAGIC SELECT
-- MAGIC     s.username,
-- MAGIC     s.program,
-- MAGIC     s.machine,
-- MAGIC     s.osuser,
-- MAGIC     s.logon_time,
-- MAGIC     COUNT(*) AS session_count
-- MAGIC FROM v$session s
-- MAGIC WHERE s.username IS NOT NULL
-- MAGIC   AND s.username NOT IN ('SYS', 'SYSTEM', 'DBSNMP')
-- MAGIC GROUP BY s.username, s.program, s.machine, s.osuser, s.logon_time
-- MAGIC ORDER BY s.logon_time DESC;
-- MAGIC
-- MAGIC -- Audit write attempts (should be zero if Oracle is truly read-only)
-- MAGIC SELECT
-- MAGIC     db_username,
-- MAGIC     action_name,
-- MAGIC     object_schema,
-- MAGIC     object_name,
-- MAGIC     sql_text,
-- MAGIC     event_timestamp
-- MAGIC FROM unified_audit_trail
-- MAGIC WHERE event_timestamp >= SYSTIMESTAMP - INTERVAL '1' DAY
-- MAGIC   AND action_name IN ('INSERT', 'UPDATE', 'DELETE', 'TRUNCATE', 'DROP', 'CREATE')
-- MAGIC   AND db_username NOT IN ('SYS', 'SYSTEM')
-- MAGIC ORDER BY event_timestamp DESC;
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Export privilege grants before account suspension (run in Oracle)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Full privilege snapshot: roles, system privs, and object grants
-- MAGIC SELECT 'ROLE_GRANT'    AS grant_type, grantee, granted_role AS privilege_or_role,
-- MAGIC        NULL            AS object_owner, NULL AS object_name, admin_option AS extra
-- MAGIC FROM dba_role_privs WHERE grantee NOT IN ('SYS', 'SYSTEM')
-- MAGIC UNION ALL
-- MAGIC SELECT 'SYS_PRIV', grantee, privilege,
-- MAGIC        NULL, NULL, admin_option
-- MAGIC FROM dba_sys_privs WHERE grantee NOT IN ('SYS', 'SYSTEM', 'PUBLIC')
-- MAGIC UNION ALL
-- MAGIC SELECT 'OBJ_GRANT', grantee, privilege,
-- MAGIC        owner, table_name, grantable
-- MAGIC FROM dba_tab_privs WHERE grantee NOT IN ('SYS', 'SYSTEM', 'PUBLIC')
-- MAGIC ORDER BY grant_type, grantee;
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
-- MAGIC                 this.textContent = '\u2713 Copied!';
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

-- DBTITLE 1,Confirm oracle-migration tagged jobs are no longer active (SQL)
-- Cross-check: confirm no Oracle-sourced jobs are still active in Databricks
-- (tagged with oracle-migration project should have state = COMPLETED or STOPPED)
SELECT
    j.name,
    j.tags['project']  AS project_tag,
    MAX(r.period_end_time) AS last_run,
    MAX(r.result_state)    AS last_state
FROM system.lakeflow.jobs j
LEFT JOIN system.lakeflow.job_run_timeline r ON j.job_id = r.job_id
GROUP BY j.name, j.tags['project']
HAVING j.tags['project'] = 'oracle-migration'
ORDER BY last_run DESC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
