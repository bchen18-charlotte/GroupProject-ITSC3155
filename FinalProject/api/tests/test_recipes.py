from fastapi.testclient import TestClient
from FinalProject.api.main import app

client = TestClient(app)

#test create recipe
def test_create_recipe():
    payload = {
        "sandwich_id": 1,
        "resource_id": 1,
        "amount": 2
    }

    response = client.post("/recipes/", json=payload)

    assert response.status_code in [200, 201]
    data = response.json()
    assert data["amount"] == 2

#test get recipes
def test_get_recipe():
    create_payload = {
        "sandwich_id": 1,
        "resource_id": 1,
        "amount": 2
    }

    create_res = client.post("/recipes/", json=create_payload)
    assert create_res.status_code in [200, 201]

    recipe_id = create_res.json()["id"]

    res = client.get(f"/recipes/{recipe_id}")
    assert res.status_code == 200
    assert res.json()["id"] == recipe_id

#test read all recipes
def test_get_all_recipes():
    payload = {
        "sandwich_id": 1,
        "resource_id": 1,
        "amount": 2
    }

    client.post("/recipes/", json=payload)

    res = client.get("/recipes/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

#test update recipe
def test_update_recipe():
    payload = {
        "sandwich_id": 1,
        "resource_id": 1,
        "amount": 2
    }

    create_res = client.post("/recipes/", json=payload)
    recipe_id = create_res.json()["id"]

    update_payload = {
        "amount": 5
    }

    res = client.put(f"/recipes/{recipe_id}", json=update_payload)
    assert res.status_code == 200
    assert res.json()["amount"] == 5

#test delete recipe
def test_delete_recipe():
    payload = {
        "sandwich_id": 1,
        "resource_id": 1,
        "amount": 2
    }

    create_res = client.post("/recipes/", json=payload)
    recipe_id = create_res.json()["id"]

    res = client.delete(f"/recipes/{recipe_id}")
    assert res.status_code in [200, 204]