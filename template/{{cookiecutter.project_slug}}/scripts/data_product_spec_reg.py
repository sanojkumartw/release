#!/usr/bin/env python3

import json

import yaml
from databricks.sdk import WorkspaceClient


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.

    :param file_path: Path to the YAML file
    :return: Dictionary containing the YAML content
    """
    with open(file_path) as f:
        data = yaml.safe_load(f)  # safe_load prevents arbitrary code execution
    return data


def read_json_file(file_path: str) -> dict:
    """
    Reads a JSON file and returns its content as a dictionary.

    :param file_path: Path to the JSON file
    :return: Dictionary containing the JSON content
    """
    with open(file_path) as f:
        data = json.load(f)
    return data


def main():
    # Authenticate using env vars: DATABRICKS_HOST + DATABRICKS_TOKEN
    w = WorkspaceClient()

    # Read YAML file
    yaml_data = read_yaml_file("data-product.odps.sample.yaml")
    print("YAML Data:", yaml_data)

    # Extract metadata
    product_id = yaml_data.get("id")
    status = yaml_data.get("status")

    # Read JSON file
    json_data = read_json_file("data-product.odps.sample.json")
    print("JSON Data:", json_data)

    # Target catalog + schema
    catalog_name = json_data["catalog_name"]
    schema_name = json_data["schema_name"]
    print(f"Parsed YAML → id: {product_id}, status: {status}")

    # Ensure schema exists (create if not)
    try:
        w.schemas.get(full_name=f"{catalog_name}.{schema_name}")
        print(f"Schema '{catalog_name}.{schema_name}' already exists")
    except Exception:
        w.schemas.create(
            catalog_name=catalog_name,
            name=schema_name,
            comment=f"Schema {schema_name} creating for catalog {catalog_name}",
        )
        print(f"Schema '{catalog_name}.{schema_name}' created")

    # Attach metadata as schema properties
    properties = {"data_product_id": product_id, "status": status}

    w.schemas.update(full_name=f"{catalog_name}.{schema_name}", properties=properties)

    print(f"Stored metadata into schema {catalog_name}.{schema_name}: {properties}")


if __name__ == "__main__":
    main()
