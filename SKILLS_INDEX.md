# AgenticOS Skills Master Catalog

This catalog outlines the **30+ modular engineering skills** included in AgenticOS across fullstack development, AI/ML, security, testing, architecture, DevOps, and delivery.

---

## 🧭 Skills Matrix

| # | Skill Name | Category | Primary Activation Trigger | MCP Interaction | Hook Interaction |
| :- | :--- | :--- | :--- | :--- | :--- |
| 1 | [`environment-guardrails`](.agents/skills/environment-guardrails/SKILL.md) | Environment | Virtualenv creation, Python version pinning, package isolation | Queries environment rules | Triggers `environment-guard.sh` / `.ps1` |
| 2 | [`python-environment`](.agents/skills/python-environment/SKILL.md) | Environment | Setting up uv / venv / conda environments | Reads runtime constraints | Triggers environment guard |
| 3 | [`dependency-management`](.agents/skills/dependency-management/SKILL.md) | Environment | Adding, upgrading, or resolving package conflicts | Records dependency decisions | Triggers lockfile checks |
| 4 | [`project-knowledge`](.agents/skills/project-knowledge/SKILL.md) | Knowledge | Reading/writing persistent codebase memory | Direct read/write to Memory MCP | None |
| 5 | [`adr-management`](.agents/skills/adr-management/SKILL.md) | Architecture | Documenting Architecture Decision Records in `docs/decisions/` | Writes decisions to Memory MCP | None |
| 6 | [`documentation-orchestrator`](.agents/skills/documentation-orchestrator/SKILL.md) | Documentation | Planning & generating adaptive project documentation | Reads architecture entities | Validates broken links |
| 7 | [`observability`](.agents/skills/observability/SKILL.md) | Operations | OpenTelemetry, JSON logging, metrics, AI/LLM telemetry | Records telemetry endpoints | None |
| 8 | [`supply-chain-security`](.agents/skills/supply-chain-security/SKILL.md) | Security | SBOM generation, vulnerability scanning (`pip-audit`, `trivy`) | Records security constraints | Triggers pre-commit scans |
| 9 | [`release-engineering`](.agents/skills/release-engineering/SKILL.md) | Operations | SemVer version bump, changelog generation, rollback runbooks | Records release tags | Triggers CI release gates |
| 10 | [`portfolio-readiness`](.agents/skills/portfolio-readiness/SKILL.md) | Showcase | Auditing 6 engineering pillars & 10 presentation dimensions | Reads project highlights | Validates link URLs |
| 11 | [`project-bootstrap`](.agents/skills/project-bootstrap/SKILL.md) | Core / Scaffolding | 17-step adaptive lifecycle orchestrator for new repos | Queries MCP memory | Initializes hooks & env |
| 12 | [`code-architecture`](.agents/skills/code-architecture/SKILL.md) | Architecture | Layered service design, dependency injection boundaries | Reads architecture graph | None |
| 13 | [`reusable-components`](.agents/skills/reusable-components/SKILL.md) | Architecture | Extracting DRY utilities, shared services, custom hooks | Records utility locations | None |
| 14 | [`testing-quality`](.agents/skills/testing-quality/SKILL.md) | Quality | Pytest/Vitest pyramid, test fixtures, coverage gates | None | Pre-commit test runs |
| 15 | [`debugging`](.agents/skills/debugging/SKILL.md) | Quality | 7-step root cause analysis, error trace isolation | Writes root causes to Memory MCP | None |
| 16 | [`git-github`](.agents/skills/git-github/SKILL.md) | DevOps | Conventional commits, feature branches, PR authoring | None | Pre-commit hook triggers |
| 17 | [`ci-cd`](.agents/skills/ci-cd/SKILL.md) | DevOps | GitHub Actions automation, test gates, release pipelines | None | Executes CI workflows |
| 18 | [`docker`](.agents/skills/docker/SKILL.md) | DevOps | Multi-stage Dockerfiles, compose orchestration, healthchecks | Records port constraints | None |
| 19 | [`deployment`](.agents/skills/deployment/SKILL.md) | DevOps | Cloud deployments to Render, Vercel, Streamlit Cloud | Records deployment URLs | Post-deploy smoke tests |
| 20 | [`security-secrets`](.agents/skills/security-secrets/SKILL.md) | Security | Secret protection, Pydantic SecretStr, CORS, OWASP | Zero-secret memory gate | Secret scan hook |
| 21 | [`python-api`](.agents/skills/python-api/SKILL.md) | Fullstack | FastAPI endpoints, Pydantic v2 validation, health probes | Records API contracts | None |
| 22 | [`frontend-react-typescript`](.agents/skills/frontend-react-typescript/SKILL.md) | Fullstack | React 19 SPA, Tailwind CSS, TanStack Query, Radix UI | None | Type-check validation |
| 23 | [`database-postgresql`](.agents/skills/database-postgresql/SKILL.md) | Fullstack | PostgreSQL schema design, Prisma ORM, SQLAlchemy/Alembic | Queries DB MCP tools | Migration integrity checks |
| 24 | [`machine-learning`](.agents/skills/machine-learning/SKILL.md) | AI / ML | Scikit-Learn, XGBoost, leak-free splits, baselines | Records model baselines | None |
| 25 | [`deep-learning`](.agents/skills/deep-learning/SKILL.md) | AI / ML | PyTorch/TensorFlow, transfer learning, GPU memory | Records training hyperparameters | None |
| 26 | [`data-engineering`](.agents/skills/data-engineering/SKILL.md) | Data | Time-series, DST handling, rolling stats, data pipelines | Records dataset schemas | None |
| 27 | [`rag-ocr-llm`](.agents/skills/rag-ocr-llm/SKILL.md) | AI / LLM | PaddleOCR, PyMuPDF, FAISS vector indexing, Ollama/OpenAI | Records chunking decisions | None |
| 28 | [`performance-optimization`](.agents/skills/performance-optimization/SKILL.md) | Performance | Profiling with `cProfile`, query optimization, benchmarks | Records latency baselines | None |
| 29 | [`documentation`](.agents/skills/documentation/SKILL.md) | Documentation | Synchronizing README, ARCHITECTURE.md, ADRs, logs | Synchronizes with memory | Link check script |
| 30 | [`agentic-development`](.agents/skills/agentic-development/SKILL.md) | Meta-Skill | 8-phase AI coding agent execution lifecycle | Master memory coordinator | Invokes hooks at gates |
