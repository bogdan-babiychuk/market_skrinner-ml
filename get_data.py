import json
import os
from datetime import datetime, timezone
from pathlib import Path
import requests

url = "https://ms.2eng.ru/api/ml/ds/feature-windows"

response = requests.get(
    url,
    params={
        "contractVersion": "model-window-64x6-v1",
        "lookbackSteps": 64,
        "readyOnly": "true",
    },
    auth=(
        os.environ["MS_DS_USER"],
        os.environ["MS_DS_PASSWORD"],
    ),
    timeout=15,
)
response.raise_for_status()

data = response.json()

output_dir = Path(__file__).resolve().parent / "data"
output_dir.mkdir(exist_ok=True)

saved_at = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S_%fZ")
output_path = output_dir / f"feature-windows_{saved_at}.json"

with output_path.open("x", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
    file.write("\n")

print(f"Данные сохранены: {output_path}")
