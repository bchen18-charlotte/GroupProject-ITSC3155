from fastapi.testclient import TestClient
from ..main import app

#THe test client that we will use to test.
client = TestClient(app)

""" 
This test creates a new customer.
sends a post request to /customers/ with a payload, then verifies status is 201 and verifies data matches
"""
def test_create_customer():
    # Create a customer payload
    payload = {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
        "phone": "123-456-7890",
        "address": "123 Main St, Anytown, USA" 
    }  

    #post request to create the customer
    response = client.post("/customers/", json=payload)

    # Check for successful creation (201)
    assert response.status_code == 201

    #check response data
    data = response.json()

    #verify 
    assert data["name"] == payload["name"] 
    assert data["email"] == payload["email"]
    assert data["phone"] == payload["phone"]
    assert data["address"] == payload["address"]


"""
retrieves a single customer by ID.
create, get, then verify.  
"""
def test_get_customer():
    #create 
    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@gmail.com",
        "phone": "098-765-4321",
        "address": "456 Oak Ave, Somewhere, USA"
    }

    response = client.post("/customers/", json=payload)
    assert response.status_code == 201

    data = response.json()
    customer_id = data["id"]

    #get request
    response = client.get(f"/customers/{customer_id}")

    assert response.status_code == 200

    data = response.json()

    #verify
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["phone"] == payload["phone"]
    assert data["address"] == payload["address"]


"""
test retrieves all customers.
create, get, verify
"""
def test_get_all_customers():
    #customer data
    customers = [
        {
            "name": "Alice Smith",
            "email": "alice.smith@gmail.com",
            "phone": "111-222-3333",
            "address": "789 Pine St, Anytown, USA"
        },
        {
            "name": "Bob Johnson",
            "email": "bob.johnson@gmail.com",
            "phone": "444-555-6666",
            "address": "321 Elm St, Somewhere, USA"
        }
    ]

    #Create
    for customer in customers:
        response = client.post("/customers/", json=customer)
        assert response.status_code == 201

    response = client.get("/customers/")

    assert response.status_code == 200

    data = response.json()

    names = [customer["name"] for customer in data]

    #verify both customers are present
    assert "Alice Smith" in names
    assert "Bob Johnson" in names