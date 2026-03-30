# inventory_server.py - Custom MCP server exposing inventory data
import os

from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("Inventory", log_level="ERROR")

PRODUCTS = {
    "PROD-001": {"name": "Wireless Headphones", "price": 79.99, "stock": 45},
    "PROD-002": {"name": "USB-C Hub", "price": 49.99, "stock": 12},
    "PROD-003": {"name": "Mechanical Keyboard", "price": 129.99, "stock": 0},
    "PROD-004": {"name": "Webcam HD Pro", "price": 89.99, "stock": 28},
    "PROD-005": {"name": "Laptop Stand", "price": 34.99, "stock": 3},
}


def check_auth():
    """Verify INVENTORY_SECRET is set — demonstrates env var expansion from .mcp.json."""
    secret = os.environ.get("INVENTORY_SECRET", "")
    if not secret:
        error = {
            "error": True,
            "message": "INVENTORY_SECRET not configured. Add it to .env and restart Claude Code.",
        }
        return error
    return None


# --- MCP Tools ---
# [Task 2.4] — custom MCP server for team-specific workflows


@mcp.tool(
    name="check_stock",
    description="Check the current stock level for a specific product by its ID (e.g., PROD-001). Returns product name, price, and stock quantity. Use this when you need details about a single known product.",
)
def check_stock(
    product_id: str = Field(description="Product ID in PROD-XXX format"),
):
    auth_error = check_auth()
    if auth_error:
        return auth_error

    product = PRODUCTS.get(product_id)
    if product is None:
        result = {"error": True, "message": f"Product {product_id} not found"}
        return result

    result = {"product_id": product_id, **product}
    return result


@mcp.tool(
    name="search_products",
    description="Search inventory products by name keyword. Returns all products whose name contains the search term (case-insensitive). Use this when you need to find products but don't know the exact ID.",
)
def search_products(
    keyword: str = Field(description="Search term to match against product names"),
):
    auth_error = check_auth()
    if auth_error:
        return auth_error

    matches = []
    for pid, product in PRODUCTS.items():
        if keyword.lower() in product["name"].lower():
            match = {"product_id": pid, **product}
            matches.append(match)

    result = {"keyword": keyword, "matches": matches, "count": len(matches)}
    return result


# --- MCP Resource ---
# [Task 2.4] — MCP resources expose content catalogs to reduce exploratory tool calls


@mcp.resource("inventory://products", mime_type="application/json")
def list_products():
    """Product catalog — lets agents see available inventory without calling a tool."""
    catalog = []
    for pid, product in PRODUCTS.items():
        entry = {"product_id": pid, "name": product["name"], "price": product["price"]}
        catalog.append(entry)
    return catalog


if __name__ == "__main__":
    mcp.run(transport="stdio")
