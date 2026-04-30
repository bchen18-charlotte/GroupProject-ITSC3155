from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_create_order():
    payload = {
        "customer_name": "John Doe",
        "phone": "123-456-7890",
        "address": "123 Main St",
        "order_type": "pickup",
        "total_price": 9.99,
        "status": "pending"
    }

    response = client.post("/orders/", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["customer_name"] == payload["customer_name"]
    assert data["phone"] == payload["phone"]
    assert data["address"] == payload["address"]
    assert data["order_type"] == payload["order_type"]
    assert data["total_price"] == payload["total_price"]
    assert data["status"] == payload["status"]