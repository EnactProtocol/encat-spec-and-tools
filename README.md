# Enact Protocol (Enact)

![Status: Alpha](https://img.shields.io/badge/Status-Alpha-yellow) ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) [![Discord](https://img.shields.io/badge/Discord-Enact_PROTOCOL-blue?logo=discord&logoColor=white)](https://discord.gg/mMfxvMtHyS)

The **Enact Protocol (Enact)** provides a standardized framework for defining and executing tasks. It enables the creation of reusable, composable, and verifiable capabilities that can be discovered and executed by AI agents and other automated systems.

## Overview

At its simplest, an Enact capability is a task with a structured description in YAML:

```yaml
enact: 1.0.0
id: HelloWorld
description: A simple Hello World example
tasks:
  - id: sayHello
    type: script
    language: python
    code: |
      print("Hello World")
```

Enact addresses a critical need in the AI ecosystem: as AI agents become more capable, they require reliable access to a diverse set of reliable tools and capabilities. Enact provides a standardized protocol for defining, discovering, and executing tasks that AI agents can use at runtime. Think of it as a universal interface between AI agents and the tools they need to get things done.

### Architecture

The Enact Protocol consists of several key components that work together:

```
┌─────────────────────────────────────────────────────────────┐
│                     Enact Ecosystem                         │
│                                                             │
│  ┌───────────────┐      ┌────────────────┐                  │
│  │ AI Agents &   │      │  Capability    │                  │
│  │ Applications  │◄────►│  Registry      │                  │
│  └───────────────┘      └────────────────┘                  │
│          ▲                      ▲                           │
│          │                      │                           │
│          ▼                      │                           │
│  ┌───────────────┐              │                           │
│  │   Execution   │              │                           │
│  │  Environment  │◄─────────────┘                           │
│  └───────────────┘                                          │
│          ▲                                                  │
│          │                                                  │
│          ▼                                                  │
│  ┌───────────────┐      ┌────────────────┐                  │
│  │ Atomic        │      │  Composite     │                  │
│  │ Capabilities  │◄────►│  Capabilities  │                  │
│  └───────────────┘      └────────────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```yaml
enact: 1.0.0
id: TemperatureConverter
description: Converts temperature from Celsius to Fahrenheit
version: 1.0.0
type: atomic
authors:
  - name: Your Name
    email: your.email@example.com
inputs:
  type: object
  properties:
    celsius:
      type: number
      description: Temperature in Celsius
  required: ["celsius"]
tasks:
  - id: convertTemperature
    type: script
    language: python
    code: |
      fahrenheit = celsius * 9/5 + 32
      return {"fahrenheit": fahrenheit}
outputs:
    type: object
    properties:
      fahrenheit:
        type: number
        description: Temperature in Fahrenheit
    required: ["fahrenheit"]
```

## Core Concepts

### Capabilities

A **capability** is a unit of functionality defined in YAML that follows the Enact Protocol Schema.

**Required Fields:**
```yaml
enact: 1.0.0              # Protocol version
id: string                # Unique identifier
description: string       # What the capability does
version: 1.0.0            # Capability version
type: atomic|composite    # Capability type
authors:                  # List of authors
  - name: string
inputs:                   # Input parameters (JSON Schema)
  type: object
  properties: {}          # JSON Schema properties
  required: []            # Required property names
tasks: array              # Task definitions (for atomic capabilities)
outputs:                  # Output parameters (JSON Schema)
  type: object
  properties: {}          # JSON Schema properties
  required: []            # Required property names
```

### Atomic Capabilities

Atomic capabilities are the basic building blocks of the Enact Protocol:

- Single, self-contained operations
- No dependencies on other capabilities
- Example: Making an API call, executing a script

In atomic capabilities, tasks are executed sequentially in the order they are defined in the `tasks` array.

```yaml
enact: 1.0.0
id: SimpleConverter
description: Converts temperature from Celsius to Fahrenheit
version: 1.0.0
type: atomic
authors:
  - name: John Smith
inputs:
    type: object
    properties:
      celsius:
        type: number
        description: Temperature in Celsius
        minimum: -273.15
    required: ["celsius"]
tasks:
  - id: convertTemperature
    type: script
    language: python
    code: |
      fahrenheit = celsius * 9/5 + 32
      return {"fahrenheit": fahrenheit}
outputs:
  type: object
  properties:
    fahrenheit:
      type: number
      description: Temperature in Fahrenheit
  required: ["fahrenheit"]
```

With enact you can also create more complicated workflows. For more details on composite capabilities, please see the [Composite Capabilities documentation](./composite-capabilities.md).

### Tasks

Tasks represent the executable units within a capability. Each task must have:

```yaml
tasks:
  - id: uniqueId          # Task identifier
    type: string          # Task type
    language: string      # For script tasks
    code: string          # Implementation
```

### Parameter Management with JSON Schema

**Input Parameters with JSON Schema:**
```yaml
inputs:
  type: object
  properties:
    paramName:
      type: string        # Data type (string, number, boolean, object, array)
      description: string # Parameter description
      format: string      # Optional format specifier
      default: any        # Optional default value
      # Any other JSON Schema validation keywords
  required: ["param1", "param2"]  # Array of required parameter names
```

**Output Parameters with JSON Schema:**
```yaml
outputs:
  type: object
  properties:
    paramName:
      type: string        # Data type (string, number, boolean, object, array)
      description: string # Parameter description
      format: string      # Optional format specifier
  required: ["param1"]    # Array of required parameter names
```

Enact's parameter definitions are fully compliant with JSON Schema, allowing for rich validation and documentation.

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
    email: jane@example.com

inputs:
  type: object
  properties:
    data:
      type: array
      description: Array of numerical values to analyze
      items:
        type: number
    options:
      type: object
      description: Configuration options for analysis
      properties:
        chart_type:
          type: string
          enum: ["bar", "line", "scatter"]
          default: "line"
        include_statistics:
          type: boolean
          default: true
  required: ["data"]

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

outputs:
  type: object
  properties:
    analysis:
      type: object
      description: Statistical analysis results
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
    visualization:
      type: string
      format: binary
      description: Base64 encoded plot
  required: ["analysis"]
```

### Environment Variables

Environment variables define the configuration and secrets required for capability execution. These are resolved at runtime by the Enact execution environment. All environment variables are treated as secrets by default to enhance security.
```yaml
env:
  type: object
  properties:
    vars:
      type: object
      properties:
        ENACT_AUTH_IDENTITY_KEY:
          type: string
          description: "API key for identity verification service"
        ENACT_EMAIL_SERVICE_KEY:
          type: string
          description: "API key for email service"
        ENACT_SLACK_WEBHOOK_URL:
          type: string
          description: "Webhook URL for Slack notifications"
          default: "https://hooks.slack.com/services/default-path"
      required: ["ENACT_AUTH_IDENTITY_KEY", "ENACT_EMAIL_SERVICE_KEY"]
  resources:
    memory: "1GB"
    timeout: "300s"
  required: ["vars"]
```

**Environment Variable Properties:**
- `name`: Identifier for the environment variable
- `description`: Human-readable description of the variable's purpose
- `required`: Whether the variable must be provided (`true`/`false`)
- `schema`: Full JSON Schema for the environment variable

All environment variables are treated as secrets by default and should be stored securely and never logged or exposed in execution traces.

### Resource Requirements

Resource requirements define the computational resources needed for capability execution:

```yaml
env:
  resources:
    memory: "1GB"     # Required memory allocation
    timeout: "300s"   # Maximum execution time
```

### Error Handling

It is recommended to handle errors using the standard `outputs` structure. A common pattern is to include error properties that are populated only when an error occurs:

```yaml
outputs:
  type: object
  properties:
    result:
      type: object
      description: The successful result of the operation (populated on success)
    error:
      type: object
      description: Error information (populated only when an error occurs)
      properties:
        message:
          type: string
          description: Human-readable error message
        code:
          type: string
          description: Machine-readable error code
        details:
          type: object
          description: Additional error details
  oneOf:
    - required: ["result"]
    - required: ["error"]
```

Example implementation in a Python task:

```python
try:
    # Task implementation
    result = process_data(data)
    return {
        "result": result,
        # No error field when successful
    }
except Exception as e:
    return {
        # No result field when error occurs
        "error": {
            "message": "Failed to process data",
            "code": "DATA_PROCESSING_ERROR",
            "details": {"exception": str(e)}
        }
    }
```

### Task Types

Enact supports the following task types:

| Type | Description | Status |
|------|-------------|--------|
| `script` | Execute code in a specified language | Available |
| `agent` | Agent operations | Coming soon |
| `prompt` | Return a prompt | Coming soon |
| `shell` | Execute shell commands | Coming soon |


## Schema Validation

Capabilities can be validated against the [Enact JSON Schema](./schema/enact-schema.json) to ensure they conform to the protocol specification.

## License

This project is licensed under the [MIT License](LICENSE).

---

© 2025 Enact Protocol Contributors