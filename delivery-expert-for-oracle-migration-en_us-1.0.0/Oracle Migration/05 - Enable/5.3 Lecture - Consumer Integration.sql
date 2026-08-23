-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">05 - Enable</span>
-- MAGIC     </div>
-- MAGIC     <div style="display: flex; align-items: center; gap: 8px;">
-- MAGIC         <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="24" height="24" />
-- MAGIC         <span style="color: #999; font-size: 16px;">-></span>
-- MAGIC         <img src="https://cdn.simpleicons.org/databricks/FF3621" width="24" height="24"/>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img
-- MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
-- MAGIC     alt="Databricks Learning"
-- MAGIC   >
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Consumer Integration

-- COMMAND ----------

-- MAGIC %md
-- MAGIC This lesson covers enabling business users to consume data and insights from Databricks. You will connect BI tools (Tableau and Power BI), enable self-service analytics through AI/BI Dashboards and Genie Spaces, and plan for advanced AI/ML initiatives that unlock the strategic value of your migration.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this lesson, you will be able to:
-- MAGIC
-- MAGIC - Describe the post-cutover enablement roadmap from BI consumers through advanced AI/ML
-- MAGIC - Connect Tableau and Power BI to Databricks SQL Warehouses using Partner Connect or Delta Sharing
-- MAGIC - Enable Databricks One and Consumer Access for business user self-service
-- MAGIC - Create and share AI/BI Dashboards with interactive filters
-- MAGIC - Configure Genie Spaces for natural language data exploration
-- MAGIC - Validate dashboard performance against SLA requirements
-- MAGIC - Identify key Databricks AI/ML capabilities (MLflow, Model Serving, Vector Search) for future initiatives

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 1. Post-Cutover Enablement Roadmap
-- MAGIC
-- MAGIC After initial cutover, systematically expand the consumer base and build toward advanced AI/ML capabilities. This roadmap prioritizes quick wins with BI consumers while laying the foundation for strategic AI initiatives where Databricks delivers significant advantages over Oracle.
-- MAGIC
-- MAGIC <div class="mermaid">
-- MAGIC gantt
-- MAGIC     title Post-Cutover Enablement Timeline
-- MAGIC     dateFormat  YYYY-MM-DD
-- MAGIC     section BI Enablement
-- MAGIC     Phase 1 - BI Functional Parity       :p1, 2025-01-06, 1w
-- MAGIC     Phase 2 - Performance Validation     :p2, after p1, 2w
-- MAGIC     Phase 3 - Self-Service Enablement    :p3, after p2, 2w
-- MAGIC     section ML Foundation
-- MAGIC     Phase 4 - ML Infrastructure          :p4, after p3, 4w
-- MAGIC     Phase 5 - Model Productionization    :p5, after p4, 4w
-- MAGIC     section GenAI
-- MAGIC     Phase 6 - GenAI and RAG              :p6, after p5, 8w
-- MAGIC     Phase 7 - Advanced AI                :p7, after p6, 8w
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC | Phase | Timeline | Focus | Key Activities | Success Criteria |
-- MAGIC |-------|----------|-------|----------------|------------------|
-- MAGIC | **Phase 1** | Cutover | BI Functional Parity | Critical dashboards, core reports migrated | All reports render correctly |
-- MAGIC | **Phase 2** | Week 1-2 | Performance Validation | Secondary BI tools, ad-hoc analysts onboarded; query tuning | Query latency within SLA |
-- MAGIC | **Phase 3** | Week 3-4 | Self-Service Enablement | AI/BI Dashboards, Genie Spaces deployed; Consumer Access configured | Users creating/sharing dashboards |
-- MAGIC | **Phase 4** | Month 2-3 | ML Infrastructure | MLflow tracking, Feature Store setup; model registry configuration | Standardized experimentation pipeline |
-- MAGIC | **Phase 5** | Month 3-4 | Model Productionization | Model Serving endpoints, monitoring dashboards | Real-time predictions at scale |
-- MAGIC | **Phase 6** | Month 4-6 | GenAI/RAG | Vector Search indexes, Agent Framework; document Q&A applications | Intelligent copilots in production |
-- MAGIC | **Phase 7** | Month 6+ | Advanced AI | Fine-tuning foundation models, compound AI systems | Domain-specific AI applications |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #9c27b0; background: #f3e5f5; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">🚀</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #6a1b9a; font-size: 1.1em;">Strategic Value of AI/ML on Databricks</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Phases 1-3 deliver immediate value by enabling BI consumers. Phases 4-7 unlock the strategic advantages of Databricks over Oracle-unified governance across data and models, native MLflow integration, auto-scaling model serving, and a complete GenAI stack. Your migrated data is already positioned for these advanced use cases.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 2. BI Integration Architecture
-- MAGIC
-- MAGIC <br/>
-- MAGIC <div class="mermaid">
-- MAGIC flowchart LR
-- MAGIC     subgraph Consumers
-- MAGIC         U["👤 Business Users"]
-- MAGIC     end
-- MAGIC     subgraph BI["BI Tools"]
-- MAGIC         TB["Tableau / Power BI"]
-- MAGIC         DC["Databricks Connector<br/>(ODBC Driver)"]
-- MAGIC     end
-- MAGIC     SQLw[("SQL Warehouse")]
-- MAGIC     UC[("Unity Catalog")]
-- MAGIC     U --> TB
-- MAGIC     TB --> DC
-- MAGIC     DC -->|"ODBC / JDBC"| SQLw
-- MAGIC     SQLw --> UC
-- MAGIC     TB -.->|"Delta Sharing<br/>(open protocol)"| UC
-- MAGIC     style Consumers fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
-- MAGIC     style BI fill:#fff3e0,stroke:#ff9800,stroke-width:2px
-- MAGIC     style SQLw fill:#fce4ec,stroke:#FF3621,stroke-width:2px
-- MAGIC     style UC fill:#fce4ec,stroke:#FF3621,stroke-width:2px
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Supported Connection Methods for Common BI Tools**
-- MAGIC
-- MAGIC | BI Tool | Connection Method | Underlying Protocol | Authentication | Notes |
-- MAGIC |---------|-------------------|---------------------|----------------|-------|
-- MAGIC | **Tableau** | Databricks Connector (native) | ODBC | OAuth (recommended), PAT, Service Principal | Requires manual ODBC driver install for Desktop <sup>*</sup> |
-- MAGIC | **Power BI** | Databricks / Azure Databricks Connector (native) | ODBC (pre-installed), ADBC (preview) | OAuth (recommended), PAT, Service Principal, Entra ID | Driver pre-installed in recent Desktop versions <sup>*</sup> |
-- MAGIC | **Both** | Delta Sharing | Open protocol | Credential file | No direct SQL Warehouse connectivity required; native connectors in both tools |
-- MAGIC
-- MAGIC <sup>*</sup> <i>Connection files can be generated directly from the SQL Warehouse **Connection details** tab in the Databricks UI.</i>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Configuring Connection Details through the User Interface**  
-- MAGIC
-- MAGIC The **Connection details** tab on any SQL Warehouse provides everything you need to configure BI tool connectivity. Click the tool icon (Tableau, Power BI, etc.) to generate a pre-configured connection file, or copy the **Server hostname** and **HTTP path** values directly into your tool's connection dialog.
-- MAGIC
-- MAGIC <br/>
-- MAGIC <br/>
-- MAGIC
-- MAGIC <img src="../assets/images/connect-bi-tools.png" alt="Connecting BI Tools" />
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #009688; background: #e0f2f1; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">💡</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #00695c; font-size: 1.1em;">Delta Sharing for BI Tools</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Delta Sharing enables secure data sharing without requiring BI tools to connect directly to your SQL Warehouse. This is useful for sharing data with external partners or when direct connectivity isn't feasible. Both Tableau and Power BI have native Delta Sharing connectors.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3. Dashboard SLA Validation
-- MAGIC
-- MAGIC After connecting BI tools, validate that dashboard refresh times meet your defined SLAs. Compare against Oracle baseline performance.
-- MAGIC
-- MAGIC | SLA Tier | Target Latency | Use Case | Example Dashboards |
-- MAGIC |----------|----------------|----------|-------------------|
-- MAGIC | **Tier 1** | < 5 seconds | Executive dashboards, real-time ops | CEO summary, live sales |
-- MAGIC | **Tier 2** | < 30 seconds | Standard business reports | Weekly sales, inventory |
-- MAGIC | **Tier 3** | < 2 minutes | Complex analytics | Customer segmentation, forecasts |
-- MAGIC | **Tier 4** | < 10 minutes | Heavy aggregations | Historical trend analysis |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Extracting Oracle Query Baselines
-- MAGIC
-- MAGIC Compare Databricks query performance against your Oracle historical baselines.
-- MAGIC
-- MAGIC <details>
-- MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 Oracle: Extract query performance baselines (run in Oracle, requires Diagnostics Pack)</summary>
-- MAGIC
-- MAGIC <div class="code-block" data-language="sql">
-- MAGIC -- Top queries by elapsed time - identify report/BI workloads (AWR)
-- MAGIC SELECT
-- MAGIC     s.parsing_schema_name AS schema_name,
-- MAGIC     NVL(s.module, 'unknown') AS application_module,
-- MAGIC     NVL(s.action, 'unknown') AS action,
-- MAGIC     s.sql_id,
-- MAGIC     s.executions_delta AS executions,
-- MAGIC     ROUND(s.elapsed_time_delta / GREATEST(s.executions_delta, 1) / 1e6, 2) AS avg_elapsed_sec,
-- MAGIC     ROUND(s.cpu_time_delta / GREATEST(s.executions_delta, 1) / 1e6, 2) AS avg_cpu_sec,
-- MAGIC     ROUND(s.disk_reads_delta / GREATEST(s.executions_delta, 1), 0) AS avg_disk_reads,
-- MAGIC     ROUND(s.buffer_gets_delta / GREATEST(s.executions_delta, 1), 0) AS avg_buffer_gets
-- MAGIC FROM dba_hist_sqlstat s
-- MAGIC JOIN dba_hist_snapshot sn ON sn.snap_id = s.snap_id AND sn.dbid = s.dbid
-- MAGIC WHERE sn.begin_interval_time >= SYSDATE - 30
-- MAGIC   AND s.executions_delta > 0
-- MAGIC   AND s.parsing_schema_name NOT IN ('SYS','SYSTEM','DBSNMP')
-- MAGIC ORDER BY s.elapsed_time_delta DESC
-- MAGIC FETCH FIRST 50 ROWS ONLY;
-- MAGIC
-- MAGIC -- Identify BI/reporting queries by module or SQL pattern
-- MAGIC SELECT
-- MAGIC     s.sql_id,
-- MAGIC     NVL(s.module, 'unknown') AS module,
-- MAGIC     NVL(s.action, 'unknown') AS action,
-- MAGIC     SUBSTR(t.sql_text, 1, 200) AS sql_preview,
-- MAGIC     ROUND(s.elapsed_time / 1e6, 2) AS total_elapsed_sec,
-- MAGIC     s.executions,
-- MAGIC     ROUND(s.elapsed_time / GREATEST(s.executions, 1) / 1e6, 2) AS avg_elapsed_sec
-- MAGIC FROM v$sql s
-- MAGIC JOIN v$sqltext_with_newlines t ON t.sql_id = s.sql_id AND t.piece = 0
-- MAGIC WHERE s.last_active_time >= SYSDATE - 7
-- MAGIC   AND s.parsing_schema_name NOT IN ('SYS','SYSTEM','DBSNMP')
-- MAGIC   AND (
-- MAGIC     LOWER(s.module) LIKE '%tableau%'
-- MAGIC     OR LOWER(s.module) LIKE '%powerbi%'
-- MAGIC     OR LOWER(s.module) LIKE '%jdbc%'
-- MAGIC     OR LOWER(s.action) LIKE '%report%'
-- MAGIC     OR LOWER(s.action) LIKE '%dashboard%'
-- MAGIC   )
-- MAGIC ORDER BY s.elapsed_time DESC
-- MAGIC FETCH FIRST 50 ROWS ONLY;
-- MAGIC </div>
-- MAGIC
-- MAGIC </details>
-- MAGIC
-- MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
-- MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js"></script>
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

-- MAGIC %md-sandbox
-- MAGIC ## 4. Self-Service Analytics
-- MAGIC
-- MAGIC Enable business users to create, share, and interact with data through AI/BI Dashboards and Genie Spaces.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Databricks One and Consumer Access
-- MAGIC
-- MAGIC **Databricks One** provides a simplified interface for business users to consume dashboards, Genie spaces, and Databricks Apps-without navigating technical concepts like clusters or notebooks.
-- MAGIC
-- MAGIC | Entitlement | Databricks One UI | Lakehouse Workspace UI | Use Case |
-- MAGIC |-------------|-------------------|------------------------|----------|
-- MAGIC | **Consumer Access** | ✅ | ❌ | Read-only business users |
-- MAGIC | **Workspace Access** | ✅ | ✅ | Analysts, developers |
-- MAGIC | **Databricks SQL Access** | ✅ | ✅ | SQL analysts, dashboard creators |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">Consumer Access Configuration</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Users with only Consumer Access see only Databricks One. If your <code>users</code> group has additional entitlements (like Workspace Access), remove them to enable the simplified consumer experience. See <a href="https://docs.databricks.com/en/admin/users-groups/consumer-access.html" target="_blank">Change default workspace access to Consumer access</a>.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### AI/BI Dashboards
-- MAGIC
-- MAGIC AI/BI Dashboards provide interactive visualizations that business users can consume and filter. Dashboard creators can add filters that allow viewers to slice data without modifying the underlying queries.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Key capabilities for self-service:**
-- MAGIC
-- MAGIC | Capability | Description |
-- MAGIC |------------|-------------|
-- MAGIC | **Dashboard Filters** | Add dropdown, date range, or text filters that viewers can use to customize their view |
-- MAGIC | **Scheduled Refreshes** | Configure automatic data refresh on a schedule |
-- MAGIC | **PDF Subscriptions** | Email dashboard snapshots to stakeholders on a schedule |
-- MAGIC | **Share with Users/Groups** | Grant access to specific users or groups with view-only or edit permissions |
-- MAGIC | **Embed in Databricks Apps** | Integrate dashboards into custom applications |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #009688; background: #e0f2f1; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">💡</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #00695c; font-size: 1.1em;">Creating Shareable Dashboards</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">When building dashboards for self-service users, add filters on commonly-filtered dimensions (date ranges, regions, product categories). Use <strong>Publish</strong> to make the dashboard available, then <strong>Share</strong> to grant access to specific users or groups. Viewers can interact with filters without needing edit permissions.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### AI/BI Genie Spaces
-- MAGIC
-- MAGIC Genie Spaces enable natural language data exploration. Users ask questions in plain English, and Genie translates them into SQL queries against your data.
-- MAGIC
-- MAGIC **Setting up a Genie Space:**
-- MAGIC
-- MAGIC 1. Navigate to **Genie** in the workspace sidebar
-- MAGIC 2. Create a new Genie Space and connect it to a SQL Warehouse
-- MAGIC 3. Add tables from Unity Catalog that users can query
-- MAGIC 4. Provide sample questions and instructions to guide the AI
-- MAGIC 5. Share the Genie Space with users or groups
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Genie in Databricks One</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">In Databricks One, users can access shared Genie Spaces and ask questions directly from the search bar using the <strong>Ask</strong> feature. This provides a conversational interface for data exploration without requiring SQL knowledge.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 5. Future GenAI and ML Initiatives
-- MAGIC
-- MAGIC Post-cutover, Databricks provides a unified platform for advanced AI/ML workloads that significantly expands capabilities beyond what Oracle offers. This is where the migration investment delivers long-term strategic value.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### AI/ML Capability Comparison
-- MAGIC
-- MAGIC | Capability | <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="16" height="16" style="vertical-align: middle;" /> Oracle | <img src="https://cdn.simpleicons.org/databricks/FF3621" width="16" height="16" style="vertical-align: middle;"> Databricks | Advantage |
-- MAGIC |------------|-----------|------------|-----------|
-- MAGIC | **Experiment Tracking** | Oracle Machine Learning (OML) - basic notebooks only | MLflow (native integration) | Full experiment lineage, artifact tracking, model comparison |
-- MAGIC | **Model Registry** | Oracle Machine Learning Services (OML Services) - limited | Unity Catalog + MLflow | Unified governance across data and models |
-- MAGIC | **Model Serving** | OCI Data Science / Oracle Functions (complex setup) | Mosaic AI Model Serving | Auto-scaling, A/B testing, GPU optimization, Foundation Model APIs |
-- MAGIC | **Feature Store** | No native feature store | Unity Catalog Feature Store | Point-in-time correctness, online/offline serving, lineage |
-- MAGIC | **Vector Search** | Oracle AI Vector Search (23ai only) | Mosaic AI Vector Search | Native Delta Lake integration, automatic sync, hybrid search |
-- MAGIC | **Foundation Models** | Oracle Select AI / OCI Generative AI | Foundation Model APIs + AI Gateway | 70+ models, fine-tuning, provisioned throughput, centralized governance |
-- MAGIC | **RAG Applications** | Manual assembly via OCI | Mosaic AI Agent Framework | End-to-end tooling for retrieval-augmented generation |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Key Components for AI/ML Initiatives
-- MAGIC
-- MAGIC **MLflow** - Unified platform for the ML lifecycle including experiment tracking, model versioning, and deployment. Models registered in Unity Catalog inherit the same governance, lineage, and access controls as your data.
-- MAGIC
-- MAGIC **Mosaic AI Model Serving** - Deploy models as REST endpoints with automatic scaling, GPU support, and built-in monitoring. Supports custom models, foundation models (Llama, Mistral, etc.), and external models (OpenAI, Anthropic) through a unified API.
-- MAGIC
-- MAGIC **Mosaic AI Vector Search** - Managed vector database that syncs automatically with Delta tables. Powers semantic search and RAG applications without managing separate infrastructure. Supports hybrid search combining keyword and semantic matching.
-- MAGIC
-- MAGIC **Feature Store** - Centralized repository for ML features with automatic lineage tracking. Features defined once can be reused across models with point-in-time correctness for training and real-time lookup for serving.
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Getting Started with AI on Databricks</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Start with the <a href="https://docs.databricks.com/en/machine-learning/index.html" target="_blank">Mosaic AI documentation</a> and explore the <a href="https://www.databricks.com/resources/demos" target="_blank">AI/ML solution accelerators</a> for production-ready templates. The AI Playground in your workspace lets you experiment with foundation models before building applications.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #4caf50; background: #e8f5e9; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">✅</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #2e7d32; font-size: 1.1em;">Consumer Integration Checklist</strong>
-- MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li>Tableau and Power BI connected via JDBC/ODBC or Delta Sharing</li>
-- MAGIC                 <li>Dashboard refresh latency validated against SLA tiers</li>
-- MAGIC                 <li>Databricks One enabled for workspace (if using consumer access)</li>
-- MAGIC                 <li>Consumer access configured for read-only business users</li>
-- MAGIC                 <li>AI/BI Dashboards created with filters for self-service</li>
-- MAGIC                 <li>Genie Spaces configured and shared with relevant teams</li>
-- MAGIC                 <li>Adoption metrics dashboard configured</li>
-- MAGIC                 <li>AI/ML roadmap defined for post-cutover initiatives</li>
-- MAGIC             </ul>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Summary
-- MAGIC
-- MAGIC This lesson covered the post-cutover enablement roadmap, from connecting BI tools and enabling self-service analytics to planning strategic AI/ML initiatives.
-- MAGIC
-- MAGIC | Consumer Type | Connection | Self-Service Features |
-- MAGIC |---------------|------------|----------------------|
-- MAGIC | **BI Power Users** | Tableau/Power BI via Warehouse connectivity | Direct SQL access, custom reports |
-- MAGIC | **Business Users** | Databricks One (Consumer Access) | Dashboards, Genie Spaces, Apps |
-- MAGIC | **External Partners** | Delta Sharing | Read-only data access without direct connectivity |
-- MAGIC | **Data Science Teams** | Workspace Access | MLflow, Feature Store, Vector Search, Model Serving |
-- MAGIC
-- MAGIC **Key Takeaways:**
-- MAGIC
-- MAGIC - **BI Tools** - Use JDBC/ODBC SQL Warehouse connectivity for Tableau/Power BI; Delta Sharing for external sharing without direct connectivity
-- MAGIC - **Consumer Access** - Enable Databricks One for a simplified, read-only business user experience
-- MAGIC - **Dashboards** - Add interactive filters for viewers to slice data; share with users or groups
-- MAGIC - **Genie Spaces** - Enable natural language queries; add sample questions and instructions to guide users
-- MAGIC - **AI/ML (Post-Cutover)** - Leverage MLflow, Model Serving, and Vector Search-this is where Databricks delivers strategic advantage over Oracle
-- MAGIC - **Adoption** - Track unique users weekly via `system.query.history` using `executed_by` column
-- MAGIC
-- MAGIC **References:**
-- MAGIC
-- MAGIC - [Databricks Consumer Access](https://docs.databricks.com/aws/en/ai-bi/consumers/)
-- MAGIC - [What is Databricks One?](https://docs.databricks.com/aws/en/workspace/databricks-one)
-- MAGIC - [AI/BI Dashboards](https://docs.databricks.com/en/dashboards/index.html)
-- MAGIC - [AI/BI Genie Spaces](https://docs.databricks.com/en/genie/index.html)
-- MAGIC - [Connect Tableau to Databricks](https://docs.databricks.com/en/partners/bi/tableau.html)
-- MAGIC - [Connect Power BI to Databricks](https://docs.databricks.com/en/partners/bi/power-bi.html)
-- MAGIC - [Delta Sharing](https://docs.databricks.com/en/delta-sharing/index.html)
-- MAGIC - [MLflow on Databricks](https://docs.databricks.com/en/mlflow/index.html)
-- MAGIC - [Mosaic AI Model Serving](https://docs.databricks.com/en/machine-learning/model-serving/index.html)
-- MAGIC - [Mosaic AI Vector Search](https://docs.databricks.com/en/generative-ai/vector-search.html)
-- MAGIC - [Feature Engineering and Serving](https://docs.databricks.com/en/machine-learning/feature-store/index.html)

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
