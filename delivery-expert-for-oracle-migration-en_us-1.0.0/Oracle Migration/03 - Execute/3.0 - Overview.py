# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
# MAGIC     <div style="font-size: 14px; color: #666;">
# MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
# MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
# MAGIC         <span style="margin-left: 8px;">03 - Execute</span>
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
# MAGIC # Execution & Data Migration Phase

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overview
# MAGIC
# MAGIC The Execution & Data Migration phase is where the migration plan becomes reality. This module covers the hands-on work of moving data from Oracle to Databricks, converting schemas and code, rebuilding pipelines, and establishing incremental sync patterns.
# MAGIC
# MAGIC Successful execution requires methodical attention to data integrity, schema fidelity, and pipeline reliability. By implementing proper Bronze/Silver/Gold ingestion patterns, CDC workflows, and orchestration frameworks, you ensure that migrated workloads perform correctly and efficiently in the new Lakehouse environment while maintaining data quality throughout the transition.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this module, you will be able to:
# MAGIC - Translate Oracle DDL to Unity Catalog Delta DDL including views and materialized views
# MAGIC - Export Oracle tables and ingest data to Delta using Auto Loader with proper schema mapping
# MAGIC - Implement CDC patterns using Delta `MERGE` and `AUTO CDC` for SCD Type 1/2 handling
# MAGIC - Convert Oracle PL/SQL functions, procedures and modules into Databricks equivalents
# MAGIC - Recreate Oracle triggers and orchestrated workflows as Lakeflow Jobs or Lakeflow Declarative Pipelines with CI/CD integration

# COMMAND ----------

# MAGIC %md
# MAGIC | Skill | Task | Activity |
# MAGIC |-------|------|----------|
# MAGIC | Schema & DDL Conversion <br/>[3.1 Lecture - Schema and DDL Conversion]($./3.1 Lecture - Schema and DDL Conversion)| Convert metadata to UC | ✅ Translate Oracle DDL to Unity Catalog Delta DDL; recreate views/materialized views.<br>✅ Adapt datatypes, constraints, and policies to Databricks SQL semantics. |
# MAGIC | Data Migration & Ingestion <br/> [3.2 Lecture - Data Migration and Ingestion]($./3.2 Lecture - Data Migration and Ingestion) | Land Bronze data | ✅ Export Oracle tables to Parquet/CSV and ingest to Delta (Bronze -> Silver) via Auto Loader.<br>✅ Map schemas and types (e.g., `NUMBER` -> `DECIMAL`); define partitioning/clustering.<br>✅ Implement one-time data migration using Oracle connector or `COPY INTO` workflow. |
# MAGIC | Incremental Sync & CDC <br/> [3.3 Lecture - Incremental Sync and CDC]($./3.3 Lecture - Incremental Sync and CDC) | Enable change data flows | ✅ Implement Delta `MERGE` / `AUTO CDC` with SCD Type 1/2; handle deletes via `APPLY AS DELETE WHEN`.<br>✅ Monitor CDC events and logs; validate sequencing and latency per SLA. |
# MAGIC | SQL & Code Conversion <br/> [3.4 Lecture - SQL and Code Conversion]($./3.4 Lecture - SQL and Code Conversion) | Port logic to Databricks | ✅ Translate Oracle PL/SQL and UDFs to Databricks SQL and UDFs; refactor for semi-structured logic.<br>✅ Validate query correctness and performance on representative datasets. |
# MAGIC | Pipeline & Orchestration <br/> [3.5 Lecture - Pipeline and Orchestration]($./3.5 Lecture - Pipeline and Orchestration) | Rebuild jobs and scheduling | ✅ Recreate Oracle Scheduler Jobs and CDC workflows as Lakeflow Jobs or Lakeflow Pipelines; define dependencies and retries.<br>✅ Implement CI/CD with Repos and environment promotion. |
# MAGIC | Demo<br/>[3.6 Demo - Execution & Data Migration Phase]($./3.6 Demo - Execution & Data Migration Phase) | Instructor-led demonstration | Hands-on demonstration of key concepts covered in this module. |
# MAGIC | Lab<br/>[3.7 Lab - Execution & Data Migration Phase]($./3.7 Lab - Execution & Data Migration Phase) | Practice exercises | Interactive exercises to reinforce learning objectives from this module. |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
