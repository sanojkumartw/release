import dlt
from transformations import filter_returned_orders


@dlt.table(
    name="sch_silver.orders", comment="Silver orders table with enforced quality rules"
)
@dlt.expect_or_drop("valid_status", "status NOT IN ('returned')")
def orders():
    return dlt.read("raw_orders")


@dlt.table(
    name="sch_silver.returned_orders",
    comment="Returned orders quarantined from silver validation",
)
def returned_orders():
    raw_orders_df = dlt.read("raw_orders")
    filter_condition = ["returned"]
    return filter_returned_orders(raw_orders_df, filter_condition)
