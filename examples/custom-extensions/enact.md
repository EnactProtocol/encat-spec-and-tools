---
enact: "2.0.0"
name: "acme-corp/monitoring/health-check"
description: "Health check tool with custom company metadata"
from: "alpine:3.18"
command: "curl -s --max-time 5 '${url}/health' | jq '.status'"
version: "1.0.0"
timeout: "10s"
license: "MIT"
tags: ["monitoring", "health", "ops"]

inputSchema:
  type: object
  properties:
    url:
      type: string
      format: uri
      description: "Service URL to check"
  required: ["url"]

outputSchema:
  type: object
  properties:
    status:
      type: string
      description: "Health check status"

annotations:
  title: "ACME Health Check"
  readOnlyHint: true
  openWorldHint: true
  idempotentHint: true

# Custom company-specific extensions (x- prefix)
x-internal-id: "tool-hc-001"
x-cost-center: "platform-engineering"
x-deployment-tier: "production"

x-monitoring:
  oncall: "platform-team@acme-corp.com"
  runbook: "https://wiki.acme-corp.com/runbook-health-check"
  slack-channel: "#platform-alerts"
  dashboard: "https://grafana.acme-corp.com/d/health-checks"

x-security:
  approved-by: "security-team@acme-corp.com"
  scan-date: "2025-07-01"
  vulnerability-exceptions: []

x-compliance:
  soc2: true
  gdpr: false
  pci: false
  data-classification: "internal"

x-ownership:
  team: "platform"
  maintainer: "john.doe@acme-corp.com"
  backup-maintainer: "jane.smith@acme-corp.com"
  created: "2025-01-15"
  last-updated: "2025-11-17"

x-deployment:
  environments: ["dev", "staging", "prod"]
  rollout-strategy: "blue-green"
  feature-flags: ["health-check-v2"]
  canary-percentage: 10
---

# ACME Health Check Tool

This tool demonstrates how to use **custom extensions** (`x-*` fields) in the YAML frontmatter to add organization-specific metadata.

## Overview

A simple health check tool that queries a service's `/health` endpoint and returns its status. This example shows how enterprises can extend the Enact protocol with custom metadata.

## Custom Extensions

All fields beginning with `x-` are custom extensions that don't affect tool execution but provide valuable organizational context:

### Internal Tracking
- `x-internal-id` - Internal tool identifier
- `x-cost-center` - Budget allocation
- `x-deployment-tier` - Environment classification

### Monitoring
- `x-monitoring` - Oncall, runbooks, dashboards, alerts

### Security & Compliance
- `x-security` - Security approvals, scan dates, exceptions
- `x-compliance` - Regulatory compliance flags (SOC2, GDPR, PCI)

### Ownership
- `x-ownership` - Team, maintainers, creation dates

### Deployment
- `x-deployment` - Environments, rollout strategy, feature flags

## Usage

```bash
enact run acme-corp/monitoring/health-check \
  --args '{"url": "https://api.acme-corp.com"}'
```

## Benefits of Custom Extensions

1. **Metadata preservation** - Keep organizational context with the tool
2. **No signature impact** - Custom fields aren't part of cryptographic signing
3. **Tool discovery** - Internal tooling can query these fields
4. **Compliance tracking** - Document security and regulatory requirements
5. **Operations integration** - Link to runbooks, dashboards, and oncall

## Notes

- All custom extensions use the `x-` prefix
- These fields are ignored by the core Enact runtime
- Useful for internal tooling, dashboards, and compliance tracking
- Can be used by MCP servers or custom integrations
