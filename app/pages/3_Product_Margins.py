import streamlit as st
from streamlit_app import run_query

st.header("Product Margin Analysis")

query = """
SELECT
    p.category,
    SUM(oi.item_price * oi.quantity) AS revenue,
    SUM(p.unit_cost * oi.quantity) AS cost,
    SUM(oi.item_price * oi.quantity) - SUM(p.unit_cost * oi.quantity) AS profit
FROM raw.order_items oi
JOIN raw.products p ON oi.product_id = p.product_id
GROUP BY p.category;
"""

df = run_query(query)

st.bar_chart(df.set_index("category")[["revenue", "profit"]])
