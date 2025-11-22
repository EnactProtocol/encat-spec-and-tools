# MCP Integration

Enact includes a native **Model Context Protocol (MCP)** server. This allows AI assistants (like Claude Desktop, IDE agents, or custom LLM loops) to interface directly with your Enact toolchain.

Instead of asking an Agent to "write a shell command," the MCP server projects installed Enact tools as native Agentic functions with structured schemas.

## Standard MCP Tools

The server exposes a set of "Meta-Tools" for managing the Enact environment:

| MCP Tool Name | Enact CLI Equivalent | Purpose |
| :--- | :--- | :--- |
| **`enact_search`** | `enact search` | **Discovery.** Finds tools in the registry or cache. |
| **`enact_inspect`** | `enact get` | **Learning.** Retrieves instructions, schemas, and context. |
| **`enact_install`** | `enact install` | **Acquisition.** Downloads and verifies a tool. |
| **`enact_list`** | `enact list` | **Inventory.** Lists currently available tools. |
| **`enact_exec`** | `enact exec` | **Debugging.** Runs arbitrary shell commands (Sandboxed). |

## Dynamic Tool Projection

This is the core power of Enact MCP. Any tool installed in your environment is **automatically projected** as a first-class MCP tool.

The Enact MCP server reads the `input` schema from `enact.md` and converts it to an MCP Tool Schema on the fly.

**Example:**
If you have `my-org/utils/weather` installed, the Agent sees:

```json
{
  "name": "weather",
  "description": "Fetches weather data (Projected from my-org/utils/weather)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "city": { "type": "string" }
    }
  }
}
```

When the Agent calls this tool, Enact automatically translates it to:
`enact run my-org/utils/weather --args '{"city": "Paris"}'`

## Tool Semantics

### `enact_search`

  * **Agent Intent:** "I need a tool that does X."
  * **Behavior:** Semantically searches the registry tags and descriptions. Returns a list of candidates with their installation commands.

### `enact_inspect`

  * **Agent Intent:** "How does this tool work?" or "Read the documentation."
  * **Behavior:** Returns the parsed `enact.md`.
      * For **Container Tools**, it returns the input schema and description.
      * For **LLM Tools**, it returns the Markdown body (instructions) so the Agent can internalize the logic before execution.

### `enact_install`

  * **Agent Intent:** "Download this tool."
  * **Behavior:** Performs `enact install <tool>`.
  * *Security Note:* The MCP server will trigger signature verification. If verification fails, the tool raises an error to the Agent.

### `enact_run` (Generic)

  * **Agent Intent:** "Run a tool using its full ID."
  * **Behavior:** Useful for running tools that aren't locally installed yet, or when the Agent wants to be explicit about the namespace (e.g., `enact_run(tool="acme/data/processor", args={...})`).

### `enact_exec`

  * **Agent Intent:** "Run a custom command inside the tool's environment."
  * **Behavior:** Executes raw shell commands inside the container.
  * *Safety:* This is a privileged action. Agents should use this primarily for debugging or when the standard `command` is insufficient.

