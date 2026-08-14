---
name: documentation
description: Synchronized technical documentation, README authoring, Architecture Decision Records (ADRs), API schemas, and engineering logs.
---

# Documentation Skill

## 1. When Should I Use This?

Use this skill when:
* Creating or updating a repository `README.md`, `ARCHITECTURE.md`, `DEPLOYMENT.md`, or `CHANGELOG.md`.
* Writing Architecture Decision Records (ADRs) under `docs/decisions/` to chronicle non-trivial technical trade-offs.
* Documenting API endpoints, request/response formats, environment variables, or local development workflows.
* Synchronizing documentation after non-trivial code modifications.

Never document an intended or unbuilt feature as if it were already implemented.

---

## 2. What Should I Inspect First?

1. **Existing Documentation Artifacts**:
   * Check for `README.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `docs/`, `docs/decisions/`.
2. **Current Code State**: Check real function signatures, route paths, environment variables (`.env.example`), and Docker ports to ensure documentation matches reality 100%.

---

## 3. What Workflow Should I Follow?

```text
Identify Documentation Target (README, ADR, API docs, Changelog)
                     ↓
Audit Code Reality (Verify endpoints, configs, scripts)
                     ↓
Draft Structured, Accurate Markdown Content
                     ↓
Include Concrete Code Snippets & ASCII/Mermaid Diagrams
                     ↓
Cross-Link Related Documents
                     ↓
Review for Accuracy & Eliminate False Claims
```

### Standard Repository README Layout

```markdown
# Project Name

One-sentence description of what this system does and the problem it solves.

[![CI Status](https://img.shields.io/badge/CI-passing-brightgreen.svg)](#)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Key Features
- **Feature A**: Description with tech stack callout.
- **Feature B**: Description with tech stack callout.

---

## 🏗️ Architecture Overview
\`\`\`text
[ ASCII / Mermaid Diagram of Architecture ]
\`\`\`

---

## 🛠️ Quickstart (Local Development)

### 1. Prerequisites
- Python >= 3.12
- Node.js >= 20 (if frontend present)
- Docker & Docker Compose (optional)

### 2. Installation
\`\`\`bash
# Clone repository
git clone https://github.com/username/project-name.git
cd project-name

# Backend setup
uv venv .venv
source .venv/bin/activate # or .venv\Scripts\Activate.ps1
uv pip install -e ".[dev]"
cp .env.example .env

# Run development server
uvicorn app.main:app --reload --port 8000
\`\`\`

---

## 🧪 Testing & Verification
\`\`\`bash
pytest -v --tb=short
\`\`\`

---

## 📄 License
MIT License.
```

### Architecture Decision Record (ADR) Template (`docs/decisions/0001-record-title.md`)

```markdown
# ADR 0001: Use FAISS with SentenceTransformers for Vector Search

## Status
Accepted

## Context
We need low-latency, self-hosted semantic search over extracted OCR PDF text chunks. We considered external hosted vector databases (Pinecone, Qdrant) versus an embedded in-memory vector store (FAISS).

## Decision
We chose **FAISS** (`IndexFlatIP` with normalized embeddings) alongside `sentence-transformers/all-MiniLM-L6-v2`.

## Consequences
- **Positive**: Zero external network latency, zero hosting costs, trivial local Docker deployment.
- **Negative / Trade-offs**: Index must be rebuilt or persisted to disk on container restarts; limited to single-node memory capacity.
```

---

## 4. What Decisions Should I Make?

| Documentation Need | File / Location |
| :--- | :--- |
| **System Overview & Setup** | `README.md` (Project root) |
| **Component Boundaries & Data Flow** | `ARCHITECTURE.md` |
| **Hosting, Cloud & Container Setup** | `DEPLOYMENT.md` |
| **Major Architectural Choices** | `docs/decisions/NNNN-<topic>.md` (ADR) |
| **Version Releases & Breaking Changes** | `CHANGELOG.md` |

---

## 5. What Should I Avoid?

* **NEVER write aspirational documentation as fact**: Always accurately reflect current code capabilities.
* **NEVER include stale or broken code examples**: Test every command listed in `README.md` to ensure it works.
* **NEVER hardcode machine-specific local paths in docs**: Use relative paths or generic placeholder variables.

---

## 6. How Should I Verify Success?

```bash
# 1. Verify markdown formatting and table rendering
# (Ensure code fences and markdown headers are valid)

# 2. Re-test all copy-pasteable commands from README.md in a clean shell
```
