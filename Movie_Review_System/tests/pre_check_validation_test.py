import pytest
import sys
from pyspark.sql import SparkSession,DataFrame
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, DoubleType, LongType,TimestampType
from datetime import datetime
from pyspark.sql.functions import when, col
from pyspark.testing.utils import assertDataFrameEqual, assertSchemaEqual
root_path = "/Workspace/Users/sandutta2020@gmail.com/DataBricks_all/Movie_Review_System"
if root_path not in sys.path:
    sys.path.insert(0, root_path)
from src.job.pipeline import PySparkJob
from src.utils.config_loader import load_config
from pyspark.dbutils import DBUtils

cfg =load_config()
expected_tables =list(cfg.get('tables', {}).values())
expected_paths = list(cfg.get('paths', {}).values())
# This is a pytest fixture that sets up a Spark session for the tests.
# The fixture is called 'spark' and it will be set up once per test session.
@pytest.fixture(scope="session")
def spark():
    # Create a Spark session. If one already exists, reuse it.
    spark = SparkSession.builder.getOrCreate()
    
    # Pass the Spark session to the test function.
    yield spark
    # After the test, you can add cleanup code if needed.

catalog_name =cfg.get('catalog')
schema_name =cfg.get('schema')

expected_tables_bkp = [
        "Movie_Demo.Movie_Schema.Movie_job_control_table",
        "Movie_Demo.Movie_Schema.movie_review_data_bronze"
    ]

def test_bronze_tables_exist(spark):
    missing = [
        tbl
        for tbl in expected_tables
        if not spark.catalog.tableExists(tbl)
    ]

    assert not missing, f"Missing tables: {missing}"

@pytest.mark.parametrize("table", expected_tables)
def test_table_read_access(spark, table):
    try:
        spark.sql(
            f"SELECT * FROM {table} LIMIT 1"
        ).collect()

    except Exception as e:
        pytest.fail(
            f"Access check failed for {table}: {e}"
        )

def test_required_path_exists(spark):
    dbutils = DBUtils(spark)
    missing =[]
    for path in expected_paths:
        try:
            dbutils.fs.ls(path)
        except Exception:
            missing.append(path)
    assert not missing,(
         f"missing directories :{', '.join(missing)}"
     )

def test_catalog_schema_exists(spark):
    assert spark.catalog.databaseExists(f"{catalog_name}.{schema_name}"),  (
        f"Schema '{catalog_name}.{schema_name}' does not exist."
    )

