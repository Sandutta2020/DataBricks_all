# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
# MAGIC     <div style="font-size: 14px; color: #666;">
# MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
# MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
# MAGIC         <span style="margin-left: 8px;">00 - Foundations</span>
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
# MAGIC # Architecture and Feature Mapping
# MAGIC
# MAGIC This module provides a **high-level overview** of how **Oracle** and **Databricks** architectures compare. Understanding these conceptual mappings helps frame the migration journey - detailed implementation guidance is covered in the **Design** phase (Module 02).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lesson, you will be able to:
# MAGIC - Understand the conceptual mapping between Oracle and Databricks
# MAGIC - Recognize key architectural differences at a high level
# MAGIC - Identify what translates easily vs what requires redesign
# MAGIC - Prepare for detailed planning in the Design phase

# COMMAND ----------

# MAGIC %md
# MAGIC ## Core Component Mapping
# MAGIC
# MAGIC At a high level, Oracle and Databricks share similar functional areas, however, there are large differences in the foundations of the systems. This table provides a conceptual overview - detailed mappings are covered in the __Design Phase__.
# MAGIC
# MAGIC | Functional Area | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
# MAGIC |-----------------|-------------------|------------|
# MAGIC | **Compute** | Instances, RAC, Exadata | SQL Warehouses, Clusters |
# MAGIC | **Storage** | Data Files (.dbf), ASM, Tablespaces | Cloud object storage + Delta Lake |
# MAGIC | **Catalog** | Data Dictionary (DBA_*, ALL_*) | Unity Catalog |
# MAGIC | **Ingestion** | SQL*Loader, Data Pump, GoldenGate | Auto Loader, COPY INTO, Lakeflow Connect |
# MAGIC | **Orchestration** | Oracle Scheduler (DBMS_SCHEDULER) | Lakeflow Jobs |
# MAGIC | **Transformations** | PL/SQL (Stored Procedures, Packages) | Lakeflow Spark Declarative Pipelines, Notebooks |
# MAGIC | **Security** | RBAC, VPD, Database Vault | Unity Catalog RBAC/ABAC |
# MAGIC | **Data Sharing** | Database Links, Data Pump | Delta Sharing (open protocol) |
# MAGIC | **BI** | Oracle Analytics Cloud (OAC), OBIEE | Databricks SQL, AI/BI Dashboards |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 12px 16px; border-radius: 4px; margin: 16px 0;">
# MAGIC <strong>📘 Detailed Mappings</strong><br/>
# MAGIC For comprehensive object-level mappings, SQL syntax differences, data type conversions, and governance configurations, see <strong>2.1 - Solution Architecture and Modeling</strong>.
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Account and Namespace Structure
# MAGIC
# MAGIC The fundamental organizational structures differ between platforms. Understanding this helps plan your migration topology.
# MAGIC
# MAGIC <br />
# MAGIC <div class="mermaid">
# MAGIC flowchart TB
# MAGIC     subgraph OR["Oracle"]
# MAGIC         direction TB
# MAGIC         ORO["<b>Organization</b><br/><i>admin umbrella</i>"]
# MAGIC         ORC["<b>Container Database</b>"]
# MAGIC         ORP["<b>Pluggable Database</b>"]
# MAGIC         ORS["<b>Schema</b>"]
# MAGIC         OROBJ["<b>Objects</b><br/><i>tables, views, etc.</i>"]
# MAGIC         ORO --> ORC --> ORP --> ORS --> OROBJ
# MAGIC     end
# MAGIC     subgraph DB["Databricks"]
# MAGIC         direction TB
# MAGIC         DBA["<b>Account</b><br/><i>admin + billing</i>"]
# MAGIC         DBM["<b>Metastore</b><br/><i>governance</i>"]
# MAGIC         DBW["<b>Workspace</b><br/><i>compute</i>"]
# MAGIC         DBC["<b>Catalog</b>"]
# MAGIC         DBS["<b>Schema</b>"]
# MAGIC         DBOBJ["<b>Objects</b><br/><i>tables, views, etc.</i>"]
# MAGIC         DBA --> DBM
# MAGIC         DBA --> DBW
# MAGIC         DBW -.->|attaches to| DBM
# MAGIC         DBM --> DBC --> DBS --> DBOBJ
# MAGIC     end
# MAGIC     style OR fill:#fff,stroke:#29B5E8,stroke-width:2px
# MAGIC     style DB fill:#fff,stroke:#FF3621,stroke-width:2px
# MAGIC </div>
# MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>
# MAGIC
# MAGIC **Key Conceptual Differences:**
# MAGIC - **Metastore**: A Unity Catalog metastore spans workspaces, enabling unified governance across compute environments
# MAGIC - **Namespace**: Oracle uses `schema.object`; Databricks uses `catalog.schema.object`

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">ℹ️</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Oracle Namespace Hierarchy - CDB/PDB Assumption</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">The diagram models Oracle's hierarchy as Organization -> Container Database -> Pluggable Database -> Schema -> Objects, which reflects Oracle 12c+ CDB/PDB architecture. Many Oracle environments being migrated may still run non-CDB (traditional) deployments, where the hierarchy is simply Database -> Schema -> Objects.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Migration Complexity Overview
# MAGIC
# MAGIC Understanding what translates easily versus what requires redesign helps scope your migration effort.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### What Translates Easily ✅
# MAGIC
# MAGIC | Category | Examples |
# MAGIC |----------|----------|
# MAGIC | **Standard SQL** | `SELECT`, `JOIN`, `GROUP BY`, `UNION`, window functions, CTEs |
# MAGIC | **Basic DDL** | `CREATE TABLE`, `CREATE VIEW`, constraints |
# MAGIC | **Analytic expressions** | Analytic functions, aggregate functions like `SUM` etc. |
# MAGIC | **Some Oracle specifics** | Sequences: map to `IDENTITY` columns, `NVL` to `COALESCE` |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### What Requires Adaptation ⚠️
# MAGIC
# MAGIC | Category | Consideration |
# MAGIC |----------|---------------|
# MAGIC | **Data types with no direct equivalents** | `CLOB`, `BLOB`, `XMLTYPE` |
# MAGIC | **Data types with differences** | Number precision questions, Oracle `DATE` stores **date and time** (second precision, no timezone); Spark's nearest equivalent is `TIMESTAMP` (add explicit `CAST` in DDL conversion) |
# MAGIC | **Oracle-specific functions** | map `DECODE` to `CASE`-`WHEN`, `CONNECT BY`, `ROWNUM` (context-dependent), `SYSDATE` (timezone warning!) |
# MAGIC | **Change data capture** | Map to Delta Change Data Feed + Structured Streaming |
# MAGIC | **Access Control** | Users, roles, basic permissions |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### What Requires Redesign 🔄
# MAGIC
# MAGIC | Category | Why |
# MAGIC |----------|-----|
# MAGIC | **Storage** | Completely different storage approach |
# MAGIC | **Stored Procedures** | Map to notebooks or Stored Procedures or SQL Scripting in Databricks |
# MAGIC | **PL/SQL packages** | Major task: packages have to be re-written as a combination of SQL functions, SQL scripts, notebooks, Lakeflow Jobs... |
# MAGIC | **Orchestration** | Use Lakeflow Jobs to orchestrate data processing |
# MAGIC | **DBLinks** | Use case dependent — Delta Sharing for cross-workspace or cross-org data access; Lakehouse Federation / external connections for querying external systems at runtime |
# MAGIC | **Synonyms** | No native synonym concept in Databricks |
# MAGIC | **Fine-grained access control** | Translate Virtual Private Database, Label Security and Redaction to row filters and column masks |
# MAGIC | **Tightly Coupled Apps** | Applications with embedded Oracle logic need refactoring |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
