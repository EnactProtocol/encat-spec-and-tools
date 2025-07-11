# Enact Protocol

![Status: Alpha](https://img.shields.io/badge/Status-Alpha-yellow) ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) [![Discord](https://img.shields.io/badge/Discord-Enact_PROTOCOL-blue?logo=discord&logoColor=white)](https://discord.gg/mMfxvMtHyS)

**Turn any command-line tool into an AI tool with simple YAML.**

## What is Enact?

Enact lets AI models safely discover and execute command-line tools. Instead of writing complex integrations, you define tools with simple YAML:

```yaml
name: hello-world
description: "Greets the world"
command: "echo 'Hello, ${name}!'"
```

That's it. This tool can now be:
- 🔍 **Discovered** by AI models searching for "greeting"
- 🚀 **Executed** safely without local installation  
- 🔐 **Verified** with cryptographic signatures
- 📌 **Versioned** with semantic versioning

## Quick Start

**Install:**
```bash
npm install -g @enactprotocol/cli
```

**Create your first tool:**
```bash
enact init my-tool
enact publish tool.yaml
```

Now any AI using MCP can discover and use your tool!

## Core Concepts

### Minimal Tool (3 lines)
```yaml
enact: "1.0.0"
name: enact/text/analyzer
description: "Analyzes text statistics"
command: "npx text-stats@1.0.0 '${text}'"
```

### Production Tool (with validation)
```yaml
enact: "1.0.0"
name: enact/markdown/converter
description: "Converts markdown to HTML"
from: "node:18-alpine"
command: "npx markdown-it@14.0.0 '${input}'"
timeout: "30s"
license: "MIT"

inputSchema:
  type: object
  properties:
    input:
      type: string
      description: "Markdown content"
  required: ["input"]
```

### Hierarchical Naming
Tools use filepath-style names for organization:
- `enact/text/analyzer` - Official text tools
- `acme-corp/internal/processor` - Company tools  
- `username/personal/utility` - Personal tools

## Key Features

### Universal Command Support
Any shell command works:
```yaml
# NPX with versions (recommended)
command: "npx prettier@3.3.3 --write '${file}'"

# Python tools with UVX
command: "uvx black@24.4.2 '${file}'"

# Docker containers
command: "docker run pandoc/core:3.1.11 -f markdown -t html"

# API calls
command: "curl -s 'https://api.example.com/v1/process' -d '${json}'"

# With container image specification
from: "node:18-alpine"
command: "npx prettier@3.3.3 --write '${file}'"

# Python environment
from: "python:3.11-slim"
command: "python -m pip install requests && python -c 'import requests; print(requests.get(\"${url}\").text)'"
```

### Multi-Signature Security
Tools can be signed by multiple parties:
```yaml
signatures:
  - signer: "71e02e2c-148c-4534-9900-bd9646e99333"
    algorithm: "sha256"
    type: "ecdsa-p256"
    value: "drwaN6pjbV24JeGOPmQhe8mgQTD1f9LZ4qRsKAV5/8jODTzTbcyToQ36lt9uv06S0Y60IdchR/40WLtAUc3Bdg=="
    created: "2025-07-08T18:42:15.501+00:00"
    role: "author"
  - signer: "security-team"
    algorithm: "sha256"
    type: "ecdsa-p256"
    value: "MEUCIDxNLAzYZQAul2/uhPkdjxNrNwkFWy2qYOGV5pWIpdabAiEB..."
    created: "2025-07-08T20:30:00.000+00:00"
    role: "reviewer"
```

### Shared Environment Variables
Tools in the same package share API keys and secrets:
```yaml
name: "acme-corp/discord/bot-maker"

env:
  DISCORD_API_KEY:
    description: "Discord bot API key"
    source: "https://discord.com/developers → Bot → Token"
    required: true
```

All Discord tools (`discord/webhook`, `discord/bot-manager`) share the same credentials stored in `~/.enact/env/acme-corp/discord/.env`.

### Container Image Specification
Specify the container image for command execution:
```yaml
name: "acme-corp/python/data-processor"
from: "python:3.11-slim"
command: "python -m pip install pandas numpy && python process.py '${data}'"

# Or use custom images
from: "ghcr.io/company/custom-env:v2.1.0"
command: "analyze-data '${input}'"

# Default behavior (no from field)
command: "echo 'Hello World'"  # Runs on system shell
```

The `from` field provides:
- **Reproducible environments** - Same runtime across different systems
- **Dependency isolation** - Tools don't interfere with each other
- **Version control** - Pin exact image versions for consistency
- **Security** - Run tools in isolated containers

### Behavior Annotations
Help AI models understand tool safety:
```yaml
enact: "1.0.0"
annotations:
  readOnlyHint: true      # Safe, no system changes
  destructiveHint: false  # Won't break anything  
  openWorldHint: true     # Connects to internet
  idempotentHint: true    # Multiple calls = same result
```

## How Enact Extends MCP

| Feature | MCP | Enact |
|---------|-----|-------|
| Tool Communication | ✅ | ✅ Uses MCP |
| Tool Execution | ❌ | ✅ Command-based |
| Tool Discovery | ❌ | ✅ Semantic search |
| Versioning | ❌ | ✅ Semantic versions |
| Security | ❌ | ✅ Crypto signatures |

## CLI Commands

```bash
# Tool lifecycle
enact init my-tool              # Create new tool
enact validate tool.yaml        # Validate definition
enact test tool.yaml            # Test locally
enact sign tool.yaml            # Add signature
enact publish tool.yaml         # Publish to registry

# Discovery
enact search "text analysis"    # Find tools
enact verify tool.yaml          # Check signatures
```

### Dagger-Powered Containerized Execution

While the Enact protocol is implementation-agnostic, the reference CLI uses [Dagger](https://dagger.io) for secure containerized execution:

```yaml
# When you specify a container image
from: "python:3.11-slim"
command: "uvx black@24.4.2 '${file}'"
```

**Behind the scenes:**
1. **Dagger pipeline** creates an isolated container from the specified image
2. **Code execution** happens entirely within the container boundary
3. **File system isolation** prevents tools from accessing host system
4. **Network policies** can be applied per-tool for additional security
5. **Resource limits** are enforced at the container level

**Security benefits:**
- ✅ **Zero host access** - Tools can't modify your system
- ✅ **Dependency isolation** - No version conflicts between tools
- ✅ **Reproducible environments** - Same runtime across all machines
- ✅ **Resource containment** - Memory/CPU limits prevent resource exhaustion
- ✅ **Audit trail** - All execution happens in logged, traceable containers

**Why Dagger specifically:**
- **Programmable** - Define execution pipelines in code
- **Portable** - Works across different container runtimes
- **Cacheable** - Efficient layer caching for fast execution
- **Composable** - Easy to chain multiple tools together

This architecture ensures that even untrusted tools can be executed safely, making Enact suitable for enterprise environments where security is paramount.

## Best Practices

1. **Use exact versions:** `npx prettier@3.3.3` not `npx prettier`
2. **Hierarchical names:** `company/category/tool-name`
3. **Include license:** Use SPDX identifiers like `"MIT"`
4. **Add input schemas:** Help AI models use tools correctly
5. **Set timeouts:** Match expected execution time
6. **Tag appropriately:** `["text", "analysis", "nlp"]`
7. **Pin container images:** Use specific tags like `python:3.11-slim` not `python:latest`
8. **Use minimal images:** Prefer `alpine` or `slim` variants for faster startup

## Example Tools

### Text Processing
```yaml
enact: "1.0.0"
name: enact/text/word-count
description: "Counts words in text"
command: "echo '${text}' | wc -w"
inputSchema:
  type: object
  properties:
    text: {type: string}
  required: ["text"]
```

### Code Formatting
```yaml
enact: "1.0.0"
name: enact/code/prettier
description: "Formats JavaScript/TypeScript code"
from: "node:18-alpine"
command: "npx prettier@3.3.3 --write '${file}'"
inputSchema:
  type: object
  properties:
    file: {type: string, description: "File to format"}
  required: ["file"]
annotations:
  destructiveHint: true  # Modifies files in place
```

### Web Scraping
```yaml
enact: "1.0.0"
name: enact/web/markdown-crawler
description: "Extracts content as markdown"
from: "python:3.11-slim"
command: "uvx markdown-crawler@2.1.0 '${url}'"
inputSchema:
  type: object
  properties:
    url: {type: string, format: uri}
  required: ["url"]
annotations:
  openWorldHint: true    # Connects to internet
  readOnlyHint: true     # Safe, no system changes
```

## Why Enact?

**For Developers:**
- Turn any CLI tool into an AI tool instantly
- No complex integrations or API servers
- Version and secure your tools
- Test locally before publishing

**For AI Applications:**
- Discover tools semantically (`search "image resize"`)
- Execute safely in Dagger-powered containers
- Trust verified tools with cryptographic signatures
- Scale without managing infrastructure or security concerns

**For Enterprises:**
- Control tool approval with multi-party signatures
- Audit all tool usage and versions
- Ensure reproducible, containerized environments
- Manage security policies with Dagger-based isolation

## Get Started

1. **Install:** `npm install -g @enactprotocol/cli`
2. **Create:** `enact init my-first-tool`
3. **Publish:** `enact publish tool.yaml`
4. **Use:** AI models can now discover and execute your tool!



## 📋 Complete Field Reference

### Core Fields

```yaml
# REQUIRED FIELDS
name: string         # Tool identifier with hierarchical path (required)
description: string  # Human-readable description (required)
command: string      # Shell command to execute with versions (required)

# RECOMMENDED FIELDS
from: string         # Container image to run the command on (optional, defaults to system shell)
timeout: string      # Go duration format: "30s", "5m", "1h" (default: "30s")
tags: [string]       # Tags for search and categorization
license: string      # SPDX License identifier (e.g., "MIT", "Apache-2.0", "GPL-3.0")
outputSchema: object # Output structure as JSON Schema (strongly recommended)

# OPTIONAL FIELDS
version: string      # Tool definition version for tracking changes
enact: string        # Version of enact being used
resources:           # Resource requirements
  memory: string     # System memory needed (e.g., "16Gi", "32Gi")
  gpu: string        # GPU memory needed (e.g., "24Gi", "48Gi")
  disk: string       # Disk space needed (e.g., "100Gi", "500Gi")
```

### Environment Variables

```yaml
env:
  SOME_VARIABLE_NAME:
    description: string  # What this variable is for (required)
    source: string       # Where to get this value (required)
    required: boolean    # Whether this is required (required)
    default: string      # Default value if not set (optional)
```

### Schema Definitions

```yaml
inputSchema: object   # Input parameters as JSON Schema (recommended)
outputSchema: object  # Output structure as JSON Schema (strongly recommended)
```

### Documentation and Testing

```yaml
doc: string          # Markdown documentation (optional)
authors:             # Tool creators (optional)
  - name: string     # Author name (required)
    email: string    # Author email (optional)
    url: string      # Author website (optional)

examples:            # Test cases and expected outputs (optional)
  - input: object    # Input parameters (optional, omit for tools with no inputs)
    output: any      # Expected output (optional)
    description: string # Test description (optional)
```

### Behavior Annotations

```yaml
annotations:         # MCP-aligned behavior hints (all default to false)
  title: string              # Human-readable display name (optional)
  readOnlyHint: boolean      # No environment modifications
  destructiveHint: boolean   # May make irreversible changes
  idempotentHint: boolean    # Multiple calls = single call
  openWorldHint: boolean     # Interacts with external systems
```

### Multi-Signature Security

```yaml
signatures:             # Cryptographic signatures (optional, supports multiple signers)
  - signer: string      # Signer identifier (UUID or human-readable name) (required)
    algorithm: string   # Hash algorithm: "sha256" (required)
    type: string        # Signature type: "ecdsa-p256" (required)
    value: string       # Base64 encoded signature (required)
    created: string     # ISO timestamp (required)
    role: string        # Signer role: "author", "reviewer", "approver", etc. (optional)
  - signer: string      # Additional signers
    algorithm: string
    type: string
    value: string
    created: string
    role: string
```

### Custom Extensions

Use the `x-` prefix for custom fields:

```yaml
name: "company/tool/example"
description: "Example tool"
command: "echo 'Hello ${name}'"

# Custom extensions
x-internal-id: "tool-12345"
x-team-owner: "platform-team"
x-cost-center: "engineering"
```


## 🔐 Canonical Security Fields & Signature Logic

Enact cryptographically signs only a subset of **critical security fields** to prevent tampering and ensure deterministic, reproducible signatures. These fields are now:

- Listed **alphabetically** for deterministic ordering
- **Empty values are excluded** (null, empty string, empty object/array)

**Critical fields included in the signature:**

- `annotations`  — Security behavior hints
- `command`      — The actual execution payload
- `description`  — What the tool claims to do
- `enact`        — Protocol version security
- `env`          — Environment variables
- `from`         — Container image (critical for security)
- `inputSchema`  — Defines the attack surface
- `name`         — Tool identity (prevents impersonation)
- `timeout`      — Prevents DoS attacks
- `version`      — Tool version for compatibility

> **Note:** Only non-empty values are included in the canonical JSON for signing. This ensures signatures are consistent and not affected by empty or missing fields.

**Example (deterministic, critical-fields-only, sorted JSON):**

```json
{
  "annotations": { ... },
  "command": "npx prettier@3.3.3 --write '${file}'",
  "description": "Formats JavaScript/TypeScript code",
  "enact": "1.0.0",
  "env": { ... },
  "from": "node:18-alpine",
  "inputSchema": { ... },
  "name": "enact/code/prettier",
  "timeout": "30s",
  "version": "1.2.3"
}
```

- The signature is computed over this canonical JSON, with keys sorted alphabetically.
- Any field that is empty or missing is omitted from the signed data.



## Community

- 💬 [Discord](https://discord.gg/mMfxvMtHyS) - Chat with developers
- 🐛 [GitHub](https://github.com/EnactProtocol/enact) - Report issues
- 📖 [Documentation](https://enactprotocol.com) - Full specification
- 🌟 [Registry](https://enact.tools) - Browse tools (coming soon)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

© 2025 Enact Protocol Contributors

---

*"Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."* — Antoine de Saint-Exupéry