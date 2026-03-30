# app.py - Main storefront application logic
from models import create_product, create_user, create_order, calculate_order_total
from utils import validate_email, format_currency, generate_order_id, sanitize_input


# --- Product catalog ---

PRODUCTS = [
    create_product("PROD-001", "Wireless Mouse", 29.99, "electronics"),
    create_product("PROD-002", "USB-C Cable", 12.99, "accessories"),
    create_product("PROD-003", "Desk Lamp", 45.00, "furniture"),
    create_product("PROD-004", "Notebook Set", 8.99, "stationery"),
]


def get_product_by_id(product_id):
    """Look up a product by ID. Returns None if not found."""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def process_order(user, items):
    """Process a new order for a user. Validates items and calculates total."""
    for item in items:
        product = get_product_by_id(item["product_id"])
        if not product:
            error = {"error": f"Product {item['product_id']} not found"}
            return error
        item["price"] = product["price"]
        item["name"] = product["name"]

    total = calculate_order_total(items)
    order_id = generate_order_id()
    order = create_order(order_id, user["id"], items, total)
    return order


def register_user(name, email):
    """Register a new user with input sanitization and email validation."""
    clean_name = sanitize_input(name)
    clean_email = sanitize_input(email)

    if not validate_email(clean_email):
        error = {"error": "Invalid email", "email": clean_email}
        return error

    import uuid
    user_id = f"USR-{uuid.uuid4().hex[:8].upper()}"
    user = create_user(user_id, clean_name, clean_email)
    return user


def get_order_summary(order):
    """Get a human-readable summary of an order."""
    lines = [f"Order {order['id']}: {order['total_formatted']}"]
    for item in order["items"]:
        item_total = format_currency(item["price"] * item["quantity"])
        line = f"  - {item['name']} x{item['quantity']}: {item_total}"
        lines.append(line)
    summary = "\n".join(lines)
    return summary
