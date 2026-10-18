
import json
from pathlib import Path
from collections import Counter

path = Path("ml_model/data/clinc150/data_full.json")

with path.open("r", encoding="utf-8") as file:
    data = json.load(file)

print("Dataset sections:", list(data.keys()))

for section, examples in data.items():
    if isinstance(examples, list):
        print(f"\n{section}: {len(examples)} examples")
        print("Sample:", examples[:3])

        intents = Counter()
        for example in examples:
            if isinstance(example, list) and len(example) >= 2:
                intents[str(example[1])] += 1

        if intents:
            print("Unique intents:", len(intents))
            print("Most common:", intents.most_common(10))
