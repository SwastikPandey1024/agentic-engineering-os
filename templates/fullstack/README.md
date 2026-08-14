# Full-Stack Starter Template (React 19 + Vite + FastAPI + PostgreSQL)

Production fullstack starter with Vite SPA, FastAPI API, and Docker Compose.

## 🚀 Local Development

```bash
# Backend Setup
cd backend
uv venv .venv --python 3.12
uv sync
uv run uvicorn app.main:app --reload --port 8000

# Frontend Setup
cd ../frontend
npm ci
npm run dev
```
