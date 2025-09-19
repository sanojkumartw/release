git init# Data as a Product (DAAP) Template

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Template](https://img.shields.io/badge/template-cookiecutter-orange.svg)](https://cookiecutter.readthedocs.io/)

A production-ready template for scaffolding standardized Databricks pipeline projects using [Cookiecutter](https://cookiecutter.readthedocs.io/) and [Cruft](https://cruft.github.io/cruft/). This template enables teams to **generate**, **version**, and **upgrade** their data pipeline projects consistently over time.

## 🚀 What's Inside the Template

This repository provides a reusable, versioned template that generates:

- **Standardized Project Structure**: Consistent folder organization for Databricks projects
- **DLT Pipeline Templates**: Ready-to-use Delta Live Tables pipeline notebooks
- **Job & Workflow Definitions**: Pre-configured Databricks job specifications
- **Cluster Configurations**: Optimized cluster settings for data processing
- **Testing Framework**: Built-in testing utilities and configurations
- **Build & Deployment**: Makefile and pyproject.toml for project management
- **CI/CD Pipelines**: GitHub Actions workflows for automated deployment

## 🚀 GitHub Actions CI/CD

This template provides GitHub Actions workflows at two levels:

### 🚀 **Template-Level Workflow (Main Repository)**

The main DAAP-TEMPLATE repository includes a **Bootstrap New Data Product** workflow that automates the entire data product creation process:

#### **What It Does:**
- **Automated Scaffolding**: Uses Cruft to generate new projects from this template
- **Repository Creation**: Automatically creates new GitHub repositories
- **Configuration Setup**: Pre-configures Databricks secrets and variables
- **Initial Commit**: Sets up the new repository with generated code

#### **How to Use:**
1. **Navigate to Actions**: Go to the Actions tab in this repository
2. **Select "Bootstrap New Data Product from Template"**
3. **Fill Required Inputs:**
   - `repo_name`: New repository name (e.g., `daap-customer-dwh`)
   - `org_name`: GitHub organization name
   - `description`: Repository description
   - `project_name`: Project display name
   - `project_slug`: Project slug for folder structure
   - `author_name`: Author or team name
   - `template_repo_branch`: Template branch to use (default: `main`)
4. **Run Workflow**: Click "Run workflow" to start automation

#### **What Gets Created:**
- New private GitHub repository
- Complete project structure from template
- Pre-configured Databricks environment variables
- Initial commit with all generated files
- Ready-to-use data pipeline project

#### **Prerequisites:**
- `GH_TOKEN` secret with repository creation permissions
- `DATABRICKS_CLIENT_ID` secret configured
- `DATABRICKS_HOST_VAR` and `SERVICE_PRINCIPAL_ID_VAR` variables set

### 🔧 **Generated Project Workflows**

Once you create a project using the template, it will include these GitHub Actions workflows:

#### **Built-in Workflows**
- **Deploy Pipeline**: Automated deployment to dev/prod environments
- **Destroy Pipeline**: Safe cleanup of Databricks resources
- **Security**: GitHub OIDC authentication with Databricks
- **Validation**: Automatic bundle validation before deployment

#### **Security Features**
- **OIDC Federation**: Secure authentication without long-lived secrets
- **Environment Control**: Separate dev/prod deployment targets
- **Branch Protection**: Workflows only run from authorized branches
- **Service Principal**: Role-based access control with Databricks

#### **Setup Requirements**
- Databricks service principal with OIDC federation policy
- GitHub repository secrets and variables configuration
- Databricks workspace access and permissions

#### **Benefits**
- **Automated Deployments**: Consistent, repeatable deployment process
- **Team Collaboration**: Centralized deployment management
- **Audit Trails**: Complete deployment history and logs
- **Security**: Production-grade authentication and authorization

## 📋 Prerequisites

- **Python 3.12+**
- **uv package manager** (recommended) or pip
- **Git** for version control
- **Databricks workspace access**
- **Access to this private repository**

## ⚡ Quick Start

```bash
# Install uv and tools
curl -LsSf https://astral.sh/uv/install.sh | sh
uv add cookiecutter cruft

# Generate your project (ensure you have access to the repo)
cruft create --checkout main --directory template <your-private-repo-url>
```

## 🛠️ Installation & Usage

### Step 1: Install uv Package Manager

Install `uv`, a fast Python package and project manager:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Step 2: Install Required Tools

```bash
unv env
uv sync
```

Installs the pre-commit tool, which automatically runs checks (linting, formatting, security scans) before each commit.
```bash
pre-commit install
pre-commit autoupdate
```

### Step 3: Generate Your Project

```bash
cruft create --checkout main --directory template <your-private-repo-url>
```

During project generation, you'll be prompted for:
- **Project Name**: Human-readable project name
- **Project Slug**: URL-friendly identifier (e.g., `my-data-pipeline`)
- **Author Name**: Your name or team name

## 📁 Template Project Structure

```
daap-template/
├── .github/                        # Template-level GitHub Actions workflows
│   └── workflows/
│       └── bootstrap-repo.yml      # Bootstrap new project workflow
├── backstage-github-template.yaml  # Backstage template configuration
├── Makefile                        # Template build and management commands
├── pyproject.toml                  # Template project configuration
├── README.md                       # This template documentation
├── uv.lock                         # Dependency lock file
└── template/                       # Cookiecutter template directory
    ├── cookiecutter.json           # Template configuration and prompts
    └── {{cookiecutter.project_slug}}/  # Generated project structure
        ├── .github/                # Generated project GitHub Actions workflows
        ├── .gitignore              # Git ignore patterns
        ├── databricks.yml          # Databricks Asset Bundle configuration
        ├── Makefile                # Development and deployment commands
        ├── pyproject.toml          # Python project configuration
        ├── README.md               # Generated project documentation
        ├── resources/              # Databricks resources (clusters, workflows)
        ├── src/                    # Source code (notebooks, Python modules)
        └── tests/                  # Test suite
```

## 🔄 Keeping Your Project Up-to-Date

When the template receives updates (bugfixes, new features, structural improvements), you can upgrade existing projects without losing your customizations.

### Check for Updates

Navigate to your project folder (where `.cruft.json` resides) and run:

```bash
cruft check --checkout main
```

### Apply Updates

```bash
cruft update --checkout main
```

Cruft will intelligently merge template changes with your customizations, prompting for conflicts when necessary.

## 🎯 Key Features

- **Version Control**: Track template source and version with `.cruft.json`
- **Conflict Resolution**: Smart merging of template updates with local changes
- **Standardization**: Consistent project structure across teams
- **Databricks Integration**: Pre-configured for Databricks workflows
- **Testing Ready**: Built-in testing framework and utilities

## 🤝 Internal Development

For internal team members contributing to this template:

1. Ensure you have proper access to the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request for review

## 📄 License

This is an internal template for organizational use.

## 🆘 Support

- **Documentation**: [Cookiecutter Docs](https://cookiecutter.readthedocs.io/)
- **Cruft Documentation**: [Cruft Docs](https://cruft.github.io/cruft/)
- **Internal Support**: Contact your team lead or data engineering team

**Internal Template for Data Engineering Team**

# test file
# release-test ok
