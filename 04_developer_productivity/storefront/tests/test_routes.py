# test_routes.py - Tests for API endpoint handlers
from api.routes import handle_get_products, handle_get_product, handle_register


def test_handle_get_products():
    response = handle_get_products()
    assert response["status"] == "ok"
    assert len(response["products"]) > 0


def test_handle_get_product_found():
    response = handle_get_product("PROD-001")
    assert response["status"] == "ok"
    assert response["product"]["name"] == "Wireless Mouse"


def test_handle_get_product_not_found():
    response = handle_get_product("NONEXISTENT")
    assert response["status"] == "error"


def test_handle_register_invalid_email():
    response = handle_register("Test", "bad-email")
    assert response["status"] == "error"
