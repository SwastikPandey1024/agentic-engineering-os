# Cross-Platform Command Matrix

This reference matrix provides equivalent command invocations across **Windows PowerShell**, **macOS/Linux (Bash/Zsh)**, and **Universal Python** scripts.

---

## 🛠️ 1. AgenticOS Developer CLI (Cross-Platform)

| Task | Command Syntax (All Platforms) | Behavior & Safety Invariants |
| :--- | :--- | :--- |
| **Workspace Health Check** | `agentic-os doctor` | Inspects `.venv`, lockfiles, toolchain, Git status, and rules. |
| **Strict Health Check** | `agentic-os doctor --strict` | Halts with non-zero code on warnings as well as critical errors. |
| **Bootstrap Workspace** | `agentic-os init` | Copies `.agents/skills/`, `hooks/`, and `AGENTS.md` with SHA-256 conflict safety. |
| **Preview Bootstrap** | `agentic-os init --dry-run` | Previews files without writing to disk. |
| **Force Overwrite Bootstrap** | `agentic-os init --force` | Overwrites conflicting files safely. |
| **List Starter Archetypes** | `agentic-os new --list-templates` | Displays all 5 production archetypes and descriptions. |
| **Scaffold Project** | `agentic-os new <name> -t <template>` | Scaffolds a project from canonical archetype without code duplication. |
| **List IDE Targets** | `agentic-os ide list` | Lists all supported AI coding assistant integration adapters. |
| **Configure IDE Adapter** | `agentic-os ide configure --target <target>` | Configures `antigravity`, `cursor`, `copilot`, `claude`, or `all`. |
| **Diagnose IDE Adapters** | `agentic-os ide doctor` | Inspects configured IDE adapters in current workspace. |

---

## 🐍 2. Python Environment & Execution

| Task | Windows PowerShell | macOS / Linux (Bash/Zsh) | Universal Python / `uv` (Cross-Platform) |
| :--- | :--- | :--- | :--- |
| **Create Virtualenv** | `uv venv .venv --python 3.12`<br>*or* `python -m venv .venv` | `uv venv .venv --python 3.12`<br>*or* `python3 -m venv .venv` | `uv venv .venv --python 3.12` *(Preferred)* |
| **Activate Virtualenv** | `.\.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` | *Not needed with `uv run`* |
| **Sync Dependencies** | `uv sync` | `uv sync` | `uv sync` *(Identical across all OS)* |
| **Add Dependency** | `uv add "fastapi>=0.110.0"` | `uv add "fastapi>=0.110.0"` | `uv add "fastapi>=0.110.0"` |
| **Add Dev Dependency** | `uv add --dev pytest` | `uv add --dev pytest` | `uv add --dev pytest` |
| **Execute Script in Env** | `uv run python script.py` | `uv run python script.py` | `uv run python script.py` *(No manual activate)* |
| **Run Pytest** | `uv run pytest -v` | `uv run pytest -v` | `uv run pytest -v` |
| **Run Linter / Formatter**| `uv run ruff check .` | `uv run ruff check .` | `uv run ruff check .` |
| **Find Active Python** | `Get-Command python | Select-Object -ExpandProperty Source` | `which python` | `python -c "import sys; print(sys.executable)"` |

---

## 📦 3. Node.js Package Managers

| Task | `npm` | `pnpm` | `yarn` | `bun` | Lockfile |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Deterministic Install** | `npm ci` | `pnpm install --frozen-lockfile` | `yarn install --frozen-lockfile` | `bun install --frozen-lockfile` | `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` / `bun.lock` |
| **Add Dependency** | `npm install <pkg>` | `pnpm add <pkg>` | `yarn add <pkg>` | `bun add <pkg>` | |
| **Add Dev Dependency** | `npm install -D <pkg>`| `pnpm add -D <pkg>` | `yarn add -D <pkg>` | `bun add -d <pkg>` | |
| **Run Script** | `npm run build` | `pnpm run build` | `yarn build` | `bun run build` | |
| **Run Dev Server** | `npm run dev` | `pnpm dev` | `yarn dev` | `bun dev` | |

---

## 📁 4. File System & Directory Operations

| Operation | Windows PowerShell | macOS / Linux (Bash/Zsh) | Cross-Platform Python (`pathlib` / `shutil`) |
| :--- | :--- | :--- | :--- |
| **Create Directory** | `New-Item -ItemType Directory -Force -Path "path/to/dir"` | `mkdir -p path/to/dir` | `python -c "import pathlib; pathlib.Path('path/to/dir').mkdir(parents=True, exist_ok=True)"` |
| **Copy File** | `Copy-Item "src.txt" "dest.txt"` | `cp src.txt dest.txt` | `python -c "import shutil; shutil.copy('src.txt', 'dest.txt')"` |
| **Copy Directory** | `Copy-Item -Recurse -Force "src_dir" "dest_dir"` | `cp -r src_dir dest_dir` | `python -c "import shutil; shutil.copytree('src_dir', 'dest_dir', dirs_exist_ok=True)"` |
| **Delete File** | `Remove-Item "file.txt" -Force` | `rm -f file.txt` | `python -c "import pathlib; pathlib.Path('file.txt').unlink(missing_ok=True)"` |
| **Delete Directory** | `Remove-Item -Recurse -Force "dir"` | `rm -rf dir` | `python -c "import shutil; shutil.rmtree('dir', ignore_errors=True)"` |
| **Check File Exists** | `Test-Path "file.txt"` | `[ -f "file.txt" ]` | `python -c "import pathlib; print(pathlib.Path('file.txt').is_file())"` |
| **List Files** | `Get-ChildItem -Path .` | `ls -la` | `python -c "import os; print(os.listdir('.'))"` |

---

## ⚙️ 5. Environment Variables

| Task | Windows PowerShell | Windows CMD | macOS / Linux (Bash/Zsh) |
| :--- | :--- | :--- | :--- |
| **Set Temporary Variable** | `$env:PORT="8000"` | `set PORT=8000` | `export PORT=8000` |
| **Read Variable** | `$env:PORT` | `echo %PORT%` | `echo $PORT` |
| **Run Command with Env** | `$env:PORT="8000"; uv run app` | `set PORT=8000 && uv run app` | `PORT=8000 uv run app` |
| **Remove Variable** | `Remove-Item Env:\PORT` | `set PORT=` | `unset PORT` |

---

## 🔎 6. Text Search & Verification (Replacing grep / sed / awk)

| Task | Windows PowerShell | macOS / Linux | Cross-Platform Python (Recommended) |
| :--- | :--- | :--- | :--- |
| **Pattern Search in Output** | `curl.exe -s http://localhost:8000/api/v1/health | Select-String "ok"` | `curl -s http://localhost:8000/api/v1/health | grep "ok"` | `python -c "import urllib.request, json; res = urllib.request.urlopen('http://localhost:8000/api/v1/health'); assert json.load(res).get('status') == 'ok', 'Check failed'"` |
| **Find String in Files** | `Get-ChildItem -Recurse -Filter *.py | Select-String "pattern"` | `grep -rn "pattern" --include="*.py" .` | `python -c "import pathlib, re; [print(f'{p}:{i+1}:{line.strip()}') for p in pathlib.Path('.').rglob('*.py') for i, line in enumerate(p.read_text(errors='ignore').splitlines()) if re.search('pattern', line)]"` |
| **Count Matched Lines** | `(Select-String "pattern" file.txt).Count` | `grep -c "pattern" file.txt` | `python -c "print(open('file.txt').read().count('pattern'))"` |

---

## 🐳 7. Docker & Container Commands (Universally Identical)

| Task | Command (All Platforms) |
| :--- | :--- |
| **Build Backend Image** | `docker build -t app-backend:latest -f Dockerfile.backend .` |
| **Run Container with Port** | `docker run -d --name app -p 8000:8000 --env-file .env app-backend:latest` |
| **Check Running Status** | `docker ps --filter "name=app"` |
| **View Container Logs** | `docker logs app --tail 50` |
| **Stop and Remove** | `docker stop app && docker rm app` |
| **Compose Start** | `docker compose up -d` |
| **Compose Stop** | `docker compose down` |

---

## 🌿 8. Git Workflows (Universally Identical)

| Task | Command (All Platforms) |
| :--- | :--- |
| **Check Working Tree** | `git status` |
| **Inspect Staged Diff** | `git diff --cached` |
| **Create & Switch Branch** | `git checkout -b feat/my-feature` |
| **Stage Specific Files** | `git add app/main.py tests/test_api.py` |
| **Conventional Commit** | `git commit -m "feat(api): add health probe endpoint"` |
| **List Release Tags** | `git tag -l "v*" --sort=-v:refname` |
| **Create Semantic Tag** | `git tag -a v1.0.0 -m "Release version 1.0.0"` |
