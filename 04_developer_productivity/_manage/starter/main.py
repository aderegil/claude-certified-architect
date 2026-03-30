# main.py - Developer productivity agent: explore and understand codebases
import asyncio
import io
import os
import sys

from claude_agent_sdk import (
    query, ClaudeAgentOptions, HookMatcher,
    create_sdk_mcp_server,  # used in Step 4
)
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

from config import CYAN, GREEN, YELLOW, RED, DIM, BOLD, RESET

_console = Console()

load_dotenv()
os.system("cls" if os.name == "nt" else "clear")


# --- Prompt loading ---

def load_prompt(filename):
    """Load a prompt template from the prompts/ directory."""
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", filename)
    with open(prompt_path, "r") as f:
        content = f.read()
    return content


# --- Hook callbacks for tool observability ---

async def on_pre_tool_use(hook_input, tool_use_id, context):
    """Log every tool call as it happens — real-time feedback."""
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    if tool_name in ("Task", "Agent"):
        agent_type = tool_input.get("subagent_type", "unknown")
        desc = tool_input.get("description", "")
        print(f"  {YELLOW}↳ Spawning: {agent_type}{RESET}", flush=True)
        if desc:
            print(f"    {DIM}{desc}{RESET}", flush=True)
    elif tool_name.startswith("mcp__"):
        short = tool_name.split("__")[-1]
        input_summary = ""
        if "query" in tool_input:
            input_summary = f'("{tool_input["query"]}")'
        print(f"    {DIM}→ {short}{input_summary}{RESET}", flush=True)
    else:
        short_input = _format_tool_input(tool_name, tool_input)
        print(f"    {DIM}→ {tool_name}{short_input}{RESET}", flush=True)

    result = {"continue_": True}
    return result


async def on_post_tool_use(hook_input, tool_use_id, context):
    """Log tool completion."""
    tool_name = hook_input.get("tool_name", "")

    if tool_name in ("Task", "Agent"):
        print(f"  {DIM}← subagent returned{RESET}", flush=True)

    result = {"continue_": True}
    return result


def _format_tool_input(tool_name, tool_input):
    """Format tool input for concise display."""
    if tool_name == "Grep":
        pattern = tool_input.get("pattern", "")
        return f'("{pattern}")'
    if tool_name == "Glob":
        pattern = tool_input.get("pattern", "")
        return f'("{pattern}")'
    if tool_name == "Read":
        path = tool_input.get("file_path", "")
        short = os.path.basename(path) if path else ""
        return f" ({short})"
    if tool_name in ("Write", "Edit"):
        path = tool_input.get("file_path", "")
        short = os.path.basename(path) if path else ""
        return f" ({short})"
    return ""


# --- Message display ---

_last_api_error = ""
_result_printed = False


def display_message(message):
    """Display messages from the agent."""
    global _last_api_error, _result_printed

    is_subagent = (
        hasattr(message, "parent_tool_use_id") and message.parent_tool_use_id
    )

    if hasattr(message, "content") and message.content:
        for block in message.content:
            if hasattr(block, "text") and block.text:
                text = block.text
                if text.lower().startswith("api error"):
                    _last_api_error = text
                    continue
                if is_subagent:
                    if len(text) > 200:
                        text = text[:200] + "..."
                    print(f"    {DIM}[explore] {text}{RESET}")
                else:
                    print()
                    md = Markdown(text)
                    _console.print(md)
                    _result_printed = True

    # result is the final complete answer — skip if we already
    # rendered from content blocks to avoid double output
    if hasattr(message, "result") and message.result:
        if _result_printed:
            return
        result_text = message.result
        error_keywords = [
            "credit balance", "usage limits", "api error",
            "exit code", "fatal", "rate limit",
        ]
        is_error = any(kw in result_text.lower() for kw in error_keywords)
        if is_error:
            return
        print()
        md = Markdown(result_text)
        _console.print(md)


# --- Agent runner ---

async def run_query(user_query):
    """Run the developer productivity agent on a question."""
    global _last_api_error, _result_printed
    _last_api_error = ""
    _result_printed = False

    lab_dir = os.path.dirname(os.path.abspath(__file__))
    system_prompt = load_prompt("system_prompt.txt")

    # --- Scratchpad ---
    # TODO [Step 6, Task 5.4]: Enable scratchpad persistence.
    # Replace the TWO lines below with:
    #
    # scratchpad_path = os.path.join(lab_dir, "scratch.md")
    # if os.path.exists(scratchpad_path):
    #     with open(scratchpad_path, "r") as f:
    #         scratchpad_content = f.read()
    # else:
    #     scratchpad_content = "No previous findings."
    #
    # scratchpad_instructions = (
    #     "After answering each question, write a brief summary of your "
    #     "key findings to scratch.md. Include file paths, function "
    #     "locations, and architectural insights you discovered. Before "
    #     "answering a new question, review the scratchpad above for "
    #     "relevant prior findings that may save you from re-exploring."
    # )
    scratchpad_content = "No previous findings."  # ← replace this
    scratchpad_instructions = ""                   # ← replace this

    # --- MCP tool guidance in system prompt ---
    # TODO [Step 4, Task 2.1]: Add guidance so the agent knows when to use
    # the MCP docs tool instead of Grep. Without this, the system prompt's
    # "use Grep for content search" wording biases the agent toward Grep
    # even when lookup_docs has a better description.
    #
    # mcp_tool_guidance = (
    #     "- **lookup_docs** (MCP) — search project documentation: "
    #     "architecture decisions, API specs, onboarding guides, tech debt. "
    #     "Returns structured results with title, section, and content. "
    #     "Use this for documentation questions; use Grep for source code.\n"
    # )
    mcp_tool_guidance = ""

    # --- Explore subagent guidance in system prompt ---
    # TODO [Step 5, Task 1.3]: Add guidance so the agent knows when to
    # delegate to the Explore subagent. Without this, the agent handles
    # all questions directly with Grep/Read even when delegation would
    # be more appropriate.
    #
    # explore_guidance = (
    #     "## Delegation\n\n"
    #     "For complex questions that require reading multiple files, "
    #     "tracing dependencies across modules, or analyzing architecture "
    #     "patterns, delegate to the **explore** subagent using the Agent "
    #     "tool. The subagent investigates autonomously and returns a "
    #     "structured summary. Use direct Grep/Read only for simple, "
    #     "single-file lookups.\n"
    # )
    explore_guidance = ""

    system_prompt = system_prompt.format(
        scratchpad_content=scratchpad_content,
        scratchpad_instructions=scratchpad_instructions,
        mcp_tool_guidance=mcp_tool_guidance,
        explore_guidance=explore_guidance,
    )

    # --- MCP documentation server ---
    # TODO [Step 4, Task 2.4]: Create the MCP documentation server and
    # add it to the ClaudeAgentOptions below.
    # Import the lookup_docs tool and wire it up:
    #
    # from tools import lookup_docs
    # docs_server = create_sdk_mcp_server(
    #     name="docs",
    #     version="1.0.0",
    #     tools=[lookup_docs],
    # )

    # --- Explore subagent ---
    # TODO [Step 5, Task 1.3]: Build the Explore subagent and add it to
    # the ClaudeAgentOptions below.
    # Import and build the subagent definition:
    #
    # from agents import build_explore_agent
    # agents = build_explore_agent()

    # --- Tool list ---
    # [Task 2.5] — built-in tools for codebase exploration
    allowed_tools = ["Read", "Write", "Edit", "Grep", "Glob"]
    # TODO [Step 4]: allowed_tools.append("mcp__docs__lookup_docs")
    # TODO [Step 5]: allowed_tools.append("Agent")

    hooks = {
        "PreToolUse": [
            HookMatcher(matcher=None, hooks=[on_pre_tool_use]),
        ],
        "PostToolUse": [
            HookMatcher(matcher=None, hooks=[on_post_tool_use]),
        ],
    }

    print(f"\n{DIM}Thinking...{RESET}\n")

    _original_stderr = sys.stderr
    try:
        sys.stderr = io.StringIO()
        async for message in query(
            prompt=user_query,
            options=ClaudeAgentOptions(
                system_prompt=system_prompt,
                allowed_tools=allowed_tools,
                # TODO [Step 4]: mcp_servers={"docs": docs_server},
                # TODO [Step 5]: agents=agents,
                permission_mode="bypassPermissions",
                hooks=hooks,
                max_turns=10,
                effort="low",
                cwd=lab_dir,
            ),
        ):
            display_message(message)
    except Exception:
        if _last_api_error:
            try:
                import re
                match = re.search(r'"message"\s*:\s*"([^"]+)"', _last_api_error)
                friendly_msg = match.group(1) if match else _last_api_error
            except Exception:
                friendly_msg = _last_api_error
            print(f"\n{RED}{BOLD}{friendly_msg}{RESET}")
            print(f"{DIM}Check your limits at https://console.anthropic.com{RESET}")
        else:
            print(f"\n{RED}{BOLD}An error occurred.{RESET}")
    finally:
        sys.stderr = _original_stderr


# --- Interactive mode ---

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_menu(test_queries):
    print(f"{BOLD}Lab 04 — Developer Productivity with Claude{RESET}\n")
    for i, q in enumerate(test_queries, 1):
        print(f"  {DIM}{i}. {q}{RESET}")
    print(f"  {DIM}c. Clear screen{RESET}")
    print(f"  {DIM}q. Quit{RESET}")
    print(f"\n{DIM}Or type a custom question about the storefront codebase.{RESET}\n")


def main():
    test_queries = [
        "Find all test files in the storefront project",
        "Find all callers of validate_email in the storefront codebase",
        "Trace validate_email — where is it defined, re-exported, and called?",
        "Refactor middleware.py to extract the duplicated pattern into a constant",
        "What is the known technical debt in the storefront project?",
        "What is the overall architecture of the storefront app?",
    ]

    clear_screen()
    show_menu(test_queries)

    while True:
        user_input = input(f"{CYAN}Question > {RESET}").strip()

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

        coro = run_query(user_input)
        asyncio.run(coro)
        print()


if __name__ == "__main__":
    main()
