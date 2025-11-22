---
enact: "2.0.0"
name: enact/examples/complete-tool
description: "A complete example tool demonstrating all Enact features"
from: "python:3.11-slim"
command: "pip install requests==2.31.0 && python -c \"import requests; print(requests.get('${url}').text[:100])\""
version: "1.0.0"
timeout: "30s"
license: "MIT"
tags: ["example", "http", "python", "demo"]

inputSchema:
  type: object
  properties:
    url:
      type: string
      format: uri
      description: "URL to fetch content from"
  required: ["url"]

outputSchema:
  type: object
  properties:
    content:
      type: string
      description: "First 100 characters of the fetched content"

annotations:
  title: "Complete Example Tool"
  readOnlyHint: true
  openWorldHint: true
  idempotentHint: true
  destructiveHint: false

env:
  HTTP_TIMEOUT:
    description: "HTTP request timeout in seconds"
    source: "Configuration or defaults"
    required: false
    default: "30"

authors:
  - name: "Enact Team"
    email: "team@enactprotocol.com"
    url: "https://enactprotocol.com"

examples:
  - input:
      url: "https://httpbin.org/get"
    output:
      content: "{\n  \"args\": {},\n  \"headers\": {\n    \"Accept\": \"*/*\",\n    \"Accept-Encoding\": \"gzip, deflate\""
    description: "Fetch JSON from httpbin.org"

resources:
  memory: "256Mi"
  disk: "1Gi"
---

# Complete Example Tool

This tool demonstrates all available Enact features in the **enact.md** format.

## Features Demonstrated

- **Container image specification** with `from: "python:3.11-slim"`
- **Input/output schemas** for validation
- **Environment variables** with defaults
- **Resource requirements** (memory, disk)
- **Comprehensive metadata** (tags, license, authors)
- **Behavior annotations** for AI models
- **Test examples** for validation

## How It Works

This tool fetches content from a URL and returns the first 100 characters. It uses:

1. Python 3.11 in a slim container
2. The `requests` library for HTTP
3. Input validation via JSON Schema
4. Configurable timeout via environment variable

## Usage

```bash
enact run enact/examples/complete-tool --args '{"url": "https://httpbin.org/get"}'
```

## Environment Variables

- `HTTP_TIMEOUT` - Optional timeout in seconds (default: 30)

## Notes

This is a reference implementation showing best practices for Enact tool definitions using the unified **enact.md** format with YAML frontmatter and Markdown documentation.
