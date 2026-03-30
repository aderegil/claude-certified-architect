# agents.py - Explore subagent definition for deep codebase investigation
import os

from claude_agent_sdk import AgentDefinition


def load_prompt(filename):
    """Load a prompt template from the prompts/ directory."""
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", filename)
    with open(prompt_path, "r") as f:
        content = f.read()
    return content


def build_explore_agent():
    """Build AgentDefinition for the Explore subagent.

    The Explore subagent handles deep codebase investigation in an
    isolated context — its verbose discovery output stays out of the
    main agent's context window. It receives a specific question and
    prior findings in its prompt, explores autonomously, and returns
    a structured summary.
    """
    explore_prompt = load_prompt("explore_agent.txt")

    # [Task 1.3] — AgentDefinition: description, system prompt, tool restrictions
    # [Task 2.1] — description tells the main agent WHEN to use this subagent
    agents = {
        "explore": AgentDefinition(
            description=(
                "Deep codebase explorer for complex multi-file analysis. "
                "Use when a question requires tracing dependencies across "
                "multiple files, understanding architecture patterns, or "
                "investigating code the main agent hasn't examined yet. "
                "Returns a structured summary of findings. Do NOT use for "
                "simple single-file lookups — use Read or Grep directly."
            ),
            prompt=explore_prompt,
            # [Step 5, Task 2.3] — restrict to read-only tools
            tools=["Read", "Grep", "Glob"],
        ),
    }
    return agents
