# Deterministic Environment Enforcement Hooks

This directory contains deterministic environment guard scripts designed to enforce project isolation, lockfile existence, and interpreter configuration before commands or commits are executed.

---

## 🏗️ Architecture

```text
       environment_guard.py  (Canonical Python 3 Engine)
                ▲
       ┌────────┴────────┐
       │                 │
environment-guard.ps1  environment-guard.sh
(PowerShell Wrapper)   (Bash Wrapper)
```

| Script | Platform | Purpose |
| :--- | :--- | :--- |
| [`environment_guard.py`](environment_guard.py) | **Universal (Python 3)** | Canonical validation engine. Works on all OS with standard library Python. |
| [`environment-guard.ps1`](environment-guard.ps1) | **Windows PowerShell** | Thin wrapper for Windows terminal and PowerShell sessions. |
| [`environment-guard.sh`](environment-guard.sh) | **Linux / macOS / Git Bash** | Thin wrapper for POSIX shells and CI/CD pipelines. |

---

## 🪟 Windows Usage (PowerShell & Git Bash)

### 1. Run in Windows PowerShell
```powershell
# Direct invocation (wrapper or python engine)
.\hooks\environment-guard.ps1
# or
python .\hooks\environment_guard.py
```

### 2. Set Up Git Pre-Commit Hook on Windows

#### Option A: Using Windows PowerShell
```powershell
New-Item -ItemType Directory -Force -Path .git\hooks
Set-Content -Path .git\hooks\pre-commit -Value "#!/bin/sh`npowershell.exe -ExecutionPolicy Bypass -File ./hooks/environment-guard.ps1"
```

#### Option B: Using Git Bash on Windows
```bash
mkdir -p .git/hooks
cat << 'EOF' > .git/hooks/pre-commit
#!/usr/bin/env bash
./hooks/environment-guard.sh
EOF
chmod +x .git/hooks/pre-commit
```

---

## 🐧 Linux / macOS / CI Usage

### 1. Manual Execution (Bash or Python)
```bash
bash ./hooks/environment-guard.sh
# or
python3 ./hooks/environment_guard.py
```

### 2. CI/CD Pre-Flight Step (GitHub Actions)
```yaml
# .github/workflows/ci.yml
jobs:
  validate-environment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Environment Guard
        run: python3 ./hooks/environment_guard.py
```
