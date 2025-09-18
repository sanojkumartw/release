# Project: {{ cookiecutter.project_name }}

A Databricks Data as a Product (DAAP) project generated with the DAAP Template. This project provides a standardized structure for building and deploying data pipelines on Databricks.

## 🚀 Quick Start

```bash
# Install dependencies
make install

# Validate the project
make validate

# Deploy to development
make deploy-dev
```

## 🔐 Environment Setup

### For Local/Manual Execution

When running commands locally or manually, you need to export the following environment variables:

```bash
# Databricks workspace host
export DATABRICKS_HOST="your-databricks-workspace-url"

# Databricks Asset Bundle variable
export BUNDLE_VAR_SERVICE_PRINCIPAL_ID="your-service-principal-application-id / UUID"

# Databricks authentication (only needed for local execution)
export DATABRICKS_CLIENT_ID="your-client-id"
export DATABRICKS_CLIENT_SECRET="your-client-secret"
```

**Note**: Replace the placeholder values with your actual Databricks service principal and client credentials. These are only required for local authentication and deployment.

### For GitHub Actions (OIDC Authentication)

GitHub Actions workflows use OpenID Connect (OIDC) for secure authentication with Databricks, eliminating the need to store long-lived secrets. See the [GitHub Actions CI/CD](#-github-actions-cicd) section below for OIDC setup instructions.

## 🚀 GitHub Actions CI/CD

This project includes GitHub Actions workflows for automated deployment and destruction of Databricks resources. The workflows use GitHub OIDC for secure authentication with Databricks.

### Available Workflows

#### 1. Deploy Pipeline (`deploy_data_pipeline.yml`)
Automatically deploys your Databricks Asset Bundle to the specified environment.

**Trigger**: Manual workflow dispatch
**Inputs**:
- `target_environment`: Choose between `dev` or `prod`

**Steps**:
- Validates the Databricks Asset Bundle
- Deploys to the selected environment
- Uses GitHub OIDC for secure authentication

#### 2. Destroy Pipeline (`destroy_data_pipeline.yml`)
Safely destroys Databricks resources in the specified environment.

**Trigger**: Manual workflow dispatch
**Inputs**:
- `target_environment`: Choose between `dev` or `prod`

**Steps**:
- Destroys resources in the selected environment
- Uses GitHub OIDC for secure authentication

### How to Use GitHub Actions

#### Prerequisites
1. **Repository Secrets**: Set `DATABRICKS_CLIENT_ID` in your repository secrets
2. **Repository Variables**: Set the following variables:
   - `DATABRICKS_HOST_VAR`: Your Databricks workspace URL
   - `SERVICE_PRINCIPAL_ID_VAR`: Your Databricks service principal ID

3. **OIDC Federation Policy**: Create the service principal federation policy in Databricks:

```bash
databricks account service-principal-federation-policy create <your-service-principal-id> --json '{
  "oidc_policy": {
    "issuer": "https://token.actions.githubusercontent.com",
    "audiences": [
        "https://github.com/my-org"
    ],
    "subject": "repo:my-github-org/my-repo:ref:refs/heads/main"
  }
}'
```

**Note**: Replace the following values with your actual configuration:
- `<your-service-principal-id>`: Your Databricks service principal ID (Application ID / UUID)
- `my-org`: Your GitHub organization name
- `my-repo`: Your repository name
- `main`: Your branch name (e.g., `main`, `develop`, `feature-branch`)

**OIDC Subject Format**: The subject `repo:my-github-org/my-repo:ref:refs/heads/main` provides:
- **Repository Access**: Controls access to specific GitHub repository
- **Branch Restriction**: Restricts access to specific branch (`main` in this example)
- **Security**: Ensures workflows only run from authorized branches

#### Running Workflows

1. **Navigate to Actions**: Go to your repository's Actions tab
2. **Select Workflow**: Choose either "Deploy pipeline to Databricks" or "Destroy pipeline on Databricks"
3. **Run Workflow**: Click "Run workflow" button
4. **Select Environment**: Choose `dev` or `prod` from the dropdown
5. **Execute**: Click "Run workflow" to start the process

#### Security Features
- **GitHub OIDC**: Secure authentication without storing long-lived secrets
- **Environment Selection**: Manual approval for production deployments
- **Validation**: Automatic bundle validation before deployment

### Local vs. GitHub Actions

| Task | Local Command | GitHub Actions |
|------|---------------|----------------|
| Deploy to Dev | `make deploy-dev` | Manual workflow dispatch |
| Deploy to Prod | `make deploy-prod` | Manual workflow dispatch |
| Destroy Dev | `make destroy-dev` | Manual workflow dispatch |
| Destroy Prod | `make destroy-prod` | Manual workflow dispatch |

**Use GitHub Actions for**:
- Production deployments
- Team collaboration
- Audit trails
- Consistent deployment environments

**Use Local Commands for**:
- Development and testing
- Quick iterations
- Local debugging

## 📁 Project Structure

```
{{ cookiecutter.project_slug }}/
├── .github/               # GitHub Actions workflows
│   └── workflows/
│       ├── deploy_data_pipeline.yml    # Deploy pipeline workflow
│       └── destroy_data_pipeline.yml   # Destroy pipeline workflow
├── .gitignore             # Git ignore patterns
├── databricks.yml         # Databricks Asset Bundle configuration
├── Makefile               # Development and deployment commands
├── pyproject.toml         # Python project configuration and dependencies
├── README.md              # This file
├── resources/             # Databricks resources
│   ├── clusters/          # Cluster configurations
│   │   └── cluster.yml    # Cluster specifications
│   └── workflows/         # Job and pipeline definitions
│       ├── job.yml        # Job configurations with pipeline orchestration
│       └── orders_pipeline.yml   # Orders ETL pipeline specifications
├── src/                   # Source code
│   ├── __init__.py        # Package initialization
│   ├── data_product_spec_reg.py # Data product specification registration
│   ├── dlt_pipelines/     # DLT pipeline implementations
│   │   └── orders/        # Orders data pipeline
│   │       ├── bronze.ipynb # Bronze layer processing
│   │       └── silver.ipynb # Silver layer processing
│   ├── main.py            # Main pipeline entry point
│   ├── notebook.ipynb     # General notebook template
│   └── utils.py           # Utility functions
└── tests/                 # Test suite
    ├── conftest.py        # Test configuration
    └── test_utils.py      # Utility tests
```

## 🛠️ Development Commands

The project includes a comprehensive Makefile with common development tasks:

### Setup & Dependencies
```bash
make install          # Install project dependencies using uv
make build            # Build Python wheel package
```

### Validation & Testing
```bash
make validate         # Validate Databricks Asset Bundle
make validate-verbose # Validate with detailed JSON output
make test             # Run tests using pytest
make lint             # Run linting checks with ruff
make format           # Format code with black and isort
```

### Deployment
```bash
make deploy-dev       # Deploy to development environment
make deploy-prod      # Deploy to production environment (with confirmation)
make destroy-dev      # Destroy development environment
make destroy-prod     # Destroy production environment
```

### Utilities
```bash
make clean            # Clean build artifacts and cache
make help             # Show all available commands
make dev-setup        # Quick setup: install, build, validate
make quick-deploy     # Quick deployment: validate and deploy to dev
```

## 🔧 Configuration

### Python Dependencies
The project uses `uv` for dependency management with the following key packages:
- **PySpark 3.5.0** - Apache Spark Python API
- **pytest 8.4.1** - Testing framework
- **ruff 0.12.8** - Fast Python linter
- **black 25.1.0** - Code formatter
- **isort 6.0.1** - Import sorting

### Databricks Configuration
- **Development Target**: `dev` - Creates development copies with paused schedules
- **Production Target**: `prod` - Production deployment with proper tagging
- **Artifacts**: Python wheel packages with dynamic versioning
- **Permissions**: Service principal-based access control

## 📊 Databricks Resources

### Clusters
Cluster configurations are defined in `resources/clusters/cluster.yml` and can be customized for your specific compute requirements.

### Workflows
Job and pipeline definitions are in `resources/workflows/`:
- **`job.yml`**: Main job configuration that orchestrates the ETL pipeline execution
- **`orders_pipeline.yml`**: Orders ETL pipeline configuration using Delta Live Tables with bronze and silver layer processing

### Notebooks
- **`dlt_pipelines/orders/bronze.ipynb`**: Bronze layer processing for raw orders data ingestion
- **`dlt_pipelines/orders/silver.ipynb`**: Silver layer processing for cleaned and transformed orders data
- **`notebook.ipynb`**: General notebook template for ad-hoc analysis and development

### Python Modules
- **`main.py`**: Main entry point for programmatic pipeline execution and orchestration
- **`data_product_spec_reg.py`**: Data product specification registration, metadata management, and schema definitions
- **`utils.py`**: Common utility functions and helper methods for pipeline operations

## 🚀 Deployment

### Development Environment
```bash
make deploy-dev
```
- Creates development copies of resources
- Pauses job schedules and triggers
- Uses development mode for safe testing

### Production Environment
```bash
make deploy-prod
```
- Deploys to production with confirmation prompt
- Applies production tags and configurations
- Uses production mode for live workloads

### Validation
Always validate before deployment:
```bash
make validate
```

## 🧪 Testing

Run the test suite:
```bash
make test
```

The project includes:
- **pytest** configuration in `pyproject.toml`
- **Test utilities** in `tests/test_utils.py`
- **Test configuration** in `tests/conftest.py`

## 📝 Code Quality

### Linting
```bash
make lint
```
Uses ruff for fast Python linting with custom rules for PySpark development.

### Formatting
```bash
make format
```
Automatically formats code using black and sorts imports with isort.

## 🔍 Troubleshooting

### Common Issues

1. **Validation Errors**: Run `make validate-verbose` for detailed error information
2. **Deployment Failures**: Check Databricks workspace access and service principal permissions
3. **Build Issues**: Ensure Python 3.11+ and run `make clean` before rebuilding

### Getting Help

- Check the [Databricks Asset Bundle documentation](https://docs.databricks.com/dev-tools/bundles/index.html)
- Review the Makefile for available commands
- Validate your configuration with `make validate`

## 📚 Next Steps

1. **Customize Resources**: Modify cluster and workflow configurations in `resources/`
2. **Implement Pipeline Logic**: Update the bronze and silver notebooks in `src/dlt_pipelines/orders/` with your data processing logic
3. **Configure Pipeline**: Adjust the pipeline settings in `resources/workflows/orders_pipeline.yml` for your data sources
4. **Add Tests**: Extend the test suite in `tests/`
5. **Configure Environments**: Update `databricks.yml` with your workspace URLs and settings

---

**Generated with the DAAP Template - Data as a Product Accelerator**

