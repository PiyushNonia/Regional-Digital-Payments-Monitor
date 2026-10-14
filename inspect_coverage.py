
import pandas as pd
from pathlib import Path

file_path = (
    Path(__file__).parent
    / "data"
    / "processed"
    / "phonepe_transactions.csv"
)

df = pd.read_csv(file_path)

print("\n1. INDIA AGGREGATE ROWS")
print(df[df["state"].str.lower() == "india"].shape[0])

print("\n2. ROWS PER YEAR")
print(df.groupby("year").size().to_string())

print("\n3. AVAILABLE QUARTERS BY YEAR")
coverage = (
    df.groupby("year")["quarter"]
    .apply(lambda x: sorted(x.unique().tolist()))
)
print(coverage.to_string())

print("\n4. ROWS PER STATE")
print(
    df.groupby("state").size()
    .sort_values(ascending=False)
    .to_string()
)

print("\n5. CATEGORY COVERAGE")
print(
    df.groupby(["year", "quarter"])["transaction_type"]
    .nunique()
    .to_string()
)

print("\n6. PAYMENT INSTRUMENT TYPES")
print(df["payment_instrument"].value_counts().to_string())
