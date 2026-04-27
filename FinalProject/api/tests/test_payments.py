from fastapi.testclient import TestClient
from ..main import app

#test client creation 
client = TestClient(app)


"""
test creates a new payment. 
create, check, verify
"""
def test_create_payment():
    #create payload
    payload = {
        "order_id": 1,
        "payment_type": "card",
        "card_last_four": "1234",
        "card_holder_name": "John Doe"
    }

    response = client.post("/payments/", json=payload) 

    #success? 201
    assert response.status_code == 201

    data = response.json()

    #verify
    assert data["order_id"] == payload["order_id"] 
    assert data["payment_type"] == payload["payment_type"] 
    assert data["card_last_four"] == payload["card_last_four"]
    assert data["card_holder_name"] == payload["card_holder_name"]


"""
test retrieves a single payment by ID.
create, get and then verify. 
"""
def test_get_payment():
    #create
    payload = {
        "order_id": 1,
        "payment_type": "card", 
        "card_last_four": "5678",
        "card_holder_name": "Jane Doe"
    }

    response = client.post("/payments/", json=payload)
    assert response.status_code == 201 

    data = response.json()
    payment_id = data["id"]

    #get
    response = client.get(f"/payments/{payment_id}")

    #success? 200
    assert response.status_code == 200

    data = response.json()

    #verify
    assert data["order_id"] == payload["order_id"]
    assert data["payment_type"] == payload["payment_type"] 
    assert data["card_last_four"] == payload["card_last_four"]
    assert data["card_holder_name"] == payload["card_holder_name"]


"""
test retrieves all payments.
create,get and then verify as usual
"""
def test_get_all_payments():
    #create multiple payments
    payments = [
        {
            "order_id": 1,
            "payment_type": "card",
            "card_last_four": "1111", 
            "card_holder_name": "Alice Smith"
        },
        {
            "order_id": 1,
            "payment_type": "card",
            "card_last_four": "2222",
            "card_holder_name": "Bob Johnson"
        }
    ]

    for payment in payments: 
        response = client.post("/payments/", json=payment)
        assert response.status_code == 201

    #Get
    response = client.get("/payments/")

    #Check 200
    assert response.status_code == 200 
 
    data = response.json() 

    last_fours = [item["card_last_four"] for item in data]

    #Verify both payments are present
    assert "1111" in last_fours 
    assert "2222" in last_fours 