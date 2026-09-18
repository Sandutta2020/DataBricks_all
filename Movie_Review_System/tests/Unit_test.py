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





# This is a pytest fixture that sets up a Spark session for the tests.
# The fixture is called 'spark' and it will be set up once per test session.
@pytest.fixture(scope="session")
def spark():
    # Create a Spark session. If one already exists, reuse it.
    spark = SparkSession.builder.getOrCreate()
    
    # Pass the Spark session to the test function.
    yield spark
    # After the test, you can add cleanup code if needed.



def test_read_csv_schema(spark):
    # Define the expected schema that the function should return and test with the
    # This is the reference schema that the function's output will be compared against.
    # If the function's behavior changes, the test will fail if the schema doesn't match.
    expected_schema =  StructType(
        [
            StructField("LMS_INSTALLATION_ID",StringType(),nullable=False),
            StructField("TOOL_PROVIDER",StringType(),nullable=False),
            StructField("INSTRUCTOR_XID",StringType(),nullable=False)
        ])

    # Call the function that retrieves the schema from the health CSV.
    # This should return a schema that will be validated against the expected schema.
   
    job =PySparkJob()
    actual_df = job.load_and_clean_data('/Volumes/adhoc_write_qastg/dna_de/lure_data_analysis/testing_dir/')
    actual_schema = actual_df.schema

    # Assert that the actual schema returned by the function matches the expected schema.
    # If the schemas don't match, the test will fail and indicate an issue with the function's output.
    assertSchemaEqual(actual_schema, expected_schema)

def test_read_csv_return_data(spark):
    # Define the expected schema that the function should return and test with the
    # This is the reference schema that the function's output will be compared against.
    # If the function's behavior changes, the test will fail if the schema doesn't match.
    expected_schema =  StructType(
        [
            StructField("LMS_INSTALLATION_ID",StringType(),nullable=False),
            StructField("TOOL_PROVIDER",StringType(),nullable=False),
            StructField("INSTRUCTOR_XID",StringType(),nullable=False),
        ])

    # Call the function that retrieves the schema from the health CSV.
    # This should return a schema that will be validated against the expected schema.
   
    job =PySparkJob()
    actual_df = job.load_and_clean_data('/Volumes/adhoc_write_qastg/dna_de/lure_data_analysis/testing_dir/')
    print("---------",actual_df.show(),'---------------------------------------')
    print("---------",actual_df.count(),'---------------------------------------')
    data = [
        (
            "0703deef-bd79-11ef-8958-0e2033bed3f9",
            "Connect",
            "urn:com.mheducation.openlearning:enterprise.identity:prod.us-east-1:person:ec52b36f-6fdf-42eb-bd43-637c532f9501",
        ),
        (
            "071c3e74-0d2a-11ed-a742-0a3238414663",
            "Simnet",
            "urn:com.mheducation.openlearning:enterprise.identity:prod.us-east-1:person:bb8a42bc-de64-4df8-8735-5222f20d1a90",
        )
    ]

    expected_schema =  StructType(
            [
                StructField("LMS_INSTALLATION_ID",StringType(),nullable=False),
                StructField("TOOL_PROVIDER",StringType(),nullable=False),
                StructField("INSTRUCTOR_XID",StringType(),nullable=False)
            ])
    df_expected = spark.createDataFrame(data, schema= expected_schema)

    assertDataFrameEqual(df_expected,actual_df)

expected_tables = [
        "adhoc_write_qastg.dna_de.lure_orcl_control_table",
        "adhoc_write_qastg.dna_de.lure_orcl_data_bronze"
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

def test_tool_provider(spark):
    actual_df = spark.sql(f"SELECT distinct TOOL_PROVIDER FROM adhoc_write_qastg.dna_de.lure_orcl_data_bronze")
    invalid = actual_df.filter(~col("TOOL_PROVIDER").isin("Connect", "Simnet")    )
    invalid_count = invalid.count()
    assert invalid_count == 0, (
        f"Found {invalid_count} records with invalid status values"
    )

