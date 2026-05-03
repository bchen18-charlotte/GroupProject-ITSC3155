from fastapi.testclient import TestClient
from sqlalchemy import text
from ..main import app
from ..dependencies.database import get_db
from ..models import promotions as promotion_model

#test client
client = TestClient(app)

def ensure_start_date_column():
    db = next(get_db())
    columns = db.execute(text("SHOW COLUMNS FROM promotions")).fetchall()
    if not any(column[0] == "start_date" for column in columns):
        db.execute(
            text("ALTER TABLE promotions ADD COLUMN start_date DATETIME NULL")
        )
        db.commit()
    db.close()
"""
deletes promo if it exists already 
"""
def delete_promotion_by_code(code):
    ensure_start_date_column()

    #db
    db = next(get_db())
    #follow same logic as previous
    promotion = db.query(promotion_model.Promotion).filter(
        promotion_model.Promotion.code == code
    ).first()

    #if found delete
    if promotion:
        db.delete(promotion)
        db.commit()
    db.close()

"""
test creating a promo 
create, delete, post, verify  
"""
def test_create_promotion():
    ensure_start_date_column()
    # create
    payload = {
        "code": "SAVE10",
        "discount_percent": 10,
        "expiration_date": "2026-12-31"
    }

    #remove old code
    delete_promotion_by_code(payload["code"])
    #post
    response = client.post("/promotions/", json=payload)

    #verify
    assert response.status_code == 200
    data = response.json()
    #verify
    assert data["code"] == payload["code"]
    assert data["discount_percent"] == payload["discount_percent"]
    assert data["expiration_date"][:10] == payload["expiration_date"]

"""
test getting a promo
create, delete duplicates, get, and verify 
"""
def test_get_promotion():
    ensure_start_date_column()
    # create
    payload = {
        "code": "SAVE20",
        "discount_percent": 20,
        "expiration_date": "2026-12-31"
    }
    #remove
    delete_promotion_by_code(payload["code"])

    #post
    response = client.post("/promotions/", json=payload)

    #verify
    assert response.status_code == 200
    promotion_id = response.json()["id"]
    #get
    response = client.get(f"/promotions/{promotion_id}")

    #verify
    assert response.status_code == 200
    data = response.json()
    #verify
    assert data["code"] == payload["code"]
    assert data["discount_percent"] == payload["discount_percent"]
    assert data["expiration_date"][:10] == payload["expiration_date"]

"""
test getting all promotions.  
create, delete duplicates, get, and verify 
"""
def test_get_all_promotions():
    ensure_start_date_column()
    #create promos
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
        #delete
        delete_promotion_by_code(promotion["code"])
        response = client.post("/promotions/", json=promotion)
        #verify
        assert response.status_code == 200

    #get
    response = client.get("/promotions/")

    #verify
    assert response.status_code == 200
    data = response.json()
    codes = [item["code"] for item in data]

    #verify
    assert "SAVE30" in codes
    assert "SAVE40" in codes