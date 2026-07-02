from pyspark import pipelines as dp
from pyspark.sql.functions import col, expr

@dp.view
def users():
  return spark.readStream.table("cdc_catalog.cdc_schema.users_cdf")

dp.create_streaming_table("users_history")

dp.create_auto_cdc_flow(
  target = "users_history",
  source = "users",
  keys = ["userId"],
  sequence_by = col("sequenceNum"),
  apply_as_deletes = expr("operation = 'DELETE'"),
  except_column_list = ["operation", "sequenceNum"],
  stored_as_scd_type = "2"
)