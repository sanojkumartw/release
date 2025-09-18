from pyspark.sql import DataFrame


def count_matching_rows(df: DataFrame, column: str, value: str) -> int:
    """
    Counts the number of rows where column == value.
    """
    return df.filter(df[column] == value).count()
