
import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

DATA_PATH = Path("ml_model/data/clinc150/data_full.json")
MODEL_PATH = Path("ml_model/models/clinc150_model.joblib")

with DATA_PATH.open("r", encoding="utf-8") as file:
    data = json.load(file)

model = joblib.load(MODEL_PATH)

# Known-intent examples from the validation split
known_texts = [item[0] for item in data["val"]]
known_labels = [0] * len(known_texts)

# Separate OOS validation examples
oos_texts = [item[0] for item in data["oos_val"]]
oos_labels = [1] * len(oos_texts)

texts = known_texts + oos_texts
true_oos = np.array(known_labels + oos_labels)

# Linear SVM has decision scores, not calibrated probabilities.
scores = model.decision_function(texts)
confidence = np.max(scores, axis=1)

print("Known validation examples:", len(known_texts))
print("OOS validation examples:", len(oos_texts))
print("\nTesting confidence thresholds")

for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
    predicted_oos = (confidence < threshold).astype(int)

    print(
        f"Threshold={threshold:.1f} | "
        f"Accuracy={accuracy_score(true_oos, predicted_oos):.3f} | "
        f"OOS precision={precision_score(true_oos, predicted_oos, zero_division=0):.3f} | "
        f"OOS recall={recall_score(true_oos, predicted_oos, zero_division=0):.3f} | "
        f"OOS F1={f1_score(true_oos, predicted_oos, zero_division=0):.3f}"
    )

print("\nThis is a threshold experiment only; no model files were changed.")
