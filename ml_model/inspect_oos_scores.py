
import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score

data_path = Path("ml_model/data/clinc150/data_full.json")
model_path = Path("ml_model/models/clinc150_model.joblib")

with data_path.open("r", encoding="utf-8") as file:
    data = json.load(file)

model = joblib.load(model_path)

known = [item[0] for item in data["val"]]
oos = [item[0] for item in data["oos_val"]]

known_scores = np.max(model.decision_function(known), axis=1)
oos_scores = np.max(model.decision_function(oos), axis=1)

print("VALIDATION SCORE DISTRIBUTION")
print("Known examples:", len(known_scores))
print("OOS examples:", len(oos_scores))

for name, scores in [("Known", known_scores), ("OOS", oos_scores)]:
    print(
        f"{name}: min={np.min(scores):.3f}, "
        f"median={np.median(scores):.3f}, max={np.max(scores):.3f}"
    )
    print(
        f"{name}: 10th percentile={np.percentile(scores, 10):.3f}, "
        f"25th percentile={np.percentile(scores, 25):.3f}, "
        f"75th percentile={np.percentile(scores, 75):.3f}, "
        f"90th percentile={np.percentile(scores, 90):.3f}"
    )

print("\nTHRESHOLD COMPARISON ON VALIDATION DATA")

y_true = np.array([0] * len(known_scores) + [1] * len(oos_scores))
all_scores = np.concatenate([known_scores, oos_scores])

for threshold in [-0.73, -0.65, -0.60, -0.55, -0.49, -0.44, -0.40]:
    predicted = (all_scores < threshold).astype(int)
    print(
        f"threshold={threshold:.2f} "
        f"precision={precision_score(y_true, predicted, zero_division=0):.3f} "
        f"recall={recall_score(y_true, predicted, zero_division=0):.3f} "
        f"F1={f1_score(y_true, predicted, zero_division=0):.3f}"
    )

print("\nNo model or threshold files were changed.")
