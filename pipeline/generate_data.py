import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

fake = Faker()

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 120
NUM_ORDERS = 3000

def generate_customers():
    data = []
    for _ in range(NUM_CUSTOMERS):
        data.append({
            "customer_id": uuid.uuid4(),
            "first_order_date": fake.date_between(start_date="-2y", end_date="-6m"),
            "acquisition_channel": random.choice(["ads", "organic", "referral"]),
            "customer_segment": random.choice(["consumer", "small_business"])
        })
    return pd.DataFrame(data)

def generate_products():
    categories = {
        "electronics": (50, 300),
        "home": (10, 80),
        "essentials": (5, 40)
    }

    data = []
    for _ in range(NUM_PRODUCTS):
        category = random.choice(list(categories.keys()))
        cost_range = categories[category]

        unit_cost = round(random.uniform(*cost_range), 2)
        price = round(unit_cost * random.uniform(1.3, 1.8), 2)

        data.append({
            "product_id": uuid.uuid4(),
            "category": category,
            "base_price": price,
            "unit_cost": unit_cost,
            "weight_class": random.choice(["light", "medium", "heavy"])
        })
    return pd.DataFrame(data)

def generate_regions():
    regions = ["Midwest", "Northeast", "South", "West"]
    return pd.DataFrame([{
        "region_id": uuid.uuid4(),
        "region_name": r
    } for r in regions])

def generate_orders(customers, regions):
    data = []
    for _ in range(NUM_ORDERS):
        data.append({
            "order_id": uuid.uuid4(),
            "customer_id": random.choice(customers["customer_id"]),
            "region_id": random.choice(regions["region_id"]),
            "order_date": fake.date_between(start_date="-1y", end_date="today"),
            "shipping_speed": random.choice(["standard", "express"]),
            "discount_rate": random.choice([0, 0.05, 0.10])
        })
    return pd.DataFrame(data)

def generate_order_items(orders, products):
    data = []
    for _, order in orders.iterrows():
        for _ in range(random.randint(1, 4)):
            product = products.sample(1).iloc[0]
            data.append({
                "order_item_id": uuid.uuid4(),
                "order_id": order["order_id"],
                "product_id": product["product_id"],
                "quantity": random.randint(1, 3),
                "item_price": product["base_price"]
            })
    return pd.DataFrame(data)

def main():
    customers = generate_customers()
    products = generate_products()
    regions = generate_regions()
    orders = generate_orders(customers, regions)
    order_items = generate_order_items(orders, products)

    customers.to_csv("data/customers.csv", index=False)
    products.to_csv("data/products.csv", index=False)
    regions.to_csv("data/regions.csv", index=False)
    orders.to_csv("data/orders.csv", index=False)
    order_items.to_csv("data/order_items.csv", index=False)

    print("Synthetic data generated successfully")

if __name__ == "__main__":
    main()
