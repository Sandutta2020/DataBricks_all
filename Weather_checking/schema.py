from pyspark.sql.types import StructField,StructType,IntegerType,StringType,DoubleType

class Schemas:
    orders = StructType(
        [
            StructField("order_id",StringType(),nullable=False),
            StructField("Customer_id",StringType(),nullable=False),
            StructField("order_count",IntegerType(),nullable=False),
            StructField("order_amount",DoubleType(),nullable=False)
        ]
    )