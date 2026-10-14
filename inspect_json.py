
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
SOURCE_DIR = BASE_DIR / "data" / "raw" / "phonepe-pulse" / "data"

files = list(SOURCE_DIR.rglob("*.json"))

print("JSON files found:", len(files))

for file in files:
    if "transaction" in str(file).lower():
        print("\nFILE:", file)

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            print("Root type:", type(data).__name__)

            if isinstance(data, dict):
                print("Root keys:", list(data.keys()))

                content = data.get("data")
                print("Data type:", type(content).__name__)

                if isinstance(content, dict):
                    print("Data keys:", list(content.keys()))
                    print("Sample:", str(content)[:1200])

                elif isinstance(content, list):
                    print("First items:", str(content[:3])[:1200])

            else:
                print("Sample:", str(data)[:1200])

            break

        except Exception as e:
            print("Error reading file:", e)
