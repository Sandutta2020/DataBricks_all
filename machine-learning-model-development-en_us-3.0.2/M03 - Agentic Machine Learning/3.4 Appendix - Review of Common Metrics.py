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

# DBTITLE 1,Untitled
# MAGIC %md-sandbox
# MAGIC # Appendix — Review of Common Metrics
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This appendix provides a visual review of key evaluation metrics used across supervised learning. Each metric is paired with an annotated graph and formula to build intuition.
# MAGIC
# MAGIC | Section | Topics |
# MAGIC | --- | --- |
# MAGIC | **A. Regression Metrics** | Residuals, Observed vs. Predicted, SS_tot, R², MAE, MSE, RMSE |
# MAGIC | **B. Bias-Variance Tradeoff** | Underfitting vs. Overfitting, mitigation strategies |
# MAGIC | **C. Classification** | Confusion Matrix, Accuracy, Precision, Recall, F1, Log Loss |

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Review of Regression Metrics

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### A1. Regression Metrics
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
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Mean Absolute Error (MAE)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Computes the average of the absolute difference between actual and predicted values. Less sensitive to outliers.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Lower is better</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Mean Squared Error (MSE)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Penalizes larger errors more than MAE due to squaring. Common for optimization.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Lower is better</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Root Mean Squared Error (RMSE)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Similar to MSE but takes the square root, making it more interpretable in the original units.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Lower is better</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">R² (Coefficient of Determination)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Measures the proportion of variance explained by the model. At most 1 (a perfect fit); 0 means no better than predicting the mean, and it can be negative when the model is worse than the mean.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Higher is better</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# DBTITLE 1,Cell 5
# MAGIC %md-sandbox
# MAGIC ### A2. Observed vs. Predicted
# MAGIC
# MAGIC The fundamental concept behind regression metrics is the **residual** — the distance between each observed value and the model's predicted value.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; flex-direction: row; gap: 20px; align-items: flex-start; justify-content: center;">
# MAGIC
# MAGIC <!-- SVG 1: Good Fit -->
# MAGIC <svg width="420" viewBox="0 0 400 260" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Good Fit — Small Residuals</title>
# MAGIC   <rect x="10" y="10" width="380" height="240" rx="12" fill="#FFFFFF" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="200" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Good Fit — Small Residuals</text>
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
# MAGIC   <text x="210" y="232" text-anchor="middle" font-size="13" fill="#1B3139">Feature Variable</text>
# MAGIC   <text x="30" y="130" text-anchor="middle" font-size="13" fill="#1B3139" transform="rotate(-90 30 130)">Target Variable</text>
# MAGIC
# MAGIC   <!-- Predicted line (dashed red) - shorter -->
# MAGIC   <line x1="75" y1="190" x2="330" y2="70" stroke="#D32F2F" stroke-width="2.5" stroke-dasharray="6,3"/>
# MAGIC
# MAGIC   <!-- Observed points (close to line) -->
# MAGIC   <circle cx="90" cy="183" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="130" cy="168" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="170" cy="150" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="210" cy="132" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="250" cy="112" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="290" cy="90" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="320" cy="75" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC
# MAGIC   <!-- Residual lines (small) -->
# MAGIC   <line x1="90" y1="183" x2="90" y2="186" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="130" y1="168" x2="130" y2="162" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="170" y1="150" x2="170" y2="145" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="210" y1="132" x2="210" y2="127" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="250" y1="112" x2="250" y2="108" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="290" y1="90" x2="290" y2="86" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="320" y1="75" x2="320" y2="72" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC
# MAGIC   <!-- Legend (stacked, just above X-axis) -->
# MAGIC   <g>
# MAGIC     <circle cx="310" cy="192" r="4" fill="#1976D2"/>
# MAGIC     <text x="320" y="196" font-size="11" fill="#1B3139">Observed</text>
# MAGIC     <line x1="300" y1="205" x2="318" y2="205" stroke="#D32F2F" stroke-width="2" stroke-dasharray="4,2"/>
# MAGIC     <text x="320" y="209" font-size="11" fill="#1B3139">Predicted</text>
# MAGIC   </g>
# MAGIC </svg>
# MAGIC
# MAGIC <!-- SVG 2: Poor Fit -->
# MAGIC <svg width="420" viewBox="0 0 400 260" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Poor Fit — Large Residuals</title>
# MAGIC   <rect x="10" y="10" width="380" height="240" rx="12" fill="#FFFFFF" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="200" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Poor Fit — Large Residuals</text>
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
# MAGIC   <text x="210" y="232" text-anchor="middle" font-size="13" fill="#1B3139">Feature Variable</text>
# MAGIC   <text x="30" y="130" text-anchor="middle" font-size="13" fill="#1B3139" transform="rotate(-90 30 130)">Target Variable</text>
# MAGIC
# MAGIC   <!-- Predicted line (dashed red) - shorter, poor fit -->
# MAGIC   <line x1="75" y1="190" x2="330" y2="70" stroke="#D32F2F" stroke-width="2.5" stroke-dasharray="6,3"/>
# MAGIC
# MAGIC   <!-- Observed points (scattered far from line) -->
# MAGIC   <circle cx="90" cy="145" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="130" cy="195" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="170" cy="175" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="210" cy="85" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="250" cy="140" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="290" cy="60" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="320" cy="110" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC
# MAGIC   <!-- Residual lines (large) -->
# MAGIC   <line x1="90" y1="145" x2="90" y2="186" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="130" y1="195" x2="130" y2="162" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="170" y1="175" x2="170" y2="145" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="210" y1="85" x2="210" y2="127" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="250" y1="140" x2="250" y2="108" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="290" y1="60" x2="290" y2="86" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="320" y1="110" x2="320" y2="72" stroke="#618794" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC
# MAGIC   <!-- Legend (stacked, just above X-axis) -->
# MAGIC   <g>
# MAGIC     <circle cx="310" cy="192" r="4" fill="#1976D2"/>
# MAGIC     <text x="320" y="196" font-size="11" fill="#1B3139">Observed</text>
# MAGIC     <line x1="300" y1="205" x2="318" y2="205" stroke="#D32F2F" stroke-width="2" stroke-dasharray="4,2"/>
# MAGIC     <text x="320" y="209" font-size="11" fill="#1B3139">Predicted</text>
# MAGIC   </g>
# MAGIC </svg>
# MAGIC
# MAGIC </div>
# MAGIC
# MAGIC **Residual:** The distance between each observed point and the predicted line. All regression error metrics are based on summarizing these residuals.

# COMMAND ----------

# DBTITLE 1,Cell 8
# MAGIC %md-sandbox
# MAGIC ### A3. Mean Absolute Error (MAE)
# MAGIC
# MAGIC MAE computes the average of the absolute differences between observed and predicted values. It is less sensitive to outliers than squared-error metrics because it does not amplify large residuals.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; justify-content: center;">
# MAGIC <svg width="600" viewBox="0 0 440 300" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Mean Absolute Error</title>
# MAGIC   <rect x="10" y="10" width="400" height="260" rx="12" fill="#FFFFFF" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="210" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Mean Absolute Error (MAE)</text>
# MAGIC
# MAGIC   <!-- Grid lines -->
# MAGIC   <line x1="60" y1="60" x2="60" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="120" y1="60" x2="120" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="180" y1="60" x2="180" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="240" y1="60" x2="240" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="300" y1="60" x2="300" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="360" y1="60" x2="360" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="90" x2="380" y2="90" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="130" x2="380" y2="130" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="170" x2="380" y2="170" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="220" x2="380" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC
# MAGIC   <!-- Axes -->
# MAGIC   <line x1="50" y1="240" x2="380" y2="240" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <line x1="50" y1="50" x2="50" y2="240" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <text x="215" y="262" text-anchor="middle" font-size="13" fill="#1B3139">Feature Variable</text>
# MAGIC   <text x="30" y="145" text-anchor="middle" font-size="13" fill="#1B3139" transform="rotate(-90 30 145)">Target Variable</text>
# MAGIC
# MAGIC   <!-- Predicted line (dashed red) -->
# MAGIC   <line x1="70" y1="205" x2="360" y2="75" stroke="#D32F2F" stroke-width="2.5" stroke-dasharray="6,3"/>
# MAGIC
# MAGIC   <!-- Observed points (scattered with visible residuals) -->
# MAGIC   <circle cx="90" cy="175" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="130" cy="200" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="175" cy="130" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="215" cy="165" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="260" cy="90" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="305" cy="125" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="345" cy="65" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC
# MAGIC   <!-- Residual lines (from observed point to predicted line) -->
# MAGIC   <!-- Predicted y at each x: 90→196, 130→178, 175→158, 215→140, 260→120, 305→100, 345→82 -->
# MAGIC   <line x1="90" y1="175" x2="90" y2="196" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="130" y1="200" x2="130" y2="178" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="175" y1="130" x2="175" y2="158" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="215" y1="165" x2="215" y2="140" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="260" y1="90" x2="260" y2="120" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="305" y1="125" x2="305" y2="100" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="345" y1="65" x2="345" y2="82" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC
# MAGIC   <!-- Legend (stacked, just above X-axis) -->
# MAGIC   <g>
# MAGIC     <circle cx="80" cy="225" r="3.5" fill="#1976D2"/>
# MAGIC     <text x="88" y="228" font-size="10" fill="#1B3139">Observed</text>
# MAGIC     <line x1="138" y1="225" x2="155" y2="225" stroke="#D32F2F" stroke-width="2" stroke-dasharray="4,2"/>
# MAGIC     <text x="160" y="228" font-size="10" fill="#1B3139">Predicted</text>
# MAGIC   </g>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="text-align: center; margin-bottom: 12px;">
# MAGIC   <span style="font-size: 1.25em; font-family: 'Latin Modern Math', 'STIX', 'Times New Roman', serif;">
# MAGIC     \( MAE = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i| \)
# MAGIC   </span>
# MAGIC   <br/>
# MAGIC   <p>The <strong>residual</strong> \( (y_i - \hat{y}_i) \) is the distance between each observed point and the predicted line.</p>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cell 9
# MAGIC %md-sandbox
# MAGIC ### A4. Mean Squared Error (MSE)
# MAGIC
# MAGIC Penalizes larger errors more than MAE due to squaring. Common for optimization because it is differentiable everywhere.
# MAGIC
# MAGIC <div style="max-width: 600px; margin: 0 auto; display: flex; justify-content: center;">
# MAGIC <svg width="600" viewBox="0 0 440 300" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Mean Squared Error</title>
# MAGIC   <rect x="10" y="10" width="400" height="260" rx="12" fill="#FFFFFF" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="210" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Mean Squared Error (MSE)</text>
# MAGIC
# MAGIC   <!-- Grid lines -->
# MAGIC   <line x1="60" y1="60" x2="60" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="120" y1="60" x2="120" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="180" y1="60" x2="180" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="240" y1="60" x2="240" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="300" y1="60" x2="300" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="360" y1="60" x2="360" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="90" x2="380" y2="90" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="130" x2="380" y2="130" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="170" x2="380" y2="170" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="220" x2="380" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC
# MAGIC   <!-- Axes -->
# MAGIC   <line x1="50" y1="240" x2="380" y2="240" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <line x1="50" y1="50" x2="50" y2="240" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <text x="215" y="262" text-anchor="middle" font-size="13" fill="#1B3139">Feature Variable</text>
# MAGIC   <text x="30" y="145" text-anchor="middle" font-size="13" fill="#1B3139" transform="rotate(-90 30 145)">Target Variable</text>
# MAGIC
# MAGIC   <!-- Predicted line (dashed red) -->
# MAGIC   <line x1="70" y1="205" x2="360" y2="75" stroke="#D32F2F" stroke-width="2.5" stroke-dasharray="6,3"/>
# MAGIC
# MAGIC   <!-- Observed points -->
# MAGIC   <circle cx="90" cy="175" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="130" cy="200" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="175" cy="130" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="215" cy="165" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="260" cy="90" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="305" cy="125" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="345" cy="65" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC
# MAGIC   <!-- Residual lines (from observed to predicted) -->
# MAGIC   <!-- Predicted y at each x: 90→196, 130→178, 175→158, 215→140, 260→120, 305→100, 345→82 -->
# MAGIC   <line x1="90" y1="175" x2="90" y2="196" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="130" y1="200" x2="130" y2="178" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="175" y1="130" x2="175" y2="158" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="215" y1="165" x2="215" y2="140" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="260" y1="90" x2="260" y2="120" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="305" y1="125" x2="305" y2="100" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="345" y1="65" x2="345" y2="82" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC
# MAGIC   <!-- Squared residual boxes (visual representation of squaring) -->
# MAGIC   <rect x="90" y="175" width="21" height="21" fill="#618794" opacity="0.35"/>
# MAGIC   <rect x="108" y="178" width="22" height="22" fill="#618794" opacity="0.35"/>
# MAGIC   <rect x="175" y="130" width="28" height="28" fill="#618794" opacity="0.35"/>
# MAGIC   <rect x="215" y="140" width="25" height="25" fill="#618794" opacity="0.35"/>
# MAGIC   <rect x="260" y="90" width="30" height="30" fill="#618794" opacity="0.35"/>
# MAGIC   <rect x="305" y="100" width="25" height="25" fill="#618794" opacity="0.35"/>
# MAGIC   <rect x="345" y="65" width="17" height="17" fill="#618794" opacity="0.35"/>
# MAGIC
# MAGIC   <!-- Legend (stacked, just above X-axis) -->
# MAGIC   <g>
# MAGIC     <circle cx="80" cy="225" r="3.5" fill="#1976D2"/>
# MAGIC     <text x="88" y="228" font-size="10" fill="#1B3139">Observed</text>
# MAGIC     <line x1="138" y1="225" x2="155" y2="225" stroke="#D32F2F" stroke-width="2" stroke-dasharray="4,2"/>
# MAGIC     <text x="160" y="228" font-size="10" fill="#1B3139">Predicted</text>
# MAGIC   </g>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="text-align: center; margin-bottom: 12px;">
# MAGIC   <span style="font-size: 1.25em; font-family: 'Latin Modern Math', 'STIX', 'Times New Roman', serif;">
# MAGIC     \( MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 \)
# MAGIC   </span>
# MAGIC   <br/>
# MAGIC   <p>The <strong>squared residual</strong> \( (y_i - \hat{y}_i)^2 \) penalizes larger errors more heavily than smaller ones.</p>
# MAGIC </div>
# MAGIC
# MAGIC Because errors are squared, a single large outlier can dominate MSE. This is a feature when large errors are especially undesirable, but a drawback when outliers are noise.
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     The <span style="color:#618794;"><strong>teal shaded boxes</strong></span> in the diagram represent the squared residuals used in both MSE and R². MSE averages these squared errors to quantify prediction error in the original squared units of the target variable. R² uses the sum of squared residuals (<code>SS_res</code>) to compare model error against the total spread (<code>SS_tot</code>), producing a unitless proportion of variance explained.
# MAGIC   </div>
# MAGIC </div>

# COMMAND ----------

# DBTITLE 1,Cell 10
# MAGIC %md-sandbox
# MAGIC ### A5. Root Mean Squared Error (RMSE)
# MAGIC
# MAGIC Similar to MSE but takes the square root, making it more interpretable in the original units of the target variable.
# MAGIC
# MAGIC <div style="max-width: 600px; margin: 0 auto; display: flex; justify-content: center;">
# MAGIC <svg width="600" viewBox="0 0 440 300" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Root Mean Squared Error</title>
# MAGIC   <rect x="10" y="10" width="400" height="260" rx="12" fill="#FFFFFF" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="210" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Root Mean Squared Error (RMSE)</text>
# MAGIC
# MAGIC   <!-- Grid lines -->
# MAGIC   <line x1="60" y1="60" x2="60" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="120" y1="60" x2="120" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="180" y1="60" x2="180" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="240" y1="60" x2="240" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="300" y1="60" x2="300" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="360" y1="60" x2="360" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="90" x2="380" y2="90" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="130" x2="380" y2="130" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="170" x2="380" y2="170" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC   <line x1="50" y1="220" x2="380" y2="220" stroke="#E0E0E0" stroke-width="0.5"/>
# MAGIC
# MAGIC   <!-- Axes -->
# MAGIC   <line x1="50" y1="240" x2="380" y2="240" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <line x1="50" y1="50" x2="50" y2="240" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <text x="215" y="262" text-anchor="middle" font-size="13" fill="#1B3139">Feature Variable</text>
# MAGIC   <text x="30" y="145" text-anchor="middle" font-size="13" fill="#1B3139" transform="rotate(-90 30 145)">Target Variable</text>
# MAGIC
# MAGIC   <!-- Predicted line (dashed red) -->
# MAGIC   <line x1="70" y1="205" x2="360" y2="75" stroke="#D32F2F" stroke-width="2.5" stroke-dasharray="6,3"/>
# MAGIC
# MAGIC   <!-- Observed points -->
# MAGIC   <circle cx="90" cy="175" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="130" cy="200" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="175" cy="130" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="215" cy="165" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="260" cy="90" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="305" cy="125" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="345" cy="65" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC
# MAGIC   <!-- Residual lines (from observed to predicted) -->
# MAGIC   <!-- Predicted y at each x: 90→196, 130→178, 175→158, 215→140, 260→120, 305→100, 345→82 -->
# MAGIC   <line x1="90" y1="175" x2="90" y2="196" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="130" y1="200" x2="130" y2="178" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="175" y1="130" x2="175" y2="158" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="215" y1="165" x2="215" y2="140" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="260" y1="90" x2="260" y2="120" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="305" y1="125" x2="305" y2="100" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC   <line x1="345" y1="65" x2="345" y2="82" stroke="#618794" stroke-width="2" stroke-dasharray="3,2"/>
# MAGIC
# MAGIC   <!-- Legend (stacked, just above X-axis) -->
# MAGIC   <g>
# MAGIC     <circle cx="80" cy="225" r="3.5" fill="#1976D2"/>
# MAGIC     <text x="88" y="228" font-size="10" fill="#1B3139">Observed</text>
# MAGIC     <line x1="138" y1="225" x2="155" y2="225" stroke="#D32F2F" stroke-width="2" stroke-dasharray="4,2"/>
# MAGIC     <text x="160" y="228" font-size="10" fill="#1B3139">Predicted</text>
# MAGIC   </g>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="text-align: center; margin-bottom: 12px;">
# MAGIC   <span style="font-size: 1.25em; font-family: 'Latin Modern Math', 'STIX', 'Times New Roman', serif;">
# MAGIC     \( RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2} \)
# MAGIC   </span>
# MAGIC   <br/>
# MAGIC   <p>Same as MSE but in the <strong>original units</strong> of the target variable, making it directly interpretable.</p>
# MAGIC </div>
# MAGIC
# MAGIC RMSE is the most commonly reported regression error metric because it is in the same units as the target — if you're predicting house prices in dollars, RMSE is also in dollars.

# COMMAND ----------

# DBTITLE 1,Cell 6
# MAGIC %md-sandbox
# MAGIC ### A6. Observed vs. Target Mean
# MAGIC
# MAGIC To understand R², we also need the **total sum of squares** — the distance between each observed value and the simple mean of the target variable.
# MAGIC
# MAGIC <div style="max-width: 800px; margin: 0 auto; display: flex; justify-content: center;">
# MAGIC <svg width="600" viewBox="0 0 440 260" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Observed vs. Target Mean</title>
# MAGIC   <rect x="10" y="10" width="400" height="240" rx="12" fill="#FFFFFF" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="200" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Observed vs. Target Mean</text>
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
# MAGIC   <text x="210" y="232" text-anchor="middle" font-size="13" fill="#1B3139">Feature Variable</text>
# MAGIC   <text x="30" y="130" text-anchor="middle" font-size="13" fill="#1B3139" transform="rotate(-90 30 130)">Target Variable</text>
# MAGIC
# MAGIC   <!-- Target Mean line (solid dark red) -->
# MAGIC   <line x1="60" y1="140" x2="360" y2="140" stroke="#8B0000" stroke-width="2"/>
# MAGIC
# MAGIC   <!-- Observed points (blue circles) -->
# MAGIC   <circle cx="90" cy="170" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="140" cy="155" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="180" cy="185" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="230" cy="95" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="280" cy="120" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="330" cy="65" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC
# MAGIC   <!-- Distance lines from observed to mean -->
# MAGIC   <line x1="90" y1="170" x2="90" y2="140" stroke="#8B0000" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="140" y1="155" x2="140" y2="140" stroke="#8B0000" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="180" y1="185" x2="180" y2="140" stroke="#8B0000" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="230" y1="95" x2="230" y2="140" stroke="#8B0000" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="280" y1="120" x2="280" y2="140" stroke="#8B0000" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC   <line x1="330" y1="65" x2="330" y2="140" stroke="#8B0000" stroke-width="1.5" stroke-dasharray="3,2"/>
# MAGIC
# MAGIC   <!-- Squared difference boxes (faint) -->
# MAGIC   <rect x="84" y="140" width="12" height="30" fill="#8B0000" opacity="0.15"/>
# MAGIC   <rect x="134" y="140" width="12" height="15" fill="#8B0000" opacity="0.15"/>
# MAGIC   <rect x="174" y="140" width="12" height="45" fill="#8B0000" opacity="0.15"/>
# MAGIC   <rect x="224" y="95" width="12" height="45" fill="#8B0000" opacity="0.15"/>
# MAGIC   <rect x="274" y="120" width="12" height="20" fill="#8B0000" opacity="0.15"/>
# MAGIC   <rect x="324" y="65" width="12" height="75" fill="#8B0000" opacity="0.15"/>
# MAGIC
# MAGIC   <!-- Legend (stacked, above X-axis) -->
# MAGIC   <g>
# MAGIC     <circle cx="300" cy="190" r="4" fill="#1976D2"/>
# MAGIC     <text x="307" y="195" font-size="11" fill="#1B3139">Observed</text>
# MAGIC     <line x1="295" y1="205" x2="310" y2="205" stroke="#8B0000" stroke-width="2"/>
# MAGIC     <text x="315" y="209" font-size="11" fill="#1B3139">Mean of Target</text>
# MAGIC   </g>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC The **Total Sum of Squares** captures the total variability in the target — it's the baseline that R² measures improvement against.
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     The <span style="color:#8B0000;"><strong>red shaded regions</strong></span> in the diagram represent the squared difference between each observed value and the mean of the target variable. This is the <strong>Total Sum of Squares (SS<sub>tot</sub>)</strong>, which quantifies the total variability in the target and serves as the baseline for measuring model improvement with R².
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# DBTITLE 1,Cell 7
# MAGIC %md-sandbox
# MAGIC ### A7. R² (Coefficient of Determination)
# MAGIC
# MAGIC R² compares how much error the model makes (SS_res) against the error of simply predicting the mean (SS_tot).
# MAGIC
# MAGIC <div style="max-width: 600px; margin: 0 auto; display: flex; justify-content: center;">
# MAGIC <svg width="600" viewBox="0 0 440 300" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>R² — Comparing SS_res to SS_tot</title>
# MAGIC   <rect x="10" y="10" width="400" height="260" rx="12" fill="#FFFFFF" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="200" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">R² — Comparing Model Error to Total Spread</text>
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
# MAGIC   <line x1="50" y1="240" x2="370" y2="240" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <line x1="50" y1="50" x2="50" y2="240" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <text x="210" y="262" text-anchor="middle" font-size="13" fill="#1B3139">Feature Variable</text>
# MAGIC   <text x="30" y="145" text-anchor="middle" font-size="13" fill="#1B3139" transform="rotate(-90 30 145)">Target Variable</text>
# MAGIC
# MAGIC   <!-- Mean of Target line (solid dark red) -->
# MAGIC   <line x1="60" y1="140" x2="360" y2="140" stroke="#8B0000" stroke-width="2"/>
# MAGIC
# MAGIC   <!-- Predicted line (dashed red) - poor fit, linear -->
# MAGIC   <line x1="75" y1="190" x2="330" y2="70" stroke="#D32F2F" stroke-width="2.5" stroke-dasharray="6,3"/>
# MAGIC
# MAGIC   <!-- Observed points (blue circles - scattered, poor fit) -->
# MAGIC   <circle cx="90" cy="170" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="140" cy="185" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="180" cy="150" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="230" cy="95" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="280" cy="120" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC   <circle cx="330" cy="65" r="5" fill="#1976D2" opacity="0.8"/>
# MAGIC
# MAGIC   <!-- SS_tot: distance from observed to mean (dark red shaded boxes) -->
# MAGIC   <rect x="84" y="140" width="12" height="30" fill="#8B0000" opacity="0.15"/>
# MAGIC   <rect x="134" y="140" width="12" height="45" fill="#8B0000" opacity="0.15"/>
# MAGIC   <rect x="174" y="140" width="12" height="10" fill="#8B0000" opacity="0.15"/>
# MAGIC   <rect x="224" y="95" width="12" height="45" fill="#8B0000" opacity="0.15"/>
# MAGIC   <rect x="274" y="120" width="12" height="20" fill="#8B0000" opacity="0.15"/>
# MAGIC   <rect x="324" y="65" width="12" height="75" fill="#8B0000" opacity="0.15"/>
# MAGIC
# MAGIC   <!-- SS_res: distance from observed to predicted (teal shaded boxes) -->
# MAGIC   <!-- Predicted y at each x: 90→179, 140→158, 180→142, 230→121, 280→100, 330→80 -->
# MAGIC   <rect x="96" y="170" width="10" height="9" fill="#618794" opacity="0.35"/>
# MAGIC   <rect x="146" y="158" width="10" height="27" fill="#618794" opacity="0.35"/>
# MAGIC   <rect x="186" y="142" width="10" height="8" fill="#618794" opacity="0.35"/>
# MAGIC   <rect x="236" y="95" width="10" height="26" fill="#618794" opacity="0.35"/>
# MAGIC   <rect x="286" y="100" width="10" height="20" fill="#618794" opacity="0.35"/>
# MAGIC   <rect x="336" y="65" width="10" height="15" fill="#618794" opacity="0.35"/>
# MAGIC
# MAGIC
# MAGIC   <!-- Legend (stacked, just above X-axis) -->
# MAGIC   <g>
# MAGIC     <circle cx="80" cy="225" r="3.5" fill="#1976D2"/>
# MAGIC     <text x="85" y="228" font-size="10" fill="#1B3139">Observed</text>
# MAGIC     <line x1="135" y1="225" x2="150" y2="225" stroke="#D32F2F" stroke-width="2" stroke-dasharray="4,2"/>
# MAGIC     <text x="155" y="228" font-size="10" fill="#1B3139">Predicted</text>
# MAGIC     <line x1="210" y1="225" x2="225" y2="225" stroke="#8B0000" stroke-width="2"/>
# MAGIC     <text x="230" y="228" font-size="11" fill="#1B3139">Mean of Target</text>
# MAGIC   </g>
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <div style="text-align: center; margin-bottom: 12px;">
# MAGIC   <span style="font-size: 1.25em; font-family: 'Latin Modern Math', 'STIX', 'Times New Roman', serif;">
# MAGIC     \( R^2 = 1 - \frac{SS_{res}}{SS_{tot}} \)
# MAGIC   </span>
# MAGIC </div>
# MAGIC
# MAGIC <div style="border-left: 4px solid #1B5162; background: #F8F9FC; padding: 14px 18px; border-radius: 4px; margin: 16px 0; font-family: sans-serif;">
# MAGIC   <strong style="display:block; color:#1B5162; margin-bottom:6px; font-size:15pt;">Note</strong>
# MAGIC   <div style="color:#0b2026; font-size:12pt; line-height:1.55;">
# MAGIC     <span style="color:#8B0000;"><strong>Red shaded boxes</strong></span> represent the <strong>total spread (SS<sub>tot</sub>)</strong>: the squared distance from each observation to the mean of the target variable.<br>
# MAGIC     <span style="color:#618794;"><strong>Teal shaded boxes</strong></span> represent the <strong>model error (SS<sub>res</sub>)</strong>: the squared distance from each observation to the predicted value.<br>
# MAGIC     R² compares these two quantities to show how much variance the model explains versus simply predicting the mean. Higher R² means the model captures more of the target's variability.
# MAGIC   </div>
# MAGIC </div>
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Classification

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B1. The Confusion Matrix
# MAGIC
# MAGIC The confusion matrix is the foundation for all classification metrics. Each cell counts a kind of prediction outcome.
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
# MAGIC - **True Positive (TP)** — predicted positive, actual positive. Correctly identified.
# MAGIC - **False Negative (FN)** — predicted negative, actual positive. Missed it.
# MAGIC - **False Positive (FP)** — predicted positive, actual negative. False alarm.
# MAGIC - **True Negative (TN)** — predicted negative, actual negative. Correctly rejected.

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### B2. Classification Metrics
# MAGIC
# MAGIC Using the confusion matrix values (TP=6, FN=4, FP=2, TN=8) as an example:
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Metric</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Formula</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Example</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Accuracy</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Proportion of correctly classified instances. Can be misleading for imbalanced datasets.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">(TP+TN) / (TP+TN+FP+FN)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">(6+8)/(6+8+2+4) = <strong>7/10</strong></td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Precision</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Measures how many predicted positives are actually correct. Important when false positives are costly.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">TP / (TP+FP)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">6/(6+2) = <strong>3/4</strong></td>
# MAGIC     </tr>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">Recall (Sensitivity)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Measures how many actual positives were correctly identified. Important when false negatives are costly.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">TP / (TP+FN)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">6/(6+4) = <strong>3/5</strong></td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">F1 Score</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Harmonic mean of precision and recall. Balances both concerns in a single number.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">2 &times; (P&times;R)/(P+R)</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">2&times;(0.75&times;0.60)/(0.75+0.60) = <strong>2/3</strong></td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# DBTITLE 1,Untitled
# MAGIC %md-sandbox
# MAGIC ### B3. Log Loss (Cross-Entropy Loss)
# MAGIC
# MAGIC Penalizes confident wrong predictions heavily. Measures how well predicted probabilities match actual outcomes.
# MAGIC
# MAGIC
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; justify-content: center;">
# MAGIC <svg viewBox="0 0 500 250" xmlns="http://www.w3.org/2000/svg">
# MAGIC   <rect width="400" height="250" fill="white"/>
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
# MAGIC   <text x="215" y="240" text-anchor="middle" font-size="10" font-weight="bold fill="#555">Predicted Probability</text>
# MAGIC   <text x="15" y="120" text-anchor="middle" font-size="10" font-weight="bold fill="#555" transform="rotate(-90,15,120)">Log Loss</text>
# MAGIC   <!-- Decision Boundary dashed line at p=0.5 -->
# MAGIC   <line x1="215" y1="30" x2="215" y2="210" stroke="#9e9e9e" stroke-width="1.5" stroke-dasharray="6,4"/>
# MAGIC   <!-- Decision Boundary label -->
# MAGIC   <text x="215" y="27" font-size="8" font-weight="bold" fill="#1B3139" text-anchor="middle">Decision Boundary</text>
# MAGIC   <!-- Blue curve: y=1, loss = -log(p) -->
# MAGIC   <polyline fill="none" stroke="#1976D2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
# MAGIC     points="61,54 71,90 81,109 87,118 103,134 119,146 135,154 151,162 167,168 183,173 199,178 215,182 231,186 247,190 263,193 279,196 295,198 311,201 327,204 343,206 359,208 369,209"/>
# MAGIC   <!-- Red curve: y=0, loss = -log(1-p) -->
# MAGIC   <polyline fill="none" stroke="#FF3621" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
# MAGIC     points="61,209 71,208 87,206 103,204 119,201 135,198 151,196 167,193 183,190 199,186 215,182 231,178 247,173 263,168 279,162 295,154 311,146 327,134 343,118 349,109 359,90 369,54"/>
# MAGIC   <!-- Legend -->
# MAGIC   <rect x="255" y="32" width="90" height="32" fill="white" stroke="#ddd" stroke-width="0.5" rx="3"/>
# MAGIC   <line x1="262" y1="43" x2="282" y2="43" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="286" y="46" font-size="8" fill="#333">y = 1</text>
# MAGIC   <line x1="262" y1="57" x2="282" y2="57" stroke="#FF3621" stroke-width="2"/>
# MAGIC   <text x="286" y="60" font-size="8" fill="#333">y = 0</text>
# MAGIC </svg>
# MAGIC </div>
# MAGIC </br>
# MAGIC <div style="text-align: center; margin-bottom: 12px;">
# MAGIC   <span style="font-size: 1.25em; font-family: 'Latin Modern Math', 'STIX', 'Times New Roman', serif;">
# MAGIC     \( \text{Log Loss} = -\frac{1}{n} \sum_{i=1}^{n} \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right] \)
# MAGIC   </span>
# MAGIC </div>
# MAGIC
# MAGIC - When the true label is 1, the model is penalized for predicting low probabilities (blue curve rises steeply near 0).
# MAGIC - When the true label is 0, the model is penalized for predicting high probabilities (red curve rises steeply near 1).
# MAGIC - A confident wrong prediction receives a very high loss.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Bias-Variance Tradeoff

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ### C1. Bias-Variance Tradeoff
# MAGIC
# MAGIC The **bias-variance tradeoff** is a fundamental concept in machine learning that describes the balance between underfitting and overfitting.
# MAGIC
# MAGIC <div style="max-width: 900px; margin: 0 auto; display: flex; justify-content: center;">
# MAGIC <svg width="700" viewBox="0 0 500 320" role="img" style="font-family: sans-serif; flex-shrink: 0;">
# MAGIC   <title>Bias-Variance Tradeoff: Underfitting vs. Overfitting</title>
# MAGIC   <rect x="10" y="10" width="480" height="300" rx="12" fill="#FFFFFF" stroke="#1976D2" stroke-width="2"/>
# MAGIC   <text x="250" y="38" text-anchor="middle" font-size="14" font-weight="bold" fill="#1565C0">Underfitting vs. Overfitting</text>
# MAGIC
# MAGIC   <!-- Underfitting region (darker blue) -->
# MAGIC   <rect x="60" y="55" width="120" height="215" fill="#90CAF9" opacity="0.7"/>
# MAGIC   <text x="120" y="72" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565C0">Underfitting</text>
# MAGIC   <text x="75" y="190" font-size="10" font-weight="bold" fill="#1565C0">High Bias</text>
# MAGIC   <text x="75" y="200" font-size="10" font-weight="bold" fill="#1565C0">Low Variance</text>
# MAGIC
# MAGIC   <!-- Overfitting region (darker red) -->
# MAGIC   <rect x="300" y="55" width="140" height="215" fill="#FFCDD2" opacity="0.7"/>
# MAGIC   <text x="370" y="72" text-anchor="middle" font-size="11" font-weight="bold" fill="#C62828">Overfitting</text>
# MAGIC   <text x="345" y="190" font-size="10" font-weight="bold" fill="#C62828">High Variance</text>
# MAGIC   <text x="345" y="200" font-size="10" font-weight="bold" fill="#C62828"> Low Bias</text> 
# MAGIC   
# MAGIC
# MAGIC   <!-- Region of balance (darker green) -->
# MAGIC   <rect x="180" y="55" width="120" height="215" fill="#A5D6A7" opacity="0.7"/>
# MAGIC   <text x="240" y="68" text-anchor="middle" font-size="10" fill="#2E7D32">Sweet</text>
# MAGIC   <text x="240" y="80" text-anchor="middle" font-size="10" fill="#2E7D32">Spot</text>
# MAGIC
# MAGIC   <!-- Axes -->
# MAGIC   <line x1="50" y1="270" x2="450" y2="270" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <line x1="50" y1="55" x2="50" y2="270" stroke="#1B3139" stroke-width="1.5"/>
# MAGIC   <text x="70" y="292" text-anchor="middle" font-size="11" fill="#1B3139">Lower</text>
# MAGIC   <text x="250" y="292" text-anchor="middle" font-weight="bold" font-size="13" fill="#1B3139">Model Complexity</text>
# MAGIC   <text x="450" y="292" text-anchor="middle" font-size="11" fill="#1B3139">Higher</text>
# MAGIC   <text x="30" y="165" text-anchor="middle" font-weight="bold" font-size="13" fill="#1B3139" transform="rotate(-90 30 165)">Error</text>
# MAGIC
# MAGIC   <!-- Validation Error curve (U-shaped) -->
# MAGIC   <path d="M75,100 C130,150 180,210 240,220 C300,210 370,140 440,70" fill="none" stroke="#C62828" stroke-width="2.5"/>
# MAGIC   <text x="410" y="110" font-size="11" fill="#C62828" font-weight="bold">Validation</text>
# MAGIC   <text x="410" y="120" font-size="11" fill="#C62828" font-weight="bold">Error</text>
# MAGIC
# MAGIC   <!-- Training Error curve (follows validation in underfitting, then trails to low value) -->
# MAGIC   <path d="M75,105 C130,155 180,215 240,240 C300,250 380,258 440,262" fill="none" stroke="#1565C0" stroke-width="2.5"/>
# MAGIC   <text x="410" y="240" font-size="11" fill="#1565C0" font-weight="bold">Training</text>
# MAGIC   <text x="410" y="250" font-size="11" fill="#1565C0" font-weight="bold">Error</text>
# MAGIC
# MAGIC   <!-- Optimal point marker -->
# MAGIC   <circle cx="240" cy="220" r="5" fill="#2E7D32" opacity="0.8"/>
# MAGIC   <line x1="240" y1="220" x2="240" y2="270" stroke="#2E7D32" stroke-width="1" stroke-dasharray="4,3"/>
# MAGIC
# MAGIC
# MAGIC </svg>
# MAGIC </div>
# MAGIC
# MAGIC <table style="border-collapse: collapse; width: 100%; max-width: 860px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 14px; margin: 16px 0;">
# MAGIC   <thead>
# MAGIC     <tr style="background-color: #1B3139;">
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Condition</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Description</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Effect on Errors</th>
# MAGIC       <th style="padding: 12px 16px; text-align: left; color: #ffffff; border-bottom: 3px solid #FF3621;">Mitigation Strategies</th>
# MAGIC     </tr>
# MAGIC   </thead>
# MAGIC   <tbody>
# MAGIC     <tr style="background-color: #F9F7F4;">
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">High Bias</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Error due to overly <strong>simplistic assumptions</strong> in the model. The model is too simple to capture the underlying pattern.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Train and validation error are both high (the model underfits).</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Add more features, increase model complexity, reduce regularization.</td>
# MAGIC     </tr>
# MAGIC     <tr>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0; font-weight: 600;">High Variance</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Error due to sensitivity to <strong>small fluctuations</strong> in the training data. The model does not generalize well.</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Training error is low but validation error is high (a large gap; the model overfits).</td>
# MAGIC       <td style="padding: 12px 16px; border-bottom: 1px solid #e0e0e0;">Add more data, regularization, reduce complexity, or use cross-validation.</td>
# MAGIC     </tr>
# MAGIC   </tbody>
# MAGIC </table>

# COMMAND ----------

# DBTITLE 1,Conclusion
# MAGIC %md
# MAGIC ## Conclusion
# MAGIC
# MAGIC This appendix reviewed the foundational evaluation metrics for supervised learning:
# MAGIC
# MAGIC **Regression Metrics:**
# MAGIC * The **residual** is the core building block — the distance between each observed value and the model's prediction
# MAGIC * **R²** measures how much of the total variability (SS_tot) the model explains by comparing model error (SS_res) to a baseline mean prediction
# MAGIC * **MAE** averages the absolute residuals — interpretable and robust to outliers
# MAGIC * **MSE** averages the squared residuals — penalizes large errors more heavily and is differentiable for optimization
# MAGIC * **RMSE** is the square root of MSE — returns the error to the original units of the target variable
# MAGIC
# MAGIC **Classification Metrics:**
# MAGIC * The **confusion matrix** (TP, FP, FN, TN) is the foundation for all classification metrics
# MAGIC * **Precision** and **Recall** capture different error costs — choose based on whether false positives or false negatives are more harmful
# MAGIC * **F1 Score** balances precision and recall into a single number
# MAGIC * **Log Loss** penalizes confident wrong predictions steeply — it evaluates predicted probabilities, not just class labels
# MAGIC
# MAGIC **Bias-Variance Tradeoff:**
# MAGIC * **High bias** (underfitting) means the model is too simple to capture patterns — both training and validation errors are high
# MAGIC * **High variance** (overfitting) means the model memorizes noise — training error is low but validation error is high
# MAGIC * The goal is to find the **sweet spot** where the gap between training and validation error is minimized

# COMMAND ----------

# MAGIC %md
# MAGIC &copy; 2026 Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank">Support</a>
