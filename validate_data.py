
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "data" / "processed" / "phonepe_transactions.csv"

df = pd.read_csv(INPUT_FILE)

print("=" * 50)
print("PHONEPE PULSE DATA VALIDATION")
print("=" * 50)

# 1. Dataset dimensions
print("\n1. Dataset shape:")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 2. Column data types
print("\n2. Data types:")
print(df.dtypes)

# 3. Missing values
print("\n3. Missing values:")
print(df.isna().sum())

# 4. Duplicate records
print("\n4. Duplicate rows:", df.duplicated().sum())

# 5. Year and quarter range
print("\n5. Year range:")
print(df["year"].min(), "to", df["year"].max())

print("\n6. Quarter values:")
print(sorted(df["quarter"].dropna().unique()))

# 6. Transaction count checks
print("\n7. Transaction count summary:")
print(df["transaction_count"].describe())

print(
    "\nNegative transaction counts:",
    (df["transaction_count"] < 0).sum()
)

# 7. Category breakdown
print("\n8. Transaction categories:")
print(df["transaction_type"].value_counts())

# 8. State breakdown
print("\n9. Number of state/path values:")
print(df["state"].nunique())

print("\nSample states:")
print(sorted(df["state"].dropna().unique())[:20])

# 9. Save a validation report
report_file = BASE_DIR / "reports" / "data_validation.txt"
report_file.parent.mkdir(parents=True, exist_ok=True)

with open(report_file, "w", encoding="utf-8") as f:
    f.write("PhonePe Pulse Data Validation Report\n\n")
    f.write(f"Rows: {df.shape[0]}\n")
    f.write(f"Columns: {df.shape[1]}\n")
    f.write(f"Duplicate rows: {df.duplicated().sum()}\n")
    f.write("\nMissing values:\n")
    f.write(df.isna().sum().to_string())
    f.write("\n\nData types:\n")
    f.write(df.dtypes.to_string())

print("\nValidation report saved:", report_file)
print("\nValidation complete!")
