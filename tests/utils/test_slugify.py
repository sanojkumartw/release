import pytest
from scripts.utils.slugify import slugify

class TestSlugify:
    def test_basic_slugify(self):
        assert slugify("Customer Analytics") == "customer_analytics"
        
    def test_special_characters(self):
        assert slugify("Sales & Marketing Dashboard") == "sales_marketing_dashboard"
        
    def test_multiple_spaces(self):
        assert slugify("Data   Product   Name") == "data_product_name"
        
    def test_leading_trailing_spaces(self):
        assert slugify("  Customer Portal  ") == "customer_portal"
        
    def test_mixed_case(self):
        assert slugify("MyDataProduct") == "mydataproduct"
        
    def test_numbers(self):
        assert slugify("Product 2024 v3") == "product_2024_v3"
