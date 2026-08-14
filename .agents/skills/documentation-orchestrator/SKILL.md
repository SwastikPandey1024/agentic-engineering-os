---
name: documentation-orchestrator
description: Adaptive project documentation suite generation, classification-based document planning (Utility vs ML vs Fullstack vs Hackathon vs Production), and truth verification.
---

# Documentation Orchestrator Skill

## 1. When Should I Use This?

Use this skill when:
* Determining the appropriate documentation suite and structure for a new or existing repository.
* Generating complete, synchronized project documentation across business, product, engineering, and operational layers.
* Auditing documentation to eliminate false claims, aspirational text, or unverified features.

Never generate enterprise-scale documentation for trivial 20-line scripts. Never skip critical architecture and runbook documentation for production applications.

---

## 2. What Should I Inspect First?

1. **Project Archetype & Scale**:
   * Small CLI / Utility?
   * ML / AI Research or Portfolio project?
   * Full-stack Web Application?
   * Fast-paced Hackathon prototype?
   * Enterprise Production Service?
2. **Current Verified Capabilities**: Inspect real endpoints, database tables, models, and test suites to ensure documentation matches code reality 100%.

---

## 3. What Workflow Should I Follow?

```text
Classify Project Archetype & Target Audience
                     ↓
Select the Required Minimum Documentation Suite
                     ↓
Audit Code Reality (Verify real functions, routes, configs)
                     ↓
Generate Core Documents Sequentially (High-level → Low-level)
                     ↓
Cross-Link Related Documents & Add Architecture Diagrams
                     ↓
Verify Accuracy: Ensure ZERO unverified or unbuilt features are claimed
```

### The 5 Project Classifications & Minimum Document Suites

```text
┌──────────────────────────────────┬───────────────────────────────────────────────────────────┐
│ Project Classification           │ Required Minimum Documentation Suite                      │
├──────────────────┼───────────────────────────────────────────────────────────┤
│ 1. Small CLI / Script Utility    │ • README.md (Overview, Prerequisites, Setup, Usage)       │
│                                  │ • LICENSE                                                 │
├──────────────────────────────────┼───────────────────────────────────────────────────────────┤
│ 2. ML / AI Portfolio Project     │ • README.md (Hero, Problem, Results, Live Demo)           │
│                                  │ • ARCHITECTURE.md (Data Pipeline, Model Architecture)     │
│                                  │ • EVALUATION_REPORT.md (Metrics, Confusion Matrix, Baselines)│
│                                  │ • MODEL_CARD.md (Intended use, Limitations, Biases)      │
├──────────────────────────────────┼───────────────────────────────────────────────────────────┤
│ 3. Full-Stack Web Application    │ • README.md (Overview, Tech Stack, Local Dev Setup)       │
│                                  │ • PRD.md (Product Requirements & User Stories)            │
│                                  │ • ARCHITECTURE.md (Frontend/Backend/DB Boundaries, Auth)  │
│                                  │ • API.md (Endpoints, Schemas, Status Codes, OpenAPI)      │
│                                  │ • DEPLOYMENT.md (Render/Vercel/Docker Setup, Env Vars)    │
│                                  │ • SECURITY.md (Auth, CORS, Secret Management)             │
├──────────────────────────────────┼───────────────────────────────────────────────────────────┤
│ 4. Hackathon Prototype           │ • README.md (1-Line Hook, Problem, Solution, Demo Video)  │
│                                  │ • PROBLEM_STATEMENT.md & PITCH.md (Judging criteria fit)  │
│                                  │ • ARCHITECTURE.md (High-speed prototype flow)             │
│                                  │ • QUICKSTART.md (1-minute local reproduction guide)       │
├──────────────────────────────────┼───────────────────────────────────────────────────────────┤
│ 5. Enterprise Production Service │ • BRD.md (Business Requirements Document)                 │
│                                  │ • PRD.md (Product Requirements Document)                  │
│                                  │ • SRS.md (Software Requirements Specification)            │
│                                  │ • ARCHITECTURE.md (System design & data flow)             │
│                                  │ • docs/decisions/ (Architecture Decision Records - ADRs)  │
│                                  │ • API.md & OPENAPI schema                                 │
│                                  │ • RUNBOOK.md / DEPLOYMENT.md (Operations, Rollback, CI/CD)│
│                                  │ • SECURITY.md & Threat Model                              │
│                                  │ • OBSERVABILITY.md (Metrics, Traces, SLA/SLO Alerts)      │
└──────────────────────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 4. What Decisions Should I Make?

| Documentation Decision | Guiding Principle |
| :--- | :--- |
| **Depth vs Overhead** | Right-size documentation to project longevity. A 2-day hackathon needs high-impact visual presentation; a production service needs rigorous operational runbooks and ADRs. |
| **Truthfulness Gate** | If a feature is planned for next week, label it in `ROADMAP.md`, NEVER in `README.md` or `API.md` as active. |
| **Visual Architecture** | Every architecture doc for a non-trivial project must include at least one ASCII or Mermaid sequence/system diagram. |

---

## 5. What Should I Avoid?

* **NEVER generate generic filler docs**: Avoid creating empty or boilerplate files with `TODO: write this section`.
* **NEVER fabricate benchmarks or test metrics**: Use actual recorded values from evaluation runs.
* **NEVER leave broken copy-paste commands**: Test every installation and run command locally.

---

## 6. How Should I Verify Success?

```bash
# 1. Verify all generated documentation files exist and are populated
ls -la docs/ || ls -la README.md ARCHITECTURE.md

# 2. Check for unbroken relative markdown links
python -c "
import os, re
for root, _, files in os.walk('.'):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            text = open(path, encoding='utf-8').read()
            links = re.findall(r'\[.*?\]\((?!http|mailto)(.*?)\)', text)
            for link in links:
                target = os.path.join(root, link.split('#')[0])
                if not os.path.exists(target) and link.split('#')[0] != '':
                    print(f'Broken link in {path}: {link}')
print('Documentation link validation complete.')
"
```
