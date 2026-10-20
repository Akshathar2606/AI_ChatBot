
import json
from pathlib import Path

import joblib
from sklearn.metrics import accuracy_score, f1_score, classification_report

DATA_PATH = Path("ml_model/data/clinc150/data_full.json")
MODEL_PATH = Path("ml_model/models/clinc150_model.joblib")
RESULT_PATH = Path("ml_model/models/clinc150_test_results.json")

with DATA_PATH.open("r", encoding="utf-8") as file:
    data = json.load(file)

model = joblib.load(MODEL_PATH)

X_test = [item[0] for item in data["test"]]
y_test = [item[1] for item in data["test"]]

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
macro_f1 = f1_score(y_test, predictions, average="macro")

print("CLINC150 held-out test results")
print("=" * 35)
print(f"Test examples: {len(X_test)}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Macro F1: {macro_f1:.4f}")

print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))

# Test out-of-scope examples separately.
X_oos = [item[0] for item in data["oos_test"]]
oos_predictions = model.predict(X_oos)

print("\nOut-of-scope test")
print("=" * 35)
print(f"Examples: {len(X_oos)}")
print("These are not automatically classified as 'oos' by this model.")
print("Predicted known intents for OOS messages:", len(oos_predictions))

results = {
    "test_examples": len(X_test),
    "test_accuracy": accuracy,
    "test_macro_f1": macro_f1,
    "oos_test_examples": len(X_oos),
    "oos_messages_predicted_as_known_intents": len(oos_predictions),
    "note": "OOS detection requires a separate rejection rule or classifier."
}

with RESULT_PATH.open("w", encoding="utf-8") as file:
    json.dump(results, file, indent=2)

print(f"\nSaved results to {RESULT_PATH}")
