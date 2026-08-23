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
# MAGIC # Foundations Phase
# MAGIC
# MAGIC The Foundations phase introduces the business and technical drivers for migrating from Oracle to Databricks. This module provides a structured framework for the migration journey, conceptual mappings between the two platforms, and strategies for data interoperability during the transition.
# MAGIC
# MAGIC Understanding the "why" and the high-level architecture ensures that the migration is aligned with business objectives, such as TCO optimization and AI readiness, while the Migration Maturity Model provides a roadmap for execution.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this module, you will be able to:
# MAGIC - Articulate the business and technical value of migrating to the Databricks Lakehouse architecture
# MAGIC - Describe the six stages of the Migration Maturity Model and their key outcomes
# MAGIC - Map core Oracle architectural components to their Databricks equivalents
# MAGIC - Explain how Lakehouse Federation enables coexistence and gradual migration
# MAGIC - Set up a federated connection to an Oracle database from Unity Catalog

# COMMAND ----------

# MAGIC %md
# MAGIC | Skill | Task | Activity |
# MAGIC |-------|------|----------|
# MAGIC | Why Migrate to Databricks<br/>[0.1 Lecture - Why Migrate to Databricks]($./0.1 Lecture - Why Migrate to Databricks) | Understand drivers | ✅ Analyze TCO optimization, platform consolidation, and open format benefits.<br>✅ Identify opportunities for new capabilities in AI/ML and real-time streaming. |
# MAGIC | Migration Maturity Model<br/>[0.2 Lecture - Migration Maturity Model]($./0.2 Lecture - Migration Maturity Model) | Define phased approach | ✅ Understand the six stages of migration (Discover -> Closeout).<br>✅ Identify key outcomes, milestones, and common anti-patterns for each phase. |
# MAGIC | Architecture & Feature Mapping<br/>[0.3 Lecture - Architecture and Feature Mapping]($./0.3 Lecture - Architecture and Feature Mapping) | Conceptual mapping | ✅ Map core components like RAC/Exadata to SQL Warehouses and Data Files to Delta Lake.<br>✅ Understand namespace differences and classify migration complexity categories. |
# MAGIC | Lakehouse Federation<br/>[0.4 Lecture - Lakehouse Federation]($./0.4 Lecture - Lakehouse Federation) | Enable interoperability | ✅ Define the role of federation in coexistence and validation.<br>✅ Differentiate between Query and Catalog federation for Oracle access. |
# MAGIC | Demo<br/>[0.5 Demo - Lakehouse Federation with Oracle]($./0.5 Demo - Lakehouse Federation with Oracle) | Instructor-led demonstration | ✅ Set up Oracle service user and connection credentials.<br>✅ Create and explore a foreign catalog for federated access to Oracle tables. |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
