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
# MAGIC # Lecture — Introduction to Pipeline Deployment
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This lecture covers pipeline (streaming) deployment — serving a model continuously as new data arrives, instead of on a fixed batch schedule.
# MAGIC
# MAGIC This lecture covers 4 sections that build on each other:
# MAGIC
# MAGIC - **A. Pipeline / Streaming Deployment Fundamentals**. What streaming deployment is, its advantages and limitations, and the typical streaming inference workflow.
# MAGIC - **B. Lakeflow Spark Declarative Pipelines**. SDP as the declarative way to do ETL and inference on Databricks, and its building blocks — streaming tables and materialized views.
# MAGIC - **C. Pipeline Features**. Built-in data quality expectations, pipeline observability, and continuous or scheduled data ingestion.
# MAGIC - **D. Building and Running a Pipeline**. The three steps to create your first Lakeflow pipeline and add streaming inference as the final step.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. Describe pipeline deployment and identify scenarios in which this method is required.
# MAGIC 2. Describe Lakeflow Spark Declarative Pipelines as a tool to develop and manage inference pipelines.
# MAGIC 3. Explain the pipeline features that support data quality, observability, and continuous ingestion.
# MAGIC 4. Outline how to develop a simple Lakeflow Declarative Pipeline that performs streaming-based inference in its final step.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Pipeline / Streaming Deployment Fundamentals

# COMMAND ----------

# DBTITLE 1,A1. What Is Pipeline / Streaming Deployment
# MAGIC %md-sandbox
# MAGIC ### A1. What Is Pipeline / Streaming Deployment
# MAGIC
# MAGIC **Streaming deployment** means deploying machine learning models that continuously perform inference as data arrives, providing low-latency, real-time insights instead of processing data in batches.
# MAGIC
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 75" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Batch Inference</title>
# MAGIC   <defs>
# MAGIC     <marker id="arrowBatch" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto">
# MAGIC       <polygon points="0 0, 8 3.5, 0 7" fill="#1B3139"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC   <text x="20" y="50" font-size="15" font-weight="bold" fill="#1565C0">Batch</text>
# MAGIC   <rect x="120" y="25" width="110" height="42" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.2"/>
# MAGIC   <text x="174" y="51" text-anchor="middle" font-size="13" fill="#1B3139">collect</text>
# MAGIC   <line x1="230" y1="45.4" x2="252" y2="45.4" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowBatch)"/>
# MAGIC   <rect x="252" y="25" width="110" height="42" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.2"/>
# MAGIC   <text x="306" y="51" text-anchor="middle" font-size="13" fill="#1B3139">wait</text>
# MAGIC   <line x1="362" y1="45.4" x2="384" y2="45.4" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowBatch)"/>
# MAGIC   <rect x="384" y="25" width="135" height="42" rx="6" fill="#1B3139"/>
# MAGIC   <text x="450" y="51" text-anchor="middle" font-size="13" fill="#FFFFFF">score batch</text>
# MAGIC   <text x="525" y="51" font-size="15" fill="#607D8B">&#8594; on a schedule</text>
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 100" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Streaming Inference</title>
# MAGIC   <text x="20" y="60" font-size="15" font-weight="bold" fill="#E65100">Streaming</text>
# MAGIC   <rect x="125" y="35" width="400" height="42" rx="6" fill="#FFF3E0" stroke="#F57C00" stroke-width="1.2"/>
# MAGIC   <text x="330" y="60" text-anchor="middle" font-size="13" fill="#1B3139">score each record continuously as it arrives</text>
# MAGIC   <text x="535" y="60" font-size="15" fill="#E65100">&#8594; low latency, continuous</text>
# MAGIC </svg>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# DBTITLE 1,A2. Advantages and Limitations
# MAGIC %md-sandbox
# MAGIC ### A2. Advantages and Limitations
# MAGIC
# MAGIC Streaming deployment buys fresher predictions than batch, at the cost of more complexity and compute. It sits between batch and true real-time serving.
# MAGIC
# MAGIC </br>
# MAGIC
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
# MAGIC       <li><strong>Lower latency</strong> predictions</li>
# MAGIC       <li>Generate predictions and <strong>act sooner</strong></li>
# MAGIC       <li><strong>Event-driven</strong> architecture; enables systems to adapt quickly</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC   <div class="ds-card coral">
# MAGIC     <div class="dd-head">LIMITATIONS</div>
# MAGIC     <ul>
# MAGIC       <li>More <strong>costly</strong> than a batch solution</li>
# MAGIC       <li>More <strong>complicated</strong> to develop, maintain, and monitor</li>
# MAGIC       <li>Less throughput than batch</li>
# MAGIC       <li><strong>Resource intensiveness</strong> — computational power to process data</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     Streaming deployment provides faster predictions than batch, but is not intended for applications needing true sub-second (real-time) inference. For those, use a real-time serving endpoint.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,A3. The Streaming Inference Workflow
# MAGIC %md-sandbox
# MAGIC ### A3. The Streaming Inference Workflow
# MAGIC
# MAGIC The streaming workflow mirrors the batch workflow, with one key difference: instead of a scheduled job scoring a fixed batch, the inference step is **continuously triggered as new data arrives** from a Lakeflow SDP pipeline or other streaming sources.
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 880 320" role="img" style="font-family: sans-serif;">
# MAGIC   <title>A Typical Streaming Model Deployment Workflow</title>
# MAGIC
# MAGIC   <!-- Build model -->
# MAGIC   <rect x="15" y="30" width="150" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="90" y="50" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Delta Lake /</text>
# MAGIC   <text x="90" y="68" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Feature Store</text>
# MAGIC
# MAGIC   <rect x="15" y="120" width="150" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="90" y="142" text-anchor="middle" font-size="13" font-weight="bold" fill="#1B3139">Model Training</text>
# MAGIC   <text x="90" y="158" text-anchor="middle" font-size="11" fill="#1B3139">TF, scikit-learn, XGBoost</text>
# MAGIC
# MAGIC   <rect x="205" y="120" width="150" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="280" y="142" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Models in</text>
# MAGIC   <text x="280" y="159" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Unity Catalog</text>
# MAGIC
# MAGIC   <!-- Dashed continuous region -->
# MAGIC   <rect x="390" y="20" width="475" height="285" rx="12" fill="none" stroke="#7B1FA2" stroke-width="1.8" stroke-dasharray="7,5"/>
# MAGIC   <text x="627" y="42" text-anchor="middle" font-size="12" font-weight="bold" fill="#6A1B9A">Continuous triggering as new data arrives</text>
# MAGIC
# MAGIC   <!-- Streaming sources -->
# MAGIC   <rect x="410" y="60" width="130" height="60" rx="8" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="475" y="85" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Lakeflow SDP</text>
# MAGIC   <text x="475" y="107" text-anchor="middle" font-size="10" font-weight="bold" fill="#2E7D32">New Data</text>
# MAGIC
# MAGIC   <rect x="560" y="60" width="130" height="60" rx="8" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="625" y="82" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Other Streaming</text>
# MAGIC   <text x="625" y="97" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Sources</text>
# MAGIC   <text x="625" y="113" text-anchor="middle" font-size="10" font-weight="bold" fill="#2E7D32">New Data</text>
# MAGIC
# MAGIC   <!-- Streaming inference -->
# MAGIC   <rect x="470" y="165" width="160" height="70" rx="8" fill="#FFF8E1" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="550" y="195" text-anchor="middle" font-size="13" font-weight="bold" fill="#E65100">Streaming Inference</text>
# MAGIC   <text x="550" y="217" text-anchor="middle" font-size="12" fill="#1B3139" font-family="monospace">pyfunc.predict</text>
# MAGIC
# MAGIC   <!-- Downstream -->
# MAGIC   <rect x="690" y="140" width="160" height="40" rx="6" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.3"/>
# MAGIC   <text x="700" y="164" font-size="12" font-weight="bold" fill="#1B3139">Data Lake / Database</text>
# MAGIC   <rect x="690" y="190" width="160" height="40" rx="6" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.3"/>
# MAGIC   <text x="700" y="214" font-size="11" fill="#607D8B">Any downstream consumer</text>
# MAGIC
# MAGIC   <!-- Arrows -->
# MAGIC   <line x1="90" y1="85" x2="90" y2="120" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowP"/>
# MAGIC   <line x1="90" y1="120" x2="90" y2="100" stroke="#1B3139" stroke-width="0" />
# MAGIC   <line x1="165" y1="147" x2="205" y2="147" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowP)"/>
# MAGIC   <line x1="355" y1="147" x2="470" y2="190" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowP)"/>
# MAGIC   <line x1="475" y1="120" x2="530" y2="165" stroke="#2E7D32" stroke-width="1.5" marker-end="url(#arrowPg)"/>
# MAGIC   <line x1="625" y1="120" x2="575" y2="165" stroke="#2E7D32" stroke-width="1.5" marker-end="url(#arrowPg)"/>
# MAGIC   <path d="M630 192 C660 192, 665 160, 690 160" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowP)"/>
# MAGIC   <path d="M630 200 C660 200, 665 210, 690 210" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowP)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowP" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#1B3139"/></marker>
# MAGIC     <marker id="arrowPg" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#2E7D32"/></marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Lakeflow Spark Declarative Pipelines

# COMMAND ----------

# DBTITLE 1,B1. SDP — The Declarative Way to Build Pipelines
# MAGIC %md-sandbox
# MAGIC ### B1. SDP — The Declarative Way to Build Pipelines
# MAGIC
# MAGIC **Lakeflow Spark Declarative Pipelines (SDP)** is the declarative way to do ETL and inference on the Databricks Data Intelligence Platform. You declare the tables you want in **SQL or Python**, and SDP automatically orchestrates the DAG, handles retries, and manages changing data.
# MAGIC
# MAGIC </br>
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; gap: 24px; align-items: flex-start;">
# MAGIC
# MAGIC <div style="flex: 1;">
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>CREATE STREAMING TABLE raw_data
# MAGIC AS SELECT * FROM STREAM
# MAGIC   read_files('/raw_data', format => 'json');
# MAGIC </br>
# MAGIC CREATE MATERIALIZED VIEW clean_data
# MAGIC AS SELECT ...
# MAGIC FROM raw_data</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <div style="flex: 1;">
# MAGIC <ul style="margin: 0; padding-left: 18px; line-height: 1.7;">
# MAGIC   <li><strong>Accelerate ETL development</strong> — declare SQL or Python and SDP orchestrates the DAG, handles retries and changing data.</li>
# MAGIC   <li><strong>Automatically manage your infrastructure</strong> — recovery, auto-scaling, and performance optimization.</li>
# MAGIC   <li><strong>Ensure high data quality</strong> — built-in quality controls, testing, monitoring, and enforcement.</li>
# MAGIC   <li><strong>Unify batch and streaming</strong> — the simplicity of SQL with the freshness of streaming, in one unified API.</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,B2. Streaming Tables and Materialized Views
# MAGIC %md-sandbox
# MAGIC ### B2. Streaming Tables and Materialized Views
# MAGIC
# MAGIC **Streaming tables** and **materialized views** are the building blocks of a Lakeflow pipeline. Both are a kind of **dataset** — defined by a SQL query and created and kept up to date by a pipeline.
# MAGIC
# MAGIC - A **streaming table** ingests and processes new records incrementally as they arrive — ideal for raw ingestion and streaming inference.
# MAGIC - A **materialized view** stores the precomputed result of a query and refreshes as its inputs change — ideal for transformations and aggregations.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; gap: 24px; align-items: flex-start;">
# MAGIC
# MAGIC <div style="flex: 1;">
# MAGIC
# MAGIC **A Dataset is:**
# MAGIC - Defined by a **SQL query**
# MAGIC - Created and kept **up-to-date** by a pipeline
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>CREATE MATERIALIZED VIEW report
# MAGIC AS SELECT sum(profit)
# MAGIC FROM prod.sales</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <div style="flex: 1; border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px;">
# MAGIC <strong style="color: #0d47a1;">Lakeflow pipelines provide tools to:</strong>
# MAGIC <ul style="margin: 10px 0 0 0; padding-left: 20px; line-height: 1.9;">
# MAGIC   <li><strong>Manage</strong> dependencies</li>
# MAGIC   <li><strong>Control</strong> quality</li>
# MAGIC   <li><strong>Automate</strong> operations</li>
# MAGIC   <li><strong>Simplify</strong> collaboration</li>
# MAGIC   <li><strong>Save</strong> costs</li>
# MAGIC   <li><strong>Reduce</strong> latency</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Pipeline Features

# COMMAND ----------

# DBTITLE 1,C1. Data Quality Validation and Monitoring
# MAGIC %md-sandbox
# MAGIC ### C1. Data Quality Validation and Monitoring
# MAGIC
# MAGIC Lakeflow SDP lets you define **data quality and integrity controls** directly in the pipeline using **expectations**. Each expectation is a constraint with a policy for what to do when a row violates it: **warn** (retain the row), **drop** the row, or **fail** the pipeline. All pipeline runs and quality metrics are captured, tracked, and reported.
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>-- Stage 1: Bronze table — drop invalid rows
# MAGIC CREATE OR REFRESH STREAMING TABLE fire_account_bronze (
# MAGIC   CONSTRAINT valid_account_open_dt
# MAGIC     EXPECT (
# MAGIC       account_open_dt IS NOT NULL
# MAGIC       AND account_close_dt > account_open_dt
# MAGIC     )
# MAGIC     ON VIOLATION DROP ROW
# MAGIC )
# MAGIC COMMENT "Bronze table with valid account IDs"
# MAGIC AS
# MAGIC SELECT * FROM STREAM(fire_account_raw);</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;"><strong>The Three Policies:</strong>
# MAGIC     <ul style="margin: 8px 0 0 0; padding-left: 20px;">
# MAGIC       <li><strong>WARN</strong>: Keep the row and record the violation.</li>
# MAGIC       <li><strong>DROP ROW</strong>: Discard the invalid row.</li>
# MAGIC       <li><strong>FAIL UPDATE</strong>: Stop the pipeline.</li>
# MAGIC     </ul>
# MAGIC     The Data Quality dashboard reports records processed, written, and dropped per expectation.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,C2. Data Pipeline Observability
# MAGIC %md-sandbox
# MAGIC ### C2. Data Pipeline Observability
# MAGIC
# MAGIC Lakeflow SDP gives you visibility into how a pipeline runs and how data flows through it — essential for operating an inference pipeline in production.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 900px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Capability</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">What it provides</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Lineage diagram</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">High-quality, high-fidelity view of how data flows through the pipeline, for impact analysis.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Granular logging</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Operational, governance, quality, and status logging down to the row level.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Monitoring</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Continuously monitor pipeline jobs to ensure continued operation.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Notifications</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Alerting on pipeline events using Databricks SQL.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# DBTITLE 1,C3. Continuous or Scheduled Data Ingestion
# MAGIC %md-sandbox
# MAGIC ### C3. Continuous or Scheduled Data Ingestion
# MAGIC
# MAGIC A streaming inference pipeline needs a reliable way to pick up new data. Lakeflow SDP ingests files **incrementally and efficiently as they arrive** in cloud storage using **Auto Loader**, and it can run either continuously or on a schedule.
# MAGIC
# MAGIC - **Incrementally** and efficiently process new data files as they arrive in cloud storage using **Auto Loader**.
# MAGIC - Automatically **infer schema** of incoming files, or superimpose what you know with **schema hints**.
# MAGIC - Automatic **schema evolution** — supported for JSON, CSV, Avro, and Parquet.
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>-- Simple SQL syntax for streaming ingestion
# MAGIC CREATE STREAMING TABLE sales_orders_raw
# MAGIC COMMENT "The raw sales orders, ingested from cloud storage."
# MAGIC AS SELECT * FROM STREAM
# MAGIC   read_files('/databricks-datasets/retail-org/sales_orders/', format => 'json');</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     Auto Loader powers incremental file ingestion in Lakeflow SDP. The current SQL syntax uses <code>read_files(...)</code> inside a <code>STREAM</code> source; older examples may reference the legacy <code>cloud_files(...)</code> function.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Building and Running a Pipeline

# COMMAND ----------

# DBTITLE 1,D1. Creating Your First Lakeflow Pipeline
# MAGIC %md-sandbox
# MAGIC ### D1. Creating Your First Lakeflow Pipeline
# MAGIC
# MAGIC Going from SQL to a running Lakeflow pipeline takes three steps.
# MAGIC
# MAGIC </br>
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .ds-row { display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 240px; }
# MAGIC .ds-card { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid var(--accent, #4299E0); }
# MAGIC .blue{--accent:#4299E0;} .green{--accent:#00A972;} .coral{--accent:#FF5F46;} .amber{--accent:#FFAB00;} .red{--accent:#98102A;}
# MAGIC .ds-card-title { font-size: 14pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
# MAGIC .ds-card-text { font-size: 12pt; color: #5E7077; line-height: 1.55; margin: 0; }
# MAGIC .ds-card ul, .ds-card ol { margin: 8px 0 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-card li { margin-bottom: 10px; }
# MAGIC .ds-card li:last-child { margin-bottom: 0; }
# MAGIC .tc { text-align: center; }
# MAGIC .ds-card-label { font-size: 14pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
# MAGIC .ds-card-para { font-size: 14pt; color: #0b2026; line-height: 1.55; margin: 0; }
# MAGIC </style>
# MAGIC
# MAGIC <div class="ds-row">
# MAGIC   <div class="ds-card blue">
# MAGIC     <div class="ds-card-label">Step One</div>
# MAGIC     <div class="ds-card-title">Write Definitions</div>
# MAGIC     <div class="ds-card-para">Write your streaming table / materialized view definitions (but do not run them) in notebooks or source files. Git folders let you version-control them.</div>
# MAGIC   </div>
# MAGIC   <div class="ds-card green">
# MAGIC     <div class="ds-card-label">Step Two</div>
# MAGIC     <div class="ds-card-title">Create a Pipeline</div>
# MAGIC     <div class="ds-card-para">A pipeline picks one or more source files of table definitions, plus any required configuration.</div>
# MAGIC   </div>
# MAGIC   <div class="ds-card amber">
# MAGIC     <div class="ds-card-label">Step Three</div>
# MAGIC     <div class="ds-card-title">Click Start</div>
# MAGIC     <div class="ds-card-para">Lakeflow SDP will create or update all the tables in the pipeline.</div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>CREATE MATERIALIZED VIEW daily_stats
# MAGIC AS SELECT sum(rev) - sum(costs) AS profits
# MAGIC FROM prod_data.transactions
# MAGIC GROUP BY day</code>
# MAGIC </pre>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,D2. Streaming Inference as the Final Step
# MAGIC %md-sandbox
# MAGIC ### D2. Streaming Inference as the Final Step
# MAGIC
# MAGIC To turn an ETL pipeline into an **inference pipeline**, make the final dataset a streaming table (or materialized view) whose query applies the model. You load the registered model from Unity Catalog as a Spark UDF and call it inside the pipeline's final table definition — so every new record is scored as it flows through.
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>import dlt
# MAGIC import mlflow
# MAGIC from pyspark.sql.functions import struct
# MAGIC </br>
# MAGIC <strong># Load the registered model from Unity Catalog as a Spark UDF</strong>
# MAGIC mlflow.set_registry_uri("databricks-uc")
# MAGIC predict_udf = mlflow.pyfunc.spark_udf(
# MAGIC     spark, "models:/main.ml_models.churn_model@champion"
# MAGIC )
# MAGIC </br>
# MAGIC <strong># Final pipeline step: score each record as it streams in</strong>
# MAGIC @dlt.table(name="churn_predictions")
# MAGIC def churn_predictions():
# MAGIC     features = dlt.read_stream("clean_data")
# MAGIC     return features.withColumn("prediction", predict_udf(struct("*")))
# MAGIC </code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:14pt; line-height:1.55;">
# MAGIC     The streaming inference pattern lets you use the same <code>pyfunc</code> model for both batch and streaming pipelines. By applying the model UDF in the final step, every new record is scored automatically as it arrives, enabling real-time predictions and seamless integration with upstream data cleaning and transformation steps.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,Conclusion
# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lecture, you covered pipeline (streaming) deployment on Databricks:
# MAGIC
# MAGIC 1. **Pipeline / Streaming Deployment Fundamentals** — Streaming deployment continuously performs inference as data arrives, providing lower latency than batch and enabling event-driven systems to act sooner. It is more costly, more complex, and lower-throughput than batch, and it is not meant for true sub-second real-time predictions.
# MAGIC 2. **Lakeflow Spark Declarative Pipelines** — SDP is the declarative way to do ETL and inference: you declare tables in SQL or Python and SDP orchestrates the DAG, manages infrastructure, and unifies batch and streaming. Its building blocks are streaming tables and materialized views — datasets defined by a query and kept up to date by a pipeline.
# MAGIC 3. **Pipeline Features** — Expectations enforce data quality with warn/drop/fail policies; lineage, logging, monitoring, and notifications provide observability; and Auto Loader ingests new files incrementally with schema inference and evolution.
# MAGIC 4. **Building and Running a Pipeline** — Write table definitions, create a pipeline from them, and click start. Making the final step a table whose query applies a `pyfunc` model UDF turns the pipeline into a streaming inference pipeline.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
