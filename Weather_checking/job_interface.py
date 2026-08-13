import abc
from  pyspark.sql.types import StructType
from pyspark.sql import SparkSession,DataFrame

class PysparkJobInterface(abc.ABC):
    def __init__(self):
        self.spark = self.init_spark_session()
    @abc.abstractmethod
    def init_spark_session(self) -> SparkSession:
        raise NotImplementedError

    def read_json(self,input_path:str,schema: StructType =None) -> DataFrame:
        reader = self.spark.read
        if schema is None:
            return reader.json(input_path)
        else:
            return reader.schema(schema).json(input_path)
    @abc.abstractmethod
    def load_and_clean_data(self,customers_path: str) -> DataFrame:
        raise NotImplementedError

    def stop(self) -> None:
        self.spark.stop()
    