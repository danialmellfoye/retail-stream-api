from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json, time, random, uuid, datetime

app = FastAPI()

products = [
    {"product_id": "P1001", "name": "Laptop"},
    {"product_id": "P1002", "name": "Phone"},
    {"product_id": "P1003", "name": "Keyboard"},
    {"product_id": "P1004", "name": "Headphones"},
    {"product_id": "P1005", "name": "Smartwatch"},
]

payment_types = ["CreditCard", "DebitCard", "Cash", "UPI"]

def generate_event():
    event_types = ["SALE", "RETURN", "RESTOCK"]

    # Initial stock for each product
    stock = {p["product_id"]: random.randint(10, 30) for p in products}

    while True:
        product = random.choice(products)
        product_id = product["product_id"]
        event_type = random.choices(event_types, weights=[0.7, 0.1, 0.2])[0]  # mostly sales
        current_stock = stock[product_id]

        if event_type == "SALE":
            if current_stock == 0:
                # Can't sell, skip or force RESTOCK
                event_type = "RESTOCK"
            else:
                quantity = -random.randint(1, min(5, current_stock))  # can't sell more than stock
                stock[product_id] += quantity  # quantity is negative, reduces stock

        elif event_type == "RESTOCK":
            quantity = random.randint(5, 20)
            stock[product_id] += quantity

        elif event_type == "RETURN":
            quantity = random.randint(1, 3)
            stock[product_id] += quantity

        event = {
            "transaction_id": str(uuid.uuid4()),
            "store_id": random.randint(100, 105),
            "product_id": product_id,
            "product_name": product["name"],
            "event_type": event_type,
            "quantity": quantity,
            "current_stock": stock[product_id],
            "price": round(random.uniform(100, 2000), 2),
            "payment_type": random.choice(payment_types),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        yield f""""data":{json.dumps(event)}\n\n"""
        time.sleep(5)  # emit one event per (n) second

@app.get("/stream")
def stream_data():
    return StreamingResponse(generate_event(), media_type="text/event-stream")

# Run with: python -m uvicorn stream_api:app --reload --port 8000
