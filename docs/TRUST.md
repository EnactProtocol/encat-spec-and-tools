# Enact Trust System

**A multi-party attestation model for verifying AI tools with cryptographic signatures and audits.**

---

## Overview

Enact uses **Sigstore** for cryptographic signing combined with a **flexible trust model** that lets you decide which publishers and auditors you trust. Every tool has a publisher signature, and auditors can add independent attestations to verify security, quality, or compliance.

**Key Concepts:**
- **Publishers** sign tools when they create them (identity from GitHub)
- **Auditors** review tools and add attestations (also signed with Sigstore)
- **Users** configure which publishers/auditors they trust
- **Registry** stores signatures and attestations (but doesn't decide trust)

---

## How It Works

### 1. Publishers Sign Tools

When a publisher creates a tool, they sign it with Sigstore:

```bash
cd my-tool/
enact sign .
enact publish .
```

This creates a **publisher signature** that proves:
- ✅ Who created the tool (GitHub identity)
- ✅ The tool hasn't been tampered with
- ✅ When it was signed (Rekor timestamp)

**Publisher identity example:**
```
repo:acme-corp/tools:ref:refs/heads/main
```

### 2. Auditors Add Attestations

Independent auditors can review published tools and add attestations:

```bash
# Download and review the tool
enact download acme-corp/data/processor@v2.1.0
cd acme-corp-data-processor/

# Manual code review, security scan, compliance check, etc.

# Create attestation
enact attest create \
  --subject "acme-corp/data/processor@v2.1.0" \
  --type "https://enactprotocol.com/audit/v1" \
  --findings "no-critical-issues" \
  --report-url "https://audits.enactprotocol.com/report/123"

# Publish attestation (signed with auditor's GitHub identity)
enact attest publish acme-corp/data/processor attestation.bundle
```

**Attestation types:**
- `https://enactprotocol.com/audit/v1` - Security/code review
- `https://enactprotocol.com/compliance/v1` - Regulatory compliance
- `https://enactprotocol.com/performance/v1` - Performance testing
- Custom types for your organization

### 3. Users Configure Trust

Users create a trust configuration that says which publishers and auditors they trust:

```json
// ~/.enact/trusted.json (global) or .enact/trusted.json (project)
{
  "version": "1.0.0",
  "publishers": {
    "direct": [
      "repo:EnactProtocol/*",
      "repo:my-company/tools:*"
    ]
  },
  "auditors": {
    "accepted": [
      "repo:EnactProtocol/audits",
      "repo:company2/security",
      "repo:ossf/audits"
    ],
    "required": {
      "financial/*": ["repo:company2/security"],
      "healthcare/*": ["repo:hipaa-auditor/compliance"]
    }
  },
  "policies": {
    "default": "prompt",
    "max_attestation_age_days": 180,
    "min_auditors": 1
  }
}
```

### 4. Installation Checks Trust

When installing a tool, Enact automatically checks if it meets your trust requirements:

```bash
enact install acme-corp/data/processor
```

**Trust verification flow:**
1. Is the publisher directly trusted? → Install
2. Has a trusted auditor attested? → Install
3. Are namespace-specific requirements met? → Install
4. Otherwise → Apply default policy (prompt, allow, or deny)

---

## Trust Configuration

### Publishers

**Direct trust** means you trust a publisher to create tools without needing audits.

```json
{
  "publishers": {
    "direct": [
      "repo:EnactProtocol/*",           // Trust all EnactProtocol repos
      "repo:my-company/tools:*",         // Trust specific repo
      "repo:acme-corp/*:ref:refs/heads/main"  // Only main branch
    ]
  }
}
```

**When to trust publishers directly:**
- Official Enact tools
- Your own organization's tools
- Well-known, reputable publishers

### Auditors

**Accepted auditors** are third parties you trust to verify tools.

```json
{
  "auditors": {
    "accepted": [
      "repo:EnactProtocol/audits",      // Official Enact audits
      "repo:ossf/audits",                // Open Source Security Foundation
      "repo:my-company/security"         // Your company's security team
    ]
  }
}
```

**When to trust auditors:**
- Established security organizations (OSSF, CNCF, etc.)
- Your company's internal security/compliance teams
- Reputable third-party audit firms

### Required Audits (Namespace-Specific)

For sensitive namespaces, you can **require** specific audits:

```json
{
  "auditors": {
    "required": {
      "financial/*": [
        "repo:my-company/security"
      ],
      "healthcare/*": [
        "repo:hipaa-auditor/compliance",
        "repo:my-company/security"
      ],
      "acme-corp/critical/*": [
        "repo:EnactProtocol/audits",
        "repo:company2/security"
      ]
    }
  }
}
```

**Required audits are strict:**
- Tool MUST have attestations from ALL specified auditors
- Installation blocked if requirements not met
- Use for high-risk tools (financial, healthcare, infrastructure)

### Policies

```json
{
  "policies": {
    // What to do for tools that don't meet trust criteria
    "default": "prompt",  // "allow" | "prompt" | "deny"
    
    // Reject attestations older than this
    "max_attestation_age_days": 180,
    
    // Minimum number of trusted auditor attestations
    "min_auditors": 1
  }
}
```

---

## User Experience

### Scenario 1: Trusted Publisher

```bash
$ enact install EnactProtocol/utils/validator

✓ Installing EnactProtocol/utils/validator@v1.2.0
  Publisher: repo:EnactProtocol/core (trusted)
  Downloaded and verified in 2.3s
```

No prompt, installs immediately because publisher is trusted.

---

### Scenario 2: Audited by Trusted Auditor

```bash
$ enact install acme-corp/data/processor

✓ Installing acme-corp/data/processor@v2.1.0
  Publisher: repo:acme-corp/tools (verified)
  Audited by: repo:EnactProtocol/audits ✓ (trusted auditor)
  Audit report: https://audits.enactprotocol.com/report/123
  Findings: no-critical-issues
  Downloaded and verified in 2.8s
```

Publisher isn't directly trusted, but a trusted auditor has verified it.

---

### Scenario 3: Unknown Tool (Prompt)

```bash
$ enact install random-org/sketchy/tool

⚠ Trust verification needed

Tool: random-org/sketchy/tool@v1.0.0
Publisher: repo:random-org/tools (not trusted)
Audits: None

This tool has not been audited by any of your trusted auditors:
  - EnactProtocol/audits
  - company2/security
  - ossf/audits

Options:
  [v] View tool details and manifest
  [a] Install anyway (not recommended)
  [t] Trust this publisher for future installs
  [c] Cancel

Choice: █
```

User is prompted to make a decision because tool doesn't meet trust criteria.

---

### Scenario 4: Missing Required Audit

```bash
$ enact install acme-corp/financial/analyzer

✗ Installation blocked by trust policy

Tool: acme-corp/financial/analyzer@v1.0.0
Publisher: repo:acme-corp/tools (verified)

Required audits for financial/* namespace:
  ✗ repo:company2/security (MISSING)

Found audits:
  ✓ repo:EnactProtocol/audits

This tool requires a security audit from company2/security 
but none was found. Contact the publisher or wait for the 
required audit to be published.
```

Installation is blocked because namespace-specific requirements aren't met.

---

### Scenario 5: Multiple Audits

```bash
$ enact get acme-corp/data/processor

Name: acme-corp/data/processor
Version: v2.1.0
Description: Process and validate CSV files

Publisher: repo:acme-corp/tools
  Signed: 2025-11-14T10:30:00Z
  Certificate: Valid ✓
  Rekor entry: 69281180

Attestations:
  ✓ Security Audit by EnactProtocol/audits
    Type: https://enactprotocol.com/audit/v1
    Date: 2025-11-14T15:00:00Z
    Report: https://audits.enactprotocol.com/report/123
    Findings: no-critical-issues
    Rekor entry: 69281245

  ✓ Compliance Audit by company2/security
    Type: https://enactprotocol.com/compliance/v1
    Date: 2025-11-14T16:30:00Z
    Report: https://company2.com/audits/456
    Findings: compliant
    Rekor entry: 69281302

Trust Status: ✓ Trusted (audited by EnactProtocol/audits)
```

Users can see all signatures and attestations with full transparency.

---

## Managing Trust

### CLI Commands

```bash
# Add a trusted publisher
enact trust add publisher "repo:my-company/*"

# Add a trusted auditor
enact trust add auditor "repo:ossf/audits"

# Require specific auditor for namespace
enact trust require "financial/*" "repo:company2/security"

# Remove trust
enact trust remove auditor "repo:old-auditor/*"

# List all trusted entities
enact trust list

# View trust status for a specific tool
enact trust check acme-corp/data/processor
```

### Example: List Trusted Entities

```bash
$ enact trust list

Trusted Publishers:
  - repo:EnactProtocol/*
  - repo:my-company/tools:*

Trusted Auditors:
  - repo:EnactProtocol/audits
  - repo:company2/security
  - repo:ossf/audits

Required Audits by Namespace:
  - financial/* → repo:company2/security
  - healthcare/* → repo:hipaa-auditor/compliance

Default Policy: prompt
Max Attestation Age: 180 days
Minimum Auditors: 1
```

---

## Project vs Global Trust

Trust configurations can exist at two levels:

### Global Trust (`~/.enact/trusted.json`)

Applies to all projects on your machine.

```bash
# Add to global config
enact trust add auditor "repo:ossf/audits" --global
```

**Use for:**
- Personal preferences
- Organization-wide auditors
- General security policies

### Project Trust (`.enact/trusted.json`)

Committed to git and shared with your team.

```bash
# Add to project config
cd my-project/
enact trust add auditor "repo:my-company/security"
git add .enact/trusted.json
git commit -m "Require company security audits"
```

**Use for:**
- Team requirements
- Project-specific policies
- Compliance requirements

### Merge Behavior

Project trust is **merged** with global trust:

```typescript
// Effective trust config = global + project
{
  publishers: {
    direct: [...global.publishers, ...project.publishers]
  },
  auditors: {
    accepted: [...global.auditors, ...project.auditors],
    required: { ...global.required, ...project.required }
  },
  policies: {
    ...global.policies,
    ...project.policies  // Project overrides global
  }
}
```

---

## Team Workflows

### Enterprise Team Example

**Team lead sets up project trust:**

```bash
cd my-company-project/
enact trust add auditor "repo:my-company/security"
enact trust require "*" "repo:my-company/security"
git add .enact/trusted.json
git commit -m "Require company security audits for all tools"
git push
```

**Team members inherit trust config:**

```bash
git clone https://github.com/my-company/project
cd project/
enact install  # Installs all tools from .enact/tools.json

# Output:
# ✓ acme-corp/data/processor@v2.1.0 
#   (audited by my-company/security ✓)
# ✓ other-org/utils/helper@v1.0.0
#   (audited by my-company/security ✓)
```

All team members automatically get the same trust requirements.

---

## Becoming an Auditor

Anyone with a GitHub account can become an auditor.

### 1. Create Audit Repository

```bash
mkdir my-org-audits
cd my-org-audits/
git init
```

### 2. Review Tools

```bash
# Download tool to audit
enact download acme-corp/data/processor@v2.1.0

# Manual review process:
# - Code review
# - Security scanning
# - Compliance checks
# - Performance testing
```

### 3. Create Attestation

```bash
enact attest create \
  --subject "acme-corp/data/processor@v2.1.0" \
  --type "https://my-org.com/audit/v1" \
  --findings "no-critical-issues" \
  --report-url "https://audits.my-org.com/report/123" \
  --metadata '{"score": 9.2, "vulnerabilities": 0}'
```

### 4. Publish Attestation

```bash
enact attest publish acme-corp/data/processor attestation.bundle
```

### 5. Share Your Auditor Identity

Tell users to trust your auditor identity:

```bash
enact trust add auditor "repo:my-org/audits"
```

### Best Practices for Auditors

**Be transparent:**
- Publish audit reports publicly
- Document your audit criteria
- Explain your methodology

**Be consistent:**
- Use consistent attestation types
- Apply uniform standards
- Update attestations regularly

**Be accountable:**
- Sign with a dedicated audit repo
- Track your audit history
- Respond to questions about audits

---

## First-Time Setup

When you first run `enact install`, you'll be prompted to configure trust:

```bash
$ enact install first-tool/ever

⚠ No trust configuration found

Enact uses cryptographic signatures to verify tools, but you 
haven't configured which publishers or auditors you trust yet.

Suggested trusted auditors:
  [x] EnactProtocol (official Enact audits)
  [x] OSSF (Open Source Security Foundation)
  [ ] npm (for npm-ecosystem tools)

Would you like to:
  [s] Use suggested defaults
  [c] Configure manually
  [n] Skip (prompt for each tool)

Choice: █
```

**Suggested defaults:**

```json
{
  "auditors": {
    "accepted": [
      "repo:EnactProtocol/audits",
      "repo:ossf/audits"
    ]
  },
  "policies": {
    "default": "prompt"
  }
}
```

---

## Security Model

### What This Trust System Provides

**Authenticity:**
- Tools are signed by verified publishers (GitHub identity)
- Attestations are signed by verified auditors (GitHub identity)
- Identities cannot be forged (Sigstore/Fulcio)

**Integrity:**
- Any tampering invalidates signatures
- Hash verification ensures content hasn't changed
- Rekor provides tamper-evident log

**Transparency:**
- All signatures logged in public Rekor
- Anyone can audit what was signed and when
- Impossible to backdate signatures

**Flexibility:**
- Users decide who to trust
- Multiple auditors can attest independently
- Namespace-specific requirements for sensitive tools

### What This Trust System Does NOT Provide

**Code Quality:**
- Signatures prove identity, not quality
- Audits are subjective (depends on auditor rigor)
- "Audited" doesn't mean "bug-free"

**Continuous Monitoring:**
- Attestations are point-in-time
- Tools can be updated after audit
- Re-audit required for new versions

**Guaranteed Safety:**
- Trust decisions are yours to make
- Attackers could compromise GitHub accounts
- Always review critical tools yourself

---

## FAQ

### Q: Who can sign tools?

Anyone with a GitHub account. Sigstore uses GitHub OAuth for authentication.

### Q: Who can audit tools?

Anyone with a GitHub account. Auditors are just publishers who review and attest to other people's tools.

### Q: Can I trust tools without audits?

Yes! You can:
- Trust specific publishers directly
- Set `"default": "allow"` in policies
- Manually approve tools when prompted

### Q: What if an auditor becomes untrustworthy?

Remove them from your trust config:

```bash
enact trust remove auditor "repo:sketchy-auditor/*"
```

Existing installed tools remain, but new installs won't trust that auditor.

### Q: Can I require multiple audits?

Yes! Use namespace-specific required audits:

```json
{
  "auditors": {
    "required": {
      "critical/*": [
        "repo:auditor1/*",
        "repo:auditor2/*"
      ]
    }
  }
}
```

### Q: What's the difference between "accepted" and "required" auditors?

- **Accepted**: ANY of these auditors is sufficient
- **Required**: ALL of these auditors are necessary (for specific namespaces)

### Q: Can I run my own auditor?

Yes! Create a GitHub repo, audit tools, and publish attestations. Others can choose to trust your auditor identity.

### Q: How do I know if an audit is recent?

Set `max_attestation_age_days` in your policies:

```json
{
  "policies": {
    "max_attestation_age_days": 180
  }
}
```

### Q: Can publishers fake audits?

No. Each attestation is signed by the auditor's GitHub identity (via Sigstore). Publishers cannot forge auditor signatures.

### Q: What if Rekor goes down?

Sigstore bundles include all verification data (certificate, signature, inclusion proof). Verification works offline using the bundle alone.

---

## Examples

### Example 1: Personal Developer

```json
// ~/.enact/trusted.json
{
  "publishers": {
    "direct": [
      "repo:EnactProtocol/*"
    ]
  },
  "auditors": {
    "accepted": [
      "repo:EnactProtocol/audits",
      "repo:ossf/audits"
    ]
  },
  "policies": {
    "default": "prompt"
  }
}
```

**Behavior:**
- Trusts official Enact tools
- Trusts tools audited by EnactProtocol or OSSF
- Prompts for everything else

---

### Example 2: Enterprise Security Team

```json
// .enact/trusted.json (committed to company repos)
{
  "publishers": {
    "direct": [
      "repo:my-company/*"
    ]
  },
  "auditors": {
    "accepted": [
      "repo:my-company/security"
    ],
    "required": {
      "*": ["repo:my-company/security"]
    }
  },
  "policies": {
    "default": "deny",
    "max_attestation_age_days": 90
  }
}
```

**Behavior:**
- Only trusts internal tools or audited-by-company tools
- REQUIRES company security audit for ALL tools
- Denies everything else by default
- Attestations must be <90 days old

---

### Example 3: Open Source Project

```json
// .enact/trusted.json
{
  "auditors": {
    "accepted": [
      "repo:EnactProtocol/audits",
      "repo:ossf/audits",
      "repo:cncf/audits"
    ]
  },
  "policies": {
    "default": "prompt",
    "min_auditors": 1
  }
}
```

**Behavior:**
- Trusts tools audited by major foundations
- Requires at least 1 audit
- Prompts for tools without audits

---

## Related Documentation

- [Sigstore Implementation Guide](SIGSTORE.md) - How signatures work
- [Complete Protocol Specification](SPEC.md) - Full technical details
- [CLI Commands Reference](COMMANDS.md) - All available commands

---

## License

MIT License © 2025 Enact Protocol Contributors