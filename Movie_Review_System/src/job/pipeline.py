from pyspark.sql import functions as F
from datetime import datetime
import sys,os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)
from src.base.job_interface import PysparkJobInterface
from src.base.schema_defn import Schemas
from pyspark.sql import DataFrame

class PySparkJob(PysparkJobInterface):
    
    def check_job_control(self, job_name: str) -> bool:
        # Check Delta control table for last status
        try:
            last_status = self.spark.sql(f"""
                SELECT job_status FROM Movie_Demo.Movie_Schema.Movie_job_control_table 
                WHERE job_name = '{job_name}' 
                and job_end_time is null limit 1
            """).collect()
            
            if last_status:
                return False
            return True
        except Exception as e:
            print("Its coming in exception---------")
            print(f"Error details: {e}")

            return False # Table might not exist on first run
    def insert_job_control(self, job_name: str,job_run_id: str) -> None:
        # Check Delta control table for last status
        try:
            last_status = self.spark.sql(f"""
                INSERT INTO  Movie_Demo.Movie_Schema.Movie_job_control_table
                (
                    job_run_id,
                    job_name ,
                    job_status,
                    job_start_time
                ) 
                values
                (
                    '{job_run_id}',
                    '{job_name}',
                    'RUNNING',
                    Current_timestamp()
                ) 
            """)
            print("Insert completed on control tables")
        except Exception:
            print("Its coming in exception---------")
            raise
    def update_job_control(self, job_name: str,job_run_id: str) -> None:
        # Check Delta control table for last status
        try:
            last_status = self.spark.sql(f"""
                update Movie_Demo.Movie_Schema.Movie_job_control_table 
                set job_end_time = current_timestamp(),
                job_status = 'COMPLETED'
                where job_run_id = '{job_run_id}'
                and job_name = '{job_name}'
            """)
            print("Insert completed on control tables")
        except Exception:
            print("Its coming in exception---------")
            raise
    def log_audit(self, job_name: str, status: str, record_count: int = 0):
        data = [(job_name, status, record_count, datetime.now())]
        columns = ["job_name", "status", "record_count", "timestamp"]
        df = self.spark.createDataFrame(data, columns)
        df.write.format("delta").mode("append").saveAsTable("audit_table")

    def load_and_clean_data(self, path: str) -> DataFrame:
        df = self.read_csv(path,Schemas.lure)
        return df.dropna(how='any')

    def write_to_bronze(self, df: DataFrame, table_name: str) -> None:
        df.write.format("delta").mode("append").saveAsTable(table_name)


