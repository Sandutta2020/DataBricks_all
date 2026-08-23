# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
# MAGIC     <div style="font-size: 14px; color: #666;">
# MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
# MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
# MAGIC         <span style="margin-left: 8px;">01 - Discover</span>
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
# MAGIC # Planning and Road-mapping
# MAGIC
# MAGIC With discovery complete, you now have the data needed to build a realistic migration plan. This lesson covers sequencing phases, defining ingestion strategies, classifying workloads into waves, and mapping security models to Unity Catalog.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lesson, you will be able to:
# MAGIC
# MAGIC - Select a migration strategy (AI/BI first or ETL first)
# MAGIC - Sequence migration phases and align them to success metrics
# MAGIC - Define ingestion strategy (batch, streaming, CDC) for each data source
# MAGIC - Classify workloads using T-shirt sizing for effort estimation
# MAGIC - Structure migration waves with dependencies and milestones
# MAGIC - Map Oracle roles and policies to Unity Catalog

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## 1. Selecting a Migration Strategy
# MAGIC
# MAGIC The first planning decision is choosing between an ETL-First or AI/BI-First approach. This choice shapes how you sequence work and when stakeholders see value.
# MAGIC <br/>
# MAGIC <br/>
# MAGIC <div class="mermaid">
# MAGIC flowchart LR
# MAGIC     A["What is your<br/>primary driver?"] --> B{"Cost<br/>reduction?"}
# MAGIC     B -->|Yes| C["<b>ETL-First</b><br/>Build pipelines, then AI/BI"]
# MAGIC     B -->|No| D{"Quick wins or<br/>AI capabilities?"}
# MAGIC     D -->|Yes| E["<b>AI/BI-First</b><br/>Federate data, unlock AI"]
# MAGIC     D -->|No| C
# MAGIC     style C fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
# MAGIC     style E fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
# MAGIC </div>
# MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

# COMMAND ----------

# MAGIC %md
# MAGIC | Strategy | Approach | Best For |
# MAGIC |----------|----------|----------|
# MAGIC | **ETL-First** | Build Bronze -> Silver -> Gold layers, then migrate AI/BI | Cost-driven migrations, greenfield Lakehouse designs, Data Mesh implementations |
# MAGIC | **AI/BI-First** | Federate existing data, unlock AI capabilities (Genie, Mosaic AI), then migrate ETL | Time-sensitive migrations, AI/ML priorities, demonstrating quick value, phased budget approval |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### ETL-First Phased Architecture
# MAGIC
# MAGIC <div class="mermaid">
# MAGIC %%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fff', 'primaryBorderColor': '#FF3621'}}}%%
# MAGIC flowchart LR
# MAGIC     subgraph ETL["<b>ETL-First Strategy</b>"]
# MAGIC         direction LR
# MAGIC         Source["Data<br/>Sources"] -->|Lakeflow Connect| BrzSlv["<b>Databricks</b><br/>Bronze -> Silver"]
# MAGIC         BrzSlv -->|"Phase 1"| Oracle["Oracle<br/><i>Gold/Serving</i>"]
# MAGIC         BrzSlv -->|"Phase 2"| DbxGld["<b>Databricks</b><br/><i>Gold/Serving</i>"]
# MAGIC         Oracle --> ExistingBI["Existing BI Tools<br/><i>Power BI, Tableau, Looker, etc</i>"]
# MAGIC         DbxGld --> ExistingBI
# MAGIC         DbxGld -->|"Phase 3"| DbxAIBI["Databricks AI/BI<br/><i>Dashboards, Genie, Mosaic AI</i>"]
# MAGIC     end
# MAGIC     style ETL fill:#fff,stroke:#FF3621,stroke-width:2px
# MAGIC     style Source fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
# MAGIC     style BrzSlv fill:#ffebee,stroke:#FF3621,stroke-width:2px
# MAGIC     style Oracle fill:#e3f2fd,stroke:#29B5E8,stroke-width:2px
# MAGIC     style DbxGld fill:#ffebee,stroke:#FF3621,stroke-width:2px
# MAGIC     style ExistingBI fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
# MAGIC     style DbxAIBI fill:#ffebee,stroke:#FF3621,stroke-width:2px
# MAGIC </div>
# MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

# COMMAND ----------

# MAGIC %md
# MAGIC | Phase | Focus | Outcome |
# MAGIC |-------|-------|---------|
# MAGIC | **Phase 1** | ETL migration to Databricks, Oracle serves Gold | Existing BI uninterrupted, cost savings on compute |
# MAGIC | **Phase 2** | Gold layer moves to Databricks | Full data platform consolidation |
# MAGIC | **Phase 3** | Adopt Databricks AI/BI | AI-assisted analytics, Genie natural language queries, Mosaic AI for ML/GenAI |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### AI/BI-First Phased Architecture
# MAGIC
# MAGIC The AI/BI-First approach uses Lakehouse Federation to provide immediate access to Oracle data from Databricks, enabling rapid deployment of AI/BI capabilities while ETL migration proceeds in parallel.
# MAGIC
# MAGIC <div class="mermaid">
# MAGIC %%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fff', 'primaryBorderColor': '#FF3621'}}}%%
# MAGIC flowchart LR
# MAGIC     subgraph AIBI["<b>AI/BI-First Strategy</b>"]
# MAGIC         direction LR
# MAGIC         Source["Data<br/>Sources"] --> Oracle["Oracle<br/><i>Existing Pipelines</i>"]
# MAGIC         Oracle -->|"Phase 1: Federation"| DbxFed["<b>Databricks</b><br/><i>Lakehouse Federation</i>"]
# MAGIC         DbxFed --> DbxAIBI["Databricks AI/BI<br/><i>Dashboards, Genie, Mosaic AI</i>"]
# MAGIC         Source -->|"Phase 2: Lakeflow Connect"| DbxETL["<b>Databricks</b><br/>Bronze -> Silver -> Gold"]
# MAGIC         DbxETL -->|"Phase 3"| DbxAIBI
# MAGIC         Oracle -.->|"Decommission"| Retired["Oracle Pipelines,<br/>Warehouses, Dashboards<br/><i>Retired</i>"]
# MAGIC     end
# MAGIC     style AIBI fill:#fff,stroke:#FF3621,stroke-width:2px
# MAGIC     style Source fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
# MAGIC     style Oracle fill:#e3f2fd,stroke:#29B5E8,stroke-width:2px
# MAGIC     style DbxFed fill:#ffebee,stroke:#FF3621,stroke-width:2px
# MAGIC     style DbxAIBI fill:#ffebee,stroke:#FF3621,stroke-width:2px
# MAGIC     style DbxETL fill:#ffebee,stroke:#FF3621,stroke-width:2px
# MAGIC     style Retired fill:#e0e0e0,stroke:#9e9e9e,stroke-width:1px,stroke-dasharray: 5 5
# MAGIC </div>
# MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

# COMMAND ----------

# MAGIC %md
# MAGIC | Phase | Focus | Outcome |
# MAGIC |-------|-------|---------|
# MAGIC | **Phase 1** | Federate Oracle data into Databricks via Lakehouse Federation | Immediate access to AI/BI capabilities without data movement |
# MAGIC | **Phase 2** | Migrate ETL pipelines to Databricks (parallel workstream) | Data lands natively in Lakehouse, reduces federation dependency |
# MAGIC | **Phase 3** | Cut over to Databricks-native data; decommission Oracle ETL pipelines, warehouses, and native dashboards | Full platform consolidation, Oracle compute and storage costs eliminated |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #e7f3fe; border-left: 4px solid #2196F3; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">
# MAGIC <strong>💡 Lakehouse Federation for BI-First</strong><br/>
# MAGIC Lakehouse Federation allows Databricks to query Oracle directly without moving data. Use this to accelerate BI modernization while ETL migration proceeds in parallel.
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Defining Ingestion Strategy
# MAGIC
# MAGIC For each data source identified in discovery, determine the appropriate ingestion pattern:
# MAGIC
# MAGIC | Pattern | Use When | Databricks Tool |
# MAGIC |---------|----------|-----------------|
# MAGIC | **Batch (Full Load)** | Small tables, reference data, infrequent updates | Lakehouse Federation, COPY INTO |
# MAGIC | **Batch (Incremental)** | Large tables | Lakehouse Federation, Auto Loader |
# MAGIC | **CDC (Change Data Capture)** | High-volume Oracle tables, real-time requirements | Lakeflow Spark Declarative Pipelines, GoldenGate, Debezium |
# MAGIC | **Streaming** | Event streams, IoT, log data | Structured Streaming, Lakeflow Spark Declarative Pipelines |
# MAGIC | **Federation** | BI-First approach, temporary access during migration | Lakehouse Federation |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Workload Classification (T-Shirt Sizing)
# MAGIC
# MAGIC Classify each workload by complexity to estimate effort and assign to appropriate waves. Use discovery data to score each dimension.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Complexity Scoring Matrix
# MAGIC
# MAGIC | Dimension | Small (1 pt) | Medium (2 pts) | Large (3 pts) | X-Large (4 pts) |
# MAGIC |-----------|--------------|----------------|---------------|-----------------|
# MAGIC | **Table Count** | < 10 | 10-50 | 50-200 | > 200 |
# MAGIC | **Data Volume** | < 10 GB | 10-100 GB | 100 GB - 1 TB | > 1 TB |
# MAGIC | **Dependencies** | None | 1-3 upstream | 4-10 upstream | > 10 or cross-instance |
# MAGIC | **Code Complexity** | Simple SQL | Materialized Views | PL/SQL Procedures | PL/SQL Packages & Triggers |
# MAGIC | **SLA Sensitivity** | None | Daily | Hourly | Real-time |
# MAGIC | **Consumers** | 1 team | 2-5 teams | Enterprise-wide | External/customers |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## 4. Wave Structure
# MAGIC
# MAGIC Organize workloads into waves based on complexity scores and dependencies. Each wave builds on patterns established in previous waves.
# MAGIC
# MAGIC <div id="wave-wbs-diagram"></div>
# MAGIC
# MAGIC <script>
# MAGIC (function() {
# MAGIC   const puml = `@startwbs
# MAGIC <style>
# MAGIC wbsDiagram {
# MAGIC   .foundation {
# MAGIC     BackgroundColor #e3f2fd
# MAGIC     LineColor #1976d2
# MAGIC   }
# MAGIC   .quickwins {
# MAGIC     BackgroundColor #e8f5e9
# MAGIC     LineColor #4caf50
# MAGIC   }
# MAGIC   .core {
# MAGIC     BackgroundColor #fff3e0
# MAGIC     LineColor #ff9800
# MAGIC   }
# MAGIC   .complex {
# MAGIC     BackgroundColor #fce4ec
# MAGIC     LineColor #e91e63
# MAGIC   }
# MAGIC   .cleanup {
# MAGIC     BackgroundColor #f3e5f5
# MAGIC     LineColor #9c27b0
# MAGIC   }
# MAGIC }
# MAGIC </style>
# MAGIC * Migration Waves
# MAGIC ** Wave 0: Foundation <<foundation>>
# MAGIC *** Workspace provisioning
# MAGIC *** Unity Catalog setup
# MAGIC *** Network & CI/CD
# MAGIC ** Wave 1: Quick Wins <<quickwins>>
# MAGIC *** Reference tables
# MAGIC *** Low-dependency pipelines
# MAGIC *** MVP use case
# MAGIC *** Establish patterns
# MAGIC ** Wave 2: Core Data <<core>>
# MAGIC *** Fact tables
# MAGIC *** Shared ETL pipelines
# MAGIC *** Primary BI reports
# MAGIC ** Wave 3: Complex Workloads <<complex>>
# MAGIC *** Stored procedures
# MAGIC *** Streams/CDC
# MAGIC *** PL/SQL Conversion
# MAGIC ** Wave 4: Cutover <<cleanup>>
# MAGIC *** Edge cases
# MAGIC *** Connection switchover
# MAGIC *** Decommission
# MAGIC
# MAGIC legend bottom right
# MAGIC   **Typical Wave Durations**
# MAGIC   |<#e3f2fd> Wave 0 | 2-4 wks |
# MAGIC   |<#e8f5e9> Wave 1 | 4-6 wks |
# MAGIC   |<#fff3e0> Wave 2 | 6-12 wks |
# MAGIC   |<#fce4ec> Wave 3 | 4-8 wks |
# MAGIC   |<#f3e5f5> Wave 4 | 2-4 wks |
# MAGIC endlegend
# MAGIC @endwbs`;
# MAGIC
# MAGIC   const encoded = Array.from(new TextEncoder().encode(puml))
# MAGIC     .map(b => b.toString(16).padStart(2, '0'))
# MAGIC     .join('');
# MAGIC
# MAGIC   const img = document.createElement('img');
# MAGIC   img.src = `https://www.plantuml.com/plantuml/svg/~h${encoded}`;
# MAGIC   img.alt = 'Migration Wave WBS';
# MAGIC   img.style.maxWidth = '100%';
# MAGIC   document.getElementById('wave-wbs-diagram').appendChild(img);
# MAGIC })();
# MAGIC </script>
# MAGIC <i>Actual durations depend on scope from discovery. Plan for 20-30% buffer for unknowns.</i>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #e7f3fe; border-left: 4px solid #2196F3; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">
# MAGIC <strong>🎯 Use Case Complexity Score Mapping</strong><br/>
# MAGIC Use the use-case complexity scores from the previous section to map migration activities to waves:<br/><br/>
# MAGIC <strong>6-10 points:</strong> Small - Wave 1 candidate<br/>
# MAGIC <strong>11-16 points:</strong> Medium - Wave 2 candidate<br/>
# MAGIC <strong>17-20 points:</strong> Large - Wave 3 candidate<br/>
# MAGIC <strong>21+ points:</strong> X-Large - Wave 3 with specialist support
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Sample Milestone Timeline
# MAGIC
# MAGIC <div class="mermaid">
# MAGIC gantt
# MAGIC     title Migration Milestones
# MAGIC     dateFormat  YYYY-MM-DD
# MAGIC     section Foundation
# MAGIC     Workspace Setup       :w0a, 2025-01-06, 2w
# MAGIC     Unity Catalog Config  :w0b, after w0a, 1w
# MAGIC     section Wave 1
# MAGIC     MVP Data Migration    :w1a, after w0b, 3w
# MAGIC     Pattern Documentation :w1b, after w1a, 1w
# MAGIC     section Wave 2
# MAGIC     Core ETL Migration    :w2a, after w1b, 6w
# MAGIC     BI Report Cutover     :w2b, after w2a, 2w
# MAGIC     section Wave 3
# MAGIC     Complex Workloads     :w3a, after w2b, 4w
# MAGIC     section Cutover
# MAGIC     Validation & Cleanup  :w4a, after w3a, 2w
# MAGIC </div>
# MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Security Mapping to Unity Catalog
# MAGIC
# MAGIC Map Oracle's role-based access control to Unity Catalog. Document exceptions requiring special handling.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Role and Policy Mapping
# MAGIC
# MAGIC | Oracle Construct | Unity Catalog Equivalent | Migration Notes |
# MAGIC |---------------------|-------------------------|-----------------|
# MAGIC | User | User / Service Principal | Sync via SCIM or Entra ID |
# MAGIC | Role | Group | Create matching groups in identity provider |
# MAGIC | Role hierarchy | Group nesting | Replicate inheritance structure |
# MAGIC | Public Synonym | Alias / View | Recreate as views in a 'common' schema |
# MAGIC | Private Synonym | Alias / View | Map to views within target schema |
# MAGIC | Table Grant | Table Grant | Direct mapping |
# MAGIC | Virtual Private DB (VPD) | Row Filter / Column Mask | Recreate logic as UC SQL expressions |
# MAGIC | DB Link | Foreign Catalog / Connection | Use Lakehouse Federation for cross-db access |
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">
# MAGIC <strong>⚠️ Document Security Exceptions</strong><br/>
# MAGIC Flag any patterns that don't map cleanly: service account permissions, cross-account shares, external functions, or compliance-specific controls. These require architecture review before migration.
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Defining Success Metrics
# MAGIC
# MAGIC Align each phase to measurable outcomes. Track these throughout migration:
# MAGIC
# MAGIC | Metric Category | Example Metrics |
# MAGIC |-----------------|-----------------|
# MAGIC | **Progress** | Tables migrated, PL/SQL modules converted, % complete by wave |
# MAGIC | **Quality** | Data reconciliation pass rate, test coverage, defect count |
# MAGIC | **Performance** | Query latency comparison (Oracle vs Photon), pipeline duration |
# MAGIC | **Cost** | Oracle license/maintenance savings, Databricks DBU consumption, TCO trend |
# MAGIC | **Adoption** | Active users on Databricks, BI reports switched, training completion |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary Checklist
# MAGIC
# MAGIC Before proceeding to the Design phase, confirm:
# MAGIC
# MAGIC ✅ Migration strategy selected (ETL-First or AI/BI-First)  
# MAGIC ✅ Ingestion pattern defined for each source  
# MAGIC ✅ All workloads scored and assigned to waves  
# MAGIC ✅ Wave structure approved by stakeholders  
# MAGIC ✅ Oracle roles mapped to Unity Catalog groups  
# MAGIC ✅ Security exceptions documented for architecture review  
# MAGIC ✅ Success metrics defined and tracking mechanism in place  
# MAGIC ✅ Milestone timeline reviewed with project sponsors  

# COMMAND ----------

# MAGIC %md
# MAGIC ## References
# MAGIC
# MAGIC - [Databricks Migration Strategy Blog](https://www.databricks.com/blog/databricks-migration-strategy-lessons-learned)
# MAGIC - [Lakehouse Federation Documentation](https://docs.databricks.com/en/query-federation/index.html)
# MAGIC - [Unity Catalog Privileges](https://docs.databricks.com/en/data-governance/unity-catalog/manage-privileges/index.html)
# MAGIC - [Lakeflow Connect](https://docs.databricks.com/en/ingestion/lakeflow-connect/index.html)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
