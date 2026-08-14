# Security Policy

## Supported Versions

| Version | Supported          |
| :--- | :--- |
| `v1.0.x` | :white_check_mark: |

---

## 🔒 Secret Zero-Exposure Invariant

AgenticOS enforces a strict **Zero-Secret Invariant**:
* No real API keys, passwords, bearer tokens, or sensitive values may ever be committed to the repository.
* All configuration templates must utilize sanitized `.env.example` placeholders (`YOUR_API_KEY`, `${API_KEY}`).
* Codebase Memory MCP schemas explicitly prohibit storing secrets in graph memory.

---

## 🚨 Reporting a Vulnerability

If you discover a potential security vulnerability in AgenticOS:
1. **DO NOT** open a public issue.
2. Please report the issue via GitHub's Private Vulnerability Reporting or email the maintainers at `security@agenticos.dev`.
3. We aim to acknowledge reports within 48 hours and provide a remediation timeline.
