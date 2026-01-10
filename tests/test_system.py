import pytest
from fastapi.testclient import TestClient

def test_scenario_user_product_order(client):
    user_response = client.post(
        "/api/users",
        json={
            "name": "ONUR BUĞTEKİN",
            "email": "onur@example.com"
        }
    )
    user_id = user_response.json()["id"]
    
    category_response = client.post(
        "/api/categories",
        json={"name": "Elektronik"}
    )
    category_id = category_response.json()["id"]
    
    product_response = client.post(
        "/api/products",
        json={
            "name": "Laptop",
            "price": 15000.00,
            "category_id": category_id
        }
    )
    product_id = product_response.json()["id"]
    
    order_response = client.post(
        "/api/orders",
        json={
            "user_id": user_id,
            "total_amount": 15000.00
        }
    )
    assert order_response.status_code == 201

def test_scenario_product_lifecycle(client):
    category_response = client.post(
        "/api/categories",
        json={"name": "Giyim"}
    )
    category_id = category_response.json()["id"]
    
    create_response = client.post(
        "/api/products",
        json={
            "name": "Tişört",
            "price": 150.00,
            "category_id": category_id
        }
    )
    product_id = create_response.json()["id"]
    
    list_response = client.get("/api/products")
    assert list_response.status_code == 200

def test_scenario_user_product_review(client):
    user_response = client.post(
        "/api/users",
        json={
            "name": "Test User",
            "email": "testuser@example.com"
        }
    )
    user_id = user_response.json()["id"]
    
    category_response = client.post(
        "/api/categories",
        json={"name": "Elektronik"}
    )
    category_id = category_response.json()["id"]
    
    product_response = client.post(
        "/api/products",
        json={
            "name": "Telefon",
            "price": 8000.00,
            "category_id": category_id
        }
    )
    assert product_response.status_code == 201
    
    review_response = client.post(
        "/api/reviews",
        json={
            "user_id": user_id,
            "product_id": product_response.json()["id"],
            "rating": 5
        }
    )
    assert review_response.status_code == 201

def test_scenario_category_product_order_review(client):
    category_response = client.post(
        "/api/categories",
        json={"name": "Spor"}
    )
    category_id = category_response.json()["id"]
    
    product_response = client.post(
        "/api/products",
        json={
            "name": "Spor Ayakkabı",
            "price": 500.00,
            "category_id": category_id
        }
    )
    assert product_response.status_code == 201
    
    user_response = client.post(
        "/api/users",
        json={
            "name": "Test User 2",
            "email": "testuser2@example.com"
        }
    )
    user_id = user_response.json()["id"]
    
    order_response = client.post(
        "/api/orders",
        json={
            "user_id": user_id,
            "total_amount": 500.00
        }
    )
    assert order_response.status_code == 201

def test_scenario_simple_user_category(client):
    user_response = client.post(
        "/api/users",
        json={
            "name": "Test Kullanıcı",
            "email": "test@example.com"
        }
    )
    assert user_response.status_code == 201
    
    category_response = client.post(
        "/api/categories",
        json={"name": "Test Kategori"}
    )
    assert category_response.status_code == 201

