---
name: performance-optimization
description: Systematic profiling, bottleneck isolation, latency reduction, memory optimization, and benchmarking without premature guesswork.
---

# Performance Optimization Skill

## 1. When Should I Use This?

Use this skill when:
* API response latency exceeds acceptable SLAs (> 200-500ms for standard CRUD, > 2s for complex RAG/inference).
* Investigating high memory consumption, CPU saturation, or GPU starvation.
* Optimizing slow SQL queries, database indexing, or ORM object serialization.
* Profiling Python execution time with `cProfile`, `py-spy`, or `line_profiler`.

Never optimize by guessing. Every optimization must begin with empirical measurement and end with benchmarking.

---

## 2. What Should I Inspect First?

1. **Bottleneck Domain**:
   * Is the bottleneck in **Database I/O** (unindexed queries, N+1 joins)?
   * Is it in **Network / External API calls** (synchronous HTTP requests, sequential LLM calls)?
   * Is it in **CPU Computation** (complex loops in Python, unvectorized Pandas/NumPy operations)?
   * Is it in **Memory / Garbage Collection** (holding giant DataFrames or tensors in RAM)?
   * Is it in **Frontend Rendering** (unnecessary re-renders, unmemoized heavy lists)?
2. **Current Baseline Metrics**: Record the current p50, p95, and p99 latency or memory watermark before making any edits.

---

## 3. What Workflow Should I Follow?

```text
1. MEASURE: Establish baseline performance with concrete metrics.
      ↓
2. PROFILE: Run profiler to locate the exact hot function or query.
      ↓
3. ISOLATE: Identify the architectural or algorithmic cause.
      ↓
4. OPTIMIZE: Apply targeted optimization (e.g. indexing, vectorization, caching).
      ↓
5. BENCHMARK: Rerun measurement under identical conditions.
      ↓
6. REGRESSION CHECK: Verify all unit and integration tests still pass.
```

### Python Profiling with `cProfile`

```python
# scripts/profile_hotspot.py
import cProfile
import pstats
from app.services.rag_service import VectorStore

def run_workload():
    store = VectorStore()
    dummy_chunks = [{"text": f"Document snippet {i}", "page_num": 1} for i in range(1000)]
    store.add_documents(dummy_chunks)
    for _ in range(50):
        store.search("Document query")

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    run_workload()
    profiler.disable()

    stats = pstats.Stats(profiler).sort_stats("cumulative")
    stats.print_stats(20)  # Print top 20 time-consuming functions
```

### Database Optimization: Eliminating N+1 Queries

```python
# SLOW (N+1 queries: 1 query for users + N queries for documents)
users = db.query(User).all()
for u in users:
    print(u.documents) # Triggers a separate SQL query per user!

# FAST (Eager joined loading: 1 single SQL query)
from sqlalchemy.orm import selectinload
users = db.query(User).options(selectinload(User.documents)).all()
```

### Pandas / NumPy Vectorization

```python
# SLOW (Python iterative loop: ~250ms on 100k rows)
for idx, row in df.iterrows():
    df.at[idx, 'adjusted'] = row['val'] * 1.05 if row['flag'] == 1 else row['val']

# FAST (Vectorized boolean indexing: ~2ms on 100k rows - 125x faster)
df['adjusted'] = np.where(df['flag'] == 1, df['val'] * 1.05, df['val'])
```

---

## 4. What Decisions Should I Make?

| Bottleneck Type | Highest-ROI Optimization |
| :--- | :--- |
| **Slow Database Query** | Add B-Tree composite index on queried columns (`WHERE a = ? AND b = ?`). |
| **Repetitive Expensive Computation** | Add In-Memory Cache with TTL (`functools.lru_cache` or Redis). |
| **Slow JSON Serialization** | Use Pydantic v2 (Rust-backed core) or `orjson` instead of standard `json.dumps`. |
| **Large DataFrame Processing** | Switch from Pandas to `Polars` for multithreaded Arrow-backed query execution. |

---

## 5. What Should I Avoid?

* **NEVER micro-optimize before profiling**: Don't waste time rewriting readable string formatting when 95% of the time is spent waiting on a database query.
* **NEVER sacrifice code correctness or readability for negligible (< 5%) speedups**.
* **NEVER cache without an invalidation or TTL strategy**: Unbounded caches cause memory leaks and serve stale data.

---

## 6. How Should I Verify Success?

```bash
# 1. Benchmark endpoint response time
python -c "
import time, httpx
times = []
for _ in range(20):
    start = time.perf_counter()
    r = httpx.get('http://localhost:8000/api/v1/health')
    times.append(time.perf_counter() - start)
print(f'Average Latency: {sum(times)/len(times)*1000:.2f}ms | Min: {min(times)*1000:.2f}ms | Max: {max(times)*1000:.2f}ms')
"

# 2. Run full regression test suite
pytest -v
```
