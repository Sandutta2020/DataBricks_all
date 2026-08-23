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
# MAGIC # Migration Maturity Model
# MAGIC
# MAGIC Migration from **Oracle** to **Databricks** is a journey, not a single event. This module introduces a six-stage maturity model that provides a structured framework for planning, executing, and measuring migration progress.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lesson, you will be able to:
# MAGIC - Describe the six stages of migration maturity
# MAGIC - Identify key activities and outcomes for each stage
# MAGIC - Assess your organization's current position in the migration journey
# MAGIC - Understand dependencies between stages

# COMMAND ----------

# MAGIC %md
# MAGIC ## Why a Maturity Model?
# MAGIC
# MAGIC **Migration Is Not a Single Task**
# MAGIC
# MAGIC An Oracle to Databricks migration **cannot be treated as a single technical task** like exporting tables or translating SQL. It is a journey that unfolds over time as multiple parts of the platform are migrated and validated.
# MAGIC
# MAGIC **Benefits of a Phased Approach**
# MAGIC
# MAGIC | Benefit | Description |
# MAGIC |---------|-------------|
# MAGIC | **Reduced Risk** | Each phase validates before proceeding |
# MAGIC | **Measurable Progress** | Clear milestones and success criteria |
# MAGIC | **Stakeholder Alignment** | Everyone understands current state |
# MAGIC | **Rollback Capability** | Can pause or reverse at defined points |
# MAGIC | **Resource Planning** | Different skills needed at each stage |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## The Migration Maturity Model
# MAGIC <br />
# MAGIC <div style="color: #FF3621; font-weight: bold; font-size: 1.1em; margin-bottom: 12px;">A Structured Framework for Managing Migration Complexity and Risk</div>
# MAGIC
# MAGIC The Migration Maturity Model provides a phased approach to migrating from Oracle to Databricks. Each stage has clear entry criteria, deliverables, and exit gates - ensuring you progress methodically while maintaining business continuity.
# MAGIC
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

# COMMAND ----------

# MAGIC %md
# MAGIC ## Phase 1: Discovery & Planning
# MAGIC
# MAGIC **Goal:** Establish engagement framework, assess current state, and build detailed migration roadmap

# COMMAND ----------

# MAGIC %md
# MAGIC ### Skill Areas
# MAGIC
# MAGIC | Skill Area | Task | Key Activities |
# MAGIC |------------|------|----------------|
# MAGIC | **Engagement & Governance** | Define scope & approach | Select Prime, Assurance+, or Advisory package based on delivery ownership; Coordinate SKU/pricing with Engagement Manager; Provide customer datasheet outlining scope, expectations, and engagement model |
# MAGIC | **Stakeholder Alignment & Readiness** | Establish objectives & roles | Define objectives, deliverables, constraints, and SME scheduling; Interview Oracle SMEs on usage, downstream systems, pain points, workflows, politics; Confirm MVP use case for templating and communicate Lakehouse vision |
# MAGIC | **Discovery & Landscape Analysis** | Assess current state | Inventory databases and tables (leverage OEM and DBA_OBJECTS), code (DBA_SOURCE); map to Databricks equivalents; Document dependencies between datasets, jobs, and BI tools (DBA_DEPENDENCIES); prioritize workloads (lift-and-shift vs refactor); Capture persona access patterns, compute budgets, and timelines; Identify facts/dimensions, SCDs, and temporal logic; Review external tools for migration risk; Analyze resource usage (AWR/ASH reports — Oracle Automatic Workload Repository and Active Session History) |
# MAGIC | **Planning & Road-mapping** | Build migration plan | Sequence phases (ingest -> schema -> validation -> cutover) and align to success metrics; Define ingestion strategy (push/pull, API, batch/stream); note out-of-scope sources; Classify datasets (active vs legacy) and tag governance/access controls; Establish lineage and dependencies with catalog tooling; Extract schema metadata; Inventory automation and scheduling details; Identify redundant staging copies and define data minimization strategy; Capture user personas, tools, and security models; Inventory Git syncs and CI/CD patterns for Databricks integration; Map Oracle roles to Unity Catalog and note security exceptions |

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Outcomes
# MAGIC
# MAGIC ✅ Engagement model and SKU confirmed  
# MAGIC ✅ Stakeholder roles and objectives documented  
# MAGIC ✅ Complete inventory of Oracle objects with Databricks equivalents mapped  
# MAGIC ✅ Dependencies and lineage documented  
# MAGIC ✅ Prioritized migration candidates with complexity scoring  
# MAGIC ✅ Detailed migration plan with sequenced phases  
# MAGIC ✅ Success metrics defined

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #7b1fa2; background: #f3e5f5; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">📝</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #4a148c; font-size: 1.1em;">Note</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">No data or pipelines are migrated in this stage. This is purely discovery.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Phase 2: Architecture & Design
# MAGIC
# MAGIC **Goal:** Define target architecture and establish Databricks platform foundation

# COMMAND ----------

# MAGIC %md
# MAGIC ### Skill Areas
# MAGIC
# MAGIC | Skill Area | Task | Key Activities |
# MAGIC |------------|------|----------------|
# MAGIC | **Solution Architecture & Modeling** | Define target architecture | Define Databricks Data Intelligence Platform target (Lakehouse architecture: UC + Lakeflow Jobs and Lakeflow Spark Declarative Pipelines + SQL Warehouses); Map Oracle constructs (Stored procedures etc.) to Databricks features; Validate performance, scalability, and cost expectations; baseline metrics; Design Bronze/Silver/Gold flow, lineage, and CDC strategy |
# MAGIC | **Platform Setup & Environment** | Stand up foundation | Enable Unity Catalog; create metastore, catalogs, schemas; assign managed storage locations; Configure workspaces, clusters, serverless SQL Warehouses; bind workspace to UC; Create service credentials (IAM/service accounts) for staging/landing paths; Establish naming and privilege model (`USAGE`, `SELECT/MODIFY`) across UC objects |
# MAGIC | **Storage & Governance Design** | Define storage and policy model | Set up staging zones and object store bindings; grant least-privilege access; Establish ownership conventions and governance hierarchy |
# MAGIC | **Security & Access Design** | Implement role model | Apply RBAC/ABAC principles for tables and volumes; design audit and compliance framework |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Outcomes
# MAGIC
# MAGIC ✅ Target Lakehouse architecture documented (UC + Lakeflow Jobs and Lakeflow Spark Declarative Pipelines + SQL Warehouses)  
# MAGIC ✅ Oracle-to-Databricks feature mapping complete  
# MAGIC ✅ Unity Catalog enabled with catalogs, schemas, and managed storage  
# MAGIC ✅ Workspaces and clusters configured  
# MAGIC ✅ Service credentials and IAM paths established  
# MAGIC ✅ Naming conventions and privilege model defined  
# MAGIC ✅ Storage zones configured with governance hierarchy  
# MAGIC ✅ RBAC/ABAC security model designed

# COMMAND ----------

# MAGIC %md
# MAGIC ## Phase 3: Execution & Data Migration
# MAGIC
# MAGIC **Goal:** Execute data migration, convert schemas and code, rebuild pipelines

# COMMAND ----------

# MAGIC %md
# MAGIC ### Skill Areas
# MAGIC
# MAGIC | Skill Area | Task | Key Activities |
# MAGIC |------------|------|----------------|
# MAGIC | **Data Engineering & Ingestion** | Land Bronze data | Export Oracle tables to Parquet/CSV and ingest to Delta (Bronze -> Silver) via Auto Loader; Map schemas and types (e.g., `DATE` -> `TIMESTAMP`); define partitioning/clustering; Implement one-time data migration using JDBC connector or `COPY INTO` workflow |
# MAGIC | **Incremental Sync & CDC** | Enable change data flows | Implement Delta `MERGE` / `AUTO CDC INTO` with SCD Type 1/2; handle deletes via `APPLY AS DELETE WHEN`; Monitor CDC events and logs; validate sequencing and latency per SLA |
# MAGIC | **Schema & DDL Conversion** | Convert metadata to UC | Translate Oracle DDL to Unity Catalog Delta DDL; recreate views/materialized views; Adapt datatypes, constraints, and policies to Databricks SQL semantics; Handle differences in numeric precision, `DATE`/`TIMESTAMP` difference, and special types like `CLOB`, `BLOB` and `XMLTYPE`;|
# MAGIC | **SQL & Code Conversion** | Port logic to Databricks | Translate PL/SQL to Databricks SQL/UDFs (e.g. replace sequences and `ROWID`); Refactor for semi-structured logic; Validate query correctness and performance on representative datasets |
# MAGIC | **Pipeline & Orchestration** | Rebuild jobs and scheduling | Recreate PL/SQL packages and procedures as Lakeflow Jobs or Lakeflow Spark Declarative Pipelines; Replace triggers; Define dependencies and retries; Implement CI/CD with Repos and environment promotion |
# MAGIC | **Testing & Data Validation** | Verify accuracy and quality | Perform data parity checks (record counts, sums, nulls, string matches); Use testing frameworks (Spark Testing Base, Chispa, ScalaTest, Great Expectations); Define quantitative governance rules (counts, stddevs, timestamp bounds) in Delta metadata |

# COMMAND ----------

# MAGIC %md
# MAGIC ### Data Migration Decision Matrix
# MAGIC
# MAGIC | Data Type | Recommended Pattern | Rationale |
# MAGIC |-----------|---------------------|-----------|
# MAGIC | Historical/Archive | Snapshot (one-time) | Static, no updates |
# MAGIC | Reference/Dimension | Scheduled (daily) | Low change frequency |
# MAGIC | Transactional | CDC (real-time) | High change frequency |
# MAGIC | Aggregate/Reporting | Scheduled (hourly) | Batch-oriented |

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Outcomes
# MAGIC
# MAGIC ✅ Bronze layer populated from Oracle exports  
# MAGIC ✅ Schema and type mappings complete  
# MAGIC ✅ CDC/incremental sync patterns operational  
# MAGIC ✅ DDL converted to Unity Catalog  
# MAGIC ✅ Procedures rebuilt as Lakeflow Jobs or Lakeflow Spark Declarative Pipelines  
# MAGIC ✅ SQL and UDFs ported and validated  
# MAGIC ✅ Data parity checks passing

# COMMAND ----------

# MAGIC %md
# MAGIC ## Phase 4: Validation & Cutover
# MAGIC
# MAGIC **Goal:** Enable observability, validate production readiness, and execute cutover

# COMMAND ----------

# MAGIC %md
# MAGIC ### Skill Areas
# MAGIC
# MAGIC | Skill Area | Task | Key Activities |
# MAGIC |------------|------|----------------|
# MAGIC | **Observability & Monitoring** | Enable runtime visibility | Enable Lakeflow pipeline event logs and system tables for usage/lineage/access monitoring; Build operational dashboards for validation coverage and throughput; Tune partitioning, clustering, and caching before cutover |
# MAGIC | **Cutover Execution** | Transition to production | Plan freeze/rollback window; run delta catch-up; switch consumers to Databricks; Validate dashboards and reports post-cutover; obtain business sign-off |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Cutover Patterns
# MAGIC
# MAGIC | Pattern | Risk | Rollback | Best For |
# MAGIC |---------|------|----------|----------|
# MAGIC | **Blue-Green** | Low | Easy | Critical workloads |
# MAGIC | **Canary** | Low | Easy | High-volume workloads |
# MAGIC | **Parallel Run** | Low | Easy | Validation-heavy |
# MAGIC | **Big-Bang** | High | Hard | Simple environments |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Outcomes
# MAGIC
# MAGIC ✅ Lakeflow Pipelines event logs and system tables enabled  
# MAGIC ✅ Operational dashboards operational  
# MAGIC ✅ Performance tuned (partitioning, clustering, caching)  
# MAGIC ✅ Freeze/rollback window planned  
# MAGIC ✅ Consumers switched to Databricks  
# MAGIC ✅ Post-cutover validation complete  
# MAGIC ✅ Business sign-off obtained

# COMMAND ----------

# MAGIC %md
# MAGIC ## Phase 5: Enablement & Automation
# MAGIC
# MAGIC **Goal:** Operationalize platform with DevOps, security, and BI/ML integration

# COMMAND ----------

# MAGIC %md
# MAGIC ### Skill Areas
# MAGIC
# MAGIC | Skill Area | Task | Key Activities |
# MAGIC |------------|------|----------------|
# MAGIC | **DevOps & Platform Ops** | Operationalize workflows | Enable Databricks SQL Serverless for BI; test concurrency and cost scaling; Integrate CI/CD (Declarative Automation Bundles (DABs), GitHub Actions) for data and ML pipelines; Apply IaC best practices for workspace and security versioning |
# MAGIC | **Security & Fine-Grained Access** | Enforce policies | Apply row/column masks in Unity Catalog; use ABAC for central policy management; Use dynamic views for read-only joins; document grants and inheritance |
# MAGIC | **BI & ML Integration** | Validate consumption layers | Re-point BI tools to SQL Warehouses; validate dashboards and SLA compliance; Migrate ML pipelines to Lakehouse; register features in Unity Catalog |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Outcomes
# MAGIC
# MAGIC ✅ SQL Serverless enabled and tested for BI concurrency  
# MAGIC ✅ CI/CD pipelines integrated (GitHub Actions, DABs)  
# MAGIC ✅ IaC patterns applied for workspace management  
# MAGIC ✅ Row/column masking and ABAC policies enforced  
# MAGIC ✅ Dynamic views configured for secure data sharing  
# MAGIC ✅ BI tools repointed to SQL Warehouses  
# MAGIC ✅ ML pipelines migrated with features registered in Unity Catalog

# COMMAND ----------

# MAGIC %md
# MAGIC ## Phase 6: Closeout & Handoff
# MAGIC
# MAGIC **Goal:** Complete documentation, enable teams, and retire legacy Oracle

# COMMAND ----------

# MAGIC %md
# MAGIC ### Skill Areas
# MAGIC
# MAGIC | Skill Area | Task | Key Activities |
# MAGIC |------------|------|----------------|
# MAGIC | **Observability & Cost Monitoring** | Implement metrics collection | Integrate with JMX, Splunk, CloudWatch, Azure Monitor; configure alerts and billing tags |
# MAGIC | **Developer Enablement** | Equip engineering teams | Support Databricks Connect and VS Code IDE integration; standardize Repos and branch models; Document migration patterns and code refactor lessons learned |
# MAGIC | **Documentation & Knowledge Transfer** | Finalize project artifacts | Document architecture, metrics, and recovery procedures with DBU tagging; Record unit/regression tests and validation queries in source control; Deliver troubleshooting playbooks, CI/CD guides, and notification policies; Publish runbooks for operations; transfer ownership to Ops teams |
# MAGIC | **Decommission & Closure** | Retire legacy Oracle | Backup Oracle tables; archive metadata; Conduct final stakeholder review and close engagement |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Decommissioning Checklist
# MAGIC
# MAGIC ✅ Monitoring integrated (JMX, Splunk, CloudWatch, Azure Monitor)  
# MAGIC ✅ Alerts and billing tags configured  
# MAGIC ✅ Developer tooling enabled (Databricks Connect, VS Code, Repos)  
# MAGIC ✅ Migration patterns and lessons learned documented  
# MAGIC ✅ Architecture and recovery procedures documented  
# MAGIC ✅ Tests and validation queries in source control  
# MAGIC ✅ Playbooks and runbooks published  
# MAGIC ✅ Operations ownership transferred  
# MAGIC ✅ Oracle backup and metadata archived  
# MAGIC ✅ Connectors shut down  
# MAGIC ✅ Final stakeholder review complete  
# MAGIC ✅ Engagement closed  

# COMMAND ----------

# MAGIC %md
# MAGIC ### Post-Migration Optimization
# MAGIC
# MAGIC ✅ Continuous optimization (liquid clustering, predictive optimization, cost optimization and right sizing)  
# MAGIC ✅ New capability enablement (GenAI, streaming, ML)  
# MAGIC ✅ Training and enablement programs

# COMMAND ----------

# MAGIC %md
# MAGIC ## Migration Anti-Patterns
# MAGIC
# MAGIC Learning from failed migrations is as important as following best practices. These anti-patterns have derailed countless data platform migrations - recognizing them early can save months of rework and significant budget overruns.
# MAGIC
# MAGIC | Anti-Pattern | Risk Level | What Happens | How to Avoid |
# MAGIC |--------------|------------|--------------|--------------|
# MAGIC | **Skipping Assessment** | Critical | Incomplete scope discovery leads to missed dependencies, surprise complexity, and blown timelines - "unknown unknowns" surface mid-migration | Invest in thorough profiling (e.g. Lakebridge); map all workloads, data flows, and downstream consumers before writing a single line of migration code |
# MAGIC | **Big-Bang Migration** | Critical | Attempting to migrate everything at once with a single cutover date - no rollback path, extended outages, and catastrophic failure modes | Adopt phased migration by workload, schema, or business domain; maintain parallel operation; ensure rollback procedures are documented and tested |
# MAGIC | **Premature Decommission** | Critical | Retiring Oracle before downstream dependencies are migrated or data retention requirements are satisfied | Maintain source platform until all consumers are migrated; archive data per retention policies; get explicit sign-off from all stakeholder groups |
# MAGIC | **Lift-and-Shift Mentality** | High | Migrating existing architecture 1:1 without leveraging Databricks capabilities - you inherit legacy technical debt and miss the opportunity to modernize | Treat migration as a transformation, not a relocation; adopt medallion architecture, Unity Catalog governance, and Lakeflow Spark Declarative Pipelines rather than replicating legacy patterns |
# MAGIC | **No Parallel Validation** | High | Cutting over to Databricks without running both platforms in parallel - data quality issues surface in production, eroding user trust | Run parallel ETL processes for 1-2 weeks minimum; implement automated validation (row counts, checksums, business rules); require sign-off before deprecating source |
# MAGIC | **Ignoring Change Management** | Medium | Focusing only on technical migration while neglecting user training, communication, and organizational readiness | Develop training programs, update documentation, communicate timeline and impact; involve end users early in UAT |
# MAGIC | **Underestimating Governance** | Medium | Migrating data without replicating (or improving) access controls, lineage tracking, and compliance requirements | Map existing security model to Unity Catalog; validate RBAC/ABAC policies; ensure audit logging meets compliance needs before cutover |
# MAGIC | **Going Dark on Stakeholders** | Medium | Poor communication during migration leads to shadow IT, resistance, and parallel efforts that undermine the project | Establish regular status updates, stakeholder checkpoints, and escalation paths; celebrate milestones to maintain momentum |
# MAGIC
# MAGIC **Key Insight:** The most successful migrations treat the project as an opportunity to modernize, not just relocate. Organizations that simply replicate their legacy architecture in Databricks miss the transformative benefits of the lakehouse - and often end up with higher costs and complexity than they started with.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary and Key Takeaways
# MAGIC
# MAGIC Migration is a journey through six phases: **Discover -> Design -> Execute -> Validate -> Enable -> Closeout**. Each phase has clear skill areas, tasks, and activities enabling measured progress with rollback capability. The framework prevents the most common failure modes: skipping discovery, attempting big-bang cutovers, and treating migration as lift-and-shift rather than transformation.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Takeaways
# MAGIC
# MAGIC - **Phased approach reduces risk** - validate at each phase before proceeding; maintain rollback capability throughout
# MAGIC - **Discovery & Planning is non-negotiable** - skipping assessment leads to missed dependencies and blown timelines  
# MAGIC - **Architecture before execution** - establish Unity Catalog, storage design, and security model before moving data
# MAGIC - **Transformation, not relocation** - adopt medallion architecture and Unity Catalog rather than replicating legacy patterns
# MAGIC - **Validation gates at each phase** - data parity checks, performance benchmarks, and business sign-off required before cutover
# MAGIC - **Never decommission prematurely** - source platform stays live until all consumers are migrated, validated, and signed off

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
