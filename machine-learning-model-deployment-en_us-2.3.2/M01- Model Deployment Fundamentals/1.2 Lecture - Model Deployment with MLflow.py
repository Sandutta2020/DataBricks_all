# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img
# MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
# MAGIC     alt="Databricks Learning"
# MAGIC   >
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,Overview
# MAGIC %md-sandbox
# MAGIC # Lecture — Model Deployment with MLflow
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This lecture shows how MLflow packages a trained model once — with its code, dependencies, and metadata — so it is ready to be served through any deployment strategy. 
# MAGIC
# MAGIC This lecture covers 4 sections that build on each other:
# MAGIC
# MAGIC - **A. MLflow for Deployment**. MLflow's core components and the three deployment benefits it provides — dependency and environment management, packaging of models and code, and multiple deployment options.
# MAGIC - **B. The MLflow Model ("Flavor")**. The standard MLflow model format — the `MLmodel` file and directory — and the concept of flavors, including the default `python_function` flavor.
# MAGIC - **C. Models in Unity Catalog**. The centralized model store: versioning, aliases such as `@champion` and `@challenger`, lineage, and governance through the Unity Catalog three-level namespace.
# MAGIC - **D. Serving and Exporting Models**. How a registered model is served for batch, streaming, and real-time inference, and how it is exported to runtimes like ONNX for edge/embedded targets.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. Describe MLflow's deployment features and the benefits they provide.
# MAGIC 2. Describe the concept of model flavors and the role of the `python_function` flavor.
# MAGIC 3. Explain how Models in Unity Catalog manages the model lifecycle with versioning and aliases.
# MAGIC 4. Describe how a registered model is served for batch, streaming, and real-time inference, and exported for edge deployment.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. MLflow for Deployment

# COMMAND ----------

# DBTITLE 1,A1. The Core Components of MLflow
# MAGIC %md-sandbox
# MAGIC ### A1. The Core Components of MLflow
# MAGIC
# MAGIC **MLflow** is an open-source platform for managing the end-to-end machine learning lifecycle. It is co-developed by Databricks and comes pre-installed on Databricks Runtime for ML. Four core components carry a model from experiment to production — the last two, **Model Registry** and **Model Serving & Deployment**, are what turn a trained model into a deployable asset.
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 880 250" role="img" style="font-family: sans-serif;">
# MAGIC   <title>The Core Components of MLflow</title>
# MAGIC
# MAGIC   <!-- Tracking -->
# MAGIC   <rect x="15" y="20" width="200" height="150" rx="10" fill="#ECEFF1" stroke="#607D8B" stroke-width="1.5"/>
# MAGIC   <text x="115" y="48" text-anchor="middle" font-size="15" font-weight="bold" fill="#1565C0">Tracking</text>
# MAGIC   <line x1="45" y1="60" x2="185" y2="60" stroke="#607D8B" stroke-width="1"/>
# MAGIC   <text x="115" y="90" text-anchor="middle" font-size="12" fill="#1B3139">Record and query</text>
# MAGIC   <text x="115" y="108" text-anchor="middle" font-size="12" fill="#1B3139">experiments: code,</text>
# MAGIC   <text x="115" y="126" text-anchor="middle" font-size="12" fill="#1B3139">data, config, results</text>
# MAGIC
# MAGIC   <!-- Models -->
# MAGIC   <rect x="230" y="20" width="200" height="150" rx="10" fill="#ECEFF1" stroke="#607D8B" stroke-width="1.5"/>
# MAGIC   <text x="330" y="48" text-anchor="middle" font-size="15" font-weight="bold" fill="#1565C0">Models</text>
# MAGIC   <line x1="260" y1="60" x2="400" y2="60" stroke="#607D8B" stroke-width="1"/>
# MAGIC   <text x="330" y="90" text-anchor="middle" font-size="12" fill="#1B3139">General model</text>
# MAGIC   <text x="330" y="108" text-anchor="middle" font-size="12" fill="#1B3139">format that supports</text>
# MAGIC   <text x="330" y="126" text-anchor="middle" font-size="12" fill="#1B3139">diverse deploy tools</text>
# MAGIC
# MAGIC   <!-- Model Registry -->
# MAGIC   <rect x="445" y="20" width="200" height="150" rx="10" fill="#FFF3E0" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="545" y="48" text-anchor="middle" font-size="15" font-weight="bold" fill="#E65100">Model Registry</text>
# MAGIC   <line x1="475" y1="60" x2="615" y2="60" stroke="#F57C00" stroke-width="1"/>
# MAGIC   <text x="545" y="88" text-anchor="middle" font-size="12" fill="#1B3139">Centralized, governed</text>
# MAGIC   <text x="545" y="106" text-anchor="middle" font-size="12" fill="#1B3139">lifecycle with versions</text>
# MAGIC   <text x="545" y="124" text-anchor="middle" font-size="12" fill="#1B3139">&amp; aliases (in UC)</text>
# MAGIC
# MAGIC   <!-- Serving & Deployment -->
# MAGIC   <rect x="660" y="20" width="205" height="150" rx="10" fill="#FFF3E0" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="762" y="48" text-anchor="middle" font-size="15" font-weight="bold" fill="#E65100">Serving &amp; Deployment</text>
# MAGIC   <line x1="690" y1="60" x2="835" y2="60" stroke="#F57C00" stroke-width="1"/>
# MAGIC   <text x="762" y="88" text-anchor="middle" font-size="12" fill="#1B3139">Deploy registered</text>
# MAGIC   <text x="762" y="106" text-anchor="middle" font-size="12" fill="#1B3139">models to batch,</text>
# MAGIC   <text x="762" y="124" text-anchor="middle" font-size="12" fill="#1B3139">streaming &amp; real-time</text>
# MAGIC
# MAGIC   <!-- Deployment bracket -->
# MAGIC   <rect x="445" y="185" width="420" height="46" rx="8" fill="#FFF8E1" stroke="#F57C00" stroke-width="1.5"/>
# MAGIC   <text x="655" y="213" text-anchor="middle" font-size="13" font-weight="bold" fill="#E65100">Model Deployment</text>
# MAGIC
# MAGIC   <line x1="545" y1="170" x2="545" y2="185" stroke="#F57C00" stroke-width="1.5"/>
# MAGIC   <line x1="762" y1="170" x2="762" y2="185" stroke="#F57C00" stroke-width="1.5"/>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     On Databricks, the model registry is managed by <strong>Models in Unity Catalog</strong>, which provides unified governance, lineage, and versioning for all registered models. For new projects, it is recommended to use Unity Catalog to ensure consistent model management and deployment.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,A2. Why MLflow for Deployment
# MAGIC %md-sandbox
# MAGIC ### A2. Why MLflow for Deployment
# MAGIC
# MAGIC Moving a model to production is where many projects stall: the environment drifts from training, a dependency is missing, or the target platform expects a different packaging. MLflow addresses these with three deployment benefits.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 900px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Benefit</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">What it provides</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Dependency &amp; Environment Management</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Ensures the deployment environment matches the training environment, so models run consistently regardless of where they are deployed.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Packaging Models and Code</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Any code and configuration are packaged with the model, so it can be deployed seamlessly without any missing components.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Multiple Deployment Options</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">One packaged model can target many environments — built-in local serving, remote container serving (AzureML, AWS SageMaker), Kubernetes clusters, and Databricks Model Serving.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     MLflow lets you package a model <em>once</em> and deploy it <em>anywhere</em>—from local machines to cloud services and Databricks Model Serving. This flexibility ensures your model is ready for production, regardless of the target environment. The next section explains what is included in an MLflow model package and how it supports seamless deployment.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. The MLflow Model ("Flavor")

# COMMAND ----------

# DBTITLE 1,B1. A Standard Format for Packaging Models
# MAGIC %md-sandbox
# MAGIC ### B1. A Standard Format for Packaging Models
# MAGIC
# MAGIC An **MLflow Model** is a standard format for packaging machine learning models. Each model is a **directory** containing arbitrary files together with an `MLmodel` file at its root. That `MLmodel` file is the manifest — it declares which **flavors** the model can be viewed in, plus metadata such as the signature and an input example, so that MLflow deployment tools know how to load and use the model.
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 20px auto 0 auto; display: flex; gap: 24px; align-items: flex-start;">
# MAGIC <div style="flex: 1; font-size: 18px; text-align: left;">
# MAGIC <ul>
# MAGIC <li>Each <strong>MLflow Model</strong> is a directory of files plus an  <code>MLmodel</code> file.</li>
# MAGIC <li>The <code>MLmodel</code> file can define <strong>multiple flavors</strong> the model can be viewed in.</li>
# MAGIC <li>With flavors, MLflow <strong>deployment tools</strong> can understand the model.</li>
# MAGIC <li>The <code>MLmodel</code> file can carry <strong>additional metadata</strong> — <code>signature</code>, <code>input_example</code>, and more.</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC
# MAGIC <div style="flex: 1; background: #0B2027; border-radius: 10px; padding: 16px; overflow-x: auto;">
# MAGIC <div style="color: #7FD4FF; font-weight: bold; font-size: 15px; margin-bottom: 8px; text-align: center;">ml<em>flow</em> Model Flavor</div>
# MAGIC <div style="background: #e3f2fd; color: #111; border-radius: 7px; padding: 10px 14px; font-size: 13px; max-width: 410px; margin: 0 auto 10px auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, Menlo, monospace; font-size: 13px; color: #111; white-space: pre;">
# MAGIC # Directory written by
# MAGIC # mlflow.sklearn.save_model(model, "my_model")
# MAGIC my_model/
# MAGIC ├── MLmodel
# MAGIC ├── model.pkl
# MAGIC ├── conda.yaml
# MAGIC ├── python_env.yaml
# MAGIC └── requirements.txt
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="background: #e3f2fd; color: #111; border-radius: 7px; padding: 10px 14px; font-size: 13px; max-width: 410px; margin: 0 auto 10px auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, Menlo, monospace; font-size: 13px; color: #111; white-space: pre;">
# MAGIC # MLmodel file
# MAGIC sklearn:
# MAGIC     sklearn_version: 1.5.1
# MAGIC     pickled_model: model.pkl
# MAGIC python_function:
# MAGIC     loader_module: mlflow.sklearn
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,B2. Built-in Model Flavors and pyfunc
# MAGIC %md-sandbox
# MAGIC ### B2. Built-in Model Flavors and `pyfunc`
# MAGIC
# MAGIC A **flavor** is a way of viewing and loading a model. Most models carry a framework-specific flavor (scikit-learn, PyTorch, …) *and* the generic **Python Function (`mlflow.pyfunc`)** flavor. Pyfunc serves as the **default model interface** for MLflow Python models: any MLflow Python model is expected to be loadable as a Python function, which is what lets a single model be deployed to many targets without framework-specific serving code.
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 20px auto 0 auto; display: flex; gap: 24px; align-items: flex-start;">
# MAGIC <div style="flex: 1; font-size: 18px; text-align: left;">
# MAGIC
# MAGIC **Python Function (`mlflow.pyfunc`):**
# MAGIC <ul>
# MAGIC <li>Serves as a <strong>default model interface</strong> for MLflow Python models.</li>
# MAGIC <li>Any MLflow Python model is expected to be loadable as a Python function.</li>
# MAGIC <li>Allows you to <strong>deploy models as Python functions</strong>.</li>
# MAGIC <li>Includes all the information necessary to <strong>load and use a model</strong>.</li>
# MAGIC <li>Common functions: <code>log_model</code>, <code>save_model</code>, <code>load_model</code>, <code>predict</code>.</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC
# MAGIC <div style="flex: 1; background: #0B2027; border-radius: 10px; padding: 16px;">
# MAGIC <div style="background: #e3f2fd; color: #111; border-radius: 7px; padding: 10px 14px; font-size: 13px; max-width: 410px; margin: 0 auto 10px auto;">
# MAGIC <div style="color: #111; font-weight: bold; font-size: 18px; margin-bottom: 10px;">Example built-in model flavors</div>
# MAGIC <ul style="margin: 0; padding-left: 20px; color: #111; font-size: 16px; line-height: 1.9;">
# MAGIC   <li><strong>Python function</strong></li>
# MAGIC   <li>Spark MLlib</li>
# MAGIC   <li>Scikit-learn</li>
# MAGIC   <li>PyTorch</li>
# MAGIC   <li>TensorFlow</li>
# MAGIC   <li>LLM models: OpenAI, LangChain, HuggingFace</li>
# MAGIC   <li>Custom flavors</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     The <code>pyfunc</code> flavor is MLflow's universal interface for Python models. With <code>pyfunc</code>, every model—regardless of its underlying framework—can be loaded and used with the same <code>predict()</code> function. This means you can deploy models to batch, streaming, or real-time endpoints without needing framework-specific code. Pyfunc simplifies deployment and ensures consistency across all serving targets.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Models in Unity Catalog

# COMMAND ----------

# DBTITLE 1,C1. A Centralized, Governed Model Store
# MAGIC %md-sandbox
# MAGIC ### C1. A Centralized, Governed Model Store
# MAGIC
# MAGIC The **Model Registry** is a centralized model store that manages a model's lifecycle after training. On Databricks this is **Models in Unity Catalog**, where each registered model lives in the Unity Catalog three-level namespace — `catalog.schema.model` — and inherits UC governance.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 900px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 18px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Capability</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Deploy &amp; organize</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">A single place to register, organize, and deploy models across the organization.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Versioning</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Every registered model gets numbered versions, so you always know exactly which artifact is in use.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Lifecycle with aliases</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Point mutable aliases such as <code>@champion</code> and <code>@challenger</code> at specific versions. In Unity Catalog, model stages are <strong>not</strong> used — aliases and the UC namespace express environment and promotion instead.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Collaboration &amp; permissions</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Unity Catalog access controls govern who can read, use, or promote each model.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Lineage</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Full lineage links a model back to the data and runs that produced it.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Tagging &amp; annotations</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Attach tags and descriptions to organize and document models.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# DBTITLE 1,C2. Aliases and the UC Namespace
# MAGIC %md-sandbox
# MAGIC ### C2. Aliases and the UC Namespace
# MAGIC
# MAGIC Aliases are named, movable pointers to a specific model version. They let deployment code reference a stable name — for example, "whatever is currently `@champion`" — while you promote new versions behind the scenes without changing the code that serves the model.
# MAGIC
# MAGIC <div style="max-width: 820px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 820 230" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Aliases pointing at model versions in Unity Catalog</title>
# MAGIC
# MAGIC   <!-- Namespace label -->
# MAGIC   <rect x="20" y="20" width="780" height="34" rx="6" fill="#1B3139"/>
# MAGIC   <text x="410" y="43" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">main.ml_models.churn_model  (catalog.schema.model)</text>
# MAGIC
# MAGIC   <!-- Versions -->
# MAGIC   <rect x="120" y="90" width="160" height="50" rx="8" fill="#ECEFF1" stroke="#607D8B" stroke-width="1.5"/>
# MAGIC   <text x="200" y="120" text-anchor="middle" font-size="13" fill="#1B3139">Version 1</text>
# MAGIC
# MAGIC   <rect x="330" y="90" width="160" height="50" rx="8" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2"/>
# MAGIC   <text x="410" y="120" text-anchor="middle" font-size="13" font-weight="bold" fill="#2E7D32">Version 2</text>
# MAGIC
# MAGIC   <rect x="540" y="90" width="160" height="50" rx="8" fill="#FFF3E0" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="620" y="120" text-anchor="middle" font-size="13" font-weight="bold" fill="#E65100">Version 3</text>
# MAGIC
# MAGIC   <!-- Aliases -->
# MAGIC   <rect x="330" y="175" width="160" height="38" rx="19" fill="#00A972"/>
# MAGIC   <text x="410" y="199" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">@champion</text>
# MAGIC
# MAGIC   <rect x="540" y="175" width="160" height="38" rx="19" fill="#F57C00"/>
# MAGIC   <text x="620" y="199" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">@challenger</text>
# MAGIC
# MAGIC   <!-- Pointers -->
# MAGIC   <line x1="410" y1="175" x2="410" y2="145" stroke="#2E7D32" stroke-width="2" marker-end="url(#arrowC)"/>
# MAGIC   <line x1="620" y1="175" x2="620" y2="145" stroke="#F57C00" stroke-width="2" marker-end="url(#arrowCo)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowC" markerWidth="9" markerHeight="7" refX="4" refY="3.5" orient="auto">
# MAGIC       <polygon points="0 0, 9 3.5, 0 7" fill="#2E7D32"/>
# MAGIC     </marker>
# MAGIC     <marker id="arrowCo" markerWidth="9" markerHeight="7" refX="4" refY="3.5" orient="auto">
# MAGIC       <polygon points="0 0, 9 3.5, 0 7" fill="#F57C00"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     <code>@champion</code> and <code>@challenger</code> are aliases in Unity Catalog that point to specific model versions. <br>
# MAGIC     <ul style="margin-top:8px;">
# MAGIC       <li><b>@champion</b> marks the version currently serving production traffic.</li>
# MAGIC       <li><b>@challenger</b> marks a candidate version under evaluation.</li>
# MAGIC     </ul>
# MAGIC     Promoting a new model to production is as simple as moving the <code>@champion</code> alias to a different version—no code changes needed for serving. This enables safe, seamless model updates and A/B testing.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Serving and Exporting Models

# COMMAND ----------

# DBTITLE 1,D1. From Registry to Deployment Modes
# MAGIC %md-sandbox
# MAGIC ### D1. From Registry to Deployment Modes
# MAGIC
# MAGIC Once a model is packaged as a flavor and registered in Unity Catalog, the *same* model can be served for any of the deployment modes from the previous lecture. The flow is always the same: train → package as a flavor → register in UC → serve.
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 880 300" role="img" style="font-family: sans-serif;">
# MAGIC   <title>MLflow and Model Deployment Modes</title>
# MAGIC
# MAGIC   <!-- Source data -->
# MAGIC   <rect x="15" y="30" width="150" height="60" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="90" y="55" text-anchor="middle" font-size="13" font-weight="bold" fill="#1B3139">Delta Lake /</text>
# MAGIC   <text x="90" y="72" text-anchor="middle" font-size="12" fill="#1B3139">Feature Store</text>
# MAGIC
# MAGIC   <!-- Model training -->
# MAGIC   <rect x="15" y="130" width="150" height="60" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="90" y="150" text-anchor="middle" font-size="13" font-weight="bold" fill="#1B3139">Model training</text>
# MAGIC   <text x="90" y="170" text-anchor="middle" font-size="11" fill="#1B3139">scikit-learn, </text>
# MAGIC   <text x="90" y="180" text-anchor="middle" font-size="11" fill="#1B3139">XGBoost & TensorFlow</text>
# MAGIC
# MAGIC   <!-- Flavor -->
# MAGIC   <rect x="205" y="130" width="140" height="60" rx="8" fill="#FFF8E1" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="275" y="155" text-anchor="middle" font-size="13" font-weight="bold" fill="#E65100">Model "Flavor"</text>
# MAGIC   <text x="275" y="173" text-anchor="middle" font-size="12" fill="#1B3139">MLflow</text>
# MAGIC
# MAGIC   <!-- Registry -->
# MAGIC   <rect x="385" y="130" width="140" height="60" rx="8" fill="#FFF8E1" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="455" y="150" text-anchor="middle" font-size="13" font-weight="bold" fill="#E65100">Model Registry</text>
# MAGIC   <text x="455" y="170" text-anchor="middle" font-size="12" fill="#1B3139">in UC</text>
# MAGIC   <text x="455" y="185" text-anchor="middle" font-size="12" fill="#1B3139">MLflow</text>
# MAGIC
# MAGIC   <!-- Serving targets: mode name (left) + service name replacing the icon (right) + description -->
# MAGIC   <!-- Batch -->
# MAGIC   <rect x="600" y="18" width="265" height="56" rx="8" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="618" y="40" font-size="13" font-weight="bold" fill="#2E7D32">Batch</text>
# MAGIC   <text x="847" y="40" text-anchor="end" font-size="11" font-weight="bold" fill="#1565C0">Apache Spark</text>
# MAGIC   <text x="618" y="60" font-size="11" fill="#1B3139">Offline data processing in batches</text>
# MAGIC
# MAGIC   <!-- Streaming -->
# MAGIC   <rect x="600" y="82" width="265" height="56" rx="8" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="618" y="104" font-size="13" font-weight="bold" fill="#2E7D32">Streaming</text>
# MAGIC   <text x="847" y="104" text-anchor="end" font-size="11" font-weight="bold" fill="#1565C0">Spark Structured Streaming</text>
# MAGIC   <text x="618" y="124" font-size="11" fill="#1B3139">Processing streaming data</text>
# MAGIC
# MAGIC   <!-- Real-time -->
# MAGIC   <rect x="600" y="146" width="265" height="56" rx="8" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="618" y="168" font-size="13" font-weight="bold" fill="#2E7D32">Real-time</text>
# MAGIC   <text x="847" y="168" text-anchor="end" font-size="11" font-weight="bold" fill="#1565C0">Databricks Model Serving</text>
# MAGIC   <text x="618" y="188" font-size="11" fill="#1B3139">Real-time predictions with low latency</text>
# MAGIC
# MAGIC   <!-- Edge -->
# MAGIC   <rect x="600" y="210" width="265" height="56" rx="8" fill="#ECEFF1" stroke="#607D8B" stroke-width="1.5"/>
# MAGIC   <text x="618" y="232" font-size="13" font-weight="bold" fill="#455A64">Edge (Embedded)</text>
# MAGIC   <text x="850" y="232" text-anchor="end" font-size="11" font-weight="bold" fill="#1565C0">Docker · TF Lite</text>
# MAGIC   <text x="618" y="252" font-size="11" fill="#1B3139">Inference on local / edge devices</text>
# MAGIC
# MAGIC   <!-- Arrows: pipeline -->
# MAGIC   <line x1="90" y1="90" x2="90" y2="130" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowD1)"/>
# MAGIC   <line x1="165" y1="160" x2="205" y2="160" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowD1)"/>
# MAGIC   <line x1="345" y1="160" x2="385" y2="160" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowD1)"/>
# MAGIC
# MAGIC   <!-- Arrows: fan-out from registry to serving targets -->
# MAGIC   <path d="M525 158 C562 158, 572 46, 600 46" stroke="#2E7D32" stroke-width="1.5" fill="none" marker-end="url(#arrowD1g)"/>
# MAGIC   <path d="M525 159 C565 159, 575 110, 600 110" stroke="#2E7D32" stroke-width="1.5" fill="none" marker-end="url(#arrowD1g)"/>
# MAGIC   <path d="M525 161 C565 161, 575 174, 600 174" stroke="#2E7D32" stroke-width="1.5" fill="none" marker-end="url(#arrowD1g)"/>
# MAGIC   <path d="M525 163 C562 163, 575 238, 600 238" stroke="#607D8B" stroke-width="1.5" fill="none" marker-end="url(#arrowD1gr)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowD1" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#1B3139"/></marker>
# MAGIC     <marker id="arrowD1g" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#2E7D32"/></marker>
# MAGIC     <marker id="arrowD1gr" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#607D8B"/></marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     On Databricks, batch and streaming inference use Spark to apply models (as UDFs or in pipelines), while real-time inference is served by <strong>Databricks Model Serving</strong>. Edge and embedded deployments run off-platform on the device, which is covered in the next section.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,D2. Exporting Models for Edge Deployment
# MAGIC %md-sandbox
# MAGIC ### D2. Exporting Models for Edge Deployment
# MAGIC
# MAGIC In some cases — such as the **edge** — models must run on specific hardware, outside the Databricks platform. These environments have distinct characteristics that drive the export decision:
# MAGIC
# MAGIC - **Offline / unreliable connectivity** — the model cannot depend on a call back to a server.
# MAGIC - **Latency requirements** — predictions must happen locally, close to the data.
# MAGIC - **Security and compliance** — data may not be allowed to leave the device.
# MAGIC
# MAGIC For these targets, export the MLflow model to a portable inference runtime such as **ONNX** or **TensorFlow Lite**. A model trained in one framework can then run on a wide range of deployment targets (CPU, GPU, mobile, embedded) through a single interoperable format.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 190" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Exporting via ONNX to multiple deployment targets</title>
# MAGIC
# MAGIC   <!-- Training frameworks -->
# MAGIC   <rect x="20" y="30" width="200" height="130" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="120" y="52" text-anchor="middle" font-size="15" font-weight="bold" fill="#1565C0">Training framework</text>
# MAGIC   <text x="120" y="82" text-anchor="middle" font-size="14" fill="#1B3139">PyTorch · Keras</text>
# MAGIC   <text x="120" y="100" text-anchor="middle" font-size="14" fill="#1B3139">MLNET · scikit-learn</text>
# MAGIC
# MAGIC   <!-- ONNX hub -->
# MAGIC   <circle cx="430" cy="95" r="55" fill="#1B3139"/>
# MAGIC   <text x="430" y="92" text-anchor="middle" font-size="16" font-weight="bold" fill="#FFFFFF">ONNX</text>
# MAGIC   <text x="430" y="112" text-anchor="middle" font-size="10" fill="#7FD4FF">open &amp; interoperable</text>
# MAGIC
# MAGIC   <!-- Deployment targets -->
# MAGIC   <rect x="640" y="30" width="200" height="130" rx="8" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="740" y="52" text-anchor="middle" font-size="15" font-weight="bold" fill="#2E7D32">Deployment target</text>
# MAGIC   <text x="740" y="82" text-anchor="middle" font-size="13" fill="#1B3139">CPU · GPU</text>
# MAGIC   <text x="740" y="104" text-anchor="middle" font-size="13" fill="#1B3139">FPGA · NPU</text>
# MAGIC   <text x="740" y="126" text-anchor="middle" font-size="13" fill="#1B3139">mobile · embedded</text>
# MAGIC
# MAGIC   <!-- Arrows -->
# MAGIC   <line x1="220" y1="95" x2="372" y2="95" stroke="#1B3139" stroke-width="2" marker-end="url(#arrowE)"/>
# MAGIC   <line x1="488" y1="95" x2="640" y2="95" stroke="#1B3139" stroke-width="2" marker-end="url(#arrowE)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowE" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" fill="#1B3139"/></marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,D3. MLflow and ONNX — Example
# MAGIC %md-sandbox
# MAGIC ### D3. MLflow and ONNX — Example
# MAGIC
# MAGIC The workflow for an edge export has three steps: **convert** the model to ONNX format, **save** it with MLflow's ONNX flavor, and **score** it with the ONNX Runtime (or convert back to a native flavor). The example below converts a Keras model and logs it, then loads and scores it.
# MAGIC
# MAGIC - Convert model to ONNX format.
# MAGIC - Save the ONNX model as the **ONNX flavor**.
# MAGIC - Scoring: use **ONNX Runtime**, or convert to a native flavor.
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 14px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code><strong># Convert and log model as ONNX</strong>
# MAGIC import onnxmltools
# MAGIC onnx_model = onnxmltools.convert_keras(model)
# MAGIC mlflow.onnx.log_model(onnx_model, name="onnx-model")
# MAGIC </br>
# MAGIC <strong># Read and score model</strong>
# MAGIC import onnxruntime
# MAGIC session = onnxruntime.InferenceSession(onnx_model.SerializeToString())
# MAGIC input_name = session.get_inputs()[0].name
# MAGIC predictions = session.run(None, {input_name: data_np.astype(np.float32)})[0]</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     Exporting to ONNX or TensorFlow Lite is only needed for edge and embedded deployments that run off-platform. For batch, streaming, and real-time inference on Databricks, models are served directly from Unity Catalog—no export step required. Use Unity Catalog for consistent, governed model management and deployment.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,Conclusion
# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lecture, you covered how MLflow supports model deployment on Databricks:
# MAGIC
# MAGIC 1. **MLflow for Deployment** — MLflow's components (Tracking, Models, Model Registry, Serving & Deployment) manage the ML lifecycle, and its deployment benefits — dependency & environment management, packaging of models and code, and multiple deployment options — let you package a model once and deploy it anywhere.
# MAGIC 2. **The MLflow Model ("Flavor")** — An MLflow model is a standard directory format with an `MLmodel` manifest that declares one or more flavors. The default `python_function` (pyfunc) flavor gives every Python model a common `predict()` interface, so a single model can be served by many tools without framework-specific code.
# MAGIC 3. **Models in Unity Catalog** — The registry is a centralized, governed model store. In Unity Catalog, models live in the `catalog.schema.model` namespace with numbered versions and movable aliases such as `@champion` and `@challenger` (stages are not used), plus lineage, permissions, and tagging.
# MAGIC 4. **Serving and Exporting Models** — The same registered model can be served for batch, streaming, and real-time inference on Databricks, while edge/embedded targets are reached by exporting to portable runtimes such as ONNX or TensorFlow Lite.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
