# Enact Protocol (Enact)

![Status: Alpha](https://img.shields.io/badge/Status-Alpha-yellow) ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) [![Discord](https://img.shields.io/badge/Discord-Enact_PROTOCOL-blue?logo=discord&logoColor=white)](https://discord.gg/mMfxvMtHyS)

The **Enact Protocol (Enact)** provides a standardized framework for defining and executing tasks. It enables the creation of reusable, composable, and verifiable capabilities that can be discovered and executed.

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
    email: jane@example.com
    url: https://example.com/jane
inputs:
  ticker:
    type: string
    description: The stock ticker symbol (e.g., AAPL)
    required: true
tasks:
  - id: fetchPrice
    type: script
    language: python
    code: |
      # Task implementation
outputs:
  price:
    type: number
    format: float
    description: The current stock price
```


## Core Concepts

### Capabilities

A **capability** is a unit of functionality defined in YAML that follows the Enact Protocol Schema. It can be either atomic (single operation) or composite (workflow combining multiple capabilities).

**Required Fields:**
```yaml
enact: 1.0.0              # Protocol version
id: string                # Unique identifier
description: string       # What the capability does
version: 1.0.0            # Capability version
type: atomic|composite    # Capability type
authors:                  # List of authors
  - name: string
inputs:                   # Input parameters (object)
  paramName:
    type: string          # Data type
    description: string   # Parameter description
    required: boolean     # Whether parameter is required
tasks: array              # Task definitions (for atomic capabilities)
imports: array            # Imported capabilities (for composite capabilities)
flow: object              # Flow control (for composite capabilities)
outputs:                  # Output parameters (object)
  paramName:
    type: string          # Data type
    description: string   # Parameter description
    format: string        # Optional format specifier
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
  celsius:
    type: number
    description: Temperature in Celsius
    required: true
tasks:
  - id: convertTemperature
    type: script
    language: python
    code: |
      fahrenheit = celsius * 9/5 + 32
      return {"fahrenheit": fahrenheit}
outputs:
  fahrenheit:
    type: number
    description: Temperature in Fahrenheit
```

### Tasks

Tasks represent the executable units within a capability. Each task must have:

```yaml
tasks:
  - id: uniqueId           # Task identifier
    type: string          # Task type (script, request, etc.)
    language: string      # For script tasks
    code: string         # Implementation
```

### Task Types (More Soon)

- `script`: Execute code in specified language

### Parameter Management

**Input Parameters:**
```yaml
inputs:
  paramName:
    type: string         # Data type
    description: string  # Parameter description
    required: boolean    # Whether parameter is required
    format: string       # Optional format specifier
    default: any         # Optional default value
```

**Output Parameters:**
```yaml
outputs:
  paramName:
    type: string         # Data type (string, number, boolean, object, array)
    description: string  # Parameter description
    format: string       # Optional format specifier (e.g., float, date-time)
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
    email: jane@example.com

inputs:
  data:
    type: array
    description: Array of numerical values to analyze
    required: true
    items:
      type: number
  options:
    type: object
    description: Configuration options for analysis
    required: false
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
outputs:
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
```

### Environment Variables

Environment variables define the configuration and secrets required for capability execution. These are resolved at runtime by the Enact execution environment. All environment variables are treated as secrets by default to enhance security.

```yaml
env:
  vars:
    - name: ENACT_AUTH_IDENTITY_KEY
      description: "API key for identity verification service"
      required: true
    - name: ENACT_EMAIL_SERVICE_KEY
      description: "API key for email service"
      required: true
    - name: ENACT_SLACK_WEBHOOK_URL
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

### Error Handling

It is recommended to handle errors using the standard `outputs` structure. A common pattern is to include an `error` output that is present only when an error occurs:

```yaml
outputs:
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

## Future Features: Composite Capabilities

Composite capabilities allow for more complex workflows by combining multiple atomic capabilities into a coordinated sequence.

### Composite Capability Structure

```yaml
enact: 1.0.0
id: CompositeExample
description: A workflow combining multiple capabilities
version: 1.0.0
type: composite
authors:
  - name: Jane Doe
inputs:
  someInput:
    type: string
    description: Input for the composite workflow
    required: true
imports:
  - id: AtomicCapability1
    version: "1.0.0"
  - id: AtomicCapability2
    version: "2.1.0"
flow:
  steps:
    - capability: AtomicCapability1
      inputs:
        paramA: "{{inputs.someInput}}"
    - capability: AtomicCapability2
      inputs:
        paramB: "{{outputs.AtomicCapability1.result}}"
outputs:
  finalResult:
    type: object
    description: The final result of the workflow
```

## Best Practices

1. **Atomic Capability Design**
   - Keep capabilities focused on single responsibility
   - Make inputs and outputs explicit
   - Include proper error handling
   - Remember that tasks execute in the order they are defined

2. **Composite Capability Design**
   - Define clear imports with specific versions
   - Handle capability failures gracefully
   - Document the workflow clearly
   - Use flow for complex orchestration

3. **Environment Variable Management**
   - Clearly document all required environment variables
   - Remember that all environment variables are treated as secrets by default
   - Provide defaults only when absolutely necessary and safe to do so
   - Consider offering multiple resolution strategies for variables (e.g., from registry, local env, etc.)
   - Validate all required variables before starting execution

5. **Documentation**
   - Provide clear descriptions for capabilities, inputs, and outputs
   - Include examples where appropriate
   - Document any special requirements or considerations

## License

This project is licensed under the [MIT License](LICENSE).
