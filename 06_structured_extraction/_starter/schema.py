# schema.py - Invoice extraction tool schema definition
#
# [Task 4.3] — tool_use with JSON schema is the most reliable method
# for getting schema-compliant structured output. The model "calls"
# the extract_invoice tool with extracted fields as arguments.

# --- extract_invoice tool schema (companion _schema dict pattern) ---
#
# The tool has no executable function — it exists only to force the
# model to return structured JSON that conforms to this schema.

extract_invoice_schema = {
    "name": "extract_invoice",
    "description": (
        "Extract structured data from an invoice document. "
        "Call this tool with all fields populated from the invoice. "
        "For fields where the document provides no information, you MUST "
        "pass null rather than fabricating a value."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "invoice_number": {
                "type": "string",
                "description": "Invoice number or identifier exactly as shown on the document.",
            },
            "vendor_name": {
                "type": "string",
                "description": "Vendor or supplier company name.",
            },
            "vendor_address": {
                "type": "string",
                "description": "Vendor street address, single-line with comma separators.",
            },
            "vendor_phone": {
                "type": ["string", "null"],
                "description": "Vendor phone number. Null if not present in the document.",
            },
            "customer_name": {
                "type": "string",
                "description": "Customer or buyer name.",
            },
            "invoice_date": {
                "type": "string",
                "description": "Invoice date normalized to YYYY-MM-DD format.",
            },
            "due_date": {
                "type": ["string", "null"],
                "description": "Payment due date normalized to YYYY-MM-DD. Null if not stated.",
            },
            "purchase_order": {
                "type": ["string", "null"],
                "description": "Purchase order number. Null if not referenced.",
            },
            # TODO (Step 4): Replace the plain string type with an enum:
            #   "type": "string",
            #   "enum": ["net_15", "net_30", "net_45", "net_60",
            #            "due_on_receipt", "unclear"]
            #   Use "unclear" when terms are ambiguous or reference
            #   external agreements.
            "payment_terms": {
                "type": "string",
                "description": "Payment terms. Use 'unclear' if ambiguous.",
            },
            "currency": {
                "type": "string",
                "description": "ISO 4217 currency code (e.g., USD, EUR, GBP).",
            },
            "line_items": {
                "type": "array",
                "description": "All line items from the invoice.",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": "Item description.",
                        },
                        "quantity": {
                            "type": "number",
                            "description": "Quantity.",
                        },
                        "unit_price": {
                            "type": "number",
                            "description": "Price per unit as a number (no currency symbols).",
                        },
                        "amount": {
                            "type": "number",
                            "description": "Line total as a number.",
                        },
                    },
                    "required": ["description", "quantity", "unit_price", "amount"],
                },
            },
            "subtotal": {
                "type": ["number", "null"],
                "description": "Subtotal before tax.",
            },
            # Nullable fields (vendor_phone, due_date, purchase_order, subtotal,
            # tax_rate, tax_amount) use ["type", "null"] and are excluded from
            # the required list. This prevents the model from fabricating values
            # when the invoice doesn't contain the information. [Task 4.3]
            "tax_rate": {
                "type": ["number", "null"],
                "description": "Tax rate as a percentage (e.g., 8.25). Null if not stated.",
            },
            "tax_amount": {
                "type": ["number", "null"],
                "description": "Tax amount as a number. Null if not applicable.",
            },
            "stated_total": {
                "type": "number",
                "description": "Total amount exactly as stated on the invoice.",
            },
            # TODO (Step 5): Add a calculated_total field here:
            #   "calculated_total": {
            #       "type": "number",
            #       "description": "Sum of line item amounts plus tax. Computed by "
            #                      "you independently of the stated total.",
            #   },

            # TODO (Step 5): Add a conflict_detected field here:
            #   "conflict_detected": {
            #       "type": "boolean",
            #       "description": "True when calculated_total differs from stated_total.",
            #   },

            # TODO (Step 4): Replace the plain string with an object that uses
            #   an enum plus a detail field:
            #   "category": {
            #       "type": "object",
            #       "properties": {
            #           "value": {
            #               "type": "string",
            #               "enum": ["consulting", "office_supplies",
            #                        "technology", "maintenance", "travel",
            #                        "utilities", "other"],
            #               "description": "Best-fit category for this invoice.",
            #           },
            #           "detail": {
            #               "type": ["string", "null"],
            #               "description": "Explanation when value is 'other'. Null otherwise.",
            #           },
            #       },
            #       "required": ["value"],
            #   },
            "category": {
                "type": "string",
                "description": "Invoice category (e.g., consulting, office_supplies, "
                "technology, maintenance, travel, utilities).",
            },
            # TODO (Step 9): Add a confidence object here:
            #   "confidence": {
            #       "type": "object",
            #       "properties": {
            #           "overall": {
            #               "type": "string",
            #               "enum": ["high", "medium", "low"],
            #               "description": "Overall extraction confidence.",
            #           },
            #           "flags": {
            #               "type": "array",
            #               "items": {"type": "string"},
            #               "description": "List of fields or issues with reduced confidence.",
            #           },
            #       },
            #       "required": ["overall", "flags"],
            #   },
        },
        "required": [
            "invoice_number",
            "vendor_name",
            "vendor_address",
            "customer_name",
            "invoice_date",
            "payment_terms",
            "currency",
            "line_items",
            "stated_total",
            "category",
        ],
    },
}
