
import os
import csv
from datetime import datetime
from pymongo import MongoClient, ASCENDING

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27020")
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "orders.csv")


def load_orders():
    client = MongoClient(MONGO_URI)
    db = client["workshop"]
    collection = db["orders"]

    print(f"Connecting to Mongo at {MONGO_URI}...")
    print("Clearing existing documents in workshop.orders...")
    collection.delete_many({})

    docs = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            doc = {
                "order_id": int(row["order_id"]),
                "customer_id": int(row["customer_id"]),
                "order_date": datetime.fromisoformat(row["order_date"]),
                "country": row["country"],
                "total_amount": float(row["total_amount"]),
                "status": row["status"],
                "item_count": int(row["item_count"]),
            }
            docs.append(doc)

    if docs:
        print(f"Inserting {len(docs)} orders...")
        collection.insert_many(docs)
    else:
        print("No rows found in CSV.")

    print("Done.")


if __name__ == "__main__":
    load_orders()
