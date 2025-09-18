import pytest
from scripts.create_data_product import generate_repo_name

class TestGenerateRepoName:
    def test_basic_repo_name(self):
        assert generate_repo_name("tw", "marketing", "customer") == "tw_marketing_customer"
        
    def test_with_spaces(self):
        # Using domain parameter instead of domain_or_team
        assert generate_repo_name("Thoughtworks", "Customer Analytics", "Sales Forecasting") == "thoughtworks_customer_analytics_sales_forecasting"
        
    def test_with_special_chars(self):
        assert generate_repo_name("TW", "Marketing & Sales", "Customer-360") == "tw_marketing_sales_customer_360"
        
    def test_default_org(self):
        assert generate_repo_name("org", "data", "pipeline") == "org_data_pipeline"