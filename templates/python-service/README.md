# Python Service Starter Template

FastAPI microservice starter configured with `uv`, Pydantic Settings, Pytest, and Ruff.

## 🚀 Quickstart

```bash
# 1. Initialize isolated environment & sync dependencies
uv venv .venv --python 3.12
uv sync

# 2. Configure environment
# Windows PowerShell: Copy-Item .env.example .env
# Linux / macOS:      cp .env.example .env

# 3. Run development server (universal cross-platform via uv run)
uv run uvicorn app.main:app --reload --port 8000
```

## 🧪 Testing & Quality

```bash
uv run pytest -v
uv run ruff check .
```
