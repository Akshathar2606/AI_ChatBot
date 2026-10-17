
from pathlib import Path
import sys

import joblib

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "intent_model.joblib"


def predict_intent(message):
    if not message or not message.strip():
        return {"intent": "unknown", "confidence": 0.0}

    model = joblib.load(MODEL_PATH)
    predicted_intent = model.predict([message])[0]

    # Logistic Regression provides class probabilities.
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba([message])[0]
        confidence = float(max(probabilities))
    else:
        confidence = 0.0

    return {
        "intent": predicted_intent,
        "confidence": confidence,
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        result = predict_intent(message)
        print(f"Message: {message}")
        print(f"Predicted intent: {result['intent']}")
        print(f"Model confidence: {result['confidence']:.2%}")
    else:
        print("Customer service intent classifier")
        print("Type a message, or type 'exit' to quit.")

        while True:
            message = input("\nYou: ")
            if message.strip().lower() in {"exit", "quit"}:
                break

            result = predict_intent(message)
            print(f"Intent: {result['intent']}")
            print(f"Model confidence: {result['confidence']:.2%}")
