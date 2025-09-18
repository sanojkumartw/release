from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp


def transform_raw_orders(df: DataFrame):
    """
    Transformation logic for raw orders ingestion.
    Adds ingestion_date and source_file_name.
    """
    return df.withColumn("ingestion_date", current_timestamp()).withColumn(
        "source_file_name", col("_metadata.file_path")
    )


def filter_returned_orders(df: DataFrame, filter_condition: list[str]) -> DataFrame:
    """
    Return only rows with invalid status values.
    """
    return df.filter(col("status").isin(filter_condition))
