-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 16px; background: #F8F9FA; border-bottom: 2px solid #E0E0E0; margin: 0; line-height: 1;">
-- MAGIC     <div style="font-size: 14px; color: #666;">
-- MAGIC         <span style="font-weight: bold; color: #333;">Oracle -> Databricks Migration</span>
-- MAGIC         <span style="margin-left: 8px; color: #999;">|</span>
-- MAGIC         <span style="margin-left: 8px;">06 - Closeout</span>
-- MAGIC     </div>
-- MAGIC     <div style="display: flex; align-items: center; gap: 8px;">
-- MAGIC         <img src="https://api.iconify.design/simple-icons:oracle.svg?color=%23F80102" width="24" height="24" />
-- MAGIC         <span style="color: #999; font-size: 16px;">-></span>
-- MAGIC         <img src="https://cdn.simpleicons.org/databricks/FF3621" width="24" height="24"/>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img
-- MAGIC     src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png"
-- MAGIC     alt="Databricks Learning"
-- MAGIC   >
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Observability and Cost Monitoring
-- MAGIC
-- MAGIC With migration complete and workloads running in production, this lesson focuses on establishing enterprise-grade observability. You will integrate Databricks with external monitoring platforms, configure notification destinations for alerting, and set up Lakehouse Monitoring for ongoing data quality. This enables your operations team to monitor, troubleshoot, and optimize the platform as part of standard ITSM processes.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Learning Objectives
-- MAGIC
-- MAGIC By the end of this lesson, you will be able to:
-- MAGIC
-- MAGIC - Integrate Databricks observability with enterprise monitoring tools (Splunk, Datadog, CloudWatch, Azure Monitor)
-- MAGIC - Configure Lakehouse Monitoring for automated data quality and drift detection
-- MAGIC - Create operational dashboards for platform health, job performance, and cost tracking
-- MAGIC - Set up notification destinations (Slack, Teams, PagerDuty, email, webhooks) for alerting
-- MAGIC - Integrate Databricks into enterprise ITSM workflows for incident management

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ## 1. Enterprise Observability Architecture
-- MAGIC
-- MAGIC Post-migration observability integrates Databricks system tables and alerting capabilities with your existing enterprise tooling. The goal is to fit Databricks monitoring into your established ITSM processes rather than creating parallel workflows.
-- MAGIC
-- MAGIC <br/>
-- MAGIC <div class="mermaid">
-- MAGIC flowchart LR
-- MAGIC     subgraph DBX["Databricks"]
-- MAGIC         SYS["System Tables"]
-- MAGIC         ALRT["SQL Alerts"]
-- MAGIC     end
-- MAGIC     subgraph ENT["Enterprise Tooling"]
-- MAGIC         MON["Monitoring Platform"]
-- MAGIC         NOTIFY["Notification Channels"]
-- MAGIC     end
-- MAGIC     subgraph OPS["Operations"]
-- MAGIC         ITSM["ITSM / Incident Mgmt"]
-- MAGIC     end
-- MAGIC     SYS -->|"Export / Query"| MON
-- MAGIC     ALRT --> NOTIFY
-- MAGIC     NOTIFY --> ITSM
-- MAGIC     MON --> ITSM
-- MAGIC     style DBX fill:#ffe0b2,stroke:#FF3621,stroke-width:2px
-- MAGIC     style ENT fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
-- MAGIC     style OPS fill:#e8f5e9,stroke:#4caf50,stroke-width:2px
-- MAGIC </div>
-- MAGIC <script type="module"> import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true, theme: "default" }); </script>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 2. System Tables for Observability
-- MAGIC
-- MAGIC System tables provide the foundation for all observability in Databricks. These tables can be queried directly, exported to external systems, or used to power dashboards and alerts.
-- MAGIC
-- MAGIC | Schema | Key Tables | Use Case |
-- MAGIC |--------|------------|----------|
-- MAGIC | `system.billing` | `usage`, `list_prices` | Cost dashboards, chargeback reports, budget alerts |
-- MAGIC | `system.lakeflow` | `jobs`, `job_tasks`, `job_task_run_timeline`, `pipelines` | Job SLA monitoring, failure alerting |
-- MAGIC | `system.compute` | `clusters`, `warehouse_events` | Capacity planning, utilization trending |
-- MAGIC | `system.access` | `audit`, `table_lineage` | Security monitoring, compliance reporting |
-- MAGIC | `system.query` | `history` | Performance analysis, slow query detection |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #1976d2; background: #e3f2fd; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">ℹ️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #0d47a1; font-size: 1.1em;">System Table Data Retention</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">System tables retain data for varying periods: billing data for 365 days, audit logs for 365 days, query history for 30 days, and job runs for 60 days. For long-term retention, configure scheduled exports to your enterprise data lake or SIEM platform.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3. Enterprise Monitoring Integration
-- MAGIC
-- MAGIC Export Databricks metrics to your existing enterprise monitoring platforms for unified observability. The general pattern involves querying system tables on a schedule and pushing data to your monitoring platform via their ingestion APIs.
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Integration Patterns by Platform
-- MAGIC
-- MAGIC | Platform | Integration Method | Data Sources |
-- MAGIC |----------|-------------------|--------------|
-- MAGIC | **Datadog** | Datadog Agent on clusters, API export | Spark metrics, system tables |
-- MAGIC | **Splunk** | HTTP Event Collector (HEC), scheduled export | Audit logs, job events, query history |
-- MAGIC | **AWS CloudWatch** | CloudWatch Agent, custom metrics API | Cluster metrics, job telemetry |
-- MAGIC | **Azure Monitor** | Diagnostic settings, Log Analytics | Workspace logs, billing data |
-- MAGIC | **New Relic** | OTLP export, custom integration | Spark metrics, job telemetry |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #009688; background: #e0f2f1; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">💡</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #00695c; font-size: 1.1em;">Integration Approach</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Most integrations follow a common pattern: create a scheduled Databricks job that queries system tables, transforms the data into the target platform's format, and pushes it via API (e.g., Splunk HEC, CloudWatch PutMetricData, Datadog API). Use Databricks Secrets to store API keys securely.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 4. Notification Destinations and SQL Alerts
-- MAGIC
-- MAGIC Databricks supports multiple notification destinations for SQL Alerts, job notifications, and pipeline alerts. Configure these to integrate with your existing communication and incident management tools.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Supported Notification Destinations
-- MAGIC
-- MAGIC | Destination | Use Case | Configuration |
-- MAGIC |-------------|----------|---------------|
-- MAGIC | **Email** | Individual notifications, distribution lists | Built-in, configure recipients |
-- MAGIC | **Slack** | Team channels, ChatOps | Webhook URL or Slack app |
-- MAGIC | **Microsoft Teams** | Enterprise communication | Incoming webhook connector |
-- MAGIC | **PagerDuty** | On-call escalation, incident management | Integration key |
-- MAGIC | **Webhook** | Custom integrations (ServiceNow, Jira, etc.) | HTTP endpoint URL |
-- MAGIC
-- MAGIC Notification destinations are configured at the workspace level via **Settings -> Notification destinations** or programmatically via the Databricks CLI/API.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### SQL Alerts
-- MAGIC
-- MAGIC SQL Alerts evaluate queries on a schedule and trigger notifications when conditions are met. Use these for proactive monitoring of job failures, data quality issues, SLA breaches, and cost anomalies.
-- MAGIC
-- MAGIC **To create an alert:** Save a query, click the three-dot menu, select "Create Alert", configure the schedule and trigger condition, then assign notification destinations.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 5. Lakehouse Monitoring
-- MAGIC
-- MAGIC Lakehouse Monitoring provides automated data quality monitoring, drift detection, and statistical profiling for your tables. This capability has no direct Oracle equivalent and represents a key advantage of the Databricks platform.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Key Capabilities
-- MAGIC
-- MAGIC | Feature | Description |
-- MAGIC |---------|-------------|
-- MAGIC | **Profile Metrics** | Automated statistics (null counts, distinct values, distributions) captured on schedule |
-- MAGIC | **Drift Detection** | Compares current data against baseline to detect schema and data drift |
-- MAGIC | **Custom Metrics** | Define business-specific quality metrics using SQL expressions |
-- MAGIC | **Inference Tables** | Monitor ML model inputs and outputs for prediction drift |
-- MAGIC | **Alert Integration** | Trigger alerts when metrics breach thresholds |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC ### Setting Up Monitors
-- MAGIC
-- MAGIC Lakehouse Monitors are configured via the Catalog Explorer UI (**Catalog -> Select table -> Quality tab -> Create monitor**) or programmatically via the Databricks SDK. When a monitor is created, Databricks automatically generates profile and drift metrics tables in your specified output schema.
-- MAGIC
-- MAGIC <div style="border-left: 4px solid #ff9800; background: #fff3e0; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">⚠️</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #e65100; font-size: 1.1em;">Monitor Configuration</strong>
-- MAGIC             <p style="margin: 8px 0 0 0; color: #333;">Lakehouse Monitoring requires a Unity Catalog-enabled workspace and a SQL Warehouse for metric computation. Configure monitors on your most critical tables first — those that feed dashboards, reports, or ML models — and expand coverage over time.</p>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 6. Operational Dashboards
-- MAGIC
-- MAGIC Create AI/BI Dashboards for centralized visibility into platform health, job performance, and costs. These dashboards support daily operations and stakeholder reporting. All dashboard queries can be built from system tables.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Recommended Dashboards
-- MAGIC
-- MAGIC | Dashboard | Key Metrics | Refresh Schedule |
-- MAGIC |-----------|------------|------------------|
-- MAGIC | **Platform Health** | Active clusters, warehouse utilization, error rates | 5 minutes |
-- MAGIC | **Job Performance** | Success rates, SLA compliance, failure trends | 15 minutes |
-- MAGIC | **Data Quality** | Monitor drift scores, freshness, expectation failures | Hourly |
-- MAGIC | **Cost Tracking** | Daily DBU consumption, team attribution, budget status | Daily |

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC <div style="border-left: 4px solid #4caf50; background: #e8f5e9; padding: 16px 20px; border-radius: 4px; margin: 16px 0;">
-- MAGIC     <div style="display: flex; align-items: flex-start; gap: 12px;">
-- MAGIC         <span style="font-size: 24px;">✅</span>
-- MAGIC         <div>
-- MAGIC             <strong style="color: #2e7d32; font-size: 1.1em;">Observability Handoff Checklist</strong>
-- MAGIC             <ul style="margin: 8px 0 0 0; color: #333; padding-left: 20px;">
-- MAGIC                 <li>System tables accessible to operations team</li>
-- MAGIC                 <li>Notification destinations configured (Slack, Teams, PagerDuty, email)</li>
-- MAGIC                 <li>SQL Alerts created for job failures, SLA breaches, and cost anomalies</li>
-- MAGIC                 <li>Enterprise monitoring integration documented (or deployed)</li>
-- MAGIC                 <li>Lakehouse Monitors configured on critical tables</li>
-- MAGIC                 <li>Operational dashboards published with appropriate access</li>
-- MAGIC                 <li>Oracle observability baselines extracted and archived</li>
-- MAGIC                 <li>Runbook documentation linked from alert descriptions</li>
-- MAGIC             </ul>
-- MAGIC         </div>
-- MAGIC     </div>
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Summary
-- MAGIC
-- MAGIC This lesson covered establishing enterprise-grade observability for ongoing platform operations after migration.
-- MAGIC
-- MAGIC **Key Takeaways:**
-- MAGIC
-- MAGIC - **System Tables** - The foundation for all Databricks observability; query directly or export to external platforms
-- MAGIC - **Enterprise Integration** - Push system table data to Splunk, Datadog, CloudWatch, or Azure Monitor via scheduled jobs
-- MAGIC - **SQL Alerts** - Proactive monitoring with multi-channel notification destinations
-- MAGIC - **Lakehouse Monitoring** - Automated data quality with no Oracle equivalent
-- MAGIC - **Dashboards** - AI/BI Dashboards powered by system tables for operational visibility
-- MAGIC
-- MAGIC **References:**
-- MAGIC
-- MAGIC - [System Tables Overview](https://docs.databricks.com/en/admin/system-tables/index.html)
-- MAGIC - [SQL Alerts](https://docs.databricks.com/en/sql/user/alerts/index.html)
-- MAGIC - [Notification Destinations](https://docs.databricks.com/aws/en/admin/workspace-settings/notification-destinations)
-- MAGIC - [Lakehouse Monitoring](https://docs.databricks.com/en/lakehouse-monitoring/index.html)
-- MAGIC - [Audit Logs](https://docs.databricks.com/en/admin/account-settings/audit-logs.html)

-- COMMAND ----------

-- MAGIC %md-sandbox
-- MAGIC &copy; <span id="dbx-year"></span> Databricks, Inc. All rights reserved. Apache, Apache Spark, Spark, the Spark Logo, Apache Iceberg, Iceberg, and the Apache Iceberg logo are trademarks of the <a href="https://www.apache.org/" target="_blank" style="color: #1a5276; text-decoration: underline;">Apache Software Foundation</a>. Oracle and the Oracle logo are trademarks or registered trademarks of <a href="https://www.oracle.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Oracle Corporation.</a> All other trademarks are the property of their respective owners.<br/><br/><a href="https://databricks.com/privacy-policy" target="_blank" style="color: #1a5276; text-decoration: underline;">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use" target="_blank" style="color: #1a5276; text-decoration: underline;">Terms of Use</a> | <a href="https://help.databricks.com/" target="_blank" style="color: #1a5276; text-decoration: underline;">Support</a>
-- MAGIC
-- MAGIC <script> document.getElementById("dbx-year").textContent = new Date().getFullYear(); </script>
