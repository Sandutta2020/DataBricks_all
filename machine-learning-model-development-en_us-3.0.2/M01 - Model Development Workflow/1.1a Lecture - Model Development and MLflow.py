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

# DBTITLE 1,Cell 2
# MAGIC %md-sandbox
# MAGIC # Lecture — Model Development and MLflow
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This lecture introduces the foundations of machine learning model development and shows how MLflow streamlines the ML lifecycle on Databricks.
# MAGIC
# MAGIC This lecture covers 4 sections that build on each other:
# MAGIC
# MAGIC - **A. Types of Machine Learning**. The four paradigms — supervised, unsupervised, hybrid, and reinforcement learning — and the supervised subtypes you will use in this course.
# MAGIC - **B. The ML Full Lifecycle**. The end-to-end workflow from business problem to production, and the core challenges that arise along the way.
# MAGIC - **C. MLflow for Model Development**. How MLflow addresses those challenges through its four components — Tracking, Evaluation, Models, and Registry.
# MAGIC - **D. MLflow Concepts and Examining Runs**. The experiment/run hierarchy, metadata vs. artifacts, and how to retrieve past runs via the UI and API.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. Categorize machine learning paradigms — supervised, unsupervised, hybrid, and reinforcement learning — and identify appropriate use cases for each.
# MAGIC 2. Outline the traditional ML model training workflow and explain how Databricks and MLflow streamline each stage.
# MAGIC 3. Apply MLflow tracking and Databricks Autologging to log experiments, parameters, metrics, and custom artifacts.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Types of Machine Learning

# COMMAND ----------

# DBTITLE 1,Cell 4
# MAGIC %md-sandbox
# MAGIC ### A1. Supervised Learning
# MAGIC
# MAGIC Machine learning divides into paradigms based on the kind of data available and the goal of the model.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; gap: 20px; align-items: flex-start;">
# MAGIC
# MAGIC <!-- SVG 1: Info Box -->
# MAGIC <svg width="420" viewBox="0 0 420 280" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Supervised Learning</title>
# MAGIC   <rect x="10" y="10" width="400" height="260" rx="12" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="210" y="45" text-anchor="middle" font-size="16" font-weight="bold" fill="#1B3139">Supervised Learning</text>
# MAGIC   <line x1="50" y1="58" x2="370" y2="58" stroke="#1976D2" stroke-width="1"/>
# MAGIC   <text x="30" y="85" font-size="14" fill="#1B3139">• Data has input records with associated labels</text>
# MAGIC   <text x="30" y="108" font-size="14" fill="#1B3139">• Goal: predict output labels for unlabeled inputs</text>
# MAGIC   <text x="30" y="131" font-size="14" fill="#1B3139">• Model the conditional probability:</text>
# MAGIC   <text x="50" y="158" font-size="15" font-style="italic" fill="#1565C0">P(Y | X₁, X₂, …, x<tspan dy="4" font-size="10">n</tspan>)</text>
# MAGIC   <text x="30" y="195" font-size="14" font-weight="bold" fill="#1B3139">Examples:</text>
# MAGIC   <text x="30" y="218" font-size="14" fill="#1B3139">• Predict house prices (regression)</text>
# MAGIC   <text x="30" y="241" font-size="14" fill="#1B3139">• Classify customer churn (classification)</text>
# MAGIC   <text x="30" y="264" font-size="14" fill="#1B3139">• Forecast demand (forecasting)</text>
# MAGIC </svg>
# MAGIC
# MAGIC <!-- SVG 2: Regression Graph -->
# MAGIC <svg width="420" viewBox="0 0 400 260" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Regression Example</title>
# MAGIC   <rect x="10" y="10" width="380" height="240" rx="12" fill="#FFFFFF" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="200" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Regression Example</text>
# MAGIC
# MAGIC   <!-- Grid lines -->
# MAGIC   <line x1="60" y1="60" x2="60" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="120" y1="60" x2="120" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="180" y1="60" x2="180" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="240" y1="60" x2="240" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="300" y1="60" x2="300" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="90" x2="370" y2="90" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="130" x2="370" y2="130" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="170" x2="370" y2="170" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="210" x2="370" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC
# MAGIC   <!-- Axes -->
# MAGIC   <line x1="50" y1="210" x2="370" y2="210" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <line x1="50" y1="50" x2="50" y2="210" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <text x="210" y="232" text-anchor="middle" font-size="13" fill="#1B3139">X (feature)</text>
# MAGIC   <text x="30" y="130" text-anchor="middle" font-size="13" fill="#1B3139" transform="rotate(-90 30 130)">Y (label)</text>
# MAGIC
# MAGIC   <!-- Data points -->
# MAGIC   <circle cx="70" cy="80" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="110" cy="105" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="150" cy="120" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="200" cy="148" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="250" cy="165" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="300" cy="190" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="340" cy="205" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC
# MAGIC   <!-- Regression line -->
# MAGIC   <line x1="60" y1="75" x2="350" y2="205" stroke="#D32F2F" stroke-width="2.5" stroke-dasharray="6,3"/>
# MAGIC
# MAGIC   <!-- Legend -->
# MAGIC   <!-- Legend: Vertically aligned to the right -->
# MAGIC   <g transform="translate(0,26)">
# MAGIC     <circle cx="300" cy="60" r="4" fill="#1976D2"/>
# MAGIC     <text x="310" y="64" font-size="11" fill="#1B3139" alignment-baseline="middle">Labeled data</text>
# MAGIC     <line x1="300" y1="80" x2="320" y2="80" stroke="#D32F2F" stroke-width="2" stroke-dasharray="4,2"/>
# MAGIC     <text x="310" y="88" font-size="11" fill="#1B3139" alignment-baseline="middle">Regression line</text>
# MAGIC   </g>
# MAGIC </svg>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC In supervised learning, the model learns from labeled examples (X → Y) and fits a function that generalizes to predict labels on new, unseen data.
# MAGIC
# MAGIC Supervised learning breaks into three task types depending on what the model predicts.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 220" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Supervised Learning Types</title>
# MAGIC
# MAGIC   <!-- Regression -->
# MAGIC   <rect x="20" y="20" width="260" height="180" rx="10" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="150" y="50" text-anchor="middle" font-size="15" font-weight="bold" fill="#1565C0">Regression</text>
# MAGIC   <line x1="50" y1="62" x2="250" y2="62" stroke="#1976D2" stroke-width="1"/>
# MAGIC   <text x="40" y="88" font-size="13" fill="#1B3139">Predicting a continuous output</text>
# MAGIC   <text x="40" y="120" font-size="13" font-weight="bold" fill="#1B3139">Examples:</text>
# MAGIC   <text x="40" y="143" font-size="13" fill="#1B3139">• Predict sales revenue</text>
# MAGIC   <text x="40" y="163" font-size="13" fill="#1B3139">• Predict number of viewers</text>
# MAGIC   <text x="40" y="183" font-size="13" fill="#1B3139">• Predict house prices</text>
# MAGIC
# MAGIC   <!-- Classification -->
# MAGIC   <rect x="300" y="20" width="260" height="180" rx="10" fill="#FFF3E0" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="430" y="50" text-anchor="middle" font-size="15" font-weight="bold" fill="#E65100">Classification</text>
# MAGIC   <line x1="330" y1="62" x2="530" y2="62" stroke="#F57C00" stroke-width="1"/>
# MAGIC   <text x="315" y="80" font-size="13" fill="#1B3139">Predicting a categorical/discrete output</text>
# MAGIC   <text x="320" y="120" font-size="13" font-weight="bold" fill="#1B3139">Examples:</text>
# MAGIC   <text x="320" y="143" font-size="13" fill="#1B3139">• Yes/No decisions</text>
# MAGIC   <text x="320" y="163" font-size="13" fill="#1B3139">• Image classification</text>
# MAGIC   <text x="320" y="183" font-size="13" fill="#1B3139">• Disease prediction</text>
# MAGIC
# MAGIC   <!-- Forecasting -->
# MAGIC   <rect x="580" y="20" width="260" height="180" rx="10" fill="#E8F5E9" stroke="#388E3C" stroke-width="2"/>
# MAGIC   <text x="710" y="50" text-anchor="middle" font-size="15" font-weight="bold" fill="#2E7D32">Forecasting</text>
# MAGIC   <line x1="610" y1="62" x2="810" y2="62" stroke="#388E3C" stroke-width="1"/>
# MAGIC   <text x="600" y="84" font-size="14" fill="#1B3139">Predicting future values from history</text>
# MAGIC   <text x="600" y="120" font-size="13" font-weight="bold" fill="#1B3139">Examples:</text>
# MAGIC   <text x="600" y="143" font-size="13" fill="#1B3139">• Demand forecasting</text>
# MAGIC   <text x="600" y="163" font-size="13" fill="#1B3139">• Stock price trends</text>
# MAGIC   <text x="600" y="183" font-size="13" fill="#1B3139">• Energy consumption</text>
# MAGIC </svg>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,Cell 5
# MAGIC %md-sandbox
# MAGIC            
# MAGIC ### A2. Unsupervised Learning
# MAGIC
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; gap: 20px; align-items: flex-start;">
# MAGIC
# MAGIC <!-- SVG 1: Info Box -->
# MAGIC <svg width="420" viewBox="0 0 420 280" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Unsupervised Learning</title>
# MAGIC   <rect x="10" y="10" width="400" height="260" rx="12" fill="#FFF3E0" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="210" y="45" text-anchor="middle" font-size="16" font-weight="bold" fill="#1B3139">Unsupervised Learning</text>
# MAGIC   <line x1="50" y1="58" x2="370" y2="58" stroke="#F57C00" stroke-width="1"/>
# MAGIC   <text x="30" y="85" font-size="14" fill="#1B3139">• Unlabeled data (no known output)</text>
# MAGIC   <text x="30" y="108" font-size="14" fill="#1B3139">• Clustering: group records with similar features</text>
# MAGIC   <text x="30" y="131" font-size="14" fill="#1B3139">• Dimensionality reduction: reduce feature space</text>
# MAGIC   <text x="30" y="158" font-size="14" fill="#1B3139">• Model the joint probability:</text>
# MAGIC   <text x="50" y="185" font-size="15" font-style="italic" fill="#E65100">P(X₁, X₂, …, x<tspan dy="4" font-size="10">n</tspan>)</text>
# MAGIC   <text x="30" y="222" font-size="14" font-weight="bold" fill="#1B3139">Examples:</text>
# MAGIC   <text x="30" y="245" font-size="14" fill="#1B3139">• Customer segmentation</text>
# MAGIC   <text x="30" y="268" font-size="14" fill="#1B3139">• Anomaly detection</text>
# MAGIC </svg>
# MAGIC
# MAGIC <!-- SVG 2: Clustering Graph -->
# MAGIC <svg width="420" viewBox="0 0 400 260" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Clustering Example</title>
# MAGIC   <rect x="10" y="10" width="380" height="240" rx="12" fill="#FFFFFF" stroke="#F57C00" stroke-width="2"/>
# MAGIC   <text x="200" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#E65100">Clustering Example</text>
# MAGIC
# MAGIC   <!-- Grid lines -->
# MAGIC   <line x1="60" y1="60" x2="60" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="120" y1="60" x2="120" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="180" y1="60" x2="180" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="240" y1="60" x2="240" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="300" y1="60" x2="300" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="90" x2="370" y2="90" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="130" x2="370" y2="130" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="170" x2="370" y2="170" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="210" x2="370" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC
# MAGIC   <!-- Axes -->
# MAGIC   <line x1="50" y1="210" x2="370" y2="210" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <line x1="50" y1="50" x2="50" y2="210" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <text x="210" y="232" text-anchor="middle" font-size="13" fill="#1B3139">X₁</text>
# MAGIC   <text x="30" y="130" text-anchor="middle" font-size="13" fill="#1B3139" transform="rotate(-90 30 130)">X₂</text>
# MAGIC
# MAGIC   <!-- Cluster A (blue, top-left) -->
# MAGIC   <circle cx="90" cy="80" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="105" cy="95" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="80" cy="100" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="110" cy="85" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="95" cy="105" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC
# MAGIC   <!-- Cluster B (orange, right) -->
# MAGIC   <circle cx="260" cy="90" r="5" fill="#F57C00" opacity="0.8"/>
# MAGIC   <circle cx="280" cy="100" r="5" fill="#F57C00" opacity="0.8"/>
# MAGIC   <circle cx="290" cy="85" r="5" fill="#F57C00" opacity="0.8"/>
# MAGIC   <circle cx="270" cy="110" r="5" fill="#F57C00" opacity="0.8"/>
# MAGIC   <circle cx="300" cy="95" r="5" fill="#F57C00" opacity="0.8"/>
# MAGIC
# MAGIC   <!-- Cluster C (green, bottom-center) -->
# MAGIC   <circle cx="170" cy="170" r="5" fill="#388E3C" opacity="0.8"/>
# MAGIC   <circle cx="190" cy="180" r="5" fill="#388E3C" opacity="0.8"/>
# MAGIC   <circle cx="180" cy="190" r="5" fill="#388E3C" opacity="0.8"/>
# MAGIC   <circle cx="200" cy="175" r="5" fill="#388E3C" opacity="0.8"/>
# MAGIC   <circle cx="165" cy="185" r="5" fill="#388E3C" opacity="0.8"/>
# MAGIC
# MAGIC   <!-- Legend -->
# MAGIC   <g transform="translate(0,26)">
# MAGIC     <circle cx="320" cy="60" r="4" fill="#1976D2"/>
# MAGIC     <text x="330" y="64" font-size="11" fill="#1B3139">Cluster A</text>
# MAGIC     <circle cx="320" cy="80" r="4" fill="#F57C00"/>
# MAGIC     <text x="330" y="84" font-size="11" fill="#1B3139">Cluster B</text>
# MAGIC     <circle cx="320" cy="100" r="4" fill="#388E3C"/>
# MAGIC     <text x="330" y="104" font-size="11" fill="#1B3139">Cluster C</text>
# MAGIC   </g>
# MAGIC </svg>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC In unsupervised learning, the model discovers hidden structure in unlabeled data — grouping similar records into clusters without any predefined target variable.

# COMMAND ----------

# DBTITLE 1,Cell - A3 Hybrid and Reinforcement
# MAGIC %md-sandbox
# MAGIC ### A3. Hybrid Learning
# MAGIC
# MAGIC Beyond the two primary paradigms, two additional approaches handle scenarios where labels are scarce or the environment is interactive.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; gap: 20px; align-items: flex-start;">
# MAGIC
# MAGIC <!-- SVG 1: Info Box -->
# MAGIC <svg width="420" viewBox="0 0 420 260" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Hybrid Learning</title>
# MAGIC   <rect x="10" y="10" width="400" height="240" rx="12" fill="#F3E5F5" stroke="#7B1FA2" stroke-width="2"/>
# MAGIC   <text x="210" y="45" text-anchor="middle" font-size="16" font-weight="bold" fill="#1B3139">Hybrid Learning</text>
# MAGIC   <line x1="50" y1="58" x2="370" y2="58" stroke="#7B1FA2" stroke-width="1"/>
# MAGIC   <text x="30" y="85" font-size="15" fill="#1B3139">• Combines supervised + unsupervised</text>
# MAGIC   <text x="30" y="108" font-size="15" fill="#1B3139">• Mostly unlabeled data</text>
# MAGIC   <text x="30" y="138" font-size="15" font-weight="bold" fill="#1B3139">Semi-supervised:</text>
# MAGIC   <text x="50" y="161" font-size="15" fill="#1B3139">• Small labeled set infers labels for larger set</text>
# MAGIC   <text x="30" y="191" font-size="15" font-weight="bold" fill="#1B3139">Self-supervised:</text>
# MAGIC   <text x="50" y="214" font-size="15" fill="#1B3139">• Learn patterns from one dataset, apply to another</text>
# MAGIC </svg>
# MAGIC
# MAGIC <!-- SVG 2: Semi-Supervised Graph -->
# MAGIC <svg width="420" viewBox="0 0 400 260" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Semi-Supervised Learning Example</title>
# MAGIC   <rect x="10" y="10" width="380" height="240" rx="12" fill="#FFFFFF" stroke="#7B1FA2" stroke-width="2"/>
# MAGIC   <text x="200" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#4A148C">Semi-Supervised Example</text>
# MAGIC
# MAGIC   <!-- Grid lines -->
# MAGIC   <line x1="60" y1="60" x2="60" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="120" y1="60" x2="120" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="180" y1="60" x2="180" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="240" y1="60" x2="240" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="300" y1="60" x2="300" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="90" x2="370" y2="90" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="130" x2="370" y2="130" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="170" x2="370" y2="170" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="210" x2="370" y2="210" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC
# MAGIC   <!-- Axes -->
# MAGIC   <line x1="50" y1="210" x2="370" y2="210" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <line x1="50" y1="50" x2="50" y2="210" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <text x="210" y="232" text-anchor="middle" font-size="13" fill="#1B3139">X₁</text>
# MAGIC   <text x="30" y="130" text-anchor="middle" font-size="13" fill="#1B3139" transform="rotate(-90 30 130)">X₂</text>
# MAGIC
# MAGIC   <!-- Unlabeled points (gray, open circles) - Class A region -->
# MAGIC   <circle cx="80" cy="190" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC   <circle cx="95" cy="145" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC   <circle cx="105" cy="120" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC   <circle cx="120" cy="140" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC   <circle cx="90" cy="120" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC   <circle cx="110" cy="160" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC   <circle cx="75" cy="148" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC   <circle cx="130" cy="175" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC
# MAGIC   <!-- Unlabeled points (gray, open circles) - Class B region -->
# MAGIC   <circle cx="250" cy="85" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC   <circle cx="270" cy="75" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC   <circle cx="280" cy="115" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/> <!-- moved below boundary -->
# MAGIC   <circle cx="300" cy="120" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/> <!-- moved below boundary -->
# MAGIC   <circle cx="260" cy="130" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/> <!-- moved below boundary -->
# MAGIC   <circle cx="290" cy="65" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC   <circle cx="310" cy="90" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC   <circle cx="240" cy="95" r="5" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC
# MAGIC   <!-- Labeled points - Class A (blue, filled) -->
# MAGIC   <circle cx="100" cy="135" r="6" fill="#1976D2" stroke="#0D47A1" stroke-width="1.5"/>
# MAGIC   <circle cx="85" cy="150" r="6" fill="#1976D2" stroke="#0D47A1" stroke-width="1.5"/>
# MAGIC
# MAGIC   <!-- Labeled points - Class B (orange, filled) -->
# MAGIC   <circle cx="275" cy="82" r="6" fill="#F57C00" stroke="#E65100" stroke-width="1.5"/>
# MAGIC   <circle cx="295" cy="72" r="6" fill="#F57C00" stroke="#E65100" stroke-width="1.5"/>
# MAGIC
# MAGIC   <!-- Decision boundary (dashed red) -->
# MAGIC   <line x1="55" y1="195" x2="360" y2="55" stroke="#D32F2F" stroke-width="2" stroke-dasharray="6,3"/>
# MAGIC
# MAGIC   <!-- Legend -->
# MAGIC   <g transform="translate(0,26)">
# MAGIC     <circle cx="280" cy="136" r="4" fill="none" stroke="#9E9E9E" stroke-width="1.5"/>
# MAGIC     <text x="290" y="140" font-size="12" fill="#1B3139">Unlabeled</text>
# MAGIC     <circle cx="280" cy="152" r="4" fill="#1976D2"/>
# MAGIC     <text x="290" y="156" font-size="12" fill="#1B3139">Class A</text>
# MAGIC     <circle cx="280" cy="162" r="4" fill="#F57C00"/>
# MAGIC     <text x="290" y="166" font-size="12" fill="#1B3139">Class B</text>
# MAGIC   </g>
# MAGIC </svg>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC In semi-supervised learning, a small number of labeled examples guide the model to classify a much larger set of unlabeled data — combining the strengths of both supervised and unsupervised approaches.

# COMMAND ----------

# DBTITLE 1,Cell 7
# MAGIC %md-sandbox
# MAGIC ### A4. Reinforcement Learning
# MAGIC
# MAGIC Reinforcement learning addresses scenarios where an agent learns by interacting with an environment, receiving feedback through rewards to optimize its actions.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; gap: 20px; align-items: flex-start;">
# MAGIC   
# MAGIC <!-- Info Box -->
# MAGIC <svg width="420" viewBox="0 0 400 260" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Reinforcement Learning</title>
# MAGIC   <rect x="10" y="10" width="380" height="220" rx="12" fill="#E8F5E9" stroke="#388E3C" stroke-width="2"/>
# MAGIC   <text x="200" y="45" text-anchor="middle" font-size="16" font-weight="bold" fill="#2E7D32">Reinforcement Learning</text>
# MAGIC   <line x1="50" y1="58" x2="350" y2="58" stroke="#388E3C" stroke-width="1"/>
# MAGIC   <text x="30" y="85" font-size="15" fill="#1B3139">• Agent interacts with environment</text>
# MAGIC   <text x="30" y="108" font-size="15" fill="#1B3139">• Receives rewards for actions</text>
# MAGIC   <text x="30" y="131" font-size="15" fill="#1B3139">• Goal: maximize cumulative reward</text>
# MAGIC   <text x="30" y="154" font-size="15" fill="#1B3139">• Learns optimal policy over time</text>
# MAGIC   <text x="30" y="177" font-size="15" font-weight="bold" fill="#1B3139">Examples:</text>
# MAGIC   <text x="30" y="200" font-size="15" fill="#1B3139">• Game playing, robotics, recommendation</text>
# MAGIC </svg>
# MAGIC
# MAGIC <!-- Agent-Environment Loop Graph -->
# MAGIC <svg width="420" viewBox="0 0 400 260" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Agent-Environment Loop</title>
# MAGIC   <rect x="10" y="20" width="380" height="220" rx="12" fill="#FFFFFF" stroke="#388E3C" stroke-width="2"/>
# MAGIC   <text x="200" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#2E7D32">Agent-Environment Loop</text>
# MAGIC
# MAGIC   <!-- Agent box -->
# MAGIC   <rect x="40" y="80" width="120" height="60" rx="10" fill="#E8F5E9" stroke="#388E3C" stroke-width="2"/>
# MAGIC   <text x="100" y="115" text-anchor="middle" font-size="14" font-weight="bold" fill="#2E7D32">Agent</text>
# MAGIC
# MAGIC   <!-- Environment box -->
# MAGIC   <rect x="240" y="80" width="120" height="60" rx="10" fill="#E3F2FD" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="300" y="115" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Environment</text>
# MAGIC
# MAGIC   <!-- Action arrow (top, agent to environment) -->
# MAGIC   <defs>
# MAGIC     <marker id="arrowOr" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto" markerUnits="strokeWidth">
# MAGIC       <polygon points="0 0, 10 3.5, 0 7" fill="#F57C00"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC   <path d="M160 90 L240 90" stroke="#F57C00" stroke-width="1.5" fill="none" marker-end="url(#arrowOr)"/>
# MAGIC   <text x="200" y="82" text-anchor="middle" font-size="11" fill="#E65100" font-weight="bold">Action</text>
# MAGIC
# MAGIC   <!-- Reward arrow (bottom, environment to agent) -->
# MAGIC   <defs>
# MAGIC     <marker id="arrowGr" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto" markerUnits="strokeWidth">
# MAGIC       <polygon points="0 0, 10 3.5, 0 7" fill="#388E3C"/>
# MAGIC     </marker>
# MAGIC   </defs>
# MAGIC   <path d="M240 130 L160 130" stroke="#388E3C" stroke-width="1.5" fill="none" marker-end="url(#arrowGr)"/>
# MAGIC   <text x="200" y="152" text-anchor="middle" font-size="11" fill="#2E7D32" font-weight="bold">Reward + State</text>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC  - **Repeat:** observe state → take action → receive reward
# MAGIC  - **Goal:** maximize total cumulative reward
# MAGIC
# MAGIC
# MAGIC The agent interacts with the environment in a loop — choosing actions, observing new states, and receiving rewards — learning over time which actions maximize long-term reward.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. The ML Full Lifecycle

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B1. Where Model Training and Evaulation Fit in the Machine Learning Lifecycle
# MAGIC
# MAGIC The Machine Learning lifecycle divides into two broad phases: **model development** and **production**.
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
# MAGIC   <text x="50" y="200" font-size="13" font-weight="600" fill="#0b2026">Model Development</text>
# MAGIC   <text x="50" y="215" font-size="11" fill="#618794">(static historical data)</text>
# MAGIC
# MAGIC   <!-- 1st step: Business problem -->
# MAGIC   <rect x="43" y="98" width="115" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.2"/>
# MAGIC   <text x="100" y="120" text-anchor="middle" font-size="12" font-weight="600" fill="#0b2026">Business</text>
# MAGIC   <text x="100" y="138" text-anchor="middle" font-size="12" font-weight="600" fill="#0b2026">Problem</text>
# MAGIC
# MAGIC   <!-- 2nd step:  Define success criteria -->
# MAGIC   <rect x="175" y="98" width="115" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.2"/>
# MAGIC   <text x="232" y="120" text-anchor="middle" font-size="12" font-weight="600" fill="#0b2026">Define Success</text>
# MAGIC   <text x="232" y="138" text-anchor="middle" font-size="12" font-weight="600" fill="#0b2026">Criteria</text>
# MAGIC
# MAGIC   <!-- 3rd step: Data collection (highlighted) -->
# MAGIC   <rect x="305" y="98" width="115" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.5"/>
# MAGIC   <text x="360" y="120" text-anchor="middle" font-size="12" font-weight="600" fill="#0b2026">Data Collection</text>
# MAGIC
# MAGIC   <!-- 4th step: Data prepprocessing / feature engineering  -->
# MAGIC   <rect x="435" y="98" width="150" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.5"/>
# MAGIC   <text x="510" y="116" text-anchor="middle" font-size="12" font-weight="600" fill="#0b2026">Data Preprocessing /</text>
# MAGIC   <text x="510" y="132" text-anchor="middle" font-size="12" font-weight="600" fill="#0b2026">Feature Engineering</text>
# MAGIC
# MAGIC   <!-- 5th step: Model training (highlighted)-->
# MAGIC   <rect x="605" y="98" width="115" height="52" rx="8" fill="#2E8B57" fill-opacity="0.18" stroke="#2E8B57" stroke-width="1.2"/>
# MAGIC   <text x="662" y="120" text-anchor="middle" font-size="12" font-weight="600" fill="#0b2026">Model Training</text>
# MAGIC   <text x="667" y="140" text-anchor="middle" font-size="10" fill="#618794">*This module*</text>
# MAGIC
# MAGIC   <!-- Arrow from Model Training to Model evaluation  -->
# MAGIC   <path d="M662 150 L662 200" fill="none" stroke="#1B3139" stroke-width="1.8" marker-end="url(#mlc-arrow)"/>
# MAGIC
# MAGIC   <!-- 6th step: Model evaluation (highlighted) -->
# MAGIC   <rect x="605" y="200" width="115" height="52" rx="8" fill="#2E8B57" fill-opacity="0.18" stroke="#2E8B57" stroke-width="1.2"/>
# MAGIC   <text x="662" y="220" text-anchor="middle" font-size="12" font-weight="600" fill="#0b2026">Model Evaluation</text>
# MAGIC   <text x="665" y="240" text-anchor="middle" font-size="10" fill="#618794">*This module*</text>
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
# MAGIC   <text x="50" y="400"  font-size="13" font-weight="600" fill="#0b2026">Deployment & Production</text>
# MAGIC   <text x="50" y="415"  font-size="11" fill="#618794">(continuously changing data)</text>
# MAGIC
# MAGIC   <!-- 7th step: Model deployment -->
# MAGIC   <rect x="440" y="350" width="115" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.5"/>
# MAGIC   <text x="500" y="380" text-anchor="middle" font-size="11.5" font-weight="600" fill="#0b2026">Model Deployment</text>
# MAGIC
# MAGIC   <!-- 8th step: Model Monitoring -->
# MAGIC   <rect x="305" y="350" width="115" height="52" rx="8" fill="#ffffff" stroke="#8B9DAA" stroke-width="1.5"/>
# MAGIC   <text x="360" y="380" text-anchor="middle" font-size="11.5" font-weight="600" fill="#0b2026">Model Monitoring</text>
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
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC What are the stages of the Machine Learning Full Lifecycle?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">The diagram above illustrates the full lifecycle from business problem to a deployed, monitored model.</p>
# MAGIC <ol style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li><strong>Define Business Problem &amp; Success Criteria</strong>: Start by clarifying the business objective and how success will be measured.</li>
# MAGIC <li><strong>Data Collection &amp; Preprocessing</strong>: Gather relevant data and prepare it for modeling.</li>
# MAGIC <li><strong>Model Training &amp; Evaluation</strong>: Build and evaluate models using historical data to select the best approach.</li>
# MAGIC <li><strong>Deployment &amp; Monitoring</strong>: Deploy the chosen model to production and monitor its performance on new, continuously changing data.</li>
# MAGIC </ol>
# MAGIC <p style="margin-top: 10px;">The development phase operates on static historical data, while the production phase must handle continuously changing new data — a transition where most teams encounter significant challenges.</p>
# MAGIC <p><strong>The key takeaway:</strong> model training is just one slice of a much larger process, and the loop never truly closes — monitoring feeds back into further data collection and retraining.</p>
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ### B1 (2nd version). Where Model Training and Evaulation Fit in the Machine Learning Lifecycle
# MAGIC
# MAGIC The Machine Learning lifecycle divides into two broad phases: **model development** and **production**.
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
# MAGIC   <text x="95" y="109" text-anchor="middle" font-size="12"font-weight="bold" fill="#1B3139">Problem &amp;</text>
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
# MAGIC   <rect x="515" y="65" width="120" height="70" rx="6" fill="#00A972" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="575" y="104" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Model Training</text>
# MAGIC   <text x="575" y="124" text-anchor="middle" font-size="10" fill="#FFFFFF">*This module*</text>
# MAGIC
# MAGIC   <rect x="675" y="65" width="120" height="70" rx="6" fill="#00A972" stroke="#2E7D32" stroke-width="1.5"/>
# MAGIC   <text x="735" y="104" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Model Evaluation</text>
# MAGIC   <text x="735" y="124" text-anchor="middle" font-size="10" fill="#FFFFFF">*This module*</text>
# MAGIC
# MAGIC   <!-- Production steps -->
# MAGIC   <rect x="195" y="205" width="120" height="45" rx="6" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="255" y="232" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Model Monitoring</text>
# MAGIC
# MAGIC   <rect x="355" y="205" width="120" height="45" rx="6" fill="#FFFFFF" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="415" y="232" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Model Deployment</text>
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
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC What are the stages of the Machine Learning Full Lifecycle?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">The diagram above illustrates the full lifecycle from business problem to a deployed, monitored model.</p>
# MAGIC <ol style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li><strong>Define Business Problem &amp; Success Criteria</strong>: Start by clarifying the business objective and how success will be measured.</li>
# MAGIC <li><strong>Data Collection &amp; Preprocessing</strong>: Gather relevant data and prepare it for modeling.</li>
# MAGIC <li><strong>Model Training &amp; Evaluation</strong>: Build and evaluate models using historical data to select the best approach.</li>
# MAGIC <li><strong>Deployment &amp; Monitoring</strong>: Deploy the chosen model to production and monitor its performance on new, continuously changing data.</li>
# MAGIC </ol>
# MAGIC <p style="margin-top: 10px;">The development phase operates on static historical data, while the production phase must handle continuously changing new data — a transition where most teams encounter significant challenges.</p>
# MAGIC <p><strong>The key takeaway:</strong> model training is just one slice of a much larger process, and the loop never truly closes — monitoring feeds back into further data collection and retraining.</p>
# MAGIC </div>
# MAGIC </details>
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cell 10
# MAGIC %md-sandbox
# MAGIC ### B2. The Machine Learning Full Lifecycle
# MAGIC
# MAGIC Building a model is only one stage in a larger workflow. The full lifecycle spans from defining the business problem through deployment and ongoing monitoring.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Stage</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Phase</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Business Problem</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; color: #1565C0; font-weight: 600;">Development</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Define the business objective and frame it as a machine learning problem.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Define Success Criteria</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; color: #1565C0; font-weight: 600;">Development</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Establish measurable goals such as accuracy, latency, or revenue impact to determine whether the model meets business needs.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Data Collection &amp; Preprocessing</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; color: #1565C0; font-weight: 600;">Development</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Gather, clean, and transform relevant data into features suitable for model training.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Model Training</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; color: #1565C0; font-weight: 600;">Development</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Train candidate models on historical data, iterating on algorithms and hyperparameters to optimize performance.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Model Evaluation</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; color: #1565C0; font-weight: 600;">Development</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Assess model performance on held-out data and compare experiments to select the best candidate.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Model Deployment</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; color: #E65100; font-weight: 600;">Production</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Package and serve the selected model in a production environment to generate predictions on continuously arriving new data.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Model Monitoring</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; color: #E65100; font-weight: 600;">Production</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Track model performance on live data, detect drift or degradation, and feed insights back into retraining.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B3. Core Machine Learning Development Issues
# MAGIC
# MAGIC The modern ML lifecycle comes with three fundamental challenges that grow with team size and model complexity.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Challenge</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Reproducibility &amp; Experiment Tracking</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Difficulty in ensuring consistent results across different environments and effectively documenting and organizing experiments.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Model Evaluation &amp; Comparison</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Challenges in accurately comparing and selecting the best-performing model due to variations in evaluation metrics and experimental design.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Deployment &amp; Standardization</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Complexities in transitioning models to production, ensuring seamless integration, and maintaining standardized deployment processes.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC MLflow was designed to address all three of these challenges in a single, unified platform.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. MLflow for Model Development

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C1. What Is MLflow?
# MAGIC
# MAGIC **MLflow** is an open-source platform for managing the end-to-end machine learning lifecycle. It is co-developed by Databricks and the ML community and comes pre-installed on Databricks Runtime.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 160" role="img" style="font-family: sans-serif;">
# MAGIC   <title>MLflow Capabilities</title>
# MAGIC
# MAGIC   <!-- Central label -->
# MAGIC   <rect x="330" y="20" width="200" height="50" rx="8" fill="#1B3139" stroke="none"/>
# MAGIC   <text x="430" y="50" text-anchor="middle" font-size="18" font-weight="bold" fill="#FFFFFF">MLflow</text>
# MAGIC
# MAGIC   <!-- Capability boxes -->
# MAGIC   <rect x="20" y="100" width="150" height="44" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="95" y="127" text-anchor="middle" font-size="12" fill="#1B3139">Experiment Tracking</text>
# MAGIC
# MAGIC   <rect x="190" y="100" width="150" height="44" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="265" y="127" text-anchor="middle" font-size="12" fill="#1B3139">Evaluation</text>
# MAGIC
# MAGIC   <rect x="360" y="100" width="150" height="44" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="435" y="127" text-anchor="middle" font-size="12" fill="#1B3139">Model Registry</text>
# MAGIC
# MAGIC   <rect x="530" y="100" width="150" height="44" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="605" y="127" text-anchor="middle" font-size="12" fill="#1B3139">Visualization</text>
# MAGIC
# MAGIC   <rect x="700" y="100" width="140" height="44" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="770" y="127" text-anchor="middle" font-size="12" fill="#1B3139">Serving</text>
# MAGIC
# MAGIC   <!-- Connecting lines -->
# MAGIC   <line x1="435" y1="70" x2="95" y2="100" stroke="#1976D2" stroke-width="1"/>
# MAGIC   <line x1="435" y1="70" x2="265" y2="100" stroke="#1976D2" stroke-width="1"/>
# MAGIC   <line x1="435" y1="70" x2="435" y2="100" stroke="#1976D2" stroke-width="1"/>
# MAGIC   <line x1="435" y1="70" x2="605" y2="100" stroke="#1976D2" stroke-width="1"/>
# MAGIC   <line x1="435" y1="70" x2="770" y2="100" stroke="#1976D2" stroke-width="1"/>
# MAGIC </svg>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C2. The Four Components of MLflow
# MAGIC
# MAGIC MLflow is organized into four components. This course focuses on **Tracking** and **Evaluation**.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Component</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Purpose</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Tracking</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Track, compare, and reproduce your ML experiments with powerful tracking capabilities.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Evaluation</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Automated evaluation tools for foundational ML techniques like classification and regression.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Models</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">A unified format to package, share, and deploy models across frameworks.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Model Registry &amp; Deployment</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Streamline model lifecycle with version control and managed deployment.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     On Databricks, the model registry is managed by <strong>Models in Unity Catalog</strong>, which provides unified governance, lineage, and versioning for all registered models. For new projects, it is recommended to use Unity Catalog to ensure consistent model management and deployment.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC **APIs available:** CLI, Python, R, Java, REST

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C3. MLflow Experiment Tracking
# MAGIC
# MAGIC Experiment tracking makes your ML workflow more manageable and transparent by recording every detail of a training run, which means at any point you can answer: 
# MAGIC - Which run produced this model? 
# MAGIC - What hyperparameters did it use? 
# MAGIC - What was the accuracy?
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 180" role="img" style="font-family: sans-serif;">
# MAGIC   <title>MLflow Experiment Tracking</title>
# MAGIC
# MAGIC   <!-- Central box -->
# MAGIC   <rect x="280" y="10" width="300" height="44" rx="8" fill="#1B3139"/>
# MAGIC   <text x="430" y="37" text-anchor="middle" font-size="14" font-weight="bold" fill="#FFFFFF">Experiment Tracking</text>
# MAGIC
# MAGIC   <!-- Four tracked items -->
# MAGIC   <rect x="40" y="90" width="170" height="70" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="125" y="118" text-anchor="middle" font-size="13" font-weight="bold" fill="#1565C0">Parameters</text>
# MAGIC   <text x="125" y="140" text-anchor="middle" font-size="11" fill="#1B3139">Hyperparameters &amp;</text>
# MAGIC   <text x="125" y="155" text-anchor="middle" font-size="11" fill="#1B3139">model configurations</text>
# MAGIC
# MAGIC   <rect x="230" y="90" width="170" height="70" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="315" y="118" text-anchor="middle" font-size="13" font-weight="bold" fill="#1565C0">Metrics</text>
# MAGIC   <text x="315" y="140" text-anchor="middle" font-size="11" fill="#1B3139">Performance measures</text>
# MAGIC   <text x="315" y="155" text-anchor="middle" font-size="11" fill="#1B3139">for comparison</text>
# MAGIC
# MAGIC   <rect x="420" y="90" width="170" height="70" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="505" y="118" text-anchor="middle" font-size="13" font-weight="bold" fill="#1565C0">Artifacts</text>
# MAGIC   <text x="505" y="140" text-anchor="middle" font-size="11" fill="#1B3139">Trained models,</text>
# MAGIC   <text x="505" y="155" text-anchor="middle" font-size="11" fill="#1B3139">plots, &amp; files</text>
# MAGIC
# MAGIC   <rect x="610" y="90" width="170" height="70" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="695" y="118" text-anchor="middle" font-size="13" font-weight="bold" fill="#1565C0">Models</text>
# MAGIC   <text x="695" y="140" text-anchor="middle" font-size="11" fill="#1B3139">Trained model</text>
# MAGIC   <text x="695" y="155" text-anchor="middle" font-size="11" fill="#1B3139">logged with run</text>
# MAGIC
# MAGIC   <!-- Lines from header to boxes -->
# MAGIC   <line x1="425" y1="54" x2="125" y2="90" stroke="#1976D2" stroke-width="1"/>
# MAGIC   <line x1="425" y1="54" x2="315" y2="90" stroke="#1976D2" stroke-width="1"/>
# MAGIC   <line x1="425" y1="54" x2="505" y2="90" stroke="#1976D2" stroke-width="1"/>
# MAGIC   <line x1="425" y1="54" x2="695" y2="90" stroke="#1976D2" stroke-width="1"/>
# MAGIC </svg>
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C4. Autologging
# MAGIC
# MAGIC `mlflow.autolog()` automatically tracks ML development — for supported frameworks, often with a single line of code. It captures parameters, metrics, the trained model (with its dependencies), the model signature, and input examples, reducing manual instrumentation.
# MAGIC
# MAGIC </br>
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 13px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>import mlflow</code>
# MAGIC <code>mlflow.autolog()</code>
# MAGIC <code># Your training code here — MLflow captures everything automatically</code>
# MAGIC <code>model.fit(X_train, y_train)</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     <b>MLflow autologging</b> automatically records key details of your training runs, including parameters, metrics, the trained model and its dependencies, model signature, and input examples. The exact information captured depends on the ML framework you use. This makes experiment tracking effortless and ensures reproducibility without manual logging.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,Cell 17
# MAGIC %md-sandbox
# MAGIC ### C5. Custom Logging
# MAGIC
# MAGIC Autologging is great for the common case, but sometimes you need finer control — a custom metric, an arbitrary artifact, or parameters MLflow doesn't know about. That's what custom logging is for.
# MAGIC
# MAGIC The four calls you'll use most:
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 110%; max-width: 946px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 18px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Function</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Purpose</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;"><code>mlflow.log_metric()</code></td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Record a custom evaluation score</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;"><code>mlflow.log_model()</code></td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Save the trained model with its framework flavor</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;"><code>mlflow.log_params()</code></td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Log a dictionary of parameters</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;"><code>mlflow.log_artifact()</code></td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Attach any file (plots, data, configs)</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC </br>
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 13px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>import mlflow</code>
# MAGIC <code># Log custom metrics</code>
# MAGIC <code>y_pred = model.predict(X_test)</code>
# MAGIC <code>super_score = custom_score(y_test, y_pred)</code>
# MAGIC <code>mlflow.log_metric('super_score', super_score)</code>
# MAGIC </br>
# MAGIC <code># Log model</code>
# MAGIC <code>mlflow.sklearn.log_model(model, name="random_forest_model")</code>
# MAGIC </br>
# MAGIC <code># Log params</code>
# MAGIC <code>mlflow.log_params({'param1': 123, 'param2': 'abc'})</code></pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #00A972; background: rgba(0,169,114,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#00A972; margin-bottom:6px; font-size:15pt;">Success</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     For best results, combine <code>mlflow.autolog()</code> with custom logging calls. Autologging captures standard metrics and artifacts automatically, while custom calls let you record domain-specific metrics, parameters, or files unique to your project. This approach ensures comprehensive experiment tracking and reproducibility.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. MLflow Concepts and Examining Runs

# COMMAND ----------

# DBTITLE 1,Cell 19
# MAGIC %md-sandbox
# MAGIC ### D1. Experiments and Runs
# MAGIC
# MAGIC Two terms you'll hear constantly: **experiment** and **run**. An experiment is the higher-level container — think of it as a folder for all the runs related to a single problem or modeling effort.
# MAGIC
# MAGIC <div style="max-width: 600px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 460 320" role="img" style="font-family: sans-serif;">
# MAGIC   <title>MLflow Experiment and Run Hierarchy</title>
# MAGIC
# MAGIC   <!-- Experiment container -->
# MAGIC   <rect x="40" y="20" width="380" height="280" rx="12" fill="#F9F7F4" stroke="#1B3139" stroke-width="2"/>
# MAGIC   <text x="230" y="50" text-anchor="middle" font-size="16" font-weight="bold" fill="#1B3139">Experiment</text>
# MAGIC   <line x1="80" y1="60" x2="380" y2="60" stroke="#1B3139" stroke-width="1"/>
# MAGIC
# MAGIC   <!-- Runs -->
# MAGIC   <rect x="70" y="75" width="320" height="35" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="230" y="97" text-anchor="middle" font-size="13" fill="#1B3139">Run 1</text>
# MAGIC
# MAGIC   <rect x="70" y="120" width="320" height="35" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="230" y="142" text-anchor="middle" font-size="13" fill="#1B3139">Run 2</text>
# MAGIC
# MAGIC   <rect x="70" y="165" width="320" height="35" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="230" y="187" text-anchor="middle" font-size="13" fill="#1B3139">Run 3 (Parent)</text>
# MAGIC
# MAGIC   <rect x="100" y="210" width="270" height="30" rx="5" fill="#FFFFFF" stroke="#1976D2" stroke-width="1" stroke-dasharray="3"/>
# MAGIC   <text x="235" y="230" text-anchor="middle" font-size="12" fill="#1B3139">Run 3.1 (Nested)</text>
# MAGIC
# MAGIC   <rect x="100" y="250" width="270" height="30" rx="5" fill="#FFFFFF" stroke="#1976D2" stroke-width="1" stroke-dasharray="3"/>
# MAGIC   <text x="235" y="270" text-anchor="middle" font-size="12" fill="#1B3139">Run 3.2 (Nested)</text>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC What are MLflow Experiments and Runs?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;"><strong>MLflow Experiment:</strong></p>
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li>A higher-level organizational unit that encompasses a set of runs</li>
# MAGIC <li>Groups and organizes related runs, typically held to explore different configurations, parameters, or algorithms</li>
# MAGIC <li>Two systems:
# MAGIC   <ul>
# MAGIC     <li><strong>Notebook Experiment</strong> — tied to a specific notebook; created automatically when you call <code>start_run()</code></li>
# MAGIC     <li><strong>Workspace Experiment</strong> — lives at a path you specify; multiple notebooks can create runs in it</li>
# MAGIC   </ul>
# MAGIC </li>
# MAGIC </ul>
# MAGIC
# MAGIC <p style="margin-top: 10px;"><strong>MLflow Run:</strong></p>
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li>A single execution of data science code</li>
# MAGIC <li>Belongs to exactly one experiment</li>
# MAGIC <li>Contains metadata + artifacts</li>
# MAGIC <li>Logged models are accessible through the framework-agnostic <strong>PyFunc</strong> flavor</li>
# MAGIC </ul>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     MLflow offers two types of experiments: <b>notebook experiments</b> (created automatically for each notebook) and <b>workspace experiments</b> (shared across notebooks and users). 
# MAGIC     <br><br>
# MAGIC     Use workspace experiments for collaborative projects or when you want to organize runs from multiple notebooks in one place. Notebook experiments are ideal for individual, iterative work. Choosing the right experiment type helps keep your ML projects organized and reproducible.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,Cell 20
# MAGIC %md-sandbox
# MAGIC ### D2. Run Contents — Metadata and Artifacts
# MAGIC
# MAGIC A **Run** is a single execution of your code — one training pass. Each run belongs to exactly one experiment and contains metadata and artifacts.
# MAGIC
# MAGIC <div style="max-width: 600px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 460 320" role="img" style="font-family: sans-serif;">
# MAGIC   <title>MLflow Experiment with Run Contents</title>
# MAGIC
# MAGIC   <!-- Experiment container -->
# MAGIC   <rect x="40" y="20" width="380" height="280" rx="12" fill="#F9F7F4" stroke="#1B3139" stroke-width="2"/>
# MAGIC   <text x="230" y="50" text-anchor="middle" font-size="16" font-weight="bold" fill="#1B3139">Experiment</text>
# MAGIC   <line x1="80" y1="60" x2="380" y2="60" stroke="#1B3139" stroke-width="1"/>
# MAGIC
# MAGIC   <!-- Run 1 (collapsed) -->
# MAGIC   <rect x="70" y="75" width="320" height="35" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="230" y="97" text-anchor="middle" font-size="13" fill="#1B3139">Run 1</text>
# MAGIC
# MAGIC   <!-- Run 2 (expanded to show artifacts) -->
# MAGIC   <rect x="70" y="125" width="320" height="160" rx="6" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="230" y="148" text-anchor="middle" font-size="13" font-weight="bold" fill="#1B3139">Run 2</text>
# MAGIC   <line x1="90" y1="158" x2="370" y2="158" stroke="#1976D2" stroke-width="0.5"/>
# MAGIC
# MAGIC   <!-- Artifact items inside Run 2 -->
# MAGIC   <rect x="100" y="168" width="260" height="28" rx="5" fill="#FFFFFF" stroke="#1976D2" stroke-width="1" stroke-dasharray="3"/>
# MAGIC   <text x="230" y="186" text-anchor="middle" font-size="12" fill="#1B3139">MLmodel</text>
# MAGIC
# MAGIC   <rect x="100" y="204" width="260" height="28" rx="5" fill="#FFFFFF" stroke="#1976D2" stroke-width="1" stroke-dasharray="3"/>
# MAGIC   <text x="230" y="222" text-anchor="middle" font-size="12" fill="#1B3139">conda.yaml</text>
# MAGIC
# MAGIC   <rect x="100" y="240" width="260" height="28" rx="5" fill="#FFFFFF" stroke="#1976D2" stroke-width="1" stroke-dasharray="3"/>
# MAGIC   <text x="230" y="258" text-anchor="middle" font-size="12" fill="#1B3139">model.pkl</text>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC What is an MLflow Run and what does it contain?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li><strong>MLflow Run:</strong> A single execution of data science code — one training pass.</li>
# MAGIC <li>Belongs to exactly one experiment.</li>
# MAGIC <li>Contains:
# MAGIC   <ul>
# MAGIC     <li><strong>Metadata</strong> — params, metrics, tags, source code reference</li>
# MAGIC     <li><strong>Artifacts</strong> — MLmodel file, conda.yaml, model.pkl, plus any custom files you log</li>
# MAGIC   </ul>
# MAGIC </li>
# MAGIC <li>Has a default <strong>PyFunc flavor</strong> — a framework-agnostic wrapper that lets your model be deployed to Databricks, SageMaker, Kubernetes, or any MLflow-compatible serving environment.</li>
# MAGIC </ul>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     The Experiment → Run hierarchy in MLflow is fundamental for tracking and comparing your work. Each run within an experiment logs parameters, metrics, and artifacts in a consistent structure, making it easy to review, analyze, and improve your models. This organization enables clear side-by-side comparisons and supports reproducibility across your ML projects.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,Cell 21
# MAGIC %md-sandbox
# MAGIC ### D3. Examining Past Runs
# MAGIC
# MAGIC Once you have runs, you'll want to find and compare them. Two ways:
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Method</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">MLflow UI</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">List and filter runs by metrics directly on the Databricks platform. Visual comparison of run parameters and performance.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">MLflow API</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Programmatic access via <code>MlflowClient</code> — list experiments, search runs by metrics, model type, and more.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC **Example — searching runs programmatically:**
# MAGIC
# MAGIC The snippet below shows `MlflowClient().search_runs` with filters, max results, and ordering:
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 13px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>from mlflow import MlflowClient</code>
# MAGIC </br>
# MAGIC <code>runs = MlflowClient().search_runs(
# MAGIC     experiment_ids=["0"],
# MAGIC     filter_string="params.model = 'random_forest'",
# MAGIC     max_results=5,
# MAGIC     order_by=["metrics.accuracy DESC"],
# MAGIC )</code>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #4299E0; background: rgba(66,153,224,0.10); padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#2272B4; margin-bottom:6px; font-size:15pt;">Info</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     The MLflow UI is ideal for quick, visual exploration—sortable columns, charts, and side-by-side comparisons make it easy to analyze runs interactively. The MLflow API is best for automation and scripting, such as programmatically retrieving the best run or registering models. Most workflows combine both approaches: use the UI for insight and the API for repeatable tasks and integration into pipelines.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cell 20
# MAGIC %md
# MAGIC ## E. Conclusion
# MAGIC
# MAGIC In this lecture, you covered the foundations of model development and how MLflow supports the ML lifecycle:
# MAGIC
# MAGIC 1. **Types of Machine Learning** — Supervised, unsupervised, hybrid, and reinforcement learning paradigms, with supervised subtypes (regression, classification, forecasting).
# MAGIC 2. **The ML Full Lifecycle** — The end-to-end workflow from business problem through deployment, and the three core challenges: reproducibility, evaluation, and standardization.
# MAGIC 3. **MLflow for Model Development** — MLflow's four components (Tracking, Evaluation, Models, Registry), experiment tracking, autologging with `mlflow.autolog()`, and custom logging.
# MAGIC 4. **MLflow Concepts and Examining Runs** — The experiment/run hierarchy, metadata vs. artifacts stored in each run, and how to retrieve past runs via the UI and API.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
