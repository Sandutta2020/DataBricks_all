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
# MAGIC # Lecture — Introduction to Real-Time Deployment
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This lecture covers real-time deployment — serving a model behind a live API that returns predictions instantly, one request at a time. 
# MAGIC
# MAGIC This lecture covers 4 sections that build on each other:
# MAGIC
# MAGIC - **A. Real-time Deployment Fundamentals**. What real-time deployment is, why Gen AI is making it increasingly common, and a typical fraud-detection use case.
# MAGIC - **B. The Real-time Deployment Workflow**. The path from a registered model to a live serving endpoint, and the role of the online feature store for low-latency feature lookups.
# MAGIC - **C. Challenges of Real-time ML Systems**. The three reasons most real-time ML models never reach production — hard infrastructure, disparate tools, and scarce expertise.
# MAGIC - **D. Databricks Model Serving**. How Model Serving delivers production-grade, unified, and simplified serving that addresses those challenges.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. Describe real-time deployment and identify scenarios in which this method is required.
# MAGIC 2. Discuss the challenges of real-time deployment systems.
# MAGIC 3. Explain how Databricks Model Serving addresses those challenges.
# MAGIC 4. Describe the features of Databricks Model Serving.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Real-time Deployment Fundamentals

# COMMAND ----------

# DBTITLE 1,A1. What Is Real-time Deployment
# MAGIC %md-sandbox
# MAGIC ### A1. What Is Real-time Deployment
# MAGIC
# MAGIC **Real-time deployment** is the process of deploying and serving machine learning models in a production environment where **predictions are generated instantly** in response to incoming data or requests. It is crucial for applications that require **low-latency responses**, such as fraud detection, autonomous systems, and other time-sensitive tasks.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 150" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Real-time Request/Response</title>
# MAGIC
# MAGIC   <!-- Client -->
# MAGIC   <rect x="30" y="50" width="180" height="60" rx="10" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="120" y="78" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Application</text>
# MAGIC   <text x="120" y="98" text-anchor="middle" font-size="12" fill="#1B3139">sends a single request</text>
# MAGIC
# MAGIC   <!-- Endpoint -->
# MAGIC   <rect x="340" y="50" width="180" height="60" rx="10" fill="#1B3139"/>
# MAGIC   <text x="430" y="78" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">Serving Endpoint</text>
# MAGIC   <text x="430" y="98" text-anchor="middle" font-size="12" fill="#F9F7F4">scores instantly</text>
# MAGIC
# MAGIC   <!-- Response -->
# MAGIC   <rect x="650" y="50" width="180" height="60" rx="10" fill="#E8F5E9" stroke="#388E3C" stroke-width="2"/>
# MAGIC   <text x="740" y="78" text-anchor="middle" font-size="14" font-weight="bold" fill="#2E7D32">Prediction</text>
# MAGIC   <text x="740" y="98" text-anchor="middle" font-size="12" fill="#1B3139">returned in milliseconds</text>
# MAGIC
# MAGIC   <line x1="210" y1="72" x2="340" y2="72" stroke="#1B3139" stroke-width="2" marker-end="url(#arrowR1)"/>
# MAGIC   <text x="275" y="65" text-anchor="middle" font-size="12" font-weight="bold"  fill="#607D8B">request</text>
# MAGIC   <line x1="520" y1="88" x2="650" y2="88" stroke="#388E3C" stroke-width="2" marker-end="url(#arrowR1g)"/>
# MAGIC   <text x="585" y="105" text-anchor="middle" font-size="12" font-weight="bold" fill="#607D8B">response</text>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowR1" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" fill="#1B3139"/></marker>
# MAGIC     <marker id="arrowR1g" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" fill="#388E3C"/></marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">With the emergence of new Gen AI applications, this deployment method is becoming increasingly common — especially as large language models need to be served in real-time.</div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,A2. A Typical Real-time Use Case
# MAGIC %md-sandbox
# MAGIC ### A2. A Typical Real-time Use Case
# MAGIC
# MAGIC **Description:** Real-time fraud detection in online banking.
# MAGIC
# MAGIC **Scenario:**
# MAGIC - A pre-trained machine learning model, specifically designed for fraud detection, is deployed in the real-time environment.
# MAGIC - The model provides immediate predictions over a **REST API**.
# MAGIC - An immediate decision is made to flag the transaction.
# MAGIC
# MAGIC **Requirements:** low latency, immediate action, 24/7 uptime, continuous monitoring.
# MAGIC
# MAGIC <div style="border-left: 4px solid #FFAB00; background: rgba(255,171,0,0.12); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#0b2026; margin-bottom:6px; font-size:15pt;">Warning</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">A transaction must be approved or declined <em>while the customer waits</em> — a batch or streaming job that scores minutes later is useless. The prediction has to come back in milliseconds, every time, around the clock.</div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. The Real-time Deployment Workflow

# COMMAND ----------

# DBTITLE 1,B1. From Registered Model to Serving Endpoint
# MAGIC %md-sandbox
# MAGIC ### B1. From Registered Model to Serving Endpoint
# MAGIC
# MAGIC The real-time workflow shares its first stages with batch and streaming — data, training, and registration in Unity Catalog — but the model is deployed to a live **Serving Endpoint** (Databricks Model Serving). A downstream application sends a **query payload** and gets a **response** back in milliseconds. For features that aren't in the request, the endpoint looks them up from an **online feature store**.
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 880 320" role="img" style="font-family: sans-serif;">
# MAGIC   <title>A Typical Real-time Model Deployment Workflow</title>
# MAGIC
# MAGIC   <!-- Source -->
# MAGIC   <rect x="15" y="30" width="150" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="90" y="50" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Delta Lake /</text>
# MAGIC   <text x="90" y="68" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Feature Store</text>
# MAGIC
# MAGIC   <rect x="15" y="120" width="150" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="90" y="142" text-anchor="middle" font-size="13" font-weight="bold" fill="#1B3139">Model Training</text>
# MAGIC   <text x="90" y="158" text-anchor="middle" font-size="11" fill="#1B3139">TF, scikit-learn, XGBoost</text>
# MAGIC
# MAGIC   <rect x="195" y="120" width="150" height="55" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="270" y="138" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Models in</text>
# MAGIC   <text x="270" y="152" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Unity Catalog</text>
# MAGIC   <text x="270" y="164" text-anchor="middle" font-size="11" fill="#1B3139">mlflow</text>
# MAGIC
# MAGIC   <!-- Serving endpoint -->
# MAGIC   <rect x="380" y="112" width="170" height="72" rx="8" fill="#FFF8E1" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="465" y="140" text-anchor="middle" font-size="13" font-weight="bold" fill="#E65100">Serving Endpoint</text>
# MAGIC   <text x="465" y="162" text-anchor="middle" font-size="11" fill="#1B3139">Databricks Model Serving</text>
# MAGIC
# MAGIC   <!-- Online feature store -->
# MAGIC   <rect x="550" y="12" width="140" height="58" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="620" y="34" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565C0">Online Feature Store</text>
# MAGIC   <text x="620" y="50" text-anchor="middle" font-size="9" fill="#607D8B">Databricks Online Feature</text>
# MAGIC   <text x="620" y="62" text-anchor="middle" font-size="9" fill="#607D8B">Store, on Lakebase</text>
# MAGIC
# MAGIC   <!-- Downstream app -->
# MAGIC   <rect x="690" y="112" width="170" height="72" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="775" y="140" text-anchor="middle" font-size="13" font-weight="bold" fill="#1B3139">Downstream App</text>
# MAGIC   <text x="775" y="162" text-anchor="middle" font-size="11" fill="#607D8B">web app, mobile app</text>
# MAGIC
# MAGIC   <!-- Monitoring -->
# MAGIC   <rect x="395" y="240" width="140" height="45" rx="8" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.3"/>
# MAGIC   <text x="465" y="267" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Monitoring</text>
# MAGIC
# MAGIC   <!-- Arrows -->
# MAGIC   <line x1="90" y1="85" x2="90" y2="120" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowR2)"/>
# MAGIC   <line x1="165" y1="147" x2="195" y2="147" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowR2)"/>
# MAGIC   <line x1="345" y1="147" x2="380" y2="147" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowR2)"/>
# MAGIC
# MAGIC   <!-- Query payload / response between app and endpoint -->
# MAGIC   <line x1="690" y1="138" x2="550" y2="138" stroke="#7B1FA2" stroke-width="1.8" marker-end="url(#arrowR2p)"/>
# MAGIC   <text x="620" y="131" text-anchor="middle" font-size="10" fill="#6A1B9A" font-weight="bold">Query payload</text>
# MAGIC   <line x1="550" y1="164" x2="690" y2="164" stroke="#3949AB" stroke-width="1.8" marker-end="url(#arrowR2b)"/>
# MAGIC   <text x="620" y="180" text-anchor="middle" font-size="10" fill="#3949AB" font-weight="bold">Response</text>
# MAGIC
# MAGIC   <!-- Endpoint -> monitoring -->
# MAGIC   <line x1="465" y1="184" x2="465" y2="240" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowR2)"/>
# MAGIC
# MAGIC   <!-- S-curve: query payload arrowhead <-> bottom of online feature store (styled like slide reference) -->
# MAGIC   <!-- From the Online Feature Store to the Query Payload -->
# MAGIC   <path d="M620,70 C620,106 561,102 563,130" fill="none" stroke="#38a3c3" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="butt" stroke-dasharray="6,4"  marker-end="url(#arrowR2teal)"/>
# MAGIC   <!-- From the Query Payload Online to the Feature Store -->
# MAGIC   <path d="M563,130 C561,102 620,106 620,70" fill="none" stroke="#38a3c3" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="butt" stroke-dasharray="6,4"  marker-end="url(#arrowR2teal)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowR2" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#1B3139"/></marker>
# MAGIC     <marker id="arrowR2p" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#7B1FA2"/></marker>
# MAGIC     <marker id="arrowR2b" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#3949AB"/></marker>
# MAGIC     <marker id="arrowR2blue" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#1976D2"/></marker>
# MAGIC     <marker id="arrowR2teal" markerWidth="7" markerHeight="6" refX="6" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#38a3c3"/></marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">For real-time serving, features must be available in milliseconds. To achieve this, precomputed features are published to the <strong>Databricks Online Feature Store</strong>, which is powered by <strong>Lakebase</strong> (serverless Postgres). The serving endpoint retrieves features from the online store at request time, instead of scanning offline Delta tables. Online feature stores are demonstrated in the demo and lab for this module.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Challenges of Real-time ML Systems

# COMMAND ----------

# DBTITLE 1,C1. Why Most ML Models Don't Reach Production
# MAGIC %md-sandbox
# MAGIC ### C1. Why Most ML Models Don't Reach Production
# MAGIC
# MAGIC Most ML models never make it into production. Building a real-time ML system runs into three recurring challenges — the reason a serving platform is worth having.
# MAGIC
# MAGIC Most ML models fail to reach production for three key reasons:
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">1. ML infrastructure is hard</summary>
# MAGIC
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC Real-time ML systems require fast and scalable serving infrastructure, which is costly to build and maintain. Teams must handle:
# MAGIC
# MAGIC <ul>
# MAGIC   <li>Low-latency networking and load balancing</li>
# MAGIC   <li>Auto-scaling to handle traffic spikes</li>
# MAGIC   <li>High availability and fault tolerance</li>
# MAGIC   <li>GPU provisioning and optimization</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC 2. Deploying real-time models needs disparate tools</summary>
# MAGIC
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC Data teams use diverse tools to develop models, and customers use separate platforms for data, ML, and serving — adding complexity and cost:
# MAGIC
# MAGIC <ul>
# MAGIC   <li>Different frameworks for training vs. serving</li>
# MAGIC   <li>Separate platforms for data engineering, ML, and deployment</li>
# MAGIC   <li>Fragmented monitoring and governance across tools</li>
# MAGIC   <li>Inconsistent feature computation between offline and online</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </details>
# MAGIC <details style="margin: 16px 0;">
# MAGIC
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">3. Operating production ML requires expert resources</summary>
# MAGIC
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC A steep learning curve for deployment tools means model deployment is bottlenecked by limited engineering resources, limiting the ability to scale AI:
# MAGIC
# MAGIC <ul>
# MAGIC   <li>MLOps expertise is scarce and expensive</li>
# MAGIC   <li>Each serving framework has its own learning curve</li>
# MAGIC   <li>Debugging production issues requires cross-domain knowledge</li>
# MAGIC   <li>Ongoing maintenance competes with new model development</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     The main barriers to real-time ML are not the models themselves, but the infrastructure, tool fragmentation, and specialized skills required to operate them. A managed serving platform removes these obstacles, making production deployment faster and easier.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Databricks Model Serving

# COMMAND ----------

# DBTITLE 1,D1. How Model Serving Addresses These Challenges
# MAGIC %md-sandbox
# MAGIC ### D1. How Model Serving Addresses These Challenges
# MAGIC
# MAGIC **Databricks Model Serving** lets you integrate your model into your websites and applications as an API. It directly answers the three challenges: managed infrastructure, one unified platform, and simplified deployment.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 900px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Capability</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">What it provides</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Challenge it solves</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Production-Grade Serving</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;"><strong>Highly available</strong>, low latency, scalable serving that works for small and large workloads.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">ML infrastructure is hard</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Unified Serving on the Data Intelligence Platform</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Automatic feature lookups, monitoring, and unified governance that <strong>automates deployment</strong> and reduces errors.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Disparate tools</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Simplified Deployment</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Simple and flexible deployment through the <strong>UI or API</strong>.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Requires expert resources</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     Databricks Model Serving is serverless by design, automatically scaling with traffic—including scale-to-zero—so you get production-grade, low-latency endpoints without managing infrastructure. This managed platform removes barriers like complex infrastructure, fragmented tools, and specialized skills, making real-time deployment fast and easy. Deeper features and hands-on deployment are covered in the next lecture.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,Conclusion
# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lecture, you covered the fundamentals of real-time deployment:
# MAGIC
# MAGIC 1. **Real-time Deployment Fundamentals** — Real-time deployment serves models in a production environment where predictions are generated instantly in response to requests, crucial for low-latency applications like fraud detection and autonomous systems — and increasingly common as Gen AI and LLMs need to be served in real-time.
# MAGIC 2. **The Real-time Deployment Workflow** — A registered model in Unity Catalog is deployed to a live serving endpoint. Applications send a query payload and receive a response in milliseconds; features not in the request are looked up from the online feature store (Databricks Online Feature Store, on Lakebase), and the endpoint is continuously monitored.
# MAGIC 3. **Challenges of Real-time ML Systems** — Most ML models never reach production because ML infrastructure is hard and costly, deploying real-time models needs disparate tools, and operating production ML requires expert resources that bottleneck deployment.
# MAGIC 4. **Databricks Model Serving** — Model Serving addresses all three with production-grade serving (highly available, low latency, scalable), unified serving on the Data Intelligence Platform (automatic feature lookups, monitoring, governance), and simplified deployment through the UI or API.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
