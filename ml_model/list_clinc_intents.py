
import json
from pathlib import Path

path = Path("ml_model/data/clinc150/data_full.json")

with path.open("r", encoding="utf-8") as file:
    data = json.load(file)

intents = sorted({
    example[1]
    for example in data["train"]
    if len(example) >= 2 and example[1] != "oos"
})

print(f"Total intents: {len(intents)}")
print("\n".join(intents))
