# AgenticOS

<div align="center">

### **The Engineering Operating System for AI Coding Agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org)
[![OS: Windows | macOS | Linux](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-green)]()
[![toolchain: uv](https://img.shields.io/badge/toolchain-uv-purple?logo=astral)](https://github.com/astral-sh/uv)
[![Skills: 30+](https://img.shields.io/badge/Skills-30%2B%20Loaded-emerald)](SKILLS_INDEX.md)
[![CI Quality Gate](https://img.shields.io/badge/CI-Quality%20Gate-emerald)](.github/workflows/ci.yml)

<br/>

> **Turn AI coding from ad-hoc code generation into a repeatable engineering workflow.**

[Origin Story](#-where-agenticos-came-from) • [Quickstart](#-quickstart) • [Architecture](#-architecture) • [Skills Catalog](SKILLS_INDEX.md) • [Case Studies](docs/case-studies/dependency-isolation.md) • [Benchmarks](benchmarks/) • [Contributing](CONTRIBUTING.md)

</div>

---

## 🌱 Where AgenticOS Came From

AgenticOS started as an experiment after learning about the **Agent Skills paradigm**: if an AI coding agent can be equipped with specialized knowledge and repeatable task workflows, could the same principle be applied to software engineering itself?

AI coding assistants are capable of generating syntax rapidly. However, building reliable, long-lived software requires more than raw model intelligence—it requires engineering context, deterministic boundaries, verification discipline, and institutional memory.

What began as an exploration evolved into a cohesive, open-source engineering operating system:
* **30+ Modular Skills** encoding procedural engineering workflows and decision matrices.
* **Deterministic Guardrails & Hooks** that block unisolated or broken environments before commands execute.
* **Project Memory & MCP Schemas** for persisting durable architectural decisions across sessions.
* **Adaptive Documentation** scaling documentation depth to actual project complexity.
* **Automated Verification & Secret Scanners** maintaining a strict zero-secret invariant.
* **5 Production Starter Archetypes** providing clean foundations across services, ML, and fullstack apps.

> *Note: AgenticOS is an independent open-source project inspired by the broader agent skills movement and is not affiliated with, sponsored by, or endorsed by Anthropic.*

---

## ⚡ The Problem: Speed Without Structure

Modern AI coding agents generate code at extraordinary speed. But without explicit engineering standards and guardrails, they behave like hyper-productive junior developers:

* **Fast ≠ Reliable**: They install unpinned packages globally, polluting system environments and breaking neighboring projects.
* **Correct ≠ Maintainable**: They produce 2,000-line monolithic files instead of clean, layered domain boundaries.
* **Passing Tests ≠ Architecture-Compliant**: They bypass dependency injection, hardcode configuration values, and skip error handling.
* **Generated ≠ Production-Ready**: They omit rollback plans, expose sensitive keys in manifests, and hallucinate unbuilt features in documentation.

> **AI coding agents can write code. They still need engineering discipline.**

---

## 💡 The Thesis

> **AgenticOS treats engineering discipline as infrastructure for AI agents.**

The goal of AgenticOS is not to add bureaucracy or slow coding agents down. The goal is to make sound engineering behavior **reusable**, **deterministic**, and **repeatable**—turning ad-hoc prompt reminders into executable system invariants.

---

## 🏛️ Architecture

AgenticOS decouples engineering into clear, specialized operational layers:

```text
                       HUMAN / DEVELOPER
                               │
                               ▼
                     ┌──────────────────┐
                     │    AGENTS.md     │
                     │ Always-on rules  │
                     └────────┬─────────┘
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
          SKILLS            HOOKS             MCP
        Knowledge        Enforcement      Tools/Memory
        (30+ modules)    (Python engine)  (Graph schemas)
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                          SUBAGENTS
                         Delegation
                              │
                              ▼
                       AI CODING AGENT
                              │
                              ▼
                      VERIFIED SOFTWARE
                              │
                              ▼
                     EMPIRICAL BENCHMARKS
```

### Core Separation of Concerns
* 📜 **Invariants (`AGENTS.md`)**: Foundational, always-on rules governing environment isolation, security, and verification.
* 🧠 **Skills (`.agents/skills/`)**: 30+ procedural modules answering the 6 Core Questions across domains.
* 🛡️ **Hooks (`hooks/`)**: Standard-library Python engine and cross-platform wrappers enforcing virtual environments and lockfiles.
* 🧩 **MCP Layer (`mcp/`)**: Structured schemas connecting codebase memory tools for persistent architectural decisions.
* 🤖 **Subagents**: Isolated context sandboxes for complex, multi-phase refactoring or audit tasks.

---

## 🧩 Core Components

| Component | Location | Role in the System |
| :--- | :--- | :--- |
| **Universal Invariants** | [`AGENTS.md`](AGENTS.md) | High-priority rules: hard environment isolation, inspection before modification, zero-secret leakage. |
| **Modular Skills** | [`.agents/skills/`](.agents/skills/) | 30 domain-specific engineering guides with triggers, checklists, step-by-step workflows, and verification steps. |
| **Deterministic Hooks** | [`hooks/`](hooks/) | Canonical validation engine (`environment_guard.py`) with PowerShell (`.ps1`) and Bash (`.sh`) wrappers. |
| **Codebase Memory MCP** | [`mcp/`](mcp/) | 7-entity graph schema (`ArchitectureDecision`, `ServiceBoundary`, `RootCauseAnalysis`) for persistent knowledge. |
| **Documentation Orchestrator** | [`.agents/skills/documentation-orchestrator/`](.agents/skills/documentation-orchestrator/SKILL.md) | 5-tier adaptive documentation framework preventing documentation drift. |
| **Testing & Quality** | [`.agents/skills/testing-quality/`](.agents/skills/testing-quality/SKILL.md) | Standardized testing pyramid (Unit, Integration, Regression) with strict execution verification. |
| **Security & Secrets** | [`SECURITY.md`](SECURITY.md) / [`.agents/skills/security-secrets/`](.agents/skills/security-secrets/SKILL.md) | Enforced Zero-Secret Invariant, `.env.example` templates, and automated regex scanning. |
| **Release Engineering** | [`.agents/skills/release-engineering/`](.agents/skills/release-engineering/SKILL.md) | SemVer release gates, changelog automation, and verified rollback runbooks. |
| **Starter Archetypes** | [`templates/`](templates/) | 5 production starter templates pre-configured with `pyproject.toml`, test suites, and strict isolation. |

---

## ⚖️ Before vs. After AgenticOS

| Engineering Dimension | Raw Coding Agent (Before) | AgenticOS Workflow (After) | Evidence / Validation |
| :--- | :--- | :--- | :--- |
| **Environment Management** | Bare `pip install` in global Python. | Strictly isolated `.venv/`, `.python-version` pinned, `uv sync` lockfiles. | Blocked by deterministic `hooks/environment_guard.py`. |
| **Cross-Project Isolation** | Upgrading Package A breaks Package B. | Independent lockfiles; no cross-project bleed observed in controlled tests. | Validated in [Case Study](docs/case-studies/dependency-isolation.md). |
| **Architecture Design** | Sprawling monolithic single-file code. | Layered domain boundaries, dependency injection, typed schema validation. | Governed by `code-architecture` skill. |
| **Testing Discipline** | "I wrote the code, it should work." | Mandatory Pytest/Vitest suites executed and verified prior to completion. | Validated via `tests/` self-verification suite. |
| **Security & Secrets** | Real API keys committed in code or `.env`. | Zero-secret invariant, `.env.example` templates, automated regex scanning. | Validated via `tests/scan_secrets.py`. |
| **Documentation** | Stale, unverified, or decorative bloat. | Adaptive 5-tier documentation tied strictly to verified capabilities. | Validated via `tests/test_documentation.py`. |

---

## 🔬 Empirical Evidence: Controlled Dependency Isolation

Can two concurrent projects with conflicting major dependencies (e.g., **Pydantic v2.7.4** vs **Pydantic v1.10.13**) coexist in the same workspace without contaminating each other or modifying global Python?

```text
Project A (Pydantic 2.7.4) ───┐
                              ├── Isolated (.venv / uv.lock) ──► Host Environment Clean
Project B (Pydantic 1.10.13) ─┘
```

In our controlled experiment across Windows, macOS, and Linux:
* **Result**: **8/8 verification metrics passed**. Both projects resolved distinct lockfiles and executed in-environment tests concurrently with zero cross-project pollution observed under the tested conditions.
* Read the full scientific report: **[docs/case-studies/dependency-isolation.md](docs/case-studies/dependency-isolation.md)**.

---

## 📦 Starter Archetypes

AgenticOS includes 5 pre-configured, tested starter templates in [`templates/`](templates/):

1. **[`python-service`](templates/python-service/)**: FastAPI microservice starter with Pydantic v2 validation, health probes, and pytest suite.
2. **[`ai-ml`](templates/ai-ml/)**: Tabular ML pipeline template with Scikit-Learn baselines, leak-free preprocessing, and evaluation tests.
3. **[`rag-llm`](templates/rag-llm/)**: Retrieval-Augmented Generation template with FAISS vector indexing, chunking, and typed query contracts.
4. **[`fullstack`](templates/fullstack/)**: Complete fullstack application with React 19 SPA, Vite, FastAPI backend, and Docker Compose.
5. **[`production-service`](templates/production-service/)**: Enterprise microservice template with OpenTelemetry, structured JSON logging, correlation IDs, and multi-stage Dockerfile.

---

## 🔌 AI Agent & IDE Compatibility

AgenticOS is designed to work across major AI coding assistants and environments:

| Assistant / IDE | Integration Mode | Configuration Mechanism |
| :--- | :--- | :--- |
| **Google Antigravity (AGY)** | **Native** | Automatically discovers `.agents/skills/` catalog and `AGENTS.md` rules. |
| **Cursor IDE** | **Convention-based** | Add `.cursorrules` or symlink rules into `.cursor/rules/`. |
| **VS Code + GitHub Copilot** | **Convention-based** | Reference `AGENTS.md` instructions in `.github/copilot-instructions.md`. |
| **Claude Code (CLI)** | **Convention-based** | Reference or symlink `AGENTS.md` as `CLAUDE.md` in project root. |
| **OpenAI Codex / Custom Agents** | **Prompt / Context Injection** | Ingest `AGENTS.md` and relevant `SKILL.md` files into system prompt context. |

---

## 🚀 Quickstart

### Option 1: Integrate into an Existing Project
Copy the foundational invariants, modular skills, and deterministic hooks into your workspace:

```bash
# Windows PowerShell
Copy-Item -Recurse "path/to/agentic-engineering-os/.agents" "./"
Copy-Item -Recurse "path/to/agentic-engineering-os/hooks" "./"
Copy-Item "path/to/agentic-engineering-os/AGENTS.md" "./"

# Linux / macOS / WSL
cp -r path/to/agentic-engineering-os/.agents ./
cp -r path/to/agentic-engineering-os/hooks ./
cp path/to/agentic-engineering-os/AGENTS.md ./
```

### Option 2: Bootstrap from a Starter Archetype
Clone one of the 5 pre-configured production templates:

```bash
# Copy template (e.g., Python FastAPI Service)
cp -r agentic-engineering-os/templates/python-service my-new-api
cd my-new-api

# Initialize isolated environment with uv
uv venv .venv --python 3.12
uv sync
uv run pytest -v
```

---

## 🐕 Dogfooding & Repository Verification

AgenticOS is built and verified using its own engineering principles. Every pull request executes a self-verification test suite:

```bash
# Run repository self-verification suite
py ./tests/validate_skills.py       # Validates YAML frontmatter, triggers & 6 Core Questions for all 30 skills
py ./tests/scan_secrets.py          # Scans repository for secrets, credentials, and sensitive tokens
py ./tests/test_templates.py        # Compiles all template code and validates test suite completeness
py ./tests/test_hooks.py            # Tests environment guard engine against unisolated and isolated projects
py ./tests/test_documentation.py    # Asserts 100% resolution of relative documentation cross-references
```

---

## 🛣️ Roadmap

* **v1.0 (Foundation — Current)**: 30+ Modular Skills, Deterministic Hooks, MCP memory layer, 5 templates, multi-OS support, and self-verification suite.
* **v1.1 (Developer Experience — Planned)**: Standalone CLI (`agentic-os init`, `agentic-os doctor`), automated scaffolding, and pre-commit hook integration.
* **v1.2 (Evidence & Benchmarks — Planned)**: Automated `AgenticEval` benchmark harness, empirical quality scorecards, and comparative evaluation suites.
* **v2.0 (Ecosystem — Planned)**: Public skill registry, community plugins, multi-agent coordination protocols, and custom organization profiles.

See **[ROADMAP.md](ROADMAP.md)** for detailed milestone tracking.

---

## 🤝 Contributing & Community

We welcome contributions from the community! Please review:
* **[CONTRIBUTING.md](CONTRIBUTING.md)** for our 6 Core Questions skill authoring standard.
* **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** for our community standards.
* **[SECURITY.md](SECURITY.md)** for our vulnerability disclosure policy and Zero-Secret Invariant.

---

## 📄 License

AgenticOS is open-source software licensed under the **[MIT License](LICENSE)**.

---

<div align="center">

*AI agents are getting better at writing software. AgenticOS explores what happens when we give them an engineering system to work within.*

**Build with your agent. Engineer with AgenticOS.**

</div>
