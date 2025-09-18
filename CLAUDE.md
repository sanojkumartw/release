# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with the Data Products Accelerator Template repository.

## Repository Overview

This is the **tw-data-products-accelerator-template** repository containing a Cookiecutter template for bootstrapping new data products on Databricks.

## Template Structure

The template generates projects with this structure:
```
project/
├── src/main.py          # Python ETL logic
├── notebooks/           # Databricks notebooks
├── jobs/job.json        # Databricks job definitions
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Key Components

### Cookiecutter Configuration
- **cookiecutter.json**: Template variables and default values
- **{{cookiecutter.project_slug}}/**: Template directory structure

### Generated Project Features
- **ETL Pipeline**: Python-based data processing logic in `src/main.py`
- **Databricks Notebooks**: Interactive data analysis notebooks
- **Job Configuration**: Databricks job definitions for production deployment
- **Dependencies**: Python package management via requirements.txt

### Backstage Integration
- **backstage-github-template.yaml**: Software catalog integration for Backstage

## Common Development Commands

### Template Usage with Cruft

```bash
# Create new project from template using Cruft
cruft create https://github.com/DATA-AI-Service-Line/tw-data-products-accelerator-template

# Check for template updates in existing project
cruft check

# Apply template updates to existing project
cruft update
```

### Local Template Development

```bash
# Test template generation locally
cookiecutter .

# Generate project with specific values
cookiecutter . project_name="My Data Product" project_slug="my-data-product"
```

## Template Variables

Available Cookiecutter variables (defined in cookiecutter.json):
- **project_name**: Human-readable project name
- **project_slug**: Machine-readable project identifier
- **project_description**: Brief project description
- **author_name**: Project author/maintainer
- **author_email**: Contact email

## Generated Project Workflow

Once a project is generated from this template:

1. **Setup**: Install dependencies from requirements.txt
2. **Development**: Implement ETL logic in src/main.py
3. **Testing**: Use notebooks for interactive development
4. **Deployment**: Deploy jobs using jobs/job.json configuration

## Key Dependencies

- **Cookiecutter**: Template engine for project scaffolding
- **Cruft**: Template version management and updates
- **Databricks SDK**: Integration with Databricks platform

## Development Workflow

1. **Template Updates**: Modify template files in {{cookiecutter.project_slug}}/
2. **Variable Configuration**: Update cookiecutter.json with new template variables
3. **Testing**: Generate test projects to validate template changes
4. **Documentation**: Update README and template documentation
5. **Release**: Tag new versions for Cruft-managed updates

## Best Practices

- Keep template minimal but functional out-of-the-box
- Provide sensible defaults in cookiecutter.json
- Include comprehensive README in generated projects
- Test template generation with various input values
- Maintain backwards compatibility for existing projects using Cruft
- always use uv to run tests