# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# %run ./_common

# COMMAND ----------

# MAGIC %md
# MAGIC #@DBAcademyHelper.add_init
# MAGIC #def initialize_uc(self):
# MAGIC
# MAGIC     #table_name = 'telco_table'
# MAGIC     #inference_table = 'batch_inference'
# MAGIC     #spark.sql(f"USE CATALOG {DA.catalog_name}")
# MAGIC     #spark.sql(f"USE SCHEMA {DA.schema_name}")
# MAGIC     #spark.sql(f"DROP TABLE IF EXISTS {table_name}")
# MAGIC     spark.sql(f"DROP TABLE IF EXISTS {inference_table}")
# MAGIC
# MAGIC     print(f'Using catalog {DA.catalog_name} and schema {DA.schema_name}.')

# COMMAND ----------

table_name = 'telco_table'
inference_table = 'batch_inference'
spark.sql(f"USE CATALOG dbx_catalog")
spark.sql(f"USE SCHEMA dbx_schema")
spark.sql(f"DROP TABLE IF EXISTS {table_name}")
spark.sql(f"DROP TABLE IF EXISTS {inference_table}")

# COMMAND ----------

# Initialize DBAcademyHelper
#DA = DBAcademyHelper() 
#DA.init()
