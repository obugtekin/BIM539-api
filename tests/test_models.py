import pytest
from models import (
    User, UserCreate,
    Category, CategoryCreate,
    Product, ProductCreate,
    Order, OrderCreate,
    Review, ReviewCreate
)

def test_user_create_valid():
    user = UserCreate(
        name="Test User",
        email="test@example.com"
    )
    assert user.name == "Test User"

def test_category_create_valid():
    category = CategoryCreate(name="Elektronik")
    assert category.name == "Elektronik"

def test_product_create_valid():
    product = ProductCreate(
        name="Laptop",
        price=15000.00
    )
    assert product.name == "Laptop"

def test_order_create_valid():
    order = OrderCreate(
        user_id=1,
        total_amount=15000.00
    )
    assert order.user_id == 1

def test_review_create_valid():
    review = ReviewCreate(
        user_id=1,
        product_id=1,
        rating=5
    )
    assert review.rating == 5

def test_product_name():
    product = ProductCreate(name="Test", price=100.0)
    assert product.name == "Test"

def test_order_total():
    order = OrderCreate(user_id=1, total_amount=500.0)
    assert order.total_amount == 500.0

def test_category_name_only():
    category = CategoryCreate(name="Test")
    assert category.name == "Test"

def test_review_rating_only():
    review = ReviewCreate(user_id=1, product_id=1, rating=3)
    assert review.rating == 3

def test_user_email_only():
    user = UserCreate(name="Test", email="test@test.com")
    assert user.email == "test@test.com"

