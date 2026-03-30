# main.py - Agentic loop with tool execution, prerequisite gate, and PostToolUse hook
import json
import os

import anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.json import JSON

from config import (
    MODEL, MAX_LOOP_ITERATIONS, MAX_REFUND_AMOUNT,
    CYAN, GREEN, YELLOW, RED, DIM, BOLD, RESET,
)
from tools import ALL_TOOLS, TOOL_FUNCTIONS

load_dotenv()

console = Console()


def load_system_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
    with open(prompt_path, "r") as f:
        content = f.read()
    return content


# --- Case facts ---
# [Task 5.1] — extract verified facts from tool results so the model retains them
# even when earlier conversation turns are summarized away


# --- Prerequisite gate ---
# [Task 1.4] — programmatic enforcement: block process_refund until get_customer has run

def check_prerequisite(tool_name, tool_history):
    """Block process_refund unless get_customer has already been called successfully."""
    # TODO: Check if tool_name is "process_refund" and if "get_customer" is NOT
    # in tool_history. If the prerequisite is missing, return a dict with:
    #   error: True
    #   errorCategory: "validation"
    #   isRetryable: True
    #   message: explaining that customer identity must be verified first
    # Otherwise return None to allow the tool call.
    return None


# --- PostToolUse hook ---
# [Task 1.5] — hook intercepts outgoing tool calls for compliance enforcement

def post_tool_use_hook(tool_name, tool_input, tool_result):
    """Intercept tool results to enforce policy rules.

    Checks process_refund calls: if the refund amount exceeds MAX_REFUND_AMOUNT,
    replace the result with a structured error redirecting to escalation.
    """
    # TODO: Check if tool_name is "process_refund" and if tool_input["amount"]
    # exceeds MAX_REFUND_AMOUNT. If it does, return a replacement result dict with:
    #   error: True
    #   errorCategory: "policy_violation"
    #   isRetryable: False
    #   message: explaining the amount exceeds the $500 limit and must be escalated
    #   action: "escalate_to_human"
    # Otherwise return tool_result unchanged.
    return tool_result


# --- Tool execution ---

def execute_tool(tool_name, tool_input, tool_history):
    """Execute a tool call with prerequisite check and post-use hook."""
    # [Task 1.4] — check prerequisite gate before execution
    gate_result = check_prerequisite(tool_name, tool_history)
    if gate_result is not None:
        print(f"  {RED}⛔ Gate blocked {tool_name}: prerequisite not met{RESET}")
        result = gate_result
        return result

    # Execute the tool
    tool_fn = TOOL_FUNCTIONS.get(tool_name)
    if not tool_fn:
        result = {
            "error": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": f"Unknown tool: {tool_name}",
        }
        return result

    raw_result = tool_fn(**tool_input)

    # [Task 1.5] — apply PostToolUse hook after execution
    result = post_tool_use_hook(tool_name, tool_input, raw_result)

    # Track which tools have been called successfully
    if not (isinstance(result, dict) and result.get("error")):
        tool_history.add(tool_name)

    return result


# --- Agentic loop ---
# [Task 1.1] — agentic loop: stop_reason "tool_use" → execute → continue; "end_turn" → stop

def run_agent(user_message):
    """Run the agentic loop for a single user message."""
    client = anthropic.Anthropic()
    system_template = load_system_prompt()

    messages = [{"role": "user", "content": user_message}]
    tool_history = set()
    # [Task 5.1] — case_facts: verified transactional facts injected into system prompt
    case_facts = "No facts collected yet."

    print(f"\n{CYAN}{BOLD}{'='*60}")
    print(f"Customer: {user_message}")
    print(f"{'='*60}{RESET}")

    for iteration in range(MAX_LOOP_ITERATIONS):
        print(f"\n{DIM}--- Iteration {iteration + 1} ---{RESET}")

        # [Task 5.1] — format system prompt template with current case_facts
        system_prompt = system_template.format(case_facts=case_facts)
        print(f"  {DIM}case_facts: {case_facts}{RESET}")

        try:
            with console.status("Processing request...", spinner="dots"):
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=1024,
                    system=system_prompt,
                    tools=ALL_TOOLS,
                    messages=messages,
                )
        except Exception as e:
            error_msg = str(e).lower()
            if "credit" in error_msg or "balance" in error_msg:
                print(f"\n{RED}{BOLD}API credit balance is too low.{RESET}")
                print(f"{DIM}Add credits at https://console.anthropic.com{RESET}")
            elif "usage limit" in error_msg or "rate limit" in error_msg:
                # Extract the human-readable message from the error
                import re
                match = re.search(r'"message"\s*:\s*"([^"]+)"', str(e))
                friendly_msg = match.group(1) if match else str(e)
                print(f"\n{RED}{BOLD}{friendly_msg}{RESET}")
                print(f"{DIM}Check your limits at https://console.anthropic.com{RESET}")
            else:
                print(f"\n{RED}{BOLD}Error: {e}{RESET}")
            return

        print(f"  {DIM}stop_reason: {response.stop_reason}{RESET}")

        # [Task 1.1] — check stop_reason to decide whether to continue or stop
        if response.stop_reason == "end_turn":
            # Extract the final text response
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"\n{GREEN}{BOLD}Agent:{RESET} {GREEN}{block.text}{RESET}")
            break

        if response.stop_reason == "tool_use":
            # Build tool results for all tool_use blocks in this response
            tool_result_blocks = []

            for block in response.content:
                if block.type == "tool_use":
                    print(f"  {YELLOW}Tool call: {block.name}{RESET}")
                    console.print(JSON(json.dumps(block.input, indent=2)), style="dim")

                    result = execute_tool(block.name, block.input, tool_history)
                    print(f"  {DIM}Result:{RESET}")
                    console.print(JSON(json.dumps(result, indent=2)), style="dim")

                    tool_result_block = {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    }
                    tool_result_blocks.append(tool_result_block)

                elif hasattr(block, "text") and block.text:
                    print(f"  {GREEN}Agent (thinking): {block.text}{RESET}")

            # [Task 1.1] — append assistant response and tool results to conversation history
            assistant_message = {"role": "assistant", "content": response.content}
            messages.append(assistant_message)

            user_tool_results = {"role": "user", "content": tool_result_blocks}
            messages.append(user_tool_results)

        else:
            print(f"  {RED}Unexpected stop_reason: {response.stop_reason}{RESET}")
            break

    else:
        print(f"\n{RED}⚠ Agent reached max iterations ({MAX_LOOP_ITERATIONS}){RESET}")

    print(f"\n{DIM}{'='*60}{RESET}\n")


# --- Interactive mode ---

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_menu(test_queries):
    print(f"{BOLD}Lab 01 — Customer Support Resolution Agent{RESET}\n")
    for i, query in enumerate(test_queries, 1):
        print(f"  {DIM}{i}. {query}{RESET}")
    print(f"  {DIM}c. Clear screen{RESET}")
    print(f"  {DIM}q. Quit{RESET}")
    print(f"\n{DIM}Or type a custom message.{RESET}\n")


def main():
    test_queries = [
        "Hi, I'm Maria Santos (CUST-1001). Can you check the status of my order ORD-5501?",
        "I'd like a refund for order ORD-5501. The headphones arrived damaged.",
        "I'm James Chen, customer CUST-1002. I want a refund for my monitor order ORD-5503 — it has dead pixels.",
        "I've been going back and forth on this for days. I want to talk to a real person.",
        "I'm Maria Santos, CUST-1001. My headphones from ORD-5501 arrived damaged and I need a refund. Also, can you check if my other order ORD-5502 has been delivered?",
    ]

    clear_screen()
    show_menu(test_queries)

    while True:
        user_input = input(f"{CYAN}Customer > {RESET}").strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if user_input.lower() == "c":
            clear_screen()
            show_menu(test_queries)
            continue
        if user_input.isdigit() and 1 <= int(user_input) <= len(test_queries):
            user_input = test_queries[int(user_input) - 1]
            print(f"  {DIM}→ {user_input}{RESET}")

        run_agent(user_input)


if __name__ == "__main__":
    main()
