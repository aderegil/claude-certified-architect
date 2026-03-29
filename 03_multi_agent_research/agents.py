# agents.py - Subagent definitions for multi-agent research system

import inspect
import json
from typing import get_type_hints

import anthropic

from config import MODEL, SUBAGENT_MAX_TOKENS, SIMULATE_SEARCH_TIMEOUT
from data import SEARCH_RESULTS, ANALYSIS_FINDINGS, TIMEOUT_ERROR


# --- Tool decorator ---
# Generates API-compatible tool schemas from decorated functions (task 2.1)

def tool(description, param_descriptions=None):
    """Decorator that attaches an API-compatible tool schema to a function."""
    def decorator(func):
        hints = get_type_hints(func)
        params = inspect.signature(func).parameters

        properties = {}
        required = []
        for name, param in params.items():
            param_type = hints.get(name, str)
            type_map = {str: "string", int: "integer", float: "number", bool: "boolean"}
            prop = {"type": type_map.get(param_type, "string")}
            if param_descriptions and name in param_descriptions:
                prop["description"] = param_descriptions[name]
            properties[name] = prop
            if param.default is inspect.Parameter.empty:
                required.append(name)

        func.tool_schema = {
            "name": func.__name__,
            "description": description,
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
        return func
    return decorator


# --- Search agent tools ---

# task 2.1 — descriptions include input format, example queries, boundaries vs similar tools
@tool(
    description=(
        "Search the web for research articles, studies, and reports on a specific topic. "
        "Input: a focused search query (e.g., 'AI diagnostic imaging accuracy studies 2024'). "
        "Returns: list of results with title, URL, excerpt, and publication date. "
        "Use for: finding primary sources and recent publications. "
        "Do NOT use for: analyzing document content — use analyze_document instead."
    ),
    param_descriptions={
        "query": "Focused search query — specific topics yield better results than broad queries"
    }
)
def web_search(query: str):
    """Execute web search with mock data."""
    for keyword, results in SEARCH_RESULTS.items():
        keywords = keyword.split("_")
        if keyword in query.lower() or any(w in query.lower() for w in keywords):
            return results
    first_key = list(SEARCH_RESULTS.keys())[0]
    fallback = SEARCH_RESULTS[first_key]
    return fallback


# --- Analysis agent tools ---

# TODO (Step 4): Define the analyze_document tool using the @tool decorator
# task 2.1 — description must include: input format, return format, boundaries
# task 2.3 — this tool is for the analysis agent ONLY, not search or synthesis
#
# Requirements:
#   - Function name: analyze_document
#   - Parameter: subtopic (str) — the subtopic keyword to look up
#   - Description must explain:
#     * What it does (extracts structured claim-source mappings from research documents)
#     * Input format (subtopic keyword like 'diagnosis', 'drug_discovery', 'patient_care')
#     * Return format (list of findings with claim, source_url, excerpt, date, confidence)
#     * Boundary: NOT for searching — use web_search instead
#   - param_descriptions: {"subtopic": "The subtopic keyword to analyze documents for"}
#   - Implementation: look up subtopic in ANALYSIS_FINDINGS from data.py,
#     matching by keyword (same pattern as web_search above)
#
# Hint: follow the exact pattern of web_search above — @tool decorator, then function body


# --- Synthesis agent tools ---

# TODO (Step 4): Define the compile_report tool using the @tool decorator
# task 2.1 — description must include: input format, return format, boundaries
# task 5.6 — output must preserve source attribution for every claim
#
# Requirements:
#   - Function name: compile_report
#   - Parameters: findings_json (str), coverage_notes (str) with default ""
#   - Description must explain:
#     * What it does (compiles analyzed findings into a structured research report)
#     * Input format (findings_json: JSON string of all findings; coverage_notes: gap annotations)
#     * Return format (report dict with findings, coverage_notes, and compiled flag)
#     * Boundary: NOT for searching or analyzing — all findings must be provided as input
#   - param_descriptions for both parameters
#   - Implementation: parse findings_json with json.loads, return dict with keys:
#     "findings" (parsed data), "coverage_notes" (from param or "No gaps noted"),
#     "compiled" (True)
#
# Hint: follow the @tool decorator pattern, handle the default param for coverage_notes


# --- Agent system prompts ---

SEARCH_AGENT_PROMPT = (
    "You are a web search research agent. Your role is to find relevant, credible "
    "sources on a given research subtopic.\n\n"
    "Instructions:\n"
    "- Use the web_search tool to find sources\n"
    "- Focus on recent, peer-reviewed, or authoritative sources\n"
    "- Return ALL search results — do not filter or summarize them\n"
    "- Your output will be passed to an analysis agent, so preserve all metadata "
    "(URLs, dates, excerpts)\n\n"
    "After searching, provide a brief summary of what you found and any notable gaps."
)

# TODO (Step 4): Define ANALYSIS_AGENT_PROMPT
# task 5.6 — every claim MUST have source attribution (source_url, excerpt, date)
# The prompt should instruct the agent to:
#   - Use analyze_document to extract findings for the given subtopic
#   - Require source_url and excerpt for every claim — no unsourced findings
#   - Include publication dates for temporal context (task 5.6)
#   - Flag conflicting statistics with both values and their sources
#   - Rate confidence as 'high', 'medium', or 'low'
#   - Output findings as structured data the synthesis agent can use directly
ANALYSIS_AGENT_PROMPT = None

# TODO (Step 4): Define SYNTHESIS_AGENT_PROMPT
# task 5.3 — annotate coverage gaps from unavailable sources or failed subagents
# task 5.6 — preserve ALL source attributions through synthesis
# The prompt should instruct the agent to:
#   - Use compile_report to produce the final output
#   - Preserve all source URLs, excerpts, and dates in the report
#   - Organize into: well-supported (multiple sources), contested (conflicts), coverage gaps
#   - When statistics conflict, include both values with their sources
#   - Note coverage gaps due to failed subagent tasks
SYNTHESIS_AGENT_PROMPT = None


# --- Agent configurations ---
# task 2.3 — each subagent gets ONLY role-relevant tools, not the full set

AGENT_CONFIGS = {
    "search": {
        "system": SEARCH_AGENT_PROMPT,
        "tools": [web_search.tool_schema],
        "handlers": {"web_search": web_search}
    }
    # TODO (Step 4): Add "analysis" and "synthesis" entries here
    # Each entry needs: "system" (prompt), "tools" (list with tool_schema), "handlers" (dict)
    # Example pattern — follow the "search" entry above:
    #   "analysis": {
    #       "system": ANALYSIS_AGENT_PROMPT,
    #       "tools": [analyze_document.tool_schema],
    #       "handlers": {"analyze_document": analyze_document}
    #   },
    #   "synthesis": {
    #       "system": SYNTHESIS_AGENT_PROMPT,
    #       "tools": [compile_report.tool_schema],
    #       "handlers": {"compile_report": compile_report}
    #   }
}


def spawn_subagent(client, agent_type, context):
    """
    Spawn a subagent via the Task tool pattern.

    task 1.3 — subagent context is explicitly provided in the prompt.
    Subagents do NOT inherit the coordinator's conversation history.
    task 2.3 — each subagent has a restricted, role-relevant tool set.
    """
    config = AGENT_CONFIGS.get(agent_type)

    if not config:
        # task 2.2 — structured error with errorCategory and isRetryable
        error = {
            "errorCategory": "validation",
            "isRetryable": False,
            "description": (
                f"Agent type '{agent_type}' is not configured. "
                f"Available types: {list(AGENT_CONFIGS.keys())}"
            )
        }
        return error

    # task 5.3 — simulate timeout for drug_discovery search when configured
    if agent_type == "search" and SIMULATE_SEARCH_TIMEOUT:
        if "drug" in context.lower():
            return TIMEOUT_ERROR

    # task 1.3 — subagent gets isolated context via explicit prompt, not inherited history
    messages = [{"role": "user", "content": context}]

    response = client.messages.create(
        model=MODEL,
        max_tokens=SUBAGENT_MAX_TOKENS,
        system=config["system"],
        tools=config["tools"],
        messages=messages
    )

    # task 1.1 — subagent's own agentic loop
    while response.stop_reason == "tool_use":
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                handler = config["handlers"].get(block.name)
                if handler:
                    result = handler(**block.input)
                else:
                    result = {"error": f"Unknown tool: {block.name}"}
                tool_result_entry = {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result)
                }
                tool_results.append(tool_result_entry)

        # Append assistant response and tool results to conversation
        assistant_content = []
        for block in response.content:
            if block.type == "text":
                assistant_content.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                assistant_content.append({
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                })

        messages.append({"role": "assistant", "content": assistant_content})
        messages.append({"role": "user", "content": tool_results})

        response = client.messages.create(
            model=MODEL,
            max_tokens=SUBAGENT_MAX_TOKENS,
            system=config["system"],
            tools=config["tools"],
            messages=messages
        )

    # Extract final text from subagent
    text_parts = [block.text for block in response.content if block.type == "text"]
    result = "\n".join(text_parts)
    return result
