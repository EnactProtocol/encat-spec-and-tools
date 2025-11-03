# Enact Protocol

A verified, portable way to define, discover, and safely run AI‑executable tools. Think npm for AI tools—publish once, run anywhere, with cryptographic verification.

Each tool is a self‑describing `enact.md` manifest with inputs, outputs, environment, and a signed execution command.

**Key features:**
- Discoverable by AI models via semantic search
- Safe, reproducible execution in containers
- Cryptographic verification with Sigstore
- Semantic versioning and tool composition

## Prerequisites

- Node.js 18+ (for the CLI)
- Docker or compatible container runtime (for tool execution)

## Quick Start

Install the CLI:

```bash
npm install -g @enactprotocol/cli
```

Create a tool (`enact.md`):

```markdown
---
enact: "1.0.0"
name: "username/utils/greeter"
description: "Greets the user by name"
command: "echo 'Hello, ${name}!'"
inputSchema:
  type: object
  properties:
    name: { type: string }
  required: ["name"]
---

# Greeter
A simple tool that greets users by name.
```

Run and publish:

```bash
# Run locally (no registry needed)
enact run . --args '{"name":"World"}'
# Output: Hello, World!

# Sign and publish to the registry
enact sign .
enact publish .
```

**Installing tools:**

```bash
# Install tool for your project (shared with team via .enact/tools.json)
enact install username/utils/greeter

# Install tool globally for your user account
enact install username/utils/greeter --global

# Install all tools defined in your project's .enact/tools.json
enact install
```

## Run vs Exec

- enact run — Execute the tool’s signed, declared command (deterministic):
```bash
enact run org/cat/tool --args '{"file":"data.csv"}'
```

- enact exec — Run any command inside the tool’s environment (great for exploration):
```bash
enact exec org/cat/tool "python utils/validate.py data.csv"
```

## Where things live

- Project tools: `.enact/` in your repo (commit `.enact/tools.json`)
- User tools (global): `~/.enact/tools/` (active installs)
- Cache (immutable bundles): `~/.enact/cache/` (fast reinstalls)
- Environment variables (namespaced): `~/.enact/env/{org}/{path}/.env`

## Discovery

```bash
# Search the registry for tools
enact search "pdf extraction"

# Get detailed info about a tool
enact get username/utils/greeter

# List your installed tools
enact list
```

## Learn more

- [Complete Protocol Specification](docs/SPEC.md) - Full technical details
- [CLI Commands Reference](docs/COMMANDS.md) - All available commands
- [Sigstore Implementation Guide](docs/SIGSTORE.md) - How signatures work
- [Examples](examples/) - Sample tools and use cases
- [Documentation](https://enactprotocol.com) - Full guides and tutorials

## License

MIT License © 2025 Enact Protocol Contributors