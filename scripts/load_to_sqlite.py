"""Load the Olist CSVs from data/raw into data/olist.db (SQLite)."""
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
DB = ROOT / "data" / "olist.db"

TABLES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

with sqlite3.connect(DB) as conn:
    for table, filename in TABLES.items():
        # Dates are already ISO strings in the CSVs; not parsing them keeps them as text.
        df = pd.read_csv(RAW / filename)
        df.to_sql(table, conn, if_exists="replace", index=False)

    for table in TABLES:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table:<22}{count:>10,}")
