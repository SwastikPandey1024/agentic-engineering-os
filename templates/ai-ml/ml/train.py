import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

def train_baseline(X_train: pd.DataFrame, y_train: pd.Series) -> Pipeline:
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', XGBClassifier(n_estimators=100, random_state=42, eval_metric="logloss"))
    ])
    pipeline.fit(X_train, y_train)
    return pipeline

if __name__ == "__main__":
    print("Training pipeline ready.")
