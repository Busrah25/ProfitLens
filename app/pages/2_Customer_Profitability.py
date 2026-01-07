import streamlit as st
from streamlit_app import run_query

# --------------------------------------------------
# Customer Profitability Page
# Displays top customers ranked by total profit
# --------------------------------------------------

# Page title for stakeholders
st.header("Customer Profitability")

# --------------------------------------------------
# SQL Query
# Retrieves customer-level profitability metrics
# Sorted by total profit to highlight highest-value customers
# --------------------------------------------------
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

# Execute query and load results into a DataFrame
df = run_query(query)

# --------------------------------------------------
# Display Results
# Uses a wide, scrollable table for easy comparison
# --------------------------------------------------
st.dataframe(
    df,
    use_container_width=True
)
