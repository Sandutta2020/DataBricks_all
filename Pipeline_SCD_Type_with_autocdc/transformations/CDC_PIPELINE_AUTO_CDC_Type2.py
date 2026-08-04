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
)