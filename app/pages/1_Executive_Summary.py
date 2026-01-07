import streamlit as st
from streamlit_app import run_query, FILTER_CLAUSE

st.header("Executive Summary")
st.caption(
    "High-level view of revenue, profitability, and customer activity for the selected period."
)

query = f"""
SELECT
    SUM(cp.total_revenue) AS revenue,
    SUM(cp.total_profit) AS profit,
    COUNT(DISTINCT cp.customer_id) AS customers
FROM analytics.customer_profit_view cp
JOIN raw.orders o
    ON cp.customer_id = o.customer_id
{FILTER_CLAUSE};
"""

df = run_query(query)

revenue = df["revenue"][0] or 0
profit = df["profit"][0] or 0
customers = df["customers"][0] or 0

margin_pct = (profit / revenue * 100) if revenue > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${revenue:,.0f}")
col2.metric("Total Profit", f"${profit:,.0f}")
col3.metric("Contribution Margin", f"{margin_pct:.1f}%")
col4.metric("Active Customers", int(customers))
