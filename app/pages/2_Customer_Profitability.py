import streamlit as st
from streamlit_app import run_query

st.header("Customer Profitability")

query = """
SELECT
    customer_id,
    total_orders,
    total_revenue,
    total_profit,
    avg_profit_per_order
FROM analytics.customer_profit_view
ORDER BY total_profit DESC
LIMIT 20;
"""

df = run_query(query)

st.dataframe(df, use_container_width=True)
