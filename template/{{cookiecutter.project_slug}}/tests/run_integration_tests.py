#!/usr/bin/env python3
"""
Script to run integration tests for the orders pipeline using uv.
This script sets up the test environment and runs all integration tests.
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    """Run the integration tests using uv."""
    print("🚀 Starting Orders Pipeline Integration Tests with uv...")

    # Get project paths
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print(f"📁 Project root: {project_root}")
    print(f"📁 Working directory: {os.getcwd()}")

    # Run integration tests using uv
    test_command = [
        "uv",
        "run",
        "pytest",
        "tests/integration/",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--strict-markers",  # Strict marker checking
        "--disable-warnings",  # Disable warnings for cleaner output
        "--color=yes",  # Colored output
    ]

    print(f"🧪 Running tests with command: {' '.join(test_command)}")

    try:
        # Run the tests using uv
        result = subprocess.run(test_command, check=False)

        if result.returncode == 0:
            print("✅ All integration tests passed!")
        else:
            print(
                f"❌ Some integration tests failed with exit code: {result.returncode}"
            )

        return result.returncode

    except FileNotFoundError:
        print(
            "❌ Error: 'uv' command not found. Please ensure uv is installed and in your PATH."
        )
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
