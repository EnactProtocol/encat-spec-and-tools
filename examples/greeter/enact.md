---
enact: "2.0.0"
name: "alice/utils/greeter"
description: "Greets the user by name"
command: "echo 'Hello, ${name}!'"
version: "1.0.0"
license: "MIT"
tags: ["example", "simple", "demo"]

inputSchema:
  type: object
  properties:
    name:
      type: string
      description: "Name of the person to greet"
  required: ["name"]

annotations:
  title: "Simple Greeter"
  readOnlyHint: true
  idempotentHint: true
  destructiveHint: false
  openWorldHint: false
---

# Greeter

A simple tool that greets users by name. This is the most basic example of an Enact tool.

## Overview

This tool demonstrates the minimal requirements for an Enact tool definition:
- **YAML frontmatter** with required fields (`name`, `description`, `command`)
- **Markdown body** with human-readable documentation
- **Input schema** defining expected parameters

## Usage

```bash
enact run alice/utils/greeter --args '{"name":"World"}'
# → Hello, World!

enact run alice/utils/greeter --args '{"name":"Alice"}'
# → Hello, Alice!
```

## How It Works

The tool uses a simple shell command with parameter substitution:
```bash
echo 'Hello, ${name}!'
```

The `${name}` placeholder is replaced with the value from the input.

## Structure

This example shows the unified **enact.md** format:
1. **YAML frontmatter** (between `---` delimiters) - Machine-readable metadata
2. **Markdown body** (this section) - Human-readable documentation

Both sections are in the same file, making it easy to maintain and version together.
