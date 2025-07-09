#!/usr/bin/env python3
"""
Enact Tool Validator

This script validates Enact tool files against the official schema.
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
import re

# ANSI colors for terminal output
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"


def load_schema(schema_path: str) -> Dict[str, Any]:
    """Load the Enact tool schema from file."""
    try:
        with open(schema_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"{RED}Error loading schema: {e}{RESET}")
        sys.exit(1)


def load_tool(tool_path: str) -> Dict[str, Any]:
    """Load a tool YAML file."""
    try:
        with open(tool_path, "r") as f:
            return yaml.safe_load(f)
    except (yaml.YAMLError, FileNotFoundError) as e:
        print(f"{RED}Error loading tool file {tool_path}: {e}{RESET}")
        return None


def validate_tool(tool: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validate a tool against the schema."""
    try:
        jsonschema.validate(instance=tool, schema=schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)


def find_tools(directory: str) -> List[str]:
    """Find all YAML tool files in the given directory and subdirectories."""
    tool_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                tool_files.append(os.path.join(root, file))
    return tool_files


def validate_tool_name(name: str) -> List[str]:
    """Validate tool name follows hierarchical naming convention."""
    warnings = []
    
    if not name:
        warnings.append("Tool name is required")
        return warnings
    
    # Check for proper hierarchical naming (e.g., "company/category/tool-name")
    if "/" not in name:
        warnings.append("Tool name should use hierarchical naming (e.g., 'company/category/tool-name')")
    
    # Check for valid characters
    if not re.match(r'^[a-zA-Z0-9/_-]+$', name):
        warnings.append("Tool name should only contain alphanumeric characters, hyphens, underscores, and forward slashes")
    
    # Check for consecutive slashes
    if "//" in name:
        warnings.append("Tool name should not contain consecutive slashes")
    
    # Check for leading/trailing slashes
    if name.startswith("/") or name.endswith("/"):
        warnings.append("Tool name should not start or end with a slash")
    
    return warnings


def validate_command_versioning(command: str) -> List[str]:
    """Check if command uses proper versioning."""
    warnings = []
    
    # Check for potentially unversioned commands first
    unversioned_patterns = [
        (r'npx\s+(\w+)(?!@)', 'npx without version'),
        (r'uvx\s+(\w+)(?!@)', 'uvx without version'),
        (r'pip\s+install\s+(\w+)(?![=<>])', 'pip without version'),
    ]
    
    for pattern, desc in unversioned_patterns:
        if re.search(pattern, command):
            warnings.append(f"Consider pinning versions in command: {desc}")
    
    return warnings


def validate_timeout_format(timeout: str) -> List[str]:
    """Validate timeout format (Go duration)."""
    warnings = []
    
    if not timeout:
        return warnings
    
    # Check for valid Go duration format
    if not re.match(r'^\d+[smh]$', timeout):
        warnings.append("Timeout should be in Go duration format (e.g., '30s', '5m', '1h')")
    
    return warnings


def validate_license_format(license_str: str) -> List[str]:
    """Validate license format."""
    warnings = []
    
    if not license_str:
        warnings.append("Consider adding a license field (SPDX identifier like 'MIT', 'Apache-2.0')")
        return warnings
    
    # Common SPDX identifiers
    common_licenses = [
        'MIT', 'Apache-2.0', 'GPL-3.0', 'GPL-2.0', 'BSD-3-Clause', 
        'BSD-2-Clause', 'ISC', 'MPL-2.0', 'LGPL-3.0', 'LGPL-2.1'
    ]
    
    if license_str not in common_licenses:
        warnings.append(f"License '{license_str}' might not be a standard SPDX identifier")
    
    return warnings


def validate_container_image(from_image: str) -> List[str]:
    """Validate container image format."""
    warnings = []
    
    if not from_image:
        return warnings
    
    # Check for 'latest' tag
    if ':latest' in from_image or from_image.endswith(':latest'):
        warnings.append("Avoid using 'latest' tag, prefer specific versions for reproducibility")
    
    # Check if no tag is specified (implies latest)
    if ':' not in from_image:
        warnings.append("Consider specifying a specific image tag for reproducibility")
    
    # Suggest minimal images
    if 'ubuntu' in from_image or 'centos' in from_image:
        warnings.append("Consider using minimal images like 'alpine' or 'slim' variants for better performance")
    
    return warnings


def perform_additional_checks(tool: Dict[str, Any], tool_path: str) -> List[str]:
    """Perform additional validation checks beyond schema validation."""
    warnings = []
    
    # Validate tool name
    name = tool.get("name", "")
    warnings.extend(validate_tool_name(name))
    
    # Validate command versioning
    command = tool.get("command", "")
    warnings.extend(validate_command_versioning(command))
    
    # Validate timeout format
    timeout = tool.get("timeout", "")
    warnings.extend(validate_timeout_format(timeout))
    
    # Validate license
    license_str = tool.get("license", "")
    warnings.extend(validate_license_format(license_str))
    
    # Validate container image
    from_image = tool.get("from", "")
    warnings.extend(validate_container_image(from_image))
    
    # Check for input/output schemas
    if "inputSchema" not in tool:
        warnings.append("Consider adding inputSchema to help AI models use the tool correctly")
    
    if "outputSchema" not in tool:
        warnings.append("Consider adding outputSchema to help AI models understand the output")
    
    # Check for tags
    if "tags" not in tool or not tool.get("tags"):
        warnings.append("Consider adding tags to improve tool discoverability")
    
    # Check for signatures
    signatures = tool.get("signatures", [])
    if signatures:
        if not isinstance(signatures, list):
            warnings.append("Signatures should be an array of signature objects")
        else:
            for i, sig in enumerate(signatures):
                if not isinstance(sig, dict):
                    warnings.append(f"Signature {i} should be an object")
                    continue
                
                required_sig_fields = ["signer", "algorithm", "type", "value", "created"]
                for field in required_sig_fields:
                    if field not in sig:
                        warnings.append(f"Signature {i} missing required field: {field}")
                
                # Check timestamp format
                if "created" in sig:
                    try:
                        # Basic ISO timestamp validation
                        from datetime import datetime
                        datetime.fromisoformat(sig["created"].replace("Z", "+00:00"))
                    except ValueError:
                        warnings.append(f"Signature {i} has invalid timestamp format")
    
    # Check for authors
    authors = tool.get("authors", [])
    if authors:
        if not isinstance(authors, list):
            warnings.append("Authors should be an array of author objects")
        else:
            for i, author in enumerate(authors):
                if not isinstance(author, dict):
                    warnings.append(f"Author {i} should be an object")
                elif "name" not in author:
                    warnings.append(f"Author {i} missing required field: name")
    
    # Check for examples
    examples = tool.get("examples", [])
    if examples:
        if not isinstance(examples, list):
            warnings.append("Examples should be an array of example objects")
        else:
            for i, example in enumerate(examples):
                if not isinstance(example, dict):
                    warnings.append(f"Example {i} should be an object")
                elif "input" not in example:
                    warnings.append(f"Example {i} missing required field: input")
    
    # Check for environment variables without descriptions
    env_vars = tool.get("env", {})
    for var_name, var_config in env_vars.items():
        if isinstance(var_config, dict):
            if "description" not in var_config:
                warnings.append(f"Environment variable '{var_name}' missing description")
            if "required" not in var_config:
                warnings.append(f"Environment variable '{var_name}' missing required field")
    
    # Check for README.md in the same directory
    directory = os.path.dirname(tool_path)
    if not os.path.exists(os.path.join(directory, "README.md")):
        warnings.append(f"Consider adding README.md in {directory}")
    
    return warnings


def validate_all_tools(schema_path: str, tools_dir: str, verbose: bool = False) -> bool:
    """Validate all tools in the specified directory."""
    schema = load_schema(schema_path)
    tool_files = find_tools(tools_dir)

    if not tool_files:
        print(f"{YELLOW}No tool files found in {tools_dir}{RESET}")
        return False

    print(f"{BLUE}Found {len(tool_files)} tool files to validate{RESET}")

    all_valid = True
    validation_results = []

    for tool_path in tool_files:
        tool = load_tool(tool_path)
        if tool is None:
            all_valid = False
            validation_results.append(
                (tool_path, False, "Failed to load tool file", []))
            continue

        valid, error = validate_tool(tool, schema)
        warnings = perform_additional_checks(tool, tool_path) if valid else []

        validation_results.append((tool_path, valid, error, warnings))

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
        description="Validate Enact tool files against the schema")
    parser.add_argument("--schema", default="schema/enact-schema.json",
                        help="Path to the Enact tool schema file")
    parser.add_argument("--tools", default="tools",
                        help="Directory containing tool files to validate")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output (show all valid tools)")
    parser.add_argument("--file", "-f",
                        help="Validate a single tool file instead of a directory")

    args = parser.parse_args()

    if args.file:
        # Validate a single file
        schema = load_schema(args.schema)
        tool = load_tool(args.file)
        if tool is None:
            return 1

        valid, error = validate_tool(tool, schema)
        if valid:
            warnings = perform_additional_checks(tool, args.file)
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
        # Validate all tools in directory
        success = validate_all_tools(args.schema, args.tools, args.verbose)
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
