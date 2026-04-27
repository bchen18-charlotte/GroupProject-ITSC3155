from fastapi.testclient import TestClient
from ..main import app

#test client  
client = TestClient(app)

"""
test creates a new promotion.
create, check, verify
"""
def test_create_promotion():
    #create payload
    payload = {
        "code": "SAVE10",
        "discount_percent": 10,
        "expiration_date": "2026-12-31"
    }

    response = client.post("/promotions/", json=payload)

    #check for 201
    assert response.status_code == 201
    data = response.json()

    #verify 
    assert data["code"] == payload["code"] 
    assert data["discount_percent"] == payload["discount_percent"] 
    assert data["expiration_date"] == payload["expiration_date"]


"""
test retrieves a single promotion by ID.
create, get, verify 
"""
def test_get_promotion():
    #create 
    payload = {
        "code": "SAVE20",
        "discount_percent": 20, 
        "expiration_date": "2026-12-31" 
    }

    response = client.post("/promotions/", json=payload) 
    assert response.status_code == 201

    data = response.json()
    promotion_id = data["id"]

    #get
    response = client.get(f"/promotions/{promotion_id}")
    assert response.status_code == 200
    data = response.json()

    #veify 
    assert data["code"] == payload["code"]
    assert data["discount_percent"] == payload["discount_percent"] 
    assert data["expiration_date"] == payload["expiration_date"]


"""
test retrieves all promotions. 
create, get, verify
"""
def test_get_all_promotions():
    #create 
    promotions = [
        {
            "code": "SAVE30", 
            "discount_percent": 30, 
            "expiration_date": "2026-12-31"
        },
        {
            "code": "SAVE40",
            "discount_percent": 40, 
            "expiration_date": "2026-12-31"
        }
    ]

    for promotion in promotions:
        response = client.post("/promotions/", json=promotion)  
        assert response.status_code == 201

    #get 
    response = client.get("/promotions/") 

    #check for 200
    assert response.status_code == 200 
    data = response.json() 
    codes = [item["code"] for item in data]

    #chekc codes exits
    assert "SAVE30" in codes 
    assert "SAVE40" in codes