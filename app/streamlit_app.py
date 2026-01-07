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
# Database Connection
# ---------------------------------
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost",
        port=5433
    )

def run_query(query):
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

start_date, end_date = st.sidebar.date_input(
    "Order Date Range",
    value=(dates["min_date"][0], dates["max_date"][0])
)

FILTER_CLAUSE = f"""
WHERE order_date BETWEEN '{start_date}' AND '{end_date}'
"""

# ---------------------------------
# Main Header
# ---------------------------------
st.title("ProfitLens Executive Dashboard")
st.caption("Customer Profitability and Demand Intelligence System")
