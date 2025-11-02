# Sigstore Implementation Guide

**Technical reference for how Enact uses Sigstore for cryptographic signing and verification.**

---

## Overview

Enact uses **Sigstore** to cryptographically sign and verify all registry tools. This ensures that tools are authentic, haven't been tampered with, and come from verified publishers.

**Key Components:**
- **Sigstore** - Open-source signing infrastructure (Linux Foundation)
- **GitHub OAuth** - Identity provider for publishers
- **Sigstore Bundles** - Self-contained signature files for offline verification

---

## Infrastructure: Public Sigstore

Enact uses the **public Sigstore infrastructure** maintained by the Linux Foundation. You don't need to run any signing infrastructure.

### Services Used

**Fulcio** (https://fulcio.sigstore.dev)
- Certificate Authority (CA) that issues short-lived signing certificates
- Certificates are valid for 10-20 minutes
- Identity tied to GitHub OAuth login

**Rekor** (https://rekor.sigstore.dev)
- Public transparency log for all signatures
- Provides tamper-evident history
- Contains Merkle tree proofs for verification

**GitHub OAuth**
- Authentication provider
- Publisher identity embedded in certificates
- Format: `repo:org/repo:ref:refs/heads/main`

### Why Public Sigstore?

**No infrastructure to manage:**
- Zero setup required
- No keys to store or rotate
- No certificate authority to maintain
- Free to use

**Battle-tested:**
- Used by Kubernetes, npm, Python packages, GitHub Actions
- Maintained by the Linux Foundation
- Well-audited and trusted

**Transparent:**
- All signatures publicly logged in Rekor
- Impossible to backdate or hide signatures
- Provides cryptographic proof of when tools were signed

---

## Signing Process

### Step-by-Step: What Happens When You Sign

```bash
enact sign ./my-tool/
```

**1. Create Tarball**
```typescript
// Bundle the entire tool directory
const tarball = await createTarball('./my-tool/', {
  ignore: ['.git', 'node_modules', '__pycache__', '.env']
});
```

**2. Compute Hash**
```typescript
const hash = crypto.createHash('sha256');
hash.update(tarball);
const digest = hash.digest('hex');
```

**3. Authenticate with GitHub**
```typescript
// Opens browser for GitHub OAuth flow
const token = await authenticateWithGitHub({
  clientId: SIGSTORE_CLIENT_ID,
  redirectUri: 'http://localhost:8080/callback'
});
```

**4. Request Certificate from Fulcio**
```typescript
import { sign } from '@sigstore/sign';

const bundle = await sign(tarball, {
  identityToken: token,  // GitHub OIDC token
  fulcioURL: 'https://fulcio.sigstore.dev'
});
```

Fulcio issues a certificate containing:
- **Subject:** `repo:your-org/your-repo:ref:refs/heads/main`
- **Issuer:** `https://token.actions.githubusercontent.com`
- **Validity:** 10-20 minutes from issuance
- **Extensions:** Workflow name, commit SHA, etc. (if from GitHub Actions)

**5. Generate Signature**
```typescript
// Sign the tarball hash with ECDSA P-256
const signature = await createSignature(digest, ephemeralPrivateKey);
```

**6. Submit to Rekor**
```typescript
// Upload to transparency log
const logEntry = await rekor.createEntry({
  kind: 'intoto',
  apiVersion: '0.0.2',
  spec: {
    content: {
      envelope: dsseEnvelope,
      hash: { algorithm: 'sha256', value: digest }
    }
  }
});

// Rekor returns:
// - Log index (unique entry ID)
// - Integrated time (timestamp)
// - Inclusion proof (Merkle tree proof)
```

**7. Create Sigstore Bundle**
```typescript
// Save complete bundle to .sigstore-bundle
const bundle = {
  mediaType: 'application/vnd.dev.sigstore.bundle+json;version=0.3',
  verificationMaterial: {
    x509CertificateChain: {
      certificates: [{ rawBytes: certPEM }]
    },
    tlogEntries: [{
      logIndex: logEntry.logIndex,
      logId: { keyId: rekorPublicKey },
      integratedTime: logEntry.integratedTime,
      inclusionProof: logEntry.inclusionProof,
      canonicalizedBody: logEntry.body
    }]
  },
  messageSignature: {
    messageDigest: {
      algorithm: 'SHA2_256',
      digest: digest
    },
    signature: signature
  }
};

fs.writeFileSync('.sigstore-bundle', JSON.stringify(bundle, null, 2));
```

---

## Sigstore Bundle Format

The `.sigstore-bundle` file is a **self-contained JSON file** with everything needed for offline verification.

### Structure

```json
{
  "mediaType": "application/vnd.dev.sigstore.bundle+json;version=0.3",
  "verificationMaterial": {
    "x509CertificateChain": {
      "certificates": [
        {
          "rawBytes": "MIIGpzCCBi2gAwIBAgIUYqJkSoOx6d5Fqqq..."
        }
      ]
    },
    "tlogEntries": [
      {
        "logIndex": "69281180",
        "logId": {
          "keyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RF..."
        },
        "kindVersion": {
          "kind": "intoto",
          "version": "0.0.2"
        },
        "integratedTime": "1707152810",
        "inclusionPromise": {
          "signedEntryTimestamp": "MEUCIQCM6/XSm99SLhXJbplg..."
        },
        "inclusionProof": {
          "logIndex": "65117749",
          "rootHash": "2zwYlYPIGczxN20gXY3wDCXel9K78ldp...",
          "treeSize": "65117750",
          "hashes": [
            "BUW6CnUEsfQhTWwiINO7yisX5mPQSJ2+",
            "n5MjF4qrCz1EZ7Sx/bJhO...",
            "..."
          ],
          "checkpoint": {
            "envelope": "rekor.sigstore.dev - 2605736670972794746\n..."
          }
        },
        "canonicalizedBody": "eyJhcGlWZXJzaW9uIjoiMC4wLjIiLCJraW5kIjoi..."
      }
    ]
  },
  "messageSignature": {
    "messageDigest": {
      "algorithm": "SHA2_256",
      "digest": "abc123def456..."
    },
    "signature": "MEUCIQD3jNlPZStk4rPSR0dvrMxMmT2ebqnX..."
  }
}
```

### What's Included

**Certificate Chain (`x509CertificateChain`):**
- The ephemeral certificate issued by Fulcio
- Contains publisher identity (GitHub repo/user)
- Valid for 10-20 minutes from issuance

**Transparency Log Entry (`tlogEntries`):**
- Proof the signature was logged in Rekor
- Merkle tree inclusion proof
- Timestamped entry (when signature was created)
- Signed checkpoint from Rekor

**Signature (`messageSignature`):**
- SHA-256 hash of the signed content
- ECDSA P-256 signature
- Can be verified against the certificate's public key

### Why Bundle Format?

**Self-contained:**
- Everything needed for verification in one file
- No network requests required
- Works in air-gapped environments

**Portable:**
- Can be shared alongside tools
- Future-proof (even if Rekor goes down)
- Standardized format across ecosystems

**Efficient:**
- Single file to store/transfer
- Includes cryptographic proofs
- Enables offline verification

---

## Verification Process

### Step-by-Step: What Happens During Verification

```bash
enact install acme-corp/data/processor
```

**1. Download Tool + Bundle**
```typescript
const response = await fetch(`${REGISTRY}/api/tools/acme-corp/data/processor/latest`);
const { bundle_url, sigstore_bundle } = await response.json();

const tarball = await fetch(bundle_url).then(r => r.arrayBuffer());
```

**2. Verify Bundle Integrity**
```typescript
import { verify } from '@sigstore/verify';

const result = await verify(sigstore_bundle, tarball, {
  // Public Fulcio root CA
  ctLogPublicKeys: FULCIO_ROOT_CA,
  // Rekor public key for log verification
  tlogPublicKeys: REKOR_PUBLIC_KEY
});
```

**3. Verification Steps (Performed by @sigstore/verify)**

**a. Verify Certificate Chain**
```typescript
// Check certificate chains to Fulcio CA
const certChain = bundle.verificationMaterial.x509CertificateChain;
const isValidChain = verifyCertificateChain(certChain, FULCIO_ROOT_CA);
```

**b. Verify Signature**
```typescript
// Extract public key from certificate
const publicKey = extractPublicKey(certChain.certificates[0]);

// Verify signature matches digest
const isValidSignature = crypto.verify(
  'sha256',
  Buffer.from(bundle.messageSignature.messageDigest.digest, 'hex'),
  publicKey,
  Buffer.from(bundle.messageSignature.signature, 'base64')
);
```

**c. Verify Transparency Log**
```typescript
// Verify entry exists in Rekor
const tlogEntry = bundle.verificationMaterial.tlogEntries[0];

// Check Merkle tree inclusion proof
const isInLog = verifyInclusionProof(
  tlogEntry.inclusionProof,
  tlogEntry.logIndex,
  REKOR_PUBLIC_KEY
);

// Verify signed checkpoint
const isValidCheckpoint = verifyCheckpoint(
  tlogEntry.inclusionProof.checkpoint,
  REKOR_PUBLIC_KEY
);
```

**d. Check Certificate Validity**
```typescript
// Certificate must have been valid at time of signing
const integratedTime = new Date(tlogEntry.integratedTime * 1000);
const cert = parseCertificate(certChain.certificates[0]);

if (integratedTime < cert.notBefore || integratedTime > cert.notAfter) {
  throw new Error('Certificate was not valid at time of signing');
}
```

**e. Verify Content Hash**
```typescript
// Recompute hash of downloaded tarball
const computedHash = crypto.createHash('sha256').update(tarball).digest('hex');

// Must match hash in bundle
if (computedHash !== bundle.messageSignature.messageDigest.digest) {
  throw new Error('Content hash mismatch');
}
```

**4. Extract Publisher Identity**
```typescript
const cert = parseCertificate(bundle.verificationMaterial.x509CertificateChain.certificates[0]);
const identity = cert.extensions.subjectAlternativeName;
// e.g., "repo:acme-corp/tools:ref:refs/heads/main"
```

**5. Check Trust Policy (Optional)**
```typescript
// Apply user/registry trust policies
if (!isTrustedPublisher(identity)) {
  throw new Error(`Untrusted publisher: ${identity}`);
}
```

**6. Cache Verified Tool**
```typescript
// Extract to cache
await extractTarball(tarball, '~/.enact/cache/acme-corp/data/processor/v2.1.0/');

// Save bundle for future verification
await fs.writeFile(
  '~/.enact/cache/acme-corp/data/processor/v2.1.0/.sigstore-bundle',
  JSON.stringify(sigstore_bundle)
);
```

---

## Registry Implementation

The Enact registry is a **simple storage service**—it doesn't run any signing infrastructure. It just stores tools and their signature bundles.

### Publishing Endpoint

```typescript
// POST /api/tools/{org}/{path}/{tool}/v{version}
import { verify } from '@sigstore/verify';

async function publishTool(req: Request, res: Response) {
  const { org, path, tool, version } = req.params;
  const { tarball, sigstore_bundle } = req.files;
  
  // Parse the bundle
  const bundle = JSON.parse(sigstore_bundle);
  
  // 1. Verify signature is cryptographically valid
  const isValid = await verify(bundle, tarball);
  if (!isValid) {
    return res.status(400).json({ 
      error: 'Invalid signature' 
    });
  }
  
  // 2. Extract publisher identity from certificate
  const cert = parseCertificate(
    bundle.verificationMaterial.x509CertificateChain.certificates[0]
  );
  const identity = cert.extensions.subjectAlternativeName;
  // e.g., "repo:acme-corp/tools:ref:refs/heads/main"
  
  // 3. Enforce namespace ownership
  // Only repo:acme-corp/* can publish to acme-corp/*
  const expectedPrefix = `repo:${org}/`;
  if (!identity.startsWith(expectedPrefix)) {
    return res.status(403).json({ 
      error: `${identity} cannot publish to ${org}/* namespace`,
      detail: `Only repositories under ${org}/ can publish to this namespace`
    });
  }
  
  // 4. Store tarball in CDN/S3
  const filename = `${org}-${path.replace(/\//g, '-')}-${tool}-v${version}.tar.gz`;
  await storage.put(`tools/${filename}`, tarball);
  
  // 5. Store metadata + bundle in database
  await db.tools.insert({
    name: `${org}/${path}/${tool}`,
    version: version,
    filename: filename,
    sigstore_bundle: bundle,
    publisher_identity: identity,
    published_at: new Date(),
    description: extractDescription(tarball) // Parse enact.md
  });
  
  return res.json({ 
    success: true,
    message: `Published ${org}/${path}/${tool}@${version}`
  });
}
```

### Download Endpoint

```typescript
// GET /api/tools/{org}/{path}/{tool}/v{version}
async function getTool(req: Request, res: Response) {
  const { org, path, tool, version } = req.params;
  
  // Fetch from database
  const toolRecord = await db.tools.findOne({
    name: `${org}/${path}/${tool}`,
    version: version === 'latest' ? undefined : version
  });
  
  if (!toolRecord) {
    return res.status(404).json({ error: 'Tool not found' });
  }
  
  // Return bundle URL + inline sigstore bundle
  return res.json({
    bundle_url: `https://cdn.enactprotocol.com/tools/${toolRecord.filename}`,
    sigstore_bundle: toolRecord.sigstore_bundle,
    metadata: {
      name: toolRecord.name,
      version: toolRecord.version,
      description: toolRecord.description,
      published_at: toolRecord.published_at,
      publisher_identity: toolRecord.publisher_identity
    }
  });
}
```

### What the Registry Does

**Stores:**
- Tool tarballs (in CDN/S3)
- Sigstore bundles (in database as JSON)
- Metadata (name, version, publisher, etc.)

**Enforces:**
- Namespace ownership rules
- Valid signatures at publish time (optional but recommended)

**Does NOT:**
- Issue certificates (Fulcio does this)
- Maintain transparency logs (Rekor does this)
- Manage keys or PKI infrastructure
- Re-verify signatures at download time (CLI does this)

The registry is effectively a **dumb storage service** with namespace ownership checks.

---

## Trust Model

### Anyone Can Sign (via Public Sigstore)

With public Sigstore:
- ✅ Anyone with a GitHub account can sign tools
- ✅ Signatures are cryptographically valid
- ✅ Identity is embedded in certificates

### Trust is Managed at Two Levels

**1. Registry Level: Namespace Ownership**

The registry enforces that only authorized identities can publish to specific namespaces:

```typescript
// Rule: repo:acme-corp/* can publish to acme-corp/*
//       repo:other-org/* CANNOT publish to acme-corp/*

if (!identity.startsWith(`repo:${namespace}/`)) {
  throw new Error('Unauthorized');
}
```

This is similar to npm's package ownership—anyone can create an npm account and sign packages, but only verified owners can publish to specific package names.

**2. Client Level: User Trust Preferences (Optional)**

Users can configure trust preferences:

```yaml
# ~/.enact/config.yaml
trust:
  # Auto-install without prompting
  verified:
    - "repo:EnactProtocol/*"
    - "repo:acme-corp/tools:*"
  
  # Prompt before installing
  prompt:
    - "*@github.com"
  
  # Never install
  deny:
    - "repo:sketchy-org/*"
```

### Publisher Identity is Always Visible

```bash
$ enact get acme-corp/data/processor

Name: acme-corp/data/processor
Version: 2.1.0
Description: Process and validate CSV files
Publisher: repo:acme-corp/tools:ref:refs/heads/main
Signed: 2025-10-24T15:30:00Z
```

Users always know who published each tool and can make informed decisions.

---

## Implementation Libraries

### For the CLI

```bash
npm install @sigstore/sign @sigstore/verify @sigstore/bundle
```

**Signing:**
```typescript
import { sign } from '@sigstore/sign';

const bundle = await sign(Buffer.from(tarballContent));
// Returns complete sigstore bundle
```

**Verification:**
```typescript
import { verify } from '@sigstore/verify';

const result = await verify(bundle, Buffer.from(tarballContent), {
  certificateIdentity: 'repo:acme-corp/tools',
  certificateIssuer: 'https://token.actions.githubusercontent.com'
});
```

### For the Registry (Optional)

You can use the same libraries to verify signatures at publish time:

```typescript
import { verify } from '@sigstore/verify';

// Verify signature is valid before storing
const isValid = await verify(bundle, tarball);
```

But this is optional—verification primarily happens client-side.

---

## Self-Hosted Sigstore (Advanced)

If you need a private signing infrastructure (not recommended for most users), you would need to run:

**Infrastructure Required:**
1. **Fulcio** (Certificate Authority)
   - Requires a root CA (AWS CloudHSM, Private CA, or manual)
   - Requires intermediate CA certificate chain
   - Uses KMS for signing operations

2. **Rekor** (Transparency Log)
   - Stores all signatures
   - Provides Merkle tree proofs

3. **OAuth Provider** (or use GitHub)
   - Authenticates publishers
   - Issues OIDC tokens

4. **TUF Server** (optional)
   - Distributes root of trust
   - Manages key rotation

**When You'd Need This:**
- ❌ Cannot use public transparency logs
- ❌ Cannot use GitHub for authentication
- ❌ Need custom certificate policies
- ❌ Air-gapped environments

**For 99% of users, public Sigstore is the right choice.** It's free, maintained by the Linux Foundation, and used by major projects (Kubernetes, npm, Python, etc.).

---

## Security Guarantees

### What Sigstore Provides

**Authenticity:**
- Tools are signed by a verified publisher (GitHub identity)
- Signatures cannot be forged without access to the publisher's GitHub account

**Integrity:**
- Any tampering with the tool invalidates the signature
- Hash verification ensures content hasn't changed

**Transparency:**
- All signatures are logged in public Rekor
- Impossible to backdate signatures
- Anyone can audit what was signed and when

**Non-repudiation:**
- Publisher cannot deny signing a tool (logged in Rekor)
- Cryptographic proof of who signed what and when

### What Sigstore Does NOT Provide

**Code Quality:**
- Signature only proves identity and integrity
- Does not guarantee the tool is safe or well-written

**Continuous Trust:**
- Certificate is valid at time of signing
- Compromised GitHub account = compromised signing ability

**Access Control:**
- Anyone with a GitHub account can sign
- Trust decisions must be made by registry/users

---

## Resources

- **Sigstore Project:** https://sigstore.dev
- **Fulcio (Public CA):** https://fulcio.sigstore.dev
- **Rekor (Public Log):** https://rekor.sigstore.dev
- **Sigstore Libraries:** https://github.com/sigstore/sigstore-js
- **Specification:** https://github.com/sigstore/protobuf-specs

---

## License

MIT License © 2025 Enact Protocol Contributors
