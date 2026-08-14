---
name: supply-chain-security
description: Software Bill of Materials (SBOM) generation, dependency vulnerability audits (pip-audit, npm audit), secret scanning, and license compliance.
---

# Supply Chain Security Skill

## 1. When Should I Use This?

Use this skill when:
* Auditing third-party dependencies for known Common Vulnerabilities and Exposures (CVEs).
* Generating Software Bill of Materials (SBOM) in **CycloneDX** or **SPDX** format.
* Configuring automated secret scanning (`gitleaks`, `detect-secrets`) in CI/CD pipelines.
* Verifying open-source license compliance (MIT, Apache-2.0 vs restrictive AGPL).
* Scanning container base images for OS-level vulnerabilities with **Trivy**.

---

## 2. What Should I Inspect First?

1. **Lockfiles**: `uv.lock`, `poetry.lock`, `package-lock.json`. Confirm that lockfiles are up to date and verified against manifests.
2. **Security Advisories**: Run vulnerability scanners to detect published CVEs in direct and transitive dependencies.
3. **Declared Licenses**: Check licenses of newly introduced packages to prevent license contamination.

---

## 3. What Workflow Should I Follow?

```text
Lockfile Integrity Verification (uv.lock / package-lock.json)
                     ↓
Dependency Vulnerability Audit (pip-audit / npm audit)
                     ↓
Secret Leakage Scan (Gitleaks / Regex Scanner)
                     ↓
License Compliance Audit (Permissive vs Copyleft)
                     ↓
Generate Software Bill of Materials (SBOM via CycloneDX / Syft)
                     ↓
Container Image Security Scan (Trivy)
                     ↓
Automate Gates in CI Pipeline
```

### Dependency Vulnerability Scanning

```bash
# Python dependency audit
pip-audit --desc

# Node.js dependency audit
npm audit --audit-level=high

# Container image audit
trivy image my-app-backend:latest
```

### Generating a CycloneDX SBOM

```bash
# Python SBOM generation (CycloneDX format)
cyclonedx-py pyproject.toml -o sbom-python.json

# Node.js SBOM generation
npm install -g @cyclonedx/cyclonedx-npm
cyclonedx-npm --output-file sbom-node.json
```

### GitHub Actions Security Pipeline Step

```yaml
# .github/workflows/security.yml
name: Supply Chain Security Audit

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          
      - name: Install pip-audit
        run: pip install pip-audit
        
      - name: Run Python Vulnerability Scan
        run: pip-audit
        
      - name: Run Secret Scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 4. What Decisions Should I Make?

| Vulnerability Severity | Action Protocol |
| :--- | :--- |
| **Critical / High CVE** | Must block PR merge. Immediately pin patched minor version in `pyproject.toml` or `package.json`. |
| **Medium / Low CVE** | Review exploitability in application context. If theoretical, schedule routine patch cycle. |
| **License Policy** | Allow: MIT, Apache 2.0, BSD-2-Clause, BSD-3-Clause, ISC. Require Review: GPL-3.0, AGPL-3.0 for commercial/proprietary SaaS distributions. |

---

## 5. What Should I Avoid?

* **NEVER ignore `npm audit` or `pip-audit` high/critical warnings** without documenting an explicit mitigation.
* **NEVER install unverified packages from untrusted third-party package indexes**.
* **NEVER disable security scans to make a broken CI build pass**.

---

## 6. How Should I Verify Success?

```bash
# 1. Run pip-audit locally
pip-audit --version && pip-audit

# 2. Run npm audit
npm audit

# 3. Verify SBOM output is valid JSON
python -c "import json; json.load(open('sbom-python.json')); print('SBOM valid!')"
```
