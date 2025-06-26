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
npm install -g enact-cli
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
```

### Multi-Signature Security
Tools can be signed by multiple parties:
```yaml
signatures:
  "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...":
    signer: "author"
    role: "developer"
    created: 2025-05-15T23:55:41.328Z
  "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAF...":
    signer: "security-team"
    role: "reviewer"
    created: 2025-05-16T08:30:00.000Z
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

## Best Practices

1. **Use exact versions:** `npx prettier@3.3.3` not `npx prettier`
2. **Hierarchical names:** `company/category/tool-name`
3. **Include license:** Use SPDX identifiers like `"MIT"`
4. **Add input schemas:** Help AI models use tools correctly
5. **Set timeouts:** Match expected execution time
6. **Tag appropriately:** `["text", "analysis", "nlp"]`

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
- Execute safely in isolated environments
- Trust verified tools with signatures
- Scale without managing infrastructure

**For Enterprises:**
- Control tool approval with multi-party signatures
- Audit all tool usage and versions
- Ensure reproducible environments
- Manage security policies centrally

## Get Started

1. **Install:** `npm install -g enact-cli`
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
  VARIABLE_NAME:
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

examples:            # Test cases and expected outputs
  - input: object    # Input parameters
    output: any      # Expected output
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
signatures:          # Cryptographic signatures (optional, supports multiple signers)
  "PUBLIC_KEY_1":    # Base64-encoded public key as map key
    algorithm: string    # Hash algorithm: "sha256" (required)
    type: string         # Signature type: "ecdsa-p256" (required)
    signer: string       # Human-readable signer identifier (required)
    created: string      # ISO timestamp (required)
    value: string        # Base64 encoded signature (required)
    role: string         # Signer role: "author", "reviewer", "approver", etc. (optional)
  "PUBLIC_KEY_2":    # Additional signers
    algorithm: sha256
    type: ecdsa-p256
    signer: "security-team"
    created: 2025-05-16T08:30:00.000Z
    value: "MEUCIDxNLAzYZQAul2/uhPkdjxNrNwkFWy2qYOGV5pWIpdabAiEB..."
    role: "security-reviewer"
```

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