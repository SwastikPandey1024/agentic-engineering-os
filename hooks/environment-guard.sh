#!/usr/bin/env bash
# ==============================================================================
# Environment Guard Hook (Bash / Linux / macOS / WSL)
# Thin wrapper around canonical Python engine (hooks/environment_guard.py)
# ==============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINE_PATH="${SCRIPT_DIR}/environment_guard.py"

# Try Python in .venv first, then python3, then python
PYTHON_CMD=""
if [[ -f ".venv/bin/python" ]]; then
    PYTHON_CMD=".venv/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
fi

if [[ -n "${PYTHON_CMD}" && -f "${ENGINE_PATH}" ]]; then
    "${PYTHON_CMD}" "${ENGINE_PATH}"
    exit $?
else
    echo -e "\033[96m[Environment Guard] Running standalone Bash fallback...\033[0m"
    EXIT_CODE=0
    if [[ -f "pyproject.toml" || -f "requirements.txt" ]]; then
        if [[ ! -d ".venv" && ! -d "venv" ]]; then
            echo -e "\033[91m  ❌ ERROR: No project-local virtual environment (.venv/) found!\033[0m"
            EXIT_CODE=1
        fi
    fi
    exit ${EXIT_CODE}
fi
