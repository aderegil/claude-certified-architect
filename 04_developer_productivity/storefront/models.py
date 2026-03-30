# models.py - Data models and validation functions for the storefront
import re


# --- Product ---

def create_product(product_id, name, price, category="general"):
    """Create a product dictionary."""
    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "category": category,
    }
    return product


# --- User ---

def validate_email(email):
    """Validate email format. Returns True if valid."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = bool(re.match(pattern, email))
    return is_valid


def create_user(user_id, name, email):
    """Create a user dictionary with email validation."""
    if not validate_email(email):
        error = {"error": "Invalid email format", "email": email}
        return error
    user = {
        "id": user_id,
        "name": name,
        "email": email,
        "orders": [],
    }
    return user


# --- Order ---

def format_currency(amount):
    """Format a number as USD currency string."""
    formatted = f"${amount:,.2f}"
    return formatted


def create_order(order_id, user_id, items, total):
    """Create an order dictionary."""
    order = {
        "id": order_id,
        "user_id": user_id,
        "items": items,
        "total": total,
        "total_formatted": format_currency(total),
        "status": "pending",
    }
    return order


def calculate_order_total(items):
    """Calculate order total from a list of items with price and quantity."""
    total = sum(item["price"] * item["quantity"] for item in items)
    return total
