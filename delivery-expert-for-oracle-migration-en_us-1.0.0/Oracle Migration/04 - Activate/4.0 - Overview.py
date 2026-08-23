# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
# MAGIC     <div style="font-size: 14px; color: #666;">
# MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
# MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
# MAGIC         <span style="margin-left: 8px;">04 - Activate</span>
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
# MAGIC # Activation Phase

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overview
# MAGIC
# MAGIC The Activation phase brings migrated workloads into production through rigorous **Validation & Cutover** activities. This module covers testing frameworks, data quality verification, observability setup, and the critical transition from Oracle to Databricks as the production system.
# MAGIC
# MAGIC Thorough validation prevents post-migration issues that can erode stakeholder confidence and disrupt business operations. By implementing comprehensive data parity checks, building operational dashboards, and executing a well-planned cutover sequence, you ensure a smooth transition with minimal risk and clear rollback options if needed.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this module, you will be able to:
# MAGIC - Perform data parity validation including record counts, aggregations, nulls, and string matching
# MAGIC - Implement testing frameworks (Spark Testing Base, Chispa, Great Expectations) for automated verification
# MAGIC - Enable Lakeflow Pipeline event logs and system tables for usage, lineage, and access monitoring
# MAGIC - Build operational dashboards tracking validation coverage, throughput, and performance metrics
# MAGIC - Execute cutover plans including freeze windows, delta catch-up, consumer switchover, and business sign-off

# COMMAND ----------

# MAGIC %md
# MAGIC | Skill | Task | Activity |
# MAGIC |-------|------|----------|
# MAGIC | Testing & Data Validation <br/>[4.1 Lecture - Testing and Data Validation]($./4.1 Lecture - Testing and Data Validation)| Verify accuracy and quality | ✅ Perform data parity checks (record counts, sums, nulls, string matches).<br>✅ Use testing frameworks (Spark Testing Base, Chispa, ScalaTest, Great Expectations).<br>✅ Define quantitative governance rules (counts, stddevs, timestamp bounds) in Delta metadata. |
# MAGIC | Observability & Monitoring <br/>[4.2 Lecture - Observability & Monitoring]($./4.2 Lecture - Observability & Monitoring)| Enable runtime visibility | ✅ Enable Lakeflow Spark Declarative Pipeline event logs and system tables for usage/lineage/access monitoring.<br>✅ Build operational dashboards for validation coverage and throughput.<br>✅ Tune partitioning, clustering, and caching before cutover. |
# MAGIC | Cutover Execution <br/>[4.3 Lecture - Cutover Execution]($./4.3 Lecture - Cutover Execution)| Transition to production | ✅ Plan freeze/rollback window; run delta catch-up; switch consumers to Databricks.<br>✅ Validate dashboards and reports post-cutover; obtain business sign-off. |
# MAGIC | Demo<br/>[4.4 Demo - Activation Phase]($./4.4 Demo - Activation Phase) | Instructor-led demonstration | Hands-on demonstration of key concepts covered in this module. |
# MAGIC | Lab<br/>[4.5 Lab - Activation Phase]($./4.5 Lab - Activation Phase) | Practice exercises | Interactive exercises to reinforce learning objectives from this module. |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
