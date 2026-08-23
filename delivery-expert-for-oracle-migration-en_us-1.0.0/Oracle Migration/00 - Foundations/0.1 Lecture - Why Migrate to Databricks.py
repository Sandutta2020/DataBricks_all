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

# MAGIC %md-sandbox
# MAGIC # Why Migrate to Databricks
# MAGIC
# MAGIC This foundational module articulates the business and technical drivers for migrating from **Oracle** to **Databricks**. Understanding the "why" is critical for building stakeholder alignment, justifying investment, and setting realistic expectations for the migration journey.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lesson, you will be able to:
# MAGIC - Articulate the key business drivers for migration
# MAGIC - Explain the technical advantages of the Databricks Lakehouse architecture
# MAGIC - Identify opportunities for platform consolidation and new capabilities
# MAGIC - Understand the Total Cost of Ownership (TCO) considerations
# MAGIC
# MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">ℹ️</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">A note on Oracle</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">There are many different ways of how an organization might use Oracle products: on-prem, public cloud, OCI etc. This document focuses mostly on the on-prem case, with some extra aspects for cloud applications.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Business Drivers
# MAGIC
# MAGIC Migration decisions are rarely purely technical. Understanding the business case is essential for securing sponsorship, prioritizing workloads, and measuring success.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Total Cost of Ownership (TCO) Optimization
# MAGIC
# MAGIC **Key Consideration:** When comparing TCO, evaluate these cost factors across both platforms:
# MAGIC
# MAGIC | Cost Factor | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
# MAGIC |-------------|-------------------|------------|
# MAGIC | **Compute pricing model** | Licensed by physical CPU core (Processor license) or Named User Plus. Requires upfront capital and fixed annual support contract, inflexible. | Flexible DBU-based pricing with workload-optimized compute: All-purpose clusters for interactive/developer use, Jobs clusters for scheduled pipelines, and SQL warehouses for BI workloads - available in both classic and serverless options |
# MAGIC | **Storage costs** | Data stored in proprietary format, scaling storage involves buying new Exadata storage cells | Data stored in **your** cloud-native object storage (S3, ADLS Gen2, GCS) using open Delta Lake format - you control retention, lifecycle policies, and avoid proprietary storage lock-in |
# MAGIC | **Orchestration and ETL** | ETL often requires Goldengate (extra licensing cost) or third-party software such as Informatica or Talend | Natively integrated tooling with Lakeflow Jobs for orchestration, Lakeflow Connect for data ingestion, and Lakeflow Spark Declarative Pipelines for reliable batch and streaming ETL - no additional licensing or third-party tools required |
# MAGIC | **Query and Processing Efficiency** | Relies on indexes, materialized views, and Exadata "Smart Scans." Tuning is manual and requires specialized DBA expertise to maintain performance as data grows. | Photon engine - a vectorized query engine included in the Databricks runtime that delivers world-class price/performance for analytics workloads |
# MAGIC | **Scalability and Concurrency** | Scaling up often involves buying bigger servers or extra Exadata hardware, scaling down is difficult, High concurrency can lead to resource contention | Auto-scaling SQL warehouses (classic and serverless) support high-concurrency use cases, automatically scaling resources to match demand and scaling down when idle to minimize costs |
# MAGIC | **Licence Audits** | Uses internal resources, might result in fines for honest mistakes (accidental usage or core factor issues with VMs) | All features are available, pay for what you consume |
# MAGIC | **Premier Support Cost Escalation** | Multi-tiered support system that tends to get pricier every year, eventually forcing an upgrade | Support is a technical and not a licensing matter, new features are released to existing customers |
# MAGIC
# MAGIC
# MAGIC **TCO Analysis Tips:**
# MAGIC - Compare like-for-like workloads, not just list prices
# MAGIC - Factor in hidden costs (data egress, premium features, support tiers, proprietary format lock-in)
# MAGIC - Consider the long-term cost trajectory of each platform and open format benefits
# MAGIC - Include productivity gains from unified platform (single governance with Unity Catalog, integrated ML/AI capabilities)
# MAGIC - Account for reduced tooling sprawl - Databricks consolidates ETL, orchestration, BI, ML and AI on one platform

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Differentiators
# MAGIC
# MAGIC **Key Consideration:** By migrating to an open, cloud-agnostic, and cost-effective modern data platform like Databricks, organizations can take advantage of cutting-edge data management solutions. This strategic move streamlines operations, fosters innovation, and drives competitive advantage in an increasingly data-driven business landscape.
# MAGIC
# MAGIC **Comparison:**
# MAGIC
# MAGIC | Aspect | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
# MAGIC |--------|------------------------|--------------------------------|
# MAGIC | **Unified Platform** | Separate services for data warehousing (Exadata/ADW), ML/AI (Oracle Machine Learning), and BI (Oracle Analytics) | Single platform for data warehousing, data science, machine learning, and BI; simplified data stack |
# MAGIC | **Cost-Effectiveness** | High TCO and complex licensing model; ongoing maintenance, support, and additional licensing costs | Flexible pricing model ("Pay as you go" or "Committed Use Contracts") with zero licensing cost |
# MAGIC | **Scalability** | Proprietary hardware/architecture limits flexibility in scaling big data workloads | Better scalability for big data workloads; handle growing volumes more efficiently |
# MAGIC | **Open-Source Ecosystem** | Vendor lock-in; proprietary tools (GoldenGate, ODI) and deep integration make migration away complex and costly | Leverages open-source (Apache Spark™, Delta Sharing, Unity Catalog); easy integration with other tools |
# MAGIC | **Collaborative Environment** | Siloed environments for different data roles | Collaborative notebooks and workspaces enhancing team productivity |
# MAGIC | **Cloud-Agnostic** | Primarily tied to OCI for full capabilities | Runs on AWS, Azure, and GCP; offering more flexibility in cloud strategy |
# MAGIC | **Performance** | Traditional database architecture can be slower for big data workloads | Optimized Spark engine with Photon delivers better performance for big data |
# MAGIC | **Governance**  | Siloed governance model split between Oracle Database and OCI IAM service. | Unified and open governance approach through Unity Catalog managing structured and unstructured data, ML models, notebooks, dashboards and files across multiple clouds. |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Platform Consolidation
# MAGIC
# MAGIC **Single Source of Truth, Unified Data Platform**
# MAGIC
# MAGIC Many organizations operate with fragmented data systems and supporting infrastructure:
# MAGIC
# MAGIC **Benefits of Consolidation:**
# MAGIC - Eliminate data silos and duplication
# MAGIC - Single governance model across all workloads (including ML/AI products as well as data assets)
# MAGIC - *"Batteries Included"* tooling (from ingestion through to serving)
# MAGIC - Consistent metrics and definitions
# MAGIC - Reduced operational complexity

# COMMAND ----------

# MAGIC %md
# MAGIC ### Avoiding Vendor Lock-in
# MAGIC
# MAGIC The Databricks platform is built on core open source technologies, many of which Databricks created, including:
# MAGIC
# MAGIC - [**Apache Spark**](https://spark.apache.org/docs/latest/index.html) - Distributed processing engine for batch and streaming workloads
# MAGIC - [**Delta Lake**](https://delta.io/) - Open table format with ACID transactions, time travel, and schema evolution
# MAGIC - [**Apache Iceberg**](https://iceberg.apache.org/) - Open table format with cross-platform interoperability (UniForm provides automatic compatibility)
# MAGIC - [**Unity Catalog**](https://www.unitycatalog.io/) - Open governance layer for data and AI assets (open sourced in 2024)
# MAGIC - [**MLflow**](https://mlflow.org/) - Open source framework to build and manage AI applications and models 
# MAGIC
# MAGIC **Open Formats vs Proprietary Formats**
# MAGIC
# MAGIC | Aspect | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
# MAGIC |--------|-------------------|------------|
# MAGIC | **Table formats** | Proprietary data format in .dbf files. Access with external tools is limited | Delta Lake and Iceberg (open source) for both managed and external tables; UniForm enables automatic cross-format compatibility. Data is readable by any compatible tool without vendor dependency |
# MAGIC | **Data portability** | Data export required; subject to vendor processes and potential fees | Data stored as Parquet files in your cloud storage - directly accessible without Databricks |
# MAGIC | **Code portability** | Limited: PL/SQL is powerful but proprietary, moving logic needs rewriting stored procedures | Code runs on open source Apache Spark, with some platform specific extras - easy to adapt to other Spark environments |
# MAGIC | **Interoperability** | Limited to the vendors ecosystem and connectors | Native support for Iceberg, Hudi, and Parquet; Delta Sharing for cross-platform data exchange |
# MAGIC | **Governance** | Proprietary metadata and access control system. Moving to a new database requires rebuilding the security system | Unity Catalog (open source) - avoid proprietary metadata lock-in |
# MAGIC | **Transparency** | Closed source, black box; you trust vendor claims without ability to verify | Open source core - inspect the code, understand behavior, contribute fixes, and influence roadmap through community participation |
# MAGIC
# MAGIC **Why This Matters:** Organizations investing in a data platform need assurance that their data, metadata, and processing logic aren't trapped in proprietary formats. Open source foundations mean your investment in skills, tooling, and data architecture remains portable - you're building on community standards, not a single vendor's roadmap.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Enabling New Use Cases
# MAGIC
# MAGIC **AI/ML, Real-Time Analytics, and Streaming**
# MAGIC
# MAGIC Databricks enables workloads that may be difficult, expensive, or impossible on traditional data warehouse platforms. Migration is an opportunity to modernize - not just replicate.
# MAGIC
# MAGIC | Use Case | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
# MAGIC |----------|-------------------|------------|
# MAGIC | **Machine Learning** | Oracle ML, limited to SQL or specific Python/R wrappers. Hard to scale for deep learning or large-scale unstructured data | Native ML Runtime with OSS packages, MLflow for experiment tracking, Feature Store, AutoML, and Model Serving - all integrated. Extendable with any Python/R library. |
# MAGIC | **Generative AI** | Primarily relies on calling external LLMs via PL/SQL, limited native capabilities | Foundation Model APIs, Vector Search for RAG applications, Mosaic AI Agent Framework, AI Gateway for model management |
# MAGIC | **Real-Time Streaming** | Requires separate tools like GoldenGate (extra fee) or Kafka, might result in \"stale\" data due to the friction between OLTP and OLAP systems | Spark Structured Streaming with sub-second latency; Lakeflow Spark Declarative Pipelines for declarative streaming pipelines |
# MAGIC | **Change Data Capture** | Usually requires extra licensing and "plumbing" to move data to downstream apps | Delta Change Data Feed with native SCD Type 1 and Type 2 support in Lakeflow Spark Declarative Pipelines (SCD = Slowly Changing Dimensions: Type 1 overwrites history, Type 2 preserves it) |
# MAGIC | **Data Science** | Sharing code is difficult in an on-prem setup, data scientists often work in isolation | Mature notebook environment with collaborative workspace, Git integration, integrated repos, and experiment tracking |
# MAGIC | **Data Sharing** | Either requires the recipient to have Oracle license or needs exports | Delta Sharing (open protocol) - share data with any platform, no vendor lock-in |
# MAGIC | **BI and Analytics** | Oracle Analytics Server (additional costs) or Oracle APEX (less convenient), external integrations through a gateway | Databricks SQL with Photon - world-class price/performance; validated integrations with Tableau, Power BI, Qlik, ThoughtSpot, Sigma, Looker |
# MAGIC
# MAGIC
# MAGIC **Migration as Modernization Opportunity:**
# MAGIC
# MAGIC Consider reengineering pipelines during migration to leverage capabilities that aren't straightforward on legacy platforms:
# MAGIC - **CDC and streaming workloads** - Spark Structured Streaming and Lakeflow Spark Declarative Pipelines provide a standard framework for both batch and streaming
# MAGIC - **SCD Type 2 tables** - Native support in Lakeflow Spark Declarative Pipelines vs. complex implementations on legacy platforms
# MAGIC - **Unified analytics** - Data instantly available for ML, AI, and ad hoc analysis without moving data between systems
# MAGIC
# MAGIC **Key Question:** What new capabilities does your organization need that your current platform cannot efficiently provide?

# COMMAND ----------

# MAGIC %md
# MAGIC ## Technical Drivers
# MAGIC
# MAGIC Beyond business considerations, technical capabilities often drive migration decisions.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Thought Leadership and Lakehouse Architecture
# MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">ℹ️</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Databricks is the Thought Leader in Modern Data Architecture</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">While the Lakehouse concept has now been adopted industry-wide (BigQuery, Oracle, Microsoft Fabric), Databricks originated these architectural paradigms and continues to drive innovation in this space.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC | Innovation | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks Origin</span> | Industry Adoption |
# MAGIC |------------|--------|-------------------|
# MAGIC | **Lakehouse Architecture** | Databricks coined the term and published the foundational research combining data lake flexibility with warehouse reliability | Now adopted by Oracle, Google BigQuery, Microsoft Fabric, and others |
# MAGIC | **Medallion Architecture** | Databricks introduced Bronze/Silver/Gold layering (~2019) as a design pattern for progressive data refinement | Microsoft Fabric uses identical terminology; pattern now considered industry standard |
# MAGIC | **Delta Lake** | Created by Databricks, open-sourced to bring ACID transactions to data lakes | Sparked the open table format movement; competitors responded with Iceberg adoption |
# MAGIC | **Unity Catalog** | Databricks developed unified governance for data and AI assets, open-sourced in 2024 | Setting the standard for lakehouse governance |
# MAGIC
# MAGIC **Why Thought Leadership Matters for Your Migration:**
# MAGIC
# MAGIC - **Proven patterns**: You're adopting architectures that have been battle-tested across thousands of enterprise deployments, not vendor retrofits
# MAGIC - **Continuous innovation**: Databricks invests heavily in R&D - new capabilities (Photon, Serverless, AI/ML integration) are designed lakehouse-native, not bolted on
# MAGIC - **Community momentum**: Open source foundations (Spark, Delta Lake, MLflow) mean a vast ecosystem of talent, tooling, and integrations
# MAGIC - **Architecture alignment**: The platform was *built* for these patterns, not adapted to compete with them
# MAGIC
# MAGIC **Key Lakehouse Benefits:**
# MAGIC - Single copy of data serves BI, data science, ML, and AI workloads - no data movement required
# MAGIC - ACID transactions on cloud object storage with Delta Lake
# MAGIC - Schema enforcement and evolution without pipeline rewrites
# MAGIC - Time travel and audit history built into the table format
# MAGIC - Unified batch and streaming on the same tables

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Open Source Foundation
# MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">ℹ️</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Built on Battle-Tested, Community-Driven Technologies</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Databricks is built on open source projects with massive adoption, active communities, and proven production reliability at scale.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC | Component | What It Is | Why It Matters |
# MAGIC |-----------|------------|----------------|
# MAGIC | **Apache Spark** | Distributed processing engine for batch and streaming workloads | Industry standard with 2,000+ contributors; skills transferable across any data organization; powers ETL, ML, and analytics at petabyte scale |
# MAGIC | **Delta Lake** | Open table format adding reliability to data lakes | ACID transactions, time travel, schema evolution, and unified batch/streaming - created by Databricks, now an industry standard |
# MAGIC | **Apache Parquet** | Columnar storage format optimized for analytics | 10x compression vs. row formats; supported by virtually every analytics tool; your data remains readable without any vendor |
# MAGIC | **MLflow** | End-to-end ML lifecycle management | Track experiments, package models, manage deployments - created by Databricks, used by 18M+ monthly users across any ML platform |
# MAGIC | **Apache Iceberg** | Open table format with cross-platform compatibility | UniForm enables Delta tables to be read as Iceberg - interoperability without data duplication |
# MAGIC | **Unity Catalog** | Unified governance for data and AI assets | Open-sourced in 2024 - avoid proprietary metadata lock-in; portable governance across platforms |
# MAGIC
# MAGIC **Why Open Source Matters for Your Organization:**
# MAGIC
# MAGIC | Consideration | Proprietary Stack | Open Source Foundation |
# MAGIC |---------------|-------------------|------------------------|
# MAGIC | **Talent pool** | Limited to vendor-certified specialists | Millions of Spark/Python developers globally; skills transfer between employers |
# MAGIC | **Community support** | Vendor support tiers and SLAs | Stack Overflow, GitHub, conferences, and thousands of contributors solving real problems |
# MAGIC | **Innovation velocity** | Dependent on single vendor's roadmap | Community-driven innovation from Netflix, Meta, Uber, Databricks, and thousands of others |
# MAGIC | **Transparency** | Closed roadmap, opaque algorithms | Open development, public issues, auditable code |
# MAGIC | **Longevity** | Tied to vendor's business viability | Projects outlive any single company; Apache governance ensures continuity |
# MAGIC | **Integration ecosystem** | Vendor-approved partners only | Broad ecosystem - any tool that reads Parquet/Delta can access your data |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Unified Governance with Unity Catalog
# MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">ℹ️</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">One Governance Layer for All Data and AI Assets</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Unity Catalog provides unified governance across your entire data and AI estate - tables, files, ML models, notebooks, and dashboards - all managed through a single, open-source catalog that was purpose-built for the lakehouse.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC | Capability | What It Does | Why It Matters |
# MAGIC |------------|--------------|----------------|
# MAGIC | **Unified Access Control** | Single permission model across all data assets using standard SQL GRANT/REVOKE syntax | No more managing separate access policies for tables, files, and ML models; one policy applies everywhere |
# MAGIC | **Fine-Grained Security** | Table, column, and row-level security with attribute-based access control | Protect sensitive data at the most granular level; dynamic data masking without duplicating data |
# MAGIC | **Automatic Data Lineage** | Column-level lineage tracking captured automatically from all workloads | Understand data origins, trace issues to source, satisfy regulatory requirements without manual documentation |
# MAGIC | **Comprehensive Audit Logging** | Every data access and operation recorded with full context | Answer "who accessed what, when, and how" for compliance; feed directly to your SIEM |
# MAGIC | **Data Discovery & Search** | Search, browse, tag, and document all data assets with AI-powered suggestions | Find trusted data across the organization; reduce duplicate datasets and shadow IT |
# MAGIC | **Delta Sharing** | Share data with external consumers using an open protocol - no proprietary connectors | Cross-organization collaboration without data copies; recipients don't need Databricks |
# MAGIC | **Lakehouse Federation** | Query external data sources (PostgreSQL, MySQL, Oracle, etc.) through Unity Catalog | Unified governance even for data that hasn't migrated yet; single pane of glass |
# MAGIC
# MAGIC **Comparison with Oracle:**
# MAGIC
# MAGIC | Aspect | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Unity Catalog</span> |
# MAGIC |--------|-------------------|---------------|
# MAGIC | **Catalog Architecture** | Siloed Instances: Metadata is tied to specific database instances; managing a unified view across multiple clusters requires complex manual integration. | Unified Intelligence: A single, global catalog for all data, ML models, and files. One interface to discover and govern every asset across the organization. |
# MAGIC | **Governance Scope** | Table-Centric: Strong security for relational tables, but governing unstructured files or ML models often requires fragmented, external tools. | Full-Spectrum: Native, consistent governance for tables, volumes (files), ML models, and AI functions — all using the same security policies. |
# MAGIC | **Data Lineage** | Manual/Additive: Tracking how data flows through various ETL steps often requires high-end licensing for OEMM and specialized metadata tools. Readily available if you use Oracle Data Integrator (ODI) or cloud-based Oracle database. | End-to-End & Automatic: Captures column-level lineage natively across all workloads (SQL, Python) with no manual instrumentation required. |
# MAGIC | **AI & Model Governance** | Disconnected: ML models are managed as database objects separate from the training data lineage, making "auditability" a manual process. | Integrated MLflow: Models and features are governed as first-class citizens. You can trace a production model back to the exact version of the data used to train it. |
# MAGIC | **Federated Reach** | Inward-Looking: Primarily optimized for Oracle-to-Oracle connectivity; querying external clouds or platforms often introduces performance and security lag. | Lakehouse Federation: Seamlessly query external sources (including Oracle, Snowflake, or SQL Server) through a single point of governance and security. |
# MAGIC | **Sharing Philosophy** | Platform-Bound: Sharing data typically requires the recipient to be on an Oracle-compatible stack, often leading to proprietary "walled gardens." | Open Sharing (Delta Sharing): An open-source protocol that allows you to share live data with any user on any platform—no vendor lock-in or Databricks account required. |
# MAGIC | **Metadata Future-Proofing** | Proprietary: Metadata and catalogs are locked into Oracle’s internal formats, making it difficult to migrate or use with third-party open-source tools. | Open Source Standard: Unity Catalog is open-sourced, ensuring that your organization’s metadata remains accessible and isn't tied to a single vendor’s roadmap. |
# MAGIC
# MAGIC
# MAGIC **Key Differentiator:** Unity Catalog governs not just data, but the entire AI lifecycle - ML models, feature tables, model endpoints, and AI agents - under the same unified permission model. As AI becomes central to data platforms, governance that spans both data and AI is essential.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Multi-Language Support
# MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">ℹ️</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">One Platform, Any Language - Meet Your Teams Where They Are</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Databricks was a pioneer in bringing notebooks into the mainstream as a first-class data platform interface - an approach now adopted by Oracle, BigQuery, and other platforms. Unlike single-language environments, Databricks lets SQL analysts, Python engineers, R statisticians, and Scala developers collaborate in the same workspace, on the same data, with seamless interoperability.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC | Language | Primary Use Cases | Why It Matters |
# MAGIC |----------|-------------------|----------------|
# MAGIC | **SQL** | BI analysts, data analysts, reporting, ad-hoc queries | Lowest barrier to entry; analysts productive immediately without learning new languages |
# MAGIC | **Python** | Data engineering, ML/AI, automation, general purpose | Most popular data language; vast ecosystem of libraries (pandas, scikit-learn, PyTorch) |
# MAGIC | **R** | Statistical analysis, academic research, biostatistics | Preferred by statisticians and researchers; rich visualization and statistical packages |
# MAGIC | **Scala** | Performance-critical Spark applications, low-level optimization | Native Spark language; maximum performance for complex distributed workloads |
# MAGIC
# MAGIC **Flexibility and Interoperability:**
# MAGIC
# MAGIC | Capability | What It Enables |
# MAGIC |------------|-----------------|
# MAGIC | **Mixed-language notebooks** | Combine SQL, Python, R, and Scala cells in a single notebook - use the right language for each task |
# MAGIC | **Seamless data handoff** | Query results from SQL flow directly into Python DataFrames |
# MAGIC | **Shared compute** | All languages run on the same clusters, accessing the same data with the same permissions |
# MAGIC | **Collaborative workspaces** | Data engineers write Python ETL, analysts query results in SQL, data scientists build models in R - all on one platform |
# MAGIC | **Git integration** | Version control notebooks in any language; enable CI/CD workflows for all team members |
# MAGIC | **Language-specific libraries** | Install PyPI, CRAN, or Maven packages as needed |
# MAGIC
# MAGIC **Comparison with Oracle:**
# MAGIC
# MAGIC | Aspect | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
# MAGIC |--------|-------------------|---------------|
# MAGIC | **Desktop software** | SQL Developer, being phased out (feature freeze) | none |
# MAGIC | **Browser access** | Oracle Database Actions (formerly SQL Developer Web) | Databricks workspaces in the browser for user-friendly access |
# MAGIC | **IDE integration** | SQL Developer VS Code extension | Databricks extension for VS Code |
# MAGIC | **Notebook-based development** | "sqlnb" notebooks in VS Code with extension, Oracle ML notebooks with OCI | Real-time cooperation with rich notebooks containing SQL, Python and other languages |
# MAGIC | **Extension possibilities** | conda in OCI ML notebooks | can install custom Python libraries in notebooks |
# MAGIC | **Git support** | clunky Git in SQL Developer, native support in VS Code | Git supported in the workspace and VS Code, too |
# MAGIC
# MAGIC **Key Benefit:** Your organization doesn't have to standardize on a single language or retrain teams. SQL analysts stay in SQL, Python engineers use Python, and everyone shares the same governed data and compute resources.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Price/Performance Leadership
# MAGIC <div style="border-left: 4px solid #ffc107; background: #fffde7; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">🎯</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #ff8f00; font-size: 1.1em;">Avoid the Idle Tax</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">With Databricks' smart scaling, you only pay for the capacity you need</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>
# MAGIC Databricks consistently delivers top-tier price/performance in independent benchmarks. This isn't about raw speed alone - it's about getting more value from every dollar of compute spend while reducing the operational burden on your teams.

# COMMAND ----------

# MAGIC %md
# MAGIC **What Drives Databricks Price/Performance:**
# MAGIC
# MAGIC | Capability | Business Impact |
# MAGIC |------------|-----------------|
# MAGIC | **Photon Engine** | Next-generation query engine delivers 2-8x faster performance on SQL and ETL workloads - same code, lower costs |
# MAGIC | **Liquid Clustering** | Automatic data organization eliminates manual table maintenance; queries find data faster without DBA intervention |
# MAGIC | **Deletion Vectors** | Efficient handling of updates and deletes without rewriting entire files - critical for GDPR/CCPA compliance workloads |
# MAGIC | **Predictive Optimization** | Databricks automatically optimizes your tables in the background - no scheduled maintenance jobs to manage |
# MAGIC | **Serverless Compute** | Instant startup, automatic scaling, zero infrastructure management, efficient incremental refresh for materialized views - pay only for what you use |
# MAGIC
# MAGIC **Comparison with Oracle:**
# MAGIC
# MAGIC | Aspect | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
# MAGIC |--------|-------------------|---------------|
# MAGIC | **Resource Sizing** | Often involves overprovisioning to handle peak month-end or seasonal loads, leading to wasted idle capacity | Serverless scaling means capacity matches demand exactly |
# MAGIC | **Idle costs** | High, licence costs money even when the analysts are asleep | Zero, compute shuts down when not used |
# MAGIC | **Financial Model** | Heavy focus on pre-paid licenses or provisioned OCCP/Exadata racks (CapEx-style commitment) | 100% consumption model where costs align directly with business activity |
# MAGIC | **Operational Overhead** | Requires DBAs for index management, patching, and tuning storage cells or RAC clusters | Engineering effort is spent on data products and AI, while the platform handles the infrastructure |
# MAGIC | **Scaling Velocity** | Scaling out often requires manual configuration or "adding nodes" to a cluster, which takes time | Serverless SQL warehouses start in seconds, allowing for a truly elastic response to user demand |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">ℹ️</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Migration Note</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Actual performance gains depend on workload characteristics. We recommend benchmarking your specific queries during assessment to quantify expected improvements and build a data-driven business case.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Building the Business Case
# MAGIC
# MAGIC <div style="border-left: 4px solid #ffc107; background: #fffde7; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">🎯</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #ff8f00; font-size: 1.1em;">Align Technical Value with Business Outcomes</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">A successful migration requires more than technical justification - it requires alignment across stakeholders who measure success differently. This section helps you frame the conversation for each audience and build a compelling, defensible business case.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ### Stakeholder Alignment
# MAGIC
# MAGIC Different stakeholders evaluate migration through different lenses. Tailor your message accordingly:
# MAGIC
# MAGIC | Stakeholder | What They Care About | How Databricks Addresses It |
# MAGIC |-------------|----------------------|----------------------------|
# MAGIC | **CFO / Finance** | TCO reduction, license cost predictability, OpEx vs CapEx, ROI timeline | Flexible DBU pricing, reduced tooling sprawl, serverless eliminates overprovisioning, open formats avoid exit fees |
# MAGIC | **CTO / Architect** | Technical capabilities, scalability, future-proofing, integration complexity | Open source foundation, lakehouse architecture, multi-cloud support, API-first design |
# MAGIC | **CDO / Data Leader** | Governance, compliance, data quality, lineage, regulatory readiness | Unity Catalog provides unified governance; automatic lineage; audit logging for SOX, GDPR, HIPAA |
# MAGIC | **CISO / Security** | Data sovereignty, access control, attack surface, incident response | Data stays in your cloud account; fine-grained ABAC; integration with your IAM and SIEM |
# MAGIC | **Data Engineers** | Developer experience, CI/CD, debugging, maintainability | Notebooks + IDE support, Git integration, Lakeflow Spark Declarative Pipelines, collaborative workflows |
# MAGIC | **Data Scientists** | ML capabilities, experiment tracking, model deployment, collaboration | MLflow, Feature Store, Model Serving, AutoML - all natively integrated |
# MAGIC | **Business Users** | Query performance, reliability, self-service access, time to insight | Photon acceleration, Databricks SQL, governed self-service with Unity Catalog |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Questions to Answer
# MAGIC
# MAGIC Before seeking approval, ensure you have clear, defensible answers to these questions:
# MAGIC
# MAGIC | Question | Why It Matters | How to Answer It |
# MAGIC |----------|----------------|------------------|
# MAGIC | **Why now?** | Establishes urgency and relevance | Contract renewal timing, scaling challenges, new AI/ML requirements, security incidents, or competitive pressure |
# MAGIC | **What's the cost of inaction?** | Reframes migration as risk mitigation, not just opportunity | Quantify: rising license costs, technical debt accumulation, missed business opportunities, compliance gaps |
# MAGIC | **What's the total cost of ownership?** | CFO's primary concern - needs apples-to-apples comparison | Include: compute, storage, egress, tooling, personnel, training, and opportunity costs |
# MAGIC | **What new capabilities do we gain?** | Justifies investment beyond cost parity | AI/ML integration, real-time streaming, unified governance, open formats - capabilities that enable new revenue or efficiency |
# MAGIC | **What are the risks?** | Demonstrates due diligence; builds confidence | Identify migration complexity, timeline, skill gaps, and business continuity - then present mitigation strategies |
# MAGIC | **How do we measure success?** | Creates accountability and tracks ROI | Define KPIs: cost per query, pipeline reliability, time to insight, developer productivity, compliance audit results |
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Building Your Business Case Document
# MAGIC
# MAGIC A compelling business case typically includes:
# MAGIC
# MAGIC | Section | Content |
# MAGIC |---------|---------|
# MAGIC | **Executive Summary** | One-page overview: problem, solution, expected outcomes, investment required |
# MAGIC | **Current State Assessment** | Pain points, costs, limitations, risks of current platform |
# MAGIC | **Future State Vision** | Target architecture, new capabilities enabled, alignment with business strategy |
# MAGIC | **Financial Analysis** | 3-year TCO comparison, ROI projections, sensitivity analysis |
# MAGIC | **Risk Assessment** | Technical, operational, and business risks with mitigation plans |
# MAGIC | **Implementation Roadmap** | Phased approach, milestones, resource requirements, timeline |
# MAGIC | **Success Metrics** | KPIs, measurement methodology, reporting cadence |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #009688; background: #e0f2f1; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">💡</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #00695c; font-size: 1.1em;">Next Step</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Use the frameworks in this module to conduct stakeholder interviews and gather the inputs needed for your business case. The subsequent modules will provide detailed guidance on assessment, planning, and execution.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary and Key Takeaways
# MAGIC This module builds the business case for migration by articulating strategic and technical drivers. The core argument: Databricks offers data sovereignty (your data in your cloud, in open formats), platform consolidation (one governed platform for ETL, BI, ML, and AI), and freedom from vendor lock-in through open source foundations. The Lakehouse architecture Databricks pioneered is now industry-standard, and Unity Catalog provides unified governance across data and AI assets.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Takeaways
# MAGIC
# MAGIC - **Data stays yours** - stored in your cloud account in open formats, not locked in proprietary vendor storage
# MAGIC - **Open source foundation** - Spark, Delta Lake, MLflow, and Unity Catalog mean portable skills and no metadata lock-in
# MAGIC - **One platform** - consolidates ETL, orchestration, BI, ML, and AI under single governance
# MAGIC - **Scalability** - easily scale storage and processing as requirements grow without CapEx
# MAGIC - **Build the business case by audience** - CFO wants TCO, CTO wants architecture, CISO wants sovereignty, CDO wants governance
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
