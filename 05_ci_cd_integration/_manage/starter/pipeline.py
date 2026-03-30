# pipeline.py - Simulates a CI pipeline runner using Claude Code

import json
import os
import subprocess
import sys
from datetime import datetime

from rich.console import Console

from config import (
    CYAN, GREEN, YELLOW, RED, DIM, BOLD, RESET,
    PR_FILES_DIR, SCHEMA_PATH, PROMPT_PATH,
    INTEGRATION_PROMPT_PATH, OUTPUT_DIR,
)

console = Console()


def load_pr_files():
    """Read PR source files (excluding test files) and return formatted content."""
    lab_dir = os.path.dirname(os.path.abspath(__file__))
    pr_dir = os.path.join(lab_dir, PR_FILES_DIR)
    files_content = []

    source_files = sorted([
        f for f in os.listdir(pr_dir)
        if f.endswith(".py") and not f.startswith("test_")
    ])

    for filename in source_files:
        filepath = os.path.join(pr_dir, filename)
        with open(filepath, "r") as f:
            content = f.read()
        files_content.append(f"### {filename}\n```python\n{content}\n```")

    result = "\n\n".join(files_content)
    return result


def load_single_file(filename):
    """Read a single PR file and return formatted content."""
    lab_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(lab_dir, PR_FILES_DIR, filename)
    with open(filepath, "r") as f:
        content = f.read()
    result = f"### {filename}\n```python\n{content}\n```"
    return result


def load_prompt():
    """Load the review prompt template."""
    lab_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(lab_dir, PROMPT_PATH)
    with open(prompt_path, "r") as f:
        template = f.read()
    return template


def load_integration_prompt():
    """Load the cross-file integration prompt template."""
    lab_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(lab_dir, INTEGRATION_PROMPT_PATH)
    with open(prompt_path, "r") as f:
        template = f.read()
    return template


def load_schema():
    """Load the JSON schema and return it as a string."""
    lab_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(lab_dir, SCHEMA_PATH)
    with open(schema_path, "r") as f:
        schema = f.read()
    return schema


def build_review_prompt(files_content):
    """Build the full review prompt from template and file contents."""
    template = load_prompt()
    schema = load_schema()
    # Use replace instead of .format() — file contents and few-shot
    # examples may contain literal braces (JSON, f-strings)
    prompt = template.replace("{files_content}", files_content)
    prompt = prompt.replace("{output_schema}", schema)
    return prompt


def run_claude_review(prompt):
    """Run Claude Code in non-interactive mode with -p flag.

    Uses -p to prevent interactive input hangs in CI [Task 3.6].
    Uses --output-format json for structured output [Task 3.6].
    The JSON schema is included in the prompt via template variable.
    """
    lab_dir = os.path.dirname(os.path.abspath(__file__))

    # [Task 3.6] -p flag: non-interactive mode for CI pipelines
    cmd = [
        "claude", "-p",
        "--output-format", "json",
        prompt,
    ]

    print(f"{DIM}Running: claude -p --output-format json{RESET}")

    try:
        with console.status("Reviewing code...", spinner="dots"):
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
                cwd=lab_dir,
            )
    except FileNotFoundError:
        print(f"{RED}Error: 'claude' command not found.{RESET}")
        print(f"{DIM}Make sure Claude Code CLI is installed and in "
              f"your PATH.{RESET}")
        return None
    except subprocess.TimeoutExpired:
        print(f"{RED}Error: Claude Code timed out after 180 "
              f"seconds.{RESET}")
        return None

    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "credit" in stderr.lower() or "balance" in stderr.lower():
            print(f"{RED}API credit balance is too low.{RESET}")
            print(f"{DIM}Check: https://console.anthropic.com{RESET}")
        else:
            print(f"{RED}Claude Code returned error:{RESET}")
            print(f"{DIM}{stderr[:500]}{RESET}")
        return None

    review = parse_review_output(result.stdout)
    if review is None:
        print(f"{RED}Failed to parse review output as JSON.{RESET}")
        raw_preview = result.stdout[:300]
        print(f"{DIM}Raw output: {raw_preview}{RESET}")
    return review


def strip_markdown_fences(text):
    """Remove markdown code fences from a string."""
    stripped = text.strip()
    if stripped.startswith("```"):
        # Remove opening fence (```json or ```)
        first_newline = stripped.index("\n")
        stripped = stripped[first_newline + 1:]
    if stripped.endswith("```"):
        stripped = stripped[:-3].rstrip()
    return stripped


def parse_review_output(raw_output):
    """Parse Claude Code JSON output, handling various envelope formats."""
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        return None

    # Direct schema-conforming output
    if isinstance(data, dict) and "findings" in data:
        return data

    # Wrapped in result field (--output-format json envelope)
    if isinstance(data, dict) and "result" in data:
        result_value = data["result"]
        if isinstance(result_value, dict) and "findings" in result_value:
            return result_value
        if isinstance(result_value, str):
            # Strip markdown fences if present (```json ... ```)
            cleaned = strip_markdown_fences(result_value)
            try:
                parsed = json.loads(cleaned)
                if isinstance(parsed, dict) and "findings" in parsed:
                    return parsed
            except json.JSONDecodeError:
                pass

    return None


def display_review(review):
    """Display review findings with ANSI colors."""
    if review is None:
        return

    findings = review.get("findings", [])
    summary = review.get("summary", "")

    severity_colors = {
        "critical": RED,
        "warning": YELLOW,
        "info": DIM,
    }

    print(f"{BOLD}Review Findings ({len(findings)} issues){RESET}\n")

    for finding in findings:
        severity = finding.get("severity", "info")
        color = severity_colors.get(severity, DIM)
        confidence = finding.get("confidence", "?")
        file_name = finding.get("file", "?")
        line = finding.get("line", "?")

        print(f"  {color}{severity.upper()}{RESET} "
              f"[{confidence}] {file_name}:{line}")
        print(f"    {finding.get('issue', '')}")
        print(f"    {DIM}Category: {finding.get('category', '?')} | "
              f"Fix: {finding.get('suggested_fix', 'N/A')}{RESET}")
        print(f"    {DIM}Reasoning: {finding.get('reasoning', '')}"
              f"{RESET}")
        print()

    if summary:
        print(f"{BOLD}Summary:{RESET} {summary}\n")

    # Count by severity
    counts = {}
    for f in findings:
        sev = f.get("severity", "unknown")
        counts[sev] = counts.get(sev, 0) + 1

    count_parts = [
        f"{RED}{counts.get('critical', 0)} critical{RESET}",
        f"{YELLOW}{counts.get('warning', 0)} warning{RESET}",
        f"{DIM}{counts.get('info', 0)} info{RESET}",
    ]
    print(f"  {BOLD}Totals:{RESET} {', '.join(count_parts)}\n")


def load_latest_review():
    """Load the most recent review from output/."""
    lab_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(lab_dir, OUTPUT_DIR)
    if not os.path.isdir(output_dir):
        return None
    files = sorted([
        f for f in os.listdir(output_dir) if f.endswith(".json")
    ])
    if not files:
        return None
    latest_path = os.path.join(output_dir, files[-1])
    with open(latest_path, "r") as f:
        review = json.load(f)
    return review


def save_review(review):
    """Save review to output/ with timestamp filename."""
    if review is None:
        return
    lab_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(lab_dir, OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    filename = f"review_{timestamp}.json"
    path = os.path.join(output_dir, filename)
    with open(path, "w") as f:
        json.dump(review, f, indent=2)
    print(f"{DIM}Saved to {OUTPUT_DIR}/{filename}{RESET}")


def count_by_severity(findings):
    """Count findings by severity level."""
    counts = {}
    for f in findings:
        sev = f.get("severity", "unknown")
        counts[sev] = counts.get(sev, 0) + 1
    return counts


def compare_reviews(previous, current):
    """Print comparison between two reviews if previous exists."""
    if previous is None or current is None:
        return
    prev_findings = previous.get("findings", [])
    curr_findings = current.get("findings", [])
    prev_counts = count_by_severity(prev_findings)
    curr_counts = count_by_severity(curr_findings)

    delta = len(curr_findings) - len(prev_findings)
    direction = "more" if delta > 0 else "fewer"
    delta_str = f"{abs(delta)} {direction}" if delta != 0 else "same count"

    print(f"{BOLD}Comparison with previous review:{RESET}")
    print(f"  Previous: {len(prev_findings)} findings "
          f"({RED}{prev_counts.get('critical', 0)}C{RESET} "
          f"{YELLOW}{prev_counts.get('warning', 0)}W{RESET} "
          f"{DIM}{prev_counts.get('info', 0)}I{RESET})")
    print(f"  Current:  {len(curr_findings)} findings "
          f"({RED}{curr_counts.get('critical', 0)}C{RESET} "
          f"{YELLOW}{curr_counts.get('warning', 0)}W{RESET} "
          f"{DIM}{curr_counts.get('info', 0)}I{RESET})")
    print(f"  Delta:    {delta_str}\n")


def get_source_files():
    """List PR source files (excluding test files)."""
    lab_dir = os.path.dirname(os.path.abspath(__file__))
    pr_dir = os.path.join(lab_dir, PR_FILES_DIR)
    source_files = sorted([
        f for f in os.listdir(pr_dir)
        if f.endswith(".py") and not f.startswith("test_")
    ])
    return source_files


# --- Review modes ---


def run_single_pass():
    """Run a single-pass review of all PR files."""
    print(f"\n{BOLD}Single-Pass Review{RESET}\n")

    previous = load_latest_review()
    files_content = load_pr_files()
    prompt = build_review_prompt(files_content)

    review = run_claude_review(prompt)
    save_review(review)
    display_review(review)
    compare_reviews(previous, review)

    return review


def run_multi_pass():
    """Run per-file passes plus a cross-file integration pass."""
    # TODO (Step 6): Implement multi-pass review
    # Phase 1 — Per-file local passes:
    #   Loop through each source file from get_source_files().
    #   For each file, call load_single_file() to get its content,
    #   then build_review_prompt() and run_claude_review().
    #   Collect all findings from all per-file passes into a list.
    #   Print which file is being reviewed for each pass.
    #
    # Phase 2 — Cross-file integration pass:
    #   Load the integration prompt template with
    #   load_integration_prompt(). Replace its template variables:
    #   {per_file_findings} with the per-file findings as JSON,
    #   {files_content} with all file contents from load_pr_files(),
    #   {output_schema} with the schema from load_schema().
    #   Run run_claude_review() with this integration prompt.
    #
    # Combine all findings (per-file + cross-file), save with
    # save_review(), and display with display_review().
    print(f"\n{YELLOW}TODO: Implement multi-pass review in "
          f"Step 6.{RESET}\n")


def run_independent_review():
    """Run two independent review instances and compare findings."""
    # TODO (Step 7): Implement independent review comparison
    # 1. Run a first review: build prompt from load_pr_files() and
    #    build_review_prompt(), then run_claude_review().
    # 2. Run a second independent review with the same prompt.
    #    Each claude -p call is a fresh session — no shared context.
    # 3. Compare findings by file:line location. Print:
    #    - How many findings both reviewers agree on
    #    - How many only reviewer 1 found
    #    - How many only reviewer 2 found
    # 4. Print the unique findings from reviewer 2 — these show
    #    the value of an independent review instance.
    # 5. Save the combined findings with save_review().
    print(f"\n{YELLOW}TODO: Implement independent review in "
          f"Step 7.{RESET}\n")


def format_as_pr_comments():
    """Format the latest review as simulated PR inline comments."""
    review = load_latest_review()

    if review is None:
        print(f"\n{RED}No review results found. Run a review "
              f"first.{RESET}\n")
        return

    findings = review.get("findings", [])

    print(f"\n{BOLD}Simulated PR Inline Comments{RESET}\n")
    print(f"{DIM}{'─' * 60}{RESET}")

    for finding in findings:
        file_name = finding.get("file", "unknown")
        line = finding.get("line", "?")
        severity = finding.get("severity", "info")
        issue = finding.get("issue", "")
        fix = finding.get("suggested_fix", "")
        confidence = finding.get("confidence", "?")

        severity_badge = f"[{severity.upper()}]"
        confidence_badge = f"(confidence: {confidence})"

        print(f"\n  {BOLD}{file_name}:{line}{RESET} "
              f"{severity_badge} {confidence_badge}")
        print(f"  {issue}")
        if fix:
            print(f"  {GREEN}Suggested: {fix}{RESET}")
        print(f"{DIM}{'─' * 60}{RESET}")

    print(f"\n{DIM}{len(findings)} comment(s) would be posted to "
          f"the PR.{RESET}\n")


# --- Interactive mode ---


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_menu():
    print(f"{BOLD}Lab 05 — Claude Code for Continuous Integration{RESET}\n")
    print(f"  {DIM}1. Run code review (single pass){RESET}")
    print(f"  {DIM}2. Run code review (multi-pass)     "
          f"[Step 6]{RESET}")
    print(f"  {DIM}3. Run independent review            "
          f"[Step 7]{RESET}")
    print(f"  {DIM}4. Format last review as PR comments{RESET}")
    print(f"  {DIM}c. Clear screen{RESET}")
    print(f"  {DIM}q. Quit{RESET}")
    print()


def main():
    clear_screen()
    show_menu()

    while True:
        user_input = input(f"{CYAN}Pipeline > {RESET}").strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if user_input.lower() == "c":
            clear_screen()
            show_menu()
            continue

        if user_input == "1":
            run_single_pass()
        elif user_input == "2":
            run_multi_pass()
        elif user_input == "3":
            run_independent_review()
        elif user_input == "4":
            format_as_pr_comments()
        else:
            print(f"{DIM}Choose 1-4, c, or q.{RESET}")


if __name__ == "__main__":
    main()
