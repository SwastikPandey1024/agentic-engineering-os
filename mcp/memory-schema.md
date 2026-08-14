# Codebase Memory MCP Schema & Integration Standard

This document defines the structured entity-relation knowledge graph schema used by coding agents when interacting with the official **Codebase Memory MCP Server** (`@modelcontextprotocol/server-memory`).

---

## 🏛️ Architectural Demarcation

```text
┌────────────────────────┬─────────────────────────────────────────────────────────────┐
│ Mechanism              │ Role in the System                                          │
├────────────────────────┼─────────────────────────────────────────────────────────────┤
│ **Skills**             │ Procedural knowledge, decision trees, and step-by-step flows │
│ **Hooks**              │ Deterministic lifecycle automation (pre-commit, env checks) │
│ **MCP Tools & Memory** │ External tool execution and persistent cross-session memory │
│ **Subagents**          │ Delegated, isolated workers for parallel or deep tasks      │
└────────────────────────┴─────────────────────────────────────────────────────────────┘
```

---

## 📋 Entity Categories & Schemas

All memory nodes must adhere to standard entity types:

### 1. `Architecture`
* **Purpose**: Captures high-level system patterns, module boundaries, and communication flows.
* **Example Observations**:
  * "FastAPI backend adheres to 4-layer structure: API Routes -> Services -> Repositories -> Models."
  * "Frontend uses React 19 + TanStack Query for server state caching."

### 2. `Decision`
* **Purpose**: Records confirmed architectural decisions and tech stack selections.
* **Example Observations**:
  * "FAISS IndexFlatIP selected for local offline vector search over Pinecone to eliminate cloud costs."
  * "uv selected as standard Python package manager for 10x faster environment resolution."

### 3. `Dependency`
* **Purpose**: Documents pinned dependency constraints and compatibility requirements.
* **Example Observations**:
  * "TensorFlow pinned to 2.16.1 to maintain binary compatibility with Keras 3 and CUDA 12.2."
  * "Pydantic v2 core used for fast Rust-based JSON serialization."

### 4. `BugFix`
* **Purpose**: Chronicles non-obvious root-cause bug resolutions to prevent future regressions.
* **Example Observations**:
  * "Daylight Saving Time duplicate hour in November handled via groupby mean aggregation."
  * "BatchNorm layers kept frozen during DenseNet121 fine-tuning to prevent feature degradation."

### 5. `RejectedApproach`
* **Purpose**: Explains why a specific technology or design pattern was evaluated and rejected.
* **Example Observations**:
  * "Pinecone rejected due to 200ms external network latency and offline Docker deployment requirement."
  * "Client-side JWT storage in localStorage rejected in favor of HttpOnly secure cookies."

### 6. `DeploymentRule`
* **Purpose**: Documents hosting limits, port mappings, and infrastructure constraints.
* **Example Observations**:
  * "Render free tier requires connection pool size <= 5 to prevent PostgreSQL exhaustion."
  * "Vercel SPA routing requires rewrite rule /* -> /index.html in vercel.json."

### 7. `ReusableUtility`
* **Purpose**: Points future agents to existing shared code modules to avoid duplication.
* **Example Observations**:
  * "StatusBadge component located in frontend/src/components/ui/status-badge.tsx."
  * "PDF bounding box extractor located in app/services/ocr_service.py."

---

## 🔗 Relation Types

Link entities using meaningful directed relations:
* `implements` (e.g. `OCRService` `implements` `MultiModalPipeline`)
* `supersedes` (e.g. `Decision: UV` `supersedes` `Decision: Pipenv`)
* `depends_on` (e.g. `RAGService` `depends_on` `VectorStore`)
* `resolved_in` (e.g. `BugFix: DST` `resolved_in` `DataEngineeringPipeline`)
* `configured_for` (e.g. `RenderConfig` `configured_for` `FastAPIBackend`)

---

## 🚫 Critical Security Invariant (Zero Secrets)

> [!CAUTION]
> **NEVER store secrets in MCP memory**:
> * NO API keys (OpenAI, Anthropic, AWS, Stripe).
> * NO Database passwords or connection strings with credentials.
> * NO JWT Secret keys or private RSA certificates.
> * NO Personal Identifiable Information (PII).
> * NO Full contents of `.env` files.
