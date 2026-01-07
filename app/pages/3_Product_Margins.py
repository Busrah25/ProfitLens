import streamlit as st
from streamlit_app import run_query, FILTER_CLAUSE

st.header("Product Margin Analysis")
st.caption(
    "Evaluates revenue, cost, and margin performance by product category to identify profit drivers and margin leakage."
)

query = f"""
SELECT
    p.category,
    SUM(oi.item_price * oi.quantity) AS revenue,
    SUM(p.unit_cost * oi.quantity) AS cost,
    SUM(oi.item_price * oi.quantity) - SUM(p.unit_cost * oi.quantity) AS profit
FROM raw.order_items oi
JOIN raw.products p
    ON oi.product_id = p.product_id
JOIN raw.orders o
    ON oi.order_id = o.order_id
{FILTER_CLAUSE}
GROUP BY p.category
ORDER BY profit DESC;
"""

df = run_query(query)

# Defensive calculations
df["margin_pct"] = (df["profit"] / df["revenue"]) * 100
df = df.fillna(0)

# ------------------------------
# Revenue vs Profit
# ------------------------------
st.subheader("Revenue vs Profit by Category")
st.bar_chart(
    df.set_index("category")[["revenue", "profit"]],
    use_container_width=True
)

# ------------------------------
# Margin Insight
# ------------------------------
st.subheader("Contribution Margin by Category (%)")
st.bar_chart(
    df.set_index("category")[["margin_pct"]],
    use_container_width=True
)

# ------------------------------
# Insight Table
# ------------------------------
st.subheader("Category Performance Summary")
st.dataframe(
    df,
    use_container_width=True
)
