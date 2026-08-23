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
-- MAGIC
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img
-- MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
-- MAGIC     alt="Databricks Learning"
-- MAGIC   >
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Platform Setup and Environment
-- MAGIC
-- MAGIC This lesson guides you through establishing the Databricks platform foundation for your Oracle migration. You will configure Unity Catalog, set up workspaces and compute resources (sizing for Exadata equivalence), and establish the credential and privilege model required for secure data access.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this lesson, you will be able to:
-- MAGIC
-- MAGIC - Enable Unity Catalog and create metastore, catalogs, and schemas
-- MAGIC - Configure workspaces and bind them to Unity Catalog
-- MAGIC - Set up serverless SQL Warehouses and compute clusters with proper sizing baselines
-- MAGIC - Create service credentials for cloud storage access (Oracle landing zones)
-- MAGIC - Introduce the privilege model for secure object management

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 1. Unity Catalog Foundation
-- MAGIC
-- MAGIC Unity Catalog provides a unified governance layer across all Databricks workspaces. Understanding its hierarchy is essential before provisioning resources.
-- MAGIC
-- MAGIC <div class="mermaid">
-- MAGIC flowchart LR
-- MAGIC     subgraph PLATFORM ["Databricks Account"]
-- MAGIC         ACCT["<b>Account</b>"] --> |has zero or many| WS["<b>Workspace</b>"]
-- MAGIC         ACCT --> |has zero or many| META["<b>Metastore</b><br/><i>Regional governance container</i>"]
-- MAGIC         WS -. assigned .-> META
-- MAGIC         META --> CAT["<b>Catalog</b><br/><i>Top-level namespace</i>"]
-- MAGIC         WS -. "optional catalog binding" .-> CAT
-- MAGIC         CAT --> SCH["<b>Schema</b>"]
-- MAGIC         SCH --> OBJ["Tables &bull; Views &bull; Volumes &bull; Functions &bull; Models &bull; more..."]
-- MAGIC     end
-- MAGIC     style PLATFORM fill:#fff,stroke:#FF3621,stroke-width:2px
-- MAGIC     style ACCT fill:#f3e5f5,stroke:#7b1fa2,color:#000
-- MAGIC     style WS fill:#f3e5f5,stroke:#7b1fa2,color:#000
-- MAGIC     style META fill:#f3e5f5,stroke:#7b1fa2,color:#000
-- MAGIC     style CAT fill:#f3e5f5,stroke:#7b1fa2,color:#000
-- MAGIC     style SCH fill:#f3e5f5,stroke:#7b1fa2,color:#000
-- MAGIC     style OBJ fill:#f3e5f5,stroke:#7b1fa2,color:#000
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "neutral" }); </script>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Metastore Configuration
-- MAGIC
-- MAGIC A metastore (an instance of Unity Catalog) is the top-level container for metadata. Each metastore is regional and can be shared accessed from multiple workspaces.
-- MAGIC
-- MAGIC | Configuration | Recommendation |
-- MAGIC |---------------|----------------|
-- MAGIC | **Region** | Same region as your primary workspaces and cloud storage |
-- MAGIC | **Managed Storage** | Dedicated cloud storage bucket/container for managed tables |
-- MAGIC | **Owner** | Account admin or platform team group |
-- MAGIC | **Workspaces** | Assign all workspaces that need shared governance |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 2. Catalog and Schema Structure
-- MAGIC
-- MAGIC Design your catalog structure to align with your migration strategy. Common patterns include mapping Oracle container databases (CDB) or pluggable databases (PDB) to catalogs.
-- MAGIC
-- MAGIC
-- MAGIC | Pattern | Structure | Best For |
-- MAGIC |---------|-----------|----------|
-- MAGIC | **Environment-based** | `dev`, `staging`, `prod` catalogs | Clear separation of development stages |
-- MAGIC | **Domain-based** | `sales`, `finance`, `marketing` catalogs | Business unit ownership |
-- MAGIC | **Hybrid** | `prod_sales`, `prod_finance`, `dev_sales` | Large enterprises with both needs |
-- MAGIC
-- MAGIC
-- MAGIC Recall that Oracle databases map to Databricks catalogs; schemas map directly to schemas. The namespace pattern changes from `OWNER.OBJECT` or `DB.SCHEMA.OBJECT` to `catalog.schema.object`.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3. Workspace Configuration
-- MAGIC
-- MAGIC Workspaces provide isolation for compute, code, pipelines, and jobs. Each workspace attaches to the metastore to access Unity Catalog objects. Workspace compute can be provisioned as **Classic** or **Serverless**.
-- MAGIC
-- MAGIC | Compute Type | Description | Best For | Notes |
-- MAGIC |--------------|-------------|----------|---------------------|
-- MAGIC | **All-Purpose Clusters** | Interactive clusters for development and exploration | Notebook development, ad-hoc analysis | Recommendation: used shared clusters for teams |
-- MAGIC | **Job Clusters** | Ephemeral clusters created for scheduled workloads | All kinds of scheduled jobs | Created at job start, terminated on completion, cost-efficient |
-- MAGIC | **SQL Warehouses** | Optimized compute for BI queries and SQL analytics | Dashboards, reporting, ad-hoc SQL | T-shirt sizing, auto-stopping, query queuing |
-- MAGIC | **Serverless Compute** | Fully managed compute with instant scaling | All workload types where available | No cluster management, startup in a few seconds, pay-per-use |
-- MAGIC | **GPU Clusters** | Clusters with GPU instances for ML workloads | Deep learning, LLM fine-tuning | Supports NVIDIA GPUs with the ML runtime |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #4caf50; background: #e8f5e9; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">✅</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #2e7d32; font-size: 1.1em;">Recommendation: Serverless Compute</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Encourage customers to adopt Serverless compute where available. Key benefits include:</p>
-- MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li><b>Better price-performance</b>: Optimized infrastructure with instant scaling</li>
-- MAGIC                 <li><b>Lower TCO</b>: No cluster management, automatic start/stop, pay only for usage</li>
-- MAGIC                 <li><b>Advanced features</b>: Incremental refresh for Materialized Views, Predictive I/O</li>
-- MAGIC                 <li><b>Faster startup</b>: Sub-second warm start vs minutes for classic clusters</li>
-- MAGIC             </ul>
-- MAGIC             <p style="margin: 12px 0 0 0; color: #333;"><b>Note:</b> Review the <a href="https://docs.databricks.com/en/compute/serverless.html">Serverless compute documentation</a> with your customer to ensure compatibility with their requirements, the customer may require Classic Compute if they have custom library requirements, specific cloud region availability, init script constraints, etc.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Compute Resource Selection
-- MAGIC
-- MAGIC Oracle and Databricks (Spark) have fundamentally different architectures and operating models. Because of this, it is not possible to recommend standard one-to-one replacements (for example, "X executors" or "on Large warehouse" to replace an Exadata instance with Y cores).
-- MAGIC
-- MAGIC Instead, a practical approach is:
-- MAGIC
-- MAGIC - Profile the Oracle workloads first (top queries, concurrency,  SLAs, CPU/IO usage).
-- MAGIC - Exploit Databricks' separation of storage and compute: use different compute types, sizes and autoscaling settings for different workload classes (ad-hoc, BI, ETL, apps).
-- MAGIC - Implement the logic on Databricks (SQL, Spark, Lakeflow) and run it on an initial compute with autoscaling enabled.
-- MAGIC   - If the job/query meets the SLA with headroom, shrink the max workers or node size.
-- MAGIC   - If it misses the SLA and is CPU-bound, increase the number of workers (scale horizontally) first, then use larger node types if needed.
-- MAGIC
-- MAGIC Typical starting points are shown in the table (to be validated with benchmarks).
-- MAGIC
-- MAGIC | Workload | <span style="white-space: nowrap;"><img src="https://cdn.simpleicons.org/databricks/FF3621" width="20" height="20" style="vertical-align: middle;"> Databricks</span> | Notes |
-- MAGIC |-----------|------------|----------|
-- MAGIC | Ad-hoc SQL | SQL Warehouse (2X-Small / X-Small / Small) | autoscaling |
-- MAGIC | Dashboards / scheduled BI | SQL Warehouse (Small) | Most common starting point |
-- MAGIC | Large scheduled ETL job | Serverless job cluster, or 16-32 vCPUs (~8 cores per worker), autoscale to 4-8 workers | Enable Photon |
-- MAGIC | High-concurrency analytics (Exadata X8/X9) | SQL Warehouse (Medium / Large) | Autoscaling for concurrency |
-- MAGIC | APEX App | Databricks Apps | Web-based data applications, serverless hosting |
-- MAGIC
-- MAGIC **A note on Exadata:** Exadata is an engineered Oracle hardware platform, not a distinct logical database type. In practice, Exadata workloads tend to be more intensive and higher-concurrency, so they usually require larger or more highly autoscaled SQL warehouses and ETL clusters than non-Exadata Oracle installations, but final sizing should always be based on workload profiling and benchmarking.

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #607d8b; background: #eceff1; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚙️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #37474f; font-size: 1.1em;">Monitoring SQL Warehouses</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Unlike Oracle's <code>V$INSTANCE</code> or <code>GV$INSTANCE</code> views, to inspect SQL warehouses in Databricks, use the Databricks UI (<strong>SQL -> SQL Warehouses</strong>), the <a href="https://docs.databricks.com/api/workspace/warehouses" target="_blank">REST API</a>, the <a href="https://docs.databricks.com/en/dev-tools/sdk-python.html" target="_blank">Python SDK</a>, or the <a href="https://docs.databricks.com/aws/en/dev-tools/cli/" target="_blank">Databricks CLI</a>.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 4. Storage Credentials and External Locations
-- MAGIC
-- MAGIC To access data in cloud storage (e.g. staging areas for Oracle exports), Unity Catalog requires storage credentials and external locations.
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Credential Hierarchy</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;"><b>Storage Credential</b> -> Cloud IAM role/service principal that can access storage<br/>
-- MAGIC             <b>External Location</b> -> Specific path within cloud storage<br/>
-- MAGIC             <b>Volume</b> -> Unity Catalog object pointing to an external location for file access</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Cloud Provider Setup
-- MAGIC
-- MAGIC | Cloud | Credential Type | Key Configuration |
-- MAGIC |-------|-----------------|-------------------|
-- MAGIC | <span style="white-space: nowrap;"><img src="https://api.iconify.design/logos:aws.svg" width="25" height="25" style="vertical-align: middle;"></span> | IAM Role | Create IAM role with S3 access, establish trust relationship with Databricks |
-- MAGIC | <span><img src="https://devicon-website.vercel.app/api/azure/original.svg" width="20" height="20" style="vertical-align: middle;"></span> | Service Principal | Grant Storage Blob Data Contributor on container |
-- MAGIC | <span><img src="https://api.iconify.design/logos:google-cloud.svg" width="25" height="25" style="vertical-align: middle;"></span> | Service Account | Grant Storage Object Admin on bucket |
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ### Required Permissions for Migration
-- MAGIC
-- MAGIC | Permission | Purpose |
-- MAGIC |------------|---------|
-- MAGIC | Read | Access Oracle Data Pump or CSV exports in staging |
-- MAGIC | Write | Create Delta tables on storage managed by Unity Catalog |
-- MAGIC | List | Discover files for Auto Loader |
-- MAGIC | Delete | Clean up temporary migration artifacts |

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 5. Naming Conventions and Standards
-- MAGIC
-- MAGIC Consistent naming conventions simplify management and reduce errors during migration. Establish these standards early and document them.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Recommended Conventions
-- MAGIC
-- MAGIC | Object Type | Pattern | Example |
-- MAGIC |-------------|---------|---------|
-- MAGIC | **Catalog** | `{env}` or `{domain}` | `prod`, `sales` |
-- MAGIC | **Schema** | `{source}_{layer}` or `{domain}_{layer}` | `oracle_raw`, `orders_gold` |
-- MAGIC | **Table** | `{entity}` or `{entity}_{suffix}` | `customers`, `orders_daily` |
-- MAGIC | **Volume** | `{purpose}` | `exports`, `landing`, `archive` |
-- MAGIC | **Storage Credential** | `{cloud}_{purpose}_credential` | `aws_migration_credential` |
-- MAGIC | **External Location** | `{purpose}_{zone}` | `oracle_staging`, `raw_landing` |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 6. Privilege Model
-- MAGIC
-- MAGIC Unity Catalog uses a hierarchical privilege model. Grants at higher levels cascade down to child objects, simplifying access management compared to Oracle's explicit object-level grants.
-- MAGIC
-- MAGIC <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
-- MAGIC     <thead>
-- MAGIC         <tr style="background: #f5f5f5;">
-- MAGIC             <th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Level</th>
-- MAGIC             <th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Privileges</th>
-- MAGIC             <th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Inheritance Behavior</th>
-- MAGIC         </tr>
-- MAGIC     </thead>
-- MAGIC     <tbody>
-- MAGIC         <tr>
-- MAGIC             <td rowspan="3" style="border: 1px solid #ddd; padding: 12px; vertical-align: top;"><b>Catalog</b></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;"><code>USE CATALOG</code></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;">Required to access any object within the catalog (similar to Oracle CONNECT)</td>
-- MAGIC         </tr>
-- MAGIC         <tr>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;"><code>CREATE SCHEMA</code></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;">Allows creating schemas in the catalog</td>
-- MAGIC         </tr>
-- MAGIC         <tr>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;"><code>SELECT</code>, <code>MODIFY</code></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;">Grants apply to <b>all</b> objects in the catalog</td>
-- MAGIC         </tr>
-- MAGIC         <tr>
-- MAGIC             <td rowspan="2" style="border: 1px solid #ddd; padding: 12px; vertical-align: top; background: #fafafa;"><b>Schema</b></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px; background: #fafafa;"><code>USE SCHEMA</code></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px; background: #fafafa;">Required to access objects in the schema</td>
-- MAGIC         </tr>
-- MAGIC         <tr>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px; background: #fafafa;"><code>SELECT</code>, <code>MODIFY</code></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px; background: #fafafa;">Grants apply to <b>all</b> tables/views within the schema</td>
-- MAGIC         </tr>
-- MAGIC                 <tr>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;"><b>Table/View</b></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;"><code>SELECT</code>, <code>MODIFY</code></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;">Applies to the specific object only</td>
-- MAGIC         </tr>
-- MAGIC         <tr>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px; background: #fafafa;"><b>Volume</b></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px; background: #fafafa;"><code>READ VOLUME</code>, <code>WRITE VOLUME</code></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px; background: #fafafa;">Applies to the specific volume only</td>
-- MAGIC         </tr>
-- MAGIC         <tr>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;"><b>Function</b></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;"><code>EXECUTE</code></td>
-- MAGIC             <td style="border: 1px solid #ddd; padding: 12px;">Applies to the specific function only</td>
-- MAGIC         </tr>
-- MAGIC     </tbody>
-- MAGIC </table>
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Detailed Coverage in 2.4</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Privilege implementation, Oracle-to-Databricks role mapping, RBAC configuration, and audit frameworks are covered in <b>2.4 - Security and Access Design</b>.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 7. Infrastructure as Code
-- MAGIC
-- MAGIC For repeatable deployments, use Declarative Automation Bundles (DABs) to manage workspace resources belonging to a project and CLI or IaC tools for account-level configuration.
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #7b1fa2; background: #f3e5f5; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">📝</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #4a148c; font-size: 1.1em;">Automation Approach</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">
-- MAGIC             <b>Declarative Automation Bundles</b>: Jobs, pipelines, notebooks, clusters<br/>
-- MAGIC             <b>Databricks CLI</b>: Account operations, metastore, user/group sync<br/>
-- MAGIC             <b>Terraform</b>: Full platform lifecycle management
-- MAGIC             </p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC | Resource | Tool | Example |
-- MAGIC |----------|------|---------|
-- MAGIC | Jobs and Pipelines | Declarative Automation Bundles | `databricks bundle deploy` |
-- MAGIC | Catalogs and Schemas | SQL or CLI | `databricks catalogs create` |
-- MAGIC | Storage Credentials | CLI | `databricks storage-credentials create` |
-- MAGIC | Cloud Infrastructure | Cloud IaC | CloudFormation, Terraform |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Example: databricks.yml for Migration Project</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="yaml">
-- MAGIC bundle:
-- MAGIC   name: oracle-migration
-- MAGIC
-- MAGIC workspace:
-- MAGIC   path: /Workspace/Shared/oracle-migration
-- MAGIC
-- MAGIC resources:
-- MAGIC   jobs:
-- MAGIC     migration_ingestion:
-- MAGIC       name: "Migration - Bronze Ingestion"
-- MAGIC       tasks:
-- MAGIC         - task_key: ingest_employees
-- MAGIC           notebook_task:
-- MAGIC             notebook_path: ./notebooks/ingest_employees
-- MAGIC           new_cluster:
-- MAGIC             spark_version: 15.4.x-scala2.12
-- MAGIC             node_type_id: m5.xlarge
-- MAGIC             num_workers: 2
-- MAGIC
-- MAGIC   pipelines:
-- MAGIC     bronze_pipeline:
-- MAGIC       name: "Migration - Lakeflow Pipelines"
-- MAGIC       target: migration_dev.oracle_hr
-- MAGIC       configuration:
-- MAGIC         source_path: "/Volumes/migration_dev/oracle_hr/oracle_exports"
-- MAGIC
-- MAGIC targets:
-- MAGIC   dev:
-- MAGIC     workspace:
-- MAGIC       host: https://your-dev-workspace.cloud.databricks.com
-- MAGIC   prod:
-- MAGIC     workspace:
-- MAGIC       host: https://your-prod-workspace.cloud.databricks.com
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
-- MAGIC
-- MAGIC <script>
-- MAGIC (function() {
-- MAGIC     function processCodeBlocks() {
-- MAGIC         document.querySelectorAll('.code-block').forEach(function(block) {
-- MAGIC             if (block.getAttribute('data-processed')) return;
-- MAGIC             block.setAttribute('data-processed', 'true');
-- MAGIC             var lang = block.getAttribute('data-language') || 'sql';
-- MAGIC             var code = block.textContent.trim();
-- MAGIC             var id = 'code-' + Math.random().toString(36).substr(2, 9);
-- MAGIC             block.innerHTML = 
-- MAGIC                 '<div style="position:relative;margin:16px 0;">' +
-- MAGIC                     '<button class="copy-btn" style="position:absolute;top:8px;right:8px;padding:4px 12px;font-size:12px;background:#ddd;color:#333;border:1px solid #ccc;border-radius:4px;cursor:pointer;z-index:10;">Copy</button>' +
-- MAGIC                     '<pre style="background:#f8f8f8;border-radius:8px;padding:16px;padding-top:40px;overflow-x:auto;margin:0;border:1px solid #e0e0e0;"><code id="' + id + '" class="language-' + lang + '" style="font-family:Consolas,Monaco,monospace;font-size:14px;"></code></pre>' +
-- MAGIC                 '</div>';
-- MAGIC             var codeEl = document.getElementById(id);
-- MAGIC             codeEl.textContent = code;
-- MAGIC             Prism.highlightElement(codeEl);
-- MAGIC             block.querySelector('.copy-btn').onclick = function() {
-- MAGIC                 var t = document.createElement('textarea');
-- MAGIC                 t.value = code;
-- MAGIC                 document.body.appendChild(t);
-- MAGIC                 t.select();
-- MAGIC                 document.execCommand('copy');
-- MAGIC                 document.body.removeChild(t);
-- MAGIC                 this.textContent = '✓ Copied!';
-- MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
-- MAGIC             };
-- MAGIC         });
-- MAGIC     }
-- MAGIC     processCodeBlocks();
-- MAGIC     document.querySelectorAll('details').forEach(function(details) {
-- MAGIC         details.addEventListener('toggle', processCodeBlocks);
-- MAGIC     });
-- MAGIC })();
-- MAGIC </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Summary

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Platform Setup Checklist
-- MAGIC
-- MAGIC ✅ Metastore created and configured with managed storage (Exadata-equivalent sizing)  
-- MAGIC ✅ Workspaces assigned to metastore  
-- MAGIC ✅ Catalogs created for migration environments (dev, prod)  
-- MAGIC ✅ Schemas created following medallion architecture  
-- MAGIC ✅ Storage credentials configured for cloud access  
-- MAGIC ✅ External locations defined for Oracle export landing zones  
-- MAGIC ✅ Volumes created for file-based data access  
-- MAGIC ✅ Privilege model established with appropriate grants  
-- MAGIC ✅ Naming conventions documented and applied  
-- MAGIC ✅ Declarative Automation Bundles prepared for deployment  
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Key Decisions Made
-- MAGIC
-- MAGIC | Decision | Your Choice |
-- MAGIC |----------|-------------|
-- MAGIC | Catalog structure | CDB/PDB-based / Environment-based |
-- MAGIC | Schema naming | Mirror Oracle / Redesign |
-- MAGIC | Compute strategy | Serverless SQL / Job clusters / Mixed |
-- MAGIC | IaC approach | DABs / Terraform |
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ## References
-- MAGIC
-- MAGIC - <a href="https://docs.databricks.com/en/data-governance/unity-catalog/get-started.html" target="_blank">Unity Catalog Setup Guide</a>
-- MAGIC - <a href="https://docs.databricks.com/en/connect/unity-catalog/storage-credentials.html" target="_blank">Storage Credentials</a>
-- MAGIC - <a href="https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior" target="_blank">SQL warehouse sizing, scaling, and queueing behavior</a>
-- MAGIC - <a href="https://docs.databricks.com/en/dev-tools/bundles/index.html" target="_blank">Declarative Automation Bundles</a>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
