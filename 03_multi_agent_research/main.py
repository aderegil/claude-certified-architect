# main.py - Multi-agent research system: coordinator with specialized subagents
import asyncio
import json
import os
import time

from claude_agent_sdk import (
    query, ClaudeAgentOptions, HookMatcher,
    create_sdk_mcp_server, tool,
)
from dotenv import load_dotenv

from agents import build_agents
from config import (
    CYAN, GREEN, YELLOW, RED, DIM, BOLD, RESET,
)
from data import ARTICLES, DOCUMENTS, TIMEOUT_URL

load_dotenv()


# --- Prompt loading ---

def load_prompt(filename):
    """Load a prompt template from the prompts/ directory."""
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", filename)
    with open(prompt_path, "r") as f:
        content = f.read()
    return content


# --- MCP tools for research ---
# [Task 2.1] — clear descriptions differentiate each tool's purpose, inputs,
# outputs, and when to use it versus alternatives

@tool(
    "web_search",
    (
        "Search for research articles on a topic. Returns a list of articles "
        "with title, URL, source name, date, and excerpt. Use this to find "
        "relevant sources for a research topic. Input: a search query string "
        "and max_results (integer, how many results to return). Example: "
        "web_search(query='AI healthcare diagnostics', max_results=5). "
        "Returns articles sorted by relevance to the query keywords. "
        "This tool SEARCHES for articles — use fetch_document to get full content."
    ),
    {"query": str, "max_results": int},
)
async def web_search(args):
    """Search mock articles by keyword matching."""
    search_query = args.get("query", "").lower()
    max_results = args.get("max_results", 5)

    # Score articles by keyword overlap with search query
    matches = []
    query_words = search_query.split()
    for article in ARTICLES:
        keywords = article["keywords"]
        score = sum(
            1 for word in query_words
            if any(word in kw for kw in keywords)
        )
        if score > 0:
            matches.append((score, article))

    matches.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, article in matches[:max_results]:
        result = {
            "title": article["title"],
            "url": article["url"],
            "source": article["source"],
            "date": article["date"],
            "excerpt": article["excerpt"],
        }
        results.append(result)

    response_text = json.dumps(results, indent=2)
    content = [{"type": "text", "text": response_text}]
    response = {"content": content}
    return response


@tool(
    "fetch_document",
    (
        "Fetch the full content of a research document by URL. Returns the "
        "document title, source name, publication date, and full text content "
        "for detailed analysis. Use this AFTER web_search to get detailed "
        "information from specific articles. Input: a document URL from search "
        "results. Note: some restricted-access URLs may timeout or return errors. "
        "This tool FETCHES full content — use web_search to find articles first."
    ),
    {"url": str},
)
async def fetch_document(args):
    """Fetch mock document content by URL."""
    url = args.get("url", "")

    # [Task 5.3] — simulated timeout for error propagation testing
    if url == TIMEOUT_URL:
        # TODO [Task 2.2, 5.3]: Return a structured error response that gives
        # the coordinator enough context to make an intelligent recovery decision.
        #
        # Replace this generic error with a structured response containing:
        #   failure_type: "timeout"
        #   attempted_url: the URL that was attempted
        #   partial_results: the article excerpt from search results (find it
        #     in ARTICLES by matching the URL)
        #   alternatives: a suggestion like "Use the search excerpt as a partial
        #     source, or search for alternative articles on this subtopic"
        #
        # Return format: {"content": [{"type": "text", "text": json.dumps(error_data)}], "isError": True}
        #
        # Currently returns a generic error — the coordinator receives "Request
        # timed out" with no context about what was attempted, what partial data
        # is available, or what alternatives exist. This prevents intelligent
        # recovery. [Task 5.3]
        error_text = "Error: Request timed out."
        content = [{"type": "text", "text": error_text}]
        response = {"content": content, "isError": True}
        return response

    # Normal document fetch
    document = DOCUMENTS.get(url)
    if not document:
        error_data = {
            "error": True,
            "failure_type": "not_found",
            "attempted_url": url,
            "message": f"No document found at {url}",
        }
        error_text = json.dumps(error_data, indent=2)
        content = [{"type": "text", "text": error_text}]
        response = {"content": content, "isError": True}
        return response

    doc_data = {
        "title": document["title"],
        "source": document["source"],
        "date": document["date"],
        "content": document["content"],
    }
    response_text = json.dumps(doc_data, indent=2)
    content = [{"type": "text", "text": response_text}]
    response = {"content": content}
    return response


# --- Hook callbacks for real-time observability ---
# [Task 1.5] — PreToolUse/PostToolUse hooks intercept tool calls for logging

_start_time = 0.0
_case_label = "custom"
_last_api_error = ""

# The currently active agent (set when Agent tool is called)
_current_agent = "coordinator"

# --- Lab convenience: tool visibility and violation detection ---
# NOTE: The SDK hooks do not expose which tools a subagent has access to.
# The _agents dict and _EXPECTED_TOOLS map below are lab conveniences that
# read from our own AgentDefinition objects — not an SDK-provided feature.
# In production, you would track tool assignments through your own registry.
_agents = {}

_EXPECTED_TOOLS = {
    "search-agent": {"mcp__research__web_search"},
    "analysis-agent": {"mcp__research__fetch_document"},
    "synthesis-agent": set(),
    "report-agent": set(),
}


def _elapsed():
    """Return elapsed seconds since research started."""
    elapsed = time.time() - _start_time
    return f"[{elapsed:5.1f}s]"


async def on_pre_tool_use(hook_input, tool_use_id, context):
    """Log every tool call as it happens — gives real-time feedback."""
    global _current_agent
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Subagent spawn — register which agent this tool_use_id belongs to
    if tool_name in ("Task", "Agent"):
        agent_type = tool_input.get("subagent_type", "unknown")
        desc = tool_input.get("description", "")
        _current_agent = agent_type
        print(f"  {YELLOW}{_elapsed()} ↳ Spawning: {agent_type}{RESET}", flush=True)
        if desc:
            print(f"    {DIM}{desc}{RESET}", flush=True)
        # Show which tools this agent has access to
        agent_def = _agents.get(agent_type)
        if agent_def:
            agent_tools = getattr(agent_def, "tools", None)
            if agent_tools is None:
                print(f"    {DIM}Tools: ALL (no restriction){RESET}", flush=True)
            elif len(agent_tools) == 0:
                print(f"    {DIM}Tools: none{RESET}", flush=True)
            else:
                short = [t.replace("mcp__research__", "") for t in agent_tools]
                print(f"    {DIM}Tools: {', '.join(short)}{RESET}", flush=True)
    # MCP tool call or built-in tool — label with agent and flag violations
    else:
        is_mcp = tool_name.startswith("mcp__research__")
        short_name = tool_name.replace("mcp__research__", "") if is_mcp else tool_name
        input_summary = _format_tool_input(short_name, tool_input) if is_mcp else ""
        label = _current_agent

        # Check if this agent should be using this tool
        expected = _EXPECTED_TOOLS.get(label)
        is_violation = expected is not None and tool_name not in expected

        if is_violation:
            print(
                f"    {DIM}{_elapsed()} [{label}] → {short_name}"
                f"{input_summary}  {RESET}{BOLD}{RED}← ⚠ VIOLATION: should not use "
                f"{short_name}{RESET}",
                flush=True,
            )
        else:
            print(
                f"    {DIM}{_elapsed()} [{label}] → {short_name}"
                f"{input_summary}{RESET}",
                flush=True,
            )

    result = {"continue_": True}
    return result


async def on_post_tool_use(hook_input, tool_use_id, context):
    """Log tool completion with a brief result summary."""
    tool_name = hook_input.get("tool_name", "")
    tool_response = hook_input.get("tool_response", "")

    # When an Agent/Task tool completes, revert to coordinator context
    if tool_name in ("Task", "Agent"):
        global _current_agent
        _current_agent = "coordinator"

    elif tool_name.startswith("mcp__research__"):
        short_name = tool_name.replace("mcp__research__", "")
        resp_str = str(tool_response)
        is_error = (
            "isError" in resp_str
            or "Error:" in resp_str
            or '"error": true' in resp_str.lower()
            or "failure_type" in resp_str
        )
        if is_error:
            print(f"    {RED}{_elapsed()}   ✗ {short_name} — error{RESET}", flush=True)
        else:
            size = len(resp_str)
            print(f"    {DIM}{_elapsed()}   ✓ {short_name} ({size} chars){RESET}", flush=True)

    result = {"continue_": True}
    return result


def _format_tool_input(tool_name, tool_input):
    """Format tool input for concise display."""
    if tool_name == "web_search":
        q = tool_input.get("query", "")
        return f'("{q}")'
    if tool_name == "fetch_document":
        url = tool_input.get("url", "")
        # Show just the domain for brevity
        short_url = url.split("//")[-1].split("/")[0] if "//" in url else url
        return f" ({short_url})"
    return ""


# --- Message display ---

def display_message(message):
    """Display a streamed message from the coordinator or its subagents."""
    is_subagent = (
        hasattr(message, "parent_tool_use_id") and message.parent_tool_use_id
    )

    # Check for content blocks (assistant messages)
    global _last_api_error
    if hasattr(message, "content") and message.content:
        for block in message.content:
            if hasattr(block, "text") and block.text:
                text = block.text
                # Capture API errors silently — the exception handler shows them
                if text.lower().startswith("api error"):
                    _last_api_error = text
                    continue
                if len(text) > 300:
                    text = text[:300] + "..."
                label = "[subagent]" if is_subagent else "[coordinator]"
                print(f"    {DIM}{label} {text}{RESET}")

    # Print final result and save report to file
    if hasattr(message, "result") and message.result:
        result_text = message.result

        # Skip saving and banner if the result is an error, not a real report
        error_keywords = [
            "credit balance", "usage limits", "api error",
            "exit code", "fatal", "rate limit",
        ]
        is_error = any(kw in result_text.lower() for kw in error_keywords)

        if is_error:
            return

        print(f"\n{GREEN}{BOLD}{'═' * 60}")
        print(f"Research Complete")
        print(f"{'═' * 60}{RESET}")
        print(f"{GREEN}{result_text}{RESET}")

        # Save report to timestamped file
        from datetime import datetime
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%y%m%d-%H%M")
        filename = f"{_case_label}-{timestamp}.md"
        report_path = os.path.join(output_dir, filename)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(result_text)
        print(f"\n{DIM}Report saved to: output/{filename}{RESET}")


# --- Research runner ---

async def run_research(topic):
    """Run the multi-agent research system on a topic."""
    # [Task 1.3] — build subagent definitions with AgentDefinition
    agents = build_agents()

    # Create MCP server with research tools
    research_server = create_sdk_mcp_server(
        name="research",
        version="1.0.0",
        tools=[web_search, fetch_document],
    )

    # Load coordinator system prompt
    coordinator_system = load_prompt("coordinator.txt")

    # Build the user prompt for the coordinator
    research_prompt = (
        f"Research the following topic and produce a comprehensive "
        f"cited report: {topic}"
    )

    global _start_time, _current_agent, _agents
    _start_time = time.time()
    _current_agent = "coordinator"
    _agents = agents

    print(f"\n{CYAN}{BOLD}{'=' * 60}")
    print(f"Research Topic: {topic}")
    print(f"{'=' * 60}{RESET}")
    print(f"{DIM}Coordinator delegating to subagents...{RESET}\n")

    # [Task 1.5] — hooks intercept tool calls for real-time observability
    hooks = {
        "PreToolUse": [
            HookMatcher(matcher=None, hooks=[on_pre_tool_use]),
        ],
        "PostToolUse": [
            HookMatcher(matcher=None, hooks=[on_post_tool_use]),
        ],
    }

    # [Task 1.2] — hub-and-spoke: coordinator manages all subagent communication
    # The SDK handles the agentic loop internally — no manual
    # while stop_reason == "tool_use" loop needed
    import sys, io
    _original_stderr = sys.stderr
    try:
        sys.stderr = io.StringIO()
        async for message in query(
            prompt=research_prompt,
            options=ClaudeAgentOptions(
                system_prompt=coordinator_system,
                # [Task 2.3] — coordinator only needs Agent tool to spawn subagents;
                # MCP tools are available to subagents via their tools lists
                allowed_tools=["Agent"],
                agents=agents,
                mcp_servers={"research": research_server},
                permission_mode="bypassPermissions",
                hooks=hooks,
                max_turns=15,
                effort="low",
            ),
        ):
            display_message(message)
    except Exception:
        # Use the captured API error if available, otherwise generic message
        if _last_api_error:
            # Extract the human-readable message from the JSON
            try:
                import re
                match = re.search(r'"message"\s*:\s*"([^"]+)"', _last_api_error)
                friendly_msg = match.group(1) if match else _last_api_error
            except Exception:
                friendly_msg = _last_api_error
            print(f"\n{RED}{BOLD}{friendly_msg}{RESET}")
            print(f"{DIM}Check your limits at https://console.anthropic.com{RESET}")
        else:
            print(f"\n{RED}{BOLD}An error occurred during research.{RESET}")
    finally:
        sys.stderr = _original_stderr

    elapsed = time.time() - _start_time
    print(f"\n{DIM}{'=' * 60}")
    print(f"Completed in {elapsed:.1f}s")
    print(f"{'=' * 60}{RESET}\n")


# --- Interactive mode ---

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_menu(test_queries):
    print(f"{BOLD}Lab 03 — Multi-Agent Research System{RESET}\n")
    for i, query_text in enumerate(test_queries, 1):
        print(f"  {DIM}{i}. {query_text}{RESET}")
    print(f"  {DIM}c. Clear screen{RESET}")
    print(f"  {DIM}q. Quit{RESET}")
    print(f"\n{DIM}Or type a custom research topic.{RESET}\n")


def main():
    test_queries = [
        "Research the impact of artificial intelligence on healthcare diagnostics and treatment",
        "Research AI in healthcare, including surgical planning from restricted-access journals",
        "Research only AI in radiology image analysis — nothing else",
    ]

    clear_screen()
    show_menu(test_queries)

    while True:
        user_input = input(f"{CYAN}Research topic > {RESET}").strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if user_input.lower() == "c":
            clear_screen()
            show_menu(test_queries)
            continue
        global _case_label
        if user_input.isdigit() and 1 <= int(user_input) <= len(test_queries):
            _case_label = f"case-{user_input}"
            user_input = test_queries[int(user_input) - 1]
            print(f"  {DIM}→ {user_input}{RESET}")
        else:
            _case_label = "custom"

        asyncio.run(run_research(user_input))


if __name__ == "__main__":
    main()
