#!/usr/bin/env python
"""
Build script for dify-utils package.
This script helps with building and publishing the package.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return its output."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout

def clean_build_files():
    """Clean build files."""
    print("Cleaning build files...")
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for dir_pattern in dirs_to_clean:
        for path in Path(".").glob(dir_pattern):
            if path.is_dir():
                run_command(["rm", "-rf", str(path)])

def build_package():
    """Build the package."""
    print("Building package...")
    run_command([sys.executable, "-m", "pip", "install", "build"])
    run_command([sys.executable, "-m", "build"])

def run_tests():
    """Run tests."""
    print("Running tests...")
    run_command([sys.executable, "-m", "pytest"])

def publish_to_pypi():
    """Publish the package to PyPI."""
    print("Publishing to PyPI...")
    run_command([sys.executable, "-m", "pip", "install", "twine"])
    run_command([sys.executable, "-m", "twine", "upload", "dist/*"])

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python build.py [clean|build|test|publish|all]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "clean":
        clean_build_files()
    elif command == "build":
        build_package()
    elif command == "test":
        run_tests()
    elif command == "publish":
        publish_to_pypi()
    elif command == "all":
        clean_build_files()
        build_package()
        run_tests()
        publish_to_pypi()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main() 