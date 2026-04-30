from fastapi.testclient import TestClient
from sqlalchemy import text
from ..main import app
from ..dependencies.database import get_db
from ..models import sandwiches as sandwich_model

#test client
client = TestClient(app)

def ensure_is_active_column():
    db = next(get_db())
    columns = db.execute(text("SHOW COLUMNS FROM menu_items")).fetchall()
    if not any(column[0] == "is_active" for column in columns):
        db.execute(text("ALTER TABLE menu_items ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT 1"))
        db.commit()

    db.close()
ensure_is_active_column()


"""
checks if our test sandwich already exists in the database  
If it exists reuse  
If it does not exist create it 
"""
def get_or_create_menu_item():
    sandwich_name = "Test Sandwich"
    #connect to database
    db = next(get_db())
    item = db.query(sandwich_model.MenuItem).filter(sandwich_model.MenuItem.sandwich_name == sandwich_name).first()

    if item:
        item_id = item.id
        db.close()
        return item_id

    db.close()
    #create
    payload = {
        "sandwich_name": sandwich_name,
        "description": "Test sandwich description",
        "price": 9.99,
        "calories": 500,
        "category": "Test"
    }

    #post
    response = client.post("/menuitems/", json=payload)
    #verify
    assert response.status_code == 200
    return response.json()["id"]

"""
creates a test order and then returns its ID.
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
test creating one order detail.
create, post, verify
"""
def test_create_order_detail():
    order_id = create_order()
    sandwich_id = get_or_create_menu_item()

    #create
    payload = {
        "order_id": order_id,
        "sandwich_id": sandwich_id,
        "amount": 2
    }
    #post
    response = client.post("/orderdetails/", json=payload)

    #verify
    assert response.status_code == 200
    data = response.json()
    #verify
    assert data["order_id"] == payload["order_id"]
    assert data["amount"] == payload["amount"]


"""
Test rretrieving one order detail by ID.
create, post, verify
"""
def test_get_order_detail():
    order_id = create_order()
    sandwich_id = get_or_create_menu_item()

    #create payload
    payload = {
        "order_id": order_id,
        "sandwich_id": sandwich_id,
        "amount": 3
    }
    #post
    response = client.post("/orderdetails/", json=payload)

    assert response.status_code == 200
    item_id = response.json()["id"]
    response = client.get(f"/orderdetails/{item_id}")

    #verify
    assert response.status_code == 200
    data = response.json()

    #verify
    assert data["order_id"] == payload["order_id"]
    assert data["amount"] == payload["amount"]


"""
test retrieving all order details.
create, post, and then verify
"""
def test_get_all_order_details():
    order_id = create_order()
    sandwich_id = get_or_create_menu_item()

    #create
    items = [
        {"order_id": order_id, "sandwich_id": sandwich_id, "amount": 1},
        {"order_id": order_id, "sandwich_id": sandwich_id, "amount": 5}
    ]

    #post
    for item in items:
        response = client.post("/orderdetails/", json=item)

        assert response.status_code == 200

    response = client.get("/orderdetails/")

    #verify
    assert response.status_code == 200

    data = response.json()
    amounts = [item["amount"] for item in data]

    #verify
    assert 1 in amounts
    assert 5 in amounts