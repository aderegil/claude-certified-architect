# data.py - Mock project documentation for the MCP documentation server

DOCS = [
    {
        "title": "Storefront Architecture Overview",
        "section": "Architecture",
        "content": (
            "The storefront application follows a layered architecture:\n\n"
            "1. API Layer (api/routes.py) — HTTP endpoint handlers that "
            "validate input and format responses\n"
            "2. Application Layer (app.py) — business logic: order processing, "
            "user registration, product lookup\n"
            "3. Model Layer (models.py) — data structures, validation "
            "(validate_email, format_currency), and factory functions\n"
            "4. Utilities (utils.py) — re-exports commonly used functions "
            "from models.py so callers import from one place\n"
            "5. Middleware (api/middleware.py) — authentication token "
            "validation and rate limiting\n\n"
            "Design decisions:\n"
            "- Functions over classes — all data models are plain dicts\n"
            "- utils.py re-exports validate_email and format_currency from "
            "models.py so other modules don't need to know the source\n"
            "- Authentication middleware runs before route handlers\n"
            "- Business logic lives in app.py, not in route handlers\n"
            "- All route handlers return {status, ...} response dicts"
        ),
    },
    {
        "title": "API Endpoint Reference",
        "section": "API",
        "content": (
            "Available endpoints:\n\n"
            "GET /products — list all products with formatted prices\n"
            "GET /products/:id — get a single product by ID\n"
            "POST /register — register a new user (requires name, email)\n"
            "POST /orders — create an order (requires user, items list)\n\n"
            "Authentication: all endpoints except GET /products require a "
            "Bearer token in the Authorization header.\n"
            "Token format: Bearer <base64-encoded-token>\n\n"
            "Rate limiting: 100 requests per client per minute. "
            "Exceeding the limit returns a rate_limit_exceeded error.\n\n"
            "Error responses use {status: 'error', message: '...'} format."
        ),
    },
    {
        "title": "Onboarding Guide for New Developers",
        "section": "Onboarding",
        "content": (
            "Getting started with the storefront codebase:\n\n"
            "1. Start with app.py — it imports from every other module and "
            "shows how the pieces connect\n"
            "2. Read models.py for data structures and validation rules\n"
            "3. utils.py is a convenience wrapper — it re-exports "
            "validate_email and format_currency from models.py so callers "
            "don't need to know which module defines each function\n"
            "4. api/routes.py handles HTTP endpoints; imports from both "
            "app.py and utils.py\n"
            "5. api/middleware.py handles auth token and API key validation\n\n"
            "Common pitfall: when searching for where validate_email is "
            "defined, you'll find it imported in utils.py — but it's "
            "actually defined in models.py. Always trace re-exports.\n\n"
            "Import chain: models.py defines → utils.py re-exports → "
            "app.py and routes.py consume"
        ),
    },
    {
        "title": "Testing Strategy",
        "section": "Testing",
        "content": (
            "Test files follow the naming convention test_<module>.py and "
            "live in the tests/ directory:\n\n"
            "- test_app.py — business logic (process_order, register_user)\n"
            "- test_models.py — data models and validation edge cases\n"
            "- test_routes.py — API endpoint handler responses\n\n"
            "Each test file imports directly from the module it tests. "
            "Tests use plain assert statements — no external framework.\n\n"
            "Coverage priority: focus on validation edge cases (invalid "
            "emails, missing fields, negative prices) over happy paths."
        ),
    },
    {
        "title": "Known Technical Debt",
        "section": "Debt",
        "content": (
            "Known issues and planned improvements:\n\n"
            "1. middleware.py duplicates the auth pattern regex in both "
            "validate_auth_header and validate_api_key — should extract "
            "to a shared AUTH_PATTERN constant\n"
            "2. No database — all data is in-memory dicts\n"
            "3. No async support — all handlers are synchronous\n"
            "4. Rate limiting is per-process, not distributed\n"
            "5. Error response format is inconsistent — some functions "
            "return error dicts, others could raise exceptions\n\n"
            "Priority: item 1 (pattern duplication) is a quick fix that "
            "demonstrates the Edit tool's non-unique anchor text limitation."
        ),
    },
]
