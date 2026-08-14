---
name: adr-management
description: Architecture Decision Record (ADR) creation, lifecycle management, alternative evaluation, and trade-off documentation under docs/decisions/.
---

# ADR Management Skill

## 1. When Should I Use This?

Use this skill when:
* Making significant, non-obvious, or difficult-to-reverse architectural decisions (Framework, Database, Vector DB, LLM provider, Package manager, Deployment host, Auth strategy, Caching, Observability, Scaling).
* Evaluating competing architectural alternatives with explicit trade-offs.
* Superseding or deprecating an earlier architectural decision.
* Maintaining the `docs/decisions/` repository index.

Do NOT use ADRs for trivial bug fixes, routine variable renames, or minor UI tweaks.

---

## 2. What Should I Inspect First?

1. **Existing ADRs**: Inspect `docs/decisions/` to identify previous decisions and the next sequential ID (e.g. `0001`, `0002`).
2. **Current Constraints**: Technical limitations, budget, hosting environment, compliance, or team skillset.
3. **Competing Options**: Identify at least two viable alternatives to the chosen approach.

---

## 3. What Workflow Should I Follow?

```text
Identify Significant Architecture Choice
                 ↓
Assign Next Sequential Number (docs/decisions/NNNN-title.md)
                 ↓
Draft Context & Problem Statement
                 ↓
List Concrete Alternatives Considered with Pros & Cons
                 ↓
Record Decision & Justification
                 ↓
Document Positive & Negative Consequences
                 ↓
Define Explicit Verification / Validation Criteria
                 ↓
Update docs/decisions/README.md Index & MCP Codebase Memory
```

### Canonical ADR Template

```markdown
# ADR-0001: Selection of FAISS and SentenceTransformers for Embedded RAG

## Status
Accepted

## Date
2026-08-14

## Context
DocMind requires real-time semantic retrieval over extracted OCR PDF text chunks. We need sub-50ms query latency, zero external API costs, and full operational support inside self-hosted Docker containers without relying on external cloud vector databases.

## Alternatives Considered

### Alternative 1: Pinecone / Managed Cloud Vector DB
* **Pros**: Fully managed, auto-scaling, built-in metadata filtering.
* **Cons**: Introduces external network latency (100-300ms roundtrip), requires recurring monthly subscription, fails in air-gapped/offline Docker environments.

### Alternative 2: PostgreSQL + pgvector
* **Pros**: Single unified database for relational tables and embeddings.
* **Cons**: Higher memory usage for index maintenance inside small container instances; slightly higher query latency than pure C++ FAISS.

### Alternative 3: FAISS (Facebook AI Similarity Search) + SentenceTransformers (Chosen)
* **Pros**: In-memory C++ execution provides sub-10ms similarity search; runs 100% locally inside Docker; zero external subscription costs.
* **Cons**: Index must be serialized to disk or rebuilt upon container restarts; memory is bounded by single-node RAM.

## Decision
We choose **FAISS** (`IndexFlatIP` with normalized embeddings) paired with `sentence-transformers/all-MiniLM-L6-v2`.

## Consequences
* **Positive**: Blazing fast retrieval, zero external dependencies, reproducible local testing.
* **Negative / Mitigations**: We must implement local index disk persistence in `storage/vectorstore/` and reload on startup via FastAPI lifespan handlers.

## Verification
* Unit tests in `tests/unit/test_rag.py` must verify retrieval latency < 50ms across 1,000 indexed chunks.
* Docker container must start and query without internet access.
```

---

## 4. What Decisions Should I Make?

| ADR Lifecycle Status | Definition |
| :--- | :--- |
| **Proposed** | Under active discussion or prototype evaluation. |
| **Accepted** | Approved and actively being implemented or deployed. |
| **Superseded** | Replaced by a newer decision (must reference `Superseded by ADR-XXXX`). |
| **Deprecated** | No longer relevant or actively phased out. |

---

## 5. What Should I Avoid?

* **NEVER write ADRs after the fact without documenting alternatives**: The primary value of an ADR is explaining *why* alternatives were rejected.
* **NEVER hide negative consequences**: Every architectural choice has trade-offs; document them honestly.
* **NEVER include secrets, passwords, or internal URLs in ADRs**.

---

## 6. How Should I Verify Success?

```bash
# 1. Verify ADR exists and has all required sections
python -c "
import os, glob
adrs = glob.glob('docs/decisions/*.md')
required = ['Status', 'Context', 'Decision', 'Alternatives Considered', 'Consequences', 'Verification']
for adr in adrs:
    content = open(adr, encoding='utf-8').read()
    for section in required:
        assert section in content, f'Missing {section} in {adr}'
print(f'All {len(adrs)} ADRs validated with complete structure.')
"
```
