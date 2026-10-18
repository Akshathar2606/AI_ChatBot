
from pathlib import Path

import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, f1_score

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
MODEL_PATH = BASE_DIR / "models" / "intent_model.joblib"
TEST_PATH = PROJECT_DIR / "evaluation" / "test_cases.csv"

data = pd.read_csv(TEST_PATH).dropna(
    subset=["customer_message", "expected_intent"]
)

model = joblib.load(MODEL_PATH)
messages = data["customer_message"].astype(str).tolist()
actual = data["expected_intent"].astype(str).tolist()

probabilities = model.predict_proba(messages)
raw_predictions = model.classes_[probabilities.argmax(axis=1)]
confidence = probabilities.max(axis=1)

print("\n=== CONFIDENCE THRESHOLD COMPARISON ===")
print("Threshold | Accuracy | Macro F1 | Clarifications")

for threshold in [0.00, 0.05, 0.10, 0.12, 0.15, 0.18, 0.20]:
    final_predictions = [
        prediction if score >= threshold else "unknown"
        for prediction, score in zip(raw_predictions, confidence)
    ]

    accuracy = accuracy_score(actual, final_predictions)
    macro_f1 = f1_score(
        actual,
        final_predictions,
        average="macro",
        zero_division=0,
    )
    clarification_count = sum(
        score < threshold for score in confidence
    )

    print(
        f"{threshold:8.2f} | "
        f"{accuracy:7.2%} | "
        f"{macro_f1:8.2%} | "
        f"{clarification_count:2d}/{len(data)}"
    )

print("\n=== GREETING CHECK ===")
for message in ["Hello", "Hi there", "Good morning"]:
    scores = model.predict_proba([message])[0]
    index = scores.argmax()
    print(
        f"{message!r}: raw={model.classes_[index]}, "
        f"confidence={scores[index]:.2%}"
    )
