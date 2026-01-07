import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# ---------------------------------
# App Configuration
# ---------------------------------
load_dotenv()

st.set_page_config(
    page_title="ProfitLens",
    layout="wide"
)

# ---------------------------------
# Database Configuration
# ---------------------------------
def get_db_config():
    """
    Returns database connection settings.

    Priority:
    1 Streamlit secrets (used on Streamlit Cloud)
    2 Environment variables (used locally with dotenv)
    """
    if "db" in st.secrets:
        cfg = st.secrets["db"]
        return {
            "host": cfg.get("host"),
            "port": int(cfg.get("port", 5432)),
            "dbname": cfg.get("name"),
            "user": cfg.get("user"),
            "password": cfg.get("password"),
            "sslmode": cfg.get("sslmode", "require"),
        }

    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5433")),
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "sslmode": os.getenv("POSTGRES_SSLMODE", "disable"),
    }

# ---------------------------------
# Database Connection
# ---------------------------------
@st.cache_resource
def get_connection():
    """
    Opens a single cached connection per session.
    Using sslmode=require for Neon in cloud.
    """
    cfg = get_db_config()

    return psycopg2.connect(
        host=cfg["host"],
        port=cfg["port"],
        dbname=cfg["dbname"],
        user=cfg["user"],
        password=cfg["password"],
        sslmode=cfg["sslmode"],
        connect_timeout=10
    )

def run_query(query: str) -> pd.DataFrame:
    """
    Executes SQL and returns a DataFrame.
    Shows a clean error in the UI if the database is unreachable.
    """
    try:
        conn = get_connection()
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error("Database connection failed. Check Streamlit Secrets and Neon connection details.")
        st.exception(e)
        return pd.DataFrame()

# ---------------------------------
# Sidebar Filters
# ---------------------------------
st.sidebar.header("Filters")

date_query = """
SELECT MIN(order_date) AS min_date, MAX(order_date) AS max_date
FROM raw.orders;
"""

dates = run_query(date_query)

if dates.empty or dates["min_date"][0] is None or dates["max_date"][0] is None:
    st.stop()

start_date, end_date = st.sidebar.date_input(
    "Order Date Range",
    value=(dates["min_date"][0], dates["max_date"][0])
)

# Used by pages that join raw.orders as alias o
FILTER_CLAUSE = f"""
WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}'
"""

# ---------------------------------
# Main Header
# ---------------------------------
st.title("ProfitLens Executive Dashboard")
st.caption("Customer Profitability and Demand Intelligence System")
