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
# MAGIC # Lecture — Hyperparameter Tuning Fundamentals
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This lecture introduces the concepts and techniques for hyperparameter tuning — the process of finding the best model configuration to maximize performance. You will learn what hyperparameters are, compare search strategies, understand cross-validation for robust evaluation, and discover how Optuna automates the optimization process on Databricks with MLflow integration.
# MAGIC
# MAGIC This lecture covers 4 sections that build on each other:
# MAGIC
# MAGIC - **A. What Are Hyperparameters**. What hyperparameters are, how they differ from model parameters the model learns on its own, and examples across common model families — plus why a search strategy is needed.
# MAGIC - **B. Hyperparameter Search Methods**. Grid search, random search, and Bayesian optimization on a spectrum from exhaustive-but-expensive to adaptive-and-efficient, with guidance on when to use each.
# MAGIC - **C. Validation and Cross-Validation**. Why repeatedly evaluating against a test set biases results, how a three-way split addresses this, and why K-fold cross-validation is the gold standard for robust performance estimation during tuning.
# MAGIC - **D. Optuna for Hyperparameter Optimization**. How Optuna automates tuning through a three-step workflow — define objective, create study, extract best results — using a define-by-run search space, TPE sampling, early pruning, and MLflow integration.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. Define hyperparameters as anything set before training that affects how the model learns, and explain how they differ from model parameters.
# MAGIC 2. Compare grid, random, and Bayesian search on a spectrum from exhaustive to adaptive, and explain when each is appropriate given search space size and compute budget.
# MAGIC 3. Explain why a single train/validation split can bias hyperparameter selection and describe K-fold cross-validation as the gold standard for robust evaluation.
# MAGIC 4. Describe Optuna’s three-step workflow, the define-by-run search space approach, and how it integrates with MLflow for experiment tracking on Databricks.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. What Are Hyperparameters

# COMMAND ----------

# DBTITLE 1,A1. Hyperparameters and Hyperparameter Tuning
# MAGIC %md-sandbox
# MAGIC ### A1. Hyperparameters and Hyperparameter Tuning
# MAGIC
# MAGIC A **hyperparameter** is anything you set **before training** that affects how the model learns — as opposed to model **parameters** (weights, coefficients, tree splits), which the model learns on its own.
# MAGIC
# MAGIC <br>
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .ds-row { display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 240px; }
# MAGIC .ds-card { background: #F9F7F4; border-radius: 8px; box-shadow: 0 2px 8px rgba(27,49,57,0.06); padding: 20px; border-top: 8px solid var(--accent, #4299E0); }
# MAGIC .blue{--accent:#4299E0;} .green{--accent:#00A972;} .coral{--accent:#FF5F46;}
# MAGIC .ds-card-title { font-size: 14pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
# MAGIC .ds-card-text { font-size: 12pt; color: #5E7077; line-height: 1.55; margin: 0; }
# MAGIC .ds-card ul, .ds-card ol { margin: 8px 0 0; padding-left: 20px; font-size: 14pt; line-height: 1.55; color: #0b2026; }
# MAGIC .ds-card li { margin-bottom: 10px; }
# MAGIC .ds-card li:last-child { margin-bottom: 0; }
# MAGIC .tc { text-align: center; }
# MAGIC </style>
# MAGIC
# MAGIC <div class="ds-row">
# MAGIC   <div class="ds-card blue">
# MAGIC     <div class="ds-card-title">Model Parameters</div>
# MAGIC     <ul>
# MAGIC       <li>Learned from data during training</li>
# MAGIC       <li>e.g., weights, coefficients, splits</li>
# MAGIC       <li>Updated by the learning algorithm</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC   <div class="ds-card green">
# MAGIC     <div class="ds-card-title">Hyperparameters</div>
# MAGIC     <ul>
# MAGIC       <li>Set before training begins</li>
# MAGIC       <li>e.g., learning rate, max depth, n_estimators</li>
# MAGIC       <li>Chosen by the practitioner or search algorithm</li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC
# MAGIC **Hyperparameter tuning** (model tuning) is the process of finding the best hyperparameter configuration to maximize model performance on a given dataset. The model cannot tune these automatically — that's why we need a **search strategy**.
# MAGIC
# MAGIC <br>
# MAGIC <div class="cw">
# MAGIC <div class="ds-row">
# MAGIC   <div class="ds-card coral">
# MAGIC     <div class="ds-card-title">Example Hyperparameters</div>
# MAGIC     <ul>
# MAGIC       <li>
# MAGIC         <strong>Random Forest</strong>
# MAGIC         <ul>
# MAGIC           <li>Maximum depth of trees</li>
# MAGIC           <li>Number of trees</li>
# MAGIC           <li>Number of features</li>
# MAGIC         </ul>
# MAGIC       </li>
# MAGIC       <li>
# MAGIC         <strong>Linear Regression</strong>
# MAGIC         <ul>
# MAGIC           <li>Regularization strength (alpha)</li>
# MAGIC         </ul>
# MAGIC       </li>
# MAGIC       <li>
# MAGIC         <strong>Neural Networks</strong>
# MAGIC         <ul>
# MAGIC           <li>Activation functions</li>
# MAGIC           <li>Number of neurons in each hidden layer</li>
# MAGIC         </ul>
# MAGIC       </li>
# MAGIC     </ul>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Hyperparameter Search Methods

# COMMAND ----------

# DBTITLE 1,B1. Overview of Search Methods
# MAGIC %md-sandbox
# MAGIC ### B1. Overview of Search Methods
# MAGIC
# MAGIC Three main approaches exist for searching hyperparameters. They sit on a spectrum — from exhaustive but expensive on one end, to adaptive and efficient on the other. We'll go deeper on each.
# MAGIC
# MAGIC <br>
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .ds-row { display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 240px; }
# MAGIC .ds-scenario { background: #F9F7F4; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(27,49,57,0.06); display: flex; flex-direction: column; }
# MAGIC .ds-scenario-band { background: var(--accent); color: #fff; padding: 14px 20px; text-align: center; font-size: 16pt; font-weight: 700; }
# MAGIC .ds-scenario-body { padding: 16px 20px; flex: 1; }
# MAGIC .ds-scenario-q { font-size: 12pt; font-style: italic; font-weight: 700; color: #0b2026; margin-bottom: 12px; text-align: center; }
# MAGIC .ds-scenario-text { font-size: 12pt; color: #0b2026; line-height: 1.6; }
# MAGIC .ds-scenario-text ul { margin: 12px 0; padding-left: 18px; }
# MAGIC .ds-scenario-text li { margin-bottom: 8px; }
# MAGIC .blue{--accent:#4299E0;} .green{--accent:#00A972;} .coral{--accent:#FF5F46;}
# MAGIC </style>
# MAGIC
# MAGIC <div class="ds-row">
# MAGIC   <div class="ds-scenario blue">
# MAGIC     <div class="ds-scenario-band">Grid Search</div>
# MAGIC     <div class="ds-scenario-body">
# MAGIC       <div class="ds-scenario-q">"Exhaustive brute-force search"</div>
# MAGIC       <div class="ds-scenario-text">
# MAGIC         Tries every combination from a predefined grid.
# MAGIC         <ul>
# MAGIC           <li><span style="color:#388E3C;">✓ Evaluates & picks the best</span></li>
# MAGIC           <li><span style="color:#D32F2F;">✗ Computationally expensive</span></li>
# MAGIC           <li><span style="color:#D32F2F;">✗ Scales poorly with dimensions</span></li>
# MAGIC         </ul>
# MAGIC       </div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC   <div class="ds-scenario green">
# MAGIC     <div class="ds-scenario-band">Random Search</div>
# MAGIC     <div class="ds-scenario-body">
# MAGIC       <div class="ds-scenario-q">"Random sampling of combinations"</div>
# MAGIC       <div class="ds-scenario-text">
# MAGIC         Samples combinations randomly from specified distributions.
# MAGIC         <ul>
# MAGIC           <li><span style="color:#388E3C;">✓ More efficient than grid search</span></li>
# MAGIC           <li><span style="color:#388E3C;">✓ Better coverage of search space</span></li>
# MAGIC           <li><span style="color:#D32F2F;">✗ No guarantee of finding best</span></li>
# MAGIC         </ul>
# MAGIC       </div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC   <div class="ds-scenario coral">
# MAGIC     <div class="ds-scenario-band">Bayesian Optimization</div>
# MAGIC     <div class="ds-scenario-body">
# MAGIC       <div class="ds-scenario-q">"Adaptive, model-based search"</div>
# MAGIC       <div class="ds-scenario-text">
# MAGIC         Uses results from previous trials to decide what to try next.
# MAGIC         <ul>
# MAGIC           <li><span style="color:#388E3C;">✓ Most efficient (fewer trials)</span></li>
# MAGIC           <li><span style="color:#388E3C;">✓ Focuses on promising regions</span></li>
# MAGIC           <li><span style="color:#D32F2F;">✗ More complex to implement</span></li>
# MAGIC         </ul>
# MAGIC       </div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <!-- Spectrum indicator -->
# MAGIC <div style="margin-top: 32px; display: flex; align-items: center; justify-content: space-between;">
# MAGIC   <span style="font-size:12pt; color:#888;">Exhaustive · Expensive</span>
# MAGIC   <div style="flex:1; margin: 0 16px; position: relative;">
# MAGIC     <svg width="100%" height="24" viewBox="0 0 520 24" style="display:block;">
# MAGIC       <line x1="10" y1="12" x2="510" y2="12" stroke="#bbb" stroke-width="2"/>
# MAGIC       <polygon points="505,7 515,12 505,17" fill="#bbb"/>
# MAGIC     </svg>
# MAGIC   </div>
# MAGIC   <span style="font-size:12pt; color:#888;">Adaptive · Efficient</span>
# MAGIC </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,B2. Grid Search
# MAGIC %md-sandbox
# MAGIC ### B2. Grid Search
# MAGIC
# MAGIC Grid Search is the brute-force approach — enumerate every combination of hyperparameters you care about and try them all. It evaluates each using cross-validation and picks the best. Simple and easy to reason about, but it scales terribly.
# MAGIC
# MAGIC **How it works:**
# MAGIC - Define discrete values for each hyperparameter
# MAGIC - Evaluate every unique combination, typically using cross-validation
# MAGIC - Select the combination with the best score
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; justify-content: center;">
# MAGIC <svg width="100%" viewBox="0 0 600 430" role="img" style="font-family: sans-serif; display: block; max-width: 750px; margin: 0 auto;">
# MAGIC
# MAGIC   <!-- Top loss rectangle -->
# MAGIC   <rect x="120" y="58" width="240" height="78" fill="#F6F6E8"/>
# MAGIC   <!-- Top Loss labels -->
# MAGIC   <text x="250" y="50" text-anchor="middle" font-size="14" font-weight="600" fill="#1B3139">Hyperparameter 1</text>
# MAGIC   <!-- Top Loss text -->
# MAGIC   <text x="132" y="130" font-size="17" font-style="italic" font-weight="600" fill="#1B3139" opacity="0.95">LOSS</text>
# MAGIC   <!-- Right loss rectangle -->
# MAGIC   <rect x="58" y="136" width="62" height="240" fill="#F6F6E8"/>
# MAGIC   <!-- Right Loss labels -->
# MAGIC   <text x="38" y="256" text-anchor="middle" font-size="14" font-weight="600" fill="#1B3139" transform="rotate(-90 38 256)">Hyperparameter 2</text>
# MAGIC   <!-- Right Loss text -->
# MAGIC   <text x="88" y="355" font-size="17" font-style="italic" font-weight="600" fill="#1B3139" opacity="0.95" transform="rotate(-90 88 330)">LOSS</text>
# MAGIC
# MAGIC   <!-- Top marginal loss curve -->
# MAGIC   <path d="M120,82 C142,80 152,112 175,116 C198,120 214,96 236,90 C255,85 268,96 280,116 C294,136 316,132 334,114 C346,102 353,95 360,90" fill="none" stroke="#2D2D2D" stroke-width="2.5" stroke-linecap="round"/>
# MAGIC
# MAGIC   <!-- Left marginal loss curve -->
# MAGIC   <path d="M86,136 C88,156 80,170 86,188 C92,208 97,224 90,244 C82,266 79,284 85,302 C92,322 86,344 86,376" fill="none" stroke="#2D2D2D" stroke-width="2.5" stroke-linecap="round"/>
# MAGIC
# MAGIC   <!-- Main search space -->
# MAGIC   <rect x="120" y="136" width="240" height="240" fill="#FFFFFF" stroke="#1B3139" stroke-width="2.5"/>
# MAGIC
# MAGIC   <!-- Axis projection circles for distinct x values -->
# MAGIC   <circle cx="150" cy="100" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="210" cy="104" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="270" cy="102" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="330" cy="118" r="6.5" fill="none" stroke="#FF3621" stroke-width="2.5"/>
# MAGIC
# MAGIC   <!-- Axis projection circles for distinct y values -->
# MAGIC   <circle cx="84" cy="165" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="93" cy="225" r="6.5" fill="none" stroke="#FF3621" stroke-width="2.5"/>
# MAGIC   <circle cx="82" cy="285" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="87" cy="345" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC
# MAGIC   <!-- 4x4 grid search samples colored by loss -->
# MAGIC   <circle cx="150" cy="165" r="12" fill="#111111" stroke="#666666" stroke-width="1.2"/>
# MAGIC   <circle cx="210" cy="165" r="12" fill="#222222" stroke="#666666" stroke-width="1.2"/>
# MAGIC   <circle cx="270" cy="165" r="12" fill="#383838" stroke="#666666" stroke-width="1.2"/>
# MAGIC   <circle cx="330" cy="165" r="12" fill="#505050" stroke="#666666" stroke-width="1.2"/>
# MAGIC
# MAGIC   <circle cx="150" cy="225" r="12" fill="#7A7A7A" stroke="#8A8A8A" stroke-width="1.2"/>
# MAGIC   <circle cx="210" cy="225" r="12" fill="#949494" stroke="#9C9C9C" stroke-width="1.2"/>
# MAGIC   <circle cx="270" cy="225" r="12" fill="#A5A5A5" stroke="#9E9E9E" stroke-width="1.2"/>
# MAGIC   <circle cx="330" cy="225" r="12" fill="#B2B2B2" stroke="#A0A0A0" stroke-width="1.2"/>
# MAGIC   <polygon points="330,219 331.5,223 335.7,223.1 332.4,225.8 333.5,229.9 330,227.5 326.5,229.9 327.6,225.8 324.3,223.1 328.5,223" fill="#1B3139" stroke="#1B3139" stroke-width="1.5" pointer-events="none"/>
# MAGIC
# MAGIC   <circle cx="150" cy="285" r="12" fill="#D8D8D8" stroke="#BEBEBE" stroke-width="1.2"/>
# MAGIC   <circle cx="210" cy="285" r="12" fill="#EEEEEE" stroke="#D0D0D0" stroke-width="1.2"/>
# MAGIC   <circle cx="270" cy="285" r="12" fill="#EFEECF" stroke="#D4D0A7" stroke-width="1.2"/>
# MAGIC   <circle cx="330" cy="285" r="12" fill="#DFDC88" stroke="#C2BE6B" stroke-width="1.2"/>
# MAGIC
# MAGIC   <circle cx="150" cy="345" r="12" fill="#D7DB56" stroke="#B5B941" stroke-width="1.2"/>
# MAGIC   <circle cx="210" cy="345" r="12" fill="#F1C34A" stroke="#CFA236" stroke-width="1.2"/>
# MAGIC   <circle cx="270" cy="345" r="12" fill="#F28D33" stroke="#CC7121" stroke-width="1.2"/>
# MAGIC   <circle cx="330" cy="345" r="12" fill="#FF6C4E" stroke="#CF4F36" stroke-width="1.2"/>
# MAGIC
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <p style="font-size: 12pt; color: #555; margin: 8px auto; max-width: 750px;">The color gradient (<strong>black → grey → yellow → orange</strong>) indicates the <strong>order of evaluation</strong>. The ★ marks the combination with the lowest combined loss as indicated by the marginal loss curves.</p>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Grid Search Trade-offs
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC   <li><strong>Simple and easy to reason about</strong></li>
# MAGIC   <li><strong>Can be computationally expensive</strong></li>
# MAGIC   <li><strong>Scales terribly</strong> — 5 hyperparameters × 10 values each = 100,000 combinations</li>
# MAGIC   <li><strong>Use only when the search space is small</strong></li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,B3. Random Search
# MAGIC %md-sandbox
# MAGIC ### B3. Random Search
# MAGIC
# MAGIC Random Search samples hyperparameter combinations randomly. Counterintuitively, this is often more efficient than grid search — research shows that when only a few hyperparameters actually matter, random sampling explores those important dimensions better in fewer trials.
# MAGIC
# MAGIC **How it works:**
# MAGIC - Define distributions for each hyperparameter
# MAGIC - Sample random combinations
# MAGIC - Evaluate each and select the best
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; justify-content: center;">
# MAGIC <svg width="100%" viewBox="0 0 600 430" role="img" style="font-family: sans-serif; display: block; max-width: 750px; margin: 0 auto;">
# MAGIC
# MAGIC   <!-- Top loss rectangle -->
# MAGIC   <rect x="120" y="58" width="240" height="78" fill="#F6F6E8"/>
# MAGIC   <!-- Top Loss labels -->
# MAGIC   <text x="250" y="50" text-anchor="middle" font-size="14" font-weight="600" fill="#1B3139">Hyperparameter 1</text>
# MAGIC   <!-- Top Loss text -->
# MAGIC   <text x="132" y="130" font-size="17" font-style="italic" font-weight="600" fill="#1B3139" opacity="0.95">LOSS</text>
# MAGIC   <!-- Left loss rectangle -->
# MAGIC   <rect x="58" y="136" width="62" height="240" fill="#F6F6E8"/>
# MAGIC   <!-- Left Loss labels -->
# MAGIC   <text x="38" y="256" text-anchor="middle" font-size="14" font-weight="600" fill="#1B3139" transform="rotate(-90 38 256)">Hyperparameter 2</text>
# MAGIC   <!-- Left Loss text -->
# MAGIC   <text x="88" y="355" font-size="17" font-style="italic" font-weight="600" fill="#1B3139" opacity="0.95" transform="rotate(-90 88 330)">LOSS</text>
# MAGIC
# MAGIC   <!-- Top marginal loss curve -->
# MAGIC   <path d="M120,72 C142,70 152,102 175,106 C198,110 214,86 236,80 C255,75 268,86 280,106 C294,126 316,122 334,104 C346,92 353,85 360,80" fill="none" stroke="#2D2D2D" stroke-width="2.5" stroke-linecap="round"/>
# MAGIC
# MAGIC   <!-- Left marginal loss curve -->
# MAGIC   <path d="M86,136 C88,156 80,170 86,188 C92,208 97,224 90,244 C82,266 79,284 85,302 C92,322 86,344 86,376" fill="none" stroke="#2D2D2D" stroke-width="2.5" stroke-linecap="round"/>
# MAGIC
# MAGIC   <!-- Main search space -->
# MAGIC   <rect x="120" y="136" width="240" height="240" fill="#FFFFFF" stroke="#1B3139" stroke-width="2.5"/>
# MAGIC
# MAGIC   <!-- Axis projection circles for random x values -->
# MAGIC   <circle cx="150" cy="90" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="170" cy="105" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="178" cy="106" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="195" cy="103" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="198" cy="101" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="226" cy="84" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="272" cy="94" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="298" cy="119" r="6.5" fill="none" stroke="#FF3621" stroke-width="2.5"/>
# MAGIC   <circle cx="306" cy="119" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="318" cy="116" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="326" cy="111" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="330" cy="108" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="332" cy="106" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="336" cy="102" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC
# MAGIC   <!-- Axis projection circles for random y values -->
# MAGIC   <circle cx="84" cy="165" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="86" cy="188" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="91" cy="205" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="93" cy="225" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="82" cy="276" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="83" cy="294" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="87" cy="308" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="88" cy="320" r="6.5" fill="none" stroke="#FF3621" stroke-width="2.5"/>
# MAGIC   <circle cx="88" cy="340" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="87" cy="348" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="87" cy="352" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC
# MAGIC   <!-- Random search samples colored by loss -->
# MAGIC   <circle cx="150" cy="165" r="12" fill="#F28D33" stroke="#CC7121" stroke-width="1.2"/>
# MAGIC   <circle cx="170" cy="225" r="12" fill="#111111" stroke="#666666" stroke-width="1.2"/>
# MAGIC   <circle cx="198" cy="205" r="12" fill="#222222" stroke="#666666" stroke-width="1.2"/>
# MAGIC   <circle cx="178" cy="276" r="12" fill="#9D9D9D" stroke="#8F8F8F" stroke-width="1.2"/>
# MAGIC   <circle cx="150" cy="308" r="12" fill="#D8D8D8" stroke="#BEBEBE" stroke-width="1.2"/>
# MAGIC   <circle cx="195" cy="294" r="12" fill="#D7DB56" stroke="#B5B941" stroke-width="1.2"/>
# MAGIC   <circle cx="170" cy="340" r="12" fill="#EFC044" stroke="#CFA030" stroke-width="1.2"/>
# MAGIC   <circle cx="226" cy="352" r="12" fill="#F1C34A" stroke="#CFA236" stroke-width="1.2"/>
# MAGIC   <circle cx="272" cy="225" r="12" fill="#B8B8B8" stroke="#A6A6A6" stroke-width="1.2"/>
# MAGIC   <circle cx="298" cy="320" r="12" fill="#EEEEEE" stroke="#D0D0D0" stroke-width="1.2"/>
# MAGIC   <polygon points="298,314 299.5,318 303.7,318.1 300.4,320.8 301.5,324.9 298,322.5 294.5,324.9 295.6,320.8 292.3,318.1 296.5,318" fill="#1B3139" stroke="#1B3139" stroke-width="1.5" pointer-events="none"/>
# MAGIC   <circle cx="318" cy="188" r="12" fill="#8F8F8F" stroke="#838383" stroke-width="1.2"/>
# MAGIC   <circle cx="332" cy="276" r="12" fill="#EFEECF" stroke="#D4D0A7" stroke-width="1.2"/>
# MAGIC   <circle cx="336" cy="308" r="12" fill="#DCD98A" stroke="#C2BE6B" stroke-width="1.2"/>
# MAGIC   <circle cx="306" cy="348" r="12" fill="#505050" stroke="#666666" stroke-width="1.2"/>
# MAGIC   <circle cx="330" cy="340" r="12" fill="#2C2C2C" stroke="#666666" stroke-width="1.2"/>
# MAGIC   <circle cx="326" cy="165" r="12" fill="#4A4A4A" stroke="#666666" stroke-width="1.2"/>
# MAGIC
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Random Search Trade-offs
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC   <li><strong>More efficient than grid</strong> when only a few hyperparameters actually drive performance</li>
# MAGIC   <li><strong>Explores important dimensions</strong> better in fewer trials</li>
# MAGIC   <li><strong>Does not guarantee</strong> the optimal combination</li>
# MAGIC   <li><strong>A much better default</strong> than grid search for medium-sized search spaces</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,B4. Bayesian Optimization
# MAGIC %md-sandbox
# MAGIC ### B4. Bayesian Optimization
# MAGIC
# MAGIC Bayesian Optimization gets smarter as it goes — it builds a model of which hyperparameter regions look promising based on past trial results, then focuses new trials on those regions. The **Tree of Parzen Estimators (TPE)** is a common implementation and the default algorithm in Optuna.
# MAGIC
# MAGIC **How it works:**
# MAGIC - Build a surrogate model (probability model) of the objective function
# MAGIC - Use an acquisition function to decide where to sample next
# MAGIC - Update the model with each new evaluation
# MAGIC - Focus on regions likely to contain the optimum
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; justify-content: center;">
# MAGIC <svg width="100%" viewBox="0 0 600 430" role="img" style="font-family: sans-serif; display: block; max-width: 750px; margin: 0 auto;">
# MAGIC   <title>Bayesian optimization focuses sampling on promising hyperparameter regions</title>
# MAGIC
# MAGIC   <!-- Top loss panel -->
# MAGIC   <rect x="120" y="58" width="240" height="78" fill="#F6F6E8"/>
# MAGIC   <text x="250" y="50" text-anchor="middle" font-size="14" font-weight="600" fill="#1B3139">Hyperparameter 1</text>
# MAGIC   <text x="132" y="130" font-size="17" font-style="italic" font-weight="600" fill="#1B3139" opacity="0.95">LOSS</text>
# MAGIC
# MAGIC   <!-- Left loss panel -->
# MAGIC   <rect x="58" y="136" width="62" height="240" fill="#F6F6E8"/>
# MAGIC   <text x="38" y="256" text-anchor="middle" font-size="14" font-weight="600" fill="#1B3139" transform="rotate(-90 38 256)">Hyperparameter 2</text>
# MAGIC   <text x="88" y="355" font-size="17" font-style="italic" font-weight="600" fill="#1B3139" opacity="0.95" transform="rotate(-90 88 330)">LOSS</text>
# MAGIC
# MAGIC   <!-- Top marginal loss curve — clear minimum toward right where Bayesian focuses -->
# MAGIC   <path d="M120,72 C142,70 152,102 175,106 C198,110 214,86 236,80 C255,75 268,86 280,106 C294,126 316,122 334,104 C346,92 353,85 360,80" fill="none" stroke="#2D2D2D" stroke-width="2.5" stroke-linecap="round"/>
# MAGIC
# MAGIC   <!-- Left marginal loss curve — minimum in upper-middle range -->
# MAGIC   <path d="M86,136 C88,156 80,170 86,188 C92,208 97,224 90,244 C82,266 79,284 85,302 C92,322 86,344 86,376" fill="none" stroke="#2D2D2D" stroke-width="2.5" stroke-linecap="round"/>
# MAGIC
# MAGIC   <!-- Main search space -->
# MAGIC   <rect x="120" y="136" width="240" height="240" fill="#FFFFFF" stroke="#1B3139" stroke-width="2.5"/>
# MAGIC
# MAGIC   <!-- Top projection circles: one per unique HP1 value across all 16 samples -->
# MAGIC   <circle cx="152" cy="92" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="155" cy="95" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="178" cy="106" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="252" cy="80" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="266" cy="88" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="268" cy="90" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="278" cy="103" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="284" cy="111" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="294" cy="118" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="300" cy="119" r="6.5" fill="none" stroke="#FF3621" stroke-width="2.5"/>
# MAGIC   <circle cx="312" cy="118" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="316" cy="117" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="324" cy="112" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="328" cy="109" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="338" cy="100" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC
# MAGIC   <!-- Left projection circles: one per unique HP2 value across all 16 samples -->
# MAGIC   <circle cx="84" cy="170" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="90" cy="200" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="92" cy="210" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="93" cy="216" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="93" cy="220" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="93" cy="226" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="93" cy="230" r="6.5" fill="none" stroke="#FF3621" stroke-width="2.5"/>
# MAGIC   <circle cx="92" cy="236" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="92" cy="238" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="91" cy="240" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="89" cy="248" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="87" cy="252" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="88" cy="338" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC   <circle cx="88" cy="342" r="6.5" fill="none" stroke="#2D2D2D" stroke-width="2"/>
# MAGIC
# MAGIC   <!-- Exploratory points: a few scattered dark samples from early exploration -->
# MAGIC   <circle cx="152" cy="170" r="12" fill="#111111" stroke="#666666" stroke-width="1.2"/>
# MAGIC   <circle cx="178" cy="200" r="12" fill="#222222" stroke="#666666" stroke-width="1.2"/>
# MAGIC   <circle cx="155" cy="338" r="12" fill="#383838" stroke="#666666" stroke-width="1.2"/>
# MAGIC   <circle cx="328" cy="342" r="12" fill="#4A4A4A" stroke="#666666" stroke-width="1.2"/>
# MAGIC
# MAGIC   <!-- Convergence cluster: densely sampled promising region (Bayesian exploitation) -->
# MAGIC   <circle cx="252" cy="216" r="12" fill="#8F8F8F" stroke="#838383" stroke-width="1.2"/>
# MAGIC   <circle cx="268" cy="200" r="12" fill="#9D9D9D" stroke="#8F8F8F" stroke-width="1.2"/>
# MAGIC   <circle cx="284" cy="220" r="12" fill="#B8B8B8" stroke="#A6A6A6" stroke-width="1.2"/>
# MAGIC   <circle cx="300" cy="210" r="12" fill="#D8D8D8" stroke="#BEBEBE" stroke-width="1.2"/>
# MAGIC   <circle cx="316" cy="226" r="12" fill="#EFEECF" stroke="#D4D0A7" stroke-width="1.2"/>
# MAGIC   <circle cx="278" cy="236" r="12" fill="#D7DB56" stroke="#B5B941" stroke-width="1.2"/>
# MAGIC   <circle cx="294" cy="248" r="12" fill="#F1C34A" stroke="#CFA236" stroke-width="1.2"/>
# MAGIC   <circle cx="312" cy="240" r="12" fill="#F28D33" stroke="#CC7121" stroke-width="1.2"/>
# MAGIC   <circle cx="324" cy="216" r="12" fill="#EEEEEE" stroke="#D0D0D0" stroke-width="1.2"/>
# MAGIC   <circle cx="266" cy="252" r="12" fill="#DCD98A" stroke="#C2BE6B" stroke-width="1.2"/>
# MAGIC   <circle cx="300" cy="230" r="12" fill="#DFDB80" stroke="#C8C060" stroke-width="1.2"/>
# MAGIC   <polygon points="300,224 301.5,228 305.7,228.1 302.4,230.8 303.5,234.9 300,232.5 296.5,234.9 297.6,230.8 294.3,228.1 298.5,228" fill="#1B3139" stroke="#1B3139" stroke-width="1.5" pointer-events="none"/>
# MAGIC   <circle cx="338" cy="238" r="12" fill="#A0A0A0" stroke="#909090" stroke-width="1.2"/>
# MAGIC   
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Bayesian Optimization Trade-offs
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC   <li><strong>Usually beats grid and random search</strong> for the same compute budget on real problems</li>
# MAGIC   <li><strong>Requires fewer trials</strong> to find good solutions</li>
# MAGIC   <li><strong>Added complexity</strong> — but Optuna handles that for us</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Validation and Cross-Validation

# COMMAND ----------

# DBTITLE 1,C1. The Validation Problem
# MAGIC %md-sandbox
# MAGIC ### C1. The Validation Problem
# MAGIC
# MAGIC Model validation ensures that hyperparameter tuning does not lead to overfitting. In the simplest approach, data is split into **training** and **test** sets — but repeatedly evaluating against the test set during tuning leaks information and biases results.
# MAGIC
# MAGIC The standard solution is a **three-way split**: training, validation, and test. 
# MAGIC  - For each candidate set of hyperparameters, the model is trained on the training set and evaluated on the validation set. 
# MAGIC  - The best hyperparameters are selected based on validation performance
# MAGIC  - Then the model is retrained on the combined training + validation data and evaluated **once** on the test set for a final, unbiased performance estimate.
# MAGIC
# MAGIC The basic idea for every candidate set of hyperparameters:
# MAGIC - Train a fresh model
# MAGIC - Evaluate it
# MAGIC - Compare. 
# MAGIC
# MAGIC Which dataset should you use for evaluation — just the validation split, or multiple folds of the training data? This is the core cross-validation question, and your answer determines how reliable your hyperparameter selection will be.
# MAGIC
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 225" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Classic 3-way Data Split</title>
# MAGIC
# MAGIC   <!-- Section container -->
# MAGIC   <rect x="40" y="15" width="780" height="195" rx="10" fill="#FFFFFF" stroke="#E0E0E0" stroke-width="1.5"/>
# MAGIC   <text x="60" y="33" font-size="11" font-weight="bold" fill="#666666">DATA SPLIT</text>
# MAGIC
# MAGIC   <!-- Target Variables bar (full width) -->
# MAGIC   <rect x="60" y="40" width="740" height="26" rx="5" fill="#FF3621"/>
# MAGIC   <text x="430" y="58" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">Target Variables</text>
# MAGIC
# MAGIC   <!-- Features bar (full width) -->
# MAGIC   <rect x="60" y="71" width="740" height="26" rx="5" fill="#1B3139"/>
# MAGIC   <text x="430" y="89" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">Features</text>
# MAGIC
# MAGIC   <!-- Split Strategy indicator -->
# MAGIC   <rect x="355" y="103" width="150" height="22" rx="5" fill="#FFF3E0" stroke="#F57C00" stroke-width="1"/>
# MAGIC   <text x="430" y="118" text-anchor="middle" font-size="11" font-weight="bold" fill="#E65100">Split Strategy</text>
# MAGIC
# MAGIC   <!-- Training bar -->
# MAGIC   <rect x="60" y="133" width="444" height="42" rx="5" fill="#F57C00"/>
# MAGIC   <text x="282" y="159" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">Training</text>
# MAGIC
# MAGIC   <!-- Validation bar -->
# MAGIC   <rect x="507" y="133" width="161" height="42" rx="5" fill="#00897B"/>
# MAGIC   <text x="587" y="159" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">Validation</text>
# MAGIC
# MAGIC   <!-- Test bar -->
# MAGIC   <rect x="671" y="133" width="129" height="42" rx="5" fill="#C62828"/>
# MAGIC   <text x="735" y="159" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">Test</text>
# MAGIC
# MAGIC   <!-- White divider lines through split bars -->
# MAGIC   <rect x="504" y="133" width="3" height="42" fill="#FFFFFF"/>
# MAGIC   <rect x="668" y="133" width="3" height="42" fill="#FFFFFF"/>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Limitations of the three-way split
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul>
# MAGIC   <li>Not enough data: Splitting into training, validation, and test sets can leave each set too small for reliable evaluation.</li>
# MAGIC   <li>Non-random splits: If the initial split isn't random, the model may overfit to patterns unique to one subset, reducing generalizability.</li>
# MAGIC   <li>Single validation set: Using only one validation set can give a misleading estimate of performance, especially if the split is unlucky.</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# DBTITLE 1,C2. K-Fold Cross-Validation
# MAGIC %md-sandbox
# MAGIC ### C2. K-Fold Cross-Validation
# MAGIC
# MAGIC K-fold cross-validation is a widely used and robust method for model validation during hyperparameter tuning. Instead of creating a single validation set, the training data is split into **k-subsets (folds)**.
# MAGIC
# MAGIC
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 700 400" role="img" style="font-family: sans-serif;">
# MAGIC   <title>K-Fold Cross Validation</title>
# MAGIC
# MAGIC  <!-- Legend (above first iteration, vertical rectangles) -->
# MAGIC  <rect x="90" y="80" width="50" height="18" rx="4" fill="#F57C00"/>
# MAGIC  <text x="150" y="90" font-size="13" fill="#1B3139" alignment-baseline="middle">Training fold</text>
# MAGIC  <rect x="240" y="80" width="50" height="18" rx="4" fill="#1B3139"/>
# MAGIC  <text x="300" y="90" font-size="13" fill="#1B3139" alignment-baseline="middle">Validation fold</text>
# MAGIC
# MAGIC   <!-- Iteration 1  -->
# MAGIC   <rect x="90" y="133" width="180" height="42" rx="5" fill="#F57C00"/>
# MAGIC   <text x="1" y="160" font-size="15" font-weight="bold" fill="#1B3139">Iteration 1:</text> 
# MAGIC
# MAGIC   <!-- White divider lines through split bars -->
# MAGIC   <rect x="150" y="133" width="3" height="42" fill="#FFFFFF"/>
# MAGIC   <rect x="210" y="133" width="3" height="42" fill="#FFFFFF"/>
# MAGIC   <text x="290" y="155" text-anchor="middle" font-size="16" font-weight="bold" fill="#1B3139">....</text> 
# MAGIC   <rect x="310" y="133" width="180" height="42" rx="5" fill="#F57C00"/>
# MAGIC   <rect x="370" y="133" width="3" height="42" fill="#FFFFFF"/>
# MAGIC   <rect x="430" y="133" width="3" height="42" fill="#FFFFFF"/>
# MAGIC   <rect x="434" y="133" width="55" height="42" rx="5" fill="#1B3139"/>
# MAGIC   <defs>
# MAGIC     <marker id="arr_a2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="strokeWidth">
# MAGIC       <polygon points="0,2 7,4 0,6" fill="#F57C00"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC   <path d="M500 154 L540 154" stroke="#F57C00" stroke-width="2" fill="none" marker-end="url(#arr_a2)"/>
# MAGIC   <text x="555" y="156" font-size="15" font-weight="bold" fill="#1B3139">Error (E₁)</text> 
# MAGIC
# MAGIC <!-- Iteration 2  -->
# MAGIC <rect x="90" y="185" width="180" height="42" rx="5" fill="#F57C00"/>
# MAGIC <text x="1" y="212" font-size="15" font-weight="bold" fill="#1B3139">Iteration 2:</text> 
# MAGIC
# MAGIC <!-- White divider lines through split bars -->
# MAGIC <rect x="150" y="185" width="3" height="42" fill="#FFFFFF"/>
# MAGIC <rect x="210" y="185" width="3" height="42" fill="#FFFFFF"/>
# MAGIC <text x="290" y="207" text-anchor="middle" font-size="16" font-weight="bold" fill="#1B3139">....</text> 
# MAGIC <rect x="310" y="185" width="180" height="42" rx="5" fill="#F57C00"/>
# MAGIC <rect x="374" y="185" width="3" height="42" fill="#FFFFFF"/>
# MAGIC <rect x="377" y="185" width="55" height="42" rx="5" fill="#1B3139"/>
# MAGIC <rect x="430" y="185" width="3" height="42" fill="#FFFFFF"/>
# MAGIC
# MAGIC <path d="M500 206 L540 206" stroke="#F57C00" stroke-width="2" fill="none" marker-end="url(#arr_a2)"/>
# MAGIC <text x="555" y="208" font-size="15" font-weight="bold" fill="#1B3139">Error (E₂)</text>
# MAGIC
# MAGIC <!-- Dots  -->
# MAGIC <rect x="90" y="230" width="40" height="15" rx="5" fill="#FFFFFF"/>
# MAGIC <text x="35" y="237" font-size="16" font-weight="bold" fill="#1B3139">.</text>
# MAGIC <text x="35" y="244" font-size="16" font-weight="bold" fill="#1B3139">.</text>
# MAGIC <text x="35" y="251" font-size="16" font-weight="bold" fill="#1B3139">.</text>
# MAGIC
# MAGIC <!-- Dots under "...." -->
# MAGIC <rect x="290" y="230" width="40" height="15" rx="5" fill="#FFFFFF"/>
# MAGIC <text x="290" y="237" font-size="16" font-weight="bold" fill="#1B3139">.</text>
# MAGIC <text x="290" y="244" font-size="16" font-weight="bold" fill="#1B3139">.</text>
# MAGIC <text x="290" y="251" font-size="16" font-weight="bold" fill="#1B3139">.</text>
# MAGIC
# MAGIC <!-- Iteration N  -->
# MAGIC <rect x="90" y="265" width="180" height="42" rx="5" fill="#F57C00"/>
# MAGIC <text x="1" y="292" font-size="15" font-weight="bold" fill="#1B3139">Iteration N:</text> 
# MAGIC
# MAGIC <!-- White divider lines through split bars -->
# MAGIC <rect x="90" y="265" width="60" height="42" rx="5" fill="#1B3139"/>
# MAGIC <rect x="151" y="265" width="3" height="42" fill="#FFFFFF"/>
# MAGIC <rect x="210" y="265" width="3" height="42" fill="#FFFFFF"/>
# MAGIC <text x="290" y="287" text-anchor="middle" font-size="16" font-weight="bold" fill="#1B3139">....</text> 
# MAGIC <rect x="310" y="265" width="180" height="42" rx="5" fill="#F57C00"/>
# MAGIC <rect x="370" y="265" width="3" height="42" fill="#FFFFFF"/>
# MAGIC <rect x="374" y="185" width="3" height="42" rx="5" fill="#FFFFFF"/>
# MAGIC <rect x="430" y="265" width="3" height="42" fill="#FFFFFF"/>
# MAGIC
# MAGIC <path d="M500 286 L540 286" stroke="#F57C00" stroke-width="2" fill="none" marker-end="url(#arr_a2)"/>
# MAGIC <text x="555" y="288" font-size="15" font-weight="bold" fill="#1B3139">Error (Eₙ)</text>
# MAGIC
# MAGIC <!-- Final pass -->
# MAGIC <rect x="90" y="320" width="400" height="30" rx="4" fill="#FFFFFF" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC <text x="275" y="340" text-anchor="middle" font-size="13" fill="#1B3139" font-weight="bold">Training with Optimal Hyperparameters</text>
# MAGIC <text x="1" y="340" font-size="15" font-weight="bold" fill="#1B3139">Final Pass:</text>
# MAGIC <rect x="535" y="320" width="105" height="30" rx="4" fill="#FFFFFF" stroke="#C62828" stroke-width="1.5"/>
# MAGIC <text x="587" y="340" text-anchor="middle" font-size="13" fill="#C62828" font-weight="bold">Test</text>
# MAGIC </svg>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="font-size: 16px; margin: 24px 0;">
# MAGIC   <strong>Average validation error:</strong>
# MAGIC   <span style="display: inline-block; margin-left: 8px;">
# MAGIC     <span style="vertical-align: middle;">
# MAGIC       <span style="font-family: 'STIX', 'Times New Roman', serif;">
# MAGIC         <em>E</em><sub>avg</sub> = (1 / <em>K</em>) &sum;<sub>i=1</sub><sup>K</sup> <em>E</em><sub>i</sub>
# MAGIC       </span>
# MAGIC     </span>
# MAGIC   </span>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC How does K-Fold Cross-Validation work?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">The model is trained and validated k times — each time using a different fold for validation and the remaining folds for training. This process produces <strong>k independent estimates of validation performance</strong>, offering a more reliable measure of how the model will generalize to unseen data.</p>
# MAGIC
# MAGIC <p>After identifying the best hyperparameters, the model is retrained on the full training set (all folds combined) and finally evaluated on the test set.</p>
# MAGIC
# MAGIC <p>Because it reduces the risk of bias or overfitting caused by a single train/validation split, k-fold cross-validation is considered the <strong>gold standard for hyperparameter tuning</strong>, especially when working with limited data.</p>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C3. Tuning Can Be Expensive!
# MAGIC
# MAGIC Combining hyperparameter search with cross-validation multiplies the number of models you must build. A simple grid search example illustrates the cost:
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; gap: 30px; align-items: flex-start;">
# MAGIC
# MAGIC <div>
# MAGIC <p><strong>Grid Search Example</strong></p>
# MAGIC <table style="border-collapse: collapse; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 10px 16px; color: #ffffff; border-bottom: 3px solid #FF3621;">Tree Depth</th>
# MAGIC       <th style="padding: 10px 16px; color: #ffffff; border-bottom: 3px solid #FF3621;">Number of Trees</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 10px 16px; text-align: center;">5</td>
# MAGIC       <td style="padding: 10px 16px; text-align: center;">2</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 10px 16px; text-align: center;">8</td>
# MAGIC       <td style="padding: 10px 16px; text-align: center;">4</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC </div>
# MAGIC <!-- Arrow between tables -->
# MAGIC <div style="display: flex; justify-content: center; align-items: center; height: 80px; margin-top: 100px;">
# MAGIC   <svg width="60" height="30">
# MAGIC     <defs>
# MAGIC       <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
# MAGIC         <polygon points="0 0, 8 3, 0 6" fill="#1B3139"/>
# MAGIC       </marker>
# MAGIC     </defs>
# MAGIC     <line x1="10" y1="15" x2="50" y2="15" stroke="#1B3139" stroke-width="2" marker-end="url(#arrowhead)"/>
# MAGIC   </svg>
# MAGIC </div>
# MAGIC <div>
# MAGIC <p><strong>All Combinations</strong></p>
# MAGIC <table style="border-collapse: collapse; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 8px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 10px 14px; color: #ffffff;">Tree Depth</th>
# MAGIC       <th style="padding: 10px 14px; color: #ffffff;">Number of Trees</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC     <td style="padding: 8px 14px; text-align: center;">5</td>
# MAGIC     <td style="padding: 8px 14px; text-align: center;">2</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC     <td style="padding: 10px 14px; text-align: center;">5</td><td style="padding: 8px 14px; text-align: center;">4</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;"><td style="padding: 8px 14px; text-align: center;">8</td>
# MAGIC     <td style="padding: 8px 14px; text-align: center;">2</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC     <td style="padding: 8px 14px; text-align: center;">8</td>
# MAGIC     <td style="padding: 8px 14px; text-align: center;">4</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     When you combine grid search with 3-fold cross-validation, each hyperparameter combination is evaluated on three different train/validation splits. For 4 combinations, this means <strong>4 × 3 = 12 models</strong> are trained and validated. After tuning, a final model is typically retrained using the best hyperparameters on the full training set, bringing the total to <strong>13 models</strong>. This multiplication effect is why tuning can quickly become computationally expensive.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Optuna for Hyperparameter Optimization

# COMMAND ----------

# DBTITLE 1,D1. Popular Tools for Hyperparameter Optimization
# MAGIC %md-sandbox
# MAGIC ### D1. Popular Tools for Hyperparameter Optimization
# MAGIC
# MAGIC Several frameworks exist for automating hyperparameter search. The table below compares the most common options:
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Tool</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Scikit-learn</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;"><code>GridSearchCV</code> and <code>RandomizedSearchCV</code>: offer grid search and random search for hyperparameter tuning.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Hyperopt</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">A popular library for Bayesian hyperparameter optimization. <strong>Hyperopt is no longer maintained and is not included in Databricks Runtime ML after 16.4 LTS ML.</strong></td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Ray Tune</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">A scalable library for hyperparameter tuning, offering both grid and advanced search algorithms.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Optuna</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;"><strong>An open-source hyperparameter optimization framework to automate hyperparameter search.</strong> This is the tool used in this course.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Why Optuna?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1976d2; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC <p style="margin-top: 10px;">
# MAGIC Two big reasons. It’s <strong>framework-agnostic</strong> — works with PyTorch, TensorFlow, Keras, scikit-learn, XGBoost, LightGBM, anything you can wrap in a Python function. And it requires <strong>no framework-specific syntax</strong> — you write a standard objective function and Optuna handles the rest. That makes it the right default for mixed-framework teams.
# MAGIC </p>
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,D2. Optuna: Lightweight, Versatile, and Platform Agnostic
# MAGIC %md-sandbox
# MAGIC ### D2. Optuna: Lightweight, Versatile, and Platform Agnostic
# MAGIC
# MAGIC Optuna is an open-source hyperparameter optimization framework with a simple, Pythonic API — written entirely in Python with few dependencies and no framework-specific configuration files needed.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621; width: 160px;">Property</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Lightweight</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Requires minimal computational resources and is easy to install, making it suitable for environments where resources are limited. The small footprint means it adds little overhead to existing workflows.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Versatile</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Supports a wide range of ML tasks with various objective functions and multiple search space definition methods (<code>suggest_int</code>, <code>suggest_float</code>, <code>suggest_categorical</code>). Optimization algorithms include Grid Search, Random Search, and the default <strong>Tree-structured Parzen Estimator (TPE)</strong>.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Platform Agnostic</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Runs on any platform supporting Python — AWS, Google Cloud, Azure, or on-premises. Integrates with <strong>PyTorch, TensorFlow, Keras, Scikit-learn, XGBoost, LightGBM</strong>, and any model you can wrap in a Python function.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### D3. Optuna Terminology
# MAGIC
# MAGIC Optuna uses specific terminology for its optimization process:
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Term</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Definition</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Trial</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">A single call of the objective function — one set of hyperparameters evaluated.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Study</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">An optimization session, which is a collection of trials.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Parameter</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">A variable whose value is to be optimized (the hyperparameter being tuned).</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Objective Function</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">The function that trains, evaluates, and returns the metric to be optimized (typically loss or accuracy).</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     Optuna is designed to automate and accelerate hyperparameter optimization studies. Its flexible, Pythonic API lets you define dynamic search spaces and efficiently find optimal configurations, making it a powerful tool for tuning models in modern ML workflows.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,D4. The Hyperparameter Optimization Framework - Define the Objective Function
# MAGIC %md-sandbox
# MAGIC ### D4. The Hyperparameter Optimization Framework - Define the Objective Function
# MAGIC
# MAGIC The Optuna workflow breaks into three clean steps. 
# MAGIC
# MAGIC
# MAGIC <div style="max-width: 1100px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 300" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Optuna HPO Framework</title>
# MAGIC
# MAGIC   <!-- Step 1: Define Objective -->
# MAGIC   <rect x="20" y="45" width="220" height="155" rx="8" fill="#1B3139"/>
# MAGIC   <circle cx="40" cy="60" r="12" fill="#FF3621"/>
# MAGIC   <text x="40" y="65" text-anchor="middle" font-size="11" font-weight="bold" fill="#FFFFFF">1</text>
# MAGIC   <text x="130" y="80" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Define Objective</text>
# MAGIC   <text x="40" y="106" font-size="11" fill="#F9F7F4">def objective(trial):</text>
# MAGIC   <text x="50" y="124" font-size="11" fill="#F9F7F4">  search_space = ...</text>
# MAGIC   <text x="50" y="142" font-size="11" fill="#F9F7F4">  model = ...</text>
# MAGIC   <text x="50" y="160" font-size="11" fill="#F9F7F4">  ...</text>
# MAGIC   <text x="50" y="178" font-size="11" fill="#F9F7F4">  return metric</text>
# MAGIC
# MAGIC   <!-- Middle: Objective Function + MLflow -->
# MAGIC   <rect x="320" y="60" width="165" height="70" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="402" y="88" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565C0">Objective Function</text>
# MAGIC   <text x="402" y="108" text-anchor="middle" font-size="11" fill="#1565C0">+ MLflow logging</text>
# MAGIC
# MAGIC   <!-- Middle lower: Optuna Study -->
# MAGIC   <rect x="320" y="150" width="165" height="48" rx="8" fill="#1B3139"/>
# MAGIC   <text x="402" y="178" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Optuna Study</text>
# MAGIC
# MAGIC   <!-- Step 2: Create Study -->
# MAGIC   <rect x="580" y="45" width="220" height="155" rx="8" fill="#1B3139"/>
# MAGIC   <circle cx="600" cy="60" r="12" fill="#FF3621"/>
# MAGIC   <text x="600" y="65" text-anchor="middle" font-size="11" font-weight="bold" fill="#FFFFFF">2</text>
# MAGIC   <text x="690" y="80" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Create Study</text>
# MAGIC   <text x="595" y="110" font-size="11" fill="#F9F7F4">study = optuna</text>
# MAGIC   <text x="605" y="128" font-size="11" fill="#F9F7F4">.create_study(</text>
# MAGIC   <text x="615" y="146" font-size="11" fill="#F9F7F4">direction=&quot;maximize&quot;)</text>
# MAGIC   <text x="595" y="170" font-size="11" fill="#F9F7F4">study.optimize(</text>
# MAGIC   <text x="605" y="188" font-size="11" fill="#F9F7F4">objective, n_trials=N)</text>
# MAGIC
# MAGIC   <!-- Flow arrows -->
# MAGIC   <line x1="250" y1="112" x2="310" y2="112" stroke="#1B3139" stroke-width="2" marker-end="url(#arrow2)"/>
# MAGIC   <line x1="485" y1="112" x2="570" y2="112" stroke="#1B3139" stroke-width="2" marker-end="url(#arrow2)"/>
# MAGIC   <line x1="402" y1="132" x2="402" y2="142" stroke="#1B3139" stroke-width="2" marker-end="url(#arrow2)"/>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrow2" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
# MAGIC       <polygon points="0 0, 8 3, 0 6" fill="#1B3139"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Step 1 — Define the Objective Function
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">
# MAGIC This is the function Optuna calls repeatedly with different hyperparameter values — each call is a <strong>Trial</strong>. Inside the function, you use the <code>suggest</code> API to pull values from your search space, train the model, and return a performance metric (accuracy, loss, or whatever you're optimizing). Because Optuna uses a <strong>define-by-run approach</strong>, your search space can be dynamic and conditional — something that's hard to do cleanly with grid or random search.
# MAGIC </p>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,D5. The Hyperparameter Optimization Framework - Create, Optimize, Extract, and Analyze
# MAGIC %md-sandbox
# MAGIC ### D5. The Hyperparameter Optimization Framework - Create, Optimize, Extract, and Analyze
# MAGIC
# MAGIC
# MAGIC
# MAGIC <div style="max-width: 1100px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 300" role="img" style="font-family: sans-serif;">
# MAGIC
# MAGIC   <!-- Step 2: Create Study -->
# MAGIC   <rect x="40" y="40" width="220" height="150" rx="8" fill="#1B3139"/>
# MAGIC   <circle cx="60" cy="55" r="12" fill="#FF3621"/>
# MAGIC   <text x="60" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#FFFFFF">2</text>
# MAGIC   <text x="150" y="75" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Create Study</text>
# MAGIC   <text x="55" y="105" font-size="11" fill="#F9F7F4">study = optuna</text>
# MAGIC   <text x="65" y="123" font-size="11" fill="#F9F7F4">.create_study(</text>
# MAGIC   <text x="75" y="141" font-size="11" fill="#F9F7F4">direction=&quot;maximize&quot;)</text>
# MAGIC   <text x="55" y="165" font-size="11" fill="#F9F7F4">study.optimize(</text>
# MAGIC   <text x="65" y="183" font-size="11" fill="#F9F7F4">objective, n_trials=N)</text>
# MAGIC
# MAGIC   <!-- Arrow Create Study -> Trial Outputs -->
# MAGIC   <line x1="270" y1="115" x2="310" y2="115" stroke="#1B3139" stroke-width="2" marker-end="url(#arrow2)"/>
# MAGIC
# MAGIC   <!-- Trial Outputs table -->
# MAGIC   <rect x="320" y="48" width="180" height="135" rx="8" fill="#FFF3E0" stroke="#F57C00" stroke-width="1.5"/>
# MAGIC   <rect x="320" y="48" width="180" height="28" rx="8" fill="#F57C00"/>
# MAGIC   <text x="410" y="67" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Trial Outputs</text>
# MAGIC   <rect x="334" y="88" width="152" height="20" rx="3" fill="#FFB74D"/>
# MAGIC   <text x="410" y="102" text-anchor="middle" font-size="10" fill="#1B3139">Trial 1  |  score  |  params</text>
# MAGIC   <rect x="334" y="113" width="152" height="20" rx="3" fill="#FFA726"/>
# MAGIC   <text x="410" y="127" text-anchor="middle" font-size="10" fill="#1B3139">Trial 2  |  score  |  params</text>
# MAGIC   <rect x="334" y="138" width="152" height="20" rx="3" fill="#FB8C00"/>
# MAGIC   <text x="410" y="152" text-anchor="middle" font-size="10" fill="#FFFFFF">Trial N  |  score  |  params</text>
# MAGIC
# MAGIC   <!-- Arrow Trial Outputs -> Best Results -->
# MAGIC   <line x1="510" y1="115" x2="550" y2="115" stroke="#1B3139" stroke-width="2" marker-end="url(#arrow2)"/>
# MAGIC
# MAGIC   <!-- Step 3: Results -->
# MAGIC   <rect x="560" y="40" width="250" height="150" rx="8" fill="#1B3139"/>
# MAGIC   <circle cx="580" cy="55" r="12" fill="#FF3621"/>
# MAGIC   <text x="580" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#FFFFFF">3</text>
# MAGIC   <text x="685" y="75" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Get Best Results</text>
# MAGIC   <text x="575" y="105" font-size="11" fill="#F9F7F4">study.best_params</text>
# MAGIC   <text x="575" y="125" font-size="11" fill="#F9F7F4">study.best_trial</text>
# MAGIC   <text x="575" y="145" font-size="11" fill="#F9F7F4">study.best_trials</text>
# MAGIC   <text x="575" y="165" font-size="11" fill="#F9F7F4">study.best_value</text>
# MAGIC
# MAGIC   <defs>
# MAGIC     <marker id="arrow2" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
# MAGIC       <polygon points="0 0, 8 3, 0 6" fill="#1B3139"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Step 2 — Create and Optimize the Study
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">
# MAGIC <code>optuna.create_study()</code> initializes the optimization task and <code>study.optimize()</code> runs N trials against your objective. Setting <code>n_jobs=-1</code> parallelizes trials across the driver node's CPU cores. To scale across the cluster, use Joblib-Spark (<code>MlflowSparkStudy</code>) or Ray Tune.
# MAGIC </p>
# MAGIC
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Step 3 — Extract and Analyze the Best Trial
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">
# MAGIC Use <code>study.best_params</code> for the winning hyperparameters, <code>study.best_trial</code> for the full trial record, and <code>study.best_value</code> for the objective score. With the MLflow callback, each Optuna trial becomes a <strong>child run</strong> under a parent run — the experiments UI stays organized and you can drill into any single trial. Optuna also prunes obviously bad trials early, spending your compute budget more wisely than grid or random search.
# MAGIC </p>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### D6. Key Concepts — Search Space and Algorithms
# MAGIC
# MAGIC Optuna provides three key mechanisms for controlling the optimization process:
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Search Space Definition (Python Syntax)
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC Hyperparameter search space can be defined using functions such as:
# MAGIC <ul>
# MAGIC   <li><code>suggest_float()</code> — continuous; use <code>step=</code> for discrete and <code>log=True</code> for log-scale (replaces the older <code>suggest_uniform</code>, <code>suggest_discrete_uniform</code>, and <code>suggest_loguniform</code>)</li>
# MAGIC   <li><code>suggest_int()</code></li>
# MAGIC   <li><code>suggest_categorical()</code></li>
# MAGIC </ul>
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Sampling Strategy
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC Determines how to decide the next hyperparameter values. Continuously refines the search space using past results. Supported strategies: Grid Search, Random Search, <strong>Tree-structured Parzen Estimator (default)</strong>.
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Pruning Strategy
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC Early stopping halts unpromising trials based on intermediate results. Call <code>report()</code> and <code>should_prune()</code> after each step to activate pruning.
# MAGIC <br>
# MAGIC <em style="font-size: 11px;">*Not covered in this course.</em>
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,D6. Optuna–MLflow Integration
# MAGIC %md-sandbox
# MAGIC ### D7. Optuna–MLflow Integration
# MAGIC
# MAGIC Optuna's integration with MLflow allows for efficient tracking of hyperparameters and metrics across all Optuna trials. This is achieved using the `MLflowCallback` from the `optuna-integration` package — pass it to `study.optimize()` and every trial is automatically logged as a child MLflow run. A parent run groups all trials under a single experiment entry, keeping the Databricks Experiments UI organized and every trial drillable.
# MAGIC
# MAGIC **MLflowCallback — automatic trial logging**
# MAGIC
# MAGIC Set `tracking_uri` to `"databricks"` to use Databricks for tracking, `metric_name` to specify the metric to track, and `mlflow_kwargs` to pass additional arguments to MLflow such as the experiment ID:
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 13px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>from optuna_integration import MLflowCallback
# MAGIC import mlflow
# MAGIC mlflow_callback = MLflowCallback(
# MAGIC     tracking_uri="databricks",
# MAGIC     metric_name="accuracy",
# MAGIC     mlflow_kwargs={"experiment_id": "YOUR_EXPERIMENT_ID"},
# MAGIC )
# MAGIC study = optuna.create_study(direction="maximize")
# MAGIC study.optimize(objective, n_trials=50,
# MAGIC                callbacks=[mlflow_callback])</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC **Parent–Child Run Organization**
# MAGIC
# MAGIC Wrap `study.optimize()` in a parent `mlflow.start_run()` to group all trials under one run. After optimization, log the best trial’s metric and parameters to the parent for easy retrieval:
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 13px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>with mlflow.start_run() as parent_run:
# MAGIC     study.optimize(objective, n_trials=50,
# MAGIC                    callbacks=[mlflow_callback])
# MAGIC     best = study.best_trial
# MAGIC     mlflow.log_metric("best_accuracy", best.value)
# MAGIC     mlflow.log_params(best.params)</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     In Databricks Experiments UI, Optuna–MLflow integration organizes each hyperparameter study as a single parent run, with every trial logged as a child run. Each child run records its own hyperparameters and objective metric, while the parent run summarizes the best result. This structure makes it easy to compare all trials, review individual trial details, and track the full optimization process for reproducibility and governance.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     When integrating Optuna with MLflow on Databricks, ensure your <code>experiment_id</code> matches an existing MLflow experiment in your workspace. For robust model governance and deployment, Databricks recommends using <strong>Models in Unity Catalog</strong>, which provides unified lineage, versioning, and access control for all registered models.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,E. Conclusion
# MAGIC %md-sandbox
# MAGIC ## E. Conclusion
# MAGIC
# MAGIC In this lecture, you covered the fundamentals of hyperparameter tuning and the tools available on Databricks:
# MAGIC
# MAGIC 1. **What Are Hyperparameters?** — Hyperparameters are set before training and control how a model learns; tuning them is the process of finding the configuration that maximizes performance.
# MAGIC
# MAGIC 2. **Hyperparameter Search Methods** — Grid search is exhaustive but combinatorially expensive; random search explores the space more efficiently; Bayesian optimization (TPE) iteratively focuses on the most promising regions using past trial results.
# MAGIC
# MAGIC 3. **Validation and Cross-Validation** — A three-way train/validation/test split prevents test-set leakage during tuning, and K-fold cross-validation produces more robust hyperparameter estimates by rotating the validation fold across K iterations.
# MAGIC
# MAGIC 4. **Optuna for Hyperparameter Optimization** — Optuna's three-step workflow — define an objective function, run a study, extract `best_params`/`best_value` — integrates with MLflow via `MLflowCallback` to log every trial as a child run under a parent experiment.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
