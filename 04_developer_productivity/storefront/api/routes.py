# routes.py - API endpoint handlers for the storefront
from app import get_product_by_id, process_order, register_user, PRODUCTS
from utils import validate_email, format_currency


def handle_get_products():
    """GET /products — list all products with formatted prices."""
    results = []
    for p in PRODUCTS:
        item = {
            "id": p["id"],
            "name": p["name"],
            "price_formatted": format_currency(p["price"]),
        }
        results.append(item)
    response = {"status": "ok", "products": results}
    return response


def handle_get_product(product_id):
    """GET /products/:id — get a single product by ID."""
    product = get_product_by_id(product_id)
    if not product:
        response = {"status": "error", "message": "Product not found"}
        return response
    response = {"status": "ok", "product": product}
    return response


def handle_register(name, email):
    """POST /register — register a new user with validation."""
    if not validate_email(email):
        response = {"status": "error", "message": "Invalid email format"}
        return response
    user = register_user(name, email)
    response = {"status": "ok", "user": user}
    return response


def handle_create_order(user, items):
    """POST /orders — create a new order for a user."""
    order = process_order(user, items)
    if "error" in order:
        response = {"status": "error", "message": order["error"]}
        return response
    response = {"status": "ok", "order": order}
    return response
