# Makefile for {{ cookiecutter.project_slug }} project
# Provides convenient commands for local development and deployment


.PHONY: help install build validate validate-verbose deploy-dev deploy-prod destroy-dev destroy-prod clean test lint format

# Default target
help:
	@echo "Available commands:"
	@echo "  install      		- Install project dependencies using uv"
	@echo "  build        		- Build the Python wheel package"
	@echo "  validate     		- Validate the Databricks Asset bundle"
	@echo "  validate-verbose   - Validate the Databricks Asset bundle"
	@echo "  deploy-dev   		- Deploy to development environment"
	@echo "  deploy-prod  		- Deploy to production environment"
	@echo "  destroy-dev  		- Destroy development environment"
	@echo "  destroy-prod 		- Destroy production environment"
	@echo "  clean        		- Clean build artifacts and cache"
	@echo "  test         		- Run all tests using pytest"
	@echo "  test-unit    		- Run unit tests only"
	@echo "  test-integration   - Run integration tests only"
	@echo "  lint         		- Run linting checks"
	@echo "  format       		- Format code using black"

# Install dependencies
install:
	@echo "Installing dependencies..."
	uv sync

# Build the Python wheel package
build:
	@echo "Building Python wheel package..."
	uv build --wheel

# Validate the Databricks Asset bundle
validate:
	@echo "Validating Databricks Asset bundle..."
	databricks bundle validate

# Validate the Databricks Asset bundle
validate-verbose:
	@echo "Validating Databricks Asset bundle..."
	 databricks bundle validate --output json

# Deploy to development environment
deploy-dev:
	@echo "Deploying to development environment..."
	databricks bundle deploy --auto-approve --target dev

# Deploy to production environment
deploy-prod:
	@echo "Deploying to production environment..."
	@read -p "Are you sure you want to deploy to PRODUCTION? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	databricks bundle deploy --auto-approve --target prod

# Destroy development environment
destroy-dev:
	@echo "Destroying development environment..."
	@read -p "Are you sure you want to destroy the DEV environment? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	databricks bundle destroy --auto-approve --target dev

# Destroy production environment
destroy-prod:
	@echo "Destroying production environment..."
	@read -p "Are you sure you want to destroy the PRODUCTION environment? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	databricks bundle destroy --auto-approve --target prod

# Clean build artifacts and cache
clean:
	@echo "Cleaning build artifacts and cache..."
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run tests
test:
	@echo "Running tests..."
	uv run pytest tests/ -v

# Run integration tests
test-integration:
	@echo "Running integration tests..."
	uv run pytest tests/integration/ -v

# Run unit tests only
test-unit:
	@echo "Running unit tests..."
	uv run pytest tests/unit/ -v

# Run linting checks
lint:
	@echo "Running linting checks..."
	uv run ruff check src/ tests/

# Format code
format:
	@echo "Formatting code..."
	uv run black src/ tests/
	uv run isort src/ tests/

# Quick development workflow: install, build, validate
dev-setup: install build validate

# Quick deployment workflow: validate and deploy to dev
quick-deploy: validate deploy-dev

# Show bundle status
status:
	@echo "Checking bundle status..."
	databricks bundle run --target dev