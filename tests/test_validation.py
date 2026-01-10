import pytest
from models import UserCreate, ProductCreate, OrderCreate, ReviewCreate, CategoryCreate

def test_user_create_basic():
    user = UserCreate(
        name="Test",
        email="test@example.com"
    )
    assert user.name == "Test"
    assert user.email == "test@example.com"

def test_review_create_basic():
    review = ReviewCreate(
        user_id=1,
        product_id=1,
        rating=3
    )
    assert review.rating == 3

def test_category_create_basic():
    category = CategoryCreate(name="Test Kategori")
    assert category.name == "Test Kategori"

def test_order_create_basic():
    order = OrderCreate(
        user_id=1,
        total_amount=1000.00
    )
    assert order.user_id == 1
    assert order.total_amount == 1000.00

def test_product_create_basic():
    product = ProductCreate(
        name="Test Ürün",
        price=500.00
    )
    assert product.name == "Test Ürün"
    assert product.price == 500.00

