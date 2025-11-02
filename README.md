# Enact Protocol - Abridged Guide

**Quick reference for the Enact Protocol: A verified registry and execution framework for AI-executable tools.**

**Version:** 1.0.1
**Last Updated:** 2025-10-28

---

## What is Enact?

Enact Protocol is an open standard and registry for trusted AI-executable tools — a verified, portable way for humans and AI agents to discover, share, and safely run modular code. Each tool is defined in a single enact.md file that describes its inputs, outputs, environment, and signed execution command. Enact combines semantic discovery, containerized execution, and cryptographic verification to form a secure, composable ecosystem — effectively an “npm for AI,” where every microapp is verifiable, reproducible, and ready for autonomous use.


Enact Protocol defines the open standard behind the kind of modular “AI capabilities” that companies like Anthropic are now building into their ecosystems. Anthropic’s Agent Skills prove the model — modular, filesystem-based extensions that give AI agents reusable expertise. But their implementation is closed, vendor-specific, and bound to one product.

Enact takes the next step: it provides a universal, verifiable, and portable protocol for defining, discovering, and executing these same kinds of tools across any AI runtime. Each Enact module is a signed, self-describing enact.md file that can run securely anywhere — enabling interoperability between agents, registries, and ecosystems.

In other words: if Claude Skills are “apps for Claude,” Enact is “the App Store protocol for AI.” Anthropic’s launch validates the concept; Enact’s opportunity is to make it open, cross-platform, and trustable.


Enact Protocol is the open registry for trusted AI tools — a shared standard for defining, discovering, and safely running code that AIs can understand and execute. Every tool is described in a single `enact.md` file — a portable manifest that combines metadata, documentation, and execution details.

**Key Features:**
- 🔍 **Discovered** by AI models via semantic search
- 🚀 **Executed** safely in isolated containers
- 🔐 **Verified** with cryptographic signatures (Sigstore)
- 📌 **Versioned** with semantic versioning
- 🤖 **Composed** by calling other tools

---

## Quick Start

### Install

```bash
npm install -g @enactprotocol/cli
```

### Create Your First Tool

Create a tool definition file `enact.md`:

```markdown
---
enact: "1.0.0"
name: "username/utils/greeter"
description: "Greets the user by name"
command: "echo 'Hello, ${name}!'"
inputSchema:
  type: object
  properties:
    name: {type: string}
  required: ["name"]
---

# Greeter

A simple tool that greets users by name.
```

Install and test the tool:

```bash
# Install locally
enact install .

# Test it
enact run username/utils/greeter --args '{"name":"World"}'
# Output: Hello, World!
```

When ready to share publicly:

```bash
# Sign and publish
enact sign .
enact publish .
```

---

## Core Concepts

### Two Execution Modes

**Mode 1: `enact run` — Run the Declared Command**

Execute the tool's canonical, signed behavior:

- Uses the `command` field from `enact.md`
- Deterministic and reproducible
- Signed and verifiable
- Takes structured `--args` input (JSON)

```bash
enact run acme-corp/data/csv-processor --args '{"file":"data.csv","operation":"summarize"}'
```

**Mode 2: `enact exec` — Execute Arbitrary Code in the Tool's Environment**

Run custom commands inside the tool's container:

- Runs **any command** inside the tool's container
- Same isolation and security guarantees
- Not signed or deterministic — great for experimentation

```bash
enact exec acme-corp/data/csv-processor "python utils/validate.py data.csv"
```

### Tool Types

**Container-Executed Tools (with `command` field)**

Tools with a `command` field can be executed deterministically using `enact run`:

```yaml
command: "python src/process.py --file='${file}' --operation='${operation}'"
from: "python:3.11-slim"
```

**LLM-Driven Tools (without `command` field)**

Tools without a `command` field are interpreted by the LLM, but can still be executed in their containerized environment using `enact exec`.

### Installation Levels

**Project-Level Installation (default)**

Install tools scoped to your current project, similar to `npm install`:

```bash
# Install tool for this project only
enact install acme-corp/data/csv-processor
```

This creates:
- `.enact/tools.json` - Project manifest (check into git)
- `.enact/{org}/{path}/{tool}/` - Project-local tool installations

**User-Level Installation (--global)**

Install tools globally for your user account, similar to `npm install -g`:

```bash
# Install from registry globally
enact install acme-corp/data/csv-processor --global

# Install current directory as global tool
cd my-tool/
enact install . --global
# Installs to: ~/.enact/tools/
```

**Understanding tools/ vs cache/**

- **`~/.enact/tools/`** - Active, user-installed tools (what you explicitly installed with `--global`)
- **`~/.enact/cache/`** - Immutable, versioned bundles (downloaded from registry or created during install)

When you `enact install`:
1. Downloads or packages the tool
2. Creates immutable bundle in `cache/`
3. Extracts/hydrates to active `tools/` directory

When you `enact uninstall`:
- Removes from `tools/` (no longer active)
- Keeps in `cache/` (instant reinstall)

**Tool Resolution Order**

When you run a tool, Enact searches in this order:

1. **Project-level** (`.enact/` in current directory or parent directories)
2. **User-level** (`~/.enact/tools/` - your active installed tools)
3. **Cache** (`~/.enact/cache/` - temporarily hydrates if not installed)
4. **Registry** (download, verify signature, cache, execute)

---

## Essential CLI Commands

### Run & Execute

```bash
# Run declared command
enact run <tool-name> --args '<json>'

# Execute custom command in tool environment
enact exec <tool-name> "<command>"
```

### Install & Manage

```bash
# Install all project tools from .enact/tools.json
enact install

# Install tool for project
enact install <tool-name>

# Install tool globally
enact install <tool-name> --global

# Install current directory as global tool
enact install . --global
```

### Discovery

```bash
# Search registry
enact search "pdf extraction"

# List installed tools
enact list

# Get tool info
enact get <tool-name>
```

### Publishing

```bash
# Validate, sign, and publish
enact validate ./my-tool/
enact sign ./my-tool/
enact publish ./my-tool/
```

### Verification

```bash
# Verify a cached tool's signature
enact verify <tool-name>

# Re-verify against registry
enact verify <tool-name> --remote
```

### Environment Variables

```bash
# Manage environment variables (namespace-scoped)
enact env set API_KEY secret123 --package acme-corp/api
enact env list --package acme-corp/api
```

---

## File Format: enact.md

Every tool is a markdown file with YAML frontmatter.

### Required Fields

```yaml
name: "org/category/tool-name"  # Hierarchical identifier (arbitrary depth)
description: "What this tool does"
```

### Recommended Fields

```yaml
enact: "1.0.0"                  # Protocol version
version: "1.2.3"                # Tool version (semver)
from: "python:3.11-slim"        # Container base image
command: "python main.py"       # Execution command (optional)
timeout: "30s"                  # Execution timeout
license: "MIT"                  # SPDX license identifier
tags: ["tag1", "tag2"]         # Discovery keywords
```

### Schema Fields

Define the structure and validation for tool inputs and outputs:

```yaml
inputSchema:
  type: object
  properties:
    file:
      type: string
      description: "File to process"
  required: ["file"]

outputSchema:
  type: object
  properties:
    status:
      type: string
      enum: ["success", "error"]
```

### Environment Variables

Tools in the same **namespace** share environment variables:

```yaml
env:
  API_KEY:
    description: "API key for service"
    source: "https://service.com/settings"
    required: true
    default: "optional-default"
```

**Namespace Sharing:**
- Tools in the same namespace share environment variables
- Storage: `~/.enact/env/{org}/{path}/.env`
- Example: All `acme-corp/api/*` tools share `~/.enact/env/acme-corp/api/.env`

### Behavior Annotations

Hints about tool behavior for AI models (all default to `false`):

```yaml
annotations:
  title: "Human-readable name"
  readOnlyHint: true          # Does not modify environment
  destructiveHint: false      # May make irreversible changes
  idempotentHint: true        # Multiple executions = same result
  openWorldHint: false        # Interacts with external systems
```

### Resource Requirements

```yaml
resources:
  memory: "2Gi"
  gpu: "24Gi"
  disk: "100Gi"
```

### Complete Example

```markdown
---
enact: "1.0.0"
name: "kgroves88/ai/pdf-extract"
description: "Extract text from PDF files"
tags: ["pdf", "text-extraction"]
command: "python src/extract.py --pdf='${pdf_path}' --pages='${pages}'"
timeout: "2m"
from: "python:3.11-slim"
inputSchema:
  type: object
  properties:
    pdf_path: {type: string}
    pages:
      type: array
      items: {type: integer}
---

# PDF Text Extractor

Extracts text from PDF files with page-level granularity.

## Usage

Extract specific pages from a PDF:

\`\`\`bash
enact run kgroves88/ai/pdf-extract --args '{
  "pdf_path": "document.pdf",
  "pages": [1, 2, 3]
}'
\`\`\`

Extract all pages:

\`\`\`bash
enact run kgroves88/ai/pdf-extract --args '{"pdf_path": "report.pdf"}'
\`\`\`
```

---

## Directory Structure

```
~/.enact/
├── tools/                     # Active user-level tools (installed with --global)
│   └── {org}/{path}/{tool}/
│       ├── enact.md
│       ├── src/              # Built source (if applicable)
│       └── node_modules/     # Dependencies (if applicable)
├── cache/                     # Immutable versioned bundles
│   └── {org}/{path}/{tool}/
│       └── v1.0.0/
│           ├── bundle.tar.gz
│           └── .sigstore-bundle
└── env/                       # Environment variables
    └── {org}/{namespace}/.env

my-project/
├── .enact/
│   ├── tools.json            # Project tool manifest (commit to git)
│   └── {org}/{path}/{tool}/  # Project-local tool installations
```

---

## Tool Lifecycle

Understanding how tools move from development to installation to execution.

### 1. Local Development

You're working in your project directory:

```
my-ts-tool/
├── src/
│   └── index.ts
├── package.json
├── enact.md
```

**Test directly without installing:**

```bash
enact run . --args '{"name":"World"}'
```

This mounts your local directory directly—no install, no cache.

### 2. User-Level Installation

When you run:

```bash
enact install .
```

Enact performs these steps:

| Step | Description | Location |
|------|-------------|----------|
| 🧩 Resolve manifest | Reads `enact.md` to identify name, version, command | — |
| 📦 Package tool | Builds or bundles (runs `build` command if specified) | temp dir |
| 💾 Cache artifact | Creates versioned, immutable bundle | `~/.enact/cache/{org}/{path}/{tool}/v{version}/` |
| 📁 Hydrate to tools | Extracts the active working copy | `~/.enact/tools/{org}/{path}/{tool}/` |

**Result:**

```
~/.enact/
├── tools/
│   └── kgroves88/utils/greeter/
│       ├── enact.md
│       ├── dist/
│       └── node_modules/
└── cache/
    └── kgroves88/utils/greeter/
        └── v1.0.0/
            ├── bundle.tar.gz
            └── .sigstore-bundle
```

### 3. Running a Tool

When you run:

```bash
enact run kgroves88/utils/greeter --args '{"name":"World"}'
```

Enact resolves in this order:

1. **Project-level** `.enact/` — if installed locally to project
2. **User-level** `tools/` — your active installed tools
3. **Cache** — temporarily hydrates if bundle exists but not installed
4. **Registry** — downloads, verifies, caches, and runs

### 4. Upgrading / Reinstalling

When you install a new version:

```bash
enact install kgroves88/utils/greeter@1.0.1
```

Enact will:
- Download and verify the new version
- Add `v1.0.1` to cache
- Replace the active copy in `tools/`
- Leave old `v1.0.0` in cache (for rollback or reproducibility)

### 5. Uninstalling

```bash
enact uninstall kgroves88/utils/greeter
```

**Removes:**
- `~/.enact/tools/kgroves88/utils/greeter/`

**Keeps:**
- `~/.enact/cache/kgroves88/utils/greeter/v1.0.0/`

This means:

```bash
enact install kgroves88/utils/greeter@1.0.0
```

...is instant—it just restores from cache.

### 6. Cache Management

```bash
# Remove unused cache entries
enact cache clean

# Remove all cached tools
enact cache clear
```

### Build Example: TypeScript Tools

For tools that need compilation:

```yaml
---
name: "kgroves88/utils/greeter"
from: "node:20"
build: "npm install && npm run build"
command: "node dist/index.js"
inputSchema:
  type: object
  properties:
    name: { type: string }
---
```

When you `enact install .`, Enact:
1. Runs the `build` step inside the container
2. Caches the resulting built tarball
3. Extracts the built version into `~/.enact/tools/`

### Quick Mental Model

| Concept | Directory | Description |
|---------|-----------|-------------|
| **Active tools** | `~/.enact/tools/` | What's currently installed and runnable |
| **Cached bundles** | `~/.enact/cache/` | Immutable, versioned artifacts for reuse |
| **Environments** | `~/.enact/env/` | Namespace-specific environment variables |

- **Install** → populates both tools and cache
- **Uninstall** → removes from tools, keeps in cache
- **Cache prune** → removes unused cache entries

---

## Security & Signatures

**All registry tools are cryptographically signed and verified using Sigstore.**

When you publish:
```bash
enact sign ./my-tool/     # Sign with your GitHub identity
enact publish ./my-tool/  # Upload tool + signature to registry
```

When you install:
```bash
enact install org/tool    # Signature automatically verified before execution
```

**How it works:**
- Publishers sign tools using GitHub authentication via public Sigstore
- Signatures are stored with tools in the registry
- The `enact` CLI automatically verifies signatures before execution
- Publisher identity is shown for all tools (e.g., `repo:org/name:ref:refs/heads/main`)

**Trust model:**
- Local tools (`enact install .`) are fully trusted—no signature needed
- Registry tools are cryptographically verified before first use
- The registry enforces namespace ownership (only `repo:acme-corp/*` can publish to `acme-corp/*`)

**If signature verification fails, the tool will not run. No exceptions.**

For technical details on how signatures work, see [Sigstore Implementation Guide](./sigstore.md).

---

## Common Workflows

### Project Development

Set up project-level tools that your team can share:

```bash
# Install tools for this project
enact install acme-corp/data/csv-processor
enact install myorg/utils/formatter

# Team members clone and install
git clone https://github.com/myorg/my-app
cd my-app
enact install   # Reads .enact/tools.json and verifies signatures
```

### Tool Development

Create and iterate on tools quickly:

```bash
# Create tool in your project directory
cd my-tool-project

# Create enact.md with your tool definition
# (see examples above)

# Install globally (no signature needed for local tools)
enact install . --global

# Test immediately
enact run myorg/utils/my-tool --args '{"name":"World"}'

# Iterate quickly - changes are immediate
# Edit enact.md, then test again
```

### Publishing

Publish tools to the registry:

```bash
# Validate your tool definition
enact validate ./my-tool/

# Sign with your GitHub identity
enact sign ./my-tool/
# This creates ./my-tool/.sigstore-bundle

# Publish to registry
enact publish ./my-tool/
# Uploads tool + signature bundle
```

### Discovery & Usage

Find and use registry tools:

```bash
# Search for tools
enact search "pdf extraction"

# Get tool information
enact get kgroves88/ai/pdf-extract

# Run the tool (automatically verifies signature)
enact run kgroves88/ai/pdf-extract --args '{"pdf_path":"doc.pdf"}'
```

### Verification

Check signatures on cached tools:

```bash
# Verify cached tool
enact verify acme-corp/data/processor

# Re-download and verify from registry
enact verify acme-corp/data/processor --remote
```

---

## Registry API

The Enact registry provides a simple REST API for tool storage and discovery.

### Download a Tool

```http
GET /api/tools/{org}/{path}/{tool}/v{version}
```

Returns:

```json
{
  "bundle_url": "https://cdn.enactprotocol.com/tools/org/path/tool-v1.2.3.tar.gz",
  "sigstore_bundle": {
    "mediaType": "application/vnd.dev.sigstore.bundle+json;version=0.3",
    "verificationMaterial": {...},
    "messageSignature": {...}
  },
  "metadata": {
    "name": "org/path/tool",
    "version": "1.2.3",
    "description": "Tool description",
    "published_at": "2025-10-24T15:30:00Z",
    "publisher_identity": "repo:org/repo:ref:refs/heads/main"
  }
}
```

The `sigstore_bundle` is included inline for efficient verification without additional requests.

### Publish a Tool

```http
POST /api/tools/{org}/{path}/{tool}/v{version}
Content-Type: multipart/form-data

Fields:
- tarball: <tool tarball file>
- sigstore_bundle: <JSON string>
```

The registry enforces namespace ownership and optionally verifies signatures before storing.

### Search Tools

```http
GET /api/tools/search?q={query}
```

Returns matching tools with metadata and publisher information.

For implementation details, see [Sigstore Implementation Guide](./sigstore.md).

---

## Best Practices

1. **Naming:** Use hierarchical paths (e.g., `org/category/tool-name`)
2. **Versions:** Pin exact versions in `command` fields
3. **Schemas:** Always provide `inputSchema` and `outputSchema`
4. **Containers:** Pin specific image tags, prefer minimal images
5. **Annotations:** Set appropriate behavior hints for safety
6. **Timeouts:** Set realistic timeout values
7. **Testing:** Include examples for validation
8. **Security:** Sign tools before public distribution

---

## Quick Command Reference

| Task | Command |
|------|---------|
| Install project tool | `enact install org/cat/tool` |
| Install all project tools | `enact install` |
| Install tool globally | `enact install org/cat/tool --global` |
| Create global tool | `cd my-tool && enact install . --global` |
| Test tool | `enact run org/cat/tool --args '{...}'` |
| Run custom command | `enact exec org/cat/tool "python script.py"` |
| Find tools | `enact search "keyword"` |
| Publish tool | `enact validate && enact sign && enact publish` |
| Verify tool | `enact verify org/cat/tool` |

### Recommended .gitignore

For projects using project-level tools:

```gitignore
# Keep the project manifest (team sync)
# .enact/tools.json should be committed

# Add other project-specific ignores as needed
node_modules/
.env
```

---

## Error Handling

### Signature Verification Failures

If a tool's signature cannot be verified, Enact will refuse to run it:

```bash
$ enact run untrusted/tool

✗ Signature verification failed for untrusted/tool@1.0.0

Reason: Certificate has expired
Publisher: repo:untrusted/tool:ref:refs/heads/main
Signed: 2025-09-15T10:23:45Z
Expired: 2025-09-15T10:43:45Z

This tool needs to be re-signed and re-published.

Try:
  • Contact the publisher to re-publish the tool
  • Search for alternative tools: enact search "tool functionality"
  • Check for newer versions: enact search untrusted/tool
```

There is no `--skip-verify` flag. If verification fails, the tool will not run.

### Certificate Revocation

```bash
$ enact run compromised/tool

✗ Signature verification failed for compromised/tool@2.1.0

Reason: Certificate revoked
Publisher: repo:compromised/tool:ref:refs/heads/main
Signed: 2025-10-15T10:23:45Z
Revoked: 2025-10-20T14:30:00Z

This tool's certificate was revoked by the publisher.
DO NOT install or execute this tool.
```

### Network Issues

If the registry is unreachable but you have a cached version:

```bash
$ enact run org/tool

⚠ Registry unreachable, using cached version

Tool: org/tool@1.2.0 (cached)
Last verified: 2025-10-20T10:15:00Z

Running cached tool...
```

---

## Resources

### Protocol Documentation

- **[Complete Protocol Specification](SPEC.md)** - Full technical specification of the Enact Protocol
- **[CLI Commands Reference](COMMANDS.md)** - Comprehensive guide to all CLI commands
- **[Sigstore Implementation Guide](SIGSTORE.md)** - Technical details on signature verification

### External Links

- **Documentation:** https://enactprotocol.com
- **GitHub:** https://github.com/EnactProtocol
- **Sigstore:** https://sigstore.dev

---

## License

MIT License © 2025 Enact Protocol Contributors