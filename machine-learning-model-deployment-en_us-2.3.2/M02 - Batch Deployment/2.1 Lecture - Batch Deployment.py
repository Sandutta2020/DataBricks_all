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
# MAGIC # Lecture — Introduction to Batch Deployment
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This lecture covers batch deployment — the most common way to put a model into production. 
# MAGIC
# MAGIC This lecture covers 4 sections that build on each other:
# MAGIC
# MAGIC - **A. Batch Deployment Fundamentals**. What batch deployment is, a typical use case, and the advantages and limitations of the approach.
# MAGIC - **B. The Batch Deployment Workflow**. The end-to-end path from a registered model to written predictions, and how to load a model from Unity Catalog with `pyfunc` and compute predictions.
# MAGIC - **C. Batch Inference with Feature Engineering**. Using offline feature tables and the `FeatureEngineeringClient` to run batch inference with `score_batch`, `FeatureLookup`, and `FeatureFunction`.
# MAGIC - **D. Performance and Optimization**. How Delta Lake features — Liquid Clustering, Predictive Optimization, `OPTIMIZE`, and `VACUUM` — keep batch inference fast and efficient.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. Describe batch deployment and identify scenarios in which this method is required.
# MAGIC 2. Identify the advantages and disadvantages of deploying a model via batch processing.
# MAGIC 3. Load a logged model from Unity Catalog using `pyfunc` and compute predictions using the `pyfunc` APIs.
# MAGIC 4. Perform batch inference using Feature Engineering's `score_batch`, and connect Delta Lake's optimization techniques to batch deployment scenarios.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Batch Deployment Fundamentals

# COMMAND ----------

# DBTITLE 1,A1. What Is Batch Deployment
# MAGIC %md-sandbox
# MAGIC ### A1. What Is Batch Deployment
# MAGIC
# MAGIC In **batch deployment**, batch processing generates predictions on a **regular schedule** and writes the results out to persistent storage to be consumed downstream (for example, ad-hoc BI). It is the **most common deployment strategy**.
# MAGIC
# MAGIC Batch deployment is ideal for cases when:
# MAGIC
# MAGIC - Immediate predictions are **not** necessary.
# MAGIC - Predictions can be made in batch fashion.
# MAGIC - The number/volume of (new) records to predict is **large**.
# MAGIC - New records arrive relatively infrequently (e.g., minutes to hours), so predictions do not need to be generated the moment data arrives.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 170" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Batch Deployment at a Glance</title>
# MAGIC
# MAGIC   <!-- Schedule -->
# MAGIC   <rect x="20" y="55" width="180" height="70" rx="10" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="110" y="85" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Regular schedule</text>
# MAGIC   <text x="110" y="106" text-anchor="middle" font-size="12" fill="#1B3139">daily / weekly / monthly</text>
# MAGIC
# MAGIC   <!-- Score batch -->
# MAGIC   <rect x="280" y="55" width="180" height="70" rx="10" fill="#1B3139"/>
# MAGIC   <text x="370" y="85" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">Score a large batch</text>
# MAGIC   <text x="370" y="106" text-anchor="middle" font-size="12" fill="#F9F7F4">of new records at once</text>
# MAGIC
# MAGIC   <!-- Persist -->
# MAGIC   <rect x="540" y="55" width="180" height="70" rx="10" fill="#E8F5E9" stroke="#388E3C" stroke-width="2"/>
# MAGIC   <text x="630" y="85" text-anchor="middle" font-size="14" font-weight="bold" fill="#2E7D32">Write to storage</text>
# MAGIC   <text x="630" y="106" text-anchor="middle" font-size="12" fill="#1B3139">read downstream later</text>
# MAGIC
# MAGIC   <line x1="200" y1="90" x2="280" y2="90" stroke="#1B3139" stroke-width="2" marker-end="url(#arrowA1)"/>
# MAGIC   <line x1="460" y1="90" x2="540" y2="90" stroke="#1B3139" stroke-width="2" marker-end="url(#arrowA1)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowA1" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" fill="#1B3139"/></marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,A2. A Typical Batch Use Case
# MAGIC %md-sandbox
# MAGIC ### A2. A Typical Batch Use Case
# MAGIC
# MAGIC **Description:** Identifying potential churners in a subscription-based service.
# MAGIC
# MAGIC **Scenario:**
# MAGIC - A machine learning model is trained on historical data — including customer usage patterns, interactions, and subscription details.
# MAGIC - The model is saved (registered) for later use.
# MAGIC - At the end of each day/week/month, the collected data for that period is processed in a batch, and churn predictions are generated.
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     Batch deployment is ideal for churn prediction because actions (like retention campaigns) are scheduled, not immediate. Predictions are generated for large volumes of records, and the data does not need to be real-time—yesterday’s results are still actionable. This approach keeps costs low and simplifies operations, making it a practical fit for business processes that run on daily, weekly, or monthly cycles.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,A3. Advantages and Limitations
# MAGIC %md-sandbox
# MAGIC ### A3. Advantages and Limitations
# MAGIC
# MAGIC Batch deployment trades freshness for simplicity and cost. Knowing both sides tells you when to reach for it — and when to choose streaming or real-time instead.
# MAGIC
# MAGIC </br>
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .ds-row { display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 240px; }
# MAGIC .ds-card { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid var(--accent, #4299E0); }
# MAGIC .green{--accent:#00A972;} .coral{--accent:#FF5F46;}
# MAGIC .ds-card-title { font-size: 16pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
# MAGIC .ds-card-text { font-size: 14pt; color: #5E7077; line-height: 1.55; margin: 0; }
# MAGIC .ds-card ul, .ds-card ol { margin: 8px 0 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-card li { margin-bottom: 10px; }
# MAGIC .ds-card li:last-child { margin-bottom: 0; }
# MAGIC .tc { text-align: center; }
# MAGIC .dd-head { font-size: 16pt; font-weight: 700; margin: 4px 0 12px; color: var(--accent); }
# MAGIC </style>
# MAGIC
# MAGIC <div class="ds-row">
# MAGIC   <div class="ds-card green">
# MAGIC     <div class="dd-head">ADVANTAGES</div>
# MAGIC     <ul>
# MAGIC       <li><strong>Cheapest</strong> deployment method</li>
# MAGIC       <li><strong>Ease</strong> of implementation</li>
# MAGIC       <li>Efficient per data point</li>
# MAGIC       <li>Can handle a <strong>high volume of data</strong></li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC   <div class="ds-card coral">
# MAGIC     <div class="dd-head">LIMITATIONS</div>
# MAGIC     <ul>
# MAGIC       <li>High <strong>latency</strong></li>
# MAGIC       <li><strong>Stale data</strong></li>
# MAGIC       <li>Not suitable for dynamic or rapidly changing data</li>
# MAGIC       <li>Not suitable for streaming data or real-time applications</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. The Batch Deployment Workflow

# COMMAND ----------

# DBTITLE 1,B1. The End-to-End Batch Workflow
# MAGIC %md-sandbox
# MAGIC ### B1. The End-to-End Batch Workflow
# MAGIC
# MAGIC A typical batch deployment workflow connects four stages: source data, model training, model registration, and scheduled batch inference. The whole path runs as an **automated job with Databricks Workflows**, and the predictions fan out to whatever downstream consumers need them.
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 880 340" role="img" style="font-family: sans-serif;">
# MAGIC   <title>A Typical Batch Model Deployment Workflow</title>
# MAGIC
# MAGIC   <!-- Left column: build the model -->
# MAGIC   <rect x="15" y="30" width="150" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="90" y="52" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Delta Lake /</text>
# MAGIC   <text x="90" y="68" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Feature Engineering</text>
# MAGIC
# MAGIC   <rect x="15" y="130" width="150" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="90" y="152" text-anchor="middle" font-size="12" font-weight="bold"  fill="#1B3139">Model training</text>
# MAGIC   <text x="90" y="169" text-anchor="middle" font-size="10" fill="#607D8B">sklearn · XGBoost · TF</text>
# MAGIC
# MAGIC   <rect x="205" y="130" width="160" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="285" y="150" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Models in</text>
# MAGIC   <text x="285" y="165" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Unity Catalog</text>
# MAGIC   <text x="285" y="180" text-anchor="middle" font-size="10" fill="#607D8B">mlflow</text>
# MAGIC
# MAGIC   <!-- Dashed automated-job region -->
# MAGIC   <rect x="400" y="20" width="465" height="300" rx="12" fill="none" stroke="#7B1FA2" stroke-width="1.8" stroke-dasharray="7,5"/>
# MAGIC   <text x="632" y="308" text-anchor="middle" font-size="12" font-weight="bold" fill="#6A1B9A">Automated job with Databricks Workflows</text>
# MAGIC
# MAGIC   <!-- New data -->
# MAGIC   <rect x="440" y="35" width="150" height="60" rx="8" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="515" y="55" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Delta Lake /</text>
# MAGIC   <text x="515" y="70" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Feature Engineering</text>
# MAGIC   <text x="515" y="88" text-anchor="middle" font-size="11" font-weight="bold" fill="#2E7D32">New Data</text>
# MAGIC
# MAGIC   <!-- Batch inference -->
# MAGIC   <rect x="440" y="140" width="150" height="70" rx="8" fill="#FFF8E1" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="515" y="170" text-anchor="middle" font-size="13" font-weight="bold" fill="#E65100">Batch Inference</text>
# MAGIC   <text x="515" y="192" text-anchor="middle" font-size="12" fill="#1B3139" font-family="monospace">pyfunc.predict</text>
# MAGIC
# MAGIC   <!-- Downstream consumers -->
# MAGIC   <rect x="650" y="35" width="200" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="665" y="57" font-size="13" font-weight="bold" fill="#1B3139">Data Lake</text>
# MAGIC   <text x="665" y="75" font-size="11" fill="#607D8B">Offline data processing</text>
# MAGIC
# MAGIC   <rect x="650" y="100" width="200" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="665" y="122" font-size="13" font-weight="bold" fill="#1B3139">Database</text>
# MAGIC   <text x="665" y="140" font-size="11" fill="#607D8B">Serving stored predictions</text>
# MAGIC
# MAGIC   <rect x="650" y="165" width="200" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="665" y="187" font-size="12" font-weight="bold" fill="#1B3139">Downstream consumer</text>
# MAGIC   <text x="665" y="205" font-size="11" fill="#607D8B">BI, apps, reports, …</text>
# MAGIC
# MAGIC   <!-- Arrows -->
# MAGIC   <line x1="90" y1="85" x2="90" y2="130" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowB1)"/>
# MAGIC   <line x1="165" y1="157" x2="205" y2="157" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowB1)"/>
# MAGIC   <line x1="365" y1="157" x2="440" y2="175" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowB1)"/>
# MAGIC   <line x1="515" y1="95" x2="515" y2="140" stroke="#2E7D32" stroke-width="1.5" marker-end="url(#arrowB1g)"/>
# MAGIC   <path d="M590 168 C620 168, 625 62, 650 62" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowB1)"/>
# MAGIC   <path d="M590 172 C620 172, 625 127, 650 127" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowB1)"/>
# MAGIC   <path d="M590 178 C620 178, 625 192, 650 192" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowB1)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowB1" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#1B3139"/></marker>
# MAGIC     <marker id="arrowB1g" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#2E7D32"/></marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     Batch deployment follows a repeatable workflow: train your model once, register it in Unity Catalog, and schedule a job to load the model, score new data, and write predictions to storage. This approach keeps operations simple and scalable—predictions are always available for downstream consumers like BI tools, databases, or reports, without needing real-time code or manual intervention.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,B2. Loading a Model with pyfunc and Predicting
# MAGIC %md-sandbox
# MAGIC ### B2. Loading a Model with `pyfunc` and Predicting
# MAGIC
# MAGIC Batch inference centers on the generic **`python_function` (pyfunc)** flavor. You load a registered model from Unity Catalog by its three-level name (`catalog.schema.model`) and an alias or version, then call `.predict()` on new data — regardless of the framework the model was trained in.
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>import mlflow
# MAGIC mlflow.set_registry_uri("databricks-uc")
# MAGIC </br>
# MAGIC <strong># Load the registered model from Unity Catalog as a generic pyfunc model</strong>
# MAGIC model_uri = "models:/main.ml_models.churn_model@champion"
# MAGIC model = mlflow.pyfunc.load_model(model_uri)
# MAGIC </br>
# MAGIC <strong># Score new data — returns a prediction per input row</strong>
# MAGIC predictions = model.predict(new_data_pdf)</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC For large tables, wrap the same model as a **Spark UDF** so scoring runs in parallel across the cluster and writes straight back to Delta:
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <strong># Distribute scoring across the cluster with a Spark UDF</strong>
# MAGIC <code>predict_udf = mlflow.pyfunc.spark_udf(spark, model_uri)
# MAGIC scored_df = new_data_df.withColumn("prediction", predict_udf(*new_data_df.columns))
# MAGIC scored_df.write.mode("overwrite").saveAsTable("main.ml_models.churn_predictions")</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     The <code>pyfunc</code> flavor provides a unified <code>predict()</code> interface for all registered models, regardless of their training framework (scikit-learn, XGBoost, TensorFlow, etc.). This means your batch deployment code stays simple and consistent—no need for framework-specific logic. Just load the model and call <code>predict()</code> on new data.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Batch Inference with Feature Engineering

# COMMAND ----------

# DBTITLE 1,C1. Offline Feature Tables
# MAGIC %md-sandbox
# MAGIC ### C1. Offline Feature Tables
# MAGIC
# MAGIC When features live in **Feature Engineering in Unity Catalog**, batch inference can pull them automatically at scoring time. An **offline feature table** is simply a Delta table with a primary key, managed through the `FeatureEngineeringClient`.
# MAGIC
# MAGIC **Offline Feature Tables:**
# MAGIC - A **Delta table with a primary key**.
# MAGIC - Train and serve a model for batch inference with `FeatureEngineeringClient()`.
# MAGIC - Support `FeatureLookup` and `FeatureFunction` for batch model inference.
# MAGIC - **Not optimized for real-time inference** due to latency.
# MAGIC
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .flow-grid { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; gap: 0; align-items: stretch; }
# MAGIC .flow-step { background: #F9F7F4; border: 3px solid var(--accent, #4299E0); border-radius: 10px; padding: 16px 12px; box-shadow: 0 2px 8px rgba(27,49,57,0.08); text-align: center; min-width: 0; }
# MAGIC .flow-num { font-size: 26pt; font-weight: 800; color: var(--accent, #4299E0); line-height: 1; margin-bottom: 8px; }
# MAGIC .flow-label { font-size: 14pt; font-weight: 600; color: #0b2026; line-height: 1.35; }
# MAGIC .flow-arrow { display: flex; align-items: center; justify-content: center; color: #618794; font-size: 22pt; line-height: 1; }
# MAGIC </style>
# MAGIC
# MAGIC <div class="flow-grid">
# MAGIC   <div class="flow-step" style="--accent:#4299E0;">
# MAGIC     <div class="flow-num">1</div>
# MAGIC     <div class="flow-label">Offline Feature Table<br><span style="font-size:12pt;font-weight:400;">Delta table + primary key</span></div>
# MAGIC   </div>
# MAGIC   <div class="flow-arrow">&rarr;</div>
# MAGIC   <div class="flow-step" style="--accent:#FFAB00;">
# MAGIC     <div class="flow-num">2</div>
# MAGIC     <div class="flow-label">Register lookups &amp; functions<br><span style="font-size:12pt;font-weight:400;">then train</span></div>
# MAGIC   </div>
# MAGIC   <div class="flow-arrow">&rarr;</div>
# MAGIC   <div class="flow-step" style="--accent:#00A972;">
# MAGIC     <div class="flow-num">3</div>
# MAGIC     <div class="flow-label">Batch Inference<br><span style="font-size:12pt;font-weight:400;">fe.score_batch</span></div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <svg width="100%" viewBox="0 0 860 170" role="img" style="font-family: sans-serif;">
# MAGIC   <!-- Client banner -->
# MAGIC   <rect x="230" y="50" width="400" height="40" rx="8" fill="#1B3139"/>
# MAGIC   <text x="430" y="75" text-anchor="middle" font-size="14" fill="#F9F7F4" font-family="monospace">fe = FeatureEngineeringClient()</text>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowC1" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" fill="#1B3139"/></marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,C2. Batch Inference with score_batch
# MAGIC %md-sandbox
# MAGIC ### C2. Batch Inference with `score_batch`
# MAGIC
# MAGIC When a model is logged with the `FeatureEngineeringClient`, the feature metadata — which features to look up and how — is packaged with the model. At inference time you pass only the **primary keys**, and `score_batch` joins the required features from the offline feature tables automatically before scoring.
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>from databricks.feature_engineering import FeatureEngineeringClient
# MAGIC fe = FeatureEngineeringClient()
# MAGIC </br>
# MAGIC <strong># Inference_df needs only the primary keys — features are looked up automatically</strong>
# MAGIC predictions_df = fe.score_batch(
# MAGIC     model_uri="models:/main.ml_models.churn_model@champion",
# MAGIC     df=inference_df,
# MAGIC )
# MAGIC display(predictions_df)</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     <strong>FeatureLookup</strong> pulls precomputed features from an offline feature table using primary keys, while <strong>FeatureFunction</strong> computes features dynamically using a Unity Catalog-governed Python UDF. Both are defined at training time and automatically applied during <code>score_batch</code>, ensuring consistent feature logic for both training and batch inference. This keeps your batch scoring reliable and repeatable, with no manual feature joins required.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Performance and Optimization

# COMMAND ----------

# DBTITLE 1,D1. Liquid Clustering
# MAGIC %md-sandbox
# MAGIC ### D1. Liquid Clustering
# MAGIC
# MAGIC Because batch inference reads and writes large Delta tables, the physical layout of those tables drives job performance. **Liquid clustering** is an alternative to **table partitioning** and **`ZORDER`** that simplifies data-layout decisions while optimizing query performance.
# MAGIC
# MAGIC - Liquid clustering replaces partitioning and `ZORDER` — you no longer choose partition columns up front.
# MAGIC - Databricks **recommends liquid clustering for all new Delta tables**.
# MAGIC - The Databricks client manages all layout and optimization operations for the data in your table.
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>CREATE TABLE table1 (col0 int, col1 string)
# MAGIC USING DELTA
# MAGIC CLUSTER BY (col0);</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     Liquid clustering is available on DBR 13.3 and above. Use <code>CLUSTER BY</code> when creating Delta tables—no need to pre-select partition columns. Clustering keys can be updated later without rewriting the table, making data layout flexible and maintenance simple.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,D2. Predictive Optimization
# MAGIC %md-sandbox
# MAGIC ### D2. Predictive Optimization
# MAGIC
# MAGIC Rather than scheduling maintenance yourself, **Predictive Optimization** lets Databricks decide when a table needs it. Databricks **automatically identifies** tables that would benefit from maintenance operations and **runs them for you**.
# MAGIC
# MAGIC - Automatically runs maintenance operations:
# MAGIC   - **`OPTIMIZE`** → improves query performance by optimizing file sizes.
# MAGIC   - **`VACUUM`** → deletes data files no longer referenced by the table.
# MAGIC - Predictive optimization is **enabled by default for Unity Catalog managed tables**.
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code><strong>-- Check predictive optimization status (catalog)</strong>
# MAGIC DESCRIBE CATALOG EXTENDED &lt;catalog_name&gt;;
# MAGIC </br>
# MAGIC <strong>-- Check predictive optimization status (schema)</strong>
# MAGIC DESCRIBE SCHEMA EXTENDED &lt;schema_name&gt;;</code>
# MAGIC </pre>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,D3. OPTIMIZE and VACUUM
# MAGIC %md-sandbox
# MAGIC ### D3. `OPTIMIZE` and `VACUUM`
# MAGIC
# MAGIC When you manage maintenance manually, two commands do most of the work. **`OPTIMIZE`** improves read-query speed by coalescing many small files into larger ones — directly benefiting the large scans a batch job performs. **`VACUUM`** removes data files that are no longer referenced by the table, reclaiming storage.
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code><strong>-- Manually compact small files into larger ones</strong>
# MAGIC OPTIMIZE table1;
# MAGIC </br>
# MAGIC <strong>-- Remove data files no longer referenced by the table</strong>
# MAGIC VACUUM table1;</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     Databricks recommends enabling <strong>predictive optimization</strong> for Delta tables. This feature automatically runs <code>OPTIMIZE</code> and <code>VACUUM</code> maintenance operations, keeping your batch tables performant without manual scheduling. Manual commands are available, but predictive optimization ensures your tables stay fast and storage-efficient with minimal effort.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,Conclusion
# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lecture, you covered batch deployment end to end:
# MAGIC
# MAGIC 1. **Batch Deployment Fundamentals** — Batch processing generates predictions on a regular schedule and writes them to storage for downstream use. It is the most common strategy — cheapest, easy to implement, and able to handle high data volumes — but it comes with high latency and stale data, so it fits cases where immediate predictions are not required.
# MAGIC 2. **The Batch Deployment Workflow** — Train a model, register it in Models in Unity Catalog, then on a schedule load it with the `pyfunc` flavor and score new data — as a pandas `predict()` call or, at scale, a Spark UDF that writes results back to Delta. The whole flow runs as an automated Databricks Workflows job.
# MAGIC 3. **Batch Inference with Feature Engineering** — Offline feature tables (Delta tables with a primary key) let the `FeatureEngineeringClient` look up features automatically. `score_batch` takes just the primary keys and joins the required features via `FeatureLookup` and `FeatureFunction`, keeping training and inference consistent.
# MAGIC 4. **Performance and Optimization** — Delta Lake features keep batch jobs fast: Liquid Clustering replaces partitioning/`ZORDER` for data layout, Predictive Optimization auto-runs `OPTIMIZE` and `VACUUM` on UC managed tables, and those same commands can be run manually when needed.
# MAGIC
# MAGIC Together, these give you a complete picture of batch deployment on Databricks — when to use it, how to run it with `pyfunc` and Feature Engineering, and how to keep the underlying Delta tables performant.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
