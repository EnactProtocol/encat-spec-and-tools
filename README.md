# Enact Protocol (Enact)

![Status: Alpha](https://img.shields.io/badge/Status-Alpha-yellow) ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) [![Discord](https://img.shields.io/badge/Discord-Enact_PROTOCOL-blue?logo=discord&logoColor=white)](https://discord.gg/mMfxvMtHyS)

The **Enact Protocol (Enact)** provides a standardized framework for defining and executing automated tasks and workflows. It enables the creation of reusable, composable, and verifiable capabilities that can be discovered and executed in a structured, auditable environment.

## Overview
As AI agents become more capable, they need reliable access to a diverse set of tools and capabilities. Enact provides a standardized protocol for defining, discovering, and executing tasks that AI agents can use at runtime. Think of it as a universal interface between AI agents and the tools they need to get things done.

**Example Scenario:**

```yaml
enact: 1.0.0
id: GetStockPrice
description: Retrieves the current stock price for a given ticker symbol.
version: 1.0.0
type: atomic
authors:
  - name: Jane Doe
inputs:
  - name: ticker
    description: The stock ticker symbol (e.g., AAPL)
    required: true
    schema:
      type: string
tasks:
  - id: fetchPrice
    type: script
    language: python
    code: |
      # Task implementation
flow:
  steps:
    - task: fetchPrice
outputs:
  - name: price
    description: The current stock price
    schema:
      type: number
      format: float
```


## Core Concepts

### Capabilities

A **capability** is a unit of functionality defined in YAML that follows the Enact Protocol Schema. It can be either atomic (single operation) or composite (workflow combining multiple capabilities).

**Required Fields:**
```yaml
enact: 1.0.0              # Protocol version
id: string                # Unique identifier
description: string       # What the capability does
version: 1.0.0           # Capability version
type: atomic|composite    # Capability type
authors:                  # List of authors
  - name: string
inputs:                  # Input parameters (array)
  - name: string
    description: string
    required: boolean
    schema: object       # OpenAPI-style schema
tasks: array             # Task definitions
flow: object            # Execution flow
outputs:                # Output parameters (array)
  - name: string
    description: string
    schema: object      # OpenAPI-style schema
```

### Capability Types

**Atomic Capabilities**
- Single, self-contained operation
- No dependencies on other capabilities
- Example: Making an API call, executing a script

**(Coming Soon) Composite Capabilities**
- Combines multiple atomic capabilities
- Defines workflow between capabilities
- Example: Multi-step data processing pipeline

### Tasks

Tasks represent the executable units within a capability. Each task must have:

```yaml
tasks:
  - id: uniqueId           # Task identifier
    type: string          # Task type (script, request, etc.)
    language: string      # For script tasks
    code: string         # Implementation
```

### Task Types

- `script`: Execute code in specified language

### Flow Control

The flow section defines how tasks are executed:

```yaml
flow:
  steps:
    - task: taskId        # Reference to task
```

### Parameter Management

**Input Parameters:**
```yaml
inputs:
  - name: paramName
    description: string    # Parameter description
    required: boolean      # Whether parameter is required
    schema:                # OpenAPI-style schema
      type: string         # Data type
      format: string       # Optional format specifier
      default: any         # Optional default value
```

**Output Parameters:**
```yaml
outputs:
  - name: paramName
    description: string    # Parameter description
    schema:                # OpenAPI-style schema
      type: string         # Data type
      format: string       # Optional format specifier
```

### Dependencies

Dependencies define the runtime requirements for executing a capability. They can specify language versions, packages, and other external requirements.

```yaml         
dependencies:
    version: string     # Runtime version requirement
    packages:           # Required packages
      - name: string    # Package name
        version: string # Version specifier
```

Example with dependencies:

```yaml
enact: 1.0.0
id: DataAnalyzer
description: Analyzes numerical data and creates visualizations
version: 1.0.0
type: atomic
authors:
  - name: Jane Doe

inputs:
  - name: data
    description: Array of numerical values to analyze
    required: true
    schema:
      type: array
      items:
        type: number
  - name: options
    description: Configuration options for analysis
    required: false
    schema:
      type: object
      properties:
        chart_type:
          type: string
          enum: ["bar", "line", "scatter"]
          default: "line"
        include_statistics:
          type: boolean
          default: true
tasks:
  - id: analyzeData
    type: script
    language: python
    dependencies:
      version: ">=3.9,<4.0"
      packages:
        - name: pandas
          version: ">=2.0.0,<3.0.0"
        - name: numpy
          version: ">=1.24.0"
        - name: matplotlib
          version: ">=3.7.0"
    code: |
      # Implementation using pandas, numpy, and matplotlib
flow:
  steps:
    - task: analyzeData
outputs:
  - name: analysis
    description: Statistical analysis results
    schema:
      type: object
      properties:
        mean:
          type: number
        median:
          type: number
        std:
          type: number
        min:
          type: number
        max:
          type: number
  - name: visualization
    description: Base64 encoded plot
    schema:
      type: string
      format: binary
```

### Environment Variables

Environment variables define the configuration and secrets required for capability execution. These are resolved at runtime by the Enact execution environment. All environment variables are treated as secrets by default to enhance security.

```yaml
env:
  vars:
    - name: API_KEY_IDENTITY
      description: "API key for identity verification service"
      required: true
    - name: EMAIL_SERVICE_API_KEY
      description: "API key for email service"
      required: true
    - name: SLACK_WEBHOOK_URL
      description: "Webhook URL for Slack notifications"
      required: true
      schema:
        type: string
        default: "https://hooks.slack.com/services/default-path" # Optional default
  resources:
    memory: "1GB"
    timeout: "300s"
```

**Environment Variable Properties:**
- `name`: Identifier for the environment variable
- `description`: Human-readable description of the variable's purpose
- `required`: Whether the variable must be provided (`true`/`false`)
- `schema`: OpenAPI-style schema with optional default value

**Environment Variables Resolution:**
The Enact runtime resolves environment variables from multiple possible sources in the following order:
1. Execution context provided variables
2. User-configured environment variable service
3. Local environment variables
4. Default values specified in the capability definition

All environment variables are treated as secrets by default and should be stored securely and never logged or exposed in execution traces.

### Resource Requirements

Resource requirements define the computational resources needed for capability execution:

```yaml
env:
  resources:
    memory: "1GB"     # Required memory allocation
    timeout: "300s"   # Maximum execution time
```

## Best Practices

1. **Atomic Capability Design**
   - Keep capabilities focused on single responsibility
   - Make inputs and outputs explicit
   - Include proper error handling

2. **Composite Capability Design**
   - Define clear dependencies
   - Handle task failures gracefully
   - Document the workflow clearly

3. **Environment Variable Management**
   - Clearly document all required environment variables
   - Remember that all environment variables are treated as secrets by default
   - Provide defaults only when absolutely necessary and safe to do so
   - Consider offering multiple resolution strategies for variables (e.g., from registry, local env, etc.)
   - Validate all required variables before starting execution

## License

This project is licensed under the [MIT License](LICENSE).