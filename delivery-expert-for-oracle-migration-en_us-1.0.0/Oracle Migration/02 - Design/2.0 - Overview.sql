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

-- MAGIC %md
-- MAGIC
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img
-- MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
-- MAGIC     alt="Databricks Learning"
-- MAGIC   >
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Architecture & Design Phase

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Overview
-- MAGIC
-- MAGIC The Architecture & Design phase translates discovery insights into a concrete technical blueprint for the Databricks Lakehouse. This module guides you through defining target architecture, setting up the platform foundation, designing storage and governance models, and implementing security controls.
-- MAGIC
-- MAGIC Thoughtful architecture decisions made during this phase directly impact migration success, operational efficiency, and long-term maintainability. By mapping Oracle constructs to their Databricks equivalents (such as PL/SQL to Python or SQL code and Flashback to Delta Time Travel), establishing Unity Catalog governance, and designing the Bronze/Silver/Gold layers, you create a scalable foundation that unlocks the full potential of the Data Intelligence Platform.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this module, you will be able to:
-- MAGIC - Design target Lakehouse architecture mapping Oracle constructs (PL/SQL, DBMS_SCHEDULER, Flashback, Materialized Views) to Databricks features
-- MAGIC - Configure Unity Catalog with metastores, catalogs, schemas, and managed storage locations
-- MAGIC - Set up workspaces, clusters, and serverless SQL Warehouses with proper bindings
-- MAGIC - Establish naming conventions, privilege models, and governance hierarchies
-- MAGIC - Implement RBAC/ABAC security patterns for tables, volumes, and audit compliance

-- COMMAND ----------

-- MAGIC %md
-- MAGIC | Skill | Task | Activity |
-- MAGIC |-------|------|----------|
-- MAGIC | Solution Architecture & Modeling<br/>[2.1 Lecture - Solution Architecture and Modeling]($./2.1 Lecture - Solution Architecture and Modeling) | Define target architecture | ✅ Define Databricks Data Intelligence Platform target (Lakehouse architecture: UC + Lakeflow + SQL Warehouses).<br>✅ Map Oracle constructs (PL/SQL, DBMS_SCHEDULER, Flashback) to Databricks features.<br>✅ Validate performance, scalability, and cost expectations; baseline metrics.<br>✅ Design Bronze/Silver/Gold layers, data flow, and CDC strategy. |
-- MAGIC | Platform Setup & Environment<br/>[2.2 Lecture - Platform Setup and Environment]($./2.2 Lecture - Platform Setup and Environment) | Stand up foundation | ✅ Enable Unity Catalog; create metastore, catalogs, schemas; assign managed storage locations.<br>✅ Configure workspaces, clusters, serverless SQL Warehouses; bind workspace to UC.<br>✅ Create service credentials (IAM/service accounts) for staging/landing zones.<br>✅ Establish naming and privilege model (USAGE, SELECT/MODIFY) across UC objects. |
-- MAGIC | Storage & Governance Design<br/>[2.3 Lecture - Storage and Governance Design]($./2.3 Lecture - Storage and Governance Design) | Define storage and policy model | ✅ Set up staging zones and object store bindings; grant least-privilege access.<br>✅ Establish ownership conventions and governance hierarchy. |
-- MAGIC | Security & Access Design<br/>[2.4 Lecture - Security and Access Design]($./2.4 Lecture - Security and Access Design) | Implement role model | ✅ Apply RBAC/ABAC principles for tables and volumes; design audit and compliance framework. |
-- MAGIC | Demo<br/>[2.5 Demo - Architecture & Design Phase]($./2.5 Demo - Architecture & Design Phase) | Instructor-led demonstration | Hands-on demonstration of key concepts covered in this module. |
-- MAGIC | Lab<br/>[2.6 Lab - Architecture & Design Phase]($./2.6 Lab - Architecture & Design Phase) | Practice exercises | Interactive exercises to reinforce learning objectives from this module. |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
