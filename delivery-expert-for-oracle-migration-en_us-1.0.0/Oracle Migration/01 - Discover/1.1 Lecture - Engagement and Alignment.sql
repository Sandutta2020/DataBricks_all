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
-- MAGIC # Engagement and Alignment
-- MAGIC
-- MAGIC Successful migrations begin before any data moves. This lesson covers the critical first steps: understanding engagement options, aligning stakeholders, and establishing clear objectives that drive every subsequent decision.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this lesson, you will be able to:
-- MAGIC
-- MAGIC - Understand the engagement options available from Databricks Professional Services
-- MAGIC - Define migration objectives, deliverables, and constraints with customer stakeholders
-- MAGIC - Identify key SMEs and establish communication cadence
-- MAGIC - Communicate the Lakehouse value proposition in context of Oracle migration

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 1. Engagement & Governance

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Professional Services Engagement Options
-- MAGIC
-- MAGIC Databricks Professional Services offers two primary engagement models for migration projects:
-- MAGIC
-- MAGIC | Engagement Model | Description | Best For |
-- MAGIC |------------------|-------------|----------|
-- MAGIC | **Full Migration Services** | Databricks leads delivery end-to-end | Organizations wanting turnkey delivery with expert guidance |
-- MAGIC | **Migration Assurance Services** | Databricks supports customer or SI partner delivery | Organizations with capable internal teams or SI partners who need expert oversight and guidance |
-- MAGIC
-- MAGIC Databricks also works with certified **Migration Brickbuilder SI partners** who provide automated tooling and delivery expertise. These partners can lead delivery with Databricks providing assurance services.
-- MAGIC
-- MAGIC **Key Actions:**
-- MAGIC - Engage your Databricks account team to discuss engagement options
-- MAGIC - Identify whether internal teams or SI partners will lead delivery
-- MAGIC - Understand the scope of assurance services if using partner delivery

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Databricks Migration Phases
-- MAGIC Databricks Professional Services uses a five-phase approach for migration projects:
-- MAGIC <div class="mermaid">
-- MAGIC flowchart LR
-- MAGIC     A["<b>Discovery</b><br/>Understand drivers<br/>& challenges"] --> B["<b>Assessment</b><br/>Analyze complexity<br/>& estimate effort"]
-- MAGIC     B --> C["<b>Strategy</b><br/>Design target<br/>architecture"]
-- MAGIC     C --> D["<b>Production Pilot</b><br/>Migrate end-to-end<br/>use case"]
-- MAGIC     D --> E["<b>Execution</b><br/>Scale migration<br/>& establish CoE"]
-- MAGIC     style A fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
-- MAGIC     style B fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
-- MAGIC     style C fill:#fff3e0,stroke:#f57c00,stroke-width:2px
-- MAGIC     style D fill:#fce4ec,stroke:#c2185b,stroke-width:2px
-- MAGIC     style E fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 2. Stakeholder Alignment & Readiness

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Establishing Objectives and Roles
-- MAGIC
-- MAGIC Before technical discovery begins, align on the "why" and "when" behind the migration. Common drivers include:
-- MAGIC
-- MAGIC - **Cost optimization** - Reduce Oracle license and maintenance costs (moving from CapEx to OpEx)
-- MAGIC - **Platform consolidation** - Unify analytics, ML, and engineering on one platform  
-- MAGIC - **New capabilities** - Enable AI/ML workloads, real-time streaming, or data sharing
-- MAGIC - **Hardware lifecycle** - Legacy hardware (e.g. Exadata) renewal or decommissioning approaching
-- MAGIC
-- MAGIC Document these drivers explicitly. They will guide prioritization decisions throughout the project.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Key Stakeholder Interviews
-- MAGIC
-- MAGIC Schedule discovery sessions with these roles:
-- MAGIC
-- MAGIC | Role | Focus Areas |
-- MAGIC |------|-------------|
-- MAGIC | **Data Engineering Lead** | Pipeline complexity, orchestration tools, pain points |
-- MAGIC | **Oracle DBA** | Schema complexity, AWR/ASH reports, CDC (GoldenGate/LogMiner) setup, networking |
-- MAGIC | **Analytics/BI Lead** | Downstream consumers, report dependencies, SLAs |
-- MAGIC | **Platform/Infra Lead** | Security model, networking, compliance requirements |
-- MAGIC | **Business Sponsor** | Success criteria, budget constraints, timeline drivers |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Stakeholder Communication Model
-- MAGIC <div id="stakeholder-diagram"></div>
-- MAGIC <script>
-- MAGIC (function() {
-- MAGIC   const puml = `@startuml
-- MAGIC !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
-- MAGIC HIDE_STEREOTYPE()
-- MAGIC title Migration Stakeholder Map
-- MAGIC Person(sponsor, "Business Sponsor", "Owns budget & success criteria")
-- MAGIC Person(eng_lead, "Data Engineering Lead", "Pipeline & orchestration SME")
-- MAGIC Person(dba, "Oracle DBA", "Oracle SME")
-- MAGIC Person(analytics, "Analytics Lead", "BI & reporting SME")
-- MAGIC Person(platform, "Platform Lead", "Security & infrastructure SME")
-- MAGIC System(migration, "Migration Team", "Databricks PS + Customer + SI")
-- MAGIC Rel(sponsor, migration, "Defines objectives")
-- MAGIC Rel(eng_lead, migration, "Integration requirements")
-- MAGIC Rel(dba, migration, "Oracle discovery")
-- MAGIC Rel(analytics, migration, "Consumer mapping")
-- MAGIC Rel(platform, migration, "Security review")
-- MAGIC @enduml`;
-- MAGIC   const encoded = Array.from(new TextEncoder().encode(puml))
-- MAGIC     .map(b => b.toString(16).padStart(2, '0'))
-- MAGIC     .join('');
-- MAGIC   const img = document.createElement('img');
-- MAGIC   img.src = `https://www.plantuml.com/plantuml/svg/~h${encoded}`;
-- MAGIC   img.alt = 'Stakeholder Map';
-- MAGIC   img.style.maxWidth = '100%';
-- MAGIC   document.getElementById('stakeholder-diagram').appendChild(img);
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### SME Interview Questions
-- MAGIC
-- MAGIC Use these questions to guide your Oracle SME interviews:
-- MAGIC
-- MAGIC **Usage & Workloads**
-- MAGIC - Which schemas or services see the heaviest usage? What drives that load?
-- MAGIC - Are there workloads that consistently hit performance limits?
-- MAGIC - What are the primary cost drivers? Are there legacy ELA (Enterprise License Agreement) or maintenance cost pressures?
-- MAGIC
-- MAGIC **Logic & Complexity**
-- MAGIC - How much business logic is embedded in PL/SQL (Packages, Procedures, Triggers)?
-- MAGIC - Are there many DB Links to other Oracle or non-Oracle databases?
-- MAGIC - Are you using specific features like Oracle Spatial, Text, or Advanced Security?
-- MAGIC
-- MAGIC **Downstream Dependencies**
-- MAGIC - What BI tools connect to Oracle? How are connections managed (TNS, JDBC)?
-- MAGIC - Which external systems consume data from Oracle (APIs, exports, shares)?
-- MAGIC
-- MAGIC **Pain Points**
-- MAGIC - What takes longer than it should today? (e.g., long-running batch windows)
-- MAGIC - Are there capabilities you wish you had but cannot implement due to hardware or version limitations?
-- MAGIC - Where do you see cost inefficiencies or budget pressure?
-- MAGIC
-- MAGIC **Organizational Dynamics**
-- MAGIC - Who are the power users we need to bring along early?
-- MAGIC - Are there teams with concerns about the migration we should address proactively?

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Selecting the MVP Use Case
-- MAGIC During the production pilot phase, a clearly defined end-to-end use case is migrated to Databricks from the legacy platform. This MVP should be:
-- MAGIC - **Representative** - Uses common patterns (batch ingestion, transformations, BI consumption)
-- MAGIC - **High value** - Delivers meaningful benefits post-cutover to validate the business case and build momentum
-- MAGIC - **Low risk** - Not business-critical; safe to iterate on
-- MAGIC - **Visible** - Success can be demonstrated to stakeholders
-- MAGIC - **Contained** - Limited dependencies to minimize scope creep
-- MAGIC A good approach is to start with the end goal: pick a reporting dashboard important for the business, identify the data and processes needed to create it, and migrate that complete flow as a test.
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Information</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">The course dataset mirrors a typical MVP scope: dimensional model, incremental loads, and downstream analytics.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Communicating the Lakehouse Vision
-- MAGIC
-- MAGIC When speaking with stakeholders, frame the migration in terms of outcomes, not technology:
-- MAGIC
-- MAGIC | Oracle Reality | Lakehouse Opportunity |
-- MAGIC |-------------------|----------------------|
-- MAGIC | Separate tools for analytics and ML | Unified platform for all data workloads |
-- MAGIC | Rigid, expensive hardware (Exadata/On-prem) | Elastic, cloud-native compute with Serverless |
-- MAGIC | Heavy reliance on proprietary PL/SQL | Open standards (SQL, Python, Spark) with better performance |
-- MAGIC | Complex CDC and integration setup | Native streaming with Lakeflow and simpler ingestion |
-- MAGIC
-- MAGIC Avoid positioning this as "replacing Oracle." Instead, emphasize expanding capabilities while optimizing costs.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Summary Checklist
-- MAGIC
-- MAGIC Before proceeding to Discovery & Landscape Analysis, confirm:
-- MAGIC
-- MAGIC ✅ Engagement model discussed with Databricks account team  
-- MAGIC ✅ Delivery ownership clarified (Databricks PS, SI partner, or internal)  
-- MAGIC ✅ Stakeholder interviews scheduled (Engineering, Analytics, Platform, DBA, Sponsor)  
-- MAGIC ✅ Migration drivers documented and prioritized  
-- MAGIC ✅ MVP use case identified for production pilot  
-- MAGIC ✅ Communication cadence established (weekly syncs, escalation path)  

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## References
-- MAGIC
-- MAGIC - [Databricks Migration Guide](https://docs.databricks.com/en/migration/index.html)
-- MAGIC - [Databricks Migration Solutions](https://www.databricks.com/solutions/migration)
-- MAGIC - [Databricks Professional Services](https://www.databricks.com/professional-services)
-- MAGIC - [Migration Strategy Blog Post](https://www.databricks.com/blog/databricks-migration-strategy-lessons-learned)
-- MAGIC - [Unity Catalog Documentation](https://docs.databricks.com/en/data-governance/unity-catalog/index.html)

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
