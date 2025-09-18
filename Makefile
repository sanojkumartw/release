# Makefile for DAAP Template Repository
# Provides commands for local development and testing of the template
# This Makefile supports both local development and GitHub Actions workflows

.PHONY: help install validate-template create-template-locally info

# Default target - shows available commands
help:
	@echo "=========================================="
	@echo "DAAP Template Development Commands"
	@echo "=========================================="
	@echo ""
	@echo "Development Commands:"
	@echo "  install                    - Install Python dependencies using uv"
	@echo "  validate-template          - Validate template structure and files"
	@echo "  info                       - Show template information and structure"
	@echo ""
	@echo "Template Creation Commands:"
	@echo "  create-template-locally   - Create test project locally for development"
	@echo ""
	@echo "Usage Examples:"
	@echo "  make install              		# Install dependencies"
	@echo "  make create-template-locally   # Test template locally"
	@echo "  make validate-template    		# Validate template structure"

# Install Python dependencies using uv package manager
install:
	@echo "=========================================="
	@echo "Installing Python Dependencies"
	@echo "=========================================="
	@echo "Using uv package manager to sync dependencies..."

	uv sync

	@echo "✅ Dependencies installed successfully!"

# Validate template structure and required files
# Ensures all necessary template files exist before use
validate-template:
	@echo "=========================================="
	@echo "Validating Template Structure"
	@echo "=========================================="
	@echo "Checking required template files exist..."
	@echo "✓ Checking cookiecutter.json..."
	@test -f template/cookiecutter.json || (echo "❌ ERROR: cookiecutter.json not found" && exit 1)
	@echo "✓ Checking pyproject.toml..."
	@test -f template/{{cookiecutter.project_slug}}/pyproject.toml || (echo "❌ ERROR: pyproject.toml not found" && exit 1)
	@echo "✓ Checking databricks.yml..."
	@test -f template/{{cookiecutter.project_slug}}/databricks.yml || (echo "❌ ERROR: databricks.yml not found" && exit 1)
	@echo "✓ Checking Makefile..."
	@test -f template/{{cookiecutter.project_slug}}/Makefile || (echo "❌ ERROR: Makefile not found" && exit 1)
	@echo "=========================================="
	@echo "✅ Template structure validation passed!"
	@echo "All required files are present and valid"

# Create a test project locally for development and testing
# This creates a sample project outside the main directory for testing
create-template-locally:
	@echo "=========================================="
	@echo "Creating Local Test Project"
	@echo "=========================================="
	@echo "Creating test project in '../test-daap-template' directory..."
	@echo "This will generate a sample project for development testing"
	@echo "Project: Sample Sales Project (daap-sales)"
	@echo "Author: Data Team"

	rm -rf ../test-tw-databricks-dataproduct

	uv run create-data-product \
		"Sample Data Product" \
		--domain "Sample Domain" \
		--description "A sample Databricks dataproduct generated with the TW Databricks data product accelerator template" \
		--org "Sample org" \
		--output-dir ../test-tw-databricks-dataproduct

	@echo "✅ Local test project created successfully!"
	@echo "📁 Location: ../test-daap-template/daap-sales"



# Display template information and usage instructions
info:
	@echo "=========================================="
	@echo "Template Information"
	@echo "=========================================="
	@echo "📁 Template Directory: template/"
	@echo "⚙️  Cookiecutter Config: template/cookiecutter.json"
	@echo "📦 Sample Project: template/{{cookiecutter.project_slug}}/"
	@echo ""
	@echo "🔧 Available Commands:"
	@echo "  make help                    	# Show this help message"
	@echo "  make install                 	# Install dependencies"
	@echo "  make validate-template       	# Validate template structure"
	@echo "  make create-template-locally 	# Test template locally"
	@echo ""
	@echo "🚀 To test locally: make create-template-locally"
	@echo "📋 To see all commands: make help"
