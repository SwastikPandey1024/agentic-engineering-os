---
name: portfolio-readiness
description: Comprehensive project readiness audit across 6 engineering pillars and 10 presentation dimensions for portfolio, resume, LinkedIn, and technical interviews.
---

# Portfolio Readiness Skill

## 1. When Should I Use This?

Use this skill when:
* Polishing and auditing a completed project for inclusion in your professional engineering portfolio.
* Generating resume bullet points, LinkedIn project summaries, or technical interview talking points.
* Validating that an open-source repository meets enterprise visual and engineering showcase standards.
* Auditing an existing project against the **6 Engineering Pillars** and **10 Presentation Dimensions**.

Never fabricate metrics, benchmarks, or user statistics.

---

## 2. What Should I Inspect First?

1. **Working State & Live Demos**: Is there a live working URL (Vercel, Render, Streamlit Cloud)?
2. **Visual Assets**: Are there high-resolution screenshots, architecture diagrams, or demo recordings in `docs/assets/` or `images/`?
3. **Repository Cleanliness**: Ensure zero untracked scratch files, no leaked API keys, and clean `main` branch Git history.

---

## 3. What Workflow Should I Follow?

```text
Audit 6 Engineering Pillars (Tests, Architecture, Security, Deploy, Observe, Docs)
                        ↓
Audit 10 Presentation Dimensions (Hero, Diagram, Screenshots, Demos, Metrics)
                        ↓
Generate Concise Resume Bullet Points (Action Verb + Tech + Quantified Result)
                        ↓
Generate LinkedIn Project Narrative & Technical Highlights
                        ↓
Prepare 2-Minute Interview Elevator Pitch & Deep-Dive Talking Points
                        ↓
Verify Zero Fabricated Claims & Verify All External Links
```

### The 6 Engineering Pillars Audit

```text
┌───────────────────────────┬───────────────────────────────────────────────────────────┐
│ Engineering Pillar        │ Minimum Readiness Criteria                                │
├───────────────────────────┼───────────────────────────────────────────────────────────┤
│ 1. Tests & Quality        │ • Automated test suite (Pytest/Vitest) with >= 80% pass   │
│                           │ • Static typing (mypy/tsc) and linting (Ruff/ESLint) clean │
├───────────────────────────┼───────────────────────────────────────────────────────────┤
│ 2. Code Architecture      │ • Layered separation (API, Service, Repository, Models)   │
│                           │ • Clean dependency injection without god-files            │
├───────────────────────────┼───────────────────────────────────────────────────────────┤
│ 3. Security & Hygiene     │ • Clean secret scan (zero leaked credentials)             │
│                           │ • Pydantic SecretStr & sanitized .env.example             │
├───────────────────────────┼───────────────────────────────────────────────────────────┤
│ 4. Deployment & DevOps    │ • Multi-stage Dockerfile or Live Cloud URL (Render/Vercel)│
│                           │ • Passing CI pipeline (.github/workflows/ci.yml)          │
├───────────────────────────┼───────────────────────────────────────────────────────────┤
│ 5. Observability          │ • Structured JSON logging with Request IDs                │
│                           │ • Health check probe (/health) returning 200 OK           │
├───────────────────────────┼───────────────────────────────────────────────────────────┤
│ 6. Documentation          │ • Synchronized README, ARCHITECTURE.md, and ADRs          │
└───────────────────────────┴───────────────────────────────────────────────────────────┘
```

### The 10 Presentation Dimensions Checklist

1. [ ] **README Hero Section**: Clear title, 1-sentence value proposition, status badges, tech stack badges.
2. [ ] **Architecture Diagram**: High-resolution ASCII or Mermaid diagram showing data flow.
3. [ ] **Visual Screenshots**: Clean, captioned UI screenshots demonstrating core user workflows.
4. [ ] **Live Demo Link**: Working public URL (Streamlit / Vercel / Render).
5. [ ] **Demo Video / GIF**: 30-90 second walkthrough video or animated GIF.
6. [ ] **Quantified Performance Metrics**: Real measured metrics (e.g. "sub-50ms OCR retrieval", "0.0% patient leakage").
7. [ ] **Key Technical Highlights**: Bulleted list of the 3 most complex engineering problems solved.
8. [ ] **Resume Bullets**: 2-3 impact-driven bullets in Google XYZ format (`Accomplished [X] as measured by [Y] by doing [Z]`).
9. [ ] **LinkedIn Project Post**: Engaging announcement with architecture image and key takeaways.
10. [ ] **Technical Interview Explanation**: 2-minute elevator pitch + trade-off defense.

---

### Resume Bullet & Interview Artifact Generator

```markdown
### 📄 Resume Bullets (Google XYZ Format)
* Architected a distributed RAG & OCR document analysis system using **FastAPI**, **PaddleOCR**, and **FAISS**, enabling sub-50ms semantic search over complex PDFs with zero external cloud API costs.
* Designed an end-to-end time-series energy demand forecasting platform with **XGBoost** and **Streamlit**, resolving Daylight Saving Time timestamp anomalies and beating 24h persistence baselines by 38% MAE.
* Implemented a patient-stratified deep learning pipeline in **TensorFlow 2.16** fine-tuning **DenseNet121** with protected BatchNorm layers, achieving 94.2% ROC-AUC on RSNA chest X-rays with 0% patient leakage.

---

### 🎙️ 2-Minute Technical Interview Pitch
"In this project, I set out to solve [Problem X]. Rather than relying on fragile single-script workflows, I designed a production-grade layered architecture separating [API layer, business services, and storage]. 

One of the most interesting technical challenges was [Challenge Y, e.g. handling Daylight Saving Time duplicate timestamps / multi-modal OCR bounding boxes]. I evaluated alternatives [Option A vs Option B] in an ADR, ultimately choosing [Option B] because [Rationale Z]. 

I verified the solution with [N tests], deployed it via [Docker/Render/Vercel], and added structured observability with correlation IDs."
```

---

## 4. What Decisions Should I Make?

| Showcase Audience | Priority Focus |
| :--- | :--- |
| **Recruiters / Hiring Managers** | Live URL, clean UI screenshots, quantified resume bullets, concise 1-sentence summary. |
| **Senior Engineers / Staff Architects** | Layered code architecture, ADR trade-offs, testing pyramid, Docker builds, OpenTelemetry. |

---

## 5. What Should I Avoid?

* **NEVER invent fake benchmark numbers**: If you did not benchmark latency, run a benchmark before quoting a number.
* **NEVER use low-resolution blurry screenshots**: Capture crisp, high-DPI screenshots with clean mock data.
* **NEVER leave broken live demo links**: Ensure cloud free tiers have not expired or spun down into permanent error states.

---

## 6. How Should I Verify Success?

```bash
# 1. Audit all links in README.md
python -c "
import urllib.request, re
readme = open('README.md', encoding='utf-8').read()
urls = re.findall(r'https?://[^\s\)\"]+', readme)
print(f'Auditing {len(urls)} external links...')
for u in set(urls):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        code = urllib.request.urlopen(req, timeout=5).getcode()
        print(f'[OK {code}] {u}')
    except Exception as e:
        print(f'[FAILED] {u}: {e}')
"
```
