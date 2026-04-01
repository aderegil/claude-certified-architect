# main.py - Invoice extraction pipeline with validation, retry, and confidence routing
import json
import os

import anthropic
from dotenv import load_dotenv

from config import (
    MODEL,
    MAX_RETRIES,
    CYAN,
    GREEN,
    YELLOW,
    RED,
    DIM,
    BOLD,
    RESET,
)
from schema import extract_invoice_schema
from data import FEW_SHOT_EXAMPLES, LABELED_VALIDATIONS

load_dotenv()

INVOICES_DIR = os.path.join(os.path.dirname(__file__), "invoices")
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")


# --- Prompt loading ---


def load_extraction_prompt():
    """Load the system prompt template from prompts/extraction_prompt.txt."""
    prompt_path = os.path.join(PROMPTS_DIR, "extraction_prompt.txt")
    with open(prompt_path, "r") as f:
        template = f.read()
    return template


def load_invoice(filename):
    """Load an invoice document from the invoices/ directory."""
    invoice_path = os.path.join(INVOICES_DIR, filename)
    with open(invoice_path, "r") as f:
        content = f.read()
    return content


# --- Few-shot formatting [Task 4.2] ---


def format_few_shot_examples(examples):
    """Format few-shot examples for the {few_shot_examples} template variable."""
    # TODO (Step 7): Format each example as a numbered block showing the
    #   invoice text and the correct extraction JSON. Return the formatted
    #   string. Here is the pattern:
    #
    #   formatted = []
    #   for i, ex in enumerate(examples, 1):
    #       extraction_json = json.dumps(ex["extraction"], indent=2)
    #       block = (
    #           f"<example>\n"
    #           f"<invoice>\n{ex['document']}\n</invoice>\n"
    #           f"<correct_extraction>\n{extraction_json}\n</correct_extraction>\n"
    #           f"</example>"
    #       )
    #       formatted.append(block)
    #   result = "\n\n".join(formatted)
    #   return result
    return "No examples provided."


# --- Extraction [Task 4.3] ---


def extract_invoice(client, invoice_text, system_prompt):
    """Call the API with tool_choice forced to extract structured data."""
    messages = [
        {
            "role": "user",
            "content": (
                "Extract all fields from this invoice:\n\n"
                f"<invoice>\n{invoice_text}\n</invoice>"
            ),
        }
    ]

    # [Task 4.3] — tool_choice forced: the model MUST call extract_invoice.
    # Compare with "auto" (model decides) and "any" (must use some tool).
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system_prompt,
        tools=[extract_invoice_schema],
        tool_choice={"type": "tool", "name": "extract_invoice"},
        messages=messages,
    )

    # The extraction is in the tool_use block's input field
    for block in response.content:
        if block.type == "tool_use":
            return block.input
    return None


# --- Validation [Task 4.4] ---


def validate_extraction(extraction):
    """Validate extracted data and return a list of error strings."""
    errors = []

    # TODO (Step 5): Compare calculated_total to stated_total.
    #   If they differ by more than $0.01, append an error message:
    #
    #   calculated = extraction.get("calculated_total")
    #   stated = extraction.get("stated_total")
    #   if calculated is not None and stated is not None:
    #       diff = abs(calculated - stated)
    #       if diff > 0.01:
    #           error = (
    #               f"Total mismatch: stated_total={stated}, "
    #               f"calculated_total={calculated}, difference={diff:.2f}"
    #           )
    #           errors.append(error)

    # TODO (Step 6): Add additional validation checks:
    #
    #   # Check required fields are not None
    #   for field in ["invoice_number", "vendor_name", "invoice_date"]:
    #       if extraction.get(field) is None:
    #           errors.append(f"Required field '{field}' is null — info absent from document")
    #
    #   # Check date format (YYYY-MM-DD)
    #   date_val = extraction.get("invoice_date", "")
    #   if date_val and not _is_valid_date(date_val):
    #       errors.append(f"Invalid date format: {date_val} (expected YYYY-MM-DD)")
    #
    #   # Check line items are not empty
    #   items = extraction.get("line_items", [])
    #   if not items:
    #       errors.append("No line items extracted")

    return errors


def _is_valid_date(date_str):
    """Check if a string matches YYYY-MM-DD format."""
    import re
    match = re.match(r"^\d{4}-\d{2}-\d{2}$", date_str)
    result = bool(match)
    return result


# --- Retry with feedback [Task 4.4] ---


def retry_with_feedback(client, invoice_text, extraction, errors, system_prompt):
    """Retry extraction, appending validation errors as feedback."""
    # TODO (Step 6): Implement the retry loop.
    #
    #   error_list = "\n".join(f"- {e}" for e in errors)
    #   failed_json = json.dumps(extraction, indent=2)
    #   messages = [
    #       {
    #           "role": "user",
    #           "content": (
    #               "Extract all fields from this invoice:\n\n"
    #               f"<invoice>\n{invoice_text}\n</invoice>"
    #           ),
    #       },
    #       {
    #           "role": "assistant",
    #           "content": [
    #               {
    #                   "type": "tool_use",
    #                   "id": "retry_call",
    #                   "name": "extract_invoice",
    #                   "input": extraction,
    #               }
    #           ],
    #       },
    #       {
    #           "role": "user",
    #           "content": [
    #               {
    #                   "type": "tool_result",
    #                   "tool_use_id": "retry_call",
    #                   "content": (
    #                       f"Validation failed. Fix these errors and re-extract:\n"
    #                       f"{error_list}\n\n"
    #                       f"Previous extraction:\n{failed_json}"
    #                   ),
    #                   "is_error": True,
    #               }
    #           ],
    #       },
    #   ]
    #
    #   response = client.messages.create(
    #       model=MODEL,
    #       max_tokens=4096,
    #       system=system_prompt,
    #       tools=[extract_invoice_schema],
    #       tool_choice={"type": "tool", "name": "extract_invoice"},
    #       messages=messages,
    #   )
    #
    #   for block in response.content:
    #       if block.type == "tool_use":
    #           return block.input
    #   return extraction
    return extraction


# --- Confidence routing [Task 5.5] ---


def classify_review_need(extraction):
    """Route an extraction to auto_approve, spot_check, or human_review."""
    # TODO (Step 9): Implement confidence-based routing.
    #
    #   confidence = extraction.get("confidence", {})
    #   overall = confidence.get("overall", "low")
    #   flags = confidence.get("flags", [])
    #
    #   if overall == "high" and not flags:
    #       return "auto_approve"
    #   elif overall == "low" or len(flags) >= 3:
    #       return "human_review"
    #   else:
    #       return "spot_check"
    return "auto_approve"


# --- Pipeline ---


def run_extraction(invoice_filename):
    """Run the full extraction pipeline on one invoice file."""
    client = anthropic.Anthropic()
    system_template = load_extraction_prompt()

    # [Task 4.2] — inject few-shot examples via the template variable
    few_shot_text = format_few_shot_examples(FEW_SHOT_EXAMPLES)
    system_prompt = system_template.format(few_shot_examples=few_shot_text)

    invoice_text = load_invoice(invoice_filename)

    print(f"\n{CYAN}{BOLD}{'=' * 60}")
    print(f"  Extracting: {invoice_filename}")
    print(f"{'=' * 60}{RESET}")

    # Step 1: extract
    try:
        extraction = extract_invoice(client, invoice_text, system_prompt)
    except Exception as exc:
        error_msg = str(exc).lower()
        if "credit" in error_msg or "balance" in error_msg:
            print(f"\n{RED}{BOLD}API credit balance is too low.{RESET}")
            print(f"{DIM}Add credits at https://console.anthropic.com{RESET}")
        else:
            print(f"\n{RED}{BOLD}  API error: {exc}{RESET}")
        return None

    if not extraction:
        print(f"\n{RED}  No extraction result returned.{RESET}")
        return None

    print(f"\n{GREEN}{BOLD}  Extraction result:{RESET}")
    print(f"{DIM}{json.dumps(extraction, indent=2)}{RESET}")

    # Step 2: validate
    errors = validate_extraction(extraction)
    if errors:
        print(f"\n{YELLOW}{BOLD}  Validation errors:{RESET}")
        for err in errors:
            print(f"    {YELLOW}- {err}{RESET}")

        # [Task 4.4] — distinguish retryable vs non-retryable errors
        retryable = [e for e in errors if "absent" not in e.lower()]
        non_retryable = [e for e in errors if "absent" in e.lower()]

        if non_retryable:
            print(f"\n{DIM}  Non-retryable (info absent from document):{RESET}")
            for err in non_retryable:
                print(f"    {DIM}- {err}{RESET}")

        # Step 3: retry if there are retryable errors
        if retryable:
            for attempt in range(1, MAX_RETRIES + 1):
                print(f"\n{DIM}  Retry {attempt}/{MAX_RETRIES} with error feedback...{RESET}")
                extraction = retry_with_feedback(
                    client, invoice_text, extraction, retryable, system_prompt
                )
                errors = validate_extraction(extraction)
                retryable = [e for e in errors if "absent" not in e.lower()]
                if not retryable:
                    print(f"  {GREEN}Retry succeeded.{RESET}")
                    break
            else:
                print(f"\n{RED}  Max retries reached. Errors remain.{RESET}")

            print(f"\n{GREEN}{BOLD}  Final extraction:{RESET}")
            print(f"{DIM}{json.dumps(extraction, indent=2)}{RESET}")

    # Step 4: route based on confidence
    review = classify_review_need(extraction)
    color_map = {"auto_approve": GREEN, "spot_check": YELLOW, "human_review": RED}
    color = color_map.get(review, DIM)
    print(f"\n{color}{BOLD}  Review routing: {review}{RESET}")
    print(f"{DIM}{'=' * 60}{RESET}\n")

    return extraction


# --- Accuracy check against labeled data [Task 5.5] ---


def check_accuracy(results):
    """Compare extraction results against labeled validation data."""
    print(f"\n{CYAN}{BOLD}{'=' * 60}")
    print(f"  Accuracy Check — Labeled Validation Set")
    print(f"{'=' * 60}{RESET}\n")

    total_fields = 0
    correct_fields = 0

    for filename, truth in LABELED_VALIDATIONS.items():
        extraction = results.get(filename)
        if not extraction:
            print(f"  {DIM}{filename}: not extracted, skipping{RESET}")
            continue

        print(f"  {BOLD}{filename}{RESET}")
        for field, expected in truth.items():
            total_fields += 1
            # Handle nested category comparison
            if field == "category_value":
                actual_cat = extraction.get("category", "")
                actual = actual_cat.get("value", actual_cat) if isinstance(actual_cat, dict) else actual_cat
            elif field == "line_item_count":
                actual = len(extraction.get("line_items", []))
            else:
                actual = extraction.get(field)

            match = actual == expected
            if match:
                correct_fields += 1
                print(f"    {GREEN}✓ {field}: {actual}{RESET}")
            else:
                print(f"    {RED}✗ {field}: got {actual}, expected {expected}{RESET}")

    if total_fields > 0:
        pct = (correct_fields / total_fields) * 100
        print(f"\n  {BOLD}Accuracy: {correct_fields}/{total_fields} ({pct:.0f}%){RESET}")
    print()


# --- Interactive menu ---


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_menu(invoice_files):
    print(f"\n{BOLD}Lab 06 — Structured Data Extraction{RESET}\n")
    for i, filename in enumerate(invoice_files, 1):
        print(f"  {DIM}{i}. Extract {filename}{RESET}")
    print(f"\n  {DIM}a. Extract all invoices{RESET}")
    print(f"  {DIM}v. Validate accuracy (after extracting all){RESET}")
    print(f"  {DIM}c. Clear screen{RESET}")
    print(f"  {DIM}q. Quit{RESET}")
    print()


def main():
    invoice_files = sorted(f for f in os.listdir(INVOICES_DIR) if f.endswith(".txt"))
    results = {}

    clear_screen()
    show_menu(invoice_files)

    while True:
        choice = input(f"{CYAN}Extract > {RESET}").strip()

        if not choice:
            continue
        if choice.lower() in ("q", "quit", "exit"):
            break
        if choice.lower() == "c":
            clear_screen()
            show_menu(invoice_files)
            continue
        if choice.lower() == "a":
            for f in invoice_files:
                result = run_extraction(f)
                if result:
                    results[f] = result
            continue
        if choice.lower() == "v":
            check_accuracy(results)
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(invoice_files):
            filename = invoice_files[int(choice) - 1]
            result = run_extraction(filename)
            if result:
                results[filename] = result
            continue

        print(f"  {RED}Unknown option. Enter a number (1-{len(invoice_files)}), 'a', 'v', or 'q'.{RESET}")


if __name__ == "__main__":
    main()
