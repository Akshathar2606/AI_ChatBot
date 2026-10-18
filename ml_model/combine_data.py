
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

original_path = DATA_DIR / "training_data.csv"
additional_path = DATA_DIR / "additional_training_data.csv"
output_path = DATA_DIR / "combined_training_data.csv"

original = pd.read_csv(original_path)
additional = pd.read_csv(additional_path)

required_columns = {"text", "intent"}

for name, dataset in [
    ("original", original),
    ("additional", additional),
]:
    if not required_columns.issubset(dataset.columns):
        raise ValueError(f"{name} dataset must contain text and intent columns")
    if dataset[list(required_columns)].isna().any().any():
        raise ValueError(f"{name} dataset contains missing values")

combined = pd.concat([original, additional], ignore_index=True)

# Remove exact duplicate message-label pairs.
combined["text"] = combined["text"].astype(str).str.strip()
combined["intent"] = combined["intent"].astype(str).str.strip()
combined = combined.drop_duplicates(subset=["text", "intent"])

# A single message should not have conflicting labels.
conflicts = combined.groupby("text")["intent"].nunique()
conflicts = conflicts[conflicts > 1]

if not conflicts.empty:
    print("Messages with conflicting labels:")
    print(conflicts.index.tolist())
    raise ValueError("Resolve conflicting labels before training.")

combined = combined.sample(frac=1, random_state=42).reset_index(drop=True)
combined.to_csv(output_path, index=False, encoding="utf-8")

print(f"Original examples:   {len(original)}")
print(f"Additional examples: {len(additional)}")
print(f"Combined examples:   {len(combined)}")
print("\nExamples per intent:")
print(combined["intent"].value_counts().sort_index().to_string())
print(f"\nSaved to: {output_path}")
