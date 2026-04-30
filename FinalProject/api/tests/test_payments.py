from fastapi.testclient import TestClient
from ..main import app

#create cleint
client = TestClient(app)
"""
creates test order.
create, post, and then verify
"""
def create_order():
    #create
    payload = {
        "customer_name": "Test Customer",
        "phone": "123-456-7890",
        "address": "123 Test St",
        "order_type": "pickup",
        "total_price": 9.99,
        "status": "pending"
    }
    #post
    response = client.post("/orders/", json=payload)
    #verify
    assert response.status_code == 200
    return response.json()["id"]

"""
test one payment
create, and then verify all 
"""
def test_create_payment():
    order_id = create_order()
    #create payment
    payload = {
        "order_id": order_id,
        "payment_type": "credit_card",
        "card_last_four": "1234",
        "card_holder_name": "John Doe"
    }
    response = client.post("/payments/", json=payload)

    #verify
    assert response.status_code == 200
    data = response.json()

    #verify all
    assert data["order_id"] == payload["order_id"]
    assert data["payment_type"] == payload["payment_type"]
    assert data["card_last_four"] == payload["card_last_four"]
    assert data["card_holder_name"] == payload["card_holder_name"]


"""
Test retrieving one payment by ID.
create, verify, get, and verify all
"""
def test_get_payment():
    order_id = create_order()
    #create payment
    payload = {
        "order_id": order_id,
        "payment_type": "credit_card",
        "card_last_four": "5678",
        "card_holder_name": "Jane Doe"
    }
    response = client.post("/payments/", json=payload)

    #verify
    assert response.status_code == 200
    payment_id = response.json()["id"]

    #get
    response = client.get(f"/payments/{payment_id}")
    assert response.status_code == 200
    data = response.json()

    #verify
    assert data["order_id"] == payload["order_id"]
    assert data["payment_type"] == payload["payment_type"]
    assert data["card_last_four"] == payload["card_last_four"]
    assert data["card_holder_name"] == payload["card_holder_name"]


"""
test retrieving all payments.
create, get, and then verify all
"""
def test_get_all_payments():
    order_id = create_order()
    #create payments
    payments = [
        {
            "order_id": order_id,
            "payment_type": "credit_card",
            "card_last_four": "1111",
            "card_holder_name": "Alice Smith"
        },
        {
            "order_id": order_id,
            "payment_type": "credit_card",
            "card_last_four": "2222",
            "card_holder_name": "Bob Johnson"
        }
    ]

    for payment in payments:
        response = client.post("/payments/", json=payment)
        assert response.status_code == 200

    #get
    response = client.get("/payments/")

    #verify
    assert response.status_code == 200

    #data check
    data = response.json()
    last_fours = [item["card_last_four"] for item in data]

    #verify
    assert "1111" in last_fours
    assert "2222" in last_fours