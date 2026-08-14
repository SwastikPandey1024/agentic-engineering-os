---
name: ci-cd
description: Continuous Integration & Continuous Deployment pipeline authoring, GitHub Actions automation, automated testing gates, and release workflows.
---

# CI/CD Skill

## 1. When Should I Use This?

Use this skill when:
* Creating or updating GitHub Actions workflows (`.github/workflows/ci.yml`).
* Setting up automated formatting, linting, type-checking, and test validation gates on Pull Requests and pushes to `main`.
* Configuring automated container builds, artifact releases, or cloud deployments.

Do NOT add bloated or slow CI steps for tools not actively configured in the project.

---

## 2. What Should I Inspect First?

1. **Existing Workflows**: Inspect `.github/workflows/` for existing jobs and secrets.
2. **Project Tooling**: Inspect `pyproject.toml`, `package.json`, or `Makefile` to see exact local test and lint commands (`ruff`, `pytest`, `npm test`, `tsc`).
3. **Repository Secrets**: Identify required environment secrets (e.g. `DOCKERHUB_TOKEN`, `RENDER_API_KEY`, `VERCEL_TOKEN`).

---

## 3. What Workflow Should I Follow?

```text
Format & Lint (Ruff, ESLint)
              ↓
Type Checking (Mypy, TypeScript tsc)
              ↓
Unit & Integration Tests (Pytest, Vitest)
              ↓
Security Audit / Secret Scan
              ↓
Container Build / Artifact Packaging
              ↓
Automated Deployment (Main branch only)
```

### Production GitHub Actions Workflow Template (`ci.yml`)

```yaml
# .github/workflows/ci.yml
name: Continuous Integration

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend-lint-and-test:
    name: Backend CI
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Lint and Format Check (Ruff)
        run: |
          ruff check .
          ruff format --check .

      - name: Run Pytest Suite
        run: |
          pytest -v --tb=short --cov=app --cov-report=xml

  frontend-lint-and-test:
    name: Frontend CI
    runs-on: ubuntu-latest
    if: hashFiles('frontend/**') != ''
    defaults:
      run:
        working-directory: frontend
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json

      - name: Install Dependencies
        run: npm ci

      - name: TypeScript Type Check
        run: npm run type-check

      - name: Lint Check
        run: npm run lint

      - name: Run Unit Tests
        run: npm test -- --run
```

---

## 4. What Decisions Should I Make?

| Pipeline Requirement | Implementation Decision |
| :--- | :--- |
| **Dependency Caching** | Use native actions caching (`cache: 'pip'` or `actions/cache`) to keep CI runs under 2 minutes. |
| **Job Parallelization** | Run backend and frontend CI jobs concurrently in separate runner instances. |
| **Branch Protection** | Require all CI checks to pass before pull requests can be merged into `main`. |
| **Deployment Gate** | Restrict deployment jobs strictly to `github.ref == 'refs/heads/main'` with explicit environment protection rules. |

---

## 5. What Should I Avoid?

* **NEVER run slow end-to-end browser tests on every single commit**: Separate heavy integration or E2E tests into nightly or scheduled triggers.
* **NEVER hardcode secrets in YAML**: Always reference `${{ secrets.MY_SECRET }}`.
* **NEVER use `npm install` in CI**: Always use `npm ci` for deterministic, clean package installation based strictly on `package-lock.json`.
* **NEVER allow CI to fail silently**: Ensure non-zero exit codes fail the job.

---

## 6. How Should I Verify Success?

```bash
# 1. Validate YAML syntax locally
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"

# 2. Replicate CI commands locally before pushing
ruff check .
pytest -v
npm run type-check # (if frontend exists)
```
