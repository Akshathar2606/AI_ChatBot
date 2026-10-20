import json
from pathlib import Path
import joblib
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
DATA = json.load(open("ml_model/data/clinc150/data_full.json", encoding="utf-8"))
model = joblib.load("ml_model/models/clinc150_model.joblib")
saved = json.load(open("ml_model/models/oos_threshold_results.json", encoding="utf-8"))
threshold = saved["selected_threshold"]
known = [x[0] for x in DATA["test"]]
oos = [x[0] for x in DATA["oos_test"]]
texts = known + oos
y = np.array([0] * len(known) + [1] * len(oos))
scores = model.decision_function(texts)
pred = (np.max(scores, axis=1) < threshold).astype(int)
print("Threshold:", threshold)
print("Known test examples:", len(known))
print("OOS test examples:", len(oos))
print("Overall accuracy:", round(accuracy_score(y, pred), 4))
print("OOS precision:", round(precision_score(y, pred, zero_division=0), 4))
print("OOS recall:", round(recall_score(y, pred, zero_division=0), 4))
print("OOS F1:", round(f1_score(y, pred, zero_division=0), 4))
