import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# ---------------------------------
# App Configuration
# ---------------------------------
load_dotenv()

st.set_page_config(page_title="ProfitLens", layout="wide")

# ---------------------------------
# Database Connection
# ---------------------------------
@st.cache_resource
def get_connection():
    """
    Create and cache a database connection.

    Local dev uses .env (Docker Postgres on localhost).
    Streamlit Cloud uses st.secrets (Neon hosted Postgres).
    """
    # Prefer Streamlit Secrets when deployed
    if "db" in st.secrets:
        cfg = st.secrets["db"]
        return psycopg2.connect(
            dbname=cfg["name"],
            user=cfg["user"],
            password=cfg["password"],
            host=cfg["host"],
            port=int(cfg.get("port", 5432)),
            sslmode=cfg.get("sslmode", "require"),
        )

    # Fallback for local development
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5433")),
    )

def run_query(query: str) -> pd.DataFrame:
    """
    Run a SQL query and return a DataFrame.
    """
    conn = get_connection()
    return pd.read_sql(query, conn)

# ---------------------------------
# Sidebar Filters
# ---------------------------------
st.sidebar.header("Filters")

date_query = """
SELECT MIN(order_date) AS min_date, MAX(order_date) AS max_date
FROM raw.orders;
"""
dates = run_query(date_query)

min_date = dates["min_date"].iloc[0]
max_date = dates["max_date"].iloc[0]

# Stop app cleanly if no data
if min_date is None or max_date is None:
    st.error("No order data available.")
    st.stop()

# Convert to Python date objects (required by Streamlit Cloud)
min_date = min_date.date() if hasattr(min_date, "date") else dt.date.fromisoformat(str(min_date))
max_date = max_date.date() if hasattr(max_date, "date") else dt.date.fromisoformat(str(max_date))

start_date, end_date = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# This clause assumes queries join raw.orders as alias o
FILTER_CLAUSE = f"""
WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}'
"""

# ---------------------------------
# Main Header
# ---------------------------------
st.title("ProfitLens Executive Dashboard")
st.caption("Customer Profitability and Demand Intelligence System")

st.sidebar.success("Secrets loaded")
st.sidebar.write("DB secrets present:", "db" in st.secrets)
