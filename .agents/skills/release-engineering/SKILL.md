---
name: release-engineering
description: Semantic versioning (SemVer), release lifecycle gates, automated changelog generation, rollback runbooks, and verified production deployments.
---

# Release Engineering Skill

## 1. When Should I Use This?

Use this skill when:
* Cutting a new release or version tag (`v1.0.0`, `v1.1.0`, `v1.0.1`) for a library, microservice, or web application.
* Updating `CHANGELOG.md` following the **Keep a Changelog** standard.
* Executing the pre-flight release gate (Tests → Lint → Security → Build → Versioning).
* Planning or executing a production rollback following a failed deployment.

Never cut a release without passing 100% of automated tests, security scans, and clean build checks.

---

## 2. What Should I Inspect First?

1. **Current Version**: Check `pyproject.toml`, `package.json`, or Git tags (`git describe --tags --abbrev=0`).
2. **Unreleased Changes**: Inspect `git log <last-tag>..HEAD` to classify changes as Major (breaking), Minor (new feature), or Patch (bug fix).
3. **CI Pipeline Status**: Verify that the latest commit on `main` passed all automated CI workflows.

---

## 3. What Workflow Should I Follow?

```text
1. CHANGE: All features & fixes merged into main
      ↓
2. TEST & LINT: Run full test suite & linters (pytest, ruff, npm test)
      ↓
3. SECURITY: Run vulnerability & secret scans (pip-audit, gitleaks)
      ↓
4. BUILD: Produce & validate build artifacts (Docker image, dist/ wheels)
      ↓
5. VERSION: Bump SemVer in pyproject.toml / package.json
      ↓
6. CHANGELOG: Document Added, Changed, Deprecated, Removed, Fixed
      ↓
7. RELEASE: Create signed Git tag (git tag -a vX.Y.Z -m "Release vX.Y.Z")
      ↓
8. DEPLOY: Trigger deployment to staging/production
      ↓
9. SMOKE TEST: Probe live health endpoints and critical user journeys
      ↓
10. OBSERVE: Monitor error logs and metrics for 15 minutes post-deploy
      ↓
(ROLLBACK if health checks fail or error rates spike > 1%)
```

### Semantic Versioning (SemVer) Rules

```text
Given version MAJOR.MINOR.PATCH (e.g. 1.2.3):

1. MAJOR (e.g. 2.0.0): Incompatible API changes, breaking database migrations.
2. MINOR (e.g. 1.3.0): Backward-compatible new functionality or endpoints.
3. PATCH (e.g. 1.2.4): Backward-compatible bug fixes or security patches.
```

### Standard Changelog Entry (`CHANGELOG.md`)

```markdown
## [1.1.0] - 2026-08-14

### Added
- Multi-modal OCR bounding box preservation in `OCRService`.
- FAISS vector store local persistence with automated reload on startup.

### Changed
- Migrated default package management toolchain to `uv`.

### Fixed
- Resolved duplicate timestamp aggregation during Daylight Saving Time fallback.

### Security
- Upgraded `cryptography` dependency to resolve CVE-2026-XXXX.
```

### Production Rollback Procedure

```bash
# 1. Identify previous stable release tag
git tag -l "v*" --sort=-v:refname | head -n 5

# 2. Revert deployment trigger
git checkout v1.0.0

# 3. Redeploy previous container image or redeploy commit on Render/Vercel
# 4. Run post-rollback health verification
curl -i https://app-backend.onrender.com/api/v1/health
```

---

## 4. What Decisions Should I Make?

| Release Decision | Standard Heuristic |
| :--- | :--- |
| **Release Tag Format** | Use prefixed semantic versioning (e.g. `v1.2.0`). |
| **Breaking Database Migrations** | Implement two-phase migrations (Expand-Contract pattern) so old code can run alongside new schema before dropping columns. |
| **Release Gate Failure** | If any single test, lint check, or security scan fails, ABORT the release immediately. |

---

## 5. What Should I Avoid?

* **NEVER tag a release on a dirty working tree**: Ensure `git status` is clean.
* **NEVER manually edit git tags after pushing**: If a release contains a bug, release a subsequent patch version (`v1.0.1`), never overwrite `v1.0.0`.
* **NEVER declare deployment success without executing post-deployment smoke tests**.

---

## 6. How Should I Verify Success?

```bash
# 1. Verify version numbers match across all manifests
python -c "
import tomllib
pyproj = tomllib.load(open('pyproject.toml', 'rb'))['project']['version']
print(f'pyproject.toml version: {pyproj}')
"

# 2. Verify git tag creation
git describe --tags --exact-match

# 3. Verify live endpoint response post-deployment (Cross-Platform)
python -c "import urllib.request, json; res = urllib.request.urlopen('https://app-backend.onrender.com/api/v1/health'); data = json.load(res); assert data.get('status') == 'ok', f'Unexpected status: {data}'; print('Post-release health probe: OK')"
```
