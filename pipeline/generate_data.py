"""
generate_data.py

Purpose
--------
Generates synthetic business data for ProfitLens.
This simulates realistic operational datasets such as customers,
orders, products, and regions for analytics development and testing.

Why this matters
----------------
Real companies often prototype analytics pipelines using synthetic
or anonymized data before connecting to production systems.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --------------------------------------------------
# Configuration
# --------------------------------------------------
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 50
NUM_ORDERS = 3000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 1, 1)

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def random_date(start, end):
    """Generate a random date between two dates."""
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# --------------------------------------------------
# Data Generation
# --------------------------------------------------
def generate_customers():
    """Generate synthetic customer data."""
    return pd.DataFrame({
        "customer_id": range(1, NUM_CUSTOMERS + 1),
        "customer_segment": np.random.choice(
            ["Consumer", "Corporate", "SMB"], NUM_CUSTOMERS
        )
    })

def generate_products():
    """Generate synthetic product catalog data."""
    return pd.DataFrame({
        "product_id": range(1, NUM_PRODUCTS + 1),
        "category": np.random.choice(
            ["Electronics", "Furniture", "Office Supplies"], NUM_PRODUCTS
        ),
        "unit_cost": np.random.uniform(5, 200, NUM_PRODUCTS).round(2)
    })

def generate_orders():
    """Generate synthetic order header data."""
    return pd.DataFrame({
        "order_id": range(1, NUM_ORDERS + 1),
        "customer_id": np.random.randint(1, NUM_CUSTOMERS + 1, NUM_ORDERS),
        "order_date": [random_date(START_DATE, END_DATE) for _ in range(NUM_ORDERS)]
    })

# --------------------------------------------------
# Save Data to CSV
# --------------------------------------------------
if __name__ == "__main__":
    generate_customers().to_csv("data/customers.csv", index=False)
    generate_products().to_csv("data/products.csv", index=False)
    generate_orders().to_csv("data/orders.csv", index=False)
