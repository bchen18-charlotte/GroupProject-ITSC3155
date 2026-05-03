from fastapi.testclient import TestClient
from FinalProject.api.main import app
import time

client = TestClient(app)

#create resource helper
def create_resource():
    payload = {
        "item": f"Flour_{int(time.time() * 1000)}",  # avoids UNIQUE constraint failure
        "amount": 2.0,  # safer for DECIMAL columns
        "unit": "kg"
    }

    response = client.post("/ingredients/", json=payload)

    assert response.status_code in [200, 201]

    data = response.json()
    assert "id" in data

    return data["id"]

#create a resource
def test_create_resource():
    create_resource()


#read one resource
def test_get_resource():
    resource_id = create_resource()

    response = client.get(f"/ingredients/{resource_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == resource_id


#read all resources
def test_get_all_resources():
    create_resource()

    response = client.get("/ingredients/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


#update a resource
def test_update_resource():
    resource_id = create_resource()

    payload = {
        "amount": 10.0
    }

    response = client.put(f"/ingredients/{resource_id}", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["amount"] == 10.0


#delete a resource
def test_delete_resource():
    resource_id = create_resource()

    response = client.delete(f"/ingredients/{resource_id}")

    assert response.status_code in [200, 204]

    #test deletion
    response = client.get(f"/ingredients/{resource_id}")
    assert response.status_code == 404