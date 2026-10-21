
from pathlib import Path
import json

import pandas as pd
from joblib import load
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
)

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
TEST_DATA_PATH = PROJECT_DIR / "evaluation" / "test_cases.csv"
MODEL_PATH = BASE_DIR / "models" / "intent_model.joblib"

THRESHOLDS = [0.00, 0.05, 0.10, 0.12, 0.15, 0.18, 0.20]


def main():
    if not TEST_DATA_PATH.exists():
        raise FileNotFoundError(f"Test cases not found: {TEST_DATA_PATH}")

    data = pd.read_csv(TEST_DATA_PATH).dropna(
        subset=["customer_message", "expected_intent"]
    )

    messages = data["customer_message"].astype(str).tolist()
    actual = data["expected_intent"].astype(str).tolist()

    model = load(MODEL_PATH)
    raw = model.predict(messages).tolist()

    # Reproduce the same relative SVM scores used by predict.py.
    import numpy as np

    if hasattr(model, "predict_proba"):
        scores = model.predict_proba(messages)
        confidence = scores.max(axis=1)
    else:
        scores = np.asarray(model.decision_function(messages))
        if scores.ndim == 1:
            scores = np.column_stack([-scores, scores])
        shifted = scores - scores.max(axis=1, keepdims=True)
        relative = np.exp(shifted)
        relative /= relative.sum(axis=1, keepdims=True)
        confidence = relative.max(axis=1)

    raw_accuracy = accuracy_score(actual, raw)
    print("\n=== THRESHOLD COMPARISON ===")
    print(f"Test cases: {len(actual)}")
    print(f"Raw model accuracy: {raw_accuracy:.2%}\n")
    print(
        f"{'Threshold':>10} {'Accuracy':>10} {'Macro F1':>10} "
        f"{'Clarify':>10} {'Correct -> unknown':>20}"
    )
    print("-" * 66)

    rows = []
    for threshold in THRESHOLDS:
        final = [
            prediction if score >= threshold else "unknown"
            for prediction, score in zip(raw, confidence)
        ]

        precision, recall, f1, _ = precision_recall_fscore_support(
            actual,
            final,
            average="macro",
            zero_division=0,
        )
        accuracy = accuracy_score(actual, final)
        clarify_count = sum(score < threshold for score in confidence)
        correct_to_unknown = sum(
            expected == prediction and score < threshold
            for expected, prediction, score in zip(actual, raw, confidence)
        )

        rows.append({
            "threshold": threshold,
            "accuracy": float(accuracy),
            "macro_precision": float(precision),
            "macro_recall": float(recall),
            "macro_f1": float(f1),
            "clarification_count": int(clarify_count),
            "correct_predictions_changed_to_unknown": int(correct_to_unknown),
        })

        print(
            f"{threshold:>10.2f} {accuracy:>9.2%} {f1:>9.2%} "
            f"{clarify_count:>10} {correct_to_unknown:>20}"
        )

    output_path = BASE_DIR / "models" / "threshold_comparison.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({
        "test_cases": len(actual),
        "raw_accuracy": float(raw_accuracy),
        "note": (
            "SVM scores are relative, not calibrated probabilities. "
            "Thresholds are experimental; this same test set has been "
            "used for comparison and should not be treated as an unbiased "
            "final estimate."
        ),
        "results": rows,
    }, indent=2), encoding="utf-8")

    print(f"\nDetailed comparison saved to:\n{output_path}")


if __name__ == "__main__":
    main()
