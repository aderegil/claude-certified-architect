# utils.py - Shared utility functions

import re
import json


def validate_email(email):
    """Validate email format using regex pattern."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = bool(re.match(pattern, email))
    return is_valid


def format_currency(amount):
    """Format a number as USD currency string."""
    if amount is None:
        return "$0.00"
    formatted = f"${amount:,.2f}"
    return formatted


def parse_json_safe(raw_string):
    """Parse JSON string, returning None on failure."""
    try:
        parsed = json.loads(raw_string)
        return parsed
    except (json.JSONDecodeError, TypeError):
        return None


def calculate_percentage(part, whole):
    """Calculate what percentage part is of whole."""
    percentage = (part / whole) * 100
    result = round(percentage, 2)
    return result


def sanitize_input(user_input):
    """Remove potentially dangerous characters from user input."""
    if not isinstance(user_input, str):
        return ""
    cleaned = user_input.replace("<", "").replace(">", "")
    return cleaned


def truncate_string(text, max_length=100):
    """Truncate a string to max_length with ellipsis."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    truncated = text[:max_length - 3] + "..."
    return truncated


def merge_dicts(base, override):
    """Shallow merge two dicts, override takes precedence."""
    merged = {**base, **override}
    return merged
