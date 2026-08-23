-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">02 - Design</span>
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

-- MAGIC %md
-- MAGIC # Solution Architecture and Modeling
-- MAGIC
-- MAGIC This lesson translates discovery insights into a concrete technical blueprint for the Databricks Lakehouse. You will map Oracle constructs to their Databricks equivalents and design the target data flow architecture.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this lesson, you will be able to:
-- MAGIC
-- MAGIC - Define Databricks Data Intelligence Platform target architecture
-- MAGIC - Map Oracle constructs (PL/SQL, DBMS_SCHEDULER, Flashback) to Databricks features
-- MAGIC - Select appropriate ingestion and CDC strategies (Lakeflow Connect vs JDBC)
-- MAGIC - Plan data engineering workflows using Lakeflow Spark Declarative Pipelines and Jobs
-- MAGIC - Define lineage tracking and governance integration points in Unity Catalog
-- MAGIC - Validate performance, scalability, and cost expectations; baseline metrics

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 1. Target Platform: Data Intelligence Platform
-- MAGIC
-- MAGIC The Databricks Data Intelligence Platform provides a unified foundation for your migration, combining AI, ETL, orchestration, and analytics on a governed data layer.
-- MAGIC <br/>
-- MAGIC
-- MAGIC <div style="border: 2px solid #4A7A8A; border-radius: 8px; overflow: hidden; font-family: sans-serif; text-align: center;">
-- MAGIC   <div style="background: #2D4F5F; color: #fff; padding: 14px; font-size: 1.05em;">
-- MAGIC     <b>Databricks Data Intelligence Platform</b>
-- MAGIC   </div>
-- MAGIC   <div style="display: flex;">
-- MAGIC     <div style="flex: 1 1 25%; background: #2D4F5F; color: #fff; border: 1px solid #4A7A8A; padding: 12px;">
-- MAGIC       <b>Lakeflow</b><br/><i>Ingestion, Orchestration,<br/>data quality</i>
-- MAGIC     </div>
-- MAGIC     <div style="flex: 1 1 25%; background: #2D4F5F; color: #fff; border: 1px solid #4A7A8A; padding: 12px;">
-- MAGIC       <b>Databricks SQL</b><br/><i>Data Warehousing,<br/>queries and alerts</i>
-- MAGIC     </div>
-- MAGIC     <div style="flex: 1 1 25%; background: #2D4F5F; color: #fff; border: 1px solid #4A7A8A; padding: 12px;">
-- MAGIC       <b>AI/BI</b><br/><i>AI Guided<br/>Business Intelligence</i>
-- MAGIC     </div>
-- MAGIC     <div style="flex: 1 1 25%; background: #2D4F5F; color: #fff; border: 1px solid #4A7A8A; padding: 12px;">
-- MAGIC       <b>Mosaic AI</b><br/><i>Create, tune and<br/>serve custom AI Apps</i>
-- MAGIC     </div>
-- MAGIC   </div>
-- MAGIC   <div style="background: #3D6B7A; color: #fff; border-top: 1px solid #5A9AAA; padding: 12px;">
-- MAGIC     <b>Data Intelligence Engine</b><br/><i>Use generative AI to understand the semantics of your data</i>
-- MAGIC   </div>
-- MAGIC   <div style="background: #4A8090; color: #fff; border-top: 1px solid #6AB0C0; padding: 12px;">
-- MAGIC     <b>Unity Catalog</b><br/><i>Unified security, governance and cataloging</i>
-- MAGIC   </div>
-- MAGIC   <div style="background: #5A90A0; color: #fff; border-top: 1px solid #7AC0D0; padding: 12px;">
-- MAGIC     <b>Delta Lake</b><br/><i>Unified data storage for reliability and sharing</i>
-- MAGIC   </div>
-- MAGIC   <div style="background: #1a2f3a; color: #fff; border-top: 1px solid #4A7A8A; padding: 12px;">
-- MAGIC     <b>Open Data Lake</b><br/><i>All raw data (logs, texts, audio, video, images)</i>
-- MAGIC   </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;">   &nbsp;Component</span> | Role | Replaces |
-- MAGIC |-----------|------|----------|
-- MAGIC | **Unity Catalog** | Unified governance for data, AI assets, and files; lineage tracking; access control | Oracle Data Dictionary (ALL_OBJECTS, etc.) + RBAC |
-- MAGIC | **Delta Lake** | Open table format providing ACID transactions, time travel, schema evolution, and optimized storage | Oracle proprietary storage, Tablespaces, and Segments |
-- MAGIC | **Lakeflow Connect** | Managed data ingestion with connectors, Auto Loader, and Streaming Tables | GoldenGate, Oracle Data Integrator (ODI), SQL*Loader |
-- MAGIC | **Lakeflow Jobs** | Orchestration and scheduling for multi-task workflows with dependencies, alerts, and retries | DBMS_SCHEDULER, Cron, Control-M, Autosys |
-- MAGIC | **Lakeflow Spark Declarative Pipelines** | Declarative ETL with automatic dependency management, data quality constraints, and incremental processing | PL/SQL ETL procedures, Materialized Views, Triggers, dbt, Talend |
-- MAGIC | **SQL Warehouses** | Serverless SQL compute for BI queries and analytics workloads | Oracle Instances / RAC Nodes (for analytics) |
-- MAGIC | **AI/BI** | AI-powered dashboards with natural language queries (Genie) and automated insights | Oracle Business Intelligence (OBIEE), Oracle Analytics Cloud (OAC) |
-- MAGIC | **Mosaic AI** | End-to-end ML platform for training, fine-tuning, and serving models including LLMs | Oracle Machine Learning (OML) |
-- MAGIC | **Compute management** | Cluster policies, multi-clustering, Intelligent Workload Management, autoscaling | Automatic Workload Repository (AWR), Active Session History (ASH), Real Application Clusters (RAC) - all included in extra licenses |
-- MAGIC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Assess Oracle-Specific Features</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Many Oracle environments rely heavily on proprietary PL/SQL logic, packages, and custom triggers. During discovery, identify which of these are core business logic versus pure data movement. Use <b>Lakeflow Connect</b> to handle the physical data movement (replacing GoldenGate or ODI). For  refactoring the logic, use Spark SQL or Python code to address the functional migration.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 2. Namespace and Governance Structure
-- MAGIC
-- MAGIC Mapping the Oracle instance/schema structure to the Databricks catalog/schema model is a critical design step.
-- MAGIC
-- MAGIC <div class="mermaid">
-- MAGIC flowchart TB
-- MAGIC     subgraph OR["Oracle"]
-- MAGIC         direction TB
-- MAGIC         ORI["<b>Instance / CDB</b><br/><i>Database context</i>"]
-- MAGIC         ORP["<b>PDB</b><br/><i>Database isolation</i>"]
-- MAGIC         ORS["<b>Schema</b><br/><i>Tenant/User isolation</i>"]
-- MAGIC         OROBJ["<b>Objects</b><br/><i>tables, views, packages,<br/>stored procedures, triggers</i>"]
-- MAGIC         ORI --> ORP --> ORS --> OROBJ
-- MAGIC     end
-- MAGIC     subgraph DB["Databricks"]
-- MAGIC         direction TB
-- MAGIC         DBA["<b>Account</b><br/><i>admin + billing</i>"]
-- MAGIC         DBM["<b>Metastore</b><br/><i>governance (regional)</i>"]
-- MAGIC         DBW["<b>Workspace</b><br/><i>compute environment</i>"]
-- MAGIC         DBC["<b>Catalog</b>"]
-- MAGIC         DBS["<b>Schema</b>"]
-- MAGIC         DBOBJ["<b>Objects</b><br/><i>tables, views, volumes,<br/>models, functions</i>"]
-- MAGIC         DBA --> DBM
-- MAGIC         DBA --> DBW
-- MAGIC         DBW -.->|attaches to| DBM
-- MAGIC         DBM --> DBC --> DBS --> DBOBJ
-- MAGIC     end
-- MAGIC     style OR fill:#fff,stroke:#F80102,stroke-width:2px
-- MAGIC     style DB fill:#fff,stroke:#FF3621,stroke-width:2px
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="24" height="24" /></span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">Oracle CDB / PDB Multi-Tenancy</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">
-- MAGIC                 Most enterprise Oracle 19c deployments use the <b>Container Database (CDB)</b> architecture with one or more <b>Pluggable Databases (PDBs)</b>. This affects migration strategy:
-- MAGIC             </p>
-- MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li>Each PDB maps to a separate <b>Databricks catalog</b> (or a top-level schema namespace within a shared catalog for smaller workloads).</li>
-- MAGIC                 <li>CDB-level objects (common users <code>C##</code>, common roles, <code>CDB_*</code> views) require schema-level export via Data Pump (<code>expdp</code>) rather than a full database dump.</li>
-- MAGIC                 <li>Confirm with the Oracle DBA whether you are migrating from a CDB/PDB or a legacy non-CDB instance — the DDL extraction commands and connection strings differ.</li>
-- MAGIC             </ul>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC | Aspect | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
-- MAGIC |--------|-----------|------------|
-- MAGIC | **Top-level admin** | Sysadmin / DBA | Account Admin |
-- MAGIC | **Isolation boundary** | Instance / CDB / PDB | Workspace (compute) / Catalog (data) |
-- MAGIC | **Governance scope** | Local Data Dictionary | Metastore (cross-workspace) |
-- MAGIC | **Namespace pattern** | `SCHEMA.OBJECT` (within DB) | `catalog.schema.object` |
-- MAGIC | **Data Sharing** | DB Links / Data Pump | Delta Sharing (open protocol) |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3. Core Construct Mapping
-- MAGIC
-- MAGIC Map your discovered Oracle objects to their Databricks equivalents:
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle Object</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks Equivalent</span> | Migration Notes |
-- MAGIC |------------------|----------------------|-----------------|
-- MAGIC | **Database / Instance** | Catalog | Align to business domain, environment (Dev/Prod), or both |
-- MAGIC | **Schema / User** | Schema | Direct mapping within a Catalog |
-- MAGIC | **Table** | Managed Delta table | Automatic optimization (Liquid Clustering) |
-- MAGIC | **View** | View | Minor SQL syntax adjustments for Spark SQL |
-- MAGIC | **Materialized View** | Materialized view | Use Lakeflow Spark Declarative Pipelines |
-- MAGIC | **Stored Procedure** | Notebook / Python code / SQL stored procedure | Complex PL/SQL is best refactored to Python notebooks |
-- MAGIC | **Package** | Python module / notebooks | Group related logic into modular notebooks or libs |
-- MAGIC | **Trigger** | Lakeflow Spark Declarative Pipeline / Change Data Feed (CDF) | Replace procedural triggers with event-driven pipelines |
-- MAGIC | **DBMS_SCHEDULER Job** | Lakeflow Job | Full DAG orchestration with triggers and alerts |
-- MAGIC | **Sequence** | Identity column | `GENERATED BY DEFAULT AS IDENTITY` (`BIGINT` only)|
-- MAGIC | **Partition (Range/Hash)** | Liquid clustering or partitioning | Use partitioning above 1 TB |
-- MAGIC | **Flashback** | Delta time travel | `VERSION AS OF`, `TIMESTAMP AS OF` |
-- MAGIC | **DB Link** | Lakehouse Federation | Direct query access to external sources via UC |
-- MAGIC | **Synonym** | No direct counterpart | Re-implement as views in Unity Catalog |
-- MAGIC | **Tablespace** | Managed storage location | Defined at metastore, catalog or schema level in UC |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 4. Medallion Architecture Design
-- MAGIC
-- MAGIC Design your data flow using the bronze-silver-gold pattern. This architecture provides clear separation of concerns and enables incremental processing.
-- MAGIC
-- MAGIC <div class="mermaid">
-- MAGIC flowchart LR
-- MAGIC     Sources["Data<br/>Sources"] --> Bronze["<b>Bronze</b><br/><i>Raw Ingestion</i>"]
-- MAGIC     Bronze --> Silver["<b>Silver</b><br/><i>Cleansed</i>"]
-- MAGIC     Silver --> Gold["<b>Gold</b><br/><i>Curated</i>"]
-- MAGIC     Gold --> Consumers["AI/BI /<br/>Apps"]
-- MAGIC     style Bronze fill:#D2691E,color:#fff
-- MAGIC     style Silver fill:#C0C0C0,color:#000
-- MAGIC     style Gold fill:#FFD700,color:#000
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC | Layer | Purpose | Transformations | Typical Consumers |
-- MAGIC |-------|---------|-----------------|-------------------|
-- MAGIC | **Bronze** | Raw data preservation, audit trail, the **Data Lake** in the Lakehouse architecture | Schema inference, metadata tagging, append-only | Data engineers (debugging, replay) |
-- MAGIC | **Silver** | Cleansed, conformed, deduplicated | Type casting, validation, CDC merge, SCD handling | Data scientists, analysts |
-- MAGIC | **Gold** | Business-ready aggregates, late binding, application specific integration | Joins, aggregations, denormalization, metrics | BI tools, applications, ML features |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 5. CDC and Incremental Processing Strategy
-- MAGIC
-- MAGIC Replace Oracle GoldenGate or legacy CDC patterns with Delta Change Data Feed (CDF) for internal tracking and Lakeflow Connect for external ingestion:
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle Pattern</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks Pattern</span> | Implementation |
-- MAGIC |-------------------|-------------------|----------------|
-- MAGIC | GoldenGate / CDC | `AUTO CDC INTO` | Simplified change data capture Lakeflow Spark Declarative Pipelines |
-- MAGIC | Trigger-based logging | Delta CDF | `ALTER TABLE SET TBLPROPERTIES (delta.enableChangeDataFeed = true)` |
-- MAGIC | Materialized Views | Materialized Views | No query rewrite in Databricks |
-- MAGIC | Sequential Processing | Streaming Read | Streaming tables in Lakeflow Spark Declarative Pipelines or `spark.readStream.table("bronze.events")` |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC Lakeflow Spark Declarative Pipelines (SDP) simplifies change data capture (CDC) with AUTO CDC INTO
-- MAGIC <br/>
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 AUTO CDC INTO Example</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Create and populate the target table.
-- MAGIC CREATE OR REFRESH STREAMING TABLE target;
-- MAGIC
-- MAGIC CREATE FLOW target_flow
-- MAGIC AS AUTO CDC INTO
-- MAGIC   target
-- MAGIC FROM
-- MAGIC   stream(cdc_data.users)
-- MAGIC KEYS
-- MAGIC   (userId)
-- MAGIC APPLY AS DELETE WHEN
-- MAGIC   operation = "DELETE"
-- MAGIC SEQUENCE BY
-- MAGIC   sequenceNum
-- MAGIC COLUMNS * EXCEPT
-- MAGIC   (operation, sequenceNum)
-- MAGIC STORED AS
-- MAGIC   SCD TYPE 2;
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
-- MAGIC ## 6. Data Engineering Workflows
-- MAGIC
-- MAGIC Planning your workflow orchestration requires understanding how Oracle job patterns map to Databricks capabilities.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Lakeflow Jobs: Replacing DBMS_SCHEDULER
-- MAGIC
-- MAGIC Lakeflow Jobs provide full DAG orchestration with richer capabilities than Oracle's scheduler:
-- MAGIC
-- MAGIC | Aspect | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle DBMS_SCHEDULER</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Lakeflow Jobs</span> |
-- MAGIC |--------|------------------|----------------------|
-- MAGIC | **Scheduling** | Calendaring, event-based, and chains | Scheduled (CRON), file arrival, table change, continuous triggers or API calls |
-- MAGIC | **Dependencies** | Job Chains | Multi-task jobs with complex DAG dependencies |
-- MAGIC | **Compute** | Shared instance resources | Job-specific clusters or serverless compute |
-- MAGIC | **Monitoring** | `DBA_SCHEDULER_JOB_RUN_DETAILS` | Jobs UI with run history, metrics, and alerts |
-- MAGIC | **Alerting** | `DBMS_SCHEDULER.SET_ATTRIBUTE` | Native email, Teams, Slack, PagerDuty, webhook integrations |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Lakeflow Spark Declarative Pipelines: Replacing Triggers + PL/SQL
-- MAGIC
-- MAGIC For incremental ETL patterns, Lakeflow Spark Declarative Pipelines provides a superior declarative approach:
-- MAGIC
-- MAGIC | Aspect | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle Triggers / PL/SQL</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Lakeflow Spark Declarative Pipelines</span> |
-- MAGIC |--------|---------------------------|--------------------------------|
-- MAGIC | **Definition** | Imperative (row-by-row or manual merge) | Declarative (define queries, system handles refresh) |
-- MAGIC | **Dependencies** | Manual handling of execution order | Automatic dependency resolution |
-- MAGIC | **Data Quality** | Manual exception handling | Built-in expectations with configurable actions |
-- MAGIC | **Recovery** | Manual rollback / redo handling | Automatic checkpointing and recovery, Delta versioning |
-- MAGIC | **Monitoring** | Query custom audit tables | UI, pipeline event log and lineage graph |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### When to Use Each
-- MAGIC
-- MAGIC - **Scheduled batch ETL** (nightly aggregations, reports) - Lakeflow Jobs with SQL or notebook tasks
-- MAGIC - **Incremental/streaming ETL** (CDC processing, real-time dashboards) - Lakeflow Spark Declarative Pipelines
-- MAGIC - **Complex orchestration** (multi-system workflows with conditions) - Lakeflow Jobs with branching logic
-- MAGIC - **Simple table refresh** (single-table materializations) - Lakeflow Spark Declarative Pipelines Materialized Views

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 7. Migration Compatibility Assessment
-- MAGIC
-- MAGIC Understanding what translates directly versus what requires redesign helps prioritize migration effort.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Migration Effort by Pattern
-- MAGIC
-- MAGIC | Category | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> | Effort |
-- MAGIC |----------|-----------|------------|--------|
-- MAGIC | **Standard SQL** | `SELECT`, `JOIN`, `GROUP BY`, `WINDOW` | Same syntax | 🟢 Direct |
-- MAGIC | **Basic DDL** | `CREATE TABLE`, `CREATE VIEW` | Same syntax | 🟢 Direct |
-- MAGIC | **Flashback** | `AS OF TIMESTAMP / SCN` | `TIMESTAMP AS OF` / `VERSION AS OF` | 🟢 Direct |
-- MAGIC | **Access Control** | `GRANT`, `REVOKE` on objects | `GRANT`, `REVOKE` via Unity Catalog | 🟢 Direct |
-- MAGIC | **Common Functions** | `COALESCE`, `NVL`, `DECODE` | Native or equivalent functions | 🟢 Direct |
-- MAGIC | **Stored Procedures** | PL/SQL logic, cursors | Refactor to notebooks (Python/SQL) or Lakeflow Spark Declarative Pipelines | 🟠 Redesign |
-- MAGIC | **Packages** | Modular PL/SQL groupings | Refactor to Python modules / libraries, Lakebridge for initial solution | 🟠 Redesign |
-- MAGIC | **Hierarchical Queries** | `CONNECT BY`, `START WITH` | `WITH RECURSIVE` (recursive CTEs) | 🟠 Redesign |
-- MAGIC | **Job Chains** | Complex scheduler dependencies | Lakeflow Jobs with conditional tasks | 🟠 Redesign |
-- MAGIC | **Triggers** | Procedural CDC logic | Lakeflow Spark Declarative Pipelines with `AUTO CDC INTO` and CDF | 🟠 Redesign |
-- MAGIC | **JSON/XML** | `JSON_VALUE`, `XMLTABLE` | `from_json()`, `xpath()` | 🟠 Redesign |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Function Mapping Reference
-- MAGIC
-- MAGIC Common Oracle-specific functions and their Databricks equivalents:
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
-- MAGIC |-----------|------------|
-- MAGIC | `NVL(a, b)` | `nvl(a, b)` or more commonly `coalesce(a, b)` |
-- MAGIC | `DECODE(x, val1, res1, ...)` | `decode(x, val1, res1, ...)` or more commonly `CASE` |
-- MAGIC | `SYSDATE` | `current_date()` or `current_timestamp()` |
-- MAGIC | `TO_CHAR(dt, 'YYYY-MM-DD')` | `date_format(dt, 'yyyy-MM-dd')` |
-- MAGIC | `TO_DATE(str, 'YYYY-MM-DD')` | `to_date(str, 'yyyy-MM-dd')` |
-- MAGIC | `LISTAGG(col, ',')` | `array_join(collect_list(col), ',')` |
-- MAGIC | `SUBSTR(str, start, len)` | `substring(str, start, len)` |
-- MAGIC
-- MAGIC For a complete list of built-in SQL functions, see <a href="https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-functions-builtin">the reference.</a>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 8. Lineage and Governance Integration
-- MAGIC
-- MAGIC Unity Catalog automatically captures lineage across your Lakehouse:
-- MAGIC
-- MAGIC | Lineage Type | Captured By | Visualization |
-- MAGIC |--------------|-------------|---------------|
-- MAGIC | Table-to-table | Unity Catalog (automatic) | Catalog Explorer lineage tab |
-- MAGIC | Column-level | Unity Catalog (automatic) | Column lineage graph |
-- MAGIC | Job-to-table | Lakeflow Job runs | Job lineage in Jobs UI |
-- MAGIC | ETL/Pipeline | Lakeflow SDP runtime | Pipeline DAG view |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Governance Design Decisions
-- MAGIC
-- MAGIC Document these decisions for your migration:
-- MAGIC
-- MAGIC ❓ **Regional/Metastore topology**: Single region or multiple regions?  
-- MAGIC ❓ **Workspace strategy**: By environment (`dev`, `prod`), by team, or by workload type (ETL vs analytics)?  
-- MAGIC ❓ **Catalog structure**: By environment (`dev`, `prod`) or by domain (`sales`, `finance`)?  
-- MAGIC ❓ **Schema naming**: Mirror Oracle schemas or redesign?  
-- MAGIC ❓ **Ownership model**: Team-based or individual owners?  
-- MAGIC ❓ **Access patterns**: RBAC only or ABAC with row/column filters?  

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 9. Performance and Cost Baseline
-- MAGIC
-- MAGIC Before migration, establish baseline metrics from Oracle to validate post-migration:
-- MAGIC
-- MAGIC | Metric Category | What to Capture | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle Source</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks Equivalent</span> |
-- MAGIC |-----------------|-----------------|------------------|----------------------|
-- MAGIC | **Query Performance** | P50/P95 latency | `V$SQL` / AWR Reports | `system.query.history` |
-- MAGIC | **Pipeline Duration** | Job execution times | `DBA_SCHEDULER_JOB_RUN_DETAILS` | Lakeflow Jobs run history |
-- MAGIC | **Compute Cost** | License + Infrastructure cost | Licensing audits | `system.billing.usage` |
-- MAGIC | **Storage** | Table/Index sizes | `DBA_SEGMENTS` | `DESCRIBE DETAIL table_name` |
-- MAGIC | **Freshness** | Data latency | Custom audit tables | Lakeflow Spark Declarative Pipeline event log |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚡</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Photon Acceleration</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">
-- MAGIC                 Enable <b>Photon</b> on all clusters used for SQL-heavy migrated workloads. Photon is a vectorized query engine written in C++ that delivers <b>2-12x throughput improvements</b> on joins, aggregations, and table scans — the operations most common in Oracle OLAP and reporting SQL. Photon incurs no additional per-query cost (included in the DBU rate for Photon-enabled instance types).
-- MAGIC             </p>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">
-- MAGIC                 <b>Serverless SQL Warehouses</b> start in a few seconds and scale concurrency automatically — ideal for BI workloads replacing Oracle's always-on OLAP schemas. 
-- MAGIC             </p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Summary
-- MAGIC
-- MAGIC In this lesson, you designed the target architecture for your Oracle to Databricks migration:
-- MAGIC
-- MAGIC - **Platform Foundation** - The Databricks Data Intelligence Platform provides unified governance (Unity Catalog), open storage (Delta Lake), and integrated AI capabilities as the target for your migration.
-- MAGIC - **Construct Mapping** - Oracle objects map to Databricks equivalents: schemas->schemas, Flashback->Delta Time Travel, DBMS_SCHEDULER->Lakeflow Jobs, and PL/SQL->Notebooks.
-- MAGIC - **Data Flow Design** - The Medallion Architecture (Bronze/Silver/Gold) structures your data processing with clear separation between raw ingestion, cleansed data, and business-ready aggregates.
-- MAGIC - **Workflow Planning** - Lakeflow Jobs replace scheduled jobs for orchestration; Lakeflow Spark Declarative Pipelines replace procedural ETL and Triggers with declarative, automatically-managed incremental processing.
-- MAGIC - **Compatibility Assessment** - Standard SQL and DDL translate directly; PL/SQL packages, procedures, and complex triggers require redesign using notebooks and Python/SQL scripting.
-- MAGIC - **Governance & Observability** - Unity Catalog provides automatic lineage tracking and unified access control; system tables replace Oracle's `V$SQL` and `DBA_SEGMENTS` for monitoring.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## References
-- MAGIC
-- MAGIC - [Unity Catalog Documentation](https://docs.databricks.com/en/data-governance/unity-catalog/index.html)
-- MAGIC - [Lakeflow Spark Declarative Pipelines Guide](https://docs.databricks.com/aws/en/ldp)
-- MAGIC - [Lakeflow Jobs](https://docs.databricks.com/en/jobs/index.html)
-- MAGIC - [Delta Time Travel](https://docs.databricks.com/en/delta/history.html)
-- MAGIC - [Databricks SQL Reference](https://docs.databricks.com/en/sql/language-manual/index.html)

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
