
import json
from pathlib import Path
from collections import Counter

data_path = Path("ml_model/data/clinc150/data_full.json")

with data_path.open("r", encoding="utf-8") as file:
    data = json.load(file)

print("CLINC150 dataset summary")
print("=" * 35)

for section in ["train", "val", "test", "oos_train", "oos_val", "oos_test"]:
    examples = data.get(section, [])
    labels = Counter(
        example[1]
        for example in examples
        if isinstance(example, list) and len(example) >= 2
    )

    print(f"\n{section}: {len(examples)} examples")
    print(f"Number of labels: {len(labels)}")

    if labels:
        print("Sample labels:", ", ".join(sorted(labels)[:10]))

print("\nOriginal project files have not been changed.")
