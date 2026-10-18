
from pathlib import Path
import sys

import joblib

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "intent_model.joblib"

# Experimental threshold; validate before deployment.
CONFIDENCE_THRESHOLD = 0.05


def predict_intent(message):
    if not message or not message.strip():
        return {
            "intent": "unknown",
            "confidence": 0.0,
            "needs_clarification": True,
        }

    model = joblib.load(MODEL_PATH)
    predicted_intent = model.predict([message])[0]

    # Use probabilities when the model supports them.
    if hasattr(model, "predict_proba"):
        scores = model.predict_proba([message])[0]
        confidence = float(max(scores))

    # LinearSVC has decision_function, not predict_proba.
    elif hasattr(model, "decision_function"):
        scores = model.decision_function([message])[0]

        # Convert multiclass decision scores into relative scores.
        # These are NOT calibrated probabilities.
        import numpy as np

        scores = np.asarray(scores, dtype=float)
        shifted = scores - np.max(scores)
        relative_scores = np.exp(shifted)
        relative_scores /= relative_scores.sum()
        confidence = float(np.max(relative_scores))

    else:
        confidence = 0.0

    needs_clarification = confidence < CONFIDENCE_THRESHOLD

    if needs_clarification:
        predicted_intent = "unknown"

    return {
        "intent": predicted_intent,
        "confidence": confidence,
        "needs_clarification": needs_clarification,
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        result = predict_intent(message)
        print(f"Message: {message}")
        print(f"Predicted intent: {result['intent']}")
        print(f"Model score: {result['confidence']:.2%}")
        print(f"Needs clarification: {result['needs_clarification']}")
    else:
        print("Customer service intent classifier")
        print("Type a message, or type 'exit' to quit.")

        while True:
            message = input("\nYou: ")
            if message.strip().lower() in {"exit", "quit"}:
                break

            result = predict_intent(message)
            print(f"Intent: {result['intent']}")
            print(f"Model score: {result['confidence']:.2%}")

            if result["needs_clarification"]:
                print(
                    "Please clarify your request, "
                    "or ask to speak with a human agent."
                )
