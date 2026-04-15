from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


"""This test is to create a new customer. It defines a payload with the customer's information, sends a POST request to the /customers/ endpoint, 
and asserts that the response status code is 201 (Created) and that the response contains the expected data."""
def test_create_customer():
    # Define the payload for creating a customer
    payload = {
        "name": "John Doe",
        "email": "john.doe@gmail.com",
        "phone": "123-456-7890",
        "address": "123 Main St, Anytown, USA"
    }

    # Send a POST request to create a new customer
    response = client.post("/customers/", json=payload)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert that the response contains the expected data
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["phone"] == payload["phone"]
    assert data["address"] == payload["address"]

"""This test is to get a customer by ID. It first creates a customer to ensure there is one to retrieve, 
then it sends a GET request to retrieve the customer and asserts that the response contains the expected data."""
def test_get_customer():
    # First, create a customer to ensure there is one to retrieve
    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@gmail.com",
        "phone": "098-765-4321",
        "address": "456 Oak Ave, Somewhere, USA"
    }

    # Send a POST request to create a new customer
    response = client.post("/customers/", json=payload)
    assert response.status_code == 201 
    data = response.json()

    # Retrieve the created customer
    customer_id = data["id"]
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["phone"] == payload["phone"]
    assert data["address"] == payload["address"]

    def test_get_all_customers():
        # Create 2 customers
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

        for customer in customers:
            response = client.post("/customers/", json=customer)
            assert response.status_code == 201

        # Retrieve all customers        response = client.get("/customers/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2  # Ensure at least 2 customers are returned
        # Check that the created customers are in the response
        names = [customer["name"] for customer in data]
        assert "Alice Smith" in names
        assert "Bob Johnson" in names


        