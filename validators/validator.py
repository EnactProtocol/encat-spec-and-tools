#!/usr/bin/env python3
"""
Enact Capability Validator

This script validates Enact capability files against the official schema.
It can be used as part of CI/CD pipelines or locally by contributors.
"""

import argparse
import json
import os
import sys
from pathlib import Path
import yaml
import jsonschema
from typing import Dict, List, Any, Optional, Tuple

# ANSI colors for terminal output
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"


def load_schema(schema_path: str) -> Dict[str, Any]:
    """Load the Enact capability schema from file."""
    try:
        with open(schema_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"{RED}Error loading schema: {e}{RESET}")
        sys.exit(1)


def load_capability(capability_path: str) -> Dict[str, Any]:
    """Load a capability YAML file."""
    try:
        with open(capability_path, "r") as f:
            return yaml.safe_load(f)
    except (yaml.YAMLError, FileNotFoundError) as e:
        print(f"{RED}Error loading capability file {capability_path}: {e}{RESET}")
        return None


def validate_capability(capability: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validate a capability against the schema."""
    try:
        jsonschema.validate(instance=capability, schema=schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)


def find_capabilities(directory: str) -> List[str]:
    """Find all capability.yaml files in the given directory and subdirectories."""
    capability_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "capability.yaml":
                capability_files.append(os.path.join(root, file))
    return capability_files


def perform_additional_checks(capability: Dict[str, Any], capability_path: str) -> List[str]:
    """Perform additional validation checks beyond schema validation."""
    warnings = []

    # Check that README.md exists in the same directory
    directory = os.path.dirname(capability_path)
    if not os.path.exists(os.path.join(directory, "README.md")):
        warnings.append(f"Missing README.md in {directory}")

    # Check type-specific requirements
    capability_type = capability.get("type")

    if capability_type == "workflow":
        # For workflows, check that run is an array
        if not isinstance(capability.get("run"), list):
            warnings.append(
                "Workflow capabilities should have 'run' as an array of steps")

    # Check that run is present
    if "run" not in capability:
        warnings.append("Missing 'run' field in capability")

    # For Python/JavaScript capabilities, check that a main function is defined
    if capability_type in ["python", "javascript"]:
        run_content = capability.get("run", "")
        if isinstance(run_content, str):
            if capability_type == "python" and "def main" not in run_content:
                warnings.append(
                    "Python capabilities should define a 'main' function")
            elif capability_type == "javascript" and "function main" not in run_content and "const main =" not in run_content:
                warnings.append(
                    "JavaScript capabilities should define a 'main' function")

    return warnings


def validate_all_capabilities(schema_path: str, capabilities_dir: str, verbose: bool = False) -> bool:
    """Validate all capabilities in the specified directory."""
    schema = load_schema(schema_path)
    capability_files = find_capabilities(capabilities_dir)

    if not capability_files:
        print(f"{YELLOW}No capability files found in {capabilities_dir}{RESET}")
        return False

    print(f"{BLUE}Found {len(capability_files)} capability files to validate{RESET}")

    all_valid = True
    validation_results = []

    for capability_path in capability_files:
        capability = load_capability(capability_path)
        if capability is None:
            all_valid = False
            validation_results.append(
                (capability_path, False, "Failed to load capability file", []))
            continue

        valid, error = validate_capability(capability, schema)
        warnings = perform_additional_checks(
            capability, capability_path) if valid else []

        validation_results.append((capability_path, valid, error, warnings))

        if not valid:
            all_valid = False

    # Print results
    for path, valid, error, warnings in validation_results:
        relative_path = os.path.relpath(path)
        if valid:
            if not warnings:
                if verbose:
                    print(f"{GREEN}✓ {relative_path}{RESET}")
            else:
                print(f"{YELLOW}⚠ {relative_path} (warnings){RESET}")
                for warning in warnings:
                    print(f"  {YELLOW}- {warning}{RESET}")
        else:
            print(f"{RED}✗ {relative_path}{RESET}")
            print(f"  {RED}Error: {error}{RESET}")

    # Summary
    valid_count = sum(1 for _, valid, _, _ in validation_results if valid)
    warning_count = sum(1 for _, valid, _,
                        warnings in validation_results if valid and warnings)
    invalid_count = sum(1 for _, valid, _,
                        _ in validation_results if not valid)

    print(f"\n{BLUE}Validation Summary:{RESET}")
    print(f"  {GREEN}Valid: {valid_count}{RESET}")
    print(f"  {YELLOW}Valid with warnings: {warning_count}{RESET}")
    print(f"  {RED}Invalid: {invalid_count}{RESET}")

    return all_valid


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Validate Enact capability files against the schema")
    parser.add_argument("--schema", default="schema/enact-capability-schema.json",
                        help="Path to the Enact capability schema file")
    parser.add_argument("--capabilities", default="capabilities",
                        help="Directory containing capability files to validate")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output (show all valid capabilities)")
    parser.add_argument("--file", "-f",
                        help="Validate a single capability file instead of a directory")

    args = parser.parse_args()

    if args.file:
        # Validate a single file
        schema = load_schema(args.schema)
        capability = load_capability(args.file)
        if capability is None:
            return 1

        valid, error = validate_capability(capability, schema)
        if valid:
            warnings = perform_additional_checks(capability, args.file)
            if warnings:
                print(f"{YELLOW}⚠ {args.file} (warnings){RESET}")
                for warning in warnings:
                    print(f"  {YELLOW}- {warning}{RESET}")
            else:
                print(f"{GREEN}✓ {args.file} is valid{RESET}")
            return 0
        else:
            print(f"{RED}✗ {args.file} is invalid{RESET}")
            print(f"  {RED}Error: {error}{RESET}")
            return 1
    else:
        # Validate all capabilities in directory
        success = validate_all_capabilities(
            args.schema, args.capabilities, args.verbose)
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
