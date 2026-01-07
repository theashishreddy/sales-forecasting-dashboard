import sqlite3
import pandas as pd

data = {
    "date": pd.date_range("2023-01-01", periods=100),
    "product_id": ["P001"] * 100,
    "region": ["South"] * 100,
    "price": [500] * 100,
    "units_sold": [20 + i % 10 for i in range(100)],
    "promotion": [1 if i % 15 == 0 else 0 for i in range(100)],
    "discount": [10 if i % 15 == 0 else 0 for i in range(100)],
    "sentiment": [0.5 + (i % 5) * 0.1 for i in range(100)]
}

df = pd.DataFrame(data)
df["revenue"] = df["price"] * df["units_sold"]

conn = sqlite3.connect("sales.db")
df.to_sql("sales", conn, if_exists="append", index=False)
conn.close()

print("Sample data inserted")
