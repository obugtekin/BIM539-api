import pytest
from fastapi.testclient import TestClient

def test_create_user(client):
    response = client.post(
        "/api/users",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "phone": "555-1234"
        }
    )
    assert response.status_code == 201
    assert "id" in response.json()

def test_delete_user(client):
    create_response = client.post(
        "/api/users",
        json={
            "name": "Test User",
            "email": "test@example.com"
        }
    )
    user_id = create_response.json()["id"]
    
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200

def test_create_product(client):
    category_response = client.post(
        "/api/categories",
        json={"name": "Elektronik"}
    )
    category_id = category_response.json()["id"]
    
    response = client.post(
        "/api/products",
        json={
            "name": "Laptop",
            "price": 15000.00,
            "category_id": category_id
        }
    )
    assert response.status_code == 201

def test_create_order(client):
    user_response = client.post(
        "/api/users",
        json={
            "name": "Test User",
            "email": "test@example.com"
        }
    )
    user_id = user_response.json()["id"]
    
    response = client.post(
        "/api/orders",
        json={
            "user_id": user_id,
            "total_amount": 15000.00
        }
    )
    assert response.status_code == 201

def test_get_users(client):
    response = client.get("/api/users")
    assert response.status_code == 200

def test_create_category(client):
    response = client.post(
        "/api/categories",
        json={
            "name": "Test Kategori"
        }
    )
    assert response.status_code == 201

def test_get_categories(client):
    response = client.get("/api/categories")
    assert response.status_code == 200

def test_get_orders(client):
    response = client.get("/api/orders")
    assert response.status_code == 200

def test_get_products(client):
    response = client.get("/api/products")
    assert response.status_code == 200

