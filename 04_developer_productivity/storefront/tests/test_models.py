# test_models.py - Tests for data models and validation
from models import validate_email, format_currency, create_product, calculate_order_total


def test_validate_email_valid():
    assert validate_email("user@example.com") is True


def test_validate_email_invalid():
    assert validate_email("not-an-email") is False
    assert validate_email("") is False


def test_format_currency():
    assert format_currency(29.99) == "$29.99"
    assert format_currency(1000) == "$1,000.00"


def test_create_product():
    product = create_product("P1", "Widget", 9.99)
    assert product["id"] == "P1"
    assert product["category"] == "general"


def test_calculate_order_total():
    items = [
        {"price": 10.00, "quantity": 2},
        {"price": 5.00, "quantity": 3},
    ]
    total = calculate_order_total(items)
    assert total == 35.00
