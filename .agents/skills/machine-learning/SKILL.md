---
name: machine-learning
description: End-to-end tabular and classical ML workflows, Scikit-Learn, XGBoost, leak-free preprocessing, validation discipline, baseline benchmarking, and artifact serialization.
---

# Machine Learning Skill

## 1. When Should I Use This?

Use this skill when:
* Building, evaluating, or deploying classical machine learning models (Classification, Regression, Time-series forecasting, Fraud detection).
* Utilizing **Scikit-Learn**, **XGBoost**, **LightGBM**, or **RandomForest**.
* Designing preprocessing pipelines, cross-validation splits, and baseline benchmarks.
* Serializing and serving model artifacts (`.joblib`, `.pkl`) with strict schema validation.

---

## 2. What Should I Inspect First?

1. **Dataset Properties**:
   * Inspect sample size, feature types (numerical, categorical, datetime), missing values, and class imbalance.
2. **Problem Type & Split Strategy**:
   * Standard I.I.D. data → Stratified K-Fold / Stratified Train/Val/Test.
   * Time-series data → Strict Chronological Split (No future data in training set).
   * Grouped/Entity data (e.g. patients, users) → Group-Stratified Split (0% group overlap).
3. **Existing Baselines**: What is the performance of a naive heuristic or persistence model (e.g. mean predictor, 24h lag)?

---

## 3. What Workflow Should I Follow?

```text
Dataset Audit & Quality Checks (NaNs, Duplicates, Types)
                     ↓
Leak-Free Partitioning (Train / Validation / Test)
                     ↓
Fit Preprocessor on TRAIN SET ONLY (Scalers, Encoders, Imputers)
                     ↓
Establish Naive / Heuristic Baselines (Persistence, DummyClassifier)
                     ↓
Train & Tune Candidate Models on Validation Set
                     ↓
Select Best Model based SOLELY on Validation Metrics
                     ↓
Single Final Evaluation on Held-Out Test Set
                     ↓
Package Pipeline & Artifact Metadata (.joblib + feature_schema.json)
                     ↓
Inference Schema Verification
```

### Complete Leak-Free Pipeline Pattern

```python
# ml/training/train_pipeline.py
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score

def build_and_train_pipeline(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_val: pd.DataFrame,
    y_val: pd.Series,
    numeric_features: list[str],
    categorical_features: list[str]
) -> Pipeline:
    # 1. Define preprocessors
    num_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, numeric_features),
            ('cat', cat_transformer, categorical_features)
        ]
    )

    # 2. Assemble complete pipeline
    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        random_state=42,
        eval_metric="logloss"
    )

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    # 3. Fit pipeline strictly on TRAIN data
    pipeline.fit(X_train, y_train)

    # 4. Evaluate on Validation Set
    val_preds = pipeline.predict(X_val)
    val_probs = pipeline.predict_proba(X_val)[:, 1]
    
    print("Validation Classification Report:")
    print(classification_report(y_val, val_preds))
    print(f"Validation ROC-AUC: {roc_auc_score(y_val, val_probs):.4f}")

    return pipeline

def save_model_artifact(pipeline: Pipeline, feature_names: list[str], output_path: str):
    artifact = {
        "pipeline": pipeline,
        "feature_names": feature_names,
        "version": "1.0.0"
    }
    joblib.dump(artifact, output_path)
    print(f"Model artifact saved to {output_path}")
```

---

## 4. What Decisions Should I Make?

| Challenge | Engineering Rule |
| :--- | :--- |
| **Model Selection** | NEVER choose hyperparameters or best models based on the test set. Test set is strictly for unbiased final evaluation. |
| **Class Imbalance** | Use PR-AUC, F1-Score, and Balanced Accuracy instead of plain accuracy. Use `scale_pos_weight` in XGBoost or SMOTE inside train splits only. |
| **Artifact Packaging** | Always bundle feature transformation (ColumnTransformer) and model inside a unified `Pipeline` object so inference receives raw features and applies identical transformations. |

---

## 5. What Should I Avoid?

* **NEVER fit scalers/encoders on the whole dataset before splitting**: This causes catastrophic data leakage.
* **NEVER shuffle time-series data**: Shuffling future timestamps into the training set creates fake 99% accuracy that fails completely in production.
* **NEVER claim ML success without comparing against a baseline**: Always beat a simple heuristic (e.g. 24h lag for energy forecasting or majority class for fraud).
* **NEVER train without fixed random seeds**: Set `random_state=42` for reproducibility.

---

## 6. How Should I Verify Success?

```bash
# 1. Run pipeline training and validation script
python ml/training/train_pipeline.py

# 2. Run inference sanity test against model artifact
python -c "
import joblib, pandas as pd
artifact = joblib.load('ml/artifacts/model.joblib')
pipeline = artifact['pipeline']
dummy_data = pd.DataFrame([{col: 0.0 for col in artifact['feature_names']}])
pred = pipeline.predict(dummy_data)
print('Inference verification passed. Prediction:', pred)
"

# 3. Execute ML unit tests
pytest tests/unit/test_ml_pipeline.py -v
```
