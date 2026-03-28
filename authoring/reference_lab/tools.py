# tools.py - Tool definitions: get_customer, lookup_order, process_refund, escalate_to_human

import json
from data import CUSTOMERS, CUSTOMERS_BY_EMAIL, ORDERS, REFUNDS_LOG, ESCALATIONS_LOG
from config import MAX_REFUND_AMOUNT


# --- get_customer ---

def get_customer(customer_id=None, email=None):
    """Look up a customer by ID or email."""
    customer = None
    if customer_id:
        customer = CUSTOMERS.get(customer_id)
    elif email:
        customer = CUSTOMERS_BY_EMAIL.get(email)

    if not customer:
        result = {
            "error": True,
            "errorCategory": "validation",
            "isRetryable": True,
            "message": f"No customer found for {'ID ' + customer_id if customer_id else 'email ' + email}. Ask the customer to verify their information.",
        }
        return result

    result = {
        "customer_id": customer["customer_id"],
        "name": customer["name"],
        "email": customer["email"],
        "account_status": customer["account_status"],
        "tier": customer["tier"],
    }
    return result


get_customer_schema = {
    "name": "get_customer",
    "description": "Look up a customer record by customer ID or email address. Returns customer profile including name, email, account status, and tier. Use this tool FIRST before any account action — customer identity must be verified before processing refunds or changes. Accepts either customer_id (e.g., 'CUST-1001') or email (e.g., 'maria.santos@example.com'), not both.",
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": "The customer ID (e.g., 'CUST-1001'). Provide this OR email, not both.",
            },
            "email": {
                "type": "string",
                "description": "The customer's email address. Provide this OR customer_id, not both.",
            },
        },
        "required": [],
    },
}


# --- lookup_order ---

def lookup_order(order_id):
    """Look up an order by order ID."""
    order = ORDERS.get(order_id)

    if not order:
        result = {
            "error": True,
            "errorCategory": "validation",
            "isRetryable": True,
            "message": f"No order found for ID {order_id}. Verify the order ID with the customer.",
        }
        return result

    result = {
        "order_id": order["order_id"],
        "customer_id": order["customer_id"],
        "items": order["items"],
        "total": order["total"],
        "status": order["status"],
        "ordered_at": order["ordered_at"],
        "delivered_at": order["delivered_at"],
    }
    return result


lookup_order_schema = {
    "name": "lookup_order",
    "description": "Look up an order by order ID. Returns order details including items, total, status (pending/shipped/delivered), and dates. Use this to check order status, verify delivery, or gather details before processing a refund. Requires an order ID like 'ORD-5501'.",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The order ID to look up (e.g., 'ORD-5501').",
            },
        },
        "required": ["order_id"],
    },
}


# --- process_refund ---

def process_refund(order_id, amount, reason):
    """Process a refund for a delivered order."""
    order = ORDERS.get(order_id)

    if not order:
        result = {
            "error": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Order {order_id} not found. Cannot process refund.",
        }
        return result

    if order["status"] != "delivered":
        result = {
            "error": True,
            "errorCategory": "business",
            "isRetryable": False,
            "message": f"Order {order_id} has status '{order['status']}'. Refunds can only be processed for delivered orders.",
        }
        return result

    if amount > order["total"]:
        result = {
            "error": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Refund amount ${amount:.2f} exceeds order total ${order['total']:.2f}.",
        }
        return result

    refund_record = {
        "refund_id": f"REF-{len(REFUNDS_LOG) + 7001}",
        "order_id": order_id,
        "amount": amount,
        "reason": reason,
        "status": "processed",
    }
    REFUNDS_LOG.append(refund_record)

    result = {
        "refund_id": refund_record["refund_id"],
        "order_id": order_id,
        "amount": amount,
        "status": "processed",
        "message": f"Refund of ${amount:.2f} processed successfully for order {order_id}.",
    }
    return result


process_refund_schema = {
    "name": "process_refund",
    "description": "Process a refund for a delivered order. Requires the order ID, refund amount, and a reason. The order must have status 'delivered' — refunds cannot be processed for pending or shipped orders. The refund amount must not exceed the order total. IMPORTANT: Customer identity must be verified via get_customer before calling this tool.",
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The order ID to refund (e.g., 'ORD-5501').",
            },
            "amount": {
                "type": "number",
                "description": "The refund amount in dollars (e.g., 249.99).",
            },
            "reason": {
                "type": "string",
                "description": "The reason for the refund (e.g., 'defective product', 'wrong item shipped').",
            },
        },
        "required": ["order_id", "amount", "reason"],
    },
}


# --- escalate_to_human ---

def escalate_to_human(customer_id, reason, summary, recommended_action=None):
    """Escalate a case to a human agent with structured context."""
    escalation_record = {
        "escalation_id": f"ESC-{len(ESCALATIONS_LOG) + 9001}",
        "customer_id": customer_id,
        "reason": reason,
        "summary": summary,
        "recommended_action": recommended_action,
        "status": "pending_review",
    }
    ESCALATIONS_LOG.append(escalation_record)

    result = {
        "escalation_id": escalation_record["escalation_id"],
        "status": "pending_review",
        "message": f"Case escalated to human agent. Escalation ID: {escalation_record['escalation_id']}. A human agent will review this case shortly.",
    }
    return result


escalate_to_human_schema = {
    "name": "escalate_to_human",
    "description": "Escalate a customer support case to a human agent. Use when: (1) the customer explicitly requests a human, (2) the situation involves a policy gap, (3) you cannot make progress after two attempts, or (4) fraud is suspected. Include a structured summary with customer ID, root cause, and recommended action so the human agent has full context without reading the transcript.",
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": "The customer's ID (e.g., 'CUST-1001').",
            },
            "reason": {
                "type": "string",
                "description": "The escalation reason: 'customer_request', 'policy_gap', 'repeated_failure', or 'fraud'.",
            },
            "summary": {
                "type": "string",
                "description": "A structured summary of the case including what was attempted and current state.",
            },
            "recommended_action": {
                "type": "string",
                "description": "Optional recommended next step for the human agent.",
            },
        },
        "required": ["customer_id", "reason", "summary"],
    },
}


# --- Tool registry ---

ALL_TOOLS = [
    get_customer_schema,
    lookup_order_schema,
    process_refund_schema,
    escalate_to_human_schema,
]

TOOL_FUNCTIONS = {
    "get_customer": get_customer,
    "lookup_order": lookup_order,
    "process_refund": process_refund,
    "escalate_to_human": escalate_to_human,
}
