
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

DATA_PATH = Path("ml_model/data/clinc150/data_full.json")
MODEL_DIR = Path("ml_model/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def load_examples(examples):
    texts = [item[0] for item in examples]
    labels = [item[1] for item in examples]
    return texts, labels


with DATA_PATH.open("r", encoding="utf-8") as file:
    data = json.load(file)

X_train, y_train = load_examples(data["train"])
X_val, y_val = load_examples(data["val"])

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=2000, class_weight="balanced"
    ),
    "Linear SVM": LinearSVC(class_weight="balanced"),
}

results = []

for name, classifier in models.items():
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            strip_accents="unicode"
        )),
        ("classifier", classifier),
    ])

    print(f"\nTraining {name}...")
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_val)

    accuracy = accuracy_score(y_val, predictions)
    macro_f1 = f1_score(y_val, predictions, average="macro")

    results.append({
        "name": name,
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "pipeline": pipeline,
    })

    print(f"Validation accuracy: {accuracy:.4f}")
    print(f"Validation macro F1: {macro_f1:.4f}")

best = max(results, key=lambda result: result["macro_f1"])

print("\nBest validation model:", best["name"])
print(f"Best validation macro F1: {best['macro_f1']:.4f}")

# Save only the validation-selected model and results.
# The existing customer-service model is not overwritten.
import joblib

joblib.dump(best["pipeline"], MODEL_DIR / "clinc150_model.joblib")

summary = [
    {
        "model": result["name"],
        "validation_accuracy": result["accuracy"],
        "validation_macro_f1": result["macro_f1"],
    }
    for result in results
]

with (MODEL_DIR / "clinc150_results.json").open(
    "w", encoding="utf-8"
) as file:
    json.dump({
        "selected_model": best["name"],
        "results": summary,
        "training_examples": len(X_train),
        "validation_examples": len(X_val),
        "intent_count": len(set(y_train)),
    }, file, indent=2)

print("\nSaved separate model to ml_model/models/clinc150_model.joblib")
print("Saved results to ml_model/models/clinc150_results.json")
