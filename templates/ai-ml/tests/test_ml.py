import pandas as pd
import numpy as np
from ml.train import train_baseline

def test_train_baseline_pipeline():
    X = pd.DataFrame({"feat1": np.random.randn(50), "feat2": np.random.randn(50)})
    y = pd.Series(np.random.randint(0, 2, size=50))
    pipeline = train_baseline(X, y)
    preds = pipeline.predict(X)
    assert len(preds) == 50
