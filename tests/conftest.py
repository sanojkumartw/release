import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder.master("local[1]")  # Single thread for testing
        .appName("pytest-pyspark")
        .getOrCreate()
    )
    yield spark
    spark.stop()
