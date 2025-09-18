from src.utils import count_matching_rows


def test_count_matching_rows(spark):
    # Sample Data
    data = [("Alice", "HR"), ("Bob", "IT"), ("Charlie", "IT"), ("David", "HR")]
    columns = ["name", "department"]
    df = spark.createDataFrame(data, columns)

    # Test
    result = count_matching_rows(df, "department", "IT")

    # Assert
    assert result == 2
