# tools.py - MCP documentation server tool definitions
import json

from claude_agent_sdk import tool
from data import DOCS


# [Task 2.1, 2.4] — MCP tool for searching project documentation
# The description is the primary mechanism the agent uses to decide whether
# to call this tool or a built-in tool like Grep.
@tool(
    "lookup_docs",
    # TODO [Step 4, Task 2.1]: This description is too vague — the agent cannot tell
    # what this tool offers that Grep doesn't. Enhance it to include:
    #   - What content it searches (API specs, architecture decisions,
    #     onboarding guides, known tech debt — NOT source code)
    #   - What it returns (structured results with title, section, content)
    #   - When to use it INSTEAD of Grep (internal project documentation
    #     vs searching source code patterns)
    #   - Example queries: "architecture", "API endpoints", "tech debt"
    # A clear description outcompetes built-in tools by telling the agent
    # exactly when this tool is the better choice.
    "Search documentation.",
    {"query": str},
)
async def lookup_docs(args):
    """Search project documentation by keyword matching."""
    search_query = args.get("query", "").lower()
    query_words = search_query.split()

    scored = []
    for doc in DOCS:
        text = f"{doc['title']} {doc['section']} {doc['content']}".lower()
        score = sum(1 for word in query_words if word in text)
        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    matches = []
    for _score, doc in scored[:3]:
        result = {
            "title": doc["title"],
            "section": doc["section"],
            "content": doc["content"],
        }
        matches.append(result)

    if not matches:
        response_data = {
            "results": [],
            "message": "No matching documentation found.",
        }
    else:
        response_data = matches

    response_text = json.dumps(response_data, indent=2)
    content = [{"type": "text", "text": response_text}]
    response = {"content": content}
    return response
