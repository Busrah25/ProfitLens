import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port=5433
)

def load_csv(table, path):
    df = pd.read_csv(path)
    cur = conn.cursor()

    for _, row in df.iterrows():
        cols = ",".join(df.columns)
        placeholders = ",".join(["%s"] * len(row))
        query = f"INSERT INTO raw.{table} ({cols}) VALUES ({placeholders})"
        cur.execute(query, tuple(row))

    conn.commit()

load_csv("customers", "data/customers.csv")
load_csv("products", "data/products.csv")
load_csv("regions", "data/regions.csv")
load_csv("orders", "data/orders.csv")
load_csv("order_items", "data/order_items.csv")

print("Data loaded into PostgreSQL")
