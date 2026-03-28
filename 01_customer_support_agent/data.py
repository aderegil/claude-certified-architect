# data.py - Mock customer and order data

CUSTOMERS = {
    "CUST-1001": {
        "customer_id": "CUST-1001",
        "name": "Maria Santos",
        "email": "maria.santos@example.com",
        "phone": "+1-555-0142",
        "account_status": "active",
        "tier": "gold",
        "created_at": "2024-03-15T10:30:00Z",
    },
    "CUST-1002": {
        "customer_id": "CUST-1002",
        "name": "James Chen",
        "email": "james.chen@example.com",
        "phone": "+1-555-0198",
        "account_status": "active",
        "tier": "standard",
        "created_at": "2024-08-22T14:15:00Z",
    },
    "CUST-1003": {
        "customer_id": "CUST-1003",
        "name": "Priya Sharma",
        "email": "priya.sharma@example.com",
        "phone": "+1-555-0267",
        "account_status": "suspended",
        "tier": "standard",
        "created_at": "2023-11-01T09:00:00Z",
    },
}

# Lookup by email for convenience
CUSTOMERS_BY_EMAIL = {c["email"]: c for c in CUSTOMERS.values()}

ORDERS = {
    "ORD-5501": {
        "order_id": "ORD-5501",
        "customer_id": "CUST-1001",
        "items": [
            {"name": "Wireless Noise-Cancelling Headphones", "sku": "WH-400", "qty": 1, "price": 249.99},
        ],
        "total": 249.99,
        "status": "delivered",
        "ordered_at": "2025-02-10T08:20:00Z",
        "delivered_at": "2025-02-14T16:45:00Z",
    },
    "ORD-5502": {
        "order_id": "ORD-5502",
        "customer_id": "CUST-1001",
        "items": [
            {"name": "USB-C Charging Dock", "sku": "CD-120", "qty": 1, "price": 89.99},
            {"name": "Laptop Stand", "sku": "LS-300", "qty": 1, "price": 59.99},
        ],
        "total": 149.98,
        "status": "delivered",
        "ordered_at": "2025-03-01T11:00:00Z",
        "delivered_at": "2025-03-05T13:30:00Z",
    },
    "ORD-5503": {
        "order_id": "ORD-5503",
        "customer_id": "CUST-1002",
        "items": [
            {"name": "4K Monitor 27-inch", "sku": "MN-270", "qty": 1, "price": 649.99},
        ],
        "total": 649.99,
        "status": "delivered",
        "ordered_at": "2025-01-20T09:15:00Z",
        "delivered_at": "2025-01-25T10:00:00Z",
    },
    "ORD-5504": {
        "order_id": "ORD-5504",
        "customer_id": "CUST-1002",
        "items": [
            {"name": "Mechanical Keyboard", "sku": "KB-700", "qty": 1, "price": 179.99},
        ],
        "total": 179.99,
        "status": "shipped",
        "ordered_at": "2025-03-18T15:40:00Z",
        "delivered_at": None,
    },
    "ORD-5505": {
        "order_id": "ORD-5505",
        "customer_id": "CUST-1003",
        "items": [
            {"name": "Ergonomic Office Chair", "sku": "CH-900", "qty": 1, "price": 399.99},
            {"name": "Desk Organizer Set", "sku": "DO-150", "qty": 2, "price": 24.99},
        ],
        "total": 449.97,
        "status": "delivered",
        "ordered_at": "2025-02-28T12:00:00Z",
        "delivered_at": "2025-03-04T09:20:00Z",
    },
}

REFUNDS_LOG = []
ESCALATIONS_LOG = []
