from fastapi.testclient import TestClient
from ..main import app

#Test client 
client = TestClient(app)

"""
This test creates a new order detail.
sends post request to /order-details/ with a payload,
then verifies: Status code is 201 and returned data matches input
"""
def test_create_order_detail():
    # Define payload (make sure these IDs exist in your DB)
    payload = {
        "order_id": 1,
        "sandwich_id": 1,
        "amount": 2
    }
 
    #post request
    response = client.post("/order-details/", json=payload)

    #check success
    assert response.status_code == 201

    #check data
    data = response.json()

    #Verify  values
    assert data["order_id"] == payload["order_id"]
    assert data["sandwich_id"] == payload["sandwich_id"]
    assert data["amount"] == payload["amount"]


"""
test retrieves a single order detail by ID.
Steps: create, check ID, verify
"""
def test_get_order_detail():
    # Create an order
    payload = {
        "order_id": 1,
        "sandwich_id": 1,
        "amount": 3
    }

    response = client.post("/order-details/", json=payload)
    assert response.status_code == 201 

    data = response.json()
    item_id = data["id"]

    #retireve order
    response = client.get(f"/order-details/{item_id}")

    #Check
    assert response.status_code == 200 

    data = response.json()

    #Verify
    assert data["order_id"] == payload["order_id"]
    assert data["sandwich_id"] == payload["sandwich_id"]
    assert data["amount"] == payload["amount"]


"""
Test retrieves all order details.
create, get order, then verify 
"""
def test_get_all_order_details():
    #multiple order detailss
    items = [
        {"order_id": 1, "sandwich_id": 1, "amount": 1},
        {"order_id": 1, "sandwich_id": 1, "amount": 5}
    ]

    #Create 
    for item in items:
        response = client.post("/order-details/", json=item)
        assert response.status_code == 201

    response = client.get("/order-details/")  

    #success?
    assert response.status_code == 200

    data = response.json() 

    amounts = [item["amount"] for item in data]

   #check created exists
    assert 1 in amounts
    assert 5 in amounts