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
  ticker: 
    type: string
    description: The stock ticker symbol (e.g., AAPL)
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
  price: 
    type: number
    format: float
    description: The current stock price
```

## Core Features

- **Composability:** Build complex workflows from simple atomic capabilities
- **Version Control:** Built-in versioning for capabilities and their dependencies
- **Task Orchestration:** Structured flow control for executing multiple tasks
- **Input/Output Contracts:** Clear definitions of data requirements and produced results

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
inputs: object           # Input parameters
tasks: array             # Task definitions
flow: object            # Execution flow
outputs: object         # Output parameters
```

### Capability Types

**Atomic Capabilities**
- Single, self-contained operation
- No dependencies on other capabilities
- Example: Making an API call, executing a script

**Composite Capabilities**
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

**Additional types can be defined as needed**
- `request`: Make HTTP/API calls
- `prompt`: feeds a prompt to the agent

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
  paramName:
    type: string         # Data type
    description: string  # Parameter description
    format: string      # Optional format specifier
    default: any        # Optional default value
```

**Output Parameters:**
```yaml
outputs:
  paramName:
    type: string         # Data type
    description: string  # Parameter description
    format: string      # Optional format specifier
```

### Dependencies

Dependencies define the runtime requirements for executing a capability. They can specify language versions, packages, and other external requirements.

```yaml
dependencies:            # Optional dependencies section
  python:               # Runtime identifier
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
dependencies:
  python:
    version: ">=3.9,<4.0"
    packages:
      - name: pandas
        version: ">=2.0.0,<3.0.0"
      - name: numpy
        version: ">=1.24.0"
      - name: matplotlib
        version: ">=3.7.0"
inputs:
  data: 
    type: array
    description: Array of numerical values to analyze
tasks:
  - id: analyzeData
    type: script
    language: python
    code: |
      # Implementation using pandas, numpy, and matplotlib
flow:
  steps:
    - task: analyzeData
outputs:
  analysis:
    type: object
    description: Statistical analysis results
  visualization:
    type: string
    format: base64
    description: Base64 encoded plot
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

## License

This project is licensed under the [MIT License](LICENSE).