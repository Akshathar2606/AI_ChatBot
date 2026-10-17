
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

DATA_FILE = DATA_DIR / "training_data.csv"
INTENTS_FILE = DATA_DIR / "intents.json"


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Load training data and the team's supported intent labels.
    data = pd.read_csv(DATA_FILE)

    required_columns = {"text", "intent"}
    if not required_columns.issubset(data.columns):
        raise ValueError("CSV must contain 'text' and 'intent' columns.")

    data = data.dropna(subset=["text", "intent"])
    data["text"] = data["text"].astype(str).str.strip()
    data["intent"] = data["intent"].astype(str).str.strip()
    data = data[(data["text"] != "") & (data["intent"] != "")]

    with open(INTENTS_FILE, "r", encoding="utf-8") as file:
        supported_intents = {
            item["name"] for item in json.load(file)["intents"]
        }

    unknown_labels = set(data["intent"]) - supported_intents
    if unknown_labels:
        raise ValueError(f"Labels not found in intents.json: {unknown_labels}")

    counts = data["intent"].value_counts()
    if len(counts) < 2 or counts.min() < 2:
        raise ValueError("Each intent needs at least two training examples.")

    X = data["text"]
    y = data["intent"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=42,
        ),
        "Linear SVM": LinearSVC(
            class_weight="balanced",
            random_state=42,
        ),
    }

    results = []

    print(f"Total examples: {len(data)}")
    print(f"Number of intents: {data['intent'].nunique()}")
    print(f"Training examples: {len(X_train)}")
    print(f"Test examples: {len(X_test)}")

    for name, classifier in models.items():
        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                sublinear_tf=True,
            )),
            ("classifier", classifier),
        ])

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test,
            predictions,
            average="macro",
            zero_division=0,
        )

        results.append({
            "name": name,
            "pipeline": pipeline,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        })

        print(f"\n{'=' * 55}")
        print(name)
        print(f"Accuracy:          {accuracy:.4f}")
        print(f"Macro precision:   {precision:.4f}")
        print(f"Macro recall:      {recall:.4f}")
        print(f"Macro F1-score:    {f1:.4f}")
        print("\nClassification report:")
        print(classification_report(
            y_test,
            predictions,
            labels=sorted(supported_intents),
            zero_division=0,
        ))
        print("Confusion matrix (labels in alphabetical order):")
        print(confusion_matrix(
            y_test,
            predictions,
            labels=sorted(supported_intents),
        ))

    # Select by macro F1, then refit the selected pipeline on all data.
    best = max(results, key=lambda item: item["f1"])
    best_pipeline = best["pipeline"]
    best_pipeline.fit(X, y)

    model_path = MODEL_DIR / "intent_model.joblib"
    joblib.dump(best_pipeline, model_path)

    summary = {
        item["name"]: {
            "accuracy": item["accuracy"],
            "macro_precision": item["precision"],
            "macro_recall": item["recall"],
            "macro_f1": item["f1"],
        }
        for item in results
    }
    summary["selected_model"] = best["name"]
    summary["selection_metric"] = "macro_f1"
    summary["note"] = (
        "Metrics are from a small held-out split; "
        "the saved model is refitted on all training examples."
    )

    with open(MODEL_DIR / "evaluation_results.json", "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print(f"\nSelected model: {best['name']}")
    print(f"Saved model to: {model_path}")
    print(f"Saved metrics to: {MODEL_DIR / 'evaluation_results.json'}")


if __name__ == "__main__":
    main()
