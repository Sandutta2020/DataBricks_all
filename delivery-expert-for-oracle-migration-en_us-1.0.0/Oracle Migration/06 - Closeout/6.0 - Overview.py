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
# MAGIC # Closeout & Handoff Phase
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overview
# MAGIC
# MAGIC The Closeout & Handoff phase completes the migration engagement by transferring ownership to operational teams and decommissioning the legacy Oracle environment. This module covers observability setup, developer enablement, documentation, and the formal retirement of source systems.
# MAGIC
# MAGIC A well-executed closeout ensures the customer can independently maintain, troubleshoot, and extend their new Databricks platform. By delivering comprehensive documentation, establishing monitoring and alerting, and conducting proper knowledge transfer, you set up the organization for long-term success while cleanly retiring legacy infrastructure.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this module, you will be able to:
# MAGIC - Integrate observability with enterprise monitoring tools (Splunk, CloudWatch, Azure Monitor) and configure alerts
# MAGIC - Enable developer productivity with Databricks Connect, VS Code integration, and standardized Repos workflows
# MAGIC - Document migration patterns, architecture decisions, and lessons learned for future reference
# MAGIC - Deliver runbooks, troubleshooting playbooks, and CI/CD guides to operations teams
# MAGIC - Execute Oracle decommissioning including backup, metadata archival, and connector shutdown

# COMMAND ----------

# MAGIC %md
# MAGIC | Skill | Task | Activity |
# MAGIC |-------|------|----------|
# MAGIC | Observability & Cost Monitoring <br/>[6.1 Lecture - Observability and Cost Monitoring]($./6.1 Lecture - Observability and Cost Monitoring)| Implement metrics collection | ✅ Integrate with JMX, Splunk, CloudWatch, Azure Monitor; configure alerts and billing tags. |
# MAGIC | Developer Enablement <br/>[6.2 Lecture - Developer Enablement]($./6.2 Lecture - Developer Enablement)| Equip engineering teams | ✅ Support Databricks Connect and VS Code IDE integration; standardize Repos and branch models. |
# MAGIC | Documentation & Knowledge Transfer <br/>[6.3 Lecture - Documentation and Knowledge Transfer]($./6.3 Lecture - Documentation and Knowledge Transfer)| Finalize project artifacts | ✅ Document migration patterns and code refactor lessons learned.<br>✅ Document architecture, metrics, and recovery procedures with DBU tagging.<br>✅ Record unit/regression tests and validation queries in source control.<br>✅ Deliver troubleshooting playbooks, CI/CD guides, and notification policies.<br>✅ Publish runbooks for operations; transfer ownership to Ops teams. |
# MAGIC | Decommission & Closure <br/>[6.4 Lecture - Decommissioning and Retirement]($./6.4 Lecture - Decommissioning and Retirement)| Retire legacy Oracle | ✅ Backup Oracle tables/stages; archive metadata; shut down connectors.<br>✅ Conduct final stakeholder review and close engagement. |
# MAGIC | Demo<br/>[6.5 Demo - Closeout & Handoff Phase]($./6.5 Demo - Closeout & Handoff Phase) | Instructor-led demonstration | Hands-on demonstration of key concepts covered in this module. |
# MAGIC | Lab<br/>[6.6 Lab - Closeout & Handoff Phase]($./6.6 Lab - Closeout & Handoff Phase) | Practice exercises | Interactive exercises to reinforce learning objectives from this module. |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
