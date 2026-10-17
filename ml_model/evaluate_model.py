
from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

MODEL_PATH = BASE_DIR / "models" / "intent_model.joblib"
TEST_DATA_PATH = PROJECT_DIR / "evaluation" / "test_cases.csv"
RESULTS_PATH = BASE_DIR / "models" / "test_evaluation_results.json"


def main():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Trained model not found: {MODEL_PATH}. Run train_model.py first."
        )

    if not TEST_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Test cases not found: {TEST_DATA_PATH}"
        )

    test_data = pd.read_csv(TEST_DATA_PATH)

    required_columns = {"customer_message", "expected_intent"}
    missing_columns = required_columns - set(test_data.columns)

    if missing_columns:
        raise ValueError(f"Missing CSV columns: {sorted(missing_columns)}")

    test_data = test_data.dropna(
        subset=["customer_message", "expected_intent"]
    )

    model = joblib.load(MODEL_PATH)

    messages = test_data["customer_message"].astype(str).tolist()
    actual_intents = test_data["expected_intent"].astype(str).tolist()
    predicted_intents = model.predict(messages).tolist()

    accuracy = accuracy_score(actual_intents, predicted_intents)

    precision, recall, f1, _ = precision_recall_fscore_support(
        actual_intents,
        predicted_intents,
        average="macro",
        zero_division=0,
    )

    labels = sorted(set(actual_intents) | set(predicted_intents))

    report = classification_report(
        actual_intents,
        predicted_intents,
        labels=labels,
        output_dict=True,
        zero_division=0,
    )

    matrix = confusion_matrix(
        actual_intents, predicted_intents, labels=labels
    )

    results = {
        "test_cases_evaluated": len(test_data),
        "accuracy": round(float(accuracy), 4),
        "macro_precision": round(float(precision), 4),
        "macro_recall": round(float(recall), 4),
        "macro_f1": round(float(f1), 4),
        "labels": labels,
        "confusion_matrix": matrix.tolist(),
        "classification_report": report,
        "predictions": [
            {
                "customer_message": message,
                "expected_intent": actual,
                "predicted_intent": predicted,
                "correct": actual == predicted,
            }
            for message, actual, predicted
            in zip(messages, actual_intents, predicted_intents)
        ],
        "note": (
            "Results are from the separate team test cases. "
            "The test cases were not used to train the model."
        ),
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    print("\n=== CUSTOMER SERVICE INTENT MODEL EVALUATION ===")
    print(f"Test cases evaluated: {len(test_data)}")
    print(f"Accuracy:             {accuracy:.2%}")
    print(f"Macro precision:      {precision:.2%}")
    print(f"Macro recall:         {recall:.2%}")
    print(f"Macro F1-score:       {f1:.2%}")

    print("\n=== PER-INTENT CLASSIFICATION REPORT ===")
    print(
        classification_report(
            actual_intents,
            predicted_intents,
            labels=labels,
            zero_division=0,
        )
    )

    print("=== INCORRECT PREDICTIONS ===")
    errors = [
        (message, actual, predicted)
        for message, actual, predicted
        in zip(messages, actual_intents, predicted_intents)
        if actual != predicted
    ]

    if errors:
        for message, actual, predicted in errors:
            print(f"Message: {message}")
            print(f"  Expected:  {actual}")
            print(f"  Predicted: {predicted}")
    else:
        print("No incorrect predictions on these test cases.")

    print(f"\nDetailed results saved to:\n{RESULTS_PATH}")


if __name__ == "__main__":
    main()
