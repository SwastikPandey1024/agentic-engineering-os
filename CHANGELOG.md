# Changelog

All notable changes to **AgenticOS** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-08-15

### Added
- Standard-library `agentic-os` developer CLI.
- `agentic-os doctor` environment and project health diagnostics.
- Conflict-safe `agentic-os init` workspace bootstrap.
- `agentic-os new` starter archetype generator.
- Five verified production starter archetypes.
- `agentic-os ide` multi-agent integration layer.
- Native Antigravity integration and optional AgenticOS rule adapter.
- Cursor `.cursorrules` integration.
- GitHub Copilot `.github/copilot-instructions.md` integration.
- Claude Code `CLAUDE.md` integration.
- Cross-platform CI quality gate and GitHub Actions verification.

### Improved
- Developer onboarding through the installable CLI.
- Conflict safety and idempotent project operations.
- Cross-platform developer experience across Windows, macOS, and Linux.
- Package distribution through the modern Python packaging configuration.
- CI verification of package installation and CLI behavior.

### Verification
- 20/20 post-merge local verification checks passed.
- 30+ modular skills validated.
- Five starter templates validated.
- Environment guard regression suite passed.
- Documentation reference validation passed.
- Secret scanning passed with zero detected secrets.
- Package installation and CLI entrypoint verified.

---

## [1.0.0] - 2026-08-14

### Initial Public Release

#### 🧠 Knowledge Layer
* **30+ Modular Engineering Skills** in `.agents/skills/` covering Architecture, Environment, Quality, DevOps, Fullstack, AI/ML, and Operations.
* **Universal Invariants (`AGENTS.md`)**: Always-on foundational rules for environment isolation, security, and truth in documentation.

#### 🛡️ Enforcement Layer
* **Canonical Python Environment Guard (`hooks/environment_guard.py`)**: Universal standard-library Python engine enforcing virtual environments, lockfiles, and interpreter isolation.
* **Thin Cross-Platform Wrappers**: `hooks/environment-guard.ps1` (PowerShell) and `hooks/environment-guard.sh` (Bash).

#### 🧩 Context & Memory Integration Layer
* **MCP Integration Guide & Schemas (`mcp/`)**: Connects active project-memory MCP tools (such as `codebase-memory-mcp`) and defines the 7-entity graph schema.

#### 📦 Starter Archetypes
* **5 Production Templates (`templates/`)**: `python-service`, `ai-ml`, `rag-llm`, `fullstack`, and `production-service`.

#### 🧪 Self-Verification & Case Studies
* **Self-Verification Suite (`tests/`)**: Automated tests for skills, templates, hooks, documentation links, and secrets.
* **Empirical Case Study (`docs/case-studies/dependency-isolation.md`)**: Scientific validation of cross-project dependency isolation under major package version collisions.
