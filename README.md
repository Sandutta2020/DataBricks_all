# Spark / Delta Live Tables (DLT) CDC Integration Guide

A production-ready documentation guide and reference architecture for implementing **Change Data Capture (CDC)** using Delta Live Tables (DLT) and Python (`pyspark.pipelines`).

---

## 📌 Executive Summary

This repository demonstrates how to build an automated, real-time **Change Data Capture (CDC) processing flow** in Databricks using Delta Live Tables (`pyspark.pipelines`).

By capturing Delta Lake **Change Data Feed (CDF)** streams and applying incremental updates to target Delta tables, this pipeline handles standard **SCD Type 1 (Slowly Changing Dimensions)** operations—including `INSERT`, `UPDATE`, `DELETE`, and `TRUNCATE` operations—seamlessly without manual merge/upsert logic.

---

## 🏗️ Architecture & Data Flow

The CDC flow follows a two-tier streaming architecture designed for low-latency state synchronisation:<br>
┌────────────────────────────────────────────────────────┐ <br>
│     cdc_catalog.cdc_schema.users_cdf    │  <-- Source Table (Delta Change Data Feed) <br> |
└────────────────────┬───────────────────────────────────┘<br>
                     │<br>
<center>▼</center><br>
┌─────────────────────────────────────────┐<br>
│              users (View)               │  <-- DLT Streaming View<br>
└────────────────────┬────────────────────┘<br>
│<br>
│  dp.create_auto_cdc_flow()
│  (Keys: userId, Seq: sequenceNum)
<center>▼</center><br>
┌─────────────────────────────────────────┐
│            users_current                │  <-- Target DLT Streaming Table (SCD Type 1)
└─────────────────────────────────────────┘

## 💻 Code Walkthrough

```python
from pyspark import pipelines as dp
from pyspark.sql.functions import col, expr

# 1. Define a streaming view on the raw CDC/CDF source table
@dp.view
def users():
    return spark.readStream.table("cdc_catalog.cdc_schema.users_cdf")

# 2. Declare the target streaming table where the state will be maintained
dp.create_streaming_table("users_current")

# 3. Configure and execute the automated CDC ingestion pipeline
dp.create_auto_cdc_flow(
    target = "users_current",
    source = "users",
    keys = ["userId"],
    sequence_by = col("sequenceNum"),
    apply_as_deletes = expr("operation = 'DELETE'"),
    apply_as_truncates = expr("operation = 'TRUNCATE'"),
    except_column_list = ["operation", "sequenceNum"],
    stored_as_scd_type = 1
)
```
⚙️ Parameter BreakdownParameterTypePurpose / FunctiontargetSTRING :-The name of the target Delta streaming table (users_current) storing the current state.sourceSTRINGThe streaming view or <br>table containing the CDC changelog stream (users).keysLIST[STRING]Primary key(s) used to uniquely identify records across updates and deletes (['userId']).sequence_byColumnColumn <br>
 used to determine message ordering (sequenceNum). Out-of-order records with lower sequence numbers are ignored.apply_as_deletesColumn / ExpressionBoolean expression identifying rows that <br><br>trigger deletion from the target (operation = 'DELETE').apply_as_truncatesColumn / ExpressionBoolean expression identifying records that trigger a full table <br>
 truncation (operation = 'TRUNCATE').except_column_listLIST[STRING]Metadata or control columns excluded from the target schema (['operation', 'sequenceNum']).stored_as_scd_typeINT /<br><br>STRINGCDC handling strategy. Set to 1 (or "1") for SCD Type 1 (overwriting existing records with the latest state).🔄 How CDC Handlers Process OperationsINSERT / UPDATE <br>Operations:Records with matching userId are overwritten with the newest payload based on the highest sequenceNum.DELETE Operations:When operation = 'DELETE', the row matching userId <br>is physically deleted from users_current.TRUNCATE Operations:When operation = 'TRUNCATE', all existing records in users_current are cleared, resetting the target table state.<br>Out-of-Order Messages:If a record arrives with a sequenceNum lower than an already processed record for the same userId, DLT automatically drops the stale record.🚀 Deployment Steps <br>(Databricks Workflows / DLT)Enable Change Data Feed (CDF) on the source Delta table:SQLALTER TABLE cdc_catalog.cdc_schema.users_cdf 
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);<br>
Create a DLT Pipeline:Navigate to Delta Live Tables in Databricks.Click Create Pipeline.Set pipeline target schema (e.g., prod_users_lakehouse).Add this Python script file as a pipeline <br> library source.Run Pipeline:Select Triggered for batch schedules or Continuous for real-time streaming state maintenance.🛡️ Best Practices & GovernanceUnity Catalog Integration:  <br>Grant explicit SELECT privileges on cdc_catalog.cdc_schema.users_cdf to the identity principal running the DLT pipeline.Sequence Column Quality: Ensure sequenceNum is strictly  <br>monotonic (e.g., timestamp or transactional LSN/offset) to prevent valid updates from being ignored.CDC Metadata Exclusion: Always exclude non-business pipeline metadata (like <br>operation, sequenceNum, or system ingest timestamps) via except_column_list to maintain clean Gold/Silver target tables.
