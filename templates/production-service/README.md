# Production Enterprise Microservice Template

FastAPI microservice starter with OpenTelemetry, structured JSON logging, correlation IDs, multi-stage Docker builds, and Render blueprint configuration.

## 🚀 Quickstart

```bash
# 1. Initialize isolated environment & sync dependencies
uv venv .venv --python 3.12
uv sync

# 2. Run development server (universal cross-platform via uv run)
uv run uvicorn app.main:app --reload --port 8000
```

## 🧪 Testing & Validation

```bash
uv run pytest -v
uv run ruff check .
```
