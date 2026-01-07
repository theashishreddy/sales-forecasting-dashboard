import sqlite3
import pandas as pd
import os

def load_sales_data():
    # Absolute path to sales.db
    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "database", "sales.db")

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()

    return df
