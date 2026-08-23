# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
# MAGIC     <div style="font-size: 14px; color: #666;">
# MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
# MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
# MAGIC         <span style="margin-left: 8px;">06 - Closeout</span>
# MAGIC     </div>
# MAGIC     <div style="display: flex; align-items: center; gap: 8px;">
# MAGIC         <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="24" height="24" />
# MAGIC         <span style="color: #999; font-size: 16px;">-></span>
# MAGIC         <img src="https://cdn.simpleicons.org/databricks/FF3621" width="24" height="24"/>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img
# MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
# MAGIC     alt="Databricks Learning"
# MAGIC   >
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # Decommissioning and Closure
# MAGIC
# MAGIC With migration complete and workloads running successfully on Databricks, the final step is retiring the legacy Oracle environment. This lesson covers the decommissioning process, including data archival, connector shutdown, and formal engagement closure.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lesson, you will be able to:
# MAGIC
# MAGIC - Execute a controlled Oracle decommissioning plan
# MAGIC - Archive Oracle tables, stages, and metadata for compliance
# MAGIC - Shut down connectors and integrations pointing to Oracle
# MAGIC - Conduct final stakeholder review and close the migration engagement

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## 1. Decommissioning Timeline
# MAGIC
# MAGIC Decommissioning should follow a phased approach with validation gates at each stage.
# MAGIC
# MAGIC <div class="mermaid">
# MAGIC gantt
# MAGIC     title Oracle Decommissioning Timeline
# MAGIC     dateFormat YYYY-MM-DD
# MAGIC     axisFormat %b %d
# MAGIC     section Validation
# MAGIC     Parallel Run Complete           :done, v1, 2025-01-06, 1w
# MAGIC     section Wind-Down
# MAGIC     Read-Only Period                :active, r1, after v1, 2w
# MAGIC     Archive & Backup                :a1, after r1, 1w
# MAGIC     section Shutdown
# MAGIC     Connector Shutdown              :crit, c1, after a1, 1w
# MAGIC     Account Suspension              :milestone, s1, after c1, 0d
# MAGIC </div>
# MAGIC
# MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

# COMMAND ----------

# MAGIC %md
# MAGIC | Phase | Duration | Activities |
# MAGIC |-------|----------|------------|
# MAGIC | **Parallel Run Complete** | Week 0 | Confirm all workloads validated on Databricks |
# MAGIC | **Read-Only Period** | Weeks 1-2 | Oracle set to read-only; monitor for access attempts |
# MAGIC | **Archive & Backup** | Week 3 | Export data, metadata, and query history |
# MAGIC | **Connector Shutdown** | Week 4 | Disable all integrations and credentials |
# MAGIC | **Account Suspension** | Week 5+ | Suspend Oracle account; retain archives per policy |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Pre-Decommission Validation
# MAGIC
# MAGIC Before beginning decommissioning, confirm all migration success criteria are met.
# MAGIC
# MAGIC | Validation | Owner |
# MAGIC |------------|-------|
# MAGIC | All tables migrated and row counts validated | Data Engineering |
# MAGIC | All pipelines running successfully on Databricks | Data Engineering |
# MAGIC | BI tools reconnected and dashboards functional | Analytics |
# MAGIC | Data quality monitors active with no critical alerts | Data Engineering |
# MAGIC | User acceptance testing signed off | Business Stakeholders |
# MAGIC | Performance SLAs met or exceeded | Data Engineering |
# MAGIC | Security and compliance review complete | Security |
# MAGIC | Runbooks and documentation delivered | Project Team |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Archive and Backup
# MAGIC
# MAGIC Before shutting down Oracle, archive critical data and metadata for compliance and potential rollback.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### What to Archive
# MAGIC
# MAGIC | Asset | Archive Method | Retention |
# MAGIC |-------|----------------|-----------|
# MAGIC | **Table data** | Oracle Data Pump (`expdp`) to cloud storage, or `CREATE TABLE ... AS SELECT` to archive tablespace | Per data retention policy |
# MAGIC | **Historical query stats** | Export from `DBA_HIST_SQLSTAT` + `DBA_HIST_SQLTEXT` (AWR) | 1 year |
# MAGIC | **Audit trail** | Export from `UNIFIED_AUDIT_TRAIL` or `DBA_AUDIT_TRAIL` | Per compliance requirements |
# MAGIC | **DDL statements** | `DBMS_METADATA.GET_DDL()` for all objects | Permanent |
# MAGIC | **User and role definitions** | Export from `DBA_USERS`, `DBA_SYS_PRIVS`, `DBA_TAB_PRIVS`, `DBA_ROLE_PRIVS` | Permanent |
# MAGIC | **Scheduler jobs** | Export from `DBA_SCHEDULER_JOBS` and `DBMS_SCHEDULER.GET_DDL` | Permanent |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Oracle Archive Scripts
# MAGIC
# MAGIC <details>
# MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Export DDL for all schema objects (run in Oracle as DBA)</summary>
# MAGIC
# MAGIC <div class="code-block" data-language="sql">
# MAGIC -- Export DDL for all tables in a schema using DBMS_METADATA
# MAGIC SELECT
# MAGIC     t.table_name,
# MAGIC     DBMS_METADATA.GET_DDL('TABLE', t.table_name, t.owner) AS ddl
# MAGIC FROM dba_tables t
# MAGIC WHERE t.owner = 'HR'
# MAGIC ORDER BY t.table_name;
# MAGIC
# MAGIC -- Export complete schema DDL (tables, views, procedures, sequences, grants)
# MAGIC SELECT DBMS_METADATA.GET_DDL('SCHEMA', 'HR') AS schema_ddl FROM DUAL;
# MAGIC
# MAGIC -- Export all views
# MAGIC SELECT
# MAGIC     v.view_name,
# MAGIC     DBMS_METADATA.GET_DDL('VIEW', v.view_name, v.owner) AS ddl
# MAGIC FROM dba_views v
# MAGIC WHERE v.owner = 'HR'
# MAGIC ORDER BY v.view_name;
# MAGIC
# MAGIC -- Export stored procedures and functions
# MAGIC SELECT
# MAGIC     o.object_name,
# MAGIC     o.object_type,
# MAGIC     DBMS_METADATA.GET_DDL(o.object_type, o.object_name, o.owner) AS ddl
# MAGIC FROM dba_objects o
# MAGIC WHERE o.owner = 'HR'
# MAGIC   AND o.object_type IN ('PROCEDURE', 'FUNCTION', 'PACKAGE', 'PACKAGE BODY', 'TRIGGER')
# MAGIC ORDER BY o.object_type, o.object_name;
# MAGIC </div>
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC <details>
# MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Export query history for archival (requires Diagnostics Pack)</summary>
# MAGIC
# MAGIC <div class="code-block" data-language="sql">
# MAGIC -- Export historical SQL statistics from AWR (last 12 months)
# MAGIC SELECT
# MAGIC     s.parsing_schema_name        AS schema_name,
# MAGIC     s.sql_id,
# MAGIC     NVL(s.module, 'unknown')     AS module,
# MAGIC     t.sql_text,
# MAGIC     s.executions,
# MAGIC     ROUND(s.elapsed_time / 1e6, 2) AS total_elapsed_sec,
# MAGIC     ROUND(s.cpu_time     / 1e6, 2) AS total_cpu_sec,
# MAGIC     s.disk_reads,
# MAGIC     s.buffer_gets,
# MAGIC     s.last_active_time
# MAGIC FROM dba_hist_sqlstat s
# MAGIC JOIN dba_hist_sqltext t ON s.sql_id = t.sql_id AND s.dbid = t.dbid
# MAGIC WHERE s.last_active_time >= ADD_MONTHS(SYSDATE, -12)
# MAGIC   AND s.parsing_schema_name NOT IN ('SYS', 'SYSTEM', 'DBSNMP')
# MAGIC ORDER BY s.elapsed_time DESC;
# MAGIC
# MAGIC -- Export unified audit trail (Oracle 12c+)
# MAGIC SELECT
# MAGIC     event_timestamp,
# MAGIC     db_username,
# MAGIC     action_name,
# MAGIC     object_schema,
# MAGIC     object_name,
# MAGIC     sql_text,
# MAGIC     return_code
# MAGIC FROM unified_audit_trail
# MAGIC WHERE event_timestamp >= ADD_MONTHS(SYSDATE, -12)
# MAGIC ORDER BY event_timestamp DESC;
# MAGIC </div>
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC <details>
# MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Export users, roles, and privilege grants</summary>
# MAGIC
# MAGIC <div class="code-block" data-language="sql">
# MAGIC -- Export all non-system users
# MAGIC SELECT
# MAGIC     username,
# MAGIC     account_status,
# MAGIC     created,
# MAGIC     profile,
# MAGIC     default_tablespace,
# MAGIC     temporary_tablespace
# MAGIC FROM dba_users
# MAGIC WHERE username NOT IN ('SYS', 'SYSTEM', 'DBSNMP', 'APPQOSSYS', 'CTXSYS',
# MAGIC                        'DBSFWUSER', 'GGSYS', 'GSMADMIN_INTERNAL', 'LBACSYS',
# MAGIC                        'MDSYS', 'OJVMSYS', 'OLAPSYS', 'ORDDATA', 'ORDSYS',
# MAGIC                        'OUTLN', 'WMSYS', 'XDB')
# MAGIC ORDER BY username;
# MAGIC
# MAGIC -- Export role grants to users
# MAGIC SELECT grantee, granted_role, admin_option, default_role
# MAGIC FROM dba_role_privs
# MAGIC WHERE grantee NOT IN ('SYS', 'SYSTEM')
# MAGIC ORDER BY grantee, granted_role;
# MAGIC
# MAGIC -- Export system privilege grants
# MAGIC SELECT grantee, privilege, admin_option
# MAGIC FROM dba_sys_privs
# MAGIC WHERE grantee NOT IN ('SYS', 'SYSTEM', 'PUBLIC')
# MAGIC ORDER BY grantee, privilege;
# MAGIC
# MAGIC -- Export object-level grants
# MAGIC SELECT grantee, owner, table_name, privilege, grantable
# MAGIC FROM dba_tab_privs
# MAGIC WHERE grantee NOT IN ('SYS', 'SYSTEM', 'PUBLIC')
# MAGIC ORDER BY grantee, owner, table_name;
# MAGIC
# MAGIC -- Export Oracle Scheduler job definitions
# MAGIC SELECT
# MAGIC     owner,
# MAGIC     job_name,
# MAGIC     job_type,
# MAGIC     job_action,
# MAGIC     schedule_type,
# MAGIC     repeat_interval,
# MAGIC     enabled,
# MAGIC     state
# MAGIC FROM dba_scheduler_jobs
# MAGIC WHERE owner NOT IN ('SYS', 'SYSTEM', 'DBMS_SCHEDULER')
# MAGIC ORDER BY owner, job_name;
# MAGIC </div>
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
# MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
# MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
# MAGIC
# MAGIC <script>
# MAGIC (function() {
# MAGIC     function processCodeBlocks() {
# MAGIC         document.querySelectorAll('.code-block').forEach(function(block) {
# MAGIC             if (block.getAttribute('data-processed')) return;
# MAGIC             block.setAttribute('data-processed', 'true');
# MAGIC             var lang = block.getAttribute('data-language') || 'sql';
# MAGIC             var code = block.textContent.trim();
# MAGIC             var id = 'code-' + Math.random().toString(36).substr(2, 9);
# MAGIC             block.innerHTML = 
# MAGIC                 '<div style="position:relative;margin:16px 0;">' +
# MAGIC                     '<button class="copy-btn" style="position:absolute;top:8px;right:8px;padding:4px 12px;font-size:12px;background:#ddd;color:#333;border:1px solid #ccc;border-radius:4px;cursor:pointer;z-index:10;">Copy</button>' +
# MAGIC                     '<pre style="background:#f8f8f8;border-radius:8px;padding:16px;padding-top:40px;overflow-x:auto;margin:0;border:1px solid #e0e0e0;"><code id="' + id + '" class="language-' + lang + '" style="font-family:Consolas,Monaco,monospace;font-size:14px;"></code></pre>' +
# MAGIC                 '</div>';
# MAGIC             var codeEl = document.getElementById(id);
# MAGIC             codeEl.textContent = code;
# MAGIC             Prism.highlightElement(codeEl);
# MAGIC             block.querySelector('.copy-btn').onclick = function() {
# MAGIC                 var t = document.createElement('textarea');
# MAGIC                 t.value = code;
# MAGIC                 document.body.appendChild(t);
# MAGIC                 t.select();
# MAGIC                 document.execCommand('copy');
# MAGIC                 document.body.removeChild(t);
# MAGIC                 this.textContent = '✓ Copied!';
# MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
# MAGIC             };
# MAGIC         });
# MAGIC     }
# MAGIC     processCodeBlocks();
# MAGIC     document.querySelectorAll('details').forEach(function(details) {
# MAGIC         details.addEventListener('toggle', processCodeBlocks);
# MAGIC     });
# MAGIC })();
# MAGIC </script>

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Connector Shutdown
# MAGIC
# MAGIC Systematically disable all integrations pointing to Oracle.
# MAGIC
# MAGIC | Integration Type | Shutdown Action |
# MAGIC |------------------|-----------------|
# MAGIC | **BI Tools** (Tableau, Power BI, Looker) | Remove Oracle JDBC/ODBC connections; confirm Databricks SQL Warehouse connections active |
# MAGIC | **ETL/ELT Tools** (Informatica, ODI, GoldenGate, Fivetran) | Disable Oracle source connections; verify Databricks targets operational |
# MAGIC | **Application JDBC/ODBC connections** | Update connection strings in application config; rotate credentials |
# MAGIC | **Service accounts** | Lock or drop Oracle service users (`ALTER USER ... ACCOUNT LOCK`) |
# MAGIC | **Oracle Scheduler jobs** | Disable all jobs (`DBMS_SCHEDULER.DISABLE(job_name)`) |
# MAGIC | **Database links** | Drop all outbound DB links (`DROP DATABASE LINK link_name`) |
# MAGIC | **Replication / GoldenGate** | Stop and remove replication processes; archive trail files |
# MAGIC | **Oracle Data Pump export targets** | Confirm all scheduled exports redirected or retired |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">⚠️</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #e65100; font-size: 1.1em;">Monitor Before Shutdown</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">During the read-only period, monitor Oracle access logs to identify any overlooked integrations or users still attempting to connect. Address these before proceeding with account suspension.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Final Stakeholder Review
# MAGIC
# MAGIC Conduct a formal review with stakeholders to confirm migration success and close the engagement.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Success Metrics to Present
# MAGIC
# MAGIC - Tables migrated and validated
# MAGIC - Pipelines operational on Databricks
# MAGIC - Performance comparison (Oracle baseline vs. Databricks)
# MAGIC - Cost comparison (projected savings)
# MAGIC - User adoption and feedback

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Summary
# MAGIC
# MAGIC <div style="border-left: 4px solid #4caf50; background: #e8f5e9; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">✅</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #2e7d32; font-size: 1.1em;">Decommissioning Checklist</strong>
# MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
# MAGIC                 <li>All migration success criteria validated</li>
# MAGIC                 <li>Oracle data and metadata archived</li>
# MAGIC                 <li>Query and access history exported</li>
# MAGIC                 <li>All connectors and integrations disabled</li>
# MAGIC                 <li>Service accounts and API keys revoked</li>
# MAGIC                 <li>Data shares terminated</li>
# MAGIC                 <li>Final stakeholder review completed</li>
# MAGIC                 <li>Sign-off obtained from business stakeholders</li>
# MAGIC                 <li>Oracle account suspended</li>
# MAGIC                 <li>Migration engagement formally closed</li>
# MAGIC             </ul>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Congratulations!
# MAGIC
# MAGIC You have completed the Oracle to Databricks Migration course. Your organization is now running on the Databricks Data Intelligence Platform with Unity Catalog governance, Lakeflow pipelines, and enterprise-grade observability.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
