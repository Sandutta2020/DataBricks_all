# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
# MAGIC     <div style="font-size: 14px; color: #666;">
# MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
# MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
# MAGIC         <span style="margin-left: 8px;">PREREQUISITES</span>
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

# MAGIC %md-sandbox
# MAGIC # Prerequisites
# MAGIC
# MAGIC This course is designed for SI/Partners of Databricks who will assist customers with migrations from **Oracle** to **Databricks**. Before participating in this course or delivering migration engagements, partners should meet the following prerequisites.
# MAGIC
# MAGIC <div style="display: flex; align-items: center; justify-content: center; gap: 40px; padding: 40px;">
# MAGIC     <div style="text-align: center;">
# MAGIC         <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="120" height="120" />
# MAGIC     </div>
# MAGIC     <div style="font-size: 72px; color: #999; display: flex; align-items: center; line-height: 1; margin-bottom: 20px;">-></div>
# MAGIC     <div style="text-align: center;">
# MAGIC         <img src="https://cdn.simpleicons.org/databricks/FF3621" width="120" height="120"/>
# MAGIC     </div>
# MAGIC </div>
# MAGIC
# MAGIC <hr/>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Certifications and Experience
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Databricks Certifications (Required)
# MAGIC
# MAGIC Partners should hold the following Databricks certifications:
# MAGIC
# MAGIC | Certification | Description |
# MAGIC |---------------|-------------|
# MAGIC | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> <b>Databricks Certified Data Engineer Professional</b></span> | Demonstrates advanced data engineering skills on the Databricks platform |

# COMMAND ----------

# MAGIC %md
# MAGIC ### Oracle Certifications (Recommended)
# MAGIC
# MAGIC Partners should hold at least one of the following Oracle certifications or have demonstrable experience with Oracle, and should be able to articulate the differences between Oracle and Databricks:
# MAGIC
# MAGIC | Certification | Description |
# MAGIC |---------------|-------------|
# MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> <b>Oracle AI Database SQL Certified Associate</b></span> | Validates foundational Oracle SQL knowledge and database concepts |
# MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> <b>Oracle Database PL/SQL Developer Certified Professional</b></span> | Demonstrates mastery of advanced PL/SQL, performance optimization, and application architecture |
# MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> <b>Oracle GoldenGate Implementation Certified Professional</b></span> | Validates real-time data integration and replication skills using GoldenGate — directly relevant to CDC migration patterns |
# MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> <b>Oracle Data Integrator (ODI) Certified Implementation Specialist</b></span> | Demonstrates expertise in Oracle ETL/ELT pipelines — the tooling most commonly replaced by Lakeflow during migration |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Environment Requirements
# MAGIC
# MAGIC To run the demonstrations and hands-on exercises in this course, partners must have access to the following:
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="25" height="25" style="vertical-align: middle;"> </span>Databricks Environment
# MAGIC
# MAGIC | Requirement | Details |
# MAGIC |-------------|----------|
# MAGIC | **Databricks Account** | Active Databricks account with at least one workspace |
# MAGIC | **Account Admin** | Account-level administrator privileges |
# MAGIC | **Metastore Admin** | Unity Catalog metastore administrator access |
# MAGIC | **Workspace Admin** | Workspace administrator privileges on the workspace(s) used for demos |

# COMMAND ----------

# MAGIC %md
# MAGIC ### <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="25" height="25" style="vertical-align: middle;" /></span> Oracle Environment
# MAGIC
# MAGIC | Requirement | Details |
# MAGIC |-------------|----------|
# MAGIC | **Oracle access** | Active Oracle access (any form: on-prem, cloud-hosted, OCI) |
# MAGIC | **SELECT on HR schema** | Access to the `HR` sample schema used in course demos |
# MAGIC | **DBA role** | Required for full migration access — grants `SELECT ANY TABLE`, `SELECT ANY DICTIONARY` (all `DBA_*` views and procedure source via `DBA_SOURCE`), and `MANAGE SCHEDULER` (stop/alter jobs) |
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Demo Data Setup
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### HR Sample Dataset
# MAGIC
# MAGIC The **HR** sample Oracle dataset will be used throughout the course for migration demonstrations.
# MAGIC
# MAGIC <div style="border-left: 4px solid #2196F3; background: #e7f3fe; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <strong style="font-size: 1.1em;">💡 Setup Instructions</strong>
# MAGIC     <ol style="margin: 8px 0 0 0; color: #333;">
# MAGIC         <li>Navigate to <a href="https://github.com/oracle-samples/db-sample-schemas" target="_blank">Oracle's samples repository</a></li>
# MAGIC         <li>Select the <code>human_resources</code> sample</li>
# MAGIC         <li>Ensure you have privileges to create another user</li>
# MAGIC         <li>Install the HR dataset following the <a href="https://github.com/oracle-samples/db-sample-schemas/blob/main/human_resources/README.md" target="_blank">description in the README</a></li>
# MAGIC         <li>Verify the <code>HR</code> schema and associated objects are created</li>
# MAGIC     </ol>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tools and Software
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Lakebridge (Recommended)
# MAGIC
# MAGIC Partners should have **Lakebridge** installed and configured for automated code conversion and migration acceleration.
# MAGIC
# MAGIC | Setup Step | Details |
# MAGIC |------------|----------|
# MAGIC | **Obtain License** | Contact your Databricks account team for Lakebridge licensing |
# MAGIC | **Install** | Follow the Lakebridge installation guide |
# MAGIC | **Configure Oracle** | Set up connectivity to source Oracle account |
# MAGIC | **Configure Databricks** | Set up connectivity to target Databricks workspace |
# MAGIC | **Verify** | Test successful connection to both platforms |
# MAGIC
# MAGIC **Lakebridge Capabilities Used in This Course:**
# MAGIC
# MAGIC - Automated SQL dialect conversion (Oracle SQL to Databricks SQL)
# MAGIC - Schema discovery and metadata extraction
# MAGIC - DDL generation for Unity Catalog
# MAGIC - Code analysis and compatibility assessment

# COMMAND ----------

# MAGIC %md
# MAGIC ### Oracle Tools
# MAGIC
# MAGIC Oracle SQL Developer and the SQLcl command line interface are recommended for running queries, discovering the database and exporting data.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Knowledge Prerequisites
# MAGIC
# MAGIC Partners should have working knowledge of the following concepts.
# MAGIC
# MAGIC | Platform | Area | Topics |
# MAGIC |--------|------|--------|
# MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> <b>Oracle</b></span> | Architecture | Virtual warehouses, storage layer, cloud services layer |
# MAGIC |  | Database Objects | Tables, views, streams, tasks, stages, pipes, stored procedures |
# MAGIC |  | Data Loading | COPY INTO, Snowpipe, external stages |
# MAGIC |  | Access Control | Roles, privileges, RBAC, Row Access Policies, Dynamic Data Masking |
# MAGIC |  | SQL | Oracle SQL syntax, VARIANT data type, FLATTEN, JavaScript UDFs |
# MAGIC | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> <b>Databricks</b></span> | Architecture | Workspace architecture, clusters, SQL warehouses |
# MAGIC |  | Unity Catalog | Catalogs, schemas, tables, volumes, governance model |
# MAGIC |  | Delta Lake | ACID transactions, time travel, OPTIMIZE, VACUUM |
# MAGIC |  | SQL | Databricks SQL, SQL warehouses, Photon engine |
# MAGIC |  | Orchestration | Lakeflow Jobs, Lakeflow Declarative Pipelines (SDP) |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Readiness Checklist
# MAGIC
# MAGIC Use this checklist to verify readiness before the course.
# MAGIC
# MAGIC ✅ <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="18" height="18" style="vertical-align: middle;"></span> Databricks target environment acess with required privileges (Account Admin, Metastore Admin, Workspace Admin)  
# MAGIC ✅ <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="18" height="18" style="vertical-align: middle;" /></span> Oracle source system environment access with required privileges  
# MAGIC ✅ Lakebridge installed and configured (optional)  

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
