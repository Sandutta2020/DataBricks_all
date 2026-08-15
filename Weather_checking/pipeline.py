from pyspark.sql import SparkSession,DataFrame
from job_interface import PysparkJobInterface
from databricks.connect import DatabricksSession
from schema import Schemas

class PySparkJob(PysparkJobInterface):
    def init_spark_session(self) -> SparkSession:
        print("inside ")
        return SparkSession.builder.appName("Orders_data_load").getOrCreate()
        #return DatabricksSession.builder.getOrCreate()
    
    def load_and_clean_data(self,orders_path :str) -> DataFrame:
        orders_df = self.read_json(orders_path, schema=Schemas.orders)
        orders_df.show()
        return orders_df
