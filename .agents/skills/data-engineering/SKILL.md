---
name: data-engineering
description: Data cleaning, schema enforcement, time-series transformations, Daylight Saving Time (DST) handling, rolling features, and leak-free feature pipelines.
---

# Data Engineering Skill

## 1. When Should I Use This?

Use this skill when:
* Cleaning, transforming, or validating tabular, time-series, or batch datasets.
* Handling timestamp discontinuities, Daylight Saving Time (DST) duplicate hours, structural gaps, or missing values.
* Engineering temporal, cyclical (sine/cosine), lag, and rolling-window statistical features.
* Building reproducible, versioned data pipelines using **Pandas**, **Polars**, or **NumPy**.

---

## 2. What Should I Inspect First?

1. **Schema & Data Types**: Inspect column types, null percentages, date formats (`ISO8601`, UNIX timestamps, naive vs UTC timezones).
2. **Temporal Integrity (For Time Series)**:
   * Are there duplicate timestamps? (Common in fall DST clock fallbacks).
   * Are there missing intervals? (Common in spring DST clock skips).
   * Is the data strictly sorted chronologically?
3. **Target Variable Stability**: Inspect target distribution, outliers, and extreme spikes.

---

## 3. What Workflow Should I Follow?

```text
Load Raw Invariant Dataset
            ↓
Data Quality Audit (Nulls, Duplicates, Types, Extreme Outliers)
            ↓
Temporal Resolution & DST Handling (Mean aggregate duplicate hours / resample)
            ↓
Feature Engineering (Calendar, Sine/Cosine Cyclical, Lags, Rolling Windows)
            ↓
Strict Chronological / Group-Aware Train-Val-Test Split
            ↓
Validate Feature Order & Export Processed Parquet / CSV Datasets
```

### Time-Series DST & Temporal Feature Engineering Pipeline

```python
# data_engineering/pipeline.py
import numpy as np
import pandas as pd

def process_energy_time_series(df: pd.DataFrame, datetime_col: str, target_col: str) -> pd.DataFrame:
    # 1. Parse timestamps and sort chronologically
    df[datetime_col] = pd.to_datetime(df[datetime_col])
    df = df.sort_values(datetime_col).reset_index(drop=True)

    # 2. DST Duplicate Timestamp Resolution: Mean aggregate duplicate hours
    df = df.groupby(datetime_col, as_index=False)[target_col].mean()

    # 3. Calendar & Cyclical Features
    dt = df[datetime_col].dt
    df['hour'] = dt.hour
    df['dayofweek'] = dt.dayofweek
    df['month'] = dt.month
    df['is_weekend'] = (df['dayofweek'] >= 5).astype(int)

    # Cyclical hour encoding (smooth 24-hour periodic boundary)
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24.0)

    # 4. Lag Features (Historical lookbacks)
    df['lag_1h'] = df[target_col].shift(1)
    df['lag_24h'] = df[target_col].shift(24)
    df['lag_168h'] = df[target_col].shift(168) # 1-week seasonal lag

    # 5. Rolling Window Statistics (Strictly backward-looking)
    df['rolling_mean_24h'] = df[target_col].shift(1).rolling(window=24).mean()
    df['rolling_std_24h'] = df[target_col].shift(1).rolling(window=24).std()
    df['rolling_mean_168h'] = df[target_col].shift(1).rolling(window=168).mean()

    # 6. Drop warm-up NaN rows created by the 168h lookback
    df = df.dropna().reset_index(drop=True)
    return df

def split_chronological(df: pd.DataFrame, train_ratio=0.70, val_ratio=0.15):
    n = len(df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()

    print(f"Train: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}")
    return train_df, val_df, test_df
```

---

## 4. What Decisions Should I Make?

| Challenge | Engineering Rule |
| :--- | :--- |
| **Rolling Stats Leakage** | Always apply `.shift(1)` before computing `.rolling()` when forecasting current target $y_t$. Otherwise, $y_t$ leaks into the rolling mean of time $t$. |
| **File Storage Format** | Use **Parquet** with Snappy compression for intermediate processed datasets. It preserves exact column types, handles nulls natively, and is 5-10x faster to load than CSV. |
| **Missing Values** | Impute time-series gaps using forward-fill (`ffill`) or linear interpolation only for small gaps (<= 3 hours). Never use future lookahead backfill (`bfill`). |

---

## 5. What Should I Avoid?

* **NEVER shuffle time-series rows**: Preserving temporal ordering is non-negotiable.
* **NEVER overwrite raw source datasets**: Raw data must remain immutable in `datasets/raw/`. Always write transformed outputs to `datasets/processed/`.
* **NEVER use current timestamp features that are unavailable at inference time**: Only use historical lag features.

---

## 6. How Should I Verify Success?

```bash
# 1. Run data engineering pipeline
python data_engineering/pipeline.py

# 2. Check for missing values and temporal continuity
python -c "
import pandas as pd
df = pd.read_parquet('datasets/processed/cleaned_features.parquet')
assert df.isna().sum().sum() == 0, 'Null values remain in processed data!'
print('Data engineering validation clean. Total rows:', len(df))
"
```
