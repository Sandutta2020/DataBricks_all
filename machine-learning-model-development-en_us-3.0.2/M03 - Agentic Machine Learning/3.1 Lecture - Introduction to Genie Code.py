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
# MAGIC # Lecture — Introduction to Genie Code
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This lecture introduces Genie Code — Databricks' AI coding and data assistant for developers and technical practitioners — and how it supports machine learning model development. You will learn how Genie Code addresses the challenges of traditional ML workflows, explore its key capabilities, understand platform integrations, and discover how to customize it with MCP connections, instructions, and skills.
# MAGIC
# MAGIC This lecture covers 4 sections that build on each other:
# MAGIC
# MAGIC - **A. The ML Development Challenge**. Why building ML models is complex, time-consuming work — and how Genie Code provides a natural-language solution that accelerates the entire process.
# MAGIC - **B. What Is Genie Code**. The core identity, design principles, and five key ML needs that Genie Code addresses — spanning ML models, pipelines, and dashboards.
# MAGIC - **C. Platform Integration and Customization**. How Genie Code integrates with Databricks services and how you customize it with MCP, instructions, and skills.
# MAGIC - **D. End-to-End Model Development**. A complete walkthrough from data exploration to deployed endpoint — all in one conversation.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC - Describe the challenges of traditional ML development workflows and how Genie Code addresses them.
# MAGIC - Describe the key ML capabilities of Genie Code on the Databricks platform.
# MAGIC - Customize Genie Code with MCP connections, instructions, and skills.
# MAGIC - Use Genie Code to perform end-to-end model development through natural language.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. The ML Development Challenge

# COMMAND ----------

# DBTITLE 1,A1. Building an ML Model Is a Lot of Work
# MAGIC %md-sandbox
# MAGIC ### A1. Building an ML Model Is a Lot of Work
# MAGIC
# MAGIC A lot of work goes into data preparation, feature engineering, model training, and evaluation — **what if we could make it easier?**
# MAGIC
# MAGIC The traditional ML development workflow involves many sequential steps, each requiring specialized expertise:
# MAGIC
# MAGIC <div style="max-width: 800px; margin: 20px auto;">
# MAGIC <svg width="100%" viewBox="0 0 760 205" style="font-family: sans-serif;">
# MAGIC
# MAGIC   <!-- Step 1 -->
# MAGIC   <rect x="10" y="20" width="160" height="50" rx="6" fill="#FF3621" opacity="0.9"/>
# MAGIC   <text x="90" y="40" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">1. Select &</text>
# MAGIC   <text x="90" y="55" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">input a dataset</text>
# MAGIC
# MAGIC   <!-- Arrow 1-2 -->
# MAGIC   <polygon points="180,40 180,50 190,45" fill="#1B3139"/>
# MAGIC
# MAGIC   <!-- Step 2 -->
# MAGIC   <rect x="205" y="20" width="160" height="50" rx="6" fill="#FF3621" opacity="0.9"/>
# MAGIC   <text x="285" y="50" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">2. Data Preparation</text>
# MAGIC
# MAGIC   <!-- Arrow 2-3 -->
# MAGIC   <polygon points="375,40 375,50 385,45" fill="#1B3139"/>
# MAGIC
# MAGIC   <!-- Step 3 -->
# MAGIC   <rect x="395" y="20" width="160" height="50" rx="6" fill="#FF3621" opacity="0.9"/>
# MAGIC   <text x="475" y="50" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">3. Feature Engineering</text>
# MAGIC
# MAGIC   <!-- Arrow 3-4 -->
# MAGIC   <polygon points="565,40 565,50 575,45" fill="#1B3139"/>
# MAGIC
# MAGIC   <!-- Step 4 -->
# MAGIC   <rect x="580" y="20" width="160" height="50" rx="6" fill="#FF3621" opacity="0.9"/>
# MAGIC   <text x="660" y="40" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">4. Training &</text>
# MAGIC   <text x="660" y="55" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">Model Selection</text>
# MAGIC
# MAGIC   <!-- Arrow 4-5 (straight down) -->
# MAGIC   <polygon points="655,75 665,75 660,85" fill="#1B3139"/>
# MAGIC
# MAGIC   <!-- Step 5 (under step 4) -->
# MAGIC   <rect x="580" y="100" width="160" height="50" rx="6" fill="#FF3621" opacity="0.9"/>
# MAGIC   <text x="660" y="120" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">5. Hyperparameter</text>
# MAGIC   <text x="660" y="135" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">Tuning</text>
# MAGIC
# MAGIC   <!-- Arrow 5-6 (pointing left) -->
# MAGIC   <polygon points="577,120 577,130 567,125" fill="#1B3139"/>
# MAGIC
# MAGIC   <!-- Step 6 (under step 3) -->
# MAGIC   <rect x="395" y="100" width="160" height="50" rx="6" fill="#FF3621" opacity="0.9"/>
# MAGIC   <text x="475" y="120" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">6. Explore Artifacts</text>
# MAGIC   <text x="475" y="135" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">&amp; Notebooks</text>
# MAGIC
# MAGIC   <!-- Arrow 6-7 (pointing left) -->
# MAGIC   <polygon points="390,120 390,130 380,125" fill="#1B3139"/>
# MAGIC
# MAGIC   <!-- Step 7 (under step 2) -->
# MAGIC   <rect x="205" y="100" width="160" height="50" rx="6" fill="#FF3621" opacity="0.9"/>
# MAGIC   <text x="285" y="130" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">7. Deploy</text>
# MAGIC
# MAGIC   <!-- Arrow 7-8 (pointing left) -->
# MAGIC   <polygon points="197,120 197,130 187,125" fill="#1B3139"/>
# MAGIC
# MAGIC   <!-- Step 8 (under step 1) -->
# MAGIC   <rect x="10" y="100" width="160" height="50" rx="6" fill="#FF3621" opacity="0.9"/>
# MAGIC   <text x="90" y="130" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">8. Monitor</text>
# MAGIC
# MAGIC   <!-- Label -->
# MAGIC   <text x="380" y="190" text-anchor="middle" font-size="13" fill="#1B3139" font-style="italic">Each step requires specialized expertise and significant time investment</text>
# MAGIC
# MAGIC </svg>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,A2. Solution: Genie Code
# MAGIC %md-sandbox
# MAGIC ### A2. Solution: Genie Code
# MAGIC
# MAGIC Rapid, simplified machine learning **for technical practitioners using natural language**.
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 20px auto;">
# MAGIC <table style="border-collapse: collapse; width: 100%; font-family: sans-serif;">
# MAGIC <tr style="border-bottom: 2px solid #1B3139;">
# MAGIC   <td style="padding: 16px 20px; width: 33%; vertical-align: top;">
# MAGIC     <span style="color: #FF3621; font-weight: bold; font-size: 16px;">Quick-start ML initiatives</span><br/><br/>
# MAGIC     Accelerate your time to production. Save weeks on ML projects.
# MAGIC   </td>
# MAGIC   <td style="padding: 16px 20px; width: 33%; vertical-align: top;">
# MAGIC     <span style="color: #FF3621; font-weight: bold; font-size: 16px;">Auto-generated code</span><br/><br/>
# MAGIC     Ensure best practices. Allows for interaction and incorporation of domain expertise.
# MAGIC   </td>
# MAGIC   <td style="padding: 16px 20px; width: 33%; vertical-align: top;">
# MAGIC     <span style="color: #FF3621; font-weight: bold; font-size: 16px;">Wide range of problems</span><br/><br/>
# MAGIC     Solve classification, regression, forecasting problems and more using a variety of ML libraries.
# MAGIC   </td>
# MAGIC </tr>
# MAGIC </table>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC How does Genie Code span the full ML lifecycle?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">
# MAGIC Genie Code spans the full ML lifecycle — data exploration, model development, hyperparameter tuning, deployment, and monitoring. The throughline is natural language: you describe what you want, and Genie Code generates and runs the code. Throughout, the user retains full control — Genie Code shows you what it's doing at every step, and you can intervene at any point.
# MAGIC </p>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. What Is Genie Code

# COMMAND ----------

# DBTITLE 1,B1. Genie Code: An Autonomous AI Partner
# MAGIC %md-sandbox
# MAGIC ### B1. Genie Code: An Autonomous AI Partner
# MAGIC
# MAGIC Genie Code is an autonomous AI partner built for modern data teams.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 20px auto;">
# MAGIC <table style="border-collapse: collapse; width: 100%; font-family: sans-serif;">
# MAGIC <tr>
# MAGIC   <td style="padding: 16px 24px; vertical-align: top; border-left: 4px solid #FF3621;">
# MAGIC     <strong style="font-size: 15px; color: #1B3139;">Designed for Data Work</strong><br/>
# MAGIC     Fluent in data engineering, data science, machine learning, and dashboards.
# MAGIC   </td>
# MAGIC </tr>
# MAGIC <tr>
# MAGIC   <td style="padding: 16px 24px; vertical-align: top; border-left: 4px solid #FF3621;">
# MAGIC     <strong style="font-size: 15px; color: #1B3139;">Knows Your Data</strong><br/>
# MAGIC     Grounded in Unity Catalog metadata, semantics, and governance.
# MAGIC   </td>
# MAGIC </tr>
# MAGIC <tr>
# MAGIC   <td style="padding: 16px 24px; vertical-align: top; border-left: 4px solid #FF3621;">
# MAGIC     <strong style="font-size: 15px; color: #1B3139;">Keeps Workflows Healthy</strong><br/>
# MAGIC     Plans and runs complex workflows end to end, proactively monitoring and resolving issues.
# MAGIC   </td>
# MAGIC </tr>
# MAGIC </table>
# MAGIC </div>
# MAGIC
# MAGIC Genie Code operates across three artifact types: **ML models** (training, evaluation, registration), **pipelines** (orchestrated workflows), and **dashboards** (visualization and monitoring). That breadth is what makes it different from a code-completion assistant — it understands the full Databricks workspace.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B2. Five Key ML Needs Solved with Genie Code
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 20px auto;">
# MAGIC <table style="border-collapse: collapse; width: 100%; font-family: sans-serif; font-size: 14px;">
# MAGIC <tr style="background-color: #1B3139; color: white;">
# MAGIC   <th style="padding: 12px 16px; text-align: left; width: 25%;">Capability</th>
# MAGIC   <th style="padding: 12px 16px; text-align: left; width: 35%;">What It Does</th>
# MAGIC   <th style="padding: 12px 16px; text-align: left; width: 40%;">Example Prompt</th>
# MAGIC </tr>
# MAGIC <tr style="border-bottom: 1px solid #ddd;">
# MAGIC   <td style="padding: 12px 16px; font-weight: bold; color: #1B3139;">Data Discovery</td>
# MAGIC   <td style="padding: 12px 16px;">Powerful search using lineage, description, code samples as signals</td>
# MAGIC   <td style="padding: 12px 16px; font-style: italic; color: #555;"><em>"Help me find a table for investigating flight delays."</em></td>
# MAGIC </tr>
# MAGIC <tr style="border-bottom: 1px solid #ddd; background-color: #F9F7F4;">
# MAGIC   <td style="padding: 12px 16px; font-weight: bold; color: #1B3139;">Exploratory Data Analysis</td>
# MAGIC   <td style="padding: 12px 16px;">Ask for insights about a table</td>
# MAGIC   <td style="padding: 12px 16px; font-style: italic; color: #555;"><em>"Do EDA on @flights and identify 5 interesting insights."</em></td>
# MAGIC </tr>
# MAGIC <tr style="border-bottom: 1px solid #ddd;">
# MAGIC   <td style="padding: 12px 16px; font-weight: bold; color: #1B3139;">Model Training</td>
# MAGIC   <td style="padding: 12px 16px;">Ideate what is needed for robust ML</td>
# MAGIC   <td style="padding: 12px 16px; font-style: italic; color: #555;"><em>"Build a predictive model. Do you think we are ready or need more EDA?"</em></td>
# MAGIC </tr>
# MAGIC <tr style="border-bottom: 1px solid #ddd; background-color: #F9F7F4;">
# MAGIC   <td style="padding: 12px 16px; font-weight: bold; color: #1B3139;">Model Deployment</td>
# MAGIC   <td style="padding: 12px 16px;">Iterates on errors and integrates with other services</td>
# MAGIC   <td style="padding: 12px 16px; font-style: italic; color: #555;"><em>"Register and deploy the model on an endpoint."</em></td>
# MAGIC </tr>
# MAGIC <tr>
# MAGIC   <td style="padding: 12px 16px; font-weight: bold; color: #1B3139;">Model Monitoring</td>
# MAGIC   <td style="padding: 12px 16px;">Creates datasets and charts automatically</td>
# MAGIC   <td style="padding: 12px 16px; font-style: italic; color: #555;"><em>"Create a dashboard for evaluating model performance from @table(s)."</em></td>
# MAGIC </tr>
# MAGIC </table>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Platform Integration and Customization

# COMMAND ----------

# DBTITLE 1,C1. Genie Code Is AI That Knows the Platform
# MAGIC %md-sandbox
# MAGIC ### C1. Genie Code Is AI That Knows the Platform
# MAGIC
# MAGIC Genie Code understands and integrates with other Databricks products.
# MAGIC
# MAGIC **Genie Code integrates with:**
# MAGIC
# MAGIC - **Feature Store**: Expand the input training dataset using existing feature tables.
# MAGIC - **MLflow Model Tracking**: All trial run metrics and parameters are tracked.
# MAGIC - **Model Registry**: Register generated models to Unity Catalog.
# MAGIC - **Model Serving**: Stand up low-latency model-serving endpoints with the right specs — Genie Code handles endpoint configuration for real-time inference.
# MAGIC - **Lakeflow Pipelines**: Create and maintain Spark Declarative Pipelines.
# MAGIC - **Multi-Language Notebooks**: Works across Python, SQL, and Scala — no context-switching as you move from data prep to modeling to evaluation.
# MAGIC - **And more...** including Data Versioning, Runtime Environments, Batch Scoring, Online Serving, and Monitoring — all governed through Unity Catalog.

# COMMAND ----------

# DBTITLE 1,C2. Genie Code's Customized Context
# MAGIC %md-sandbox
# MAGIC ### C2. Genie Code's Customized Context
# MAGIC
# MAGIC Customization provides greater flexibility and context for an improved result.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 20px auto;">
# MAGIC <svg width="100%" viewBox="0 0 680 280" style="font-family: sans-serif;">
# MAGIC
# MAGIC   <!-- Foundation bar -->
# MAGIC   <rect x="40" y="240" width="600" height="35" rx="4" fill="#1B3139"/>
# MAGIC   <text x="340" y="263" text-anchor="middle" font-size="13" font-weight="bold" fill="#fff">General Knowledge</text>
# MAGIC
# MAGIC   <!-- UC bar -->
# MAGIC   <rect x="40" y="200" width="600" height="35" rx="4" fill="#2D4F5C"/>
# MAGIC   <text x="340" y="223" text-anchor="middle" font-size="13" font-weight="bold" fill="#fff">Unity Catalog Data and Metadata</text>
# MAGIC
# MAGIC   <!-- Three pillars -->
# MAGIC   <!-- MCP -->
# MAGIC   <rect x="70" y="80" width="160" height="110" rx="4" fill="#FF3621" opacity="0.15" stroke="#FF3621" stroke-width="2"/>
# MAGIC   <text x="150" y="110" text-anchor="middle" font-size="14" font-weight="bold" fill="#1B3139">MCP</text>
# MAGIC   <text x="150" y="140" text-anchor="middle" font-size="12" fill="#555">Connections</text>
# MAGIC   <text x="150" y="160" text-anchor="middle" font-size="11" fill="#555">External tools &amp;</text>
# MAGIC   <text x="150" y="175" text-anchor="middle" font-size="11" fill="#555">data sources</text>
# MAGIC
# MAGIC   <!-- Instructions -->
# MAGIC   <rect x="260" y="80" width="160" height="110" rx="4" fill="#FF3621" opacity="0.15" stroke="#FF3621" stroke-width="2"/>
# MAGIC   <text x="340" y="110" text-anchor="middle" font-size="14" font-weight="bold" fill="#1B3139">Instructions</text>
# MAGIC   <text x="340" y="140" text-anchor="middle" font-size="12" fill="#555">Guidance</text>
# MAGIC   <text x="340" y="160" text-anchor="middle" font-size="11" fill="#555">Always-on context:</text>
# MAGIC   <text x="340" y="175" text-anchor="middle" font-size="11" fill="#555">standards, style</text>
# MAGIC
# MAGIC   <!-- Skills -->
# MAGIC   <rect x="450" y="80" width="160" height="110" rx="4" fill="#FF3621" opacity="0.15" stroke="#FF3621" stroke-width="2"/>
# MAGIC   <text x="530" y="110" text-anchor="middle" font-size="14" font-weight="bold" fill="#1B3139">Skills</text>
# MAGIC   <text x="530" y="140" text-anchor="middle" font-size="12" fill="#555">Task-specific</text>
# MAGIC   <text x="530" y="160" text-anchor="middle" font-size="11" fill="#555">Domain knowledge</text>
# MAGIC   <text x="530" y="175" text-anchor="middle" font-size="11" fill="#555">&amp; workflows</text>
# MAGIC
# MAGIC   <!-- Roof / Genie Code label -->
# MAGIC   <polygon points="40,70 340,20 640,70" fill="#1B3139"/>
# MAGIC   <text x="340" y="58" text-anchor="middle" font-size="14" font-weight="bold" fill="#fff">Genie Code</text>
# MAGIC
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC How is Genie Code customizable?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">
# MAGIC Genie Code is highly customizable — and that's a feature. Teams can tailor Genie Code to their stack and conventions using three layers:
# MAGIC </p>
# MAGIC
# MAGIC <ol style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li><strong>MCP connections</strong>: Link Genie Code to external tools or data sources it can call at runtime.</li>
# MAGIC <li><strong>Instructions</strong>: Persistent markdown files that apply across every conversation, encoding your team's standards, libraries, and style.</li>
# MAGIC <li><strong>Skills</strong>: Bundles of domain-specific procedures Genie Code can invoke on demand.</li>
# MAGIC </ol>
# MAGIC
# MAGIC <p>Together, these three layers let teams shape Genie Code to their stack and conventions.</p>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,C3. Extend Genie Code with MCP
# MAGIC %md-sandbox
# MAGIC ### C3. Extend Genie Code with MCP
# MAGIC
# MAGIC Improve response quality through context enrichment and tool integration.
# MAGIC
# MAGIC **MCP (Model Context Protocol)** connects Genie Code to **additional tools and data sources** (both native Databricks services and external systems) — designed for cases where **important context already exists** but is difficult to access from an AI agent.
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC What types of context can MCP access?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li><strong>Documentation systems:</strong> Centralized docs</li>
# MAGIC <li><strong>Tools and services:</strong> APIs and automation tools</li>
# MAGIC <li><strong>Data sources:</strong> Query structured data</li>
# MAGIC <li><strong>Custom systems:</strong> Proprietary internal tools</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC What MCP server types does Genie Code support?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li><strong>Unity Catalog Functions</strong> — Execute predefined SQL queries by selecting a schema containing custom functions</li>
# MAGIC <li><strong>AI Search</strong> — Query an AI Search index (backed by Vector Search) to retrieve relevant documents</li>
# MAGIC <li><strong>Genie Spaces</strong> — Invoke Genie as a tool, permitting natural language data analysis</li>
# MAGIC <li><strong>UC Connections (external MCP servers)</strong> — Wire Genie Code to external MCP servers governed through Unity Catalog, keeping access controls and lineage in one place</li>
# MAGIC <li><strong>Databricks Apps (custom MCP servers)</strong> — Build and deploy custom MCP servers directly in your workspace, exposing proprietary tools and workflows to Genie Code</li>
# MAGIC </ul>
# MAGIC
# MAGIC <p>Genie Code becomes capable of calling whatever tools your team has standardized on.</p>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,C4. Guide Genie Code with Instructions
# MAGIC %md-sandbox
# MAGIC ### C4. Guide Genie Code with Instructions
# MAGIC
# MAGIC Define clear guidance and structure to improve response quality.
# MAGIC
# MAGIC **Instructions:**
# MAGIC
# MAGIC - Markdown files that give Genie Code **always-on context**: your team's coding standards, preferred libraries, naming conventions, and the language you want responses in.
# MAGIC - **Configurable** at workspace or user level — scope them broadly to apply everywhere, or narrowly for personal preferences.
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Best practices for Instructions
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li>Write clear, specific instructions</li>
# MAGIC <li>Keep instructions under 20,000 characters</li>
# MAGIC <li>Use markdown headers to organize instructions into sections — Genie Code parses them cleanly, and well-structured instructions produce noticeably better results</li>
# MAGIC <li>Scope: Keep instructions broadly relevant</li>
# MAGIC <li>Provide context and references</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,C5. Equip Genie Code with Skills
# MAGIC %md-sandbox
# MAGIC ### C5. Equip Genie Code with Skills
# MAGIC
# MAGIC Operationalize domain knowledge through reusable workflows and automation.
# MAGIC
# MAGIC **Skills:**
# MAGIC
# MAGIC - On-demand **bundles of domain knowledge** and workflows — markdown plus optional scripts — that Genie Code pulls in when invoked in Agent mode.
# MAGIC - Think of skills as **recipes for common tasks**: a *"deploy this model"* skill, a *"build a churn model"* skill, a *"set up monitoring"* skill.
# MAGIC - Build them once and reuse them across the team.
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Best practices for Skills
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li>Focus on a single task or workflow</li>
# MAGIC <li>Use clear, descriptive names</li>
# MAGIC <li>Provide step-by-step examples</li>
# MAGIC <li>Include only necessary context</li>
# MAGIC <li>Iterate and refine over time</li>
# MAGIC <li>Separate guidance from automation</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. End-to-End Model Development

# COMMAND ----------

# DBTITLE 1,D1. Genie Code: End-to-End Model Development
# MAGIC %md-sandbox
# MAGIC ### D1. Genie Code: End-to-End Model Development
# MAGIC
# MAGIC From data exploration to deployed endpoint — all in one conversation. Supported with context and guidance.
# MAGIC
# MAGIC The following steps illustrate a complete Genie Code session that progresses through four phases:
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Phase 1 — Exploratory Data Analysis
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li>Step 1: Open a notebook, start the Genie Code assistant, and request exploration of the flights dataset.</li>
# MAGIC <li>Step 2: Use Genie Code to perform EDA by profiling column types, generating summary statistics, distribution plots, and a correlogram.</li>
# MAGIC <li>Step 3: Ask Genie Code if you are ready to build a predictive model or if more EDA is needed.</li>
# MAGIC <li>Step 4: Review Genie Code's recommendations on data gaps (such as null handling, class imbalance, feature distributions) and suggested next steps.</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Phase 2 — Model Training and Tuning
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li>Step 1: Instruct Genie Code to build a classification model predicting flight delays using selected features.</li>
# MAGIC <li>Step 2: Run pre-modeling checks with Genie Code, including null analysis, class balance, feature distributions, and a correlogram.</li>
# MAGIC <li>Step 3: Train a LightGBM model with Optuna hyperparameter tuning, evaluate on a test set (ROC curve, metrics), and log all results to MLflow.</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Phase 3 — Model Registration and Deployment
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li>Step 1: Request Genie Code to add checks and build a classification model predicting DEP_DEL15 with airline, origin, destination, and time features.</li>
# MAGIC <li>Step 2: Let Genie Code iterate by adding dependencies, updating install cells, and running the workflow end-to-end.</li>
# MAGIC <li>Step 3: Register the trained model to Unity Catalog and deploy a serving endpoint using Genie Code.</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Phase 4 — Validation and Summary
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li>Step 1: Confirm deployment completion—Genie Code reports the model is registered in Unity Catalog, the serving endpoint is live with scale-to-zero, and predictions are returned correctly for test samples.</li>
# MAGIC <li>Step 2: Review important notes, such as the model's expectation for target-encoded numeric values for categorical features due to encoding applied outside the model during training.</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,E. Conclusion
# MAGIC %md
# MAGIC ## E. Conclusion
# MAGIC
# MAGIC In this lecture, you learned how Genie Code transforms the ML development workflow by providing an AI coding and data assistant that:
# MAGIC
# MAGIC - **Addresses the ML challenge** — Generates and runs the code for the complex, multi-step process from data preparation through deployment using natural language — while keeping you in full control at every step.
# MAGIC - **Integrates deeply with the platform** — Leverages Feature Store, MLflow, Model Registry, Model Serving, multi-language notebooks, and more to produce production-ready results across ML models, pipelines, and dashboards.
# MAGIC - **Supports customization** — MCP connections wire it to external tools, persistent instructions encode your team’s standards and conventions, and skills package domain workflows as reusable recipes the whole team can invoke.
# MAGIC - **Enables end-to-end development** — From exploratory analysis to deployed endpoint, all in one conversation with human oversight.

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
