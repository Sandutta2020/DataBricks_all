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
# MAGIC # Lecture — Databricks Model Serving
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This lecture goes deep on **Databricks Model Serving** — the managed platform for serving models as real-time REST APIs. 
# MAGIC
# MAGIC This lecture covers 4 sections that build on each other:
# MAGIC
# MAGIC - **A. Databricks Model Serving Overview**. The unified UI, API, and SDK for serving all types of AI models, and the core features that support real-time production workloads.
# MAGIC - **B. Serving Infrastructure**. Serverless compute with fast autoscaling and scale-to-zero, and native MLflow integration for a fast path to production.
# MAGIC - **C. Deploying and Managing Endpoints**. The endpoint-centric workflow — serving via UI or API, traffic splitting for A/B testing, serving custom models, monitoring, and the Endpoint API for CI/CD.
# MAGIC - **D. Online Feature Store and Automated Lookups**. Automatic feature and vector lookups, the online feature store on Lakebase, and feature functions for on-demand features.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. Describe the features of Databricks Model Serving.
# MAGIC 2. Serve a model with Model Serving using the UI and the API.
# MAGIC 3. Serve multiple model versions to a serving endpoint by splitting the incoming traffic.
# MAGIC 4. Serve a custom model with Databricks Model Serving, and explain how the online feature store enables automated lookups.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Databricks Model Serving Overview

# COMMAND ----------

# DBTITLE 1,A1. A Unified Platform for All AI Models
# MAGIC %md-sandbox
# MAGIC ### A1. A Unified Platform for All AI Models
# MAGIC
# MAGIC **Databricks Model Serving** is a unified UI, API, and SDK for managing all types of AI models. A single interface serves three categories of model.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 900px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Model type</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Custom Models</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Deploy any model as a REST API with serverless compute, managed via MLflow — on CPU and GPU, with integration to Feature Engineering and Vector Search.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Foundation Models APIs</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Databricks curates top foundation models and provides them behind simple APIs, so you can start experimentation immediately without setting up serving yourself.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">External Models</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Govern external models and APIs (e.g., OpenAI, Anthropic, AI21) through the Unity AI Gateway, plus monitoring and payload logging for Databricks Model Serving.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">For this course, this module focuses on serving <strong>custom models</strong> — your own trained models registered in Unity Catalog. Foundation Model APIs and External Models are governed through the same platform and Unity AI Gateway.
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# DBTITLE 1,A2. Core Features of Model Serving
# MAGIC %md-sandbox
# MAGIC ### A2. Core Features of Model Serving
# MAGIC
# MAGIC Model Serving is built to support real-time production ML workloads. Its features group into three themes.
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">1. Real Time</summary>
# MAGIC
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC Model Serving is built for low-latency, high-availability production workloads:
# MAGIC
# MAGIC <ul>
# MAGIC   <li><strong>Low overhead latency:</strong> &lt;100ms</li>
# MAGIC   <li><strong>Throughput:</strong> 3K+ QPS</li>
# MAGIC   <li><strong>Availability:</strong> 99.9%</li>
# MAGIC   <li><strong>Scalable:</strong> automatically scales up/down for bursty traffic</li>
# MAGIC   <li><strong>Secure:</strong> PrivateLink and IP allowlist</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">2. Unified on the Data Intelligence Platform</summary>
# MAGIC
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC Model Serving is deeply integrated with the Databricks platform for a seamless workflow:
# MAGIC
# MAGIC <ul>
# MAGIC   <li><strong>Feature store integrated:</strong> automated feature/vector lookups</li>
# MAGIC   <li><strong>MLflow integrated:</strong> fast, easy model deployment</li>
# MAGIC   <li><strong>Quality &amp; diagnostics:</strong> built-in metrics, integrated with monitoring</li>
# MAGIC   <li><strong>Unified governance:</strong> manage data &amp; AI with Unity Catalog</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">3. Simplified Deployment</summary>
# MAGIC
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC Model Serving removes complexity from the deployment process:
# MAGIC
# MAGIC <ul>
# MAGIC   <li><strong>Simple:</strong> endpoints via UI and API</li>
# MAGIC   <li><strong>CPU and GPU support</strong></li>
# MAGIC   <li><strong>Flexible:</strong> traffic splitting for staged roll-out and A/B testing</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Serving Infrastructure

# COMMAND ----------

# DBTITLE 1,B1. Serverless Compute
# MAGIC %md-sandbox
# MAGIC ### B1. Serverless Compute
# MAGIC
# MAGIC For operational ML use cases that need to be on 24/7, Model Serving provides out-of-the-box autoscaling on **serverless compute** — quickly scaling up and down to handle bursty traffic.
# MAGIC
# MAGIC - **GPU Support:** deploy LLMs with ease.
# MAGIC - **Fast Autoscaling:** compute is managed and kept warm by Databricks, allowing rapid scaling.
# MAGIC - **Scale within workload size:** autoscale within a selected range.
# MAGIC - **Scale to zero:** save costs for use cases with predictable, non-24/7 traffic.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 700px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 16px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Workload size</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Concurrency range</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Small</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">0–4 concurrent requests (0–4 DBU)</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Medium</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">0–16 concurrent requests (0–16 DBU)</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Large</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">0–64 concurrent requests (0–64 DBU)</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">Enabling <em>Scale to zero</em> lets an endpoint drop to no running compute when idle, so you only pay when it is serving requests — ideal for predictable, non-24/7 traffic. The first request after idle incurs a cold-start delay.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,B2. MLflow Integration
# MAGIC %md-sandbox
# MAGIC ### B2. MLflow Integration
# MAGIC
# MAGIC Model Serving integrates natively with MLflow, giving a **faster path to production**: it connects directly to the model registry in Unity Catalog, so a registered model can be deployed to a REST endpoint without extra packaging.
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 880 190" role="img" style="font-family: sans-serif;">
# MAGIC   <title>MLflow to Model Serving</title>
# MAGIC
# MAGIC   <rect x="15" y="70" width="150" height="75" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="90" y="93" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">MLflow Models</text>
# MAGIC   <text x="90" y="111" text-anchor="middle" font-size="11" fill="#607D8B">Flavor 1</text>
# MAGIC   <text x="90" y="125" text-anchor="middle" font-size="11" fill="#607D8B">Flavor 2</text>
# MAGIC
# MAGIC   <rect x="205" y="70" width="150" height="75" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="280" y="93" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">MLflow Tracking</text>
# MAGIC   <text x="280" y="111" text-anchor="middle" font-size="11" fill="#607D8B">Parameters · Metrics</text>
# MAGIC   <text x="280" y="125" text-anchor="middle" font-size="11" fill="#607D8B">Artifacts · Metadata</text>
# MAGIC
# MAGIC   <rect x="395" y="65" width="180" height="85" rx="8" fill="#FFF8E1" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="485" y="85" text-anchor="middle" font-size="14" font-weight="bold" fill="#E65100">Models in Unity Catalog</text>
# MAGIC   <rect x="415" y="95" width="70" height="26" rx="13" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="1"/>
# MAGIC   <text x="450" y="112" text-anchor="middle" font-size="11" fill="#6A1B9A">@challenger</text>
# MAGIC   <rect x="490" y="95" width="70" height="26" rx="13" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1"/>
# MAGIC   <text x="525" y="112" text-anchor="middle" font-size="11" fill="#2E7D32">@champion</text>
# MAGIC
# MAGIC   <rect x="615" y="70" width="180" height="75" rx="8" fill="#1B3139"/>
# MAGIC   <text x="705" y="93" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">Model Serving</text>
# MAGIC   <text x="705" y="111" text-anchor="middle" font-size="11" fill="#F9F7F4">REST Endpoint</text>
# MAGIC   <text x="705" y="125" text-anchor="middle" font-size="11" fill="#F9F7F4">Dashboards · Applications </text>
# MAGIC
# MAGIC   <line x1="165" y1="105" x2="205" y2="105" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowMS)"/>
# MAGIC   <line x1="355" y1="105" x2="395" y2="105" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowMS)"/>
# MAGIC   <line x1="575" y1="105" x2="615" y2="105" stroke="#1B3139" stroke-width="1.5" marker-end="url(#arrowMS)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowMS" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#1B3139"/></marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     MLflow integration streamlines model deployment: once your model is registered in Unity Catalog, you can serve it directly via Databricks Model Serving. Simply select a model version or alias (like <code>@champion</code>) and deploy it to a REST endpoint—no extra packaging required. This enables rapid, reliable production workflows for dashboards and applications.
# MAGIC   </div>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Deploying and Managing Endpoints

# COMMAND ----------

# DBTITLE 1,C1. The Endpoint-Centric Workflow
# MAGIC %md-sandbox
# MAGIC ### C1. The Endpoint-Centric Workflow
# MAGIC
# MAGIC Model Serving uses an **endpoint-centric workflow** that streamlines deployment with simplicity, stability, and flexibility. You can easily create and manage serving endpoints using the UI or API.
# MAGIC
# MAGIC - **Stable Scoring URI:** provides a 1:1 mapping with a scoring URI, so client code targets a fixed address.
# MAGIC - **Flexible Deployments:** deploy multiple models behind the same endpoint, or the same model behind multiple endpoints.
# MAGIC - **Staged Rollout:** gradually roll out models to minimize risk and ensure stability.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 700 240" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Endpoint-Centric Deployment</title>
# MAGIC
# MAGIC   <!-- Models -->
# MAGIC   <rect x="20" y="20" width="150" height="34" rx="6" fill="#FFFFFF" stroke="#607D8B" stroke-width="1.3"/>
# MAGIC   <text x="95" y="42" text-anchor="middle" font-size="12" fill="#1B3139">Model A</text>
# MAGIC   <rect x="20" y="72" width="150" height="34" rx="6" fill="#FFFFFF" stroke="#607D8B" stroke-width="1.3"/>
# MAGIC   <text x="95" y="94" text-anchor="middle" font-size="12" fill="#1B3139">Model B</text>
# MAGIC   <rect x="20" y="134" width="150" height="34" rx="6" fill="#FFFFFF" stroke="#607D8B" stroke-width="1.3"/>
# MAGIC   <text x="95" y="156" text-anchor="middle" font-size="12" fill="#1B3139">Model C</text>
# MAGIC   <rect x="20" y="186" width="150" height="34" rx="6" fill="#FFFFFF" stroke="#607D8B" stroke-width="1.3"/>
# MAGIC   <text x="95" y="208" text-anchor="middle" font-size="12" fill="#1B3139">Model D</text>
# MAGIC
# MAGIC   <!-- Endpoints -->
# MAGIC   <rect x="500" y="55" width="160" height="44" rx="8" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2"/>
# MAGIC   <text x="580" y="82" text-anchor="middle" font-size="13" font-weight="bold" fill="#2E7D32">Endpoint 1</text>
# MAGIC   <rect x="500" y="140" width="160" height="44" rx="8" fill="#FFF3E0" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="580" y="167" text-anchor="middle" font-size="13" font-weight="bold" fill="#E65100">Endpoint 2</text>
# MAGIC
# MAGIC   <!-- Routes (many-to-many) -->
# MAGIC   <path d="M170 37 C330 37, 350 77, 500 77" stroke="#2E7D32" stroke-width="1.5" fill="none" marker-end="url(#arrowGreen)"/>
# MAGIC   <path d="M170 89 C330 89, 350 162, 500 162" stroke="#F57C00" stroke-width="1.5" fill="none" marker-end="url(#arrowOrange)"/>
# MAGIC   <path d="M170 148 C330 151, 350 90, 500 77" stroke="#2E7D32" stroke-width="1.5" fill="none" marker-end="url(#arrowGreen)"/>
# MAGIC   <path d="M170 203 C330 203, 350 172, 490 77" stroke="#2E7D32" stroke-width="1.5" fill="none"/>
# MAGIC   <path d="M170 158 C310 150, 300 200, 500 160" stroke="#F57C00" stroke-width="1.5" fill="none" marker-end="url(#arrowOrange)"/>
# MAGIC   
# MAGIC   <defs>
# MAGIC     <marker id="arrowGreen" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto">
# MAGIC       <polygon points="0 0, 8 3.5, 0 7" fill="#2E7D32"/>
# MAGIC     </marker>
# MAGIC     <marker id="arrowOrange" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto">
# MAGIC       <polygon points="0 0, 8 3.5, 0 7" fill="#F57C00"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,C2. A/B Testing with Traffic Splitting
# MAGIC %md-sandbox
# MAGIC ### C2. A/B Testing with Traffic Splitting
# MAGIC
# MAGIC Because an endpoint can host multiple models and **distribute traffic** among them, you can safely and securely deploy new models — performing a progressive rollout or online model validation (A/B testing). You assign each served model a percentage of incoming traffic.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 760 220" role="img" style="font-family: sans-serif;">
# MAGIC   <title>A/B Testing via Traffic Split</title>
# MAGIC
# MAGIC   <!-- Model v1 -->
# MAGIC   <rect x="20" y="30" width="220" height="50" rx="8" fill="#FFFFFF" stroke="#2E7D32" stroke-width="1.8"/>
# MAGIC   <text x="130" y="60" text-anchor="middle" font-size="14" fill="#1B3139">fraud_classifier / <tspan font-weight="bold" fill="#2E7D32">v1</tspan></text>
# MAGIC
# MAGIC   <!-- Model v2 -->
# MAGIC   <rect x="20" y="140" width="220" height="50" rx="8" fill="#FFFFFF" stroke="#F57C00" stroke-width="1.8"/>
# MAGIC   <text x="130" y="170" text-anchor="middle" font-size="14" fill="#1B3139">fraud_classifier / <tspan font-weight="bold" fill="#E65100">v2</tspan></text>
# MAGIC
# MAGIC   <!-- Traffic labels -->
# MAGIC   <rect x="330" y="45" width="120" height="28" rx="14" fill="#00A972"/>
# MAGIC   <text x="390" y="64" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">Traffic: 80%</text>
# MAGIC   <rect x="330" y="150" width="120" height="28" rx="14" fill="#F57C00"/>
# MAGIC   <text x="390" y="169" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">Traffic: 20%</text>
# MAGIC
# MAGIC   <!-- Endpoint -->
# MAGIC   <rect x="560" y="85" width="180" height="50" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="650" y="108" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Endpoint</text>
# MAGIC   <text x="650" y="125" text-anchor="middle" font-size="11" fill="#607D8B">endpoint/fraud_prod</text>
# MAGIC
# MAGIC   <!-- Arrows -->
# MAGIC   <path d="M240 55 C300 55, 450 100, 560 105" stroke="#2E7D32" stroke-width="1.8" fill="none" marker-end="url(#arrowAB)"/>
# MAGIC   <path d="M240 165 C300 165, 450 118, 560 115" stroke="#F57C00" stroke-width="1.8" fill="none" marker-end="url(#arrowABo)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowAB" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#2E7D32"/></marker>
# MAGIC     <marker id="arrowABo" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#F57C00"/></marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     Traffic splitting enables safe, real-time A/B testing of models in production. By assigning a percentage of incoming requests to each model version, you can monitor performance and validate improvements before fully rolling out a new model. Adjust traffic allocation at any time to support progressive rollout or rollback.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,C3. Serving Custom Models, Libraries, and Artifacts
# MAGIC %md-sandbox
# MAGIC ### C3. Serving Custom Models, Libraries, and Artifacts
# MAGIC
# MAGIC Model Serving supports packing models with custom artifacts, so real-world models with their own preprocessing code and dependencies serve cleanly.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 24px auto;">
# MAGIC <svg width="100%" viewBox="0 0 700 200" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Serve Custom Models</title>
# MAGIC
# MAGIC   <!-- Models -->
# MAGIC   <rect x="20" y="20" width="170" height="40" rx="6" fill="#FFFFFF" stroke="#607D8B" stroke-width="1.3"/>
# MAGIC   <text x="105" y="45" text-anchor="middle" font-size="12" fill="#1B3139">PyTorch Model</text>
# MAGIC
# MAGIC   <rect x="20" y="80" width="170" height="40" rx="6" fill="#FFFFFF" stroke="#607D8B" stroke-width="1.3"/>
# MAGIC   <text x="105" y="105" text-anchor="middle" font-size="12" fill="#1B3139">Scikit-learn Model</text>
# MAGIC
# MAGIC   <rect x="20" y="140" width="170" height="40" rx="6" fill="#FFFFFF" stroke="#607D8B" stroke-width="1.3"/>
# MAGIC   <text x="105" y="165" text-anchor="middle" font-size="12" fill="#1B3139">HuggingFace Model</text>
# MAGIC
# MAGIC   <!-- Endpoints -->
# MAGIC   <rect x="500" y="35" width="170" height="50" rx="8" fill="#E8F5E9" stroke="#2E7D32" stroke-width="2"/>
# MAGIC   <text x="585" y="58" text-anchor="middle" font-size="13" font-weight="bold" fill="#2E7D32">Endpoint 1</text>
# MAGIC   <text x="585" y="75" text-anchor="middle" font-size="10" fill="#607D8B">REST API</text>
# MAGIC
# MAGIC   <rect x="500" y="120" width="170" height="50" rx="8" fill="#FFF3E0" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="585" y="143" text-anchor="middle" font-size="13" font-weight="bold" fill="#E65100">Endpoint 2</text>
# MAGIC   <text x="585" y="160" text-anchor="middle" font-size="10" fill="#607D8B">REST API</text>
# MAGIC
# MAGIC   <!-- Routes -->
# MAGIC   <path d="M190 40 C330 40, 370 60, 500 60" stroke="#2E7D32" stroke-width="1.5" fill="none" marker-end="url(#arrowGreen)"/>
# MAGIC   <path d="M190 160 C330 160, 370 60, 500 60" stroke="#2E7D32" stroke-width="1.5" fill="none" marker-end="url(#arrowGreen)"/>
# MAGIC   <path d="M190 160 C330 160, 370 145, 500 145" stroke="#F57C00" stroke-width="1.5" fill="none" marker-end="url(#arrowOrange)"/>
# MAGIC   <path d="M190 100 C330 100, 370 145, 500 145" stroke="#F57C00" stroke-width="1.5" fill="none" marker-end="url(#arrowOrange)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowGreen" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto">
# MAGIC       <polygon points="0 0, 8 3.5, 0 7" fill="#2E7D32"/>
# MAGIC     </marker>
# MAGIC     <marker id="arrowOrange" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto">
# MAGIC       <polygon points="0 0, 8 3.5, 0 7" fill="#F57C00"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">Custom Libraries</summary>
# MAGIC
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC Include custom libraries — or libraries from a private mirror server — while logging your model, and use them with model deployments.
# MAGIC
# MAGIC <ul>
# MAGIC   <li>Private PyPI mirrors and custom wheels</li>
# MAGIC   <li>Pinned dependency versions for reproducibility</li>
# MAGIC   <li>Automatic environment reconstruction at serve time</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">Custom Artifacts</summary>
# MAGIC
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC Package custom files and artifacts with your models and serve them with Model Serving.
# MAGIC
# MAGIC <ul>
# MAGIC   <li>Tokenizers, config files, and lookup tables</li>
# MAGIC   <li>Preprocessing scripts and feature transformers</li>
# MAGIC   <li>Any file the model needs at inference time</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">Custom Models</summary>
# MAGIC
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC Serve models trained with various ML libraries:
# MAGIC
# MAGIC <ul>
# MAGIC   <li>scikit-learn, XGBoost, LightGBM</li>
# MAGIC   <li>HuggingFace Transformers</li>
# MAGIC   <li>PyTorch and TensorFlow</li>
# MAGIC   <li>Any framework via MLflow PyFunc</li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     In real-world production, models often require custom code, libraries, and files for preprocessing or inference. Databricks Model Serving lets you package these artifacts—such as tokenizers, config files, and custom wheels—alongside your model. This ensures the serving environment matches training, avoids missing dependencies, and supports reproducible, reliable deployments.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,C4. Monitoring and Observability
# MAGIC %md-sandbox
# MAGIC ### C4. Monitoring and Observability
# MAGIC
# MAGIC Every serving endpoint comes with monitoring, and you can export those metrics for alerting on your own platform.
# MAGIC
# MAGIC - **Metrics:** a ready-to-use metrics dashboard for endpoints (latency, request and error rates, CPU/memory).
# MAGIC - **External Export API:** if you have a centralized observability platform, export your endpoint metrics with the export API.
# MAGIC - **Alerting:** set up alerts after export with Databricks SQL or your external platform of choice.
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     The metrics dashboard tracks latency percentiles (p50–p99), QPS, and 4XX/5XX error rates per endpoint. The export API surfaces the same metrics programmatically (for example, via a <code>GET</code> against the model-serving metrics endpoint) so they can flow into external monitoring and alerting.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,C5. The Endpoint API for CI/CD
# MAGIC %md-sandbox
# MAGIC ### C5. The Endpoint API for CI/CD
# MAGIC
# MAGIC Beyond the UI, endpoints can be deployed as APIs within your CI/CD system for fully automated deployment.
# MAGIC
# MAGIC - **Create/manage endpoints** with the REST API, the Databricks SDK for Python, or the Go SDK.
# MAGIC - **Integrate with** your CI/CD process and Terraform.
# MAGIC
# MAGIC The example below creates a serving endpoint programmatically, specifying the served model, version, workload size, and scale-to-zero:
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 15px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>from databricks.sdk import WorkspaceClient
# MAGIC from databricks.sdk.service.serving import (
# MAGIC     EndpointCoreConfigInput, ServedEntityInput
# MAGIC )
# MAGIC </br>
# MAGIC w = WorkspaceClient()
# MAGIC w.serving_endpoints.create(
# MAGIC     name="feed-ads",
# MAGIC     config=EndpointCoreConfigInput(
# MAGIC         served_entities=[
# MAGIC             ServedEntityInput(
# MAGIC                 entity_name="main.ml_models.ads",
# MAGIC                 entity_version="1",
# MAGIC                 workload_size="Small",
# MAGIC                 scale_to_zero_enabled=True,
# MAGIC             )
# MAGIC         ]
# MAGIC     ),
# MAGIC )</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">Endpoints can equally be created with the raw REST API or Terraform. The Databricks SDK for Python shown here is the most common choice inside notebooks and CI/CD pipelines.
# MAGIC </div></div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Online Feature Store and Automated Lookups

# COMMAND ----------

# DBTITLE 1,D1. Automated Feature and Vector Lookups
# MAGIC %md-sandbox
# MAGIC ### D1. Automated Feature and Vector Lookups
# MAGIC
# MAGIC A real-time request often carries only identifiers, not full feature vectors. Model Serving completes the payload automatically.
# MAGIC
# MAGIC - **Automatic Feature Lookups:** define your features once, publish them to the online store, and Databricks automatically grabs and joins the correct features to complete the payload for inference.
# MAGIC - **Automatic Vector Lookups:** seamlessly integrate with Vector Stores for vector search while using LLMs.
# MAGIC
# MAGIC
# MAGIC <div style="background: #F9F7F4; border: 1px solid #ddd; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, Menlo, monospace; font-size: 13px; color: #0a0a0a; white-space: pre;">
# MAGIC {
# MAGIC   "dataframe_records": [
# MAGIC     { "user_id": "0004815a-dfec-45c4-be01-...",
# MAGIC       "impression_timestamp": "2022-06-26T21:33:37",
# MAGIC       "session_id": "abb42041-2eab-41dd-..." }
# MAGIC   ]
# MAGIC }
# MAGIC # → age, num_purchases_last_6_months, etc. are looked up
# MAGIC #   from the Online Feature Store to complete the payload
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     With automated feature lookups, you only need to send keys (like <code>user_id</code>) in your inference request. The endpoint automatically fetches all relevant features from the online feature store and completes the payload for you. This simplifies client code and ensures consistent, up-to-date features for real-time inference.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,D2. The Online Feature Store
# MAGIC %md-sandbox
# MAGIC ### D2. The Online Feature Store
# MAGIC
# MAGIC Offline feature tables are optimized for training, not for millisecond lookups. The **online feature store** is the low-latency counterpart that a serving endpoint reads from at request time.
# MAGIC
# MAGIC <div style="border-left: 4px solid #00A972; background: rgba(0,169,114,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC <strong style="color: #424242;">Three steps:</strong>
# MAGIC <ol>
# MAGIC   <li>Sync the offline feature table (keyed by PK) to the online feature store.</li>
# MAGIC   <li>Train and deploy the model to a serving endpoint.</li>
# MAGIC   <li>At request time, the endpoint performs feature lookups/functions against the online store.</li>
# MAGIC </ol>
# MAGIC The Databricks Online Feature Store is backed by <strong>Lakebase</strong> (serverless Postgres).
# MAGIC </div>
# MAGIC
# MAGIC </br>
# MAGIC <div style="max-width: 1000px; margin: 0 auto; display: flex; justify-content: center;">
# MAGIC <svg width="100%" viewBox="0 0 860 350" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Online Feature Store Workflow</title>
# MAGIC
# MAGIC   <!-- Register/train region -->
# MAGIC   <rect x="200" y="15" width="540" height="135" rx="10" fill="none" stroke="#607D8B" stroke-width="1.5" stroke-dasharray="6,4"/>
# MAGIC   <text x="240" y="50" font-size="14" font-weight="bold" fill="#1B3139">Register feature</text>
# MAGIC   <text x="240" y="66" font-size="14" font-weight="bold" fill="#1B3139">lookups and</text>
# MAGIC   <text x="240" y="82" font-size="14" font-weight="bold" fill="#1B3139">functions</text>
# MAGIC   <text x="470" y="55" font-size="14" font-weight="bold" fill="#607D8B">Train</text>
# MAGIC   <text x="470" y="85" font-size="14" font-weight="bold" fill="#1565C0" font-family="monospace">mlflow</text>
# MAGIC   <rect x="360" y="8" width="230" height="22" rx="4" fill="#1B3139"/>
# MAGIC   <text x="475" y="25" text-anchor="middle" font-size="12" fill="#F9F7F4" font-family="monospace">fe = FeatureEngineeringClient()</text>
# MAGIC   <text x="660" y="70" font-size="16" font-weight="bold" fill="#607D8B">Models</text>
# MAGIC   <line x1="360" y1="66" x2="640" y2="65" stroke="#607D8B" stroke-width="2" marker-end="url(#arrowOF)"/>
# MAGIC
# MAGIC   <!-- Offline feature table -->
# MAGIC   <rect x="400" y="120" width="150" height="55" rx="8" fill="#F9F7F4" stroke="#607D8B" stroke-width="1.3"/>
# MAGIC   <text x="475" y="145" text-anchor="middle" font-size="14" font-weight="bold" fill="#1B3139">Offline Feature</text>
# MAGIC   <text x="475" y="162" text-anchor="middle" font-size="14" font-weight="bold" fill="#1B3139">Table (PK)</text>
# MAGIC
# MAGIC   <!-- Online feature store -->
# MAGIC   <rect x="170" y="240" width="150" height="55" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="245" y="265" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Online Feature</text>
# MAGIC   <text x="245" y="282" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Store</text>
# MAGIC
# MAGIC   <!-- Serving endpoint -->
# MAGIC   <rect x="620" y="240" width="150" height="55" rx="8" fill="#FFF8E1" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="695" y="265" text-anchor="middle" font-size="14" font-weight="bold" fill="#E65100">Model Serving</text>
# MAGIC   <text x="695" y="282" text-anchor="middle" font-size="14" font-weight="bold" fill="#E65100">Endpoint</text>
# MAGIC
# MAGIC   <!-- 1 Sync -->
# MAGIC   <line x1="400" y1="180" x2="310" y2="235" stroke="#FF3621" stroke-width="1.5" marker-end="url(#arrowOFr)"/>
# MAGIC   <text x="370" y="215" font-size="14" font-weight="bold" fill="#1B3139">Sync</text>
# MAGIC   <text x="340" y="205" font-size="18" font-weight="bold" fill="#FF3621">1</text>
# MAGIC
# MAGIC   <!-- 2 train -> endpoint -->
# MAGIC   <line x1="685" y1="90" x2="685" y2="220" stroke="#FF3621" stroke-width="1.5" marker-end="url(#arrowOFr)"/>
# MAGIC   <text x="700" y="180" font-size="18" font-weight="bold" fill="#FF3621">2</text>
# MAGIC
# MAGIC   <!-- 3 lookups -->
# MAGIC   <line x1="580" y1="265" x2="350" y2="265" stroke="#FF3621" stroke-width="1.5" marker-end="url(#arrowOFr)"/>
# MAGIC   <text x="470" y="255" font-size="18" font-weight="bold" fill="#FF3621">3</text>
# MAGIC   <text x="380" y="290" font-size="14" font-weight="bold" fill="#1B3139">Feature Lookups/Functions</text> 
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowOF" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#607D8B"/></marker>
# MAGIC     <marker id="arrowOFr" markerWidth="8" markerHeight="7" refX="7" refY="3.5" orient="auto"><polygon points="0 0, 8 3.5, 0 7" fill="#FF3621"/></marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">Online Feature Store Tables</summary>
# MAGIC
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC The online feature store provides low-latency feature serving for real-time inference:
# MAGIC
# MAGIC <ul>
# MAGIC   <li><strong>Low-latency, high-throughput access:</strong> optimized for real-time applications and ML serving at high scale</li>
# MAGIC   <li><strong>Managed capacity and scaling:</strong> uses capacity units that scale up/down, with optional read replicas for higher concurrency; supports serverless compute</li>
# MAGIC   <li><strong>Seamless Model Serving integration:</strong> models deployed to Mosaic AI Model Serving automatically perform feature lookups based on feature lineage — no extra endpoint wiring required</li>
# MAGIC   <li><strong>Time-series point-in-time retrieval:</strong> publish feature tables with a time series designation (latest-row per key) or without (all rows), enabling accurate retrieval by entity ID and timestamp for verification and back-testing</li>
# MAGIC   <li><strong>Scheduled updates:</strong> keep online features fresh with automated sync from offline tables</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC

# COMMAND ----------

# DBTITLE 1,D3. Feature Functions — On-Demand Features
# MAGIC %md-sandbox
# MAGIC ### D3. Feature Functions — On-Demand Features
# MAGIC
# MAGIC Some features can't be precomputed — they depend on values only known at request time. **Feature functions** compute these on demand during inference.
# MAGIC
# MAGIC - Automatically calculate on-demand features during inference requests.
# MAGIC - Feature functions are **Python UDFs governed by Unity Catalog**.
# MAGIC - Provide function and input bindings during training.
# MAGIC - Support all data types supported by Feature Engineering **except `MapType` and `ArrayType`**.
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     <b>FeatureLookup</b> retrieves precomputed features from the online feature store at inference time, ensuring fast, consistent access to historical values — the same mechanism <code>score_batch</code> uses for batch inference, except it reads from the low-latency online store instead of the offline feature table. <b>FeatureFunction</b> computes features dynamically using a Unity Catalog-governed Python UDF, allowing for real-time calculations based on request data (such as distance or recency). Both are defined during training and automatically applied by the serving endpoint, simplifying feature engineering for production ML.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,Conclusion
# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lecture, you covered Databricks Model Serving in depth:
# MAGIC
# MAGIC 1. **Databricks Model Serving Overview** — A unified UI, API, and SDK for serving custom models, Foundation Model APIs, and external models. Core features span real-time performance (< 100ms latency, 3K+ QPS, 99.9% availability), unification on the Data Intelligence Platform (feature/vector lookups, MLflow, monitoring, UC governance), and simplified deployment (UI/API, CPU/GPU, traffic splitting).
# MAGIC 2. **Serving Infrastructure** — Serverless compute autoscales within a chosen workload size and can scale to zero to save cost; native MLflow integration connects the model registry in Unity Catalog directly to a REST endpoint for a fast path to production.
# MAGIC 3. **Deploying and Managing Endpoints** — The endpoint-centric workflow gives a stable scoring URI, flexible many-to-many model/endpoint mapping, and staged rollout. Traffic splitting enables A/B testing; custom libraries and artifacts serve alongside the model; endpoints are monitored and can be created via the REST API, Databricks SDK, or Terraform for CI/CD.
# MAGIC 4. **Online Feature Store and Automated Lookups** — Requests carry only keys, and the endpoint completes the payload via automatic feature and vector lookups. The online feature store (on Lakebase) syncs from offline tables for low-latency reads, and feature functions compute on-demand features as UC-governed Python UDFs.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
