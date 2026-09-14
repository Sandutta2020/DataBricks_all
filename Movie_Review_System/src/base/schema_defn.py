from pyspark.sql.types import StructField,StructType,TimestampType,StringType,DoubleType,IntegerType

class Schemas:
    lure = StructType(
        [
            StructField("MovieID",IntegerType(),nullable=False),
            StructField("Rating",DoubleType(),nullable=False),
            StructField("ReviewYM",IntegerType(),nullable=False)
            ]
    )
	
