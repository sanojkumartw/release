from pyspark.sql.functions import col
from pyspark.sql.types import StringType, TimestampType

from src.dlt_pipelines.orders.transformations import (
    filter_returned_orders,
    transform_raw_orders,
)


class TestOrdersDLTPipelineIntegration:
    """Integration tests for the complete orders pipeline transformation logic."""

    def test_bronze_layer_raw_orders_creation(self, orders_data_df):
        """Test that bronze layer transformation correctly processes raw orders data."""
        # Act: Apply bronze transformation
        result_df = transform_raw_orders(orders_data_df)

        # Assert: Check that all expected columns are present
        expected_columns = {
            "id",
            "user_id",
            "order_date",
            "status",
            "ingestion_date",
            "source_file_name",
        }
        actual_columns = set(result_df.columns)
        assert expected_columns.issubset(
            actual_columns
        ), f"Missing columns. Expected: {expected_columns}, Got: {actual_columns}"

        # Assert: Check that ingestion_date is populated
        assert (
            result_df.filter(col("ingestion_date").isNotNull()).count()
            == result_df.count()
        )

        # Assert: Check that source_file_name is populated
        assert (
            result_df.filter(col("source_file_name").isNotNull()).count()
            == result_df.count()
        )

        # Assert: Check data types
        assert result_df.schema["ingestion_date"].dataType == TimestampType()
        assert result_df.schema["source_file_name"].dataType == StringType()

    def test_silver_layer_orders_filtering_logic(self, orders_data_df):
        """Test the logic for filtering out returned orders (silver layer logic)."""
        # First apply bronze transformation to get the base data
        bronze_df = transform_raw_orders(orders_data_df)

        # Simulate silver layer filtering by excluding returned orders
        # This tests the business logic without DLT functions
        valid_orders_df = bronze_df.filter(col("status") != "returned")

        # Assert: Check that returned orders are filtered out
        returned_count = valid_orders_df.filter(col("status") == "returned").count()
        assert returned_count == 0, f"Expected 0 returned orders, got {returned_count}"

        # Assert: Check that valid orders remain
        valid_orders = valid_orders_df.filter(~col("status").isin(["returned"]))
        assert valid_orders.count() > 0, "Should have valid orders after filtering"

        # Assert: Check that all expected columns are present
        expected_columns = {
            "id",
            "user_id",
            "order_date",
            "status",
            "ingestion_date",
            "source_file_name",
        }
        actual_columns = set(valid_orders_df.columns)
        assert expected_columns.issubset(actual_columns)

    def test_returned_orders_quarantine_logic(self, orders_data_df):
        """Test the logic for quarantining returned orders."""
        # First apply bronze transformation
        bronze_df = transform_raw_orders(orders_data_df)

        # Simulate returned orders quarantine using the filter function
        returned_df = filter_returned_orders(bronze_df, ["returned"])

        # Assert: Check that only returned orders are present
        returned_count = returned_df.filter(col("status") == "returned").count()
        total_count = returned_df.count()
        assert (
            returned_count == total_count
        ), f"All orders should be returned orders. Got {returned_count}/{total_count}"

        # Assert: Check that returned orders have correct statuses
        statuses = {row["status"] for row in returned_df.collect()}
        assert statuses == {
            "returned"
        }, f"Expected only 'returned' status, got {statuses}"

        # Assert: Check that all expected columns are present
        expected_columns = {
            "id",
            "user_id",
            "order_date",
            "status",
            "ingestion_date",
            "source_file_name",
        }
        actual_columns = set(returned_df.columns)
        assert expected_columns.issubset(actual_columns)

    def test_end_to_end_pipeline_logic(self, orders_data_df):
        """Test the complete pipeline logic flow from raw data to filtered results."""
        # Step 1: Bronze layer - raw ingestion and transformation
        bronze_df = transform_raw_orders(orders_data_df)

        # Step 2: Silver layer - quality filtering (simulate business logic)
        valid_orders_df = bronze_df.filter(col("status") != "returned")
        returned_df = filter_returned_orders(bronze_df, ["returned"])

        # Assert: Bronze layer has all data
        assert bronze_df.count() == orders_data_df.count()

        # Assert: Silver layer has filtered data (no returned orders)
        silver_count = valid_orders_df.count()
        returned_count = returned_df.count()
        total_original = orders_data_df.count()

        assert (
            silver_count + returned_count == total_original
        ), f"Valid orders ({silver_count}) + Returned orders ({returned_count}) should equal original ({total_original})"

        # Assert: No overlap between valid and returned tables
        valid_ids = set(valid_orders_df.select("id").collect())
        returned_ids = set(returned_df.select("id").collect())
        assert (
            len(valid_ids.intersection(returned_ids)) == 0
        ), "No overlap between valid and returned tables"

    def test_pipeline_schema_consistency(self, orders_data_df):
        """Test that schema remains consistent across pipeline transformations."""
        # Get schemas from each transformation step
        bronze_df = transform_raw_orders(orders_data_df)
        valid_orders_df = bronze_df.filter(col("status") != "returned")
        returned_df = filter_returned_orders(bronze_df, ["returned"])

        # Assert: All transformations maintain the same column names
        bronze_columns = set(bronze_df.columns)
        valid_columns = set(valid_orders_df.columns)
        returned_columns = set(returned_df.columns)

        assert (
            bronze_columns == valid_columns
        ), "Bronze and Valid orders should have same columns"
        assert (
            bronze_columns == returned_columns
        ), "Bronze and Returned orders should have same columns"

        # Assert: All transformations maintain the same data types for common columns
        for col_name in ["id", "user_id", "order_date", "status"]:
            assert (
                bronze_df.schema[col_name].dataType
                == valid_orders_df.schema[col_name].dataType
            ), f"Data type mismatch for column {col_name}"
            assert (
                bronze_df.schema[col_name].dataType
                == returned_df.schema[col_name].dataType
            ), f"Data type mismatch for column {col_name}"
