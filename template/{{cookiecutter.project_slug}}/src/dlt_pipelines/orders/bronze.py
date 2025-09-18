import dlt
from transformations import transform_raw_orders

# Default to bucket name; path is constructed in code
RAW_DATA_DEFAULT_BUCKET = "databricks-dev-external-ext-str-raw-data-eu-central-1"


# 🔹 Step 1: Read raw CSV as strings (schema-on-read with inferSchema disabled)
@dlt.table(
    name="sch_bronze.raw_orders",
    comment="Bronze layer raw ingestion of orders CSV with ingestion_date",
    table_properties={"quality": "bronze"},
)
def load_raw_orders():
    # Read S3 bucket from pipeline configuration with a default
    raw_bucket_path = spark.conf.get("raw.bucket", RAW_DATA_DEFAULT_BUCKET)
    raw_data_path = f"s3://{raw_bucket_path}/sources/orders/"

    # Read CSV with all columns as STRING (no schema inference)
    df = (
        spark.read.option("header", "true")
        .option("inferSchema", "false")  # forces all as string
        .csv(raw_data_path)
    )

    return transform_raw_orders(df)
