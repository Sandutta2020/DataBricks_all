# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
# MAGIC     <div style="font-size: 14px; color: #666;">
# MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
# MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
# MAGIC         <span style="margin-left: 8px;">AGENDA</span>
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
# MAGIC # Oracle Migration to Databricks: Course Agenda
# MAGIC
# MAGIC <div style="display: flex; align-items: center; justify-content: center; gap: 40px; padding: 40px;">
# MAGIC     <div style="text-align: center;">
# MAGIC         <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="150" height="150" />
# MAGIC     </div>
# MAGIC     <div style="font-size: 96px; color: #999; display: flex; align-items: center; line-height: 1; margin-bottom: 20px;">-></div>
# MAGIC     <div style="text-align: center;">
# MAGIC         <img src="https://cdn.simpleicons.org/databricks/FF3621" width="150" height="150"/>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Course Overview
# MAGIC
# MAGIC This course provides a comprehensive, structured approach to migrating from **Oracle** to **Databricks**. The migration journey is organized into six modules that follow the recommended phased approach, reducing risk and ensuring successful outcomes.
# MAGIC <br />
# MAGIC <br />
# MAGIC <div class="mermaid"> 
# MAGIC flowchart LR
# MAGIC     S0["Phase 1<br/><b>DISCOVER</b><br/>Discovery & Planning"]
# MAGIC     S1["Phase 2<br/><b>DESIGN</b><br/>Architecture & Design"]
# MAGIC     S2["Phase 3<br/><b>EXECUTE</b><br/>Execution & Data Migration"]
# MAGIC     S3["Phase 4<br/><b>ACTIVATE</b><br/>Activation, Cutover & Validation"]
# MAGIC     S4["Phase 5<br/><b>ENABLE</b><br/>Enablement & Automation"]
# MAGIC     S5["Phase 6<br/><b>CLOSEOUT</b><br/>Closeout & Handoff"]
# MAGIC     S0 --> S1 --> S2 --> S3 --> S4 --> S5
# MAGIC     style S0 fill:#E8F4FD,stroke:#5A9BD5,stroke-width:2px
# MAGIC     style S1 fill:#E5F5F3,stroke:#5BA8A0,stroke-width:2px
# MAGIC     style S2 fill:#EFF6E8,stroke:#7CB342,stroke-width:2px
# MAGIC     style S3 fill:#FFF8E6,stroke:#E6AC00,stroke-width:2px
# MAGIC     style S4 fill:#FFEFE8,stroke:#E86A4A,stroke-width:2px
# MAGIC     style S5 fill:#FFE8E5,stroke:#D94530,stroke-width:2px 
# MAGIC </div> 
# MAGIC
# MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>
# MAGIC <br />
# MAGIC <hr/>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Module Structure
# MAGIC
# MAGIC | Module | Focus | Key Outcomes |
# MAGIC |--------|-------|--------------|
# MAGIC | [00 - Foundations]($./00 - Foundations/0.1 Lecture - Why Migrate to Databricks) | Why migrate, maturity stages, architecture mapping | Clear understanding of drivers and target state |
# MAGIC | [01 - Discover]($./01 - Discover/1.0 - Overview) | Engagement, stakeholder alignment, discovery, profiling, planning | Documented scope, dependencies, and roadmap |
# MAGIC | [02 - Design]($./02 - Design/2.0 - Overview) | Target architecture, platform setup, storage, security, interoperability patterns | Environment ready, governance in place |
# MAGIC | [03 - Execute]($./03 - Execute/3.0 - Overview) | Data ingestion, replication and interoperability patterns, schema creation, CDC | Data landed and flowing in Databricks |
# MAGIC | [04 - Activate]($./04 - Activate/4.0 - Overview) | Data validation, observability, cutover execution, activation | Verified correctness, performance, and sign-off |
# MAGIC | [05 - Enable]($./05 - Enable/5.0 - Overview) | Cost optimization, consumer integration, enablement | Platform optimized, client team enabled |
# MAGIC | [06 - Closeout]($./06 - Closeout/6.0 - Overview) | Documentation, decommissioning | Migration complete, source retired |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Licensing
# MAGIC
# MAGIC This courseware uses the  <a href="https://github.com/oracle-samples/db-sample-schemas/tree/main/human_resources" target="_blank">Oracle HR dataset</a>.
# MAGIC
# MAGIC ```
# MAGIC Copyright (c) 2023 Oracle and/or its affiliates. All rights reserved.
# MAGIC
# MAGIC Permission is hereby granted, free of charge, to any person obtaining
# MAGIC a copy of this software and associated documentation files (the
# MAGIC "Software"), to deal in the Software without restriction, including
# MAGIC without limitation the rights to use, copy, modify, merge, publish,
# MAGIC distribute, sublicense, and/or sell copies of the Software, and to
# MAGIC permit persons to whom the Software is furnished to do so, subject to
# MAGIC the following conditions:
# MAGIC
# MAGIC The above copyright notice and this permission notice shall be
# MAGIC included in all copies or substantial portions of the Software.
# MAGIC
# MAGIC THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# MAGIC EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MAGIC MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# MAGIC NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# MAGIC LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# MAGIC OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# MAGIC WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
