# utils.py - Utility re-exports and helpers
#
# Re-exports commonly used functions from models so other modules
# can import from utils instead of knowing which module defines each function.

from models import validate_email, format_currency


def generate_order_id():
    """Generate a unique order ID."""
    import uuid
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    return order_id


def sanitize_input(text):
    """Basic input sanitization — strip whitespace and escape HTML."""
    sanitized = text.strip()
    sanitized = sanitized.replace("<", "&lt;").replace(">", "&gt;")
    return sanitized
