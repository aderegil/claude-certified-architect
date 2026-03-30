# agents.py - Subagent definitions for search, analysis, and synthesis agents
import os

from claude_agent_sdk import AgentDefinition


def load_prompt(filename):
    """Load a prompt template from the prompts/ directory."""
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", filename)
    with open(prompt_path, "r") as f:
        content = f.read()
    return content


def build_agents():
    """Build AgentDefinition dict for the coordinator's subagents.

    Each agent has a description (tells the coordinator WHEN to use it),
    a system prompt (defines its role and output format), and a tools list
    (restricts which tools it can access).
    """
    search_prompt = load_prompt("search_agent.txt")
    analysis_prompt = load_prompt("analysis_agent.txt")
    synthesis_prompt = load_prompt("synthesis_agent.txt")
    report_prompt = load_prompt("report_agent.txt")

    # [Task 2.1] — agent descriptions differentiate each agent's purpose
    # [Task 2.3] — each subagent should get ONLY tools relevant to its role

    agents = {
        "search-agent": AgentDefinition(
            # [Task 2.1] description tells the coordinator when to use this agent
            description=(
                "Research search specialist. Finds relevant articles and sources "
                "on a topic using web_search. Use this FIRST to discover what "
                "sources are available before deep analysis."
            ),
            prompt=search_prompt,
            # [Task 2.3] Restrict to search tool only — prevents misuse of
            # fetch_document or other tools outside its search role.
            tools=["mcp__research__web_search"],
        ),
        "analysis-agent": AgentDefinition(
            # [Task 2.1] description differentiates from search agent
            description=(
                "Document analysis specialist. Fetches and analyzes full "
                "document content by URL using fetch_document. Use AFTER "
                "search-agent has found relevant URLs to analyze in depth."
            ),
            prompt=analysis_prompt,
            # [Task 2.3] Restrict to fetch tool only — prevents an analysis
            # agent from attempting web searches instead of analyzing documents.
            tools=["mcp__research__fetch_document"],
        ),
        "synthesis-agent": AgentDefinition(
            # [Task 2.1] description clarifies this agent receives data, not fetches it
            description=(
                "Research synthesis specialist. Combines findings from search "
                "and analysis into structured, cited findings. "
                "Does NOT search or fetch — receives ALL data in its prompt. "
                "Does NOT write files — pass its output to the report-agent."
            ),
            prompt=synthesis_prompt,
            # [Task 2.3] No tools — receives ALL findings directly in its prompt
            # from the coordinator. A synthesis agent attempting web searches
            # violates role boundaries.
            tools=[],
        ),
        "report-agent": AgentDefinition(
            # [Task 2.1] description clarifies this agent formats, not analyzes
            description=(
                "Report formatter. Takes synthesized research findings and "
                "produces a clean, formatted markdown report. "
                "Does NOT search, fetch, or analyze — receives the final "
                "synthesis in its prompt and returns formatted markdown."
            ),
            prompt=report_prompt,
            # [Task 2.3] No tools — receives synthesis output in its prompt and
            # returns formatted markdown. File saving is handled by main.py.
            tools=[],
        ),
    }
    return agents
