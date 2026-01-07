"""
quality_checks.py

Purpose
--------
Runs basic data validation checks on raw and analytics tables.

Why this matters
----------------
Data quality checks catch issues early and improve trust
in dashboards and business decisions.
"""

import psycopg2
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
# Quality Checks
# --------------------------------------------------
def check_row_counts():
    """Verify that raw tables contain data."""
    conn = get_connection()
    cursor = conn.cursor()

    tables = ["customers", "products", "orders"]
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM raw.{table}")
        count = cursor.fetchone()[0]
        print(f"{table} row count:", count)

    cursor.close()
    conn.close()

# --------------------------------------------------
# Execution
# --------------------------------------------------
if __name__ == "__main__":
    check_row_counts()
