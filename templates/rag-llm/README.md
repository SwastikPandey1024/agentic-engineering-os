# RAG & LLM Document Intelligence Template

Self-hosted semantic search and RAG template using SentenceTransformers, FAISS, PyMuPDF, and FastAPI.

## 🚀 Quickstart

```bash
# 1. Initialize isolated environment & sync dependencies
uv venv .venv --python 3.11
uv sync

# 2. Start RAG semantic search service (universal cross-platform via uv run)
uv run uvicorn app.main:app --reload --port 8000

# 3. Run validation test suite
uv run pytest -v
```
