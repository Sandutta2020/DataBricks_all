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

## 💻 Code Walkthrough for SSCD Type 1

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
    sequence_by = col("_commit_timestamp"),
    apply_as_deletes = expr("operation = 'delete'"),
    apply_as_truncates = expr("operation = 'truncate'"),
    except_column_list = ["_change_type", "_commit_version","_commit_timestamp"],
    stored_as_scd_type = 1
)
```




# Pipeline Documentation: Automated CDC Ingestion (`users_current`)

| Component / Step | Details & Configuration | Explanation / Technical Behavior |
| :--- | :--- | :--- |
| **Pipeline Type** | Delta Live Tables / Declarative Pipelines (`pyspark.pipelines`) | Automated Change Data Capture (CDC) processing using **SCD Type 1** |
| **1. Source View** | `@dp.view`<br>`def users():`<br>`  return spark.readStream.table("cdc_catalog.cdc_schema.users_cdf")` | Reads continuously from the source Unity Catalog table (`cdc_catalog.cdc_schema.users_cdf`). An ephemeral view that exists only within the pipeline execution scope. |
| **2. Target Table** | `dp.create_streaming_table("users_current")` | Declares the materialized target streaming table where the current state is stored and maintained. |
| **3. Target Setting** | `target = "users_current"` | Specifies the destination table where all CDC actions (inserts, updates, deletes, truncates) are applied. |
| **4. Source Setting** | `source = "users"` | Identifies the streaming view supplying the incoming Change Data Capture / Change Data Feed events. |
| **5. Primary Keys** | `keys = ["userId"]` | Defines the primary key column(s) used to match incoming records against existing records in the target table. |
| **6. Event Ordering** | `sequence_by = col("_commit_timestamp")` | Resolves out-of-order CDC events. If multiple events arrive for the same `userId`, the record with the latest `_commit_timestamp` is applied. |
| **7. Delete Condition** | `apply_as_deletes = expr("operation = 'delete'")` | Evaluates incoming records; when `operation = 'delete'`, the matching record in `users_current` is deleted. |
| **8. Truncate Condition**| `apply_as_truncates = expr("operation = 'truncate'")` | Evaluates incoming records; when `operation = 'truncate'`, all data in the target table is cleared. |
| **9. Excluded Columns**| `except_column_list = ["_change_type", "_commit_version", "_commit_timestamp"]` | Excludes internal CDC metadata columns from being saved into the destination schema. |
| **10. Storage Strategy**| `stored_as_scd_type = 1` | Applies **Slowly Changing Dimension Type 1 (SCD1)** logic. Incoming updates overwrite existing matching rows in place without retaining historical records. |

## 💻 Code Walkthrough for SCD Type 2

```python
from pyspark import pipelines as dp
from pyspark.sql.functions import col, expr

@dp.view
def users_2():
  return spark.readStream.table("cdc_catalog.cdc_schema.customers_cdf")

dp.create_streaming_table("cdc_catalog.cdc_schema.users_history")

dp.create_auto_cdc_flow(
  target = "cdc_catalog.cdc_schema.users_history",
  source = "users_2",
  keys = ["userId"],
  sequence_by = col("_commit_timestamp"),
  apply_as_deletes = expr("_change_type = 'delete'"),
  except_column_list = ["_change_type", "_commit_version","_commit_timestamp"],
  stored_as_scd_type = "2"
```
# Pipeline Documentation: Historical CDC Ingestion (`users_history`)

| Component / Step | Details & Configuration | Explanation / Technical Behavior |
| :--- | :--- | :--- |
| **Pipeline Type** | Delta Live Tables / Declarative Pipelines (`pyspark.pipelines`) | Automated Change Data Capture (CDC) processing using **SCD Type 2** |
| **1. Source View** | `@dp.view`<br>`def users_2():`<br>`  return spark.readStream.table("cdc_catalog.cdc_schema.customers_cdf")` | Reads continuously from the source Unity Catalog table (`cdc_catalog.cdc_schema.customers_cdf`). An ephemeral view that exists only within the pipeline execution scope. |
| **2. Target Table** | `dp.create_streaming_table("cdc_catalog.cdc_schema.users_history")` | Declares the fully-qualified materialized target streaming table where current and historical states are stored. |
| **3. Target Setting** | `target = "cdc_catalog.cdc_schema.users_history"` | Specifies the destination table where all CDC actions are tracked over time. |
| **4. Source Setting** | `source = "users_2"` | Identifies the streaming view supplying the incoming Change Data Capture / Change Data Feed events. |
| **5. Primary Keys** | `keys = ["userId"]` | Defines the primary key column(s) used to track individual entity state changes over time. |
| **6. Event Ordering** | `sequence_by = col("_commit_timestamp")` | Resolves out-of-order CDC events. If multiple events arrive for the same `userId`, the record with the latest `_commit_timestamp` determines the timeline. |
| **7. Delete Condition** | `apply_as_deletes = expr("_change_type = 'delete'")` | Evaluates incoming records; when `_change_type = 'delete'`, the active record for that `userId` is closed/deactivated in `users_history`. |
| **8. Excluded Columns**| `except_column_list = ["_change_type", "_commit_version", "_commit_timestamp"]` | Excludes raw CDC metadata columns from being saved directly into the destination table payload. |
| **9. Storage Strategy**| `stored_as_scd_type = "2"` | Applies **Slowly Changing Dimension Type 2 (SCD2)** logic. Automatically generates effective/expiration timestamps (`__START_AT`, `__END_AT`) to retain full historical records for each change. |

----------------------------------------------------------------------
```python
def calling_customer_cdf():
    spark.\
        readStream.\
            option("readChangeFeed", "true").\
                option("startingVersion", 0).\
                    table("customer_source_table").\
                        writeStream.\
                            option("checkpointLocation", "/Volumes/cdc_catalog/cdc_schema/cdc_customer_vol_ckpoint").\
                                trigger (availableNow=True).\
                                    table("customers_cdf")
```
----------------------------------------------------------------------

# Pipeline Documentation: Spark Structured Streaming CDF Reader (`calling_customer_cdf`)

| Component / Step | Details & Configuration | Explanation / Technical Behavior |
| :--- | :--- | :--- |
| **Pipeline Type** | PySpark Structured Streaming | Continuous/Batch-triggered Delta Lake Change Data Feed (CDF) extraction |
| **1. Function Name** | `def calling_customer_cdf():` | Encapsulates the PySpark streaming reader and writer pipeline logic. |
| **2. Stream Reader** | `spark.readStream` | Initiates a PySpark Structured Streaming reader. |
| **3. Enable CDF** | `option("readChangeFeed", "true")` | Configures the Delta reader to stream change events (inserts, updates, deletes) instead of standard table snapshots. |
| **4. Starting Point** | `option("startingVersion", 0)` | Instructs the reader to process Change Data Feed records starting from Delta table version `0` (full history replay). |
| **5. Source Table** | `table("customer_source_table")` | Sets `customer_source_table` as the origin table supplying the change stream. |
| **6. Stream Writer** | `writeStream` | Configures the streaming sink write execution. |
| **7. Checkpoint Path**| `option("checkpointLocation", "/Volumes/...")` | Stores streaming metadata and progress state in Unity Catalog Volumes (`/Volumes/cdc_catalog/cdc_schema/cdc_customer_vol_ckpoint`) to ensure fault tolerance and exactly-once processing guarantees. |
| **8. Trigger Mode** | `trigger(availableNow=True)` | Executes the stream as a batch micro-batch (processes all available unread data and stops automatically). |
| **9. Target Table** | `table("customers_cdf")` | Persists the raw Change Data Feed output directly into the `customers_cdf` destination Delta table. |


