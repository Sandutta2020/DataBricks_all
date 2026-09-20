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
# MAGIC # Lecture — Model Deployment Strategies
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This lecture introduces model deployment — the step that turns a trained model into something the business can actually use. 
# MAGIC
# MAGIC This lecture covers 4 sections that build on each other:
# MAGIC
# MAGIC - **A. What Is Model Deployment**. A definition of model deployment for traditional ML models, and where deployment sits in the machine learning full lifecycle — the boundary between static historical data and continuously changing production data.
# MAGIC - **B. Deployment Strategies**. The four ways to serve predictions — batch, streaming, real-time, and edge/embedded — and how each one works.
# MAGIC - **C. Choosing a Strategy**. The throughput–latency tradeoff that drives the decision, a side-by-side comparison of the modes, and guidance on matching a scenario to the right strategy.
# MAGIC - **D. Model Deployment on Databricks**. How each strategy is implemented on Databricks — batch inference, streaming/pipeline scoring, and real-time Model Serving — and how the rest of this course is organized around them.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. Define model deployment for traditional machine learning models.
# MAGIC 2. Describe batch, streaming, real-time, and edge/embedded deployment.
# MAGIC 3. Identify scenarios in which each type of deployment is best suited.
# MAGIC 4. Compare and contrast these deployment strategies on Databricks.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. What Is Model Deployment

# COMMAND ----------

# DBTITLE 1,A1. Defining Model Deployment
# MAGIC %md-sandbox
# MAGIC ### A1. Defining Model Deployment
# MAGIC
# MAGIC **Machine learning model deployment** is the process of integrating a machine learning model into a **production environment**, making it accessible for end-users or other systems to **generate predictions or insights**.
# MAGIC
# MAGIC A model that only produces predictions inside a training notebook delivers no business value. Deployment is what closes that gap — it takes the trained model and puts it somewhere other people and systems can call it to get answers on new data.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 220" role="img" style="font-family: sans-serif;">
# MAGIC   <title>From Trained Model to Production Predictions</title>
# MAGIC
# MAGIC   <!-- Trained model -->
# MAGIC   <rect x="20" y="70" width="200" height="80" rx="10" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="120" y="105" text-anchor="middle" font-size="15" font-weight="bold" fill="#1565C0">Trained Model</text>
# MAGIC   <text x="120" y="128" text-anchor="middle" font-size="12" fill="#1B3139">Built on historical data</text>
# MAGIC
# MAGIC   <!-- Deployment step -->
# MAGIC   <rect x="330" y="70" width="200" height="80" rx="10" fill="#1B3139" stroke="none"/>
# MAGIC   <text x="430" y="98" text-anchor="middle" font-size="15" font-weight="bold" fill="#FFFFFF">Deployment</text>
# MAGIC   <text x="430" y="120" text-anchor="middle" font-size="12" fill="#F9F7F4">Integrate into a</text>
# MAGIC   <text x="430" y="136" text-anchor="middle" font-size="12" fill="#F9F7F4">production environment</text>
# MAGIC
# MAGIC   <!-- Predictions -->
# MAGIC   <rect x="640" y="70" width="200" height="80" rx="10" fill="#E8F5E9" stroke="#388E3C" stroke-width="2"/>
# MAGIC   <text x="740" y="98" text-anchor="middle" font-size="15" font-weight="bold" fill="#2E7D32">Predictions</text>
# MAGIC   <text x="740" y="120" text-anchor="middle" font-size="12" fill="#1B3139">Served to end-users</text>
# MAGIC   <text x="740" y="136" text-anchor="middle" font-size="12" fill="#1B3139">&amp; other systems</text>
# MAGIC
# MAGIC   <!-- Arrows -->
# MAGIC   <line x1="220" y1="110" x2="330" y2="110" stroke="#1B3139" stroke-width="2" marker-end="url(#arrowA)"/>
# MAGIC   <line x1="530" y1="110" x2="640" y2="110" stroke="#1B3139" stroke-width="2" marker-end="url(#arrowA)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowA" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
# MAGIC       <polygon points="0 0, 9 3.5, 0 7" fill="#1B3139"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     There are four main ways to deploy a machine learning model: <strong>batch</strong>, <strong>streaming</strong>, <strong>real-time</strong>, and <strong>edge/embedded</strong>. Each strategy fits different business needs, depending on how quickly predictions are required and how much data must be scored. Understanding these options helps you match deployment to your use case and maximize the value of your model.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### A2. Deployment in the ML Full Lifecycle
# MAGIC
# MAGIC Your model is ready — then what? Model training is only one stage in a larger workflow. The full lifecycle spans from defining the business problem through deployment and ongoing monitoring, and it splits into two halves at a critical boundary.
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 800 525" role="img" style="font-family: sans-serif;">
# MAGIC   <title>The Machine Learning Lifecycle — Data Preparation Context</title>
# MAGIC   <desc>Two phases of the Machine Learning lifecycle. Model Development contains Business problem, Data collection, and Data prep / feature engineering in a top row, with Model training and Model evaluation in a bottom row connected by a downward then leftward arrow. An arrow exits Model evaluation rightward into the Production phase, which contains Model deployment, Model monitoring, and Model retrain in sequence.</desc>
# MAGIC   <defs>
# MAGIC     <marker id="mlc-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
# MAGIC       <path d="M2 1L8 5L2 9" fill="none" stroke="#1B3139" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC
# MAGIC
# MAGIC   <!-- Top subgroup: Model Development — fill then dashed outline -->
# MAGIC   <rect x="30" y="52" width="700" height="250" rx="12" fill="#2272B4" fill-opacity="0.08"/>
# MAGIC   <rect x="30" y="52" width="700" height="250" rx="12" fill="none" stroke="#2272B4" stroke-width="1.5" stroke-dasharray="6 3"/>
# MAGIC   <text x="50" y="200" font-size="13" font-weight="bold" fill="#0b2026">Model Development</text>
# MAGIC   <text x="50" y="215" font-size="11" fill="#618794">(static historical data)</text>
# MAGIC
# MAGIC   <!-- 1st step: Business problem -->
# MAGIC   <rect x="43" y="98" width="115" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.2"/>
# MAGIC   <text x="100" y="120" text-anchor="middle" font-size="12" font-weight="bold"" fill="#0b2026">Business</text>
# MAGIC   <text x="100" y="138" text-anchor="middle" font-size="12" font-weight="bold" fill="#0b2026">Problem</text>
# MAGIC
# MAGIC   <!-- 2nd step:  Define success criteria -->
# MAGIC   <rect x="175" y="98" width="115" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.2"/>
# MAGIC   <text x="232" y="120" text-anchor="middle" font-size="12" font-weight="bold" fill="#0b2026">Define Success</text>
# MAGIC   <text x="232" y="138" text-anchor="middle" font-size="12" font-weight="bold" fill="#0b2026">Criteria</text>
# MAGIC
# MAGIC   <!-- 3rd step: Data collection (highlighted) -->
# MAGIC   <rect x="305" y="98" width="115" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.5"/>
# MAGIC   <text x="360" y="120" text-anchor="middle" font-size="12" font-weight="bold"fill="#0b2026">Data Collection</text>
# MAGIC
# MAGIC   <!-- 4th step: Data prepprocessing / feature engineering  -->
# MAGIC   <rect x="435" y="98" width="150" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.5"/>
# MAGIC   <text x="510" y="116" text-anchor="middle" font-size="12" font-weight="bold" fill="#0b2026">Data Preprocessing /</text>
# MAGIC   <text x="510" y="132" text-anchor="middle" font-size="12" font-weight="bold" fill="#0b2026">Feature Engineering</text>
# MAGIC
# MAGIC   <!-- 5th step: Model training (highlighted)-->
# MAGIC   <rect x="605" y="98" width="115" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.2"/>
# MAGIC   <text x="662" y="130" text-anchor="middle" font-size="12" font-weight="bold" fill="#0b2026">Model Training</text>
# MAGIC
# MAGIC   <!-- Arrow from Model Training to Model evaluation  -->
# MAGIC   <path d="M662 150 L662 200" fill="none" stroke="#1B3139" stroke-width="1.8" marker-end="url(#mlc-arrow)"/>
# MAGIC
# MAGIC   <!-- 6th step: Model evaluation (highlighted) -->
# MAGIC   <rect x="605" y="200" width="115" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.2"/>
# MAGIC   <text x="662" y="230" text-anchor="middle" font-size="12" font-weight="bold" fill="#0b2026">Model Evaluation</text>
# MAGIC
# MAGIC   <!-- Top row arrows -->
# MAGIC   <path d="M158 124 L175 124" fill="none" stroke="#1B3139" stroke-width="1.8" marker-end="url(#mlc-arrow)"/>
# MAGIC   <path d="M290 124 L305 124" fill="none" stroke="#1B3139" stroke-width="1.8" marker-end="url(#mlc-arrow)"/>
# MAGIC   <path d="M420 124 L435 124" fill="none" stroke="#1B3139" stroke-width="1.8" marker-end="url(#mlc-arrow)"/>
# MAGIC   <path d="M585 124 L605 124" fill="none" stroke="#1B3139" stroke-width="1.8" marker-end="url(#mlc-arrow)"/>
# MAGIC
# MAGIC <!-- Bottom subgroup: Deployment and Production — fill then dashed outline -->
# MAGIC   <rect x="30" y="310" width="700" height="200" rx="12" fill="#00A972" fill-opacity="0.07"/>
# MAGIC   <rect x="30" y="310" width="700" height="200" rx="12" fill="none" stroke="#00A972" stroke-width="1.5" stroke-dasharray="6 3"/>
# MAGIC   <text x="50" y="400"  font-size="13" font-weight="bold" fill="#0b2026">Deployment & Production</text>
# MAGIC   <text x="50" y="415"  font-size="11" fill="#618794">(continuously changing data)</text>
# MAGIC
# MAGIC   <!-- 7th step: Model deployment -->
# MAGIC   <rect x="440" y="350" width="115" height="52" rx="8" fill="#00A972" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="500" y="380" text-anchor="middle" font-size="12" font-weight="bold" fill="#ffffff">Model Deployment</text>
# MAGIC
# MAGIC   <!-- 8th step: Model Monitoring -->
# MAGIC   <rect x="305" y="350" width="115" height="52" rx="8" fill="#00A972" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="360" y="380" text-anchor="middle" font-size="12" font-weight="bold" fill="#ffffff">Model Monitoring</text>
# MAGIC   
# MAGIC   <!-- Arrow from Model Monitoring (top center) to Data Collection (bottom center) -->
# MAGIC   <path d="M362.5 350 L362.5 150" fill="none" stroke="#1B3139" stroke-width="1.8" marker-end="url(#mlc-arrow)"/>
# MAGIC
# MAGIC   <!-- Bottom row arrows -->
# MAGIC   <path d="M440 375 L420 375" fill="none" stroke="#1B3139" stroke-width="1.8" marker-end="url(#mlc-arrow)"/>
# MAGIC
# MAGIC   <!-- Feedback: Model Evaluation → Data Preprocessing / Feature Engineering -->
# MAGIC   <path d="M 605 218 C 558 218 510 184 510 150" fill="none" stroke="#1B3139" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#mlc-arrow)"/>
# MAGIC
# MAGIC   <!-- Feedback: Model Evaluation → Data Collection -->
# MAGIC   <path d="M 605 234 C 555 274 362 274 362 150" fill="none" stroke="#1B3139" stroke-width="1.8" stroke-dasharray="5 3" marker-end="url(#mlc-arrow)"/>
# MAGIC
# MAGIC   <!-- Forward: Model Evaluation → Model Deployment -->
# MAGIC   <path d="M 662 252 C 662 308 497 308 497 350" fill="none" stroke="#1B3139" stroke-width="1.8" marker-end="url(#mlc-arrow)"/>
# MAGIC
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC </br>
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC     The transition from model development to deployment is crucial: development uses <strong>static historical data</strong> to build and evaluate models, while deployment and production must handle <strong>continuously changing new data</strong> from the real world. Ongoing monitoring ensures models stay accurate and relevant, feeding back into data collection and retraining as needed. This feedback loop keeps your models effective in production.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,A2. Deployment in the ML Full Lifecycle
# MAGIC %md-sandbox
# MAGIC ### A2 (2nd version). Deployment in the ML Full Lifecycle
# MAGIC
# MAGIC Your model is ready — then what? Model training is only one stage in a larger workflow. The full lifecycle spans from defining the business problem through deployment and ongoing monitoring, and it splits into two halves at a critical boundary.
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 903 280" role="img" style="font-family: sans-serif;">
# MAGIC   <title>The Machine Learning Full Lifecycle</title>
# MAGIC
# MAGIC   <!-- Background regions -->
# MAGIC   <rect x="20" y="30" width="820" height="140" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5" stroke-dasharray="4"/>
# MAGIC   <text x="451" y="50" text-anchor="middle" font-size="13" fill="#1565C0" font-weight="bold">MODEL DEVELOPMENT — use static historical data</text>
# MAGIC
# MAGIC   <rect x="20" y="170" width="820" height="110" rx="8" fill="#E8F5E9" stroke="#2E7D32" stroke-width="1.5" stroke-dasharray="4"/>
# MAGIC   <text x="451" y="265" text-anchor="middle" font-size="13" fill="#2E7D32" font-weight="bold">DEPLOYMENT &amp; PRODUCTION — deal with continuously changing new data</text>
# MAGIC
# MAGIC   <!-- Development steps -->
# MAGIC   <rect x="35" y="65" width="120" height="70" rx="6" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="95" y="95" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Business</text>
# MAGIC   <text x="95" y="109" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Problem &amp;</text>
# MAGIC   <text x="95" y="123" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Success Criteria</text>
# MAGIC
# MAGIC   <rect x="195" y="65" width="120" height="70" rx="6" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="255" y="104" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Data Collection</text>
# MAGIC
# MAGIC   <rect x="355" y="65" width="120" height="70" rx="6" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="415" y="95" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Data Preprocessing</text>
# MAGIC   <text x="415" y="109" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">&amp; Feature</text>
# MAGIC   <text x="415" y="123" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Engineering</text>
# MAGIC
# MAGIC   <rect x="515" y="65" width="120" height="70" rx="6" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="575" y="104" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Model Training</text>
# MAGIC
# MAGIC   <rect x="675" y="65" width="120" height="70" rx="6" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="735" y="104" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Model Evaluation</text>
# MAGIC
# MAGIC   <!-- Production steps -->
# MAGIC   <rect x="195" y="205" width="120" height="45" rx="6" fill="#00A972" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="255" y="232" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Model Monitoring</text>
# MAGIC
# MAGIC   <rect x="355" y="205" width="120" height="45" rx="6" fill="#00A972" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="415" y="232" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Model Deployment</text>
# MAGIC
# MAGIC   
# MAGIC
# MAGIC   <!-- Arrows across development -->
# MAGIC   <line x1="155" y1="100" x2="195" y2="100" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowB)"/>
# MAGIC   <line x1="315" y1="100" x2="355" y2="100" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowB)"/>
# MAGIC   <line x1="475" y1="100" x2="515" y2="100" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowB)"/>
# MAGIC   <line x1="635" y1="100" x2="675" y2="100" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowB)"/>
# MAGIC
# MAGIC   <!-- Arrow from Model Monitoring up to Data Collection -->
# MAGIC   <line x1="255" y1="205" x2="255" y2="135" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowB)"/>
# MAGIC   
# MAGIC   <!-- Arrow from Model Deployment to Model Monitoring -->
# MAGIC   <path d="M355 225 L315 225" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowB)"/>
# MAGIC
# MAGIC   <!-- Feedback loop: Model Evaluation back up to Data Collection -->
# MAGIC   <polyline points="735,135 735,146 255,146" stroke="#1B3139" stroke-width="1.5" fill="none"/>
# MAGIC
# MAGIC   <!-- Feedback loop: Model Evaluation back up to Data Preprocessing/Feature Engineering -->
# MAGIC   <polyline points="735,135 735,146 415,146, 415 135" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowB)"/>
# MAGIC
# MAGIC   <!-- Feedback loop: Model Evaluation to Model Deployment -->
# MAGIC   <polyline points="735,135 735,227 475,227" stroke="#1B3139" stroke-width="1.5" fill="none" marker-end="url(#arrowB)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowB" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
# MAGIC       <path d="M0,0 L0,6 L6,3 z" fill="#1B3139"/>
# MAGIC     </marker>
# MAGIC     <marker id="arrowG" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
# MAGIC       <path d="M0,0 L0,6 L6,3 z" fill="#2E7D32"/>
# MAGIC     </marker>
# MAGIC     <marker id="arrowRed" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
# MAGIC       <path d="M0,0 L0,6 L6,3 z" fill="#FF3621"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC </br>
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC     The transition from model development to deployment is crucial: development uses <strong>static historical data</strong> to build and evaluate models, while deployment and production must handle <strong>continuously changing new data</strong> from the real world. Ongoing monitoring ensures models stay accurate and relevant, feeding back into data collection and retraining as needed. This feedback loop keeps your models effective in production.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Deployment Strategies

# COMMAND ----------

# DBTITLE 1,B1. The Four Deployment Modes
# MAGIC %md-sandbox
# MAGIC ### B1. The Four Deployment Modes
# MAGIC
# MAGIC Once a model is ready for production, there are four main strategies for serving its predictions. They differ mainly in **how much data** they score at once and **how quickly** a prediction must be available.
# MAGIC
# MAGIC <div class="rc-wrap">
# MAGIC <style>
# MAGIC .rc-wrap { width: 100%; display: flex; flex-direction: column; align-items: center; gap: 18px; font-family: sans-serif; }
# MAGIC .rc-wrap * { box-sizing: border-box; }
# MAGIC .rc-hint { width: 100%; max-width: 1100px; text-align: center; font-size: 14pt; color: #5E7077; font-style: italic; }
# MAGIC .rc-hint strong { color: #FF5F46; font-style: normal; font-weight: 700; }
# MAGIC .rc-row { display: block; white-space: nowrap; font-size: 0; width: 100%; max-width: 1100px; }
# MAGIC .rc-box { display: inline-block; width: 23.5%; margin-right: 2%; min-height: 100px; background: #F9F7F4; border-top: 8px solid transparent; border-left: 2px solid transparent; border-right: 2px solid transparent; border-bottom: 2px solid transparent; border-radius: 8px; padding: 16px 14px; text-align: center; cursor: pointer; user-select: none; vertical-align: top; transition: transform 0.12s; box-shadow: 0 2px 8px rgba(27,49,57,0.06); white-space: normal; }
# MAGIC .rc-box:last-child { margin-right: 0; }
# MAGIC .rc-box:hover { transform: translateY(-2px); }
# MAGIC .rc-box.active { background: #fff; border-left-color: var(--pc); border-right-color: var(--pc); border-bottom-color: var(--pc); }
# MAGIC .rc-label { display: block; font-weight: 700; font-size: 16pt; letter-spacing: 2px; text-transform: uppercase; line-height: 1.2; pointer-events: none; }
# MAGIC .rc-title { display: block; font-size: 14pt; font-weight: 700; color: #0b2026; line-height: 1.3; margin-top: 6px; pointer-events: none; }
# MAGIC .rc-text { display: block; font-size: 12pt; color: #0b2026; line-height: 1.3; margin-top: 6px; pointer-events: none; }
# MAGIC .rc-detail-wrap { overflow: hidden; max-height: 0; opacity: 0; transition: max-height 0.35s ease, opacity 0.28s ease, margin-top 0.28s ease; margin-top: 0; width: 100%; max-width: 1100px; }
# MAGIC .rc-detail-wrap.open { max-height: 700px; opacity: 1; margin-top: 12px; }
# MAGIC .rc-detail-card { background: #F9F7F4; border-radius: 10px; padding: 22px 26px; border-top: 7px solid #ccc; box-shadow: 0 2px 8px rgba(27,49,57,0.06); }
# MAGIC .rc-detail-title { font-size: 17pt; font-weight: 700; color: #0b2026; margin-bottom: 12px; line-height: 1.3; }
# MAGIC .rc-detail-body { font-size: 14pt; color: #0b2026; line-height: 1.55; }
# MAGIC .rc-detail-body ul { margin: 0; padding-left: 22px; }
# MAGIC .rc-detail-body li { margin-bottom: 8px; }
# MAGIC .rc-detail-body li:last-child { margin-bottom: 0; }
# MAGIC </style>
# MAGIC
# MAGIC <div class="rc-hint">For more detail, <strong>click each card below</strong>.</div>
# MAGIC
# MAGIC <div class="rc-row">
# MAGIC   <span class="rc-box" data-id="0" onclick="rcSelect(0)" style="--pc:#1976D2; border-top-color:#1976D2;">
# MAGIC     <span class="rc-label" style="color:#1976D2;">Batch</span>
# MAGIC     <span class="rc-title">High throughput.</span>
# MAGIC     <span class="rc-text">Results in hours to days.</span>
# MAGIC   </span>
# MAGIC   <span class="rc-box" data-id="1" onclick="rcSelect(1)" style="--pc:#F57C00; border-top-color:#F57C00;">
# MAGIC     <span class="rc-label" style="color:#F57C00;">Streaming</span>
# MAGIC     <span class="rc-title">Moderate throughput</span>
# MAGIC     <span class="rc-text">Results in seconds to minutes.</span>
# MAGIC   </span>
# MAGIC   <span class="rc-box" data-id="2" onclick="rcSelect(2)" style="--pc:#7B1FA2; border-top-color:#7B1FA2;">
# MAGIC     <span class="rc-label" style="color:#7B1FA2;">Real-time</span>
# MAGIC     <span class="rc-title">Low latency</span>
# MAGIC     <span class="rc-text">Return predictions within milliseconds.</span>
# MAGIC   </span>
# MAGIC   <span class="rc-box" data-id="3" onclick="rcSelect(3)" style="--pc:#388E3C; border-top-color:#388E3C;">
# MAGIC     <span class="rc-label" style="color:#388E3C;">Edge / Embedded</span>
# MAGIC     <span class="rc-title">On device</span>
# MAGIC     <span class="rc-text">Ultra-low latency close to the data source.</span>
# MAGIC   </span>
# MAGIC </div>
# MAGIC
# MAGIC <div class="rc-detail-wrap" id="rc-detail-wrap">
# MAGIC   <div class="rc-detail-card" id="rc-detail-card"></div>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC <script>
# MAGIC var REVEAL = [
# MAGIC   {
# MAGIC     title: "Batch",
# MAGIC     color: "#1976D2",
# MAGIC     text: "<ul><li>Score large volumes of data on a schedule.</li><li>Compute predictions ahead of time for later use.</li><li>Write results to storage for downstream consumption.</li></ul><div style='margin-top:12px;'><strong>Example:</strong> Periodic customer churn prediction — score the full customer base each night and hand the results to the marketing team.</div>"
# MAGIC   },
# MAGIC   {
# MAGIC     title: "Streaming",
# MAGIC     color: "#F57C00",
# MAGIC     text: "<ul><li>Score records as they arrive continuously.</li><li>Keep pace with incoming data streams.</li><li>Write predictions to a sink for immediate use.</li></ul><div style='margin-top:12px;'><strong>Example:</strong> Dynamic pricing application — adjusts prices as new demand and inventory events stream in.</div>"
# MAGIC   },
# MAGIC   {
# MAGIC     title: "Real-time",
# MAGIC     color: "#7B1FA2",
# MAGIC     text: "<ul><li>Score one request at a time, on demand.</li><li>Return predictions within milliseconds.</li><li>Expose the model behind a live REST endpoint.</li></ul><div style='margin-top:12px;'><strong>Example:</strong> Recommendation systems and chatbots — respond instantly as a user interacts.</div>"
# MAGIC   },
# MAGIC   {
# MAGIC     title: "Edge / Embedded",
# MAGIC     color: "#388E3C",
# MAGIC     text: "<ul><li>Score directly on the device, often offline.</li><li>Generate predictions locally, close to the data source.</li><li>Operate with little or no network connection.</li></ul><div style='margin-top:12px;'><strong>Example:</strong> IoT applications — e.g., a farm sensor that detects humidity and acts on-device.</div>"
# MAGIC   }
# MAGIC ];
# MAGIC var rcCurrent = null;
# MAGIC function rcSelect(id) {
# MAGIC   var wrap = document.getElementById('rc-detail-wrap');
# MAGIC   var card = document.getElementById('rc-detail-card');
# MAGIC   var d = REVEAL[id];
# MAGIC   document.querySelectorAll('.rc-box').forEach(function(b) {
# MAGIC     b.classList.toggle('active', parseInt(b.dataset.id) === id && rcCurrent !== id);
# MAGIC   });
# MAGIC   if (rcCurrent === id) { wrap.classList.remove('open'); rcCurrent = null; return; }
# MAGIC   rcCurrent = id;
# MAGIC   card.style.borderTopColor = d.color;
# MAGIC   card.innerHTML = '<div class="rc-detail-title" style="color:' + d.color + ';">' + d.title + '</div><div class="rc-detail-body">' + d.text + '</div>';
# MAGIC   wrap.classList.add('open');
# MAGIC }
# MAGIC </script>

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Choosing a Strategy

# COMMAND ----------

# DBTITLE 1,C1. The Throughput–Latency Tradeoff
# MAGIC %md-sandbox
# MAGIC ### C1. The Throughput–Latency Tradeoff
# MAGIC
# MAGIC The choice of deployment strategy comes down to two competing requirements:
# MAGIC
# MAGIC - **Throughput** — how many predictions you can produce per unit of time (favors scoring big batches at once).
# MAGIC - **Latency** — how quickly a single prediction is available after it is requested (favors scoring one record at a time, immediately).
# MAGIC
# MAGIC These pull in opposite directions. Batch maximizes throughput but accepts high latency; real-time minimizes latency but scores far less data per call. The modes sit on a spectrum between the two.
# MAGIC
# MAGIC
# MAGIC
# MAGIC <div style="max-width: 1100px; margin: 0 auto; padding-left: 1.7%; padding-right: 2.3%;">
# MAGIC   <div style="display: flex; justify-content: space-between; font-size: 12px; color: #888; margin-bottom: 6px;">
# MAGIC     <span>← High throughput · High latency</span>
# MAGIC     <span>Low latency · Low throughput →</span>
# MAGIC   </div>
# MAGIC   <div style="height: 12px; background: linear-gradient(to right, #1976D2, #F57C00, #7B1FA2, #388E3C); border-radius: 5px; margin-bottom: 10px;"></div>
# MAGIC   <div style="display: flex; font-size: 13px; font-weight: 600;">
# MAGIC     <span style="flex: 1; text-align: center; color: #1976D2;">Batch</span>
# MAGIC     <span style="flex: 1; text-align: center; color: #F57C00;">Streaming</span>
# MAGIC     <span style="flex: 1; text-align: center; color: #7B1FA2;">Real-time</span>
# MAGIC     <span style="flex: 1; text-align: center; color: #388E3C;">Edge</span>
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,C2. Comparing the Deployment Modes
# MAGIC %md-sandbox
# MAGIC ### C2. Comparing the Deployment Modes
# MAGIC
# MAGIC The table below summarizes how the four modes compare on throughput and latency, with a representative example for each.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 900px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Deployment Method</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Throughput</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Latency (response time)</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Example Application</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Batch</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">High</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">High — slow response (hours to days)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Periodic customer churn prediction</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Streaming</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Moderate</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Moderate (seconds to minutes)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Dynamic pricing application</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Real-time</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Low</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Low (milliseconds)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Recommendation systems, chatbots</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Edge / Embedded</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Low</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Low (dependent on device processing power)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">IoT applications — e.g., a farm sensor detecting humidity</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# DBTITLE 1,C3. Matching a Scenario to a Strategy
# MAGIC %md-sandbox
# MAGIC ### C3. Matching a Scenario to a Strategy
# MAGIC
# MAGIC To choose a strategy, start from the use case and ask two questions: *how fresh must the prediction be?* and *how much data must be scored?*
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 900px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Choose…</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">When…</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Batch</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Predictions can be computed ahead of time and consumed later; you need to score large volumes efficiently and freshness of minutes/seconds is not required.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Streaming</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Data arrives continuously and predictions should keep up within seconds to minutes, but sub-second responses are not required.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Real-time</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">An application needs an answer on demand, per request, within milliseconds — a user is waiting on the other end.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Edge / Embedded</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Predictions must run on the device itself — limited connectivity, strict privacy, or ultra-low latency close to the data source.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     The same trained model can be deployed in multiple modes. Deployment strategy is a choice about <em>how</em> predictions are served, based on the use case—not a property of the model itself.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Model Deployment on Databricks

# COMMAND ----------

# DBTITLE 1,D1. From Strategy to Implementation
# MAGIC %md-sandbox
# MAGIC ### D1. From Strategy to Implementation
# MAGIC
# MAGIC Databricks provides a path for each of the three platform-served strategies. In every case the model is registered in **Models in Unity Catalog** and then served through the mechanism that fits the use case.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 900px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Strategy</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">How it is served on Databricks</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Batch</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Load the registered model as a Spark UDF, or call it with the <code>ai_query()</code> SQL function, to score a Delta table on a schedule. Predictions are written back to Delta for downstream use.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Streaming / Pipeline</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Apply the same model UDF to a Structured Streaming DataFrame or within a Lakeflow declarative pipeline, so records are scored continuously as they arrive.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Real-time</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;"><strong>Databricks Model Serving</strong> hosts the model behind a serverless REST endpoint that returns predictions within milliseconds, scaling automatically with traffic.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     The same registered model can be served in multiple ways—batch, streaming, or real-time—without retraining. MLflow packaging and Unity Catalog governance make it possible to select the serving path that best fits your use case.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,D2. How This Course Is Organized
# MAGIC %md-sandbox
# MAGIC ### D2. How This Course Is Organized
# MAGIC
# MAGIC The rest of this course takes each deployment strategy in turn, moving from highest-throughput to lowest-latency.
# MAGIC
# MAGIC <div style="max-width: 950px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 150" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Course Roadmap</title>
# MAGIC
# MAGIC   <rect x="20" y="45" width="180" height="60" rx="8" fill="#1B3139"/>
# MAGIC   <text x="110" y="72" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">This module</text>
# MAGIC   <text x="110" y="90" text-anchor="middle" font-size="11" fill="#F9F7F4">Deployment Fundamentals</text>
# MAGIC
# MAGIC   <rect x="230" y="45" width="180" height="60" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="320" y="72" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565C0">Batch</text>
# MAGIC   <text x="320" y="90" text-anchor="middle" font-size="11" fill="#1B3139">Batch Deployment</text>
# MAGIC
# MAGIC   <rect x="440" y="45" width="180" height="60" rx="8" fill="#FFF3E0" stroke="#F57C00" stroke-width="1.5"/>
# MAGIC   <text x="530" y="72" text-anchor="middle" font-size="12" font-weight="bold" fill="#E65100">Streaming</text>
# MAGIC   <text x="530" y="90" text-anchor="middle" font-size="11" fill="#1B3139">Pipeline Deployment</text>
# MAGIC
# MAGIC   <rect x="650" y="45" width="190" height="60" rx="8" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="1.5"/>
# MAGIC   <text x="745" y="72" text-anchor="middle" font-size="12" font-weight="bold" fill="#6A1B9A">Real-time</text>
# MAGIC   <text x="745" y="90" text-anchor="middle" font-size="11" fill="#1B3139">Real-time &amp; Online Stores</text>
# MAGIC
# MAGIC   <line x1="200" y1="75" x2="230" y2="75" stroke="#1B3139" stroke-width="2" marker-end="url(#arrowD)"/>
# MAGIC   <line x1="410" y1="75" x2="440" y2="75" stroke="#1B3139" stroke-width="2" marker-end="url(#arrowD)"/>
# MAGIC   <line x1="620" y1="75" x2="650" y2="75" stroke="#1B3139" stroke-width="2" marker-end="url(#arrowD)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrowD" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
# MAGIC       <polygon points="0 0, 9 3.5, 0 7" fill="#1B3139"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC The next lecture in this module, **Model Deployment with MLflow**, shows how MLflow packages a model once — with its dependencies and a standard format — so it is ready to be served through any of these strategies.

# COMMAND ----------

# DBTITLE 1,Conclusion
# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC In this lecture, you covered the fundamentals of model deployment strategies:
# MAGIC
# MAGIC 1. **What Is Model Deployment** — Deployment is the process of integrating a trained model into a production environment so end-users and other systems can generate predictions or insights. It marks the transition from model development on static historical data to production on continuously changing new data, followed by monitoring that feeds back into retraining.
# MAGIC 2. **Deployment Strategies** — There are four strategies for serving predictions: **batch** (score large volumes on a schedule), **streaming** (score records continuously as they arrive), **real-time** (score one request on demand behind an API), and **edge/embedded** (score directly on the device).
# MAGIC 3. **Choosing a Strategy** — The decision is driven by the throughput–latency tradeoff. Batch maximizes throughput at high latency; real-time minimizes latency at low throughput; streaming sits in between. Match the strategy to the use case by asking how fresh a prediction must be and how much data must be scored.
# MAGIC 4. **Model Deployment on Databricks** — A single model registered in Models in Unity Catalog can be served as a batch job (Spark UDF or `ai_query()`), a streaming/pipeline job (Structured Streaming or Lakeflow pipelines), or a real-time endpoint (Databricks Model Serving). The rest of the course explores each path in turn.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
