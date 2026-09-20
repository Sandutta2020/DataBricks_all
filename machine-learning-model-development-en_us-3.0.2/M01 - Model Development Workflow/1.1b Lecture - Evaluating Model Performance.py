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
# MAGIC # Lecture — Evaluating Model Performance
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This lecture covers how to measure and compare machine learning model quality. You will learn the end-to-end model development workflow, how to structure data splits for reliable assessment, and which metrics to use for regression, classification, and clustering tasks.
# MAGIC
# MAGIC This lecture covers 4 sections that build on each other:
# MAGIC
# MAGIC - **A. Purpose of Evaluation Metrics**. Why we compute metrics, the end-to-end model development workflow (prepare → split → train → tune → evaluate), and the roles of train/validation/test splits. Tools: MLflow for experiment tracking, Optuna for hyperparameter tuning.
# MAGIC - **B. Regression Metrics**. R², Mean Absolute Error, Mean Squared Error, and Root Mean Squared Error — when to use each and how to compute them.
# MAGIC - **C. Classification Metrics**. The confusion matrix, accuracy, precision, recall, F1 score, log loss (cross-entropy), and ROC/AUC — choosing the right metric based on the business cost of errors.
# MAGIC - **D. Clustering Metrics**. K-Means fundamentals, the silhouette score for measuring cluster separation, and the elbow method for choosing the optimal number of clusters.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this lecture, you will be able to:
# MAGIC
# MAGIC 1. Describe the end-to-end model development workflow and explain the distinct role of training, validation, and test data in model selection.
# MAGIC 2. Select and interpret the appropriate metrics for regression, classification, and clustering tasks.
# MAGIC 3. Choose between precision, recall, and F1 based on the business cost of different error types.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Purpose of Evaluation Metrics

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### A1. Why Evaluation Metrics Matter
# MAGIC
# MAGIC Evaluation metrics serve four essential purposes in the model development workflow:
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Purpose</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Quantify Performance</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Provide a numerical representation of how well a model is performing.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Enable Comparison</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Compare different models or different versions of the same model on equal footing.</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Guide Tuning</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Direct the fine-tuning of model hyperparameters toward better outcomes.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Objective Selection</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Provide an objective basis for choosing between different models or approaches.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# DBTITLE 1,Cell 5
# MAGIC %md-sandbox
# MAGIC ### A2. How to Build and Evaluate Models
# MAGIC
# MAGIC
# MAGIC <div style="max-width: 1000px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 395" role="img" style="font-family: sans-serif;">
# MAGIC   <title>How to Build and Evaluate Models</title>
# MAGIC
# MAGIC   <!-- Data Preparation Section -->
# MAGIC   <rect x="40" y="20" width="780" height="140" rx="10" fill="#FFFFFF" stroke="#E0E0E0" stroke-width="1.5"/>
# MAGIC   <text x="60" y="45" font-size="11" font-weight="bold" fill="#666666">DATA PREPARATION</text>
# MAGIC
# MAGIC   <!-- Target, Variables bar -->
# MAGIC   <rect x="60" y="55" width="740" height="30" rx="5" fill="#FF3621" />
# MAGIC   <text x="430" y="75" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Target &amp; Variables</text>
# MAGIC
# MAGIC   <!-- Features bar -->
# MAGIC   <rect x="60" y="92" width="740" height="30" rx="5" fill="#1B3139" />
# MAGIC   <text x="430" y="112" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Features</text>
# MAGIC
# MAGIC   <!-- Split Strategy bar -->
# MAGIC   <rect x="60" y="129" width="740" height="30" rx="5" fill="#F57C00" />
# MAGIC   <text x="430" y="149" text-anchor="middle" font-size="12" font-weight="bold" fill="#FFFFFF">Split Strategy</text>
# MAGIC
# MAGIC   <!-- Arrow down -->
# MAGIC   <path d="M430 165 L430 190" stroke="#1B3139" stroke-width="2.5" fill="none" marker-end="url(#arr_a2)"/>
# MAGIC
# MAGIC   <!-- Model Building Section -->
# MAGIC   <rect x="40" y="195" width="780" height="165" rx="10" fill="#FFFFFF" stroke="#E0E0E0" stroke-width="1.5"/>
# MAGIC   <text x="60" y="220" font-size="11" font-weight="bold" fill="#666666">MODEL BUILDING &amp; EVALUATION</text>
# MAGIC
# MAGIC   <!-- Hyperparameter Tuning -->
# MAGIC   <rect x="60" y="232" width="240" height="45" rx="8" fill="#FFF3E0" stroke="#F57C00" stroke-width="1.5"/>
# MAGIC   <text x="180" y="260" text-anchor="middle" font-size="12" font-weight="bold" fill="#E65100">Train Multiple Models</text>
# MAGIC
# MAGIC   <!-- Arrow right -->
# MAGIC   <path d="M305 255 L330 255" stroke="#1B3139" stroke-width="2" fill="none" marker-end="url(#arr_a2)"/>
# MAGIC
# MAGIC   <!-- Train Multiple Models -->
# MAGIC   <rect x="335" y="232" width="220" height="45" rx="8" fill="#E3F2FD" stroke="#1976D2" stroke-width="1.5"/>
# MAGIC   <text x="445" y="260" text-anchor="middle" font-size="12" font-weight="bold" fill="#1565C0">Hyperparameter Tuning</text>
# MAGIC
# MAGIC   <!-- Arrow right -->
# MAGIC   <path d="M560 255 L585 255" stroke="#1B3139" stroke-width="2" fill="none" marker-end="url(#arr_a2)"/>
# MAGIC
# MAGIC   <!-- Evaluate Champion -->
# MAGIC   <rect x="590" y="232" width="210" height="45" rx="8" fill="#E8F5E9" stroke="#388E3C" stroke-width="1.5"/>
# MAGIC   <text x="695" y="260" text-anchor="middle" font-size="12" font-weight="bold" fill="#2E7D32">Evaluate Champion</text>
# MAGIC
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC Building and Evaluating Model Workflows
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">The end-to-end workflow for building and evaluating models follows these steps:</p>
# MAGIC
# MAGIC <ol style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li><strong>Prepare your dataset</strong>: Clean, transform, and select features and target variables.</li>
# MAGIC <li><strong>Split the data</strong>: Use a strategy to divide data into training, validation, and test sets.</li>
# MAGIC <li><strong>Train multiple candidate models</strong>: Track every run with <strong>MLflow</strong> for experiment management.</li>
# MAGIC <li><strong>Hyperparameter tuning and selection</strong>: Use <strong>Optuna</strong> and the validation set to pick a champion model.</li>
# MAGIC <li><strong>Final evaluation</strong>: Assess the champion on the held-out test set to measure generalizability.</li>
# MAGIC </ol>
# MAGIC
# MAGIC </div>
# MAGIC </details>
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cell 6
# MAGIC %md-sandbox
# MAGIC ### A3. Train, Validation, and Test Split — Cheat Sheet
# MAGIC
# MAGIC The table below is the cheat sheet: training data directly updates model parameters; validation data indirectly influences them through hyperparameter choices; test data has no influence at all — it only measures generalizability.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Dataset</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Purpose</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Usage</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Impact on Model</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600; color: #1565C0;">Training</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Learn patterns from data</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Minimize loss during optimization</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;"><strong>Direct</strong> impact on parameters</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600; color: #E65100;">Validation</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Tune hyperparameters; prevent overfitting</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Compare models &amp; select champion</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;"><strong>Indirect</strong> impact on parameters</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600; color: #2E7D32;">Test</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Assess real-world generalizability</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Final evaluation on unseen data</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;"><strong>No influence</strong> on training</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Regression Metrics

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B1. Common Regression Metrics
# MAGIC
# MAGIC Regression models predict continuous outputs. These four metrics quantify prediction error in different ways.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Metric</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Direction</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">R² (Coefficient of Determination)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Measures how well the model explains the variation in the target variable. At most 1 (a perfect fit); can be negative when the model is worse than predicting the mean.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Larger is better</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Mean Absolute Error (MAE)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Average absolute difference between actual and predicted values.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Lower is better</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Mean Squared Error (MSE)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Average of squared differences between actual and predicted values. Squaring gives higher weight to large errors.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Lower is better</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Root Mean Squared Error (RMSE)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Square root of MSE, making it interpretable in the original units of the target.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Lower is better</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# DBTITLE 1,Cell 9
# MAGIC %md-sandbox
# MAGIC ### B2. Regression Metrics in Code
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Metric</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Code</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">R² (Coefficient of Determination)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;"><code style="font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px;">from sklearn.metrics import r2_score</code><br><code style="font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px;">r2_score(y_true, y_pred)</code></td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Mean Absolute Error (MAE)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;"><code style="font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px;">from sklearn.metrics import mean_absolute_error</code><br><code style="font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px;">mean_absolute_error(y_true, y_pred)</code></td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Mean Squared Error (MSE)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;"><code style="font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px;">from sklearn.metrics import mean_squared_error</code><br><code style="font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px;">mean_squared_error(y_true, y_pred)</code></td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Root Mean Squared Error (RMSE)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;"><code style="font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px;">from sklearn.metrics import root_mean_squared_error</code><br><code style="font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px;">root_mean_squared_error(y_true, y_pred)</code></td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Classification Metrics

# COMMAND ----------

# DBTITLE 1,Cell 11
# MAGIC %md-sandbox
# MAGIC ### C1. The Confusion Matrix
# MAGIC
# MAGIC The confusion matrix is the foundation for everything we're about to discuss. Each cell counts a kind of prediction outcome.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto;">
# MAGIC <svg width="100%" viewBox="0 0 860 340" role="img" style="font-family: sans-serif;">
# MAGIC   <title>Confusion Matrix</title>
# MAGIC
# MAGIC   <!-- Column header: Prediction -->
# MAGIC   <rect x="40" y="20" width="750" height="300" rx="12" fill="#FFFFFF" stroke="#1B3139" stroke-width="2"/>
# MAGIC   <text x="390" y="40" text-anchor="middle" font-size="14" font-weight="bold" fill="#1B3139">Prediction</text>
# MAGIC   <text x="290" y="70" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Positive</text>
# MAGIC   <text x="490" y="70" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Negative</text>
# MAGIC   <line x1="200" y1="80" x2="600" y2="80" stroke="#1B3139" stroke-width="1"/>
# MAGIC
# MAGIC   <!-- TP (top-left) -->
# MAGIC   <rect x="200" y="100" width="180" height="90" rx="8" fill="#00897B"/>
# MAGIC   <text x="155" y="155" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Positive</text>
# MAGIC   <text x="290" y="145" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">True Positive</text>
# MAGIC   <text x="100" y="200" text-anchor="middle" font-size="14" font-weight="bold" fill="#1B3139">Actual</text>
# MAGIC   <text x="290" y="167" text-anchor="middle" font-size="12" fill="#FFFFFF">(TP)</text>
# MAGIC
# MAGIC   <!-- FN (top-right) -->
# MAGIC   <rect x="410" y="100" width="180" height="90" rx="8" fill="#F57C00"/>
# MAGIC   <text x="500" y="145" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">False Negative</text>
# MAGIC   <text x="500" y="167" text-anchor="middle" font-size="12" fill="#FFFFFF">(FN)</text>
# MAGIC
# MAGIC   <!-- FP (bottom-left) -->
# MAGIC   <rect x="200" y="200" width="180" height="90" rx="8" fill="#F57C00"/>
# MAGIC   <text x="290" y="245" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">False Positive</text>
# MAGIC   <text x="290" y="267" text-anchor="middle" font-size="12" fill="#FFFFFF">(FP)</text>
# MAGIC
# MAGIC   <!-- TN (bottom-right) -->
# MAGIC   <rect x="410" y="200" width="180" height="90" rx="8" fill="#00897B"/>
# MAGIC   <text x="155" y="245" text-anchor="middle" font-size="12" font-weight="bold" fill="#1B3139">Negative</text>
# MAGIC   <text x="500" y="245" text-anchor="middle" font-size="13" font-weight="bold" fill="#FFFFFF">True Negative</text>
# MAGIC   <text x="500" y="267" text-anchor="middle" font-size="12" fill="#FFFFFF">(TN)</text>
# MAGIC
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC What are the four cells of the confusion matrix?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC   <li><strong>True Positive (TP)</strong> — predicted positive, actual positive. Correctly identified what we were looking for.</li>
# MAGIC   <li><strong>False Negative (FN)</strong> — predicted negative, actual positive. Missed it. Can be very costly: missed disease, missed fraud, missed security breach.</li>
# MAGIC   <li><strong>False Positive (FP)</strong> — predicted positive, actual negative. False alarm. Creates noise, wasted effort, and sometimes harm.</li>
# MAGIC   <li><strong>True Negative (TN)</strong> — predicted negative, actual negative. Correctly said "nothing here." Often the largest cell on imbalanced data, which is why raw accuracy can be misleading.</li>
# MAGIC </ul>
# MAGIC <p>The confusion matrix is the single most useful visualization for any classifier — from these four counts you derive every classification metric: accuracy, precision, recall, F1, and so on.</p>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C2. Accuracy, Precision, Recall, and F1 Score
# MAGIC
# MAGIC These four metrics are derived from the confusion matrix, each emphasizing different aspects of classification quality.
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Metric</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">When to Prioritize</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Accuracy</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Proportion of correctly classified instances. Can be misleading for imbalanced datasets.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Balanced class distributions</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Precision</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Of all predicted positives, how many are actually positive. TP / (TP + FP)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">False positives are costly (e.g., spam filter)</td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Recall (Sensitivity)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Of all actual positives, how many were correctly identified. TP / (TP + FN)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">False negatives are costly (e.g., disease detection)</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">F1 Score</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Harmonic mean of precision and recall. Balances both concerns in a single number.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Need balance between precision and recall</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>
# MAGIC
# MAGIC </br>
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 13px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score</code>
# MAGIC </br>
# MAGIC <code>accuracy = accuracy_score(y_true, y_pred)</code>
# MAGIC <code>precision = precision_score(y_true, y_pred)</code>
# MAGIC <code>recall = recall_score(y_true, y_pred)</code>
# MAGIC <code>f1 = f1_score(y_true, y_pred)</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     For metric functions like <code>precision_score</code>, <code>recall_score</code>, and <code>f1_score</code>, the default settings assume a binary classification problem (<code>average='binary'</code>, <code>pos_label=1</code>). For multiclass tasks, specify <code>average='macro'</code> or <code>average='weighted'</code> to get meaningful results.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,Cell 13
# MAGIC %md-sandbox
# MAGIC ### C3. Choosing Between Precision, Recall, and F1
# MAGIC
# MAGIC From the confusion matrix come the three metrics you'll use most often in classification. The right one to optimize depends on the business cost: high precision matters when false positives are expensive, high recall when false negatives are costly, and F1 when you need a balance between the two.
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
# MAGIC .blue{--accent:#4299E0;} .amber{--accent:#FFAB00;} .green{--accent:#00A972;}
# MAGIC .ds-card-title { font-size: 14pt; font-weight: 700; line-height: 1.25; margin: 0 0 8px; }
# MAGIC .ds-card-para { font-size: 12pt; color: #0b2026; line-height: 1.55; margin: 0; }
# MAGIC .ds-card-label { font-size: 16pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
# MAGIC </style>
# MAGIC
# MAGIC <div class="ds-row">
# MAGIC   <div class="ds-card blue">
# MAGIC     <div class="ds-card-label">Precision</div>
# MAGIC     <div class="ds-card-title">Minimize False Positives</div>
# MAGIC     <div class="ds-card-para">
# MAGIC       High precision is crucial when false positives are costly.<br><br>
# MAGIC       <b>Example:</b> Spam filter — ensure emails marked spam are truly spam.
# MAGIC     </div>
# MAGIC   </div>
# MAGIC   <div class="ds-card amber">
# MAGIC     <div class="ds-card-label">Recall</div>
# MAGIC     <div class="ds-card-title">Capture All Positives</div>
# MAGIC     <div class="ds-card-para">
# MAGIC       High recall is important when missing positives is costly.<br><br>
# MAGIC       <b>Example:</b> Medical diagnosis — identify all patients with a disease.
# MAGIC     </div>
# MAGIC   </div>
# MAGIC   <div class="ds-card green">
# MAGIC     <div class="ds-card-label">F1 Score</div>
# MAGIC     <div class="ds-card-title">Balance Precision & Recall</div>
# MAGIC     <div class="ds-card-para">
# MAGIC       F1 is useful when you need a balance between precision and recall.<br><br>
# MAGIC       <b>Example:</b> Search engine — retrieve relevant docs, minimize noise.
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC What do Precision, Recall, and F1 Score mean?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li><strong>Precision</strong> — Of everything I predicted positive, what fraction actually was positive?</li>
# MAGIC <li><strong>Recall</strong> — Of everything that was actually positive, what fraction did I catch?</li>
# MAGIC <li><strong>F1 Score</strong> — Harmonic mean of precision and recall; useful as a single number when you care about both.</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,Cell 14
# MAGIC %md-sandbox
# MAGIC ### C4. Log Loss
# MAGIC
# MAGIC Log loss — also called cross-entropy — measures how well your model's predicted probabilities match the true labels. 
# MAGIC
# MAGIC
# MAGIC
# MAGIC <svg viewBox="0 0 500 250" xmlns="http://www.w3.org/2000/svg">
# MAGIC   <rect width="400" height="250" fill="white"/>
# MAGIC   <!-- Title -->
# MAGIC   <text x="200" y="18" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">Log Loss — Penalizes Confident Wrong Predictions</text>
# MAGIC   <!-- Axes -->
# MAGIC   <line x1="55" y1="210" x2="375" y2="210" stroke="#ddd" stroke-width="1"/>
# MAGIC   <line x1="55" y1="30" x2="55" y2="210" stroke="#ddd" stroke-width="1"/>
# MAGIC   <!-- Y gridlines -->
# MAGIC   <line x1="55" y1="170" x2="375" y2="170" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="55" y1="130" x2="375" y2="130" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="55" y1="90" x2="375" y2="90" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="55" y1="50" x2="375" y2="50" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <!-- X gridlines -->
# MAGIC   <line x1="135" y1="30" x2="135" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="215" y1="30" x2="215" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="295" y1="30" x2="295" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="375" y1="30" x2="375" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <!-- Y-axis labels (loss 0 to 4.5) -->
# MAGIC   <text x="48" y="214" text-anchor="end" font-size="8" fill="#555">0</text>
# MAGIC   <text x="48" y="174" text-anchor="end" font-size="8" fill="#555">1</text>
# MAGIC   <text x="48" y="134" text-anchor="end" font-size="8" fill="#555">2</text>
# MAGIC   <text x="48" y="94" text-anchor="end" font-size="8" fill="#555">3</text>
# MAGIC   <text x="48" y="54" text-anchor="end" font-size="8" fill="#555">4</text>
# MAGIC   <!-- X-axis labels (probability 0 to 1) -->
# MAGIC   <text x="55" y="224" text-anchor="middle" font-size="8" fill="#555">0</text>
# MAGIC   <text x="135" y="224" text-anchor="middle" font-size="8" fill="#555">0.25</text>
# MAGIC   <text x="215" y="224" text-anchor="middle" font-size="8" fill="#555">0.5</text>
# MAGIC   <text x="295" y="224" text-anchor="middle" font-size="8" fill="#555">0.75</text>
# MAGIC   <text x="375" y="224" text-anchor="middle" font-size="8" fill="#555">1.0</text>
# MAGIC   <!-- Axis titles -->
# MAGIC   <text x="215" y="240" text-anchor="middle" font-size="9" fill="#555">Predicted Probability</text>
# MAGIC   <text x="15" y="120" text-anchor="middle" font-size="9" fill="#555" transform="rotate(-90,15,120)">Log Loss</text>
# MAGIC   <!-- Decision Boundary dashed line at p=0.5 -->
# MAGIC   <line x1="215" y1="30" x2="215" y2="210" stroke="#9e9e9e" stroke-width="1.5" stroke-dasharray="6,4"/>
# MAGIC   <!-- Decision Boundary label -->
# MAGIC   <text x="215" y="27" font-size="7.5" font-weight="bold" fill="#1B3139" text-anchor="middle">Decision Boundary</text>
# MAGIC   <!-- Blue curve: y=1, loss = -log(p) -->
# MAGIC   <polyline fill="none" stroke="#1976D2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
# MAGIC     points="61,54 71,90 81,109 87,118 103,134 119,146 135,154 151,162 167,168 183,173 199,178 215,182 231,186 247,190 263,193 279,196 295,198 311,201 327,204 343,206 359,208 369,209"/>
# MAGIC   <!-- Red curve: y=0, loss = -log(1-p) -->
# MAGIC   <polyline fill="none" stroke="#FF3621" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
# MAGIC     points="61,209 71,208 87,206 103,204 119,201 135,198 151,196 167,193 183,190 199,186 215,182 231,178 247,173 263,168 279,162 295,154 311,146 327,134 343,118 349,109 359,90 369,54"/>
# MAGIC   <!-- Legend -->
# MAGIC   <rect x="255" y="32" width="115" height="32" fill="white" stroke="#ddd" stroke-width="0.5" rx="3"/>
# MAGIC   <line x1="262" y1="43" x2="282" y2="43" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="286" y="46" font-size="8" fill="#333">y = 1: −log(p)</text>
# MAGIC   <line x1="262" y1="57" x2="282" y2="57" stroke="#FF3621" stroke-width="2"/>
# MAGIC   <text x="286" y="60" font-size="8" fill="#333">y = 0: −log(1−p)</text>
# MAGIC </svg>
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 13px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>from sklearn.metrics import log_loss</code>
# MAGIC <code>ll_value = log_loss(y_true, y_pred_proba)</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC What does log loss measure and how is it calculated?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">Unlike accuracy, log loss considers how confident the predictions are: being 51% confident in the right answer scores worse than being 99% confident. Use log loss when you care about probability calibration, not just final classifications.</p>
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li><strong>Penalizes confident but incorrect predictions heavily</strong> — lower values = better calibration</li>
# MAGIC <li><strong>Formula:</strong>
# MAGIC <ul>
# MAGIC   <li><span style="font-family: 'Times New Roman', serif; font-size: 20px; font-style: italic;">Log Loss = &minus;(1/N) &sum; [yᵢ &middot; log(pᵢ) + (1 &minus; yᵢ) &middot; log(1 &minus; pᵢ)]</span></li>
# MAGIC </ul>
# MAGIC </li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,Cell 15
# MAGIC %md-sandbox
# MAGIC ### C5. ROC/AUC
# MAGIC
# MAGIC ROC-AUC measures how well your model separates the two classes across every possible threshold. 
# MAGIC
# MAGIC
# MAGIC
# MAGIC <svg viewBox="0 0 500 250" xmlns="http://www.w3.org/2000/svg">
# MAGIC   <rect width="400" height="250" fill="white"/>
# MAGIC   <!-- Title -->
# MAGIC   <text x="200" y="18" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">ROC Curve</text>
# MAGIC   <!-- Axes -->
# MAGIC   <line x1="55" y1="210" x2="375" y2="210" stroke="#ddd" stroke-width="1"/>
# MAGIC   <line x1="55" y1="30" x2="55" y2="210" stroke="#ddd" stroke-width="1"/>
# MAGIC   <!-- Y gridlines -->
# MAGIC   <line x1="55" y1="170" x2="375" y2="170" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="55" y1="130" x2="375" y2="130" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="55" y1="90" x2="375" y2="90" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="55" y1="50" x2="375" y2="50" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <!-- X gridlines -->
# MAGIC   <line x1="135" y1="30" x2="135" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="215" y1="30" x2="215" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="295" y1="30" x2="295" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="375" y1="30" x2="375" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <!-- Y-axis labels (TPR 0 to 1) -->
# MAGIC   <text x="48" y="214" text-anchor="end" font-size="8" fill="#555">0</text>
# MAGIC   <text x="48" y="169" text-anchor="end" font-size="8" fill="#555">0.25</text>
# MAGIC   <text x="48" y="124" text-anchor="end" font-size="8" fill="#555">0.5</text>
# MAGIC   <text x="48" y="79" text-anchor="end" font-size="8" fill="#555">0.75</text>
# MAGIC   <text x="48" y="34" text-anchor="end" font-size="8" fill="#555">1.0</text>
# MAGIC   <!-- X-axis labels (FPR 0 to 1) -->
# MAGIC   <text x="55" y="224" text-anchor="middle" font-size="8" fill="#555">0</text>
# MAGIC   <text x="135" y="224" text-anchor="middle" font-size="8" fill="#555">0.25</text>
# MAGIC   <text x="215" y="224" text-anchor="middle" font-size="8" fill="#555">0.5</text>
# MAGIC   <text x="295" y="224" text-anchor="middle" font-size="8" fill="#555">0.75</text>
# MAGIC   <text x="375" y="224" text-anchor="middle" font-size="8" fill="#555">1.0</text>
# MAGIC   <!-- Axis titles -->
# MAGIC   <text x="215" y="240" text-anchor="middle" font-size="9" fill="#555">False Positive Rate</text>
# MAGIC   <text x="15" y="120" text-anchor="middle" font-size="9" fill="#555" transform="rotate(-90,15,120)">True Positive Rate</text>
# MAGIC   <!-- AUC shaded area -->
# MAGIC   <polygon fill="#1976D2" fill-opacity="0.15"
# MAGIC     points="55,210 71,138 87,102 103,84 119,75 135,66 151,61 167,55 183,52 215,46 247,41 279,37 311,35 343,34 375,30 375,210"/>
# MAGIC   <!-- Random guess diagonal -->
# MAGIC   <line x1="55" y1="210" x2="375" y2="30" stroke="#9e9e9e" stroke-width="1.5" stroke-dasharray="6,4"/>
# MAGIC   <!-- ROC curve -->
# MAGIC   <polyline fill="none" stroke="#1976D2" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"
# MAGIC     points="55,210 71,138 87,102 103,84 119,75 135,66 151,61 167,55 183,52 215,46 247,41 279,37 311,35 343,34 375,30"/>
# MAGIC   <!-- Legend -->
# MAGIC   <rect x="255" y="160" width="115" height="42" fill="white" stroke="#ddd" stroke-width="0.5" rx="3"/>
# MAGIC   <line x1="262" y1="173" x2="282" y2="173" stroke="#1976D2" stroke-width="2.5"/>
# MAGIC   <text x="286" y="176" font-size="8" fill="#333">ROC (AUC = 0.85)</text>
# MAGIC   <line x1="262" y1="191" x2="282" y2="191" stroke="#9e9e9e" stroke-width="1.5" stroke-dasharray="4,3"/>
# MAGIC   <text x="286" y="194" font-size="8" fill="#333">Random Guess</text>
# MAGIC </svg>
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 13px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>from sklearn.metrics import roc_auc_score</code>
# MAGIC <code>auc_score = roc_auc_score(y_true, y_pred_proba)</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 16px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC What does ROC-AUC measure and how is it interpreted?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">The ROC curve plots true positive rate against false positive rate at each threshold, and AUC is the area under that curve — 0.5 is random, 1.0 is perfect. It's threshold-independent, which makes it great for comparing models without committing to a specific decision boundary.</p>
# MAGIC
# MAGIC <ul style="margin: 12px 0; padding-left: 24px;">
# MAGIC   <li><strong>AUC = 1.0</strong> — perfect classifier</li>
# MAGIC   <li><strong>AUC = 0.5</strong> — random guessing (the diagonal)</li>
# MAGIC   <li><strong>Threshold-independent</strong> — compare models without picking a specific cutoff</li>
# MAGIC </ul>
# MAGIC
# MAGIC </div>
# MAGIC </details>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Clustering Metrics

# COMMAND ----------

# DBTITLE 1,Cell 17
# MAGIC %md-sandbox
# MAGIC ### D1. Silhouette Score
# MAGIC
# MAGIC For unsupervised clustering you don't have labels, so you can't use accuracy or AUC. The most common metric is the **silhouette score** — for each point, how close it is to its own cluster versus the next-nearest one. It ranges from −1 to 1; higher is better. The visual below contrasts a low silhouette score (clusters bleed into each other) with a high one (clusters are well-separated).
# MAGIC
# MAGIC <br>
# MAGIC <div class="cw">
# MAGIC <style>
# MAGIC .cw { font-family: sans-serif; max-width: 1100px; margin: 0 auto; color: #0b2026; }
# MAGIC .cw * { box-sizing: border-box; }
# MAGIC .ds-row { display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; }
# MAGIC .ds-row > * { flex: 1; min-width: 240px; }
# MAGIC .ds-headcard { background: #F9F7F4; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(27,49,57,0.06); }
# MAGIC .blue{--accent:#4299E0;} .green{--accent:#00A972;}
# MAGIC .ds-headband { background: var(--accent); color: #fff; font-size: 16pt; font-weight: 700; text-align: center; }
# MAGIC .ds-headbody { padding: 18px 20px; font-size: 14pt; color: #0b2026; line-height: 1.55; text-align: center;}
# MAGIC .tc { text-align: center; }
# MAGIC </style>
# MAGIC
# MAGIC <div class="ds-row">
# MAGIC   <div class="ds-headcard blue">
# MAGIC     <div class="ds-headband">High Silhouette</div>
# MAGIC     <div class="ds-headbody">
# MAGIC       Cluster A and B
# MAGIC       <div class="tc" style="margin-top:18px;">
# MAGIC         <svg width="100%" viewBox="0 0 420 200" role="img" style="font-family: sans-serif; max-width:350px;">
# MAGIC           <title>High Silhouette Score (~0.85)</title>
# MAGIC           <rect x="10" y="10" width="400" height="180" rx="10" fill="#E8F5E9" stroke="#388E3C" stroke-width="2"/>
# MAGIC           <text x="210" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#2E7D32">Score (~0.85)</text>
# MAGIC           <text x="210" y="58" text-anchor="middle" font-size="12" fill="#1B3139">Clear separation between clusters</text>
# MAGIC           <!-- Cluster A (left, high) -->
# MAGIC           <circle cx="110" cy="120" r="8" fill="#1976D2" opacity="0.7"/>
# MAGIC           <circle cx="130" cy="135" r="8" fill="#1976D2" opacity="0.7"/>
# MAGIC           <circle cx="95" cy="140" r="8" fill="#1976D2" opacity="0.7"/>
# MAGIC           <circle cx="120" cy="150" r="8" fill="#1976D2" opacity="0.7"/>
# MAGIC           <circle cx="105" cy="160" r="8" fill="#1976D2" opacity="0.7"/>
# MAGIC           <!-- Cluster B (right, high) -->
# MAGIC           <circle cx="290" cy="110" r="8" fill="#F57C00" opacity="0.7"/>
# MAGIC           <circle cx="310" cy="125" r="8" fill="#F57C00" opacity="0.7"/>
# MAGIC           <circle cx="275" cy="135" r="8" fill="#F57C00" opacity="0.7"/>
# MAGIC           <circle cx="300" cy="145" r="8" fill="#F57C00" opacity="0.7"/>
# MAGIC           <circle cx="320" cy="140" r="8" fill="#F57C00" opacity="0.7"/>
# MAGIC         </svg>
# MAGIC       </div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC   <div class="ds-headcard green">
# MAGIC     <div class="ds-headband">Low Silhouette</div>
# MAGIC     <div class="ds-headbody">
# MAGIC       Overlapping clusters
# MAGIC       <div class="tc" style="margin-top:18px;">
# MAGIC         <svg width="100%" viewBox="0 0 420 200" role="img" style="font-family: sans-serif; max-width:350px;">
# MAGIC           <title>Low Silhouette Score (~0.25)</title>
# MAGIC           <rect x="10" y="10" width="400" height="180" rx="10" fill="#FFCDD2" stroke="#D32F2F" stroke-width="2"/>
# MAGIC           <text x="210" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#C62828">Score (~0.25)</text>
# MAGIC           <text x="210" y="58" text-anchor="middle" font-size="12" fill="#1B3139">Unclear separation — clusters overlap</text>
# MAGIC           <!-- Overlapping clusters -->
# MAGIC           <circle cx="170" cy="120" r="8" fill="#1976D2" opacity="0.7"/>
# MAGIC           <circle cx="190" cy="130" r="8" fill="#F57C00" opacity="0.7"/>
# MAGIC           <circle cx="210" cy="115" r="8" fill="#1976D2" opacity="0.7"/>
# MAGIC           <circle cx="230" cy="135" r="8" fill="#F57C00" opacity="0.7"/>
# MAGIC           <circle cx="200" cy="145" r="8" fill="#1976D2" opacity="0.7"/>
# MAGIC           <circle cx="220" cy="150" r="8" fill="#F57C00" opacity="0.7"/>
# MAGIC           <circle cx="180" cy="155" r="8" fill="#1976D2" opacity="0.7"/>
# MAGIC           <circle cx="240" cy="125" r="8" fill="#F57C00" opacity="0.7"/>
# MAGIC           <circle cx="195" cy="110" r="8" fill="#F57C00" opacity="0.7"/>
# MAGIC           <circle cx="225" cy="145" r="8" fill="#1976D2" opacity="0.7"/>
# MAGIC         </svg>
# MAGIC       </div>
# MAGIC     </div>
# MAGIC   </div>
# MAGIC </div>
# MAGIC </div>
# MAGIC
# MAGIC </br>
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 13px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>from sklearn.metrics import silhouette_score</code>
# MAGIC <code>from sklearn.cluster import KMeans</code>
# MAGIC </br>
# MAGIC <code>kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)</code>
# MAGIC <code>labels = kmeans.fit_predict(X)</code>
# MAGIC <code>s_score = silhouette_score(X, labels)</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cell 18
# MAGIC %md-sandbox
# MAGIC ### D2. The Elbow Method
# MAGIC
# MAGIC K-Means is the classic clustering algorithm. You pick K, the number of clusters, and the algorithm iteratively assigns points to the nearest cluster centroid and then recomputes centroids until they stop moving. Simple, fast, and surprisingly effective — but you have to choose K, and the algorithm assumes clusters are roughly spherical and similar in size. Those assumptions don't always hold, which is why alternatives such as DBSCAN or Gaussian mixtures — which relax them — exist.
# MAGIC
# MAGIC
# MAGIC
# MAGIC <svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
# MAGIC   <rect width="400" height="250" fill="white"/>
# MAGIC   <!-- Title -->
# MAGIC   <text x="200" y="18" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">Elbow Method — Optimal Number of Clusters</text>
# MAGIC   <!-- Axes -->
# MAGIC   <line x1="55" y1="210" x2="375" y2="210" stroke="#ddd" stroke-width="1"/>
# MAGIC   <line x1="55" y1="30" x2="55" y2="210" stroke="#ddd" stroke-width="1"/>
# MAGIC   <!-- Y gridlines -->
# MAGIC   <line x1="55" y1="170" x2="375" y2="170" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="55" y1="130" x2="375" y2="130" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="55" y1="90" x2="375" y2="90" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="55" y1="50" x2="375" y2="50" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <!-- X gridlines -->
# MAGIC   <line x1="119" y1="30" x2="119" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="183" y1="30" x2="183" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="247" y1="30" x2="247" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="311" y1="30" x2="311" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <line x1="375" y1="30" x2="375" y2="210" stroke="#eee" stroke-width="0.5"/>
# MAGIC   <!-- Y-axis labels -->
# MAGIC   <text x="48" y="214" text-anchor="end" font-size="8" fill="#555">0</text>
# MAGIC   <text x="48" y="174" text-anchor="end" font-size="8" fill="#555">200</text>
# MAGIC   <text x="48" y="134" text-anchor="end" font-size="8" fill="#555">400</text>
# MAGIC   <text x="48" y="94" text-anchor="end" font-size="8" fill="#555">600</text>
# MAGIC   <text x="48" y="54" text-anchor="end" font-size="8" fill="#555">800</text>
# MAGIC   <!-- X-axis labels -->
# MAGIC   <text x="55" y="224" text-anchor="middle" font-size="8" fill="#555">1</text>
# MAGIC   <text x="119" y="224" text-anchor="middle" font-size="8" fill="#555">2</text>
# MAGIC   <text x="183" y="224" text-anchor="middle" font-size="8" fill="#555">3</text>
# MAGIC   <text x="247" y="224" text-anchor="middle" font-size="8" fill="#555">4</text>
# MAGIC   <text x="311" y="224" text-anchor="middle" font-size="8" fill="#555">5</text>
# MAGIC   <text x="375" y="224" text-anchor="middle" font-size="8" fill="#555">6</text>
# MAGIC   <!-- Axis titles -->
# MAGIC   <text x="215" y="240" text-anchor="middle" font-size="9" fill="#555">Number of Clusters (k)</text>
# MAGIC   <text x="15" y="120" text-anchor="middle" font-size="9" fill="#555" transform="rotate(-90,15,120)">Inertia</text>
# MAGIC   <!-- Elbow curve -->
# MAGIC   <polyline fill="none" stroke="#1976D2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
# MAGIC     points="55,42 119,95 183,148 247,172 311,188 375,195"/>
# MAGIC   <!-- Data points -->
# MAGIC   <circle cx="55" cy="42" r="4" fill="#1976D2"/>
# MAGIC   <circle cx="119" cy="95" r="4" fill="#1976D2"/>
# MAGIC   <circle cx="183" cy="148" r="4" fill="#F57C00"/>
# MAGIC   <circle cx="247" cy="172" r="4" fill="#1976D2"/>
# MAGIC   <circle cx="311" cy="188" r="4" fill="#1976D2"/>
# MAGIC   <circle cx="375" cy="195" r="4" fill="#1976D2"/>
# MAGIC   <!-- Elbow point annotation -->
# MAGIC   <line x1="183" y1="148" x2="183" y2="80" stroke="#F57C00" stroke-width="1" stroke-dasharray="4,3"/>
# MAGIC   <rect x="140" y="62" width="86" height="16" fill="#FFF3E0" stroke="#F57C00" stroke-width="0.8" rx="3" opacity="0.9"/>
# MAGIC   <text x="183" y="73" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#E65100">Elbow Point (k=3)</text>
# MAGIC </svg>
# MAGIC
# MAGIC <div style="background: #FFF3E0; border-left: 4px solid #F57C00; border-radius: 6px; padding: 16px; margin: 12px 0; overflow-x: auto;">
# MAGIC <pre style="margin: 0; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 13px; color: #0a0a0a; white-space: pre-wrap;">
# MAGIC <code>from sklearn.cluster import KMeans</code>
# MAGIC <code>from kneed import KneeLocator</code>
# MAGIC </br>
# MAGIC <code>k_values = range(1, 7)</code>
# MAGIC <code>inertia_values = [
# MAGIC     KMeans(n_clusters=k, random_state=42, n_init=10).fit(X).inertia_
# MAGIC     for k in k_values
# MAGIC ]</code>
# MAGIC </br>
# MAGIC <code>knee_locator = KneeLocator(k_values, inertia_values, curve="convex", direction="decreasing")</code>
# MAGIC <code>optimal_k = knee_locator.elbow</code>
# MAGIC </pre>
# MAGIC </div>
# MAGIC
# MAGIC <details style="margin: 8px 0;">
# MAGIC <summary style="background: linear-gradient(135deg, #1B5162, #4299E0); color: white; padding: 12px 18px; cursor: pointer; font-weight: 600; font-size: 13pt; border-radius: 8px; user-select: none;">
# MAGIC How do you pick K?
# MAGIC </summary>
# MAGIC <div style="border: 2px solid #1B5162; border-top: none; border-radius: 0 0 8px 8px; padding: 16px 20px; background: #F9F7F4; font-size: 13pt; line-height: 1.7; color: #333;">
# MAGIC
# MAGIC <p style="margin-top: 10px;">You don't know in advance — you try several values and look for the elbow in the inertia curve.</p>
# MAGIC <ol style="margin: 12px 0; padding-left: 24px;">
# MAGIC <li>The code snippet sweeps <code>k_values = range(1, 7)</code> and fits a model for each, capturing the metric.</li>
# MAGIC <li>Plot the result and you'll typically see diminishing returns past some point — that's your elbow.</li>
# MAGIC <li>There's no perfectly objective answer; domain knowledge usually plays a role.</li>
# MAGIC </ol>
# MAGIC
# MAGIC </div>
# MAGIC </details>

# COMMAND ----------

# DBTITLE 1,Cell 18
# MAGIC %md
# MAGIC ## E. Conclusion
# MAGIC
# MAGIC In this lecture, you covered the end-to-end model development workflow and how to measure model quality across ML paradigms:
# MAGIC
# MAGIC 1. **Purpose of Evaluation Metrics & the Model Development Workflow** — Metrics quantify performance, enable comparison, guide tuning, and provide objective model selection. The workflow runs from data preparation through split strategy, training (tracked with MLflow), hyperparameter tuning (Optuna), and final evaluation on the held-out test set. Training data directly updates parameters; validation data indirectly influences them; test data has no influence — it only measures generalizability.
# MAGIC 2. **Regression Metrics** — R² measures explained variance; MAE, MSE, and RMSE quantify prediction error at different scales. Use `root_mean_squared_error` for interpretable error in original units.
# MAGIC 3. **Classification Metrics** — The confusion matrix is the foundation — from its four cells you derive accuracy, precision, recall, and F1. Choose based on business cost: precision when false positives are expensive, recall when false negatives are. Log loss measures probability calibration (confidence matters, not just correctness). ROC/AUC provides threshold-independent model comparison.
# MAGIC 4. **Clustering Metrics** — Without labels, use the silhouette score to measure cluster separation. K-Means is the classic algorithm, but you must choose K — the elbow method helps by plotting inertia against cluster count and finding diminishing returns. Domain knowledge plays a role; alternatives like DBSCAN relax K-Means' spherical-cluster assumption.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
