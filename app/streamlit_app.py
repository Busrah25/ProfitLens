import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# --------------------------------------------------
# Application Configuration
# Loads environment variables and sets Streamlit layout
# --------------------------------------------------
load_dotenv()

st.set_page_config(
    page_title="ProfitLens",
    layout="wide"
)

# --------------------------------------------------
# Database Connection Utilities
# Uses a cached PostgreSQL connection for performance
# --------------------------------------------------
@st.cache_resource
d@st.cache_resource
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )


def run_query(query):
    """
    Executes a SQL query against PostgreSQL
    and returns the results as a Pandas DataFrame.
    """
    conn = get_connection()
    return pd.read_sql(query, conn)

# --------------------------------------------------
# Sidebar Filters
# Global date filter shared across all dashboard pages
# --------------------------------------------------
st.sidebar.header("Filters")

# Determine the valid date range from order data
date_query = """
SELECT MIN(order_date) AS min_date, MAX(order_date) AS max_date
FROM raw.orders;
"""
dates = run_query(date_query)

# Date range selector for filtering analytics views
start_date, end_date = st.sidebar.date_input(
    "Order Date Range",
    value=(dates["min_date"][0], dates["max_date"][0])
)

# Global SQL filter clause
# NOTE: Uses explicit table alias (o) to avoid SQL ambiguity
FILTER_CLAUSE = f"""
WHERE o.order_date BETWEEN '{start_date}' AND '{end_date}'
"""

# --------------------------------------------------
# Main Dashboard Header
# --------------------------------------------------
st.title("ProfitLens Executive Dashboard")
st.caption("Customer Profitability and Demand Intelligence System")
