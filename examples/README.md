# Enact Tool Examples

This directory contains example tools demonstrating the **enact.md** format and various Enact protocol features.

## Format Overview

All Enact tools are defined in a single **`enact.md`** file that combines:

1. **YAML frontmatter** (between `---` delimiters) - Machine-readable metadata
2. **Markdown body** - Human-readable documentation and instructions

This unified format serves as the single source of truth for both AI models and human developers.

## Examples

### 1. [greeter/](greeter/) - Basic Example
**Type:** Container-executed (has `command` field)

The simplest possible Enact tool. Shows:
- Minimal required fields (`name`, `description`, `command`)
- Basic input schema
- Parameter substitution with `${name}`

Perfect starting point for understanding the enact.md format.

### 2. [complete-tool/](complete-tool/) - Full Feature Set
**Type:** Container-executed (has `command` field)

Comprehensive example demonstrating all Enact features:
- Container image specification (`from`)
- Input/output schemas
- Environment variables with defaults
- Resource requirements (memory, disk)
- Behavior annotations
- Test examples
- Multiple authors
- Tags and license

Use this as a reference for production tools.

### 3. [custom-extensions/](custom-extensions/) - Enterprise Metadata
**Type:** Container-executed (has `command` field)

Shows how to add organization-specific metadata using the `x-*` prefix:
- Internal tracking (`x-internal-id`, `x-cost-center`)
- Monitoring integration (`x-monitoring`)
- Security & compliance (`x-security`, `x-compliance`)
- Ownership info (`x-ownership`)
- Deployment configuration (`x-deployment`)

Perfect for enterprise environments with internal tooling.

### 4. [llm-driven-analyzer/](llm-driven-analyzer/) - LLM-Driven Tool
**Type:** LLM-driven (NO `command` field)

AI-powered code review tool without deterministic execution:
- No `command` field - LLM interprets instructions
- Rich documentation in Markdown body
- Detailed step-by-step instructions for LLM
- Complex reasoning and analysis tasks
- Non-deterministic output

Demonstrates how to create tools that leverage LLM capabilities.

## File Structure

Each example follows this structure:

```
example-name/
├── enact.md           # Tool definition (YAML + Markdown)
└── RESOURCES.md       # Optional: Progressive disclosure content
```

## Legacy Examples

The old `.yaml` examples in the root are deprecated:
- `complete-tool.yaml` → See [complete-tool/enact.md](complete-tool/enact.md)
- `custom-extensions.yaml` → See [custom-extensions/enact.md](custom-extensions/enact.md)

These will be removed in a future version.

## Tool Types

### Container-Executed Tools
- **Have:** `command` field in YAML frontmatter
- **Execution:** Run in isolated Dagger containers
- **Characteristics:** Deterministic, reproducible
- **Examples:** greeter, complete-tool, custom-extensions

### LLM-Driven Tools
- **Have:** NO `command` field in YAML frontmatter
- **Execution:** Markdown instructions interpreted by LLM
- **Characteristics:** Non-deterministic, flexible, intelligent
- **Examples:** llm-driven-analyzer

## Creating Your Own Tool

1. Create a directory: `mkdir my-tool/`
2. Create `enact.md` with YAML frontmatter + Markdown body
3. Define required fields: `name`, `description`
4. Add `command` for container-executed tools, or omit for LLM-driven tools
5. Test locally: `enact run . --args '{"param":"value"}'`

## Validation

Validate your enact.md against the schema:

```bash
# Using the Enact CLI
enact validate my-tool/enact.md

# Or manually with a JSON Schema validator
yaml2json my-tool/enact.md | jq '.frontmatter' | \
  jsonschema -i /dev/stdin ../schema/enact-schema.json
```

## More Information

- **Specification:** [../docs/SPEC.md](../docs/SPEC.md)
- **Schema:** [../schema/enact-schema.json](../schema/enact-schema.json)
- **Main README:** [../README.md](../README.md)

---

## License

MIT License © 2025 Enact Protocol Contributors
