import sqlite3

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    product_id TEXT,
    region TEXT,
    price REAL,
    units_sold INTEGER,
    revenue REAL,
    promotion INTEGER,
    discount REAL,
    sentiment REAL
)
""")

conn.commit()
conn.close()

print("Database initialized successfully")
