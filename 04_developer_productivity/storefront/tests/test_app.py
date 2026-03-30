# test_app.py - Tests for storefront application logic
from app import get_product_by_id, register_user, PRODUCTS


def test_get_product_by_id():
    product = get_product_by_id("PROD-001")
    assert product is not None
    assert product["name"] == "Wireless Mouse"


def test_get_product_not_found():
    product = get_product_by_id("NONEXISTENT")
    assert product is None


def test_register_user_valid():
    user = register_user("Alice", "alice@example.com")
    assert "id" in user
    assert user["name"] == "Alice"


def test_register_user_invalid_email():
    result = register_user("Bob", "not-an-email")
    assert "error" in result
