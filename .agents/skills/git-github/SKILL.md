---
name: git-github
description: Git version control, conventional commit standards, feature branch workflows, pull request authoring, and secret avoidance.
---

# Git & GitHub Skill

## 1. When Should I Use This?

Use this skill when:
* Creating git branches, staging changes, authoring commits, or submitting Pull Requests.
* Checking repository status, diffs, and untracked files before and after modifications.
* Resolving merge conflicts or rebasing feature branches.
* Reviewing commit history and maintaining a clean Git log.

---

## 2. What Should I Inspect First?

1. **Current Working Tree**: Run `git status` to view staged, unstaged, and untracked files.
2. **Current Branch**: Run `git branch --show-current` to confirm you are on a feature branch, not directly modifying protected branches (`main`/`master`) unless intended.
3. **Diff Audit**: Run `git diff` (or `git diff --cached`) to inspect exact lines changed. Check for accidentally included secret keys, large dataset files, `.env`, or `.venv`.

---

## 3. What Workflow Should I Follow?

```text
Inspect git status & branch
           ↓
Create or Switch to Focused Feature Branch (feature/name or fix/issue)
           ↓
Make Minimal, Targeted Code Changes
           ↓
Run Tests & Linters to Ensure Quality
           ↓
Review Full git diff (Secret & Unintended Change Audit)
           ↓
Stage Specific Files (git add <file1> <file2>)
           ↓
Author Conventional Commit Message
           ↓
Push Branch & Open Pull Request / Review Diff
```

### Conventional Commit Standard

Format: `<type>(<scope>): <short imperative description>`

| Commit Type | Purpose | Example |
| :--- | :--- | :--- |
| `feat` | New feature or capability | `feat(auth): add JWT token refresh endpoint` |
| `fix` | Bug fix | `fix(ocr): handle empty PDF page bounding boxes` |
| `refactor` | Code change that neither fixes a bug nor adds a feature | `refactor(db): extract repository layer from services` |
| `test` | Adding or updating tests | `test(api): add integration tests for document upload` |
| `docs` | Documentation updates | `docs(readme): update deployment instructions for Render` |
| `ci` | CI/CD pipeline modifications | `ci(github): add Ruff and Pytest workflow` |
| `build` | Build tool, Docker, or dependency changes | `build(deps): upgrade fastapi to 0.110.0` |
| `chore` | Routine maintenance tasks | `chore(gitignore): ignore local test database files` |

### Concrete Branch & PR Workflow

```bash
# 1. Create a focused branch
git checkout -b feat/ocr-bounding-boxes

# 2. Stage specific files (never blind `git add .` without checking status)
git add app/services/ocr_service.py tests/unit/test_ocr.py

# 3. Commit with conventional format
git commit -m "feat(ocr): preserve word-level bounding boxes in PaddleOCR output"

# 4. Push to remote
git push -u origin feat/ocr-bounding-boxes
```

---

## 4. What Decisions Should I Make?

| Git Scenario | Recommended Action |
| :--- | :--- |
| **Commit Granularity** | Make small, atomic commits that represent a single logical change. Do not bundle a database migration, frontend UI change, and unrelated bug fix into one commit. |
| **Untracked Artifacts** | Add them to `.gitignore` before committing. If an artifact was accidentally tracked, use `git rm --cached <file>`. |
| **Branch Naming** | Use prefix conventions: `feat/<name>`, `fix/<name>`, `refactor/<name>`, `chore/<name>`. |

---

## 5. What Should I Avoid?

* **NEVER blind commit with `git add -A` or `git add .`**: Always inspect untracked files with `git status` first.
* **NEVER commit credentials, `.env`, or API tokens**: If committed, credentials must be considered compromised and rotated immediately.
* **NEVER force-push (`git push --force`) to shared branches**: Use `--force-with-lease` only on private feature branches when strictly necessary.
* **NEVER author vague commit messages**: Avoid commits like `update`, `fix bug`, `changes`, or `wip`.

---

## 6. How Should I Verify Success?

```bash
# 1. Inspect recent commit in log
git log -n 1 --stat

# 2. Verify working tree is clean
git status

# 3. Verify no secrets or unintended files are in the commit
git show HEAD --stat
```
