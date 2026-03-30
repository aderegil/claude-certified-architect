# middleware.py - Authentication and request middleware
import re

BEARER_TOKEN_PATTERN = r'^Bearer [A-Za-z0-9\-._~+/]+=*$'


def validate_auth_header(header):
    """Validate the Authorization header format."""
    if not header:
        error = {"error": "Missing Authorization header"}
        return error
    is_valid = bool(re.match(BEARER_TOKEN_PATTERN, header))
    if not is_valid:
        error = {"error": "Invalid token format"}
        return error
    token = header.split(" ")[1]
    result = {"valid": True, "token": token}
    return result


def validate_api_key(key):
    """Validate an API key format."""
    if not key:
        error = {"error": "Missing API key"}
        return error
    is_valid = bool(re.match(BEARER_TOKEN_PATTERN, key))
    if not is_valid:
        error = {"error": "Invalid API key format"}
        return error
    result = {"valid": True, "key": key}
    return result


def rate_limit_check(client_id, request_count, max_requests=100):
    """Check if a client has exceeded the rate limit."""
    if request_count >= max_requests:
        error = {
            "error": "Rate limit exceeded",
            "client_id": client_id,
            "limit": max_requests,
        }
        return error
    remaining = max_requests - request_count
    result = {"allowed": True, "remaining": remaining}
    return result
