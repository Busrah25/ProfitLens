import streamlit as st
from streamlit_app import run_query

st.header("Executive Summary")

query = """
SELECT
    SUM(total_revenue) AS revenue,
    SUM(total_profit) AS profit,
    COUNT(customer_id) AS customers
FROM analytics.customer_profit_view;
"""

df = run_query(query)

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${df['revenue'][0]:,.0f}")
col2.metric("Total Profit", f"${df['profit'][0]:,.0f}")
col3.metric("Active Customers", int(df['customers'][0]))
