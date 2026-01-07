import streamlit as st
from streamlit_app import run_query

st.header("Regional Performance")

query = """
SELECT
    r.region_name,
    SUM(op.gross_revenue) AS revenue,
    SUM(op.gross_profit) AS profit
FROM analytics.order_profit_view op
JOIN raw.regions r ON op.region_id = r.region_id
GROUP BY r.region_name;
"""

df = run_query(query)

st.dataframe(df, use_container_width=True)
