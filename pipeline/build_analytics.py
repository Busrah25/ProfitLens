"""
build_analytics.py

Purpose
--------
Transforms raw transactional data into analytics-ready tables
and views used by the ProfitLens dashboard.

Why this matters
----------------
Analytics layers should be reproducible and independent
from the dashboard application.
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
# Build Analytics Views
# --------------------------------------------------
def build_customer_profit_view():
    """Create or refresh customer profitability analytics."""
    query = """
    CREATE OR REPLACE VIEW analytics.customer_profit_view AS
    SELECT
        customer_id,
        COUNT(order_id) AS total_orders,
        SUM(order_total) AS total_revenue,
        SUM(order_profit) AS total_profit,
        AVG(order_profit) AS avg_profit_per_order
    FROM analytics.order_profit_view
    GROUP BY customer_id;
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

# --------------------------------------------------
# Execution
# --------------------------------------------------
if __name__ == "__main__":
    build_customer_profit_view()
