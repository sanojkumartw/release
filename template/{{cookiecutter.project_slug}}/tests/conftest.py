import os

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit


@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder.master("local[1]")  # Single thread for testing
        .appName("pytest-pyspark")
        .getOrCreate()
    )
    yield spark
    spark.stop()


@pytest.fixture
def orders_data_df(spark):
    orders_data_path = os.path.join(os.path.dirname(__file__), "../data/orders.csv")
    orders_df = (
        spark.read.option("header", "true")
        .option("inferSchema", "false")
        .csv(orders_data_path)
        .withColumn("_metadata.file_path", lit("s3://dummy/orders/orders.csv"))
    )

    return orders_df
