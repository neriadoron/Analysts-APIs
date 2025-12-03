
import os
from datetime import datetime
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27020")

client = MongoClient(MONGO_URI)
db = client["workshop"]
orders_collection = db["orders"]

app = Flask(__name__)


def parse_date(value: str | None):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


def mongo_projection_from_fields(fields_param: str | None):
    if not fields_param:
        return None
    fields = [f.strip() for f in fields_param.split(",") if f.strip()]
    if not fields:
        return None
    # Always keep _id unless explicitly removed, but we'll strip it in response
    return {field: 1 for field in fields}


def serialize_order(doc):
    if not doc:
        return None
    doc = dict(doc)
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


# --------------- BROKEN ENDPOINTS (for students to diagnose) -----------------


@app.get("/broken/orders")
def broken_get_all_orders():
    """Return ALL orders with no pagination, no filters, no projection."""
    docs = list(orders_collection.find({}))
    return jsonify({
        "count": len(docs),
        "items": [serialize_order(d) for d in docs]
    })


@app.get("/broken/orders/by-customer/<int:customer_id>")
def broken_get_orders_by_customer(customer_id: int):
    """Naive implementation: no pagination, no projection."""
    docs = list(orders_collection.find({"customer_id": customer_id}))
    return jsonify({
        "count": len(docs),
        "items": [serialize_order(d) for d in docs]
    })


@app.get("/broken/orders/search")
def broken_search_orders():
    """
    Naive search endpoint.
    Query params: country, date_from, date_to (ISO format)
    - No pagination
    - No projection
    - No input validation
    """
    country = request.args.get("country")
    date_from_raw = request.args.get("date_from")
    date_to_raw = request.args.get("date_to")

    query = {}

    if country:
        query["country"] = country

    if date_from_raw or date_to_raw:
        date_filter = {}
        if date_from_raw:
            date_filter["$gte"] = parse_date(date_from_raw)
        if date_to_raw:
            date_filter["$lte"] = parse_date(date_to_raw)
        if date_filter:
            query["order_date"] = date_filter

    docs = list(orders_collection.find(query))
    return jsonify({
        "count": len(docs),
        "items": [serialize_order(d) for d in docs]
    })


# --------------- FIXED ENDPOINTS (students implement during workshop) -------


@app.get("/fixed/orders")
def fixed_get_orders():
    """
    TODO (students):
    - Implement pagination using page & page_size query params
    - Add optional sorting (e.g. by order_date desc)
    - Use a projection if `fields` query param is provided
    - Return:
      {
        "page": ...,
        "page_size": ...,
        "items": [...],
        "next_page": ... or null
      }
    """


@app.get("/fixed/orders/by-customer/<int:customer_id>")
def fixed_get_orders_by_customer(customer_id: int):
    """
    TODO (students):
    - Same idea as /fixed/orders but filtered by customer_id
    - Add pagination + projection
    """


@app.get("/fixed/orders/search")
def fixed_search_orders():
    """
    TODO (students):
    - Implement filtered & paginated search.
    - Query params: country, date_from, date_to, page, page_size, fields
    - Use the same helper functions as above.
    """


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
