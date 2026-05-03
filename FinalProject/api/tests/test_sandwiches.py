from fastapi.testclient import TestClient
from FinalProject.api.main import app
import time

client = TestClient(app)


#create sandwich helper function
def create_sandwich():
    payload = {
        #time used as a workaround to avoid the UNIQUE constraint#
        #set in model for sandwiches.py
        "sandwich_name": f"Sandwich_{int(time.time() * 1000)}",
        "description": "Test sandwich",
        "price": 5.99,
        "calories": 500,
        "category": "Lunch",
        "is_active": True
    }

    response = client.post("/menuitems/", json=payload)

    assert response.status_code in [200, 201]

    data = response.json()
    assert "id" in data

    return data["id"]


#testing create
def test_create_sandwich():
    create_sandwich()


#test read one sandwich
def test_get_sandwich():
    sandwich_id = create_sandwich()

    response = client.get(f"/menuitems/{sandwich_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == sandwich_id


#test read all sandwiches
def test_get_all_sandwiches():
    create_sandwich()

    response = client.get("/menuitems/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


#test update sandwich
def test_update_sandwich():
    sandwich_id = create_sandwich()

    payload = {
        "price": 7.99,
        "category": "Dinner"
    }

    response = client.put(f"/menuitems/{sandwich_id}", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["price"] == 7.99

#test delete sandwich
def test_delete_sandwich():
    sandwich_id = create_sandwich()

    response = client.delete(f"/menuitems/{sandwich_id}")

    assert response.status_code in [200, 204]

    # confirm deletion
    response = client.get(f"/menuitems/{sandwich_id}")
    assert response.status_code == 404