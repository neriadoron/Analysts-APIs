
# Data API Design Workshop (MongoDB Edition)

This repo is for a hands-on session on **Data API Design for Analysts**.

You will:
- Run a local **MongoDB** instance (via Docker)
- Load sample **orders** data from CSV into MongoDB
- Call **broken** API endpoints
- Fix them by adding **pagination**, **filtering**, and **projections**
- Optionally add **indexes** and measure performance

---

## Prerequisites

- Docker + Docker Compose
- Python 3.10+
- `pip` (or `pipx` / venv if you prefer)

---

## 1. Start MongoDB (Docker)

From the repo root, run:

```bash
docker compose up -d
```

This will start:
- `mongo` on port **27020**

You can stop it later with:

```bash
docker compose down
```

---

## 2. Create virtualenv and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 3. Load sample data into MongoDB

This will:
- Read `data/orders.csv`
- Insert documents into the `workshop.orders` collection

```bash
python scripts/load_data.py
```

You can run it multiple times; it will clear the collection first.

---

## 4. Run the API

```bash
export MONGO_URI="mongodb://localhost:27020"  # Windows: set MONGO_URI=...
python app.py
```

The API will start on **http://localhost:5000**.

---

## 5. Broken endpoints (for the exercise)

These endpoints are intentionally **bad** and should be optimized.

- `GET /broken/orders`
  - Returns **all** orders (no pagination, no filters)
  - Heavy payload, slow for large datasets

- `GET /broken/orders/by-customer/<customer_id>`
  - No pagination, no projection
  - Scans the whole collection if no index

- `GET /broken/orders/search`
  - Query parameters: `country`, `date_from`, `date_to`
  - Implementation is naive and missing indexes

Your job in the workshop:

1. **Call** these endpoints and observe:
   - Response size
   - Response time
2. Implement **better versions** under `/fixed/...`:
   - Add **pagination**: `page`, `page_size`
   - Add **filtering**: `country`, `date_from`, `date_to`
   - Add **projection**: optional `fields` query parameter
3. (Optional) Add an index in Mongo:
   - On `customer_id`
   - On `order_date`
   - On `(country, order_date)`

---

## 6. Fixed endpoints (to implement during session)

In `app.py` you will find placeholders for:

- `GET /fixed/orders`
- `GET /fixed/orders/by-customer/<customer_id>`
- `GET /fixed/orders/search`

These should:
- Use **pagination** (`page`, `page_size`)
- Validate params (sane max page_size, defaults)
- Use **filtering** and **projection**
- Optionally rely on indexes (see `scripts/load_data.py:create_indexes()`)

---

## 7. Example calls

Broken:

```bash
curl "http://localhost:5000/broken/orders"
curl "http://localhost:5000/broken/orders/by-customer/42"
curl "http://localhost:5000/broken/orders/search?country=DE&date_from=2024-01-01&date_to=2024-01-31"
```

Fixed (to be implemented):

```bash
curl "http://localhost:5000/fixed/orders?page=1&page_size=50"
curl "http://localhost:5000/fixed/orders/by-customer/42?page=1&page_size=20&fields=order_id,total_amount,order_date"
curl "http://localhost:5000/fixed/orders/search?country=US&date_from=2024-01-01&date_to=2024-01-31&page=1&page_size=100"
```

---

## 8. Instructor Notes (idea)

- Timebox:
  - 10–15 min: clone, set up env, run Mongo + app
  - 10–15 min: call broken endpoints, discuss what feels wrong
  - 25–30 min: implement fixed endpoints in small groups
  - 10–15 min: share performance improvements and API designs
- Encourage students to:
  - Cap `page_size` (e.g. max 500)
  - Add default sorting (e.g. by `order_date desc`)
  - Think about query shapes before adding indexes

Enjoy breaking and fixing APIs 🚀
