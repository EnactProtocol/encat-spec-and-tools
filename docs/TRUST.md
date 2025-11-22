# TRUST.md

## Enact Trust System

**A multi-party attestation model for verifying AI tools with cryptographic signatures.**

Enact uses two types of identities for comprehensive security:

1. **Publishers** (Enact usernames) - Who created/published the tool
2. **Auditors** (OIDC identities) - Who reviewed and attested the tool

Users configure trust for both, giving them full control over what runs on their system.

---

## Overview

### Two Identity Types

**Publishers** - Enact accounts
- Created on enact.io
- Username becomes namespace (e.g., `alice` → `alice/*`)
- Used for publishing tools to registry

**Auditors** - OIDC identities (GitHub, Google, Microsoft, etc.)
- Used for cryptographically signing attestations
- Verified via Sigstore (Fulcio + Rekor)
- Can be anyone - tool publishers, third-party reviewers, security firms

**Key insight:** Publishers upload tools. Auditors sign attestations about those tools. Users decide which publishers and auditors they trust.

---

## How It Works

### 1. Publishers Create and Upload Tools

```bash
# Sign up on https://enact.io
# Username: alice

# Login and publish
enact auth login
enact publish .
# ✓ Published alice/utils/greeter@v1.0
```

**Namespace rule:** Your Enact username = your namespace.

### 2. Auditors Review and Sign Tools

Anyone can audit any tool by signing an attestation:

```bash
# Review the tool (future: enact inspect for containerized review)
# For now, review via registry source code view or install locally

# Sign if it passes review
enact sign alice/utils/greeter@v1.0

? Sign attestation with:
  > GitHub
    Google
    Microsoft

# Opens browser for OIDC authentication
# Creates Sigstore signature
# ✓ Attestation published
  Signed by: github.com/EnactProtocol
  Logged to Rekor: #123456
```

**Or report issues:**
```bash
# Report if tool has security issues
enact report alice/utils/greeter@v1.0 --reason "SQL injection vulnerability in query handler"

# ✓ Failed attestation published
  Signed by: github.com/security-firm
```

**What gets signed:**
- Tool bundle hash (cryptographic proof of exact version)
- Status: passed or failed
- Optional: reason, report URL, findings
- Your OIDC identity
- Timestamp (via Rekor)

### 3. Users Configure Trust

Control which publishers and auditors you trust:

```bash
# Trust publishers (no colon = Enact username)
enact trust alice
enact trust EnactProtocol
enact trust acme-corp

# Trust auditors (has colon = OIDC identity)
enact trust github:EnactProtocol
enact trust google:security@company.com
enact trust github:ossf

# Remove trust (automatically inferred from format)
enact trust -r alice                    # Removes publisher
enact trust -r github:untrusted-org     # Removes auditor

# List all trusted identities
enact trust list
```

**Or edit config directly:**
```yaml
# ~/.enact/config.yaml
trust:
  publishers:
    - EnactProtocol
    - alice
    - acme-corp
  
  auditors:
    - github:EnactProtocol
    - github:ossf
    - google:security@company.com
  
  policy: require_audit
```

### 4. Installing with Trust Verification

```bash
enact install alice/utils/greeter

Tool: alice/utils/greeter@v1.0
  Published by: @alice (Enact)
  
Attestations:
  ✓ github.com/EnactProtocol - passed
    Audit date: 2025-01-15
  
  ✓ github.com/ossf - passed
    Audit date: 2025-01-16

Trust Status:
  Publisher: @alice (not in trusted publishers)
  Auditors: ✓ 2 trusted attestations found
  
Decision: ✓ INSTALL (trusted auditor attestations)

Install? [Y/n]:
```

---

## Trust Decision Flow

When you install a tool, Enact checks:

1. **Is publisher trusted?** → ✅ Install immediately
2. **Any trusted auditor signed it?** → ✅ Install
3. **Neither trusted?** → Apply policy (prompt, block, or allow)

**Example scenarios:**

```yaml
# Scenario 1: Trust the publisher
trust:
  publishers:
    - alice

# alice/tool → Installs immediately (no audit needed)
# bob/tool → Checks auditors
```

```yaml
# Scenario 2: Only trust auditors
trust:
  auditors:
    - github:EnactProtocol

# alice/tool (audited by EnactProtocol) → Installs
# alice/tool (not audited) → Blocked/prompted
# bob/tool (audited by EnactProtocol) → Installs
```

```yaml
# Scenario 3: Trust both
trust:
  publishers:
    - alice
  auditors:
    - github:EnactProtocol

# alice/tool → Installs (trusted publisher)
# bob/tool (audited) → Installs (trusted auditor)
# bob/tool (not audited) → Blocked/prompted
```

---

## Trust Policies

```yaml
trust:
  policy: require_audit  # Options: require_audit, prompt, allow
  minimum_attestations: 1  # How many trusted auditors required
```

**Policies:**
- **require_audit** - Block if no trusted publisher/auditor (recommended)
- **prompt** - Ask user to confirm
- **allow** - Install anyway (development mode)

**Minimum attestations:**
```yaml
trust:
  auditors:
    - github:EnactProtocol
    - github:ossf
  minimum_attestations: 2  # Require both auditors to sign
```

---

## Self-Attestation

Publishers can audit their own tools:

```bash
# Publish
enact publish .
# ✓ Published alice/my-tool@v1.0

# Self-attest
enact sign alice/my-tool@v1.0
# Signs with: github.com/alice
```

**User perspective:**
```
Attestations:
  ✓ github.com/alice - passed (self-attested)

Your trust:
  Publisher: @alice (not trusted)
  Auditors: github:alice (not trusted)

⚠ No trusted attestations found
Install anyway? [y/N]:
```

**To trust self-attestations:**
```bash
# Option 1: Trust the publisher
enact trust alice

# Option 2: Trust their OIDC identity as auditor
enact trust github:alice
```

---

## CLI Commands

### Trust Management
```bash
# Trust publishers (no colon = Enact username)
enact trust alice
enact trust EnactProtocol
enact trust acme-corp

# Trust auditors (has colon = OIDC identity)
enact trust github:EnactProtocol
enact trust google:security@company.com
enact trust github:my-company/*

# Remove trust (format automatically inferred)
enact trust -r alice                    # Removes publisher
enact trust -r github:sketchy-org       # Removes auditor

# List all trusted identities
enact trust list

# Check trust status for a tool
enact trust check alice/my-tool@v1.0
```

### Auditing
```bash
# Review tool (future: enact inspect)
# For now, review via registry or install locally

# Sign if it passes audit
enact sign tool@version

# Report if it fails audit
enact report tool@version --reason "Security issue found"

# Check trust status and view attestations
enact trust check tool@version
```

---

## Identity Format

### Publishers (Enact Usernames)
```bash
enact trust alice
enact trust acme-corp
enact trust EnactProtocol
```

Simple username from enact.io account. **No colon in the identifier.**

### Auditors (OIDC Identities)

**Shorthand (has colon):**
```bash
enact trust github:EnactProtocol
enact trust google:alice@example.com
enact trust microsoft:security@company.com
```

**Wildcards:**
```bash
enact trust github:my-org/*        # Trust entire GitHub org
enact trust google:*@company.com   # Trust all company emails
```

**Advanced (explicit in config file):**
```yaml
trust:
  auditors:
    - issuer: https://token.actions.githubusercontent.com
      subject: https://github.com/EnactProtocol/*
```

**The colon (`:`) is the key:** It tells Enact whether you're trusting a publisher or an auditor.

---

## Default Configuration

```yaml
# ~/.enact/config.yaml (created on first run)
trust:
  publishers:
    - EnactProtocol  # Trust official Enact tools
  
  auditors:
    - github:EnactProtocol  # Trust official auditor
  
  policy: prompt
  minimum_attestations: 1
```

---

## Example Workflows

### Personal Developer
```yaml
trust:
  publishers:
    - alice  # Trust your own tools
  auditors:
    - github:EnactProtocol
    - github:alice  # Trust your own audits
  policy: prompt
```

```bash
# Your workflow
enact publish .           # Publish to alice/*
enact sign alice/tool@v1  # Self-attest
enact install alice/tool  # Installs (trusted publisher)
```

### Enterprise Security Team
```yaml
trust:
  publishers: []  # Don't auto-trust any publisher
  
  auditors:
    - microsoft:security@company.com
    - github:company-security/*
  
  policy: require_audit
  minimum_attestations: 1
```

Only tools audited by internal security team can be installed.

### Open Source Project
```yaml
trust:
  publishers:
    - my-project  # Trust official project account
  
  auditors:
    - github:EnactProtocol
    - github:ossf
    - github:my-project/*
  
  policy: require_audit
```

### Development Mode
```yaml
trust:
  publishers:
    - alice
  
  policy: allow  # Install anything (for testing)
```

---

## Becoming an Auditor

1. **Choose your OIDC identity** (GitHub, Google, etc.)
2. **Review tools thoroughly**
   - Review source code (via registry or local install)
   - Analyze code, run security scans
   - Test functionality
3. **Publish attestations**
   - `enact sign tool@ver` if it passes
   - `enact report tool@ver` if it fails
4. **Build reputation**
   - Be transparent about methodology
   - Provide detailed reports
   - Be consistent
5. **Tell users to trust you**
   - Document your process
   - Share your OIDC identity: `provider:identity`
   - Users add with `enact trust github:your-org`

---

## Security Guarantees

### What Enact Provides

✅ **Publisher identity** - Verified Enact accounts  
✅ **Attestation authenticity** - Cryptographic proof via Sigstore  
✅ **Integrity** - Tools haven't been tampered with  
✅ **Transparency** - All attestations in public Rekor log  
✅ **User control** - You choose who to trust  

### What Enact Does NOT Provide

❌ **Code quality** - Attestations don't guarantee bug-free code  
❌ **Auditor competence** - You must vet auditors  
❌ **Continuous monitoring** - Point-in-time attestations only  
❌ **Legal warranties** - Technical verification, not legal liability  

---

## FAQ

### Q: What's the difference between publishers and auditors?

**A:** Publishers are Enact accounts that upload tools. Auditors are OIDC identities that cryptographically sign attestations about tools. The format tells them apart: `alice` is a publisher, `github:alice` is an auditor.

### Q: Why separate them?

**A:** Flexibility. You might trust a publisher to create good tools, or you might only trust third-party auditors. Or both! You can also have multiple team members attest using different OIDC identities while publishing from one Enact account.

### Q: Can publishers and auditors be the same person?

**A:** Yes! If you trust Enact user "alice" as a publisher AND trust "github:alice" as an auditor, you're trusting the same person in both roles. But they're technically separate systems.

### Q: Do I need to configure both publishers and auditors?

**A:** No. You can:
- Only trust publishers (install their tools without audits)
- Only trust auditors (any tool is OK if audited)
- Trust both (maximum flexibility)
- Trust neither (prompt for everything)

### Q: What if I trust a publisher but they publish a bad tool?

**A:** Remove them from your trusted publishers list: `enact trust -r alice`. You can also check if trusted auditors have reported issues with specific tools.

### Q: Can attestations be faked?

**A:** No. Sigstore provides cryptographic proof. Attestations are signed with OIDC identities and logged in Rekor's transparency log. Tampering is cryptographically detectable.

### Q: What happens if an auditor reports a tool as failed?

**A:** Failed attestations are still attestations. If a trusted auditor reports a tool, installation will be blocked/prompted even if other auditors passed it. Failed attestations create an audit trail.

### Q: How do I see why a tool was reported?

**A:** Use `enact trust check tool@version` to show the trust status, attestations, and any reported issues.

### Q: What OIDC providers are supported?

**A:** Any provider that Sigstore accepts: GitHub, Google, Microsoft, GitLab, and custom OIDC servers. The CLI will guide you through authentication.

### Q: How does the colon (`:`) work in trust identifiers?

**A:** The colon separates the OIDC provider from the identity. `github:alice` means "GitHub user alice". No colon means it's an Enact username (publisher). This lets the CLI automatically infer whether you're trusting a publisher or auditor.

---

## Technical Details

### Attestation Structure

Attestations follow the in-toto statement format:

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [{
    "name": "pkg:enact/alice/utils/greeter@v1.0",
    "digest": {
      "sha256": "abc123..."
    }
  }],
  "predicateType": "https://enactprotocol.com/audit/v1",
  "predicate": {
    "status": "passed",
    "audit_date": "2025-01-15T10:30:00Z",
    "reason": "No security issues found",
    "report_url": "https://audits.example.com/report-123"
  }
}
```

This is signed with Sigstore and stored in the registry with the certificate containing:
- Issuer (OIDC provider URL)
- Subject (user/workflow identity)
- Email (if available)

### Trust Matching

When verifying trust, Enact:

1. Extracts OIDC identity from Sigstore certificate
2. Checks if it matches any trusted auditor pattern
3. Supports wildcards: `github:my-org/*` matches any identity from that org
4. Verifies Sigstore signature cryptographically
5. Checks Rekor transparency log for tampering

---

## Learn More

- **Sigstore Documentation** - https://docs.sigstore.dev
- **Rekor Transparency Log** - https://rekor.sigstore.dev
- **OIDC Explained** - https://openid.net/connect/
- **Enact Registry** - https://enact.io

---

## License

MIT License © 2025 Enact Protocol Contributors