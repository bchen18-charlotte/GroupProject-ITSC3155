from fastapi.testclient import TestClient
from ..main import app
from ..dependencies.database import get_db
from ..models import customers as model

#THe test client that we will use to test.
client = TestClient(app)

#gotta delete the old tests so that duplicates aren't created ...
def delete_customer_by_email(email):
    db = next(get_db())

    customer = db.query(model.Customer).filter(
        model.Customer.email == email
    ).first()

    if customer:
        db.delete(customer)
        db.commit()

    db.close()

""" 
This test creates a new customer.
sends a post request to /customers/ with a payload, then verifies status is 201 and verifies data matches
"""
def test_create_customer():
    # Create a customer payload
    payload = {
        "name": "John Doe",
        "email": "john.doe.test1@gmail.com",
        "phone": "123-456-7890",
        "address": "123 Main St, Anytown, USA"
    }

    #remove
    delete_customer_by_email(payload["email"])

    #post request to create the customer
    response = client.post("/customers/", json=payload)

    # Check for successful creation (200)
    assert response.status_code == 200

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
        "email": "jane.doe.test1@gmail.com",
        "phone": "098-765-4321",
        "address": "456 Oak Ave, Somewhere, USA"
    }

    #remove
    delete_customer_by_email(payload["email"])

    response = client.post("/customers/", json=payload)
    assert response.status_code == 200

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

    customers = [
        {
            "name": "Alice Smith",
            "email": "alice.smith.test1@gmail.com",
            "phone": "111-222-3333",
            "address": "789 Pine St, Anytown, USA"
        },
        {
            "name": "Bob Johnson",
            "email": "bob.johnson.test1@gmail.com",
            "phone": "444-555-6666",
            "address": "321 Elm St, Somewhere, USA"
        }
    ]

    for customer in customers:
        # Remove old test data first
        delete_customer_by_email(customer["email"])

        response = client.post("/customers/", json=customer)

        assert response.status_code == 200

    response = client.get("/customers/")

    assert response.status_code == 200

    data = response.json()
    names = [customer["name"] for customer in data]

    assert "Alice Smith" in names
    assert "Bob Johnson" in names