-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">01 - Discover</span>
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
-- MAGIC # Discovery & Planning Phase
-- MAGIC
-- MAGIC The Discovery & Planning phase establishes the foundation for a successful Oracle to Databricks migration. This module guides you through understanding the customer's current environment, aligning stakeholders, selecting the right migration strategy, and building an actionable roadmap.
-- MAGIC
-- MAGIC A thorough discovery prevents costly surprises during execution. By systematically inventorying data assets, profiling workload complexity, and mapping dependencies, you create the insights needed to estimate effort accurately, prioritize workloads effectively, and set realistic expectations with stakeholders.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this module, you will be able to:
-- MAGIC - Establish governance structures and align stakeholders around migration objectives
-- MAGIC - Select the appropriate migration strategy (ETL-First vs BI-First) based on customer drivers
-- MAGIC - Conduct comprehensive discovery across data assets (Oracle objects, PL/SQL), pipelines, consumers, security, and operations
-- MAGIC - Profile the Oracle environment using AWR/ASH reports and score workload complexity using T-shirt sizing
-- MAGIC - Build a phased migration plan with waves, milestones, and resource allocation

-- COMMAND ----------

-- MAGIC %md
-- MAGIC | Skill | Task | Activity |
-- MAGIC |-------|------|----------|
-- MAGIC | Engagement & Governance<br/>[1.1 Lecture - Engagement and Alignment]($./1.1 Lecture - Engagement and Alignment) | Define scope & approach | ✅ Select Prime, Assurance+, or Advisory package based on delivery ownership.<br>✅ Coordinate SKU/pricing with Engagement Manager and attach correct deal SKU.<br>✅ Provide customer datasheet outlining scope, expectations, and engagement model. |
-- MAGIC | Stakeholder Alignment & Readiness<br/>[1.1 Lecture - Engagement and Alignment]($./1.1 Lecture - Engagement and Alignment) | Establish objectives & roles | ✅ Define objectives, deliverables, constraints, and SME scheduling.<br>✅ Interview Oracle SMEs on usage, downstream systems, pain points, workflows, politics.<br>✅ Confirm MVP use case for templating and communicate Lakehouse vision. |
-- MAGIC | Discovery & Landscape Analysis<br/>[1.2 Lecture - Discovery and Landscape Analysis]($./1.2 Lecture - Discovery and Landscape Analysis) | Assess current state | ✅ Inventory databases, tables, PL/SQL packages/procedures, and materialized views; map to Databricks equivalents.<br>✅ Audit PL/SQL complexity to estimate refactoring vs. rewrite effort.<br>✅ Document DB Links and external dependencies between datasets, jobs, and BI tools; prioritize workloads (lift-and-shift vs refactor).<br>✅ Capture persona access patterns, compute usage (via AWR/ASH reports), and timelines.<br>✅ Identify facts/dimensions, SCDs, and temporal/versioned logic.<br>✅ Review external tools and orchestration frameworks for migration risk. |
-- MAGIC | Planning & Road-mapping<br/>[1.3 Lecture - Planning and Road-mapping]($./1.3 Lecture - Planning and Road-mapping) | Build migration plan | ✅ Sequence phases (ingest -> schema -> validation -> cutover) and align to success metrics.<br>✅ Define ingestion strategy (CDC for production tables vs. Batch for history); note out-of-scope sources.<br>✅ Classify datasets (active vs legacy) and tag governance/access controls.<br>✅ Establish lineage and dependencies with catalog tooling.<br>✅ Extract DDL and metadata from Oracle for schema conversion.<br>✅ Inventory automation and scheduling details.<br>✅ Capture user personas, tools, and security models.<br>✅ Map Oracle roles to Unity Catalog and note security exceptions (e.g., VPD policies). |
-- MAGIC | Demo<br/>[1.4 Demo - Discovery & Planning Phase]($./1.4 Demo - Discovery & Planning Phase) | Instructor-led demonstration | Hands-on demonstration of key concepts covered in this module. |
-- MAGIC | Lab<br/>[1.5 Lab - Discovery & Planning Phase]($./1.5 Lab - Discovery & Planning Phase) | Practice exercises | Interactive exercises to reinforce learning objectives from this module. |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
