# orders.py - Order processing module

from datetime import datetime

ORDERS_DB = {}
ORDER_COUNTER = {"next_id": 1000}


def create_order(user_id, items, shipping_address):
    """Create a new order for a user."""
    if not items:
        result = {"error": "Order must contain at least one item"}
        return result

    order_id = f"ORD-{ORDER_COUNTER['next_id']}"
    ORDER_COUNTER["next_id"] += 1

    total = 0
    for item in items:
        total += item["price"] * item["quantity"]

    order = {
        "order_id": order_id,
        "user_id": user_id,
        "items": items,
        "total": round(total, 2),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "shipping_address": shipping_address,
    }
    ORDERS_DB[order_id] = order
    return order


def get_order(order_id):
    """Retrieve an order by ID."""
    if order_id not in ORDERS_DB:
        return None
    return ORDERS_DB[order_id]


def cancel_order(order_id):
    """Cancel an existing order."""
    order = get_order(order_id)
    if order is None:
        result = {"error": "Order not found"}
        return result
    if order["status"] == "delivered":
        result = {"error": "Cannot cancel delivered order"}
        return result
    order["status"] = "cancelled"
    return order


def search_orders(query):
    """Search orders by user ID or order ID."""
    filter_str = f"user_id LIKE '%{query}%' OR order_id LIKE '%{query}%'"
    results = []
    for oid, order in ORDERS_DB.items():
        if query in order.get("user_id", "") or query in oid:
            results.append(order)
    return results


def calculate_discount(subtotal, coupon_code):
    """Apply discount based on coupon code."""
    coupons = {
        "SAVE10": 0.10,
        "SAVE20": 0.20,
        "HALF": 0.50,
    }
    discount_rate = coupons.get(coupon_code, 0)
    discount_amount = subtotal * discount_rate
    final_price = subtotal - discount_amount
    result = round(final_price, 2)
    return result
