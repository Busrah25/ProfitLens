"""
load_raw.py

Purpose
--------
Loads raw CSV files into the PostgreSQL raw schema.
This represents the ingestion step of the data pipeline.

Why this matters
----------------
Separating raw ingestion from analytics logic is a
best practice in data engineering.
"""

import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# Database Connection
# --------------------------------------------------
def get_connection():
    """Create a PostgreSQL connection."""
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost",
        port=5433
    )

# --------------------------------------------------
# Load CSV into Database
# --------------------------------------------------
def load_csv(table_name, file_path):
    """
    Loads a CSV file into a raw schema table.
    """
    df = pd.read_csv(file_path)
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        placeholders = ",".join(["%s"] * len(row))
        query = f"INSERT INTO raw.{table_name} VALUES ({placeholders})"
        cursor.execute(query, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()

# --------------------------------------------------
# Execution
# --------------------------------------------------
if __name__ == "__main__":
    load_csv("customers", "data/customers.csv")
    load_csv("products", "data/products.csv")
    load_csv("orders", "data/orders.csv")
