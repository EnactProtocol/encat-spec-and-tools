# Enact CLI Commands Reference

This document provides a comprehensive overview of all available commands in the Enact CLI tool.

## Overview

Enact CLI manages containerized tools with cryptographic signing. It supports local development in `~/.enact/local/` and automatic caching of registry tools in `~/.enact/cache/`.

## Global Options

- `--help, -h` - Show help message
- `--version, -v` - Show version information
- `--verbose` - Show detailed execution information

## Core Commands

### 1. run - Run Tool's Declared Command

**Purpose**: Execute a tool's canonical, signed command.

**Usage**: `enact run <tool-name> --args '<json>'`

**Arguments**:
- `tool-name` - Tool identifier (e.g., "myorg/utils/hello")
- `--args` - JSON object with tool parameters

**Options**:
- `--timeout <duration>` - Override tool timeout (e.g., 30s, 5m)
- `--dry-run` - Show what would execute without running
- `--verbose` - Show detailed execution info

**Behavior**:
- If tool has `command` field → executes in container with declared command
- If tool has no `command` field → errors with: "Tool has no command field. Use 'enact get' to read instructions or 'enact exec' to run custom commands."

**Resolution order**: Project `.enact/` → `~/.enact/tools/` (user-level) → `~/.enact/cache/` → download from registry

**Examples**:
```bash
# Run local tool
enact run myorg/utils/hello --args '{"name":"Alice"}'

# Run from cache or download
enact run kgroves88/ai/pdf-extract --args '{"pdf_path":"doc.pdf","pages":[1,2]}'

# Dry run to see what would execute
enact run myorg/data/processor --args '{"file":"data.csv"}' --dry-run
```

---

### 2. exec - Execute Arbitrary Command in Tool's Environment

**Purpose**: Run custom commands inside a tool's containerized environment.

**Usage**: `enact exec <tool-name> "<command>"`

**Arguments**:
- `tool-name` - Tool identifier (e.g., "myorg/utils/hello")
- `command` - Shell command to execute inside the container

**Options**:
- `--timeout <duration>` - Override tool timeout (e.g., 30s, 5m)
- `--verbose` - Show detailed execution info

**Behavior**:
- Runs the provided command inside the tool's container (defined by `from:` field)
- Same isolation and security guarantees as `run`
- Not signed or deterministic — useful for experimentation, debugging, or one-off tasks

**Resolution order**: Project `.enact/` → `~/.enact/tools/` (user-level) → `~/.enact/cache/` → download from registry

**Examples**:
```bash
# Run custom Python script in tool's environment
enact exec acme-corp/data/processor "python scripts/validate.py data.csv"

# Execute shell commands for debugging
enact exec myorg/utils/analyzer "ls -la && cat config.json"

# Run one-off data transformation
enact exec kgroves88/ai/pdf-extract "python extract.py --file=doc.pdf --pages=1-5"
```

---

### 3. install - Install Tool

**Purpose**: Install tools to project or globally (like npm).

**Usage**: `enact install [tool-name] [options]`

**Arguments**:
- `tool-name` - Tool identifier from registry, current directory (`.`), or omit for batch install

**Options**:
- `--global, -g` - Install to `~/.enact/tools/` for user-level access (like npm -g)

**Behavior**:

**Project-level (default):**
- `enact install <tool-name>` → Adds to `./.enact/tools.json`, downloads to cache, extracts to `./.enact/{tool}/`
- `enact install` → Installs all tools from `./.enact/tools.json`
- `enact install .` → Installs current directory to `./.enact/`

**User-level (--global):**
- `enact install <tool-name> --global` → Downloads to cache, extracts to `~/.enact/tools/`
- `enact install . --global` → Packages, caches, and installs current directory to `~/.enact/tools/`

**Resolution order**: `./.enact/` (project) → `~/.enact/tools/` (user-level) → `~/.enact/cache/` (temporarily hydrates)

**Examples**:
```bash
# Install tool for current project (like npm install <package>)
enact install acme-corp/data/csv-processor
# Adds to ./.enact/tools.json
# Downloads to ~/.enact/cache/acme-corp/data/csv-processor/v1.0.0/
# Extracts to ./.enact/acme-corp/data/csv-processor/

# Install all project tools (like npm install)
enact install
# Reads ./.enact/tools.json and installs all listed tools

# Install tool at user-level (like npm install -g <package>)
enact install acme-corp/data/csv-processor --global
# Downloads to ~/.enact/cache/acme-corp/data/csv-processor/v1.0.0/
# Extracts to ~/.enact/tools/acme-corp/data/csv-processor/

# Install current directory at user-level (like npm install -g .)
cd my-tool/
enact install . --global
# Packages and caches to ~/.enact/cache/myorg/category/my-tool/v1.0.0/
# Installs to ~/.enact/tools/myorg/category/my-tool/

# Install current directory to project
cd my-tool/
enact install .
# Packages and installs to ./.enact/myorg/category/my-tool/
```

**Project tools.json** (`./.enact/tools.json`):
```json
{
  "tools": {
    "acme-corp/data/csv-processor": "^1.0.0",
    "myorg/utils/formatter": "latest"
  }
}
```

---

### 4. search - Discover Tools

**Purpose**: Search registry for tools using tags and descriptions.

**Usage**: `enact search <query> [options]`

**Arguments**:
- `query` - Search keywords (matches tags, descriptions, names)

**Options**:
- `--tags <tags>` - Filter by tags (comma-separated)
- `--limit <n>` - Max results (default: 20)
- `--json` - Output as JSON

**Examples**:
```bash
enact search "pdf extraction"
enact search --tags csv,data --limit 10
enact search formatter --json
```

---

### 5. validate - Validate Tool

**Purpose**: Validate tool definition before publishing.

**Usage**: `enact validate [path]`

**Arguments**:
- `path` - Path to tool directory (default: current directory)

**Checks**:
- Protocol version compatibility
- Required fields present
- Name format valid
- Tags present for discovery
- Schema validity
- File references exist

**Examples**:
```bash
enact validate                    # Validate current directory
enact validate ./my-tool/         # Validate specific directory
```

---

### 6. sign - Sign Tool

**Purpose**: Cryptographically sign a tool for publishing.

**Usage**: `enact sign <path> [options]`

**Arguments**:
- `path` - Path to tool directory

**Options**:
- `--identity <email>` - Sign with specific identity (uses OAuth)

**Process**:
1. Authenticates via OAuth (GitHub, Google, etc.)
2. Generates ephemeral keypair
3. Requests certificate from Fulcio
4. Creates signature
5. Logs to Rekor transparency log
6. Creates signature bundle

**Examples**:
```bash
enact sign ./my-tool/
enact sign ./my-tool/ --identity=me@example.com
```

---

### 7. publish - Publish Tool

**Purpose**: Publish signed tool to registry.

**Usage**: `enact publish <path> [options]`

**Arguments**:
- `path` - Path to tool directory (must be signed)

**Requirements**:
- Tool must be validated
- Tool must be signed
- Must be authenticated

**Examples**:
```bash
# Complete publishing workflow
enact validate ./my-tool/
enact sign ./my-tool/
enact publish ./my-tool/
```

---

### 8. get - Get Tool Info

**Purpose**: Retrieve tool metadata and instructions (works for all tools).

**Usage**: `enact get <tool-name> [options]`

**Arguments**:
- `tool-name` - Tool identifier

**Options**:
- `--format <format>` - Output format: yaml, json, md (default: yaml)

**Returns**:
- Tool metadata (name, description, tags)
- Full instructions from enact.md
- Input/output schemas
- Whether tool is executable (has `command` field)

**Examples**:
```bash
# Get executable tool info
enact get kgroves88/ai/pdf-extract

# Get instruction-only tool
enact get acme-corp/workflows/data-pipeline

# Output as JSON
enact get acme-corp/data/processor --format json

# Output as markdown (shows full instructions)
enact get acme-corp/workflows/data-pipeline --format md
```

---

### 9. verify - Verify Tool

**Purpose**: Verify cryptographic signature and authenticity.

**Usage**: `enact verify <tool-name>`

**Arguments**:
- `tool-name` - Tool identifier from registry

**Verification includes**:
- Tarball hash matches signature
- Signature valid
- Certificate chain valid
- Rekor transparency log entry
- Certificate not revoked

**Examples**:
```bash
enact verify kgroves88/ai/pdf-extract
```

---

## Environment & Configuration

### 10. env - Environment Variables

**Purpose**: Manage package-scoped environment variables for tool execution.

**Usage**: `enact env <subcommand> [options]`

**Subcommands**:
- `set <key> <value>` - Set variable for package
- `get <key>` - Get variable value
- `list` - List all variables for package
- `delete <key>` - Delete variable

**Options**:
- `--package <package>` - Package identifier (e.g., "acme-corp/api")

**Storage**: `~/.enact/env/<org>/<path>/.env`

**Examples**:
```bash
enact env set API_KEY secret123 --package acme-corp/api
enact env get API_KEY --package acme-corp/api
enact env list --package acme-corp/api
enact env delete API_KEY --package acme-corp/api
```

---

### 11. config - Configuration

**Purpose**: Manage CLI configuration.

**Usage**: `enact config <subcommand> [options]`

**Subcommands**:
- `set <key> <value>` - Set configuration value
- `get <key>` - Get configuration value
- `list` - List all configuration
- `reset` - Reset to defaults

**Common settings**:
- `registry.url` - Registry URL (default: https://enact.dev)
- `cache.dir` - Cache directory (default: ~/.enact/cache)
- `tools.dir` - User-level tools directory (default: ~/.enact/tools)

**Examples**:
```bash
enact config set registry.url https://my-registry.com
enact config get registry.url
enact config list
```

---

## Utility Commands

### 12. cache - Cache Management

**Purpose**: Manage downloaded tool cache.

**Usage**: `enact cache <subcommand>`

**Subcommands**:
- `list` - List cached tools
- `clean` - Remove unused cached tools
- `clear` - Remove all cached tools
- `info` - Show cache statistics

**Examples**:
```bash
enact cache list
enact cache clean              # Remove tools not used in 30 days
enact cache clear              # Remove all cached tools
enact cache info               # Show cache size and stats
```

---

### 13. list - List Tools

**Purpose**: List installed local and cached tools.

**Usage**: `enact list [options]`

**Options**:
- `--user` - Show only user-level tools (from ~/.enact/tools)
- `--project` - Show only project-level tools (from ./.enact)
- `--cache` - Show only cached tools
- `--json` - Output as JSON

**Examples**:
```bash
enact list                     # Show all tools
enact list --user              # Show only user-level tools
enact list --project           # Show only project tools
enact list --cache             # Show only cached tools
```

---

## Authentication

### 14. auth - Authentication

**Purpose**: Manage authentication for publishing and private registries.

**Usage**: `enact auth <subcommand>`

**Subcommands**:
- `login` - Authenticate via OAuth
- `logout` - Remove credentials
- `status` - Show authentication status

**Examples**:
```bash
enact auth login
enact auth status
enact auth logout
```

---

## Quick Workflows

### User-Level Tool Development
```bash
# 1. Create tool in project directory
cd my-tool-project

# 2. Create enact.md
cat > enact.md <<'EOF'
---
enact: "1.0.0"
name: "myorg/utils/my-tool"
description: "My tool"
tags: ["utility"]
command: "echo 'Hello ${name}!'"
---

# My Tool

Simple greeting tool.
EOF

# 3. Test locally first (no install needed)
enact run . --args '{"name":"World"}'

# 4. Install at user-level when ready
enact install . --global
# Packages to ~/.enact/cache/myorg/utils/my-tool/v1.0.0/
# Installs to ~/.enact/tools/myorg/utils/my-tool/

# 5. Test the installed version
enact run myorg/utils/my-tool --args '{"name":"World"}'
```

### Publishing Workflow
```bash
# 1. Validate
enact validate ./my-tool/

# 2. Sign
enact sign ./my-tool/

# 3. Publish
enact publish ./my-tool/
```

### Project Tool Setup
```bash
# 1. Initialize project with tools
cd my-project

# 2. Install tools for project
enact install acme-corp/data/csv-processor
enact install myorg/utils/formatter
# Creates ./.enact/tools.json

# 3. Team members clone and install
git clone https://github.com/myorg/my-project
cd my-project
enact install
# Reads ./.enact/tools.json and installs all tools

# 4. Use project tools
enact run acme-corp/data/csv-processor --args '{"file":"data.csv"}'
```

### Installing & Using
```bash
# 1. Search
enact search "pdf extraction"

# 2. Get info
enact get kgroves88/ai/pdf-extract

# 3. Install and execute
enact install kgroves88/ai/pdf-extract
enact run kgroves88/ai/pdf-extract --args '{"pdf_path":"doc.pdf"}'
```

### Customizing Registry Tool
```bash
# 1. Install at user-level for editing
enact install acme-corp/brand/reviewer --global

# 2. Customize
cd ~/.enact/tools/acme-corp/brand/reviewer/
vim VOICE_GUIDE.md

# 3. Use your customized version (user-level tools take priority)
enact run acme-corp/brand/reviewer --args '{"content":"test"}'
```

---

## Directory Structure

```
my-project/                   # Project directory
├── .enact/
│   ├── tools.json           # Project tools manifest (commit to git)
│   └── {org}/{path}/{tool}/ # Project-local tool installations
└── ...

~/.enact/
├── tools/                   # Active user-level tools (installed with --global)
│   └── {org}/
│       └── {path}/
│           └── {tool}/
│               ├── enact.md
│               ├── src/
│               └── node_modules/
├── cache/                   # Immutable versioned bundles (auto-managed)
│   └── {org}/
│       └── {path}/
│           └── {tool}/
│               └── v1.0.0/
│                   ├── bundle.tar.gz
│                   ├── .sigstore-bundle
│                   └── metadata.json
├── env/                     # Environment variables
│   └── {org}/{path}/.env
└── config.json              # CLI configuration
```

---

## Configuration Files

### ~/.enact/config.json
```json
{
  "registry": {
    "url": "https://enact.dev"
  },
  "cache": {
    "dir": "~/.enact/cache",
    "maxSize": "10GB"
  },
  "tools": {
    "dir": "~/.enact/tools"
  }
}
```

### Tool Resolution

When executing a tool, Enact searches in this order:

1. **Project tools** (`./.enact/`) - Tools installed for current project
2. **User-level tools** (`~/.enact/tools/`) - Tools installed with `--global`
3. **Cache** (`~/.enact/cache/`) - Temporarily hydrates if cached but not installed
4. **Registry** - Download, verify signature, cache, execute

---

## Exit Codes

- `0` - Success
- `1` - General error
- `2` - Validation error
- `3` - Authentication error
- `4` - Network error
- `5` - Signature verification failed
- `6` - Tool not found

---

## Environment Variables

- `ENACT_REGISTRY_URL` - Override registry URL
- `ENACT_CACHE_DIR` - Override cache directory
- `ENACT_TOOLS_DIR` - Override user-level tools directory
- `ENACT_DEBUG` - Enable debug logging

---

## Security Notes

1. **User-level tools** (`~/.enact/tools/`) skip signature verification (user-controlled workspace)
2. **Cached tools** are verified on download from registry
3. **Signature verification** happens automatically during download
4. **Environment variables** are scoped to tool namespaces
5. Use `enact verify` to independently verify any cached tool

---

## Common Patterns

| Task | Command |
|------|---------|
| Install tool for project | `enact install org/cat/tool` |
| Install all project tools | `enact install` (reads ./.enact/tools.json) |
| Install tool globally | `enact install org/cat/tool --global` |
| Install current dir globally | `enact install . --global` |
| Run tool | `enact run org/cat/tool --args '{...}'` |
| Run custom command | `enact exec org/cat/tool "command"` |
| Find tools | `enact search "keyword"` |
| Customize registry tool | `enact install org/cat/tool --global` then edit |
| Publish tool | `enact validate && enact sign && enact publish` |
| Verify tool | `enact verify org/cat/tool` |
| Clean cache | `enact cache clean` |
