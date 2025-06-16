# Enact Protocol

![Status: Alpha](https://img.shields.io/badge/Status-Alpha-yellow) ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) [![Discord](https://img.shields.io/badge/Discord-Enact_PROTOCOL-blue?logo=discord&logoColor=white)](https://discord.gg/mMfxvMtHyS)

**Enact** revolutionizes how AI tools are defined, packaged, and shared.

## Enact in 30 Seconds

**Enact lets AI models use command-line tools safely and reliably.**

Instead of writing code integrations, you define tools with simple YAML:

```yaml
  name: hello-world
  description: "Greets the world"
  command: "echo 'Hello, ${name}!'"
```

That's it. This tool can now be:
- 🔍 **Discovered** by AI models searching for "hello world" or "greeting"
- 🚀 **Executed** safely without local installation
- 🔐 **Verified** with cryptographic signatures
- 📌 **Versioned** with standard semantic versioning

**Why Enact?**
- Any command-line tool becomes an AI tool
- No coding required - just YAML
- Built on the Model Context Protocol (MCP)
- Secure by default with signatures and versioning

**Get Started:**
```bash
# Install
npm install -g enact-cli

# Create your first tool
enact init my-tool

# Publish it
enact publish tool.yaml
```

Now any AI using MCP can discover and use your tool!

## Now in more detail

Enact is a protocol that complements the [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol) by providing a standardized way to define, package, discover, and secure AI tools.

While MCP enables communication between AI models and tools, **Enact handles the complete lifecycle of those tools**—ensuring they are:

* 🌐 **Discoverable** — semantically searchable across registries
* 📦 **Packaged** — defined in a consistent, executable format
* 🔐 **Secure** — protected with cryptographic signatures and verification
* 🕒 **Versioned** — using pinning or familiar semantic versioning for reliability

> **Enact provides the standards for packaging, securing, and discovering tools**

---

## 🚀 Quick Start

### Your First Tool (3 lines!)

```yaml
name: enact/nasa/markdown-crawler
description: "Extracts markdown content from nasa website"
command: "uvx markdown-crawler@1.0.0 https://www.nasa.gov/news/"
```

That's it! This tool can now be published, discovered, and used by any AI model.

### A More Complete Example

```yaml
enact: "1.0.0"
name: enact/json/formatter
description: "Formats and validates JSON data"
command: "npx jq-cli@1.7.1 --raw-output '${filter}' <<< '${json}'"
timeout: "30s"

# Input validation (JSON Schema)
inputSchema:
  type: object
  properties:
    json:
      type: string
      description: "JSON data to process"
    filter:
      type: string
      description: "jq filter expression"
      default: "."
  required: ["json"]

# Test cases
examples:
  - input: {json: '{"name":"John","age":30}', filter: ".name"}
    output: "John"
```

---

## 🧱 Core Concepts

### Field Requirements

```yaml
# REQUIRED (minimum viable tool)
name: string         # Tool identifier with hierarchical path
description: string  # What the tool does  
command: string      # Shell command to execute

# RECOMMENDED (production best practices)
enact: string        # Protocol version
timeout: string      # Execution timeout (Go duration format)
tags: [string]       # Search and categorization tags
license: string      # SPDX License identifier

# OPTIONAL (advanced features)
inputSchema: object  # JSON Schema for input validation
signatures: object  # Cryptographic signatures (multiple signers supported)
resources: object    # Resource requirements
```

### Hierarchical Tool Names

Enact uses filepath-style naming for natural organization:

```yaml
# Official Enact tools
name: enact/text/analyzer
name: enact/discord/bot-maker
name: enact/web/scraper

# Organization tools
name: acme-corp/analytics/processor
name: github/actions/deployer

# Personal tools
name: johndoe/utils/file-converter
name: janedoe/ai/prompt-optimizer
```

**Benefits:**
- **Natural Discovery**: Search `enact/discord` for all Discord tools
- **Clear Ownership**: Registry enforces prefix permissions
- **Simple Organization**: Familiar filesystem-like hierarchy
- **No Namespace Conflicts**: Full path ensures uniqueness

### Universal Command Execution

Enact's superpower is its **command interface** executed through the Enact MCP Server. Any shell command works:

```yaml
# NPX with version tags (recommended)
command: "npx prettier@3.3.3 --write '${file}'"
command: "npx eslint@9.0.0 --fix '${file}'"

# UVX for Python tools
command: "uvx black@24.4.2 '${file}'"
command: "uvx ruff@0.5.0 check '${file}'"

# Docker with specific tags
command: "docker run pandoc/core:3.1.11 -f markdown -t html '${input}'"

# HTTP APIs with versioned endpoints
command: "curl -s 'https://api.example.com/v1/process' -d '${json}'"

# Shell pipelines
command: "echo '${text}' | npx slugify-cli@2.0.0"

# Complex workflows
command: |
  echo "Processing ${input}" &&
  uvx pyyaml@6.0.1 validate &&
  npx prettier@3.3.3 --write output.yaml
```

**For maximum reproducibility**, you can also use commit hashes:
```yaml
# Using commit hashes for absolute immutability
command: "npx github:prettier/prettier#abc123def --write '${file}'"
command: "uvx --from git+https://github.com/psf/black@d47cbd5 black '${file}'"
```

### Progressive Complexity

Start simple, add features as needed:

**Level 1: Minimal** (3 required fields)
```yaml
name: enact/text/slugify
description: "Converts text to URL-friendly slugs"
command: "npx slugify-cli@2.0.0 '${text}'"
```

**Level 2: Production-Ready** (+ validation & metadata)
```yaml
enact: "1.0.0"
name: enact/markdown/to-html
description: "Converts markdown to HTML with syntax highlighting"
command: "npx markdown-it@14.0.0 -o '${output}' '${input}'"
timeout: "30s"
tags: ["markdown", "html", "converter", "documentation"]
license: "MIT"

inputSchema:
  type: object
  properties:
    input:
      type: string
      description: "Markdown content or file path"
    output:
      type: string
      description: "Output HTML file path"  
      default: "output.html"
  required: ["input"]

# Output schema helps AI models understand tool responses
outputSchema:
  type: object
  properties:
    success:
      type: boolean
      description: "Whether conversion succeeded"
    outputPath:
      type: string
      description: "Path to generated HTML file"
  required: ["success", "outputPath"]
```

**Level 3: Enterprise** (+ environment & signatures)
```yaml
enact: 1.0.0
name: acme-corp/ai/code-review
description: "Reviews code using OpenAI's API"
command: "uvx openai-cli@1.0.0 review --file='${file}' --model='${model}'"
timeout: "2m"
tags: ["ai", "code-review", "openai", "analysis"]
license: "Apache-2.0"

env:
  OPENAI_API_KEY:
    description: "OpenAI API key for GPT access"
    source: "https://platform.openai.com/api-keys"
    required: true

inputSchema:
  type: object
  properties:
    file:
      type: string
      description: "Code file to review"
    model:
      type: string
      enum: ["gpt-4", "gpt-3.5-turbo"]
      default: "gpt-4"
  required: ["file"]

# Multiple signatures from different parties
signatures:
  # Using public key as the map key
  "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...":
    algorithm: sha256
    type: ecdsa-p256
    signer: "enact-official"  # Human-readable identifier
    created: 2025-05-15T23:55:41.328Z
    value: "MEUCICwNLAzYZQAul2/uhPkdjxNrNwkFWy2qYOGV5pWIpdabAiEA..."
    role: "author"
  "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAF...":
    algorithm: sha256
    type: ecdsa-p256
    signer: "security-auditor"
    created: 2025-05-16T10:30:00.000Z
    value: "MEUCIDxNLAzYZQAul2/uhPkdjxNrNwkFWy2qYOGV5pWIpdabAiEB..."
    role: "reviewer"
```

---

## 🧠 How Enact Extends MCP

MCP defines [tools](https://modelcontextprotocol.io/docs/concepts/tools) with a basic structure, but doesn't address the complete tool lifecycle. Enact fills this gap:

**MCP Tool Definition:**
```
{
  "name": "string",          // Unique identifier for the tool
  "description": "string",   // Human-readable description (optional)
  "inputSchema": {           // JSON Schema for the tool's parameters
    "type": "object",
    "properties": {}         // Tool-specific parameters
  }
}
```

**Enact builds on this foundation** by adding essential lifecycle management capabilities:

| Capability | MCP | Enact |
|------------|-----|-------|
| Communication Protocol | ✅ Defines interaction | ✅ Uses MCP protocol |
| Tool Execution | ❌ Server implementation required | ✅ Command-based execution via Enact MCP Server |
| Tool Discovery | ❌ | ✅ Semantic search & registry |
| Tool Packaging | ❌ | ✅ Standard YAML schema |
| Versioning | ❌ | ✅ Semantic versioning support |
| Security & Verification | ❌ | ✅ Cryptographic signatures with multi-signer support |
| Environment Management | ❌ | ✅ Isolated execution environments |

---

## 📋 Tool Definition Reference

### Required Fields

```yaml
name: string         # Tool identifier with hierarchical path (must be unique in registry)
description: string  # Human-readable description of what the tool does
command: string      # Shell command to execute (with versions or hash pins recommended)
```

### Recommended Fields

```yaml
timeout: string      # Execution timeout in Go duration format: "30s", "5m", "1h" (default: "30s")
tags: [string]       # Tags for search and categorization
license: string      # SPDX License identifier (e.g., "MIT", "Apache-2.0", "GPL-3.0")
```

### Optional Fields

```yaml
version: string      # Tool definition version for tracking changes
```

### Input & Output Schemas (JSON Schema)

Tools use [JSON Schema](https://json-schema.org/) for input validation and output documentation:

```yaml
# Input validation (recommended for production tools)
inputSchema:
  type: object
  properties:
    text:
      type: string
      description: "Text to analyze"
    format:
      type: string
      enum: ["json", "plain"]
      default: "json"
    count:
      type: integer
      minimum: 1
      maximum: 100
  required: ["text"]

# Output schema (strongly recommended - helps AI models understand responses)
outputSchema:
  type: object
  properties:
    words:
      type: integer
      description: "Number of words found"
    characters:
      type: integer
      description: "Number of characters found"
    format:
      type: string
      description: "Output format used"
  required: ["words", "characters"]
```

### Tool Behavior Annotations

```yaml
# Behavior hints (all default to false, aligned with MCP)
annotations:
  readOnlyHint: true      # Tool doesn't modify the system
  idempotentHint: true    # Multiple calls produce same result as single call
  destructiveHint: false  # Tool may make permanent/irreversible changes
  openWorldHint: false    # Tool connects to external systems/internet
```

### Environment Variables

Environment variables are stored based on the tool's hierarchical name:

```yaml
# Tool name determines storage location
name: "acme-corp/discord/bot-maker"

# Declare required environment variables
env:
  API_KEY:
    description: "Discord bot API key"
    source: "https://discord.com/developers → Create App → Bot → Token"
    required: true
  WEBHOOK_URL:
    description: "Discord webhook for notifications"
    source: "Server Settings → Integrations → Webhooks → Create"
    required: true
  REQUEST_TIMEOUT:
    description: "API request timeout in seconds"
    default: "10"
    required: false
```

**Storage Structure:**
```bash
~/.enact/
└── env/
    └── acme-corp/
        └── discord/
            └── bot-maker/
                ├── .env          # User's actual secrets
                └── .env.example  # Template from tool
```

**Security Model:**
- Each tool execution reads ONLY from its specific directory
- No access to parent process environment
- Secrets stored in `.env` files (use OS file permissions)
- Simple security model to start, will enhance over time

### Testing & Examples

```yaml
examples:
  - input: {text: "hello world", format: "json"}
    output: {words: 2, characters: 11}
    description: "Basic word counting"
  - input: {text: "one"}
    output: {words: 1}
    description: "Single word test"
```

### Cryptographic Signatures

Tools can be signed by multiple parties for authenticity verification. The new format uses public keys as map keys, enabling multiple signatures and streamlined verification:

```yaml
signatures:
  # Using public key as the map key for direct verification
  "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...":
    algorithm: sha256
    type: ecdsa-p256
    signer: "enact-official"  # Human-readable identifier
    created: 2025-05-15T23:55:41.328Z
    value: "MEUCICwNLAzYZQAul2/uhPkdjxNrNwkFWy2qYOGV5pWIpdabAiEA..."
    role: "author"
  "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAF...":
    algorithm: sha256
    type: ecdsa-p256
    signer: "security-auditor"
    created: 2025-05-16T10:30:00.000Z
    value: "MEUCIDxNLAzYZQAul2/uhPkdjxNrNwkFWy2qYOGV5pWIpdabAiEB..."
    role: "reviewer"
```

**Benefits of the new format:**
- **Multiple Signers**: Support for author, reviewer, auditor signatures
- **Direct Verification**: Public key in the map key enables immediate verification
- **Clear Roles**: Optional role field clarifies each signer's relationship to the tool
- **Extensible**: Easy to add new signers without breaking existing tools

---

## 🏗 Architecture

```mermaid
flowchart TB
    Dev[Developer] --> CLI["enact publish"]
    CLI --> Registry[(Enact Registry)]
    
    LLM --> MCPClient["MCP Client"]
    MCPClient --> EnactMCP["Enact MCP Server"]
    EnactMCP --> Registry
    EnactMCP --> ExecEnv["Command Execution"]
    
    classDef ai fill:#6366F1,color:white
    classDef enact fill:#10B981,color:white
    classDef dev fill:#7C3AED,color:white

    class LLM,MCPClient ai
    class Registry,ExecEnv,EnactMCP enact
    class Dev,CLI dev
```

**Flow:**
1. Developer creates tool definition (YAML)
2. CLI validates and publishes to registry
3. AI models discover tools via semantic search
4. Enact MCP Server fetches and executes tool commands
5. Results return to AI model

---

## 🧪 Example Tools

### Text Analysis
```yaml
name: enact/text/statistics
description: "Analyzes text statistics and readability"
command: "npx text-stats-cli@1.0.0 '${text}'"
timeout: "30s"
tags: ["text", "analysis", "statistics", "readability"]
license: "MIT"

inputSchema:
  type: object
  properties:
    text:
      type: string
      description: "Text to analyze"
  required: ["text"]

examples:
  - input: {text: "The quick brown fox jumps over the lazy dog."}
    output: |
      {
        "words": 9,
        "characters": 44,
        "sentences": 1,
        "readability": "easy"
      }
    description: "Basic text analysis"

outputSchema:
  type: object
  properties:
    words:
      type: integer
      description: "Number of words"
    characters:
      type: integer
      description: "Number of characters"
    sentences:
      type: integer
      description: "Number of sentences"
    readability:
      type: string
      description: "Reading difficulty level"
```

### Code Formatting
```yaml
name: enact/code/prettier
description: "Formats code using Prettier"
command: "npx prettier@3.3.3 --write '${file}' --config '${config}'"
timeout: "1m"
tags: ["code", "formatter", "prettier", "javascript", "typescript"]
license: "MIT"

inputSchema:
  type: object
  properties:
    file:
      type: string
      description: "File or glob pattern to format"
    config:
      type: string
      description: "Path to prettier config"
      default: ".prettierrc"
  required: ["file"]

annotations:
  destructiveHint: true  # Modifies files in place
```

### Data Validation with Multiple Signatures
```yaml
name: enact/data/json-validator
description: "Validates JSON against a schema"
command: "npx ajv-cli@5.0.0 validate -s '${schema}' -d '${data}'"
timeout: "30s"
tags: ["json", "validation", "schema", "data"]
license: "Apache-2.0"

inputSchema:
  type: object
  properties:
    schema:
      type: string
      description: "Path to JSON schema file"
    data:
      type: string
      description: "Path to data file to validate"
  required: ["schema", "data"]

outputSchema:
  type: object
  properties:
    valid:
      type: boolean
      description: "Whether the data is valid"
    errors:
      type: array
      description: "Validation errors if any"
      items:
        type: object

# Multiple signatures for trust and verification
signatures:
  "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...":
    algorithm: sha256
    type: ecdsa-p256
    signer: "data-team-lead"
    created: 2025-05-15T23:55:41.328Z
    value: "MEUCICwNLAzYZQAul2/uhPkdjxNrNwkFWy2qYOGV5pWIpdabAiEA..."
    role: "author"
  "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAF...":
    algorithm: sha256
    type: ecdsa-p256
    signer: "security-team"
    created: 2025-05-16T08:30:00.000Z
    value: "MEUCIDxNLAzYZQAul2/uhPkdjxNrNwkFWy2qYOGV5pWIpdabAiEB..."
    role: "security-reviewer"
```

### Web Scraping
```yaml
name: enact/web/content-extractor
description: "Extracts content from web pages as markdown"
command: "uvx markdown-crawler@2.1.0 '${url}' --depth='${depth}'"
timeout: "2m"
tags: ["web", "scraping", "markdown", "content", "extraction"]
license: "BSD-3-Clause"

inputSchema:
  type: object
  properties:
    url:
      type: string
      format: uri
      description: "URL to scrape"
    depth:
      type: integer
      description: "Crawl depth (0 for single page)"
      default: 0
      minimum: 0
      maximum: 3
  required: ["url"]

annotations:
  openWorldHint: true
  readOnlyHint: true
```

### Data Pipeline
```yaml
name: acme-corp/data/csv-processor
description: "Validates and transforms CSV data"
command: |
  enact exec csv-validator --file='${file}' --schema='${schema}' &&
  enact exec csv-transformer --file='${file}' --output=processed.csv
timeout: "5m"
tags: ["data", "csv", "validation", "etl", "pipeline"]
license: "GPL-3.0"

inputSchema:
  type: object
  properties:
    file:
      type: string
      description: "CSV file path"
    schema:
      type: string
      format: uri
      description: "Validation schema URL"
  required: ["file"]
```

### Video Processing
```yaml
name: media-tools/video/transcoder
description: "Transcodes videos using GPU acceleration"
command: "docker run --gpus all video-tools:2.5.0 transcode --input='${input}' --output='${output}' --format='${format}'"
timeout: "30m"
tags: ["video", "media", "transcoding", "gpu"]
license: "LGPL-2.1"

resources:
  memory: "16Gi"
  gpu: "24Gi"
  disk: "100Gi"

inputSchema:
  type: object
  properties:
    input:
      type: string
      description: "Input video URL"
    output:
      type: string
      description: "Output filename"
    format:
      type: string
      enum: ["mp4", "webm", "mov"]
      default: "mp4"
  required: ["input", "output"]

annotations:
  openWorldHint: true
```

### API Testing
```yaml
name: enact/http/tester
description: "Tests HTTP endpoints"
command: "npx got-cli@3.0.0 '${url}' --method='${method}' --headers='${headers}' --body='${body}'"
timeout: "30s"
tags: ["api", "http", "testing", "rest"]
license: "MIT"

inputSchema:
  type: object
  properties:
    url:
      type: string
      format: uri
      description: "URL to test"
    method:
      type: string
      enum: ["GET", "POST", "PUT", "DELETE", "PATCH"]
      default: "GET"
    headers:
      type: string
      description: "JSON string of headers"
      default: "{}"
    body:
      type: string
      description: "Request body"
  required: ["url"]

annotations:
  openWorldHint: true
  idempotentHint: false  # Depends on the method
```

---

## 🔐 Security

### Versioning Best Practices

Enact supports multiple versioning strategies to balance convenience and security:

```yaml
# Standard version tags (recommended for most tools)
command: "npx prettier@3.3.3"
command: "uvx black@24.4.2"
command: "docker run node:20-alpine"

# Version ranges for flexibility
command: "npx eslint@^9.0.0"  # Compatible with 9.x.x
command: "uvx ruff@~0.5.0"    # Compatible with 0.5.x

# Commit hashes for maximum reproducibility
command: "npx github:prettier/prettier#abc123def"
command: "uvx --from git+https://github.com/psf/black@d47cbd5 black"
command: "docker run node@sha256:abc123..."
```

**Recommendations:**
- Use **exact versions** (`@1.2.3`) for production tools
- Use **version ranges** (`@^1.2.0`) for development tools
- Use **commit hashes** for security-critical applications

### Multi-Signature Support

Verify tool authenticity with signatures:

```yaml
signatures:
  # Author signature
  "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...":
    algorithm: sha256
    type: ecdsa-p256
    signer: "john-doe"
    created: 2025-05-15T23:55:41.328Z
    value: "MEUCICwNLAzYZQAul2/uhPkdjxNrNwkFWy2qYOGV5pWIpdabAiEA..."
    role: "author"
    
  # Security team review
  "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAF...":
    algorithm: sha256
    type: ecdsa-p256
    signer: "security-team"
    created: 2025-05-16T08:30:00.000Z
    value: "MEUCIDxNLAzYZQAul2/uhPkdjxNrNwkFWy2qYOGV5pWIpdabAiEB..."
    role: "security-reviewer"
    
  # Management approval
  "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAG...":
    algorithm: sha256
    type: ecdsa-p256
    signer: "engineering-manager"
    created: 2025-05-16T14:15:00.000Z
    value: "MEUCIAxNLAzYZQAul2/uhPkdjxNrNwkFWy2qYOGV5pWIpdabAiEC..."
    role: "approver"
```

**Signature verification is handled automatically by the Enact MCP Server, with support for:**
- **Multiple verification**: All signatures must be valid
- **Role-based policies**: Require specific roles (author + reviewer)
- **Key rotation**: Support for updating keys while maintaining trust
- **Revocation**: Mark compromised keys as invalid

---

## 🛠 CLI Usage

```bash
# Create a new tool
enact init my-tool

# Validate tool definition
enact validate tool.yaml

# Test locally
enact test tool.yaml --input '{"text": "hello"}'

# Sign a tool (adds to signatures)
enact sign tool.yaml --key my-private-key.pem --role author

# Publish to registry
enact publish tool.yaml

# Search for tools
enact search "text analysis"

# Verify signatures
enact verify tool.yaml
```

---

## 🌐 MCP Integration

Enact tools are available through the Enact MCP Server:

```javascript
// Search for tools
const tools = await client.call('enact-search-capabilities', {
  query: 'sentiment analysis'
});

// Register a tool
await client.call('enact-register-capability', { 
  id: tools[0].id 
});

// Execute a registered tool
const result = await client.call('execute-capability-by-id', {
  id: tools[0].id,
  args: { text: 'I love this!' }
});
```

---

## 🤝 Why Enact?

**For Developers:**
- Write tools in any language or technology
- Use familiar shell commands
- Test locally before publishing
- Version and sign your tools
- **Multi-party signing** for enterprise approval workflows

**For AI Applications:**
- Discover tools semantically
- Trust verified tool
- Scale seamlessly
- Consistent execution model

**For Enterprises:**
- Control tool approval with signatures
- Audit tool usage and versions
- Ensure reproducibility
- Manage security policies

---

## 📚 Best Practices

### 1. Start Simple
Begin with the minimal 3-field format and add features as needed.

### 2. Use Hierarchical Names
Choose clear, descriptive paths that indicate purpose and ownership:
- ✅ `enact/markdown/to-html-converter`
- ✅ `acme-corp/analytics/revenue-processor`
- ❌ `md2html`
- ❌ `tool123`

### 3. Version Your Dependencies
Always specify versions in your commands:
- ✅ `npx prettier@3.3.3`
- ✅ `uvx black@24.4.2`
- ❌ `npx prettier` (no version)

For maximum security, you can use commit hashes:
- `npx github:org/tool#abc123def`
- `uvx --from git+https://github.com/org/tool@abc123`

### 4. Specify License
Always include a license field using SPDX identifiers:
- ✅ `license: "MIT"`
- ✅ `license: "Apache-2.0"`
- ✅ `license: "GPL-3.0"`
- ✅ `license: "BSD-3-Clause"`
- ❌ `license: "MIT License"` (use SPDX identifier)

### 5. Test Your Tools
Include examples to verify behavior and document expected outputs.

### 6. Organize by Purpose
Use logical hierarchies for better discovery:
- `enact/text/*` for text processing tools
- `enact/web/*` for web-related tools
- `company/internal/*` for internal company tools
- `username/personal/*` for personal utilities

### 7. Document Behavior with Annotations
Use `readOnlyHint`, `idempotentHint`, `destructiveHint`, and `openWorldHint` to help AI models understand tool behavior.

### 8. Set Appropriate Timeouts
Use Go duration format: `"30s"`, `"5m"`, `"1h"`. Match timeout values to expected execution time.

### 9. Use Tags for Better Discovery
Add relevant tags to help users find your tools:
- ✅ `["text", "analysis", "sentiment"]` for sentiment analysis
- ✅ `["image", "resize", "media"]` for image processing
- ✅ `["data", "csv", "validation"]` for data tools

### 10. Prefer Universal Tools
Use tools that work across platforms without installation:
- ✅ `npx package@version` (works everywhere with npm)
- ✅ `uvx package@version` (works everywhere with Python)
- ✅ `docker run image:tag` (requires Docker but platform-agnostic)
- ❌ `pdftotext` (requires system package installation)

### 11. Use Multi-Signature for Production Tools
For enterprise or critical tools, implement a signing workflow:
- **Author signs** during development
- **Security team reviews** and signs
- **Manager approves** and signs
- **Registry validates** all signatures before publication

---

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

### Extensions

```yaml
x-*: any             # Custom extensions (must begin with 'x-')
```

---

## 🚧 Roadmap

**Current (Alpha)**
- ✅ Core protocol specification
- ✅ Command-based execution
- ✅ Multi-signature support with public key mapping
- ✅ Basic MCP integration via Enact MCP Server
- 🔄 Signature verification implementation

**Next (Beta)**
- 🔄 Enhanced CLI with testing
- 🔄 Public registry launch at enact.tools
- 🔄 Advanced security features
- 🔄 Performance optimizations

**Future**
- ⏳ Visual tool builder
- ⏳ Marketplace features
- ⏳ Enhanced environment security
- ⏳ Multi-language execution environments
- ⏳ Federated signature verification

---

## 💬 Community

Join our growing community:

- 💬 [Discord](https://discord.gg/mMfxvMtHyS) - Chat with developers
- 🐛 [GitHub Issues](https://github.com/EnactProtocol/enact) - Report bugs
- 📖 [Protocol Site](https://enactprotocol.com) - Full specification
- 🌟 [Tool Registry](https://enact.tools) - Browse and publish tools (WIP)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

© 2025 Enact Protocol Contributors

---

*"Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."* — Antoine de Saint-Exupéry