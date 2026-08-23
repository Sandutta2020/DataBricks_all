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
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img
-- MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
-- MAGIC     alt="Databricks Learning"
-- MAGIC   >
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Storage and Governance Design
-- MAGIC
-- MAGIC This lesson focuses on designing storage zones and establishing governance hierarchies for your migration. You will map Oracle storage constructs (Tablespaces, Directories) to Unity Catalog storage objects, define ownership models, and implement least-privilege access patterns.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this lesson, you will be able to:
-- MAGIC
-- MAGIC - Design storage zones (Bronze/Silver/Gold) for migration data flow
-- MAGIC - Map Oracle DIRECTORY objects to Unity Catalog external locations and volumes
-- MAGIC - Replace Oracle Tablespaces with Unity Catalog managed storage locations
-- MAGIC - Establish ownership conventions across catalogs and schemas

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 1. Storage Zone Architecture
-- MAGIC
-- MAGIC A well-designed storage architecture separates concerns across landing, staging, and serving zones. This pattern ensures data flows through governed checkpoints before reaching consumers.
-- MAGIC
-- MAGIC <div class="mermaid">
-- MAGIC flowchart LR
-- MAGIC     subgraph SOURCES["External Sources"]
-- MAGIC         ORA["<b>Oracle</b><br/>Data Pump / CSV exports"]
-- MAGIC         EXT["<b>Other Sources</b><br/>APIs, files, streams"]
-- MAGIC     end
-- MAGIC     subgraph ZONES["Storage Zones"]
-- MAGIC         direction TB
-- MAGIC         LAND["<b>Landing Zone</b><br/><i>Raw exports, untouched</i>"]
-- MAGIC         STAGE["<b>Staging Zone</b><br/><i>Validated, schema-applied</i>"]
-- MAGIC         MANAGED["<b>Managed Storage</b><br/><i>Unity Catalog tables</i>"]
-- MAGIC     end
-- MAGIC     subgraph UC["Unity Catalog"]
-- MAGIC         EL["External<br/>Locations"]
-- MAGIC         VOL["Volumes"]
-- MAGIC         TBL["Managed<br/>Tables"]
-- MAGIC     end
-- MAGIC     ORA --> LAND
-- MAGIC     EXT --> LAND
-- MAGIC     LAND --> STAGE
-- MAGIC     STAGE --> MANAGED
-- MAGIC     LAND -.-> EL
-- MAGIC     STAGE -.-> VOL
-- MAGIC     MANAGED -.-> TBL
-- MAGIC     style SOURCES fill:#fff,stroke:#F80102,stroke-width:2px
-- MAGIC     style ZONES fill:#fff,stroke:#607d8b,stroke-width:2px
-- MAGIC     style UC fill:#fff,stroke:#FF3621,stroke-width:2px
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "neutral" }); </script>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC | Zone | Purpose | Unity Catalog Object | Lifecycle |
-- MAGIC |------|---------|---------------------|-----------|
-- MAGIC | **Landing** | Receive raw exports from Oracle | External Location | Short-term (days); delete after ingestion |
-- MAGIC | **Staging** | Schema validation, type coercion | External Volume | Medium-term (weeks); archive or delete |
-- MAGIC | **Managed** | Production Delta tables | Managed Tables | Long-term; governed by retention policies |
-- MAGIC | **Archive** | Historical snapshots, compliance | External Volume | Long-term; cold storage tier |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 2. Mapping Oracle Storage to Unity Catalog
-- MAGIC
-- MAGIC Oracle constructs map to different Unity Catalog objects depending on whether they are for physical storage or file access.
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle Object</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks Equivalent</span> | Use Case |
-- MAGIC |----------------------|------------------------|----------|
-- MAGIC | **Tablespace** | Managed Storage Location | Defined at Catalog/Schema level in UC |
-- MAGIC | **DIRECTORY Object** | Volume / External Location | Governed file access for exports/imports |
-- MAGIC | **Data Pump File** | Parquet file in Volume | Standard format for high-speed ingestion |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3. External Location Design
-- MAGIC
-- MAGIC External locations define the cloud storage paths that Unity Catalog can access. For Oracle migrations, these typically point to landing zones where Data Pump or JDBC extractors land files.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ### Recommended External Location Structure
-- MAGIC
-- MAGIC | Location Name | Path Pattern | Purpose |
-- MAGIC |---------------|--------------|---------|
-- MAGIC | `oracle_landing` | `s3://bucket/migration/landing/` | Raw Oracle Data Pump / CSV exports |
-- MAGIC | `migration_staging` | `s3://bucket/migration/staging/` | Validated intermediate Parquet files |
-- MAGIC | `migration_archive` | `s3://bucket/migration/archive/` | Historical snapshots |
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ### Cloud Provider Paths
-- MAGIC
-- MAGIC | Cloud | Storage Type | Path Format | Example |
-- MAGIC |-------|--------------|-------------|---------|
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/logos:aws.svg" width="25" height="25" style="vertical-align: middle;"></span> | S3 | `s3://bucket/path/` | `s3://acme-datalake/oracle/landing/` |
-- MAGIC | <span><img src="https://devicon-website.vercel.app/api/azure/original.svg" width="20" height="20" style="vertical-align: middle;"></span> | ADLS Gen2 | `abfss://container@account.dfs.core.windows.net/path/` | `abfss://data@acmedl.dfs.core.windows.net/landing/` |
-- MAGIC | <span><img src="https://api.iconify.design/logos:google-cloud.svg" width="25" height="25" style="vertical-align: middle;"></span> | GCS | `gs://bucket/path/` | `gs://acme-datalake/oracle/landing/` |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 4. Volume Design for File Access
-- MAGIC
-- MAGIC Volumes provide governed file access within Unity Catalog. Use external volumes to access Oracle exports and load directly into managed Delta tables, or optionally stage in a managed volume for validation.
-- MAGIC
-- MAGIC <div class="mermaid">
-- MAGIC flowchart LR
-- MAGIC     subgraph SCHEMA["<b>CATALOG:</b> migration_dev<br/><b>SCHEMA:</b> hr_raw"]
-- MAGIC         EV["<b>oracle_exports</b><br/><i>External Volume</i><br/>-> oracle_landing"]
-- MAGIC         MV["<b>landing or staging</b><br/><i>Managed Volume</i><br/>UC-managed storage"]
-- MAGIC     end
-- MAGIC     ORT[("Oracle<br/>Source Tables")] --> |"export<br />and upload"| EV
-- MAGIC     EV --> |"Option A:<br/>Direct load"| TBL["Bronze<br/>Delta Tables"]
-- MAGIC     EV -.-> |"Option B:<br/>Replicate"| MV
-- MAGIC     MV -.-> |"Load after<br/>validation"| TBL
-- MAGIC     style ORT fill:#29B5E8,stroke:#1a8bb5,color:#fff
-- MAGIC     style SCHEMA fill:#fff,stroke:#FF3621,stroke-width:2px
-- MAGIC     style EV fill:#e3f2fd,stroke:#1976d2
-- MAGIC     style MV fill:#f3e5f5,stroke:#7b1fa2
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "neutral" }); </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Volume Types
-- MAGIC
-- MAGIC | Volume Type | Storage Location | Use Case | Lifecycle |
-- MAGIC |-------------|------------------|----------|-----------|
-- MAGIC | **Managed** | UC-managed storage for the schema | Databricks-only workloads: processing files, notebook outputs, checkpoints | UC manages lifecycle, files deleted when volume dropped |
-- MAGIC | **External** | Registered against existing cloud storage path | Landing zones from external systems, files accessed by both Databricks and external tools | Data remains in cloud storage when volume is dropped |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #43a047; background: #e8f5e9; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">💡</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #2e7d32; font-size: 1.1em;">When to Use Each</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Use <b>external volumes</b> when Oracle (or other external systems) writes directly to cloud storage. Use <b>managed volumes</b> for Databricks-only intermediate processing.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 5. Storage Access Patterns
-- MAGIC
-- MAGIC Apply the principle of least privilege when granting access to storage resources. Different personas need different levels of access.
-- MAGIC
-- MAGIC | Persona | External Location | Volume Access |
-- MAGIC |---------|-------------------|---------------|
-- MAGIC | **Migration Service** | `READ FILES`, `WRITE FILES` | `READ VOLUME`, `WRITE VOLUME` |
-- MAGIC | **Data Engineers** | `READ FILES`, `WRITE FILES` | `READ VOLUME`, `WRITE VOLUME` |
-- MAGIC | **Data Analysts** | None | `READ VOLUME` (gold layer only) |
-- MAGIC | **Pipeline Service Principal** | `READ FILES` | `READ VOLUME` |
-- MAGIC
-- MAGIC We will cover table-level privileges (<code>SELECT</code>, <code>MODIFY</code>) and schema-level grants are covered in <b>2.4 - Security and Access Design</b>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">Avoid Over-Privileging</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Do not grant <code>ALL PRIVILEGES</code> on external locations or storage credentials. This effectively gives cloud-level access to the underlying storage, bypassing Unity Catalog governance. Instead, grant specific privileges like <code>READ FILES</code> or <code>CREATE EXTERNAL TABLE</code> as needed.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 6. Ownership Conventions
-- MAGIC
-- MAGIC Establish clear ownership to ensure accountability and simplify access management. Unity Catalog supports ownership at every level of the hierarchy.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Ownership by Level
-- MAGIC
-- MAGIC | Level | Recommended Owner | Pattern | Responsibilities |
-- MAGIC |-------|-------------------|---------|------------------|
-- MAGIC | **Metastore** | Platform Team (group) | Centralized | Storage credentials, external locations, global policies |
-- MAGIC | **Catalog** | Domain Lead or Platform Team | Team-Based | Schema creation, cross-schema access policies |
-- MAGIC | **Schema** | Data Product Owner (group) | Team-Based | Table/view/volume creation within schema |
-- MAGIC | **Table/View** | Creator or Service Principal | Individual / Automated | Data quality, refresh schedules |
-- MAGIC | **Volume** | Data Product Owner (group) | Team-Based | File lifecycle, access grants |
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Migration Recommendation
-- MAGIC
-- MAGIC For migrations, use a **hybrid pattern**:
-- MAGIC - Platform team owns catalogs and storage infrastructure
-- MAGIC - Domain teams own schemas within their catalogs
-- MAGIC - Service principals own production pipeline outputs
-- MAGIC - Transfer ownership post-migration to appropriate teams

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 7. Governance Hierarchy
-- MAGIC
-- MAGIC Unity Catalog enforces an ownership hierarchy that establishes accountability at each level. The diagram below shows the recommended ownership model for migration assets, where platform teams own infrastructure and domain teams own their data products.
-- MAGIC
-- MAGIC <div class="mermaid">
-- MAGIC flowchart TB
-- MAGIC     META["<b>Metastore</b><br/><i>Owner: Platform Team</i>"]
-- MAGIC     CAT_DEV["<b>Catalog: migration_dev</b><br/><i>Owner: Platform Team</i>"]
-- MAGIC     CAT_PROD["<b>Catalog: migration_prod</b><br/><i>Owner: Platform Team</i>"]
-- MAGIC     SCH_RAW["<b>Schema: hr_raw</b><br/><i>Owner: Data Engineering</i>"]
-- MAGIC     SCH_GOLD["<b>Schema: hr_analytics</b><br/><i>Owner: Analytics Team</i>"]
-- MAGIC     TBL["Tables & Views"]
-- MAGIC     VOL["Volumes"]
-- MAGIC     META --> CAT_DEV
-- MAGIC     META --> CAT_PROD
-- MAGIC     CAT_DEV --> SCH_RAW
-- MAGIC     CAT_DEV --> SCH_GOLD
-- MAGIC     SCH_RAW --> TBL
-- MAGIC     SCH_RAW --> VOL
-- MAGIC     SCH_GOLD --> TBL
-- MAGIC     style META fill:#e8f5e9,stroke:#4caf50,color:#000
-- MAGIC     style CAT_DEV fill:#e3f2fd,stroke:#1976d2,color:#000
-- MAGIC     style CAT_PROD fill:#e3f2fd,stroke:#1976d2,color:#000
-- MAGIC     style SCH_RAW fill:#f3e5f5,stroke:#7b1fa2,color:#000
-- MAGIC     style SCH_GOLD fill:#f3e5f5,stroke:#7b1fa2,color:#000
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "neutral" }); </script>
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Privilege Inheritance</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Unity Catalog supports privilege inheritance: grants at the catalog level automatically flow down to schemas and objects within. This simplifies administration - granting <code>USE CATALOG</code> and <code>USE SCHEMA</code> at higher levels provides baseline access, while object-level grants handle exceptions.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 8. Mapping Oracle Governance to Unity Catalog
-- MAGIC
-- MAGIC Use this reference when translating Oracle governance patterns to Databricks.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Storage Mapping
-- MAGIC
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="20" height="20" style="vertical-align: middle;" /> Oracle</span> | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> |
-- MAGIC |-----------|------------|
-- MAGIC | `CREATE DIRECTORY` | `CREATE EXTERNAL LOCATION` + `CREATE VOLUME` |
-- MAGIC | `TABLESPACE` | Managed Storage Location (UC Metastore/Catalog) |
-- MAGIC | `GRANT READ ON DIRECTORY` | `GRANT READ VOLUME ON VOLUME` |
-- MAGIC | `Data Pump Export` | Volume file upload / landing |
-- MAGIC | `LIST DIRECTORY` | `LIST '/Volumes/catalog/schema/volume/'` |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## Summary
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Storage and Governance Checklist
-- MAGIC
-- MAGIC ✅ Storage zones defined (landing, staging, managed, archive)  
-- MAGIC ✅ External locations created for Oracle exports  
-- MAGIC ✅ Storage credentials configured with least-privilege IAM  
-- MAGIC ✅ Volumes created for governed file access  
-- MAGIC ✅ Storage privilege grants applied (external locations, volumes)  
-- MAGIC ✅ Ownership assigned to appropriate teams/service principals  
-- MAGIC ✅ Governance hierarchy documented  

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Key Decisions Made
-- MAGIC
-- MAGIC | Decision | Your Choice |
-- MAGIC |----------|-------------|
-- MAGIC | Zone structure | Landing / Staging / Managed / Archive |
-- MAGIC | Volume strategy | External for Persistence / Managed for Ephemeral |
-- MAGIC | Ownership model | Hybrid Platform/Domain Team |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## References
-- MAGIC
-- MAGIC - [External Locations](https://docs.databricks.com/en/connect/unity-catalog/external-locations.html)
-- MAGIC - [Volumes](https://docs.databricks.com/en/connect/unity-catalog/volumes.html)
-- MAGIC - [Unity Catalog Privileges](https://docs.databricks.com/en/data-governance/unity-catalog/manage-privileges/privileges.html)
-- MAGIC - [Lakebridge Documentation](https://docs.databricks.com/en/migration/lakebridge.html)

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
