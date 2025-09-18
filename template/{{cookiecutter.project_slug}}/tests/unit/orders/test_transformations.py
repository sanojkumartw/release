from src.dlt_pipelines.orders.transformations import (
    filter_returned_orders,
    transform_raw_orders,
)


def test_transform_raw_orders(orders_data_df):
    # Act: apply transformation
    result_df = transform_raw_orders(orders_data_df)

    # Assert: columns exist
    cols = result_df.columns
    assert "id" in cols
    assert "user_id" in cols
    assert "order_date" in cols
    assert "status" in cols
    assert "ingestion_date" in cols
    assert "source_file_name" in cols


def test_orders_bronze_columns_are_string(orders_data_df):
    # Act: apply transformation
    result_df = transform_raw_orders(orders_data_df)

    # Get column types
    col_types = dict(result_df.dtypes)

    # Assert: ingestion_date is timestamp
    assert col_types["ingestion_date"] == "timestamp"

    # Assert: all other original columns are string
    for col in ["id", "user_id", "order_date", "status", "source_file_name"]:
        assert col_types[col] == "string", f"Column {col} should be string"


def test_filter_returned_orders(orders_data_df):
    filter_condition = ["returned"]
    result_df = filter_returned_orders(orders_data_df, filter_condition)

    # Assert: only bad statuses remain
    statuses = {row["status"] for row in result_df.collect()}
    assert statuses == {"returned"}
