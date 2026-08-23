# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
# MAGIC     <div style="font-size: 14px; color: #666;">
# MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
# MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
# MAGIC         <span style="margin-left: 8px;">01 - Discover</span>
# MAGIC     </div>
# MAGIC     <div style="display: flex; align-items: center; gap: 8px;">
# MAGIC         <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="24" height="24" />
# MAGIC         <span style="color: #999; font-size: 16px;">-></span>
# MAGIC         <img src="https://cdn.simpleicons.org/databricks/FF3621" width="24" height="24"/>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img
# MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
# MAGIC     alt="Databricks Learning"
# MAGIC   >
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # Discovery and Landscape Analysis
# MAGIC
# MAGIC Discovery is the foundation of accurate migration planning. This lesson walks through the systematic discovery of an Oracle environment, covering the strategy, profiling, and analysis required to build a complete migration roadmap.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lesson, you will be able to:
# MAGIC
# MAGIC - Define the scope and priorities of a migration based on business value and technical readiness
# MAGIC - Profile the environment to map upstream/downstream dependencies and ETL patterns
# MAGIC - Utilize automated tools like Lakebridge for code complexity analysis
# MAGIC - Identify candidates for archival vs. active migration

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Migration Discovery Strategy
# MAGIC
# MAGIC A successful discovery starts with clear objectives. We must identify what provides the most value to the business and what is technically feasible to move first.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Define Scope & Priorities
# MAGIC - **Identify Business Drivers**: Are we migrating for performance, cost reduction, or modern features (Genie AI/BI, Delta Sharing)?
# MAGIC - **Criticality Ranking**: Rank systems and schemas by their importance to the business and their migration complexity.
# MAGIC - **Archival Workloads**: Explicitly identify low-value logic or archival datasets that can be excluded or handled separately to focus on high-impact targets.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Discovery Categories
# MAGIC
# MAGIC A complete discovery spans five categories. Missing any category leads to surprises during migration.
# MAGIC
# MAGIC <br />
# MAGIC <div class="mermaid">
# MAGIC flowchart LR
# MAGIC     subgraph DISCOVERY["Migration Discovery"]
# MAGIC         direction TB
# MAGIC         A["Data<br/>Assets"] 
# MAGIC         B["Pipelines<br/>& ETL"]
# MAGIC         C["Consumers<br/>& Users"]
# MAGIC         D["Security<br/>& Access"]
# MAGIC         E["Operations<br/>& SLAs"]
# MAGIC     end
# MAGIC     style DISCOVERY fill:#fff,stroke:#FF3621,stroke-width:2px
# MAGIC </div>
# MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC | Category | What to Discover | Why It Matters |
# MAGIC |----------|------------------|----------------|
# MAGIC | **Data Assets** | Tables, views, schemas, sizes, formats | Scope the data migration effort |
# MAGIC | **Pipelines & ETL** | Procedures and modules | Plan code conversion and testing |
# MAGIC | **Consumers & Users** | BI tools, apps, user types, connections | Coordinate downstream cutover |
# MAGIC | **Security & Access** | Roles, policies, compliance requirements | Replicate access controls |
# MAGIC | **Operations & SLAs** | Schedules, SLAs, monitoring | Maintain service levels |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Environment Profiling
# MAGIC
# MAGIC Beyond simple object counts, we must understand the environment's interconnectedness.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Inventory Dependencies
# MAGIC - **Upstream/Downstream Systems**: Catalog all source systems feeding into Oracle and all downstream consumers (BI, APIs, external feeds).
# MAGIC - **ETL Patterns**: Document the mix of tool-based ETL (Informatica, Talend) vs. database-native PL/SQL logic.
# MAGIC - **Orchestration & Schedules**: Identify all tools used for job scheduling (Oracle Scheduler, Control-M, Airflow) and their current frequency.
# MAGIC - **Licensing & Windows**: Identify licensing renewal dates or specific maintenance windows that influence the migration sequence.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Automated Discovery with Lakebridge
# MAGIC
# MAGIC **Lakebridge** is a Databricks Labs project that accelerates migration by automating SQL/DDL discover, transpilation and data reconciliation. It supports multiple source platforms, including Oracle.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Supported Source Platforms
# MAGIC
# MAGIC Lakebridge supports transpilation from multiple source platforms:
# MAGIC
# MAGIC | Platform | Dialect Flag | Notes |
# MAGIC |----------|--------------|-------|
# MAGIC | Snowflake | `snowflake` | Full DDL and SQL support |
# MAGIC | SQL Server | `mssql` | T-SQL conversion |
# MAGIC | Synapse | `synapse` | Azure Synapse Analytics |
# MAGIC | Oracle | `oracle` | PL/SQL conversion |
# MAGIC | Teradata | `teradata` | BTEQ and SQL |
# MAGIC | Netezza | `netezza` | IBM Netezza |
# MAGIC | DataStage | `datastage` | IBM DataStage ETL |
# MAGIC | Informatica | `informatica` | Desktop edition |
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC <div class="mermaid">
# MAGIC flowchart LR
# MAGIC     subgraph INPUT["Input Sources"]
# MAGIC         SRC["DDL Scripts / SQL Queries / ETL Code<br/><i>.sql files</i>"]
# MAGIC     end
# MAGIC     subgraph LB["Lakebridge"]
# MAGIC         ANALYZE["analyze<br/><i>Assessment</i>"]
# MAGIC         TRANSPILE["transpile<br/><i>Conversion</i>"]
# MAGIC     end
# MAGIC     subgraph OUTPUT["Output"]
# MAGIC         REPORT["Compatibility<br/>Report (.xlsx)"]
# MAGIC         DBSQL["Databricks<br/>SQL"]
# MAGIC     end
# MAGIC     SRC --> ANALYZE
# MAGIC     SRC --> TRANSPILE
# MAGIC     ANALYZE --> REPORT
# MAGIC     TRANSPILE --> DBSQL
# MAGIC     style INPUT fill:#e3f2fd,stroke:#1976d2
# MAGIC     style LB fill:#fff3e0,stroke:#ff9800
# MAGIC     style OUTPUT fill:#e8f5e9,stroke:#4caf50
# MAGIC </div>
# MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "neutral" }); </script>
# MAGIC
# MAGIC While manual queries provide detailed control, **Lakebridge Analyzer** offers automated code analysis that accelerates the discovery phase significantly.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 1: Install Lakebridge
# MAGIC
# MAGIC Lakebridge can be installed using the Databricks CLI.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 2: Export Oracle Metadata
# MAGIC
# MAGIC Before running the Analyzer, you need to export your Oracle object DDLs (Tables, Views, Procedures, Functions). Lakebridge analyzes these to detect dependencies and Oracle-specific syntax patterns.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 3: Run Lakebridge Analyzer
# MAGIC
# MAGIC Lakebridge scans the DDL files and classifies code complexity using "T-shirt sizing" (Small, Medium, Large, Extra-Large) to guide resource allocation and timeline planning.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Analyzer Output
# MAGIC
# MAGIC Lakebridge generates an Excel report with critical worksheets for planning:
# MAGIC
# MAGIC | Worksheet | Description |
# MAGIC |-----------|-------------|
# MAGIC | **Summary** | High-level complexity overview |
# MAGIC | **SQL Programs** | Complexity scores (LOW/MEDIUM/HIGH) for every script |
# MAGIC | **SQL Special Patterns** | Oracle-specific patterns (like DECODE, SYSDATE) needing conversion |
# MAGIC | **Referenced Objects** | Maps every table/view to the scripts that READ or WRITE to them |
# MAGIC | **SQL Data Types** | Inventory of all data types used (NUMBER, VARCHAR2, CLOB, etc.) |

# COMMAND ----------

# MAGIC %md
# MAGIC ### What Lakebridge Discovers
# MAGIC
# MAGIC - **Complexity Scoring**: Rated LOW/MEDIUM/HIGH based on loops, logic nesting, and proprietary functions.
# MAGIC - **Function Usage**: Detects Oracle-specific built-ins that require Spark SQL equivalents.
# MAGIC - **Object Dependencies**: Builds a lineage map of which scripts reference which objects.
# MAGIC
# MAGIC Use these outputs to size your developer enablement efforts and establish a realistic migration timeline.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Data Assets Discovery
# MAGIC
# MAGIC We must build an inventory of schemas, tables, and views from system catalog views like `ALL_TABLES`, `ALL_OBJECTS`, and `ALL_TAB_COLUMNS`.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Table Detail Inventory
# MAGIC - **Row Counts & Sizes**: Use Oracle statistics to estimate the total data volume.
# MAGIC - **Statistics Freshness**: Check `LAST_ANALYZED` to see if the metadata is current.
# MAGIC - **Active vs. Legacy**: Identify tables that haven't been modified or analyzed in years as candidates for archival.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Pipelines & ETL Discovery
# MAGIC
# MAGIC Identify automation objects that require equivalent implementations in Databricks (Lakeflow Jobs or Spark SQL scripts).

# COMMAND ----------

# MAGIC %md
# MAGIC ### Scheduler Jobs
# MAGIC - **Oracle Scheduler (`DBMS_SCHEDULER`)**: Map these to Databricks Lakeflow Jobs.
# MAGIC - **Frequency Analysis**: Identify high-frequency jobs (hourly) vs. batch (daily/monthly).
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Triggers and Stored Procedures
# MAGIC - **Triggers**: Often used for CDC or data validation. These usually move to Lakeflow Spark Declarative Pipelines or Spark streaming logic.
# MAGIC - **Stored Procedures**: PL/SQL logic must be rewritten as Python or Databricks SQL scripts.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Consumers & Access Patterns
# MAGIC
# MAGIC Analyzing workload patterns helps guide compute sizing (SQL Warehouses) and concurrency settings.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Workload Analysis
# MAGIC - **User Concurrency**: How many active sessions are running during peak periods?
# MAGIC - **Query Frequency**: Which schemas or users generate the most `V$SQL` activity?
# MAGIC - **Resource Usage**: Identify high-CPU or high-I/O queries that might indicate complex logic or large table scans.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Security & Access Discovery
# MAGIC
# MAGIC Map Oracle's security model to Unity Catalog's unified governance model.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Role Hierarchy
# MAGIC - **Role Grants**: Document nested roles from `DBA_ROLE_PRIVS`.
# MAGIC - **Object Privileges**: Catalog table-level grants from `DBA_TAB_PRIVS`.
# MAGIC - **Sensitive Data**: Identify any Virtual Private Database (VPD) policies or Dynamic Data Masking that must be recreated using Unity Catalog Row Filters or Column Masks.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Databricks Equivalents Reference
# MAGIC
# MAGIC Use this mapping when planning conversions:
# MAGIC
# MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle Object</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks Equivalent</span> | Notes |
# MAGIC |------------------|----------------------|-------|
# MAGIC | Database | Catalog | Unity Catalog provides 3-level namespace |
# MAGIC | Schema | Schema | Direct mapping |
# MAGIC | Table | Table | Delta is the default table format |
# MAGIC | View | View | Minor SQL syntax differences apply |
# MAGIC | Scheduler Job | Lakeflow Jobs | Use Lakeflow Jobs for orchestration |
# MAGIC | Trigger / CDC Logic | Delta Change Data Feed | Change tracking and CDC in Lakeflow Spark Declarative Pipelines |
# MAGIC | Modules | Job / notebook / script | No drop in replacement, has to be re-implemented |
# MAGIC | Stored Procedure | Notebook / SQL Script | Often rewritten as Python or SQL |
# MAGIC | UDF (PL/SQL) | SQL / Python UDF | Requires rewrite (depending on complexity) |
# MAGIC | Role | Group + Grants | Unity Catalog RBAC |
# MAGIC | Row-Level Security (VPD) | Row Filter | Unity Catalog row filters |
# MAGIC | Data Redaction | Column Mask | Unity Catalog column masks |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary Checklist
# MAGIC
# MAGIC Before proceeding to Planning & Road-mapping, confirm you have documented:
# MAGIC
# MAGIC ✅ Business drivers and criticality ranking for all systems  
# MAGIC ✅ Complete schema/table inventory with sizes  
# MAGIC ✅ Upstream/downstream dependencies and licensing windows  
# MAGIC ✅ Complexity classification (T-shirt sizing) using Lakebridge  
# MAGIC ✅ All Scheduler Jobs, Triggers, Stored Procedures, and UDFs  
# MAGIC ✅ Database workload patterns (concurrency, SQL execution stats)  
# MAGIC ✅ Role hierarchy and row/column security policies  

# COMMAND ----------

# MAGIC %md
# MAGIC ## References
# MAGIC
# MAGIC - [Lakebridge Documentation](https://databrickslabs.github.io/lakebridge/docs/overview/)
# MAGIC - [Oracle Catalog (Data Dictionary) Views](https://docs.oracle.com/cd/E11882_01/nav/catalog_views.htm)
# MAGIC - [Unity Catalog Best Practices](https://docs.databricks.com/en/data-governance/unity-catalog/best-practices.html)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
