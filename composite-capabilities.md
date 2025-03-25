# Composite Capabilities

Composite capabilities allow for more complex workflows by combining multiple atomic capabilities into a coordinated sequence.

## Overview

While atomic capabilities focus on individual tasks, composite capabilities provide a way to orchestrate multiple capabilities into coherent workflows. This enables more complex functionality to be built from simpler building blocks.

## Composite Capability Structure

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

## Key Components

### Imports

The `imports` section defines which capabilities are used within the composite workflow:

```yaml
imports:
  - id: AtomicCapability1    # Capability identifier
    version: "1.0.0"         # Specific version to use
  - id: AtomicCapability2
    version: "2.1.0"
```

### Flow

The `flow` section orchestrates how capabilities are executed:

```yaml
flow:
  steps:
    - capability: AtomicCapability1    # The capability to execute
      inputs:                          # Input mappings
        paramA: "{{inputs.someInput}}" # Reference to composite's inputs
    - capability: AtomicCapability2
      inputs:
        paramB: "{{outputs.AtomicCapability1.result}}" # Reference to previous step's output
```

## Example: Data Processing Pipeline

Here's a more complete example of a composite capability that processes customer data:

```yaml
enact: 1.0.0
id: CustomerDataProcessor
description: Processes customer data through validation, enrichment, and analytics
version: 1.0.0
type: composite
authors:
  - name: Jane Smith
    email: jane@example.com
inputs:
  customerData:
    type: array
    description: Array of customer records to process
    required: true
    items:
      type: object
  options:
    type: object
    description: Processing options
    required: false
    default: {}
imports:
  - id: DataValidator
    version: "1.2.0"
  - id: DataEnricher
    version: "2.0.1"
  - id: DataAnalyzer
    version: "1.5.0"
flow:
  steps:
    - capability: DataValidator
      inputs:
        data: "{{inputs.customerData}}"
        schema: "customer"
      handler:
        onSuccess: next
        onError: fail
    - capability: DataEnricher
      inputs:
        data: "{{outputs.DataValidator.validatedData}}"
        enrichmentLevel: "{{inputs.options.enrichmentLevel || 'standard'}}"
      handler:
        onSuccess: next
        onError: next
    - capability: DataAnalyzer
      inputs:
        data: "{{outputs.DataEnricher.enrichedData || outputs.DataValidator.validatedData}}"
        analysisType: "{{inputs.options.analysisType || 'basic'}}"
outputs:
  processedData:
    type: object
    description: The fully processed customer data
    source: "{{outputs.DataEnricher.enrichedData || outputs.DataValidator.validatedData}}"
  analytics:
    type: object
    description: Analytical insights from the data
    source: "{{outputs.DataAnalyzer.results}}"
  errors:
    type: array
    description: Any errors encountered during processing
    source: "{{[].concat(
              outputs.DataValidator.errors || [],
              outputs.DataEnricher.errors || [],
              outputs.DataAnalyzer.errors || []
            )}}"
```

## Advanced Flow Control

Composite capabilities can include conditional logic and more advanced flow control:

```yaml
flow:
  steps:
    - capability: DataValidator
      inputs:
        data: "{{inputs.data}}"
      handler:
        onSuccess:
          condition: "{{outputs.DataValidator.validCount > 10}}"
          true: nextStep
          false: skipToAnalysis
    - id: nextStep
      capability: DataEnricher
      inputs:
        data: "{{outputs.DataValidator.validatedData}}"
    - id: skipToAnalysis
      capability: DataAnalyzer
      inputs:
        data: "{{outputs.DataValidator.validatedData}}"
```

## Best Practices for Composite Capabilities

1. **Version Management**
   - Always specify exact versions for imported capabilities
   - Consider compatibility between different capability versions
   - Test composite workflows thoroughly after updating imported capabilities

2. **Error Handling**
   - Define clear error handling strategies at each step
   - Aggregate errors from all steps in the output
   - Consider fallback options for non-critical failures

3. **Input and Output Mapping**
   - Use clear, consistent naming conventions
   - Handle optional outputs properly with fallbacks
   - Consider data transformations between steps

4. **Flow Design**
   - Keep flows as linear as possible for maintainability
   - Use conditional branching only when necessary
   - Document the intended flow clearly

5. **Testing**
   - Test each step independently