#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path

from scripts.utils.slugify import slugify


def generate_repo_name(org: str, domain: str, data_product_name: str) -> str:
    org_slug = slugify(org)
    domain_slug = slugify(domain)
    product_slug = slugify(data_product_name)
    return f"{org_slug}_{domain_slug}_{product_slug}"


def create_data_product(
    data_product_name: str,
    domain: str = "data",
    org: str = "org",
    description: str = None,
    output_dir: str = "./",
    template_path: str = "./",
    checkout: str = "main",
):
    project_slug = slugify(data_product_name)
    repo_name = generate_repo_name(org, domain, data_product_name)

    context = {
        "project_name": data_product_name,
        "project_slug": project_slug,
        "domain": domain,
        "description": description,
        "author_name": domain,
        "python_version": "3.12",
    }

    print(f"Creating data product: {data_product_name}")
    print(f"  Project slug: {project_slug}")
    print(f"  Repository name: {repo_name}")
    print(f"  Organization: {org}")
    print(f"  Domain/Team: {domain}")

    cmd = [
        "cruft",
        "create",
        str(template_path),
        "--directory",
        "template",  # Specify the template subdirectory
        "--no-input",
        "--output-dir",
        output_dir,
        "--checkout",
        checkout,
        "--extra-context",
        json.dumps(context),
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ Data product created successfully at: {output_dir}/{project_slug}")
        return project_slug, repo_name
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating data product: {e}")
        if e.stderr:
            print(e.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Create a new data product from template"
    )
    parser.add_argument("data_product_name", help="Name of the data product")
    parser.add_argument(
        "--domain", default="data", help="Domain or team owning the data product"
    )
    parser.add_argument("--org", default="org", help="Organization name")
    parser.add_argument("--description", help="Data product description")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    parser.add_argument("--template-path", default=".", help="Template path")
    parser.add_argument(
        "--checkout", default="main", help="Template checkout reference"
    )
    args = parser.parse_args()

    project_slug, repo_name = create_data_product(
        args.data_product_name,
        args.domain,
        args.org,
        args.description,
        args.output_dir,
        args.template_path,
        args.checkout,
    )

    print(f"project_slug={project_slug}")
    print(f"repo_name={repo_name}")


if __name__ == "__main__":
    main()
