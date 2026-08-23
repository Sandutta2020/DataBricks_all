# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
# MAGIC     <div style="font-size: 14px; color: #666;">
# MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
# MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
# MAGIC         <span style="margin-left: 8px;">06 - Closeout</span>
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

# MAGIC %md
# MAGIC # Developer Enablement
# MAGIC
# MAGIC With the migration complete, engineering teams need productive development workflows. This lesson covers the key tools that enable developers to work in familiar environments while executing code against Databricks compute: Databricks Connect for local IDE development, the VS Code extension for notebook workflows, Git Folders for version control, and Declarative Automation Bundles (DABs) for CI/CD deployment.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lesson, you will be able to:
# MAGIC
# MAGIC - Describe how Databricks Connect enables local IDE development with remote execution
# MAGIC - Configure the VS Code extension for notebook and job development
# MAGIC - Explain how Git Folders integrate version control into the Databricks workspace
# MAGIC - Deploy Declarative Automation Bundles with GitHub Actions for automated CI/CD

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## 1. Developer Workflow Architecture
# MAGIC
# MAGIC Databricks supports multiple development patterns, from browser-based notebooks to full local IDE workflows with remote execution.
# MAGIC
# MAGIC <br/>
# MAGIC <div class="mermaid">
# MAGIC flowchart LR
# MAGIC     subgraph LOCAL["Local Development"]
# MAGIC         IDE["VS Code / PyCharm"]
# MAGIC         CLI["Databricks CLI"]
# MAGIC     end
# MAGIC     subgraph TOOLS["Connection Layer"]
# MAGIC         DBC["Databricks Connect"]
# MAGIC         DAB["DABs"]
# MAGIC     end
# MAGIC     subgraph DBX["Databricks"]
# MAGIC         COMPUTE["Clusters / Serverless"]
# MAGIC         GIT["Git Folders"]
# MAGIC         JOBS["Lakeflow Jobs"]
# MAGIC     end
# MAGIC     IDE --> DBC
# MAGIC     DBC --> COMPUTE
# MAGIC     CLI --> DAB
# MAGIC     DAB --> JOBS
# MAGIC     IDE --> GIT
# MAGIC     style LOCAL fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
# MAGIC     style TOOLS fill:#fff3e0,stroke:#ff9800,stroke-width:2px
# MAGIC     style DBX fill:#ffe0b2,stroke:#FF3621,stroke-width:2px
# MAGIC </div>
# MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Databricks Connect
# MAGIC
# MAGIC Databricks Connect is a client library that allows you to run Spark code from local IDEs against Databricks compute. Built on open-source Spark Connect, it provides the familiar local development experience while leveraging Databricks clusters, Unity Catalog governance, and production-scale data.

# COMMAND ----------

# MAGIC %md
# MAGIC ### How It Works
# MAGIC
# MAGIC - **General code runs locally** - Python code executes on your local machine for interactive debugging
# MAGIC - **DataFrame operations run remotely** - Spark transformations execute on Databricks compute and are materialized locally when you call `collect()`, `show()`, or `toPandas()`
# MAGIC - **UDFs run on Databricks** - User-defined functions are serialized and transmitted to the cluster

# COMMAND ----------

# MAGIC %md
# MAGIC ### When to Use Databricks Connect
# MAGIC
# MAGIC | Use Case | Recommendation |
# MAGIC |----------|----------------|
# MAGIC | Interactive development and debugging | ✅ Databricks Connect |
# MAGIC | Integration testing with production data | ✅ Databricks Connect |
# MAGIC | Production job execution | ❌ Use Lakeflow Jobs |
# MAGIC | Notebook collaboration | ❌ Use Databricks workspace |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">ℹ️</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">Version Matching</strong>
# MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Install a Databricks Connect version that matches your cluster's DBR version. For example, use <code>pip install databricks-connect==14.3.*</code> for DBR 14.3 LTS. Configure authentication via the Databricks CLI with <code>databricks auth login</code>.</p>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. VS Code Extension
# MAGIC
# MAGIC The Databricks extension for Visual Studio Code provides a complete development environment for Databricks, enabling you to develop, debug, and deploy code without leaving your IDE.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Key Capabilities
# MAGIC
# MAGIC | Feature | Description |
# MAGIC |---------|-------------|
# MAGIC | **Run Python on clusters** | Execute local `.py` files on Databricks clusters or serverless compute |
# MAGIC | **Debug with Databricks Connect** | Set breakpoints and step through code with full IDE debugging |
# MAGIC | **Notebook support** | Run and debug notebooks cell-by-cell (`.py`, `.ipynb`, `.r`, `.scala`, `.sql`) |
# MAGIC | **DAB integration** | Define, deploy, and run DABs directly from the VS Code UI |
# MAGIC | **Workspace sync** | Synchronize local code with your Databricks workspace |

# COMMAND ----------

# MAGIC %md
# MAGIC ### Getting Started
# MAGIC
# MAGIC 1. Install the **Databricks** extension from the VS Code Marketplace
# MAGIC 2. Click the Databricks icon in the sidebar and select **Create a new project** or **Create configuration** for existing projects
# MAGIC 3. Authenticate to your workspace (OAuth or personal access token)
# MAGIC 4. Select a cluster for execution
# MAGIC 5. Start developing-run Python files, debug notebooks, or deploy bundles

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Git Folders
# MAGIC
# MAGIC Git Folders (formerly Repos) provide native Git integration within the Databricks workspace, enabling version control for notebooks, libraries, and configuration files directly in the UI.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Supported Git Providers
# MAGIC
# MAGIC | Provider | Authentication |
# MAGIC |----------|----------------|
# MAGIC | GitHub | Personal access token or GitHub App |
# MAGIC | GitLab | Personal access token |
# MAGIC | Azure DevOps | Azure AD or personal access token |
# MAGIC | Bitbucket | App password |
# MAGIC | AWS CodeCommit | HTTPS Git credentials |

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Workflow
# MAGIC
# MAGIC Git Folders enable a development workflow where code is authored and tested in the workspace, then committed and pushed to your Git provider. CI/CD pipelines can then deploy validated code to production workspaces.
# MAGIC
# MAGIC Configure Git credentials via **Settings -> Linked accounts** in the Databricks UI, or use the CLI:
# MAGIC
# MAGIC <div class="code-block" data-language="bash">
# MAGIC databricks git-credentials create --git-provider GitHub --git-username your-username --personal-access-token ghp_xxxx
# MAGIC </div>
# MAGIC
# MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
# MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
# MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
# MAGIC
# MAGIC <script>
# MAGIC (function() {
# MAGIC     document.querySelectorAll('.code-block').forEach(function(block) {
# MAGIC         if (block.getAttribute('data-processed')) return;
# MAGIC         block.setAttribute('data-processed', 'true');
# MAGIC         var lang = block.getAttribute('data-language') || 'bash';
# MAGIC         var code = block.textContent.trim();
# MAGIC         var id = 'code-' + Math.random().toString(36).substr(2, 9);
# MAGIC         block.innerHTML = 
# MAGIC             '<div style="position:relative;margin:16px 0;">' +
# MAGIC                 '<button class="copy-btn" style="position:absolute;top:8px;right:8px;padding:4px 12px;font-size:12px;background:#ddd;color:#333;border:1px solid #ccc;border-radius:4px;cursor:pointer;z-index:10;">Copy</button>' +
# MAGIC                 '<pre style="background:#f8f8f8;border-radius:8px;padding:16px;padding-top:40px;overflow-x:auto;margin:0;border:1px solid #e0e0e0;"><code id="' + id + '" class="language-' + lang + '" style="font-family:Consolas,Monaco,monospace;font-size:14px;"></code></pre>' +
# MAGIC             '</div>';
# MAGIC         var codeEl = document.getElementById(id);
# MAGIC         codeEl.textContent = code;
# MAGIC         Prism.highlightElement(codeEl);
# MAGIC         block.querySelector('.copy-btn').onclick = function() {
# MAGIC             var t = document.createElement('textarea');
# MAGIC             t.value = code;
# MAGIC             document.body.appendChild(t);
# MAGIC             t.select();
# MAGIC             document.execCommand('copy');
# MAGIC             document.body.removeChild(t);
# MAGIC             this.textContent = '✓ Copied!';
# MAGIC             setTimeout(() => this.textContent = 'Copy', 2000);
# MAGIC         };
# MAGIC     });
# MAGIC })();
# MAGIC </script>

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Declarative Automation Bundles (DABs)
# MAGIC
# MAGIC Declarative Automation Bundles are the recommended approach for deploying Databricks resources programmatically. A bundle is a collection of source files (notebooks, Python code, SQL), configuration, and resource definitions packaged together and deployed via the Databricks CLI.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Why Declarative Automation Bundles?
# MAGIC
# MAGIC - **Infrastructure as code** - Define jobs, pipelines, and resources in YAML alongside your source code
# MAGIC - **Multi-environment deployment** - Use targets to deploy the same bundle to dev, staging, and production
# MAGIC - **CI/CD integration** - Validate, deploy, and run bundles from GitHub Actions, Azure DevOps, or any CI system
# MAGIC - **Version control** - Store bundle configuration in Git for auditability and collaboration

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Bundle Structure
# MAGIC
# MAGIC ```bash
# MAGIC hr-migration-pipelines/
# MAGIC ├── databricks.yml              # Bundle configuration
# MAGIC ├── resources/
# MAGIC │   └── hr_migration_job.yml    # Job definition
# MAGIC ├── src/
# MAGIC │   ├── ingest_hr_data.py       # Bronze ingestion
# MAGIC │   └── validate_hr_data.py     # Silver validation
# MAGIC └── .github/
# MAGIC     └── workflows/
# MAGIC         └── deploy.yml          # CI/CD pipeline
# MAGIC ```

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### Example: HR Migration Pipeline Bundle
# MAGIC
# MAGIC The following example shows a complete bundle configuration for deploying an Oracle-to-Databricks HR migration pipeline across environments.
# MAGIC
# MAGIC <details>
# MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 databricks.yml: Bundle configuration</summary>
# MAGIC
# MAGIC <div class="code-block" data-language="yaml">
# MAGIC bundle:
# MAGIC   name: hr-migration-pipelines
# MAGIC
# MAGIC variables:
# MAGIC   catalog:
# MAGIC     default: migration_dev
# MAGIC   tags:
# MAGIC     team: data-engineering
# MAGIC     project: oracle-migration
# MAGIC
# MAGIC targets:
# MAGIC   dev:
# MAGIC     mode: development
# MAGIC     default: true
# MAGIC     workspace:
# MAGIC       host: https://dev-workspace.cloud.databricks.com
# MAGIC     variables:
# MAGIC       catalog: migration_dev
# MAGIC
# MAGIC   prod:
# MAGIC     mode: production
# MAGIC     workspace:
# MAGIC       host: https://prod-workspace.cloud.databricks.com
# MAGIC     variables:
# MAGIC       catalog: migration_prod
# MAGIC     run_as:
# MAGIC       service_principal_name: sp-hr-migration-prod
# MAGIC
# MAGIC resources:
# MAGIC   jobs:
# MAGIC     hr_daily_pipeline:
# MAGIC       name: "HR Daily Pipeline"
# MAGIC       tags:
# MAGIC         team: ${var.tags.team}
# MAGIC         project: ${var.tags.project}
# MAGIC         environment: ${bundle.target}
# MAGIC       schedule:
# MAGIC         quartz_cron_expression: "0 0 6 * * ?"
# MAGIC         timezone_id: UTC
# MAGIC       tasks:
# MAGIC         - task_key: ingest_hr_data
# MAGIC           notebook_task:
# MAGIC             notebook_path: ./src/ingest_hr_data.py
# MAGIC             base_parameters:
# MAGIC               catalog: ${var.catalog}
# MAGIC           job_cluster_key: pipeline_cluster
# MAGIC         - task_key: validate_hr_data
# MAGIC           depends_on:
# MAGIC             - task_key: ingest_hr_data
# MAGIC           notebook_task:
# MAGIC             notebook_path: ./src/validate_hr_data.py
# MAGIC             base_parameters:
# MAGIC               catalog: ${var.catalog}
# MAGIC           job_cluster_key: pipeline_cluster
# MAGIC       job_clusters:
# MAGIC         - job_cluster_key: pipeline_cluster
# MAGIC           new_cluster:
# MAGIC             spark_version: 15.4.x-scala2.12
# MAGIC             node_type_id: i3.xlarge
# MAGIC             num_workers: 2
# MAGIC             custom_tags:
# MAGIC               team: ${var.tags.team}
# MAGIC               project: ${var.tags.project}
# MAGIC </div>
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
# MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
# MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
# MAGIC
# MAGIC <script>
# MAGIC (function() {
# MAGIC     function processCodeBlocks() {
# MAGIC         document.querySelectorAll('.code-block').forEach(function(block) {
# MAGIC             if (block.getAttribute('data-processed')) return;
# MAGIC             block.setAttribute('data-processed', 'true');
# MAGIC             var lang = block.getAttribute('data-language') || 'sql';
# MAGIC             var code = block.textContent.trim();
# MAGIC             var id = 'code-' + Math.random().toString(36).substr(2, 9);
# MAGIC             block.innerHTML = 
# MAGIC                 '<div style="position:relative;margin:16px 0;">' +
# MAGIC                     '<button class="copy-btn" style="position:absolute;top:8px;right:8px;padding:4px 12px;font-size:12px;background:#ddd;color:#333;border:1px solid #ccc;border-radius:4px;cursor:pointer;z-index:10;">Copy</button>' +
# MAGIC                     '<pre style="background:#f8f8f8;border-radius:8px;padding:16px;padding-top:40px;overflow-x:auto;margin:0;border:1px solid #e0e0e0;"><code id="' + id + '" class="language-' + lang + '" style="font-family:Consolas,Monaco,monospace;font-size:14px;"></code></pre>' +
# MAGIC                 '</div>';
# MAGIC             var codeEl = document.getElementById(id);
# MAGIC             codeEl.textContent = code;
# MAGIC             Prism.highlightElement(codeEl);
# MAGIC             block.querySelector('.copy-btn').onclick = function() {
# MAGIC                 var t = document.createElement('textarea');
# MAGIC                 t.value = code;
# MAGIC                 document.body.appendChild(t);
# MAGIC                 t.select();
# MAGIC                 document.execCommand('copy');
# MAGIC                 document.body.removeChild(t);
# MAGIC                 this.textContent = '✓ Copied!';
# MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
# MAGIC             };
# MAGIC         });
# MAGIC     }
# MAGIC     processCodeBlocks();
# MAGIC     document.querySelectorAll('details').forEach(function(details) {
# MAGIC         details.addEventListener('toggle', processCodeBlocks);
# MAGIC     });
# MAGIC })();
# MAGIC </script>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### GitHub Actions Deployment
# MAGIC
# MAGIC Deploy Declarative Automation Bundles automatically on push or pull request using GitHub Actions.
# MAGIC
# MAGIC <details>
# MAGIC <summary style="cursor: pointer; font-weight: bold; font-size: 1.1em; padding: 8px 0;">🔽 .github/workflows/deploy.yml: CI/CD pipeline</summary>
# MAGIC
# MAGIC <div class="code-block" data-language="yaml">
# MAGIC name: Deploy HR Migration Pipeline
# MAGIC
# MAGIC on:
# MAGIC   push:
# MAGIC     branches: [main]
# MAGIC   pull_request:
# MAGIC     branches: [main]
# MAGIC
# MAGIC jobs:
# MAGIC   validate:
# MAGIC     runs-on: ubuntu-latest
# MAGIC     steps:
# MAGIC       - uses: actions/checkout@v4
# MAGIC
# MAGIC       - name: Install Databricks CLI
# MAGIC         uses: databricks/setup-cli@main
# MAGIC
# MAGIC       - name: Validate bundle
# MAGIC         run: databricks bundle validate
# MAGIC         env:
# MAGIC           DATABRICKS_HOST: ${{secrets}}
# MAGIC           DATABRICKS_TOKEN: ${{secrets}}
# MAGIC
# MAGIC   deploy-prod:
# MAGIC     needs: validate
# MAGIC     if: github.ref == 'refs/heads/main' && github.event_name == 'push'
# MAGIC     runs-on: ubuntu-latest
# MAGIC     environment: production
# MAGIC     steps:
# MAGIC       - uses: actions/checkout@v4
# MAGIC
# MAGIC       - name: Install Databricks CLI
# MAGIC         uses: databricks/setup-cli@main
# MAGIC
# MAGIC       - name: Deploy to production
# MAGIC         run: databricks bundle deploy --target prod
# MAGIC         env:
# MAGIC           DATABRICKS_HOST: ${{secrets}}
# MAGIC           DATABRICKS_TOKEN: ${{secrets}}
# MAGIC </div>
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
# MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
# MAGIC <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
# MAGIC
# MAGIC <script>
# MAGIC (function() {
# MAGIC     function processCodeBlocks() {
# MAGIC         document.querySelectorAll('.code-block').forEach(function(block) {
# MAGIC             if (block.getAttribute('data-processed')) return;
# MAGIC             block.setAttribute('data-processed', 'true');
# MAGIC             var lang = block.getAttribute('data-language') || 'sql';
# MAGIC             var code = block.textContent.trim();
# MAGIC             var id = 'code-' + Math.random().toString(36).substr(2, 9);
# MAGIC             block.innerHTML = 
# MAGIC                 '<div style="position:relative;margin:16px 0;">' +
# MAGIC                     '<button class="copy-btn" style="position:absolute;top:8px;right:8px;padding:4px 12px;font-size:12px;background:#ddd;color:#333;border:1px solid #ccc;border-radius:4px;cursor:pointer;z-index:10;">Copy</button>' +
# MAGIC                     '<pre style="background:#f8f8f8;border-radius:8px;padding:16px;padding-top:40px;overflow-x:auto;margin:0;border:1px solid #e0e0e0;"><code id="' + id + '" class="language-' + lang + '" style="font-family:Consolas,Monaco,monospace;font-size:14px;"></code></pre>' +
# MAGIC                 '</div>';
# MAGIC             var codeEl = document.getElementById(id);
# MAGIC             codeEl.textContent = code;
# MAGIC             Prism.highlightElement(codeEl);
# MAGIC             block.querySelector('.copy-btn').onclick = function() {
# MAGIC                 var t = document.createElement('textarea');
# MAGIC                 t.value = code;
# MAGIC                 document.body.appendChild(t);
# MAGIC                 t.select();
# MAGIC                 document.execCommand('copy');
# MAGIC                 document.body.removeChild(t);
# MAGIC                 this.textContent = '✓ Copied!';
# MAGIC                 setTimeout(() => this.textContent = 'Copy', 2000);
# MAGIC             };
# MAGIC         });
# MAGIC     }
# MAGIC     processCodeBlocks();
# MAGIC     document.querySelectorAll('details').forEach(function(details) {
# MAGIC         details.addEventListener('toggle', processCodeBlocks);
# MAGIC     });
# MAGIC })();
# MAGIC </script>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <div style="border-left: 4px solid #4caf50; background: #e8f5e9; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
# MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
# MAGIC         <span style="font-size: 24px;">✅</span>
# MAGIC         <div>
# MAGIC             <strong style="color: #2e7d32; font-size: 1.1em;">Developer Enablement Checklist</strong>
# MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
# MAGIC                 <li>Databricks Connect installed and configured for local development</li>
# MAGIC                 <li>VS Code extension installed with workspace authentication</li>
# MAGIC                 <li>Git credentials configured in Databricks</li>
# MAGIC                 <li>Repository cloned to Git Folders</li>
# MAGIC                 <li>Declarative Automation Bundles (DABs) configured for multi-environment deployment</li>
# MAGIC                 <li>CI/CD pipeline operational (GitHub Actions, Azure DevOps, etc.)</li>
# MAGIC                 <li>Developer onboarding guide published</li>
# MAGIC             </ul>
# MAGIC         </div>
# MAGIC     </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC
# MAGIC This lesson covered the key tools for enabling developer productivity on Databricks after migration.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Developer Tools Comparison
# MAGIC
# MAGIC | <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="16" height="16" style="vertical-align: middle;" /> Oracle | <img src="https://cdn.simpleicons.org/databricks/FF3621" width="16" height="16" style="vertical-align: middle;"> Databricks | Notes |
# MAGIC |-----------|------------|-------|
# MAGIC | Oracle Connector for Python | Databricks Connect | Local IDE with remote compute |
# MAGIC | VS Code Oracle extension | VS Code Databricks extension | Full IDE integration |
# MAGIC | Oracle SQL\*Plus / SQLcl | Databricks CLI | Command-line operations |
# MAGIC | Git integration (limited) | Git Folders | Native workspace Git support |
# MAGIC | N/A | Declarative Automation Bundles (DABs) | Infrastructure as code + CI/CD |
# MAGIC
# MAGIC **Key Takeaways:**
# MAGIC
# MAGIC - **Databricks Connect** - Run Spark code locally against remote Databricks compute for interactive development
# MAGIC - **VS Code Extension** - Full IDE integration for notebooks, debugging, and DAB deployment
# MAGIC - **Git Folders** - Native Git integration in the workspace for version control
# MAGIC - **Declarative Automation Bundles** - Define jobs and resources as code; deploy via CI/CD pipelines
# MAGIC
# MAGIC **References:**
# MAGIC
# MAGIC - [Databricks Connect](https://docs.databricks.com/en/dev-tools/databricks-connect/index.html)
# MAGIC - [VS Code Extension](https://docs.databricks.com/en/dev-tools/vscode-ext/index.html)
# MAGIC - [Git Folders](https://docs.databricks.com/en/repos/index.html)
# MAGIC - [Declarative Automation Bundles](https://docs.databricks.com/en/dev-tools/bundles/index.html)

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
# MAGIC
# MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
