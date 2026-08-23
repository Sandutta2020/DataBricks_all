# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
# MAGIC     <div style="font-size: 14px; color: #666;">
# MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
# MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
# MAGIC         <span style="margin-left: 8px;">DELIVERY EXPERT</span>
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
# MAGIC # Delivery Expert Badge Certification
# MAGIC
# MAGIC <div style="display: flex; align-items: center; justify-content: center; gap: 40px; padding: 40px;">
# MAGIC     <div style="text-align: center;">
# MAGIC         <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="100" height="100" />
# MAGIC     </div>
# MAGIC     <div style="font-size: 64px; color: #999; display: flex; align-items: center; line-height: 1; margin-bottom: 20px;">-></div>
# MAGIC     <div style="text-align: center;">
# MAGIC         <img src="https://cdn.simpleicons.org/databricks/FF3621" width="100" height="100"/>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Overview
# MAGIC
# MAGIC The **Delivery Expert Badge Certification** is a comprehensive certification program designed for Databricks SI/Partners who demonstrate expertise in planning, designing, and executing successful migrations from **Oracle** to **Databricks**.
# MAGIC
# MAGIC This certification validates that partners have the knowledge and hands-on skills required to guide customers through every phase of a migration engagement - from initial discovery and assessment through execution and cutover.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Why Get Certified?
# MAGIC
# MAGIC | Benefit | Description |
# MAGIC |---------|-------------|
# MAGIC | **Demonstrate Expertise** | Validate your migration skills with a recognized Databricks certification |
# MAGIC | **Win More Engagements** | Differentiate your practice with proven Oracle-to-Databricks migration credentials |
# MAGIC | **Reduce Risk** | Apply battle-tested methodologies and best practices to deliver successful migrations |
# MAGIC | **Access Resources** | Gain access to migration tooling, templates, and Databricks support channels |
# MAGIC | **Build Confidence** | Give customers assurance that their migration is in expert hands |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Certification Path
# MAGIC
# MAGIC The Delivery Expert certification is earned by completing three progressive courses, each with hands-on lab assessments. The program builds skills from initial assessment through successful execution.
# MAGIC
# MAGIC <table style="width:100%; border-collapse: collapse;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #f5f5f5;">
# MAGIC       <th style="border: 1px solid #ddd; padding: 10px;"></th>
# MAGIC       <th style="border: 1px solid #ddd; padding: 10px;">Skills</th>
# MAGIC       <th style="border: 1px solid #ddd; padding: 10px;">Courses</th>
# MAGIC       <th style="border: 1px solid #ddd; padding: 10px;">Assessment</th>
# MAGIC       <th style="border: 1px solid #ddd; padding: 10px;">Badge</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;"><strong>Migration Assessment</strong></td>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;">
# MAGIC         • Executing Discovery Workshops<br>
# MAGIC         • Architecture Assessment<br>
# MAGIC         • Feature mapping
# MAGIC       </td>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;">
# MAGIC         <strong>Course 1:</strong><br>
# MAGIC         How to assess a migration project
# MAGIC       </td>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;">
# MAGIC         <strong>Hands-on Lab:</strong><br>
# MAGIC         Assessing a migration project
# MAGIC       </td>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px; text-align: center;">
# MAGIC         <img src="assets/images/tech-presales-expert.png" alt="Tech Presales Expert" style="width: 80px; height: auto;"><br>
# MAGIC         <strong>TECH PRESALES EXPERT</strong>
# MAGIC       </td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;"><strong>Migration Preparation</strong></td>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;">
# MAGIC         • Profiling Tools<br>
# MAGIC         • Cost estimation<br>
# MAGIC         • Migration process<br>
# MAGIC         • Failover plan
# MAGIC       </td>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;">
# MAGIC         <strong>Course 2:</strong><br>
# MAGIC         How to prepare a migration project
# MAGIC       </td>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;">
# MAGIC         <strong>Hands-on Lab:</strong><br>
# MAGIC         Preparing a migration project
# MAGIC       </td>
# MAGIC       <td rowspan="2" style="border: 1px solid #ddd; padding: 10px; text-align: center; vertical-align: middle;">
# MAGIC         <img src="assets/images/tech-delivery-expert.png" alt="Delivery Expert" style="width: 80px; height: auto;"><br>
# MAGIC         <strong>DELIVERY EXPERT</strong>
# MAGIC       </td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;"><strong>Migration Execution</strong></td>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;">
# MAGIC         • Schema migration<br>
# MAGIC         • Validation<br>
# MAGIC         • Performing Cutlovers<br>
# MAGIC         • Downstream tool integration
# MAGIC       </td>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;">
# MAGIC         <strong>Course 3:</strong><br>
# MAGIC         How to execute a migration project
# MAGIC       </td>
# MAGIC       <td style="border: 1px solid #ddd; padding: 10px;">
# MAGIC         <strong>Hands-on Lab:</strong><br>
# MAGIC         Executing a migration project
# MAGIC       </td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Course Details

# COMMAND ----------

# MAGIC %md
# MAGIC ### Course 1: Migration Assessment
# MAGIC
# MAGIC Learn how to conduct effective discovery workshops, assess source Oracle environments, and map features to Databricks equivalents.
# MAGIC
# MAGIC | Topic | Description |
# MAGIC |-------|-------------|
# MAGIC | Discovery Workshops | Facilitate stakeholder sessions to understand business requirements, pain points, and success criteria |
# MAGIC | Architecture Assessment | Analyze current Oracle architecture including warehouses, databases, schemas, and workloads |
# MAGIC | Feature Mapping | Map Oracle constructs (Tasks, Streams, Stored Procedures, UDFs) to Databricks equivalents |
# MAGIC | Complexity Scoring | Apply T-shirt sizing and effort estimation frameworks to scope the migration |
# MAGIC
# MAGIC **Assessment:** Hands-on lab demonstrating assessment of a sample Oracle environment
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Course 2: Migration Preparation
# MAGIC
# MAGIC Master the tools and processes required to plan and prepare for a successful migration.
# MAGIC
# MAGIC | Topic | Description |
# MAGIC |-------|-------------|
# MAGIC | Profiling Tools | Use Oracle Account Usage, Query History, and Lakebridge for workload analysis |
# MAGIC | Cost Estimation | Build accurate TCO models comparing Oracle and Databricks costs |
# MAGIC | Migration Process | Design wave-based migration plans with clear milestones and dependencies |
# MAGIC | Failover Planning | Create rollback procedures and business continuity plans |
# MAGIC
# MAGIC **Assessment:** Hands-on lab creating a migration plan for a complex Oracle environment

# COMMAND ----------

# MAGIC %md
# MAGIC ### Course 3: Migration Execution
# MAGIC
# MAGIC Execute migrations with confidence using proven patterns for schema conversion, validation, and cutover.
# MAGIC
# MAGIC | Topic | Description |
# MAGIC |-------|-------------|
# MAGIC | Schema Migration | Convert Oracle DDL to Databricks, including data type mapping and Unity Catalog setup |
# MAGIC | Data Validation | Implement automated validation frameworks for data quality and completeness |
# MAGIC | Performing Cutlovers | Execute parallel runs, traffic switching, and production cutover procedures |
# MAGIC | Downstream Integration | Reconnect BI tools, applications, and APIs to the new Databricks environment |
# MAGIC
# MAGIC **Assessment:** Hands-on lab executing a full migration including cutover and validation

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prerequisites
# MAGIC
# MAGIC Before starting the Delivery Expert certification program, candidates should:
# MAGIC
# MAGIC | Requirement | Details |
# MAGIC |-------------|----------|
# MAGIC | **Databricks Certification** | Databricks Certified Data Engineer Professional |
# MAGIC | **Oracle Knowledge** | SnowPro Core or equivalent hands-on experience |
# MAGIC | **Course Completion** | Complete the Oracle Migration to Databricks course materials |
# MAGIC | **Environment Access** | Access to both Databricks and Oracle environments for lab exercises |
# MAGIC
# MAGIC See the [PREREQUISITES]($./PREREQUISITES) notebook for detailed requirements.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Getting Started
# MAGIC
# MAGIC Ready to become a certified Delivery Expert? Follow these steps:
# MAGIC
# MAGIC 1. **Review Prerequisites** - Ensure you meet the certification requirements
# MAGIC 2. **Complete Course Materials** - Work through the [course modules]($./AGENDA) in sequence
# MAGIC 3. **Register for Certification** - Contact your Databricks Partner Development representative
# MAGIC 4. **Complete Assessments** - Pass hands-on labs for each course
# MAGIC 5. **Earn Your Badge** - Receive your Delivery Expert certification
# MAGIC
# MAGIC <hr/>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Contact
# MAGIC
# MAGIC For questions about the Delivery Expert certification program:
# MAGIC
# MAGIC | Resource | Contact |
# MAGIC |----------|----------|
# MAGIC | **Partner Development** | Contact your Databricks Partner Development team |
# MAGIC | **Certification Support** | Reach out to your Databricks account team |
# MAGIC | **Course Materials** | See the [AGENDA]($./AGENDA) for course content |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
