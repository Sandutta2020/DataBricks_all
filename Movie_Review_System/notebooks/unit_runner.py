# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
import sys
sys.path.insert(0, "/Workspace/Users/santanu.dutta@mheducation.com/Lure_data_analysis_pipeline/notebooks")
import app
app.main()


# COMMAND ----------

# MAGIC %md
# MAGIC To Check how many logs are created

# COMMAND ----------

# MAGIC %sh
# MAGIC ls -al /Volumes/adhoc_write_qastg/dna_de/lure_data_analysis/logDir/

# COMMAND ----------

# MAGIC %sql
# MAGIC Create or replace table Movie_Demo.Movie_Schema.Movie_job_control_table
# MAGIC (ID BIGINT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
# MAGIC  job_run_id string,
# MAGIC  job_name string,
# MAGIC  job_status string,
# MAGIC  job_start_time timestamp,
# MAGIC  job_end_time timestamp
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from Movie_Demo.Movie_Schema.Movie_job_control_table

# COMMAND ----------

# MAGIC %sql
# MAGIC update Movie_Demo.Movie_Schema.Movie_job_control_table
# MAGIC set job_end_time = current_timestamp()
# MAGIC where job_run_id = '2807971217842'

# COMMAND ----------

import sys

root_path = "/Workspace/Users/sandutta2020@gmail.com/DataBricks_all/Movie_Review_System"
if root_path not in sys.path:
    sys.path.insert(0, root_path)


from src.utils.config_loader import load_config
from src.utils.logger_utils import get_logger
cfg =load_config()
print(cfg)
print("--------------------------------------",cfg.get('paths', {}))
print(type(cfg.get('paths', {})))


# COMMAND ----------

list(cfg.get('paths', {}).values())

# COMMAND ----------

list(cfg.get('tables', {}).values())

# COMMAND ----------

list(cfg.get('paths', {}).values())

# COMMAND ----------

cfg.get('catalog')

# COMMAND ----------

cfg.get('schema')
