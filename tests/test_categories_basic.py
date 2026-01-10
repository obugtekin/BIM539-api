import pytest
from fastapi.testclient import TestClient

def test_categories_create_and_delete(client):
    create_response = client.post(
        "/api/categories",
        json={
            "name": "Test Category",
            "description": "Test açıklama"
        }
    )
    assert create_response.status_code == 201
    category_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/categories/{category_id}")
    assert delete_response.status_code == 200
