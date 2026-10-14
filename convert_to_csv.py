
import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent

SOURCE_DIR = (
    BASE_DIR / "data" / "raw" / "phonepe-pulse"
    / "data" / "aggregated" / "transaction"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

rows = []
errors = 0

json_files = list(SOURCE_DIR.rglob("*.json"))

print(f"JSON files found: {len(json_files)}")

for file in json_files:
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        transaction_data = data.get("data", {}).get(
            "transactionData", []
        )

        # Expected path: .../state/year/quarter.json
        relative_parts = file.relative_to(SOURCE_DIR).parts

        if len(relative_parts) < 3:
            continue

        state = relative_parts[-3]
        year = int(relative_parts[-2])
        quarter = int(file.stem)

        for item in transaction_data:
            category = item.get("name")

            for payment in item.get("paymentInstruments", []):
                rows.append({
                    "state": state,
                    "year": year,
                    "quarter": quarter,
                    "transaction_type": category,
                    "payment_instrument": payment.get("type"),
                    "transaction_count": payment.get("count")
                })

    except (OSError, json.JSONDecodeError, ValueError, TypeError) as e:
        errors += 1
        print(f"Skipped {file}: {e}")

if rows:
    df = pd.DataFrame(rows)

    output_file = OUTPUT_DIR / "phonepe_transactions.csv"
    df.to_csv(output_file, index=False)

    print("\nCSV created successfully!")
    print(f"Rows: {len(df):,}")
    print(f"Errors: {errors}")
    print(f"Saved to: {output_file}")
    print("\nPreview:")
    print(df.head(10).to_string(index=False))

    print("\nMissing values:")
    print(df.isna().sum())

else:
    print("No records extracted. Check the source folder structure.")
