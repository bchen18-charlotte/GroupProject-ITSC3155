from fastapi.testclient import TestClient
from FinalProject.api.main import app
import time

client = TestClient(app)
#create review helper
def create_review():
    payload = {
        "customer_id": 1,
        "order_id": 1,
        "score": 5,
        "review_text": f"Great!_{int(time.time() * 1000)}"
    }

    response = client.post("/reviews/", json=payload)

    assert response.status_code in [200, 201]

    data = response.json()
    assert "id" in data

    return data["id"]


#create a review
def test_create_review():
    create_review()


#test read one review
def test_get_review():
    review_id = create_review()

    response = client.get(f"/reviews/{review_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == review_id


#test read all reviews
def test_get_all_reviews():
    create_review()

    response = client.get("/reviews/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


#test update review
def test_update_review():
    review_id = create_review()

    payload = {
        "score": 4,
        "review_text": "Updated review"
    }

    response = client.put(f"/reviews/{review_id}", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["score"] == 4


#test delete review
def test_delete_review():
    review_id = create_review()

    response = client.delete(f"/reviews/{review_id}")

    assert response.status_code in [200, 204]

    #confirm deletion
    response = client.get(f"/reviews/{review_id}")
    assert response.status_code == 404