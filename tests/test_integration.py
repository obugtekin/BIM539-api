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

def test_get_user_by_id(client):
    create_response = client.post(
        "/api/users",
        json={"name": "Test User", "email": "test2@example.com"}
    )
    user_id = create_response.json()["id"]
    
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200

def test_get_category_by_id(client):
    create_response = client.post(
        "/api/categories",
        json={"name": "Test Kategori 2"}
    )
    category_id = create_response.json()["id"]
    
    response = client.get(f"/api/categories/{category_id}")
    assert response.status_code == 200

def test_get_product_by_id(client):
    category_response = client.post(
        "/api/categories",
        json={"name": "Test Kategori 3"}
    )
    category_id = category_response.json()["id"]
    
    product_response = client.post(
        "/api/products",
        json={"name": "Test Ürün", "price": 100.00, "category_id": category_id}
    )
    product_id = product_response.json()["id"]
    
    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 200

def test_get_order_by_id(client):
    user_response = client.post(
        "/api/users",
        json={"name": "Test User", "email": "test3@example.com"}
    )
    user_id = user_response.json()["id"]
    
    order_response = client.post(
        "/api/orders",
        json={"user_id": user_id, "total_amount": 5000.00}
    )
    order_id = order_response.json()["id"]
    
    response = client.get(f"/api/orders/{order_id}")
    assert response.status_code == 200

def test_get_reviews(client):
    response = client.get("/api/reviews")
    assert response.status_code == 200

def test_get_review_by_id(client):
    user_response = client.post(
        "/api/users",
        json={"name": "Test User", "email": "test4@example.com"}
    )
    user_id = user_response.json()["id"]
    
    category_response = client.post(
        "/api/categories",
        json={"name": "Test Kategori 4"}
    )
    category_id = category_response.json()["id"]
    
    product_response = client.post(
        "/api/products",
        json={"name": "Test Ürün 2", "price": 200.00, "category_id": category_id}
    )
    product_id = product_response.json()["id"]
    
    review_response = client.post(
        "/api/reviews",
        json={"user_id": user_id, "product_id": product_id, "rating": 5}
    )
    review_id = review_response.json()["id"]
    
    response = client.get(f"/api/reviews/{review_id}")
    assert response.status_code == 200

