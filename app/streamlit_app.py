import streamlit as st
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="ProfitLens",
    layout="wide"
)

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

st.title("ProfitLens Executive Dashboard")
st.caption("Customer Profitability and Demand Intelligence System")
