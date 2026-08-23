# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
# MAGIC     <div style="font-size: 14px; color: #666;">
# MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
# MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
# MAGIC         <span style="margin-left: 8px;">05 - Enable</span>
# MAGIC     </div>
# MAGIC     <div style="display: flex; align-items: center; gap: 8px;">
# MAGIC         <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="24" height="24" />
# MAGIC         <span style="color: #999; font-size: 16px;">-></span>
# MAGIC         <img src="https://cdn.simpleicons.org/databricks/FF3621" width="24" height="24"/>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img
# MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
# MAGIC     alt="Databricks Learning"
# MAGIC   >
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # Enablement & Automation Phase

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overview
# MAGIC
# MAGIC The Enablement & Automation phase operationalizes the migrated platform for long-term success. This module covers DevOps integration, fine-grained security enforcement, and validation of BI and ML consumption layers to ensure the Databricks environment is production-ready and self-sustaining.
# MAGIC
# MAGIC Automation and proper enablement reduce operational overhead while improving reliability and security posture. By integrating CI/CD pipelines, applying Unity Catalog row/column security, and validating that downstream consumers work correctly with SQL Warehouses, you create a platform that teams can confidently operate and extend independently.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this module, you will be able to:
# MAGIC - Enable Databricks SQL Serverless for BI workloads with proper concurrency and cost scaling
# MAGIC - Integrate CI/CD workflows using the Databricks CLI (DABs), GitHub Actions, and Terraform for data and ML pipelines
# MAGIC - Apply row-level and column-level security masks in Unity Catalog using ABAC policies
# MAGIC - Re-point BI tools to SQL Warehouses and validate dashboard functionality and SLA compliance
# MAGIC - Migrate ML pipelines to Lakehouse architecture with features registered in Unity Catalog

# COMMAND ----------

# MAGIC %md
# MAGIC | Skill | Task | Activity |
# MAGIC |-------|------|----------|
# MAGIC | DevOps & Platform Ops <br/>[5.1 Lecture - Platform Operations and Cost Management]($./5.1 Lecture - Platform Operations and Cost Management)| Operationalize workflows | ✅ Enable Databricks SQL Serverless for BI; test concurrency and cost scaling.<br>✅ Integrate CI/CD (Databricks CLI / DABs, GitHub Actions, Terraform) for data and ML pipelines.<br>✅ Apply IaC best practices for workspace and security versioning. |
# MAGIC | Security & Fine-Grained Access <br/>[5.2 Lecture - Security and Fine-Grained Access]($./5.2 Lecture - Security and Fine-Grained Access)| Enforce policies | ✅ Apply row/column masks in Unity Catalog; use ABAC for central policy mgmt.<br>✅ Use dynamic views for read-only joins; document grants and inheritance. |
# MAGIC | BI & ML Integration <br/>[5.3 Lecture - Consumer Integration]($./5.3 Lecture - Consumer Integration) | Validate consumption layers | ✅ Re-point BI tools to SQL Warehouses; validate dashboards and SLA compliance.<br>✅ Migrate ML pipelines to Lakehouse; register features in Unity Catalog. |
# MAGIC | Demo<br/>[5.4 Demo - Enablement & Automation Phase]($./5.4 Demo - Enablement & Automation Phase) | Instructor-led demonstration | Hands-on demonstration of key concepts covered in this module. |
# MAGIC | Lab<br/>[5.5 Lab - Enablement & Automation Phase]($./5.5 Lab - Enablement & Automation Phase) | Practice exercises | Interactive exercises to reinforce learning objectives from this module. |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
