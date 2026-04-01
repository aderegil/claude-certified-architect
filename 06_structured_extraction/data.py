# data.py - Few-shot examples and labeled validation data

# --- Few-shot examples for the extraction prompt [Task 4.2] ---
#
# Each example pairs a short invoice snippet with the correct extraction.
# These demonstrate ambiguous-case handling so the model generalizes
# to novel invoice formats without fabricating missing fields.

FEW_SHOT_EXAMPLES = [
    # Example 1 — clean invoice, all fields present
    {
        "document": (
            "INVOICE #EX-001\n"
            "Acme Corp, 100 Main St, NY 10001, (212) 555-0100\n"
            "To: Sample Client, 200 Oak Ave, LA 90001\n"
            "Date: 2025-01-10 | Due: 2025-02-09 | PO: PO-100 | Terms: Net 30\n"
            "Web design (40 hrs @ $150) .............. $6,000.00\n"
            "Hosting setup (1 @ $500) ................   $500.00\n"
            "Subtotal: $6,500.00 | Tax (8%): $520.00 | Total: $7,020.00 | USD"
        ),
        "extraction": {
            "invoice_number": "EX-001",
            "vendor_name": "Acme Corp",
            "vendor_address": "100 Main St, NY 10001",
            "vendor_phone": "(212) 555-0100",
            "customer_name": "Sample Client",
            "invoice_date": "2025-01-10",
            "due_date": "2025-02-09",
            "purchase_order": "PO-100",
            "payment_terms": "net_30",
            "currency": "USD",
            "line_items": [
                {"description": "Web design", "quantity": 40, "unit_price": 150.00, "amount": 6000.00},
                {"description": "Hosting setup", "quantity": 1, "unit_price": 500.00, "amount": 500.00},
            ],
            "subtotal": 6500.00,
            "tax_rate": 8.0,
            "tax_amount": 520.00,
            "stated_total": 7020.00,
            "calculated_total": 7020.00,
            "conflict_detected": False,
            "category": {"value": "technology", "detail": None},
            "confidence": {"overall": "high", "flags": []},
        },
    },
    # Example 2 — missing fields → null (not fabricated) [Task 4.2 S5]
    {
        "document": (
            "Invoice from: River Stone Landscaping\n"
            "Date: March 5, 2025\n"
            "Customer: Oakwood Apartments\n"
            "Spring cleanup and mulching — $1,800.00\n"
            "Tree trimming (3 trees) — $600.00\n"
            "Total: $2,400.00"
        ),
        "extraction": {
            "invoice_number": None,
            "vendor_name": "River Stone Landscaping",
            "vendor_address": None,
            "vendor_phone": None,
            "customer_name": "Oakwood Apartments",
            "invoice_date": "2025-03-05",
            "due_date": None,
            "purchase_order": None,
            "payment_terms": "unclear",
            "currency": "USD",
            "line_items": [
                {"description": "Spring cleanup and mulching", "quantity": 1, "unit_price": 1800.00, "amount": 1800.00},
                {"description": "Tree trimming (3 trees)", "quantity": 1, "unit_price": 600.00, "amount": 600.00},
            ],
            "subtotal": 2400.00,
            "tax_rate": None,
            "tax_amount": None,
            "stated_total": 2400.00,
            "calculated_total": 2400.00,
            "conflict_detected": False,
            "category": {"value": "maintenance", "detail": None},
            "confidence": {"overall": "medium", "flags": ["invoice_number missing", "no payment terms stated"]},
        },
    },
    # Example 3 — European format + total mismatch [Task 4.2 S4]
    {
        "document": (
            "FACTURE #FR-4421\n"
            "Dupont & Fils SARL, 12 Rue de Rivoli, 75001 Paris\n"
            "Tel: +33 1 55 00 1234\n"
            "Client: EuroTech GmbH\n"
            "Date: 28/02/2025 | Echeance: 30/03/2025 | Terms: Net 30\n"
            "Consulting (10 jours @ €950,00) ......... €9.500,00\n"
            "Frais de deplacement ..................... €1.200,00\n"
            "Sous-total: €10.700,00 | TVA (20%): €2.140,00\n"
            "Total: €12.940,00 | EUR"
        ),
        "extraction": {
            "invoice_number": "FR-4421",
            "vendor_name": "Dupont & Fils SARL",
            "vendor_address": "12 Rue de Rivoli, 75001 Paris",
            "vendor_phone": "+33 1 55 00 1234",
            "customer_name": "EuroTech GmbH",
            "invoice_date": "2025-02-28",
            "due_date": "2025-03-30",
            "purchase_order": None,
            "payment_terms": "net_30",
            "currency": "EUR",
            "line_items": [
                {"description": "Consulting", "quantity": 10, "unit_price": 950.00, "amount": 9500.00},
                {"description": "Frais de deplacement", "quantity": 1, "unit_price": 1200.00, "amount": 1200.00},
            ],
            "subtotal": 10700.00,
            "tax_rate": 20.0,
            "tax_amount": 2140.00,
            "stated_total": 12940.00,
            "calculated_total": 12840.00,
            "conflict_detected": True,
            "category": {"value": "consulting", "detail": None},
            "confidence": {
                "overall": "medium",
                "flags": ["stated_total (12940.00) != calculated_total (12840.00)"],
            },
        },
    },
]


# --- Labeled validation set for confidence calibration [Task 5.5] ---
#
# Ground-truth extractions for a subset of invoices. Used to measure
# per-field and per-document-type accuracy before adjusting thresholds.

LABELED_VALIDATIONS = {
    "invoice_01.txt": {
        "invoice_number": "INV-2025-0421",
        "vendor_name": "Pinnacle Consulting Group",
        "invoice_date": "2025-01-15",
        "stated_total": 11149.75,
        "category_value": "consulting",
        "line_item_count": 3,
    },
    "invoice_02.txt": {
        "invoice_number": "TF-0892",
        "vendor_name": "TechForge Solutions",
        "invoice_date": "2025-02-03",
        "stated_total": 21050.00,
        "category_value": "technology",
        "line_item_count": 4,
    },
    "invoice_06.txt": {
        "invoice_number": "SW-2025-0087",
        "vendor_name": "Schmidt & Weber Ingenieurgesellschaft mbH",
        "invoice_date": "2025-03-15",
        "stated_total": 15642.55,
        "category_value": "consulting",
        "line_item_count": 3,
    },
    "invoice_07.txt": {
        "invoice_number": None,
        "vendor_name": "Mike's Plumbing & Heating",
        "invoice_date": "2025-03-18",
        "stated_total": 897.50,
        "category_value": "maintenance",
        "line_item_count": 4,
    },
}
