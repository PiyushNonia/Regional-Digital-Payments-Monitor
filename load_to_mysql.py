
import pandas as pd
import mysql.connector
from pathlib import Path

csv_path = Path("data/processed/phonepe_state_transactions.csv")

if not csv_path.exists():
    raise FileNotFoundError(f"CSV not found: {csv_path.resolve()}")

df = pd.read_csv(csv_path)
print("CSV rows:", len(df))

password = input("Enter MySQL root password: ")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="regional_payments"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS phonepe_state_transactions (
    state VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    payment_instrument VARCHAR(30) NOT NULL,
    transaction_count BIGINT NOT NULL
)
""")

# Replace existing rows with the complete CSV
cursor.execute("TRUNCATE TABLE phonepe_state_transactions")

query = """
INSERT INTO phonepe_state_transactions
(state, year, quarter, transaction_type, payment_instrument, transaction_count)
VALUES (%s, %s, %s, %s, %s, %s)
"""

rows = [
    (
        str(r.state),
        int(r.year),
        int(r.quarter),
        str(r.transaction_type),
        str(r.payment_instrument),
        int(r.transaction_count)
    )
    for r in df.itertuples(index=False)
]

cursor.executemany(query, rows)
conn.commit()

cursor.execute("SELECT COUNT(*) FROM phonepe_state_transactions")
db_count = cursor.fetchone()[0]

print("Rows in MySQL:", db_count)

if db_count == len(df):
    print("SUCCESS: All rows imported correctly!")
else:
    print("WARNING: Row counts do not match.")

cursor.close()
conn.close()
