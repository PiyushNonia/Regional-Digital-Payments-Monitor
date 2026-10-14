
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed"
    / "phonepe_transactions.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

# Standardize text fields
df["state"] = (
    df["state"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df["transaction_type"] = (
    df["transaction_type"]
    .astype(str)
    .str.strip()
)

df["payment_instrument"] = (
    df["payment_instrument"]
    .astype(str)
    .str.strip()
)

# Validate year and quarter
df = df[
    df["year"].between(2018, 2026)
    & df["quarter"].between(1, 4)
].copy()

# Keep national and state-level data separate
india_df = df[df["state"] == "india"].copy()
state_df = df[df["state"] != "india"].copy()

# Convert state slugs to readable names
def readable_state(value):
    special_names = {
        "andaman-&-nicobar-islands": "Andaman & Nicobar Islands",
        "dadra-&-nagar-haveli-&-daman-&-diu":
            "Dadra & Nagar Haveli & Daman & Diu",
        "jammu-&-kashmir": "Jammu & Kashmir",
        "andhra-pradesh": "Andhra Pradesh",
        "arunachal-pradesh": "Arunachal Pradesh",
        "madhya-pradesh": "Madhya Pradesh",
        "tamil-nadu": "Tamil Nadu",
        "uttar-pradesh": "Uttar Pradesh",
        "west-bengal": "West Bengal"
    }

    if value in special_names:
        return special_names[value]

    return value.replace("-", " ").title()


state_df["state"] = state_df["state"].apply(readable_state)
india_df["state"] = "India"

# Sort records for analysis
sort_columns = ["year", "quarter", "state", "transaction_type"]

state_df = state_df.sort_values(sort_columns)
india_df = india_df.sort_values(sort_columns)

# Save separate files
state_file = OUTPUT_DIR / "phonepe_state_transactions.csv"
india_file = OUTPUT_DIR / "phonepe_india_transactions.csv"

state_df.to_csv(state_file, index=False)
india_df.to_csv(india_file, index=False)

print("CLEANING COMPLETE")
print("-" * 40)

print("\nState-level data:")
print("Rows:", len(state_df))
print("States:", state_df["state"].nunique())
print("Saved:", state_file)

print("\nIndia-level data:")
print("Rows:", len(india_df))
print("Saved:", india_file)

print("\nState-level preview:")
print(state_df.head(10).to_string(index=False))

print("\nMissing values after cleaning:")
print(state_df.isna().sum())

print("\nDuplicate rows after cleaning:")
print(state_df.duplicated().sum())
