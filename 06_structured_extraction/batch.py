# batch.py - Message Batches API for bulk invoice extraction
#
# [Task 4.5] — Batch processing: 50% cost reduction, 24-hour window,
# no latency SLA. Use for non-blocking overnight runs, not for
# blocking workflows like pre-merge checks.
import json
import os
import time

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
from dotenv import load_dotenv

from config import (
    MODEL,
    CYAN,
    GREEN,
    YELLOW,
    RED,
    DIM,
    BOLD,
    RESET,
)
from schema import extract_invoice_schema
from data import FEW_SHOT_EXAMPLES

load_dotenv()

INVOICES_DIR = os.path.join(os.path.dirname(__file__), "invoices")
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")


def load_extraction_prompt():
    """Load and format the system prompt with few-shot examples."""
    prompt_path = os.path.join(PROMPTS_DIR, "extraction_prompt.txt")
    with open(prompt_path, "r") as f:
        template = f.read()

    # Format few-shot examples (same logic as main.py)
    formatted = []
    for ex in FEW_SHOT_EXAMPLES:
        extraction_json = json.dumps(ex["extraction"], indent=2)
        block = (
            f"<example>\n"
            f"<invoice>\n{ex['document']}\n</invoice>\n"
            f"<correct_extraction>\n{extraction_json}\n</correct_extraction>\n"
            f"</example>"
        )
        formatted.append(block)
    few_shot_text = "\n\n".join(formatted)
    prompt = template.format(few_shot_examples=few_shot_text)
    return prompt


def build_batch_requests():
    """Build a list of batch Request objects, one per invoice file."""
    system_prompt = load_extraction_prompt()
    invoice_files = sorted(f for f in os.listdir(INVOICES_DIR) if f.endswith(".txt"))
    requests = []

    for filename in invoice_files:
        invoice_path = os.path.join(INVOICES_DIR, filename)
        with open(invoice_path, "r") as f:
            invoice_text = f.read()

        # [Task 4.5] — custom_id ties each result back to its source file
        custom_id = filename.replace(".txt", "")

        user_content = (
            "Extract all fields from this invoice:\n\n"
            f"<invoice>\n{invoice_text}\n</invoice>"
        )
        params = MessageCreateParamsNonStreaming(
            model=MODEL,
            max_tokens=4096,
            system=system_prompt,
            tools=[extract_invoice_schema],
            tool_choice={"type": "tool", "name": "extract_invoice"},
            messages=[{"role": "user", "content": user_content}],
        )
        request = Request(custom_id=custom_id, params=params)
        requests.append(request)

    return requests


def preview_batch():
    """Show what the batch submission would look like (dry run)."""
    requests = build_batch_requests()
    print(f"\n{CYAN}{BOLD}Batch Preview — {len(requests)} requests{RESET}\n")
    for req in requests:
        msg_content = req["params"]["messages"][0]["content"]
        preview = msg_content[:80].replace("\n", " ")
        print(f"  {DIM}custom_id: {req['custom_id']:<20} | {preview}...{RESET}")
    print(f"\n  {DIM}Model: {MODEL}{RESET}")
    print(f"  {DIM}Tool: extract_invoice (forced){RESET}")
    print(f"  {DIM}Estimated cost: ~50% of standard API pricing{RESET}\n")
    return requests


def submit_batch():
    """Submit the batch to the Message Batches API."""
    client = anthropic.Anthropic()
    requests = build_batch_requests()

    print(f"\n{CYAN}{BOLD}Submitting batch ({len(requests)} invoices)...{RESET}")
    try:
        batch = client.messages.batches.create(requests=requests)
    except Exception as exc:
        error_msg = str(exc).lower()
        if "credit" in error_msg or "balance" in error_msg:
            print(f"\n{RED}{BOLD}API credit balance is too low.{RESET}")
            print(f"{DIM}Add credits at https://console.anthropic.com{RESET}")
        else:
            print(f"\n{RED}{BOLD}  API error: {exc}{RESET}")
        return None

    print(f"\n  {GREEN}Batch created: {batch.id}{RESET}")
    print(f"  {DIM}Status: {batch.processing_status}{RESET}")
    print(f"  {DIM}Save this batch ID to check status and retrieve results.{RESET}\n")
    return batch.id


def check_status(batch_id):
    """Check the processing status of a batch."""
    client = anthropic.Anthropic()
    try:
        batch = client.messages.batches.retrieve(batch_id)
    except Exception as exc:
        print(f"\n{RED}{BOLD}  API error: {exc}{RESET}")
        return None

    print(f"\n{CYAN}{BOLD}Batch Status: {batch_id}{RESET}")
    print(f"  {DIM}Status: {batch.processing_status}{RESET}")
    counts = batch.request_counts
    print(f"  {DIM}Processing: {counts.processing}{RESET}")
    print(f"  {GREEN}Succeeded:  {counts.succeeded}{RESET}")
    print(f"  {RED}Errored:    {counts.errored}{RESET}")
    print(f"  {YELLOW}Expired:    {counts.expired}{RESET}")
    print(f"  {DIM}Canceled:   {counts.canceled}{RESET}\n")
    return batch.processing_status


def retrieve_results(batch_id):
    """Stream results from a completed batch and display extractions."""
    client = anthropic.Anthropic()

    print(f"\n{CYAN}{BOLD}Retrieving results for {batch_id}...{RESET}\n")
    try:
        results_iter = client.messages.batches.results(batch_id)
    except Exception as exc:
        print(f"\n{RED}{BOLD}  API error: {exc}{RESET}")
        return [], []

    succeeded = []
    failed = []

    for result in results_iter:
        cid = result.custom_id

        if result.result.type == "succeeded":
            message = result.result.message
            extraction = None
            for block in message.content:
                if block.type == "tool_use":
                    extraction = block.input
                    break

            if extraction:
                succeeded.append({"custom_id": cid, "extraction": extraction})
                total = extraction.get("stated_total", "N/A")
                vendor = extraction.get("vendor_name", "Unknown")
                print(f"  {GREEN}✓ {cid:<20} | {vendor:<35} | ${total}{RESET}")
            else:
                failed.append({"custom_id": cid, "reason": "no tool_use block"})
                print(f"  {RED}✗ {cid:<20} | no extraction in response{RESET}")

        elif result.result.type == "errored":
            error_msg = result.result.error.message
            failed.append({"custom_id": cid, "reason": error_msg})
            print(f"  {RED}✗ {cid:<20} | {error_msg}{RESET}")

        elif result.result.type == "expired":
            failed.append({"custom_id": cid, "reason": "expired"})
            print(f"  {YELLOW}⏰ {cid:<20} | request expired{RESET}")

        elif result.result.type == "canceled":
            failed.append({"custom_id": cid, "reason": "canceled"})
            print(f"  {DIM}— {cid:<20} | canceled{RESET}")

    print(f"\n  {BOLD}Results: {len(succeeded)} succeeded, {len(failed)} failed{RESET}")

    # [Task 4.5] — resubmit failures by custom_id
    if failed:
        print(f"\n  {YELLOW}Failed requests:{RESET}")
        for f_item in failed:
            print(f"    {YELLOW}- {f_item['custom_id']}: {f_item['reason']}{RESET}")
        print(f"\n  {DIM}To resubmit failures, run the batch again with only the")
        print(f"  failed custom_ids. For oversized documents, consider chunking")
        print(f"  the input before resubmission.{RESET}")

    print()
    return succeeded, failed


# --- Interactive menu ---


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_menu():
    print(f"\n{BOLD}Lab 06 — Batch Processing{RESET}\n")
    print(f"  {DIM}1. Preview batch requests (dry run){RESET}")
    print(f"  {DIM}2. Submit batch{RESET}")
    print(f"  {DIM}3. Check batch status{RESET}")
    print(f"  {DIM}4. Retrieve results{RESET}")
    print(f"  {DIM}c. Clear screen{RESET}")
    print(f"  {DIM}q. Quit{RESET}")
    print()


def main():
    clear_screen()
    show_menu()
    batch_id = None

    while True:
        choice = input(f"{CYAN}Batch > {RESET}").strip()

        if not choice:
            continue
        if choice.lower() in ("q", "quit", "exit"):
            break
        if choice.lower() == "c":
            clear_screen()
            show_menu()
            continue
        if choice == "1":
            preview_batch()
        elif choice == "2":
            batch_id = submit_batch()
        elif choice == "3":
            if not batch_id:
                batch_id = input(f"  {DIM}Batch ID: {RESET}").strip()
            if batch_id:
                check_status(batch_id)
        elif choice == "4":
            if not batch_id:
                batch_id = input(f"  {DIM}Batch ID: {RESET}").strip()
            if batch_id:
                retrieve_results(batch_id)
        else:
            print(f"  {RED}Unknown option.{RESET}")


if __name__ == "__main__":
    main()
