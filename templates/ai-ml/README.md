# AI / Machine Learning Starter Template

Production-grade tabular ML template with leak-free preprocessing, XGBoost, and test suites.

## 🚀 Quickstart

```bash
# 1. Initialize isolated environment & sync dependencies
uv venv .venv --python 3.11
uv sync

# 2. Train baseline model (universal cross-platform via uv run)
uv run python ml/train.py

# 3. Run validation test suite
uv run pytest -v
```
