---
name: project-knowledge
description: Codebase Memory MCP read and write protocols, durable architectural decisions, root-cause knowledge persistence, and secret-free knowledge graphs.
---

# Project Knowledge (Codebase Memory) Skill

## 1. When Should I Use This?

Use this skill when:
* Reading prior architectural decisions, known root causes, or design constraints before undertaking major changes.
* Writing durable project knowledge, newly discovered constraints, or resolved root causes after completing a significant task.
* Interacting with the official **Codebase Memory MCP Server** (`@modelcontextprotocol/server-memory`) or local knowledge graph.

Never use this skill to store ephemeral chatter, full file dumps, or raw code that is already tracked in Git.

---

## 2. What Should I Inspect First?

1. **MCP Memory Server Availability**:
   * Check if MCP memory tools are available in the current session (`codebase-memory-mcp` tools like `search_graph`, `query_graph`, or standard tools like `read_graph`, `create_entities`, `create_relations`, `search_nodes`).
   * **Use existing active MCP servers directly** — never attempt to install or spawn a duplicate server.
2. **Local Memory Manifest**:
   * Inspect `docs/decisions/` (ADRs), `mcp/memory-schema.md`, or project knowledge files.
3. **Secret Scan**:
   * Ensure NO credentials, `.env` values, API keys, passwords, or personal identifying information are present in memory payloads.

---

## 3. What Workflow Should I Follow?

```text
┌─────────────────────────────────────────────────────────────┐
│ READ MEMORY TRIGGERS                                        │
│  - Before major architecture changes                        │
│  - Before major dependency additions / upgrades             │
│  - Before database schema alterations                       │
│  - Before deployment platform / cloud config changes        │
│  - Before investigating recurring or complex bugs           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               │ [ Execute Development / Task ]
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ WRITE MEMORY TRIGGERS                                       │
│  - After completing an Architecture Decision Record (ADR)   │
│  - After isolating & fixing a non-obvious root-cause bug    │
│  - After rejecting an approach with a concrete reason       │
│  - After discovering critical performance or latency limits │
│  - After verifying a production deployment runbook          │
└─────────────────────────────────────────────────────────────┘
```

### Memory Entity Categories & Schema

```text
┌──────────────────┬───────────────────────────────────────────────────────────────────┐
│ Entity Type      │ Purpose & Example Observation                                     │
├──────────────────┼───────────────────────────────────────────────────────────────────┤
│ Architecture     │ Core system patterns ("FastAPI 4-tier layered architecture")       │
│ Decision         │ Chosen tech & rationale ("FAISS chosen for low-latency local RAG")│
│ Dependency       │ Pinned constraint reasons ("TensorFlow 2.16 pinned for Keras 3")  │
│ BugFix           │ Resolved root cause ("DST duplicate hour resolved via mean agg")  │
│ RejectedApproach │ Failed experiment ("Pinecone rejected due to external API latency")│
│ DeploymentRule   │ Hosting constraints ("Render free tier requires pool_size=5")     │
│ ReusableUtility  │ Shared library location ("StatusBadge in src/components/ui/")     │
└──────────────────┴───────────────────────────────────────────────────────────────────┘
```

### Structured Memory Creation Pattern (MCP Tool Format)

```json
{
  "entities": [
    {
      "name": "Decision: FAISS Vector Store",
      "entityType": "Decision",
      "observations": [
        "Selected FAISS IndexFlatIP with normalized SentenceTransformer embeddings.",
        "Chosen over Pinecone and Qdrant to enable 100% self-hosted, offline Docker deployments with zero network overhead.",
        "Requires re-indexing or local disk serialization upon container startup."
      ]
    },
    {
      "name": "BugFix: Daylight Saving Time Timestamp Duplication",
      "entityType": "BugFix",
      "observations": [
        "Historical hourly energy data contains 1 duplicate hour in November due to clock fallback.",
        "Resolved by grouping by timestamp and applying mean aggregation in data_engineering/pipeline.py.",
        "Prevents indexing errors in downstream lag and rolling statistics calculations."
      ]
    }
  ],
  "relations": [
    {
      "from": "Decision: FAISS Vector Store",
      "to": "DocMind RAG Pipeline",
      "relationType": "implements_semantic_search_for"
    }
  ]
}
```

---

## 4. What Decisions Should I Make?

| Information Category | Decision Rule |
| :--- | :--- |
| **Is it worth storing in memory?** | Store if it prevents future agents or developers from making the same mistake or repeating a 30-minute discovery phase. Do not store trivial facts like "app.py exists". |
| **Granularity** | Use concise, structured bullet points (1-3 sentences per observation). Avoid giant multi-page markdown dumps inside single memory nodes. |
| **Format** | Link related decisions using relations (e.g. `Decision X` `supersedes` `Decision Y` or `BugFix A` `resolved_in` `Module B`). |

---

## 5. What Should I Avoid?

* **NEVER store secrets in memory**: API keys, database connection strings with passwords, JWT secret tokens, and bearer tokens are strictly forbidden.
* **NEVER store speculative assumptions**: Only store decisions that have been tested, approved, or verified.
* **NEVER store transient debug logs**: Memory is for durable, long-term engineering knowledge.

---

## 6. How Should I Verify Success?

```bash
# 1. Query memory to verify newly added entities
# (Using MCP search_nodes tool or inspecting local ADRs)

# 2. Verify ADR sync
ls docs/decisions/
```
