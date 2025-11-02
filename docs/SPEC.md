# Enact Protocol Field Specification

**Version:** 1.0.1
**Last Updated:** 2025-10-21

This document provides a comprehensive reference for all Enact protocol fields used in tool definitions.

---

## Required Fields

### `name`
- **Type:** `string`
- **Description:** Hierarchical tool identifier using filepath-style naming
- **Format:** `org/path/to/tool-name` (arbitrary depth, like Java packages)
- **Common pattern:** `org/category/tool-name` (but not prescribed)
- **Examples:**
  - `enact/text/analyzer` - Two levels
  - `acme-corp/internal/data/processor` - Three levels
  - `username/personal/utility` - Two levels
  - `mycompany/ai/nlp/sentiment/advanced-analyzer` - Five levels
- **Notes:**
  - Used for tool identity and prevents impersonation
  - No prescribed depth — use what makes sense for your organization
  - Like Java packages, deeper hierarchies provide better organization

### `description`
- **Type:** `string`
- **Description:** Human-readable description of what the tool does
- **Best Practice:** Include what it does and when to use it
- **Example:** `"Formats JavaScript/TypeScript code using Prettier"`

### `command`
- **Type:** `string`
- **Description:** Shell command to execute with parameter substitution
- **Format:** Uses `${parameter}` syntax for variable substitution
- **Examples:**
  ```yaml
  command: "echo 'Hello ${name}!'"
  command: "npx prettier@3.3.3 --write '${file}'"
  command: "python src/process.py --file='${file}' --operation='${operation}'"
  ```
- **Best Practice:** Use exact versions for reproducibility
- **Notes:**
  - Required for container-executed tools
  - Omitted for LLM-driven tools (tools without deterministic execution)

---

## Recommended Fields

### `enact`
- **Type:** `string`
- **Description:** Version of the Enact protocol specification
- **Format:** Semantic version (e.g., `"1.0.0"`)
- **Default:** Latest version at time of tool creation
- **Example:** `enact: "1.0.0"`

### `from`
- **Type:** `string`
- **Description:** Container base image for tool execution
- **Format:** Docker image name with tag
- **Examples:**
  - `from: "node:18-alpine"`
  - `from: "python:3.11-slim"`
  - `from: "ghcr.io/company/custom-env:v2.1.0"`
- **Default:** `"alpine:latest"` (if omitted)
- **Best Practice:** Pin specific tags, prefer minimal images (`alpine`, `slim`)

### `timeout`
- **Type:** `string`
- **Description:** Maximum execution time for the tool
- **Format:** Go duration format
- **Examples:** `"30s"`, `"5m"`, `"1h"`
- **Default:** `"30s"`
- **Notes:** Critical for preventing DoS attacks

### `version`
- **Type:** `string`
- **Description:** Tool version (not protocol version)
- **Format:** Semantic versioning (major.minor.patch)
- **Example:** `version: "1.2.3"`
- **Best Practice:** Follow semver conventions

### `license`
- **Type:** `string`
- **Description:** Software license for the tool
- **Format:** SPDX license identifier
- **Examples:** `"MIT"`, `"Apache-2.0"`, `"GPL-3.0"`
- **Best Practice:** Always include for published tools

### `tags`
- **Type:** `array of strings`
- **Description:** Keywords for tool discovery and categorization
- **Example:**
  ```yaml
  tags:
    - text
    - analysis
    - nlp
  ```
- **Best Practice:** Use relevant, searchable terms

---

## Schema Fields

### `inputSchema`
- **Type:** `object` (JSON Schema)
- **Description:** Defines the structure and validation for tool input parameters
- **Format:** JSON Schema (typically `type: object`)
- **Example:**
  ```yaml
  inputSchema:
    type: object
    properties:
      file:
        type: string
        description: "Path to file to process"
      operation:
        type: string
        enum: ["summarize", "validate", "transform"]
    required: ["file", "operation"]
  ```
- **Best Practice:** Always include for container-executed tools
- **Notes:** Helps AI models use tools correctly

### `outputSchema`
- **Type:** `object` (JSON Schema)
- **Description:** Defines the structure of tool output
- **Format:** JSON Schema
- **Example:**
  ```yaml
  outputSchema:
    type: object
    properties:
      status:
        type: string
        enum: ["success", "error"]
      result:
        type: object
      errors:
        type: array
        items:
          type: string
  ```
- **Best Practice:** Strongly recommended for all tools
- **Notes:** Enables structured output validation

---

## Environment Variables

### `env`
- **Type:** `object`
- **Description:** Environment variable configuration for the tool
- **Package Scope:** Variables are shared across all tools in the same namespace (parent path)
- **Storage:** `~/.enact/env/{org}/{path}/.env` (namespace-based sharing)
- **Sharing examples:**
  - `acme-corp/api/slack-notifier` → `~/.enact/env/acme-corp/api/.env`
  - `acme-corp/api/discord-bot` → `~/.enact/env/acme-corp/api/.env` (shares with slack-notifier)
  - `acme-corp/data/processors/csv` → `~/.enact/env/acme-corp/data/processors/.env`
- **Structure:**
  ```yaml
  env:
    VARIABLE_NAME:
      description: string    # What this variable is for (required)
      source: string         # Where to get this value (required)
      required: boolean      # Whether this is required (required)
      default: string        # Default value if not set (optional)
  ```
- **Example:**
  ```yaml
  env:
    API_KEY:
      description: "API key for external service"
      source: "https://service.com/settings"
      required: true
      default: "optional-default-value"
  ```

---

## Behavior Annotations

### `annotations`
- **Type:** `object`
- **Description:** Hints about tool behavior for AI models
- **All fields default to `false`**
- **Fields:**

#### `title`
- **Type:** `string`
- **Description:** Human-readable display name
- **Optional**

#### `readOnlyHint`
- **Type:** `boolean`
- **Description:** Tool does not modify the environment
- **Example use:** Read-only operations, analysis tools

#### `destructiveHint`
- **Type:** `boolean`
- **Description:** Tool may make irreversible changes
- **Example use:** Delete operations, file modifications

#### `idempotentHint`
- **Type:** `boolean`
- **Description:** Multiple executions produce the same result
- **Example use:** Stateless transformations

#### `openWorldHint`
- **Type:** `boolean`
- **Description:** Tool interacts with external systems (network, APIs)
- **Example use:** Web scraping, API calls

**Example:**
```yaml
annotations:
  title: "Data Analyzer"
  readOnlyHint: true
  destructiveHint: false
  idempotentHint: true
  openWorldHint: false
```

---

## Resource Requirements

### `resources`
- **Type:** `object`
- **Description:** Resource limits and requirements for tool execution
- **Fields:**

#### `memory`
- **Type:** `string`
- **Description:** System memory needed
- **Format:** Kubernetes-style units
- **Examples:** `"512Mi"`, `"2Gi"`, `"16Gi"`

#### `gpu`
- **Type:** `string`
- **Description:** GPU memory needed
- **Format:** Kubernetes-style units
- **Examples:** `"24Gi"`, `"48Gi"`

#### `disk`
- **Type:** `string`
- **Description:** Disk space needed
- **Format:** Kubernetes-style units
- **Examples:** `"100Gi"`, `"500Gi"`, `"1Ti"`

**Example:**
```yaml
resources:
  memory: "2Gi"
  gpu: "24Gi"
  disk: "100Gi"
```

---

## Documentation Fields

### `doc`
- **Type:** `string`
- **Description:** Extended Markdown documentation for the tool
- **Format:** Markdown
- **Best Practice:** Keep brief in YAML; use separate `.md` files for extensive docs

### `authors`
- **Type:** `array of objects`
- **Description:** Tool creators and maintainers
- **Structure:**
  ```yaml
  authors:
    - name: string     # Author name (required)
      email: string    # Author email (optional)
      url: string      # Author website (optional)
  ```
- **Example:**
  ```yaml
  authors:
    - name: "Alice Developer"
      email: "alice@acme-corp.com"
      url: "https://example.com"
  ```

---

## Testing and Examples

### `examples`
- **Type:** `array of objects`
- **Description:** Test cases and expected outputs for validation
- **Structure:**
  ```yaml
  examples:
    - input: object         # Input parameters (optional, omit for no-input tools)
      output: any           # Expected output (optional)
      description: string   # Test description (optional)
  ```
- **Example:**
  ```yaml
  examples:
    - input:
        file: "data.csv"
        operation: "validate"
      output:
        status: "success"
        result:
          valid: true
          rows: 1000
      description: "Validate CSV structure"
  ```

---

## Security and Signing

Enact uses **Sigstore** for cryptographic signing and verification of published tools. Signatures are **not stored in the tool metadata file** but in separate `.sigstore-bundle` files alongside tool bundles.

### Sigstore-Based Signing

**How it works:**
1. **Local tools** (`~/.enact/local/`) do not require signing (trusted environment)
2. **Published tools** are signed using Sigstore before distribution
3. **Signature bundles** (`.sigstore-bundle`) contain:
   - Short-lived X.509 certificates from Fulcio (Certificate Authority)
   - ECDSA P-256 signatures
   - Rekor transparency log entries
   - Identity claims (GitHub OAuth, SSO)

**Signing process:**
```bash
$ enact sign my-tool/
Creating bundle...
├─ Creating tarball: my-tool-v1.0.0.tar.gz
├─ Computing SHA256 hash: abc123...
└─ ✓ Bundle created

Signing with Sigstore...
├─ Authenticating with GitHub OAuth...
├─ ✓ Authenticated as alice@acme-corp.com
├─ Requesting certificate from Fulcio...
├─ ✓ Issued: 10 minute validity
├─ Generating ECDSA P-256 signature...
├─ Submitting to Rekor transparency log...
├─ ✓ Logged at index: 12347
└─ ✓ Created: my-tool.sigstore-bundle
```

**Verification checks:**
1. Bundle integrity (SHA-256 hash)
2. Signature validity (ECDSA P-256)
3. Certificate chain to Fulcio CA
4. Rekor transparency log proof
5. Certificate revocation status (CRL)
6. Identity claims in certificate

**Storage locations:**
- Active tools: `~/.enact/tools/{org}/{path}/{tool}/` - No signature required (user-controlled)
- Cached bundles: `~/.enact/cache/{org}/{path}/{tool}/v{version}/` - Verified on download from registry
- Signature bundles: Stored alongside cached bundles as `.sigstore-bundle`

**Security benefits:**
- Identity-based certificates (no long-lived keys)
- Immutable audit trail (Rekor)
- Real-time revocation (CRL)
- Public auditability

---

## Custom Extensions

### `x-*` prefix
- **Type:** Any
- **Description:** Custom fields for implementation-specific or organizational metadata
- **Format:** Must start with `x-`
- **Not included in signature verification**
- **Examples:**
  ```yaml
  x-internal-id: "tool-12345"
  x-team-owner: "platform-team"
  x-cost-center: "engineering"
  x-compliance-level: "high"
  ```

---

## Signed Content

When publishing tools, Sigstore signs the **entire tool bundle** (tarball). The signature covers:

**What gets signed:**
- The complete tarball (`.tar.gz`) containing:
  - Tool metadata file (`enact.md`)
  - Source code and dependencies
  - Documentation files
  - All resources

**Hash computation:**
- SHA-256 hash of the entire tarball
- Any modification to any file breaks the signature
- Ensures complete bundle integrity

**What is NOT signed in the metadata:**
- Signatures are stored separately in `.sigstore-bundle` files
- The tool metadata file does not contain signature fields
- This keeps the metadata clean and focused on tool definition

**Example:**
```bash
# Tool structure
my-tool/
├── enact.md           # Tool metadata and documentation
├── src/               # Source code
└── RESOURCES.md       # Additional documentation (optional)

# After signing
my-tool-v1.0.0.tar.gz           # Signed tarball
my-tool.sigstore-bundle         # Signature + certificate + Rekor proof
```

---

## File Format

All Enact tools use **`enact.md`** — a Markdown file with YAML frontmatter.

### Structure
- **YAML frontmatter** contains structured metadata
- **Markdown body** contains human-readable documentation and instructions
- Example:
  ```markdown
  ---
  enact: "1.0.0"
  name: "org/category/tool"
  description: "Tool description"
  command: "python src/main.py ${args}"  # Optional
  ---

  # Tool Name

  Detailed documentation in Markdown format.

  ## Usage
  ...
  ```

### Execution Model

The presence of a `command` field determines execution:
- **With `command`** → Container-executed (deterministic)
- **Without `command`** → LLM-driven (instructions interpreted by AI)

---

## Tool Types

### Container-Executed Tools
- **Has:** `command` field
- **Execution:** Runs in isolated Dagger container
- **Characteristics:** Deterministic, reproducible
- **Format:** `enact.md` with command in frontmatter

### LLM-Driven Tools
- **No:** `command` field
- **Execution:** Instructions interpreted by LLM
- **Characteristics:** Non-deterministic, flexible
- **Format:** `enact.md` with rich documentation in body
- **Supports:** Progressive disclosure (on-demand content loading)

---

## Directory Structure

### Active User-Level Tools
```
~/.enact/tools/
└── {org}/
    └── {path}/                      # Arbitrary depth hierarchy (like Java packages)
        └── {to}/
            └── {tool}/
                ├── enact.md         # Tool definition
                ├── src/             # Built source code (if any)
                ├── dist/            # Compiled output (if any)
                ├── node_modules/    # Dependencies (if any)
                └── RESOURCES.md     # Additional docs (for progressive disclosure)
```

**Examples:**
```
~/.enact/tools/acme-corp/api/slack-notifier/
~/.enact/tools/mycompany/ai/nlp/sentiment/analyzer/
~/.enact/tools/username/utils/helper/
```

**Notes:**
- These are the "active" installed tools (like npm global installs)
- No version directory - only one active version at a time per tool
- Can be modified/customized by the user
- Created when you run `enact install --global` or `enact install .`

### Immutable Cached Bundles
```
~/.enact/cache/
└── {org}/
    └── {path}/                      # Arbitrary depth hierarchy
        └── {to}/
            └── {tool}/
                └── v1.0.0/          # Specific version (immutable)
                    ├── bundle.tar.gz
                    ├── .sigstore-bundle
                    └── metadata.json
```

**Examples:**
```
~/.enact/cache/acme-corp/api/slack-notifier/v1.0.0/
~/.enact/cache/acme-corp/api/slack-notifier/v1.0.1/
~/.enact/cache/mycompany/ai/nlp/sentiment/analyzer/v2.3.0/
```

**Notes:**
- Immutable, versioned artifacts
- Can store multiple versions simultaneously
- Used for instant reinstall, project reproducibility
- Verified signatures stored here
- Created automatically during install or download

### Project-Level Tools
```
my-project/
├── .enact/
│   ├── tools.json               # Project manifest (commit to git)
│   └── {org}/
│       └── {path}/
│           └── {tool}/
│               ├── enact.md
│               └── ...
```

**Notes:**
- Tools installed for specific projects only
- Created when you run `enact install <tool>` (without --global)
- Team members can sync via `tools.json`

### Environment Variables
```
~/.enact/env/
└── {org}/{namespace-path}/.env      # Shared by namespace
```

**Examples:**
```
~/.enact/env/acme-corp/api/.env                    # Shared by all acme-corp/api/* tools
~/.enact/env/mycompany/ai/nlp/.env                 # Shared by all mycompany/ai/nlp/* tools
~/.enact/env/username/utils/.env                   # Shared by all username/utils/* tools
```

---

## Best Practices Summary

1. **Naming:** Use hierarchical paths like Java packages (e.g., `org/category/tool-name` or deeper as needed)
2. **Versions:** Pin exact versions in `command` fields (e.g., `npx prettier@3.3.3`)
3. **Schemas:** Always provide `inputSchema` and `outputSchema`
4. **Containers:** Pin specific image tags, prefer minimal images
5. **Annotations:** Set appropriate behavior hints for safety
6. **Documentation:** Include clear descriptions and examples
7. **Security:** Sign tools before public distribution
8. **Timeouts:** Set realistic timeout values
9. **Resources:** Specify resource limits for resource-intensive tools
10. **Testing:** Include examples for validation

---

## References

- **Full Specification:** [new.md](new.md)
- **Implementation Guide:** [README.md](README.md)
- **Examples:** See `examples/` directory
- **JSON Schema:** `schema.json` (for validation)

---

## License

MIT License

© 2025 Enact Protocol Contributors
