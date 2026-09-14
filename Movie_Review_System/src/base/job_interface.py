import abc
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType
from pyspark.dbutils import DBUtils

class PysparkJobInterface(abc.ABC):
    def __init__(self, env="DEV"):
        self.spark = SparkSession.builder.getOrCreate()
        self.env = env
        # In Databricks, we use dbutils for file system operations        
        self.dbutils = DBUtils(self.spark)

    @abc.abstractmethod
    def check_job_control(self, job_name: str) -> bool:
        """Check if the previous job failed."""
        pass

    @abc.abstractmethod
    def log_audit(self, job_name: str, status: str, record_count: int):
        """Log job metrics to Delta table."""
        pass



    def move_file(self, source: str, destination: str) -> bool:
        files = self.dbutils.fs.ls(source)
        file_count = len(files)
        if file_count >  0:
            #self.dbutils.fs.mv(source, destination, recurse=True)
            for file in files:
                src_path = file.path
                # Extract just the file/folder name
                file_name = file.name
                dest_path = f"{destination.rstrip('/')}/{file_name}"
                self.dbutils.fs.mv(src_path, dest_path, recurse=True)
                print(f"Moved: {src_path} -> {dest_path}")
            return True
        else:
            return False
        

    def read_csv(self, path: str, schema: StructType = None) -> DataFrame:
        reader = self.spark.read
        df = reader.csv(path,header=True,schema=schema) if schema else reader.csv(path,header=True)
        print("-----Number of records-------------",df.count())
        return df 

    def stop(self):
        self.spark.stop()
