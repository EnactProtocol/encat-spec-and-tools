# Enact Protocol

A verified, portable way to define, discover, and safely run **AI-executable tools**.

Think **npm for AI tools**—publish once, run anywhere, with cryptographic verification and deterministic execution.

Each tool includes a self-contained `enact.md` manifest describing its inputs, outputs, environment, and execution command.

**What Enact provides:**
* 🔍 **Semantic discovery** — AI models and developers can find tools by task or capability
* 🛡️ **Verified execution** — Cryptographic attestations via Sigstore + container sandboxing
* 🔁 **Determinism** — Tools execute exactly as defined in their manifest
* 🧩 **Composition** — Tools can be combined in workflows
* 🗂️ **Versioning** — Semantic versions and reproducible, immutable bundles
* 🔐 **Trust control** — You decide which publishers and auditors to trust

---

## Prerequisites

* Node.js 18+ (for the CLI)
* Docker or compatible container runtime (for execution)
* Enact account (sign up at [enact.tools](https://enact.tools))

---

## Quick Start

### 1. Install the CLI

```bash
npm install -g @enactprotocol/cli
```

### 2. Create an Enact account

Sign up at [https://enact.tools](https://enact.tools) to claim your namespace.

Your username becomes your namespace (e.g., username `alice` can publish to `alice/*`).

### 3. Create a tool

Create an `enact.md` manifest:

```markdown
---
enact: "2.0.0"
name: "alice/utils/greeter"
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

### 4. Test locally

```bash
enact run . --args '{"name":"World"}'
# → Hello, World!
```

### 5. Publish

```bash
enact auth login
enact publish .
# ✓ Published alice/utils/greeter@v1.0.0
```

### 6. (Optional) Attest your tool

Self-attest your tool to build trust:

```bash
enact sign alice/utils/greeter@v1.0.0

? Sign attestation with:
  > GitHub
    Google
    Microsoft

# Opens browser for authentication
# ✓ Attestation published
  Signed by: github.com/alice
  Logged to Rekor: #123456
```

---

## Trust System

Enact uses a dual-identity trust model:

- **Publishers** (Enact usernames) - Who uploaded the tool
- **Auditors** (OIDC identities) - Who cryptographically attested the tool (Github, Gitlab, etc.)

You control which publishers and auditors you trust:

```bash
# Trust publishers (Enact accounts)
enact trust alice
enact trust EnactProtocol

# Trust auditors (OIDC identities)
enact trust github:EnactProtocol
enact trust google:security@company.com

# Remove trust
enact trust -r alice
enact trust -r github:sketchy-org
```

**When you install a tool:**
1. Is the publisher trusted ? → Install
2. Has a trusted auditor attested it? → Install
3. Neither? → Prompt or block based on policy

See [TRUST.md](docs/TRUST.md) for complete details.

---

## Installing Tools

```bash
# Install with trust verification
enact install alice/utils/greeter

Tool: alice/utils/greeter@v1.0.0
  Published by: @alice (Enact)
  
Attestations:
  ✓ github.com/EnactProtocol - passed
  
Trust Status: ✓ TRUSTED
Install? [Y/n]:

# Install for your project (tracked in .enact/tools.json)
enact install alice/utils/greeter

# Install globally
enact install alice/utils/greeter --global

# Install all project-defined tools
enact install
```

---

## Running Tools

**Deterministic execution** (only the manifest-defined command runs):

```bash
enact run alice/utils/greeter --args '{"name":"Alice"}'
# → Hello, Alice!
```

**Exploratory execution** (run arbitrary commands in the tool's environment):

```bash
enact exec alice/utils/greeter "cat enact.md"
```

---

## Auditing Tools

Anyone can review and attest tools:

```bash
# Download tool to review
enact download alice/utils/greeter@v1.0.0

# Review the code, run security scans, test it
# ...

# Sign if it passes
enact sign alice/utils/greeter@v1.0.0

# Or report issues
enact report alice/utils/greeter@v1.0.0 --reason "Security vulnerability found"
```

Your attestation is cryptographically signed via Sigstore and logged to the public Rekor transparency log.

---

## Discovery

```bash
# Search the registry
enact search "pdf extraction"

# View detailed tool information
enact get alice/utils/greeter

# Check tool's trust status and attestations
enact trust check alice/utils/greeter@v1.0.0

# List installed tools
enact list
```

---

## Directory Layout

Where Enact stores things:

| Location                         | Purpose                                              |
| -------------------------------- | ---------------------------------------------------- |
| `.enact/`                        | Project-installed tools (commit `.enact/tools.json`) |
| `~/.enact/tools/`                | Global installs                                      |
| `~/.enact/cache/`                | Immutable tool bundles for fast reinstalls           |
| `~/.enact/config.yaml`           | Trust configuration (publishers, auditors, policies) |
| `~/.enact/env/{org}/{path}/.env` | Namespaced environment variables                     |

---

## Trust Configuration

Example `~/.enact/config.yaml`:

```yaml
trust:
  # Trust these Enact publishers
  publishers:
    - EnactProtocol
    - alice
  
  # Trust these auditors (OIDC identities)
  auditors:
    - github:EnactProtocol
    - github:ossf
    - google:security@company.com
  
  # Policy: require_audit, prompt, or allow
  policy: prompt
  
  # Require at least this many trusted attestations
  minimum_attestations: 1
```

---

## Security Model

### What Enact Provides

✅ **Publisher identity** - Verified Enact accounts control namespaces  
✅ **Attestation authenticity** - Cryptographic proof via Sigstore  
✅ **Integrity** - Tools haven't been tampered with since attestation  
✅ **Transparency** - All attestations logged in public Rekor log  
✅ **User control** - You choose who to trust  
✅ **Container isolation** - Tools run in sandboxed environments  

### What Enact Does NOT Provide

❌ **Code quality guarantees** - Attestations verify identity, not correctness  
❌ **Auditor competence** - You must evaluate auditors yourself  
❌ **Continuous monitoring** - Attestations are point-in-time  
❌ **Absolute safety** - Always review tools before trusting them  

---

## Example Workflows

### Personal Developer

```bash
# Create and publish your own tools
enact publish .
enact sign alice/my-tool@v1.0

# Trust yourself
enact trust alice
enact trust github:alice

# Install your tools without prompts
enact install alice/my-tool
```

### Enterprise Team

```yaml
# ~/.enact/config.yaml
trust:
  auditors:
    - microsoft:security@company.com
    - github:company-security/*
  policy: require_audit
```

Only tools audited by your security team can be installed.

### Open Source Project

```bash
# Trust official auditors
enact trust github:EnactProtocol
enact trust github:ossf

# Install community tools
enact install community/useful-tool
# ✓ Verified by github.com/ossf
```

---

## CLI Commands

### Publishing
```bash
enact auth login               # Authenticate with Enact
enact publish .                # Publish tool to your namespace
enact sign tool@version        # Attest your own tool
```

### Trust Management
```bash
enact trust alice              # Trust publisher
enact trust github:auditor     # Trust auditor
enact trust -r alice           # Remove trust
enact trust list               # Show trusted identities
enact trust check tool@version # Check tool's trust status
```

### Installation
```bash
enact install tool             # Install with verification
enact install tool --global    # Install globally
enact install                  # Install all project tools
```

# Search the registry
enact search "pdf extraction"

# View detailed tool information
enact get username/utils/greeter

### Auditing
```bash


enact download tool@version    # Download for review
enact sign tool@version        # Attest if it passes
enact report tool@version      # Report issues
```

### Running
```bash
enact run tool --args '{...}'  # Deterministic execution
enact exec tool "command"      # Exploratory execution
```

### Discovery
```bash
enact search "query"           # Search registry
enact get tool                 # View tool details
enact list                     # List installed tools
```

---

## Learn More

* **Trust System** — [TRUST.md](docs/TRUST.md) - Complete guide to publishers, auditors, and attestations
* **Protocol Specification** — [SPEC.md](docs/SPEC.md) - Technical specification
* **CLI Commands** — [COMMANDS.md](docs/COMMANDS.md) - Full command reference
* **Sigstore Integration** — [SIGSTORE.md](docs/SIGSTORE.md) - How attestations work
* **Full Documentation** — [https://enactprotocol.com](https://enactprotocol.com)

---

## Getting Help

* **GitHub Issues** - [github.com/enactprotocol/cli/issues](https://github.com/enactprotocol/cli/issues)
* **Documentation** - [enactprotocol.com/docs](https://enactprotocol.com)

---


---

## License

MIT License © 2025 Enact Protocol Contributors