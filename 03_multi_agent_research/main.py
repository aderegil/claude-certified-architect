# main.py - Coordinator loop and subagent spawning for multi-agent research

import json
import os

import anthropic
from dotenv import load_dotenv

from agents import spawn_subagent
from config import DEFAULT_TOPIC, MAX_TOKENS, MODEL

load_dotenv()

# ANSI colors for console output
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


# task 1.3 — coordinator's allowedTools must include "task" to spawn subagents
TASK_TOOL = {
    "name": "task",
    "description": (
        "Spawn a specialized subagent to perform a research subtask. "
        "Available agent types: 'search' (finds web sources), 'analysis' "
        "(extracts structured findings from documents), 'synthesis' "
        "(compiles findings into a cited report). "
        "The subagent receives ONLY the context you provide in the prompt — "
        "it does NOT inherit your conversation history. Include all necessary "
        "prior findings and context explicitly. "
        "You may call this tool multiple times in a single response to spawn "
        "parallel subagents (e.g., multiple search agents for different subtopics)."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "agent_type": {
                "type": "string",
                "enum": ["search", "analysis", "synthesis"],
                "description": "The type of subagent to spawn"
            },
            "prompt": {
                "type": "string",
                "description": (
                    "Complete instructions and context for the subagent — "
                    "include ALL prior findings it needs since it has no memory"
                )
            }
        },
        "required": ["agent_type", "prompt"]
    }
}

# task 1.2 — coordinator system prompt with decomposition guidance
COORDINATOR_PROMPT = (
    "You are a research coordinator agent. Your job is to produce a comprehensive, "
    "cited research report by delegating to specialized subagents.\n\n"
    "Your workflow:\n"
    "1. DECOMPOSE the topic into 3 distinct subtopics that together cover the full scope\n"
    "2. SEARCH: spawn search subagents for each subtopic — use multiple task calls in a "
    "single response for parallel execution\n"
    "3. ANALYZE: spawn an analysis subagent — pass ALL search results in its prompt\n"
    "4. SYNTHESIZE: spawn a synthesis subagent — pass ALL analyzed findings in its prompt, "
    "plus any error context from failed subagents\n\n"
    "Critical rules:\n"
    "- Use the 'task' tool to spawn subagents — this is the ONLY way to delegate\n"
    "- Each subagent has isolated context — include ALL relevant findings in the prompt\n"
    "- Spawn multiple search subagents in a SINGLE response for parallel execution\n"
    "- If a subagent returns an error, include that error context when calling synthesis "
    "so it can annotate coverage gaps\n"
    "- Preserve all source attribution (URLs, dates, excerpts) through every stage\n\n"
    "Task decomposition guidance:\n"
    "- Subtopics must be BROAD enough to cover distinct major aspects of the topic\n"
    "- Avoid overly narrow decomposition — e.g., for 'AI in healthcare,' do NOT create "
    "3 subtopics all about radiology (task 1.2)\n"
    "- Each subtopic should cover a different dimension of the research topic"
)


def execute_task(client, agent_type, prompt):
    """Execute a Task tool call by spawning the appropriate subagent."""
    print(f"\n{YELLOW}  > Spawning {agent_type} subagent...{RESET}")
    prompt_preview = prompt[:120].replace("\n", " ")
    print(f"{DIM}    Context: {prompt_preview}...{RESET}")

    result = spawn_subagent(client, agent_type, prompt)

    # task 5.3 — check for structured error responses
    if isinstance(result, dict) and "failure_type" in result:
        print(f"{RED}  x {agent_type} subagent failed: {result['failure_type']}{RESET}")
        formatted = json.dumps(result, indent=2)
        print(f"{DIM}{formatted}{RESET}")
        return json.dumps(result)

    # task 2.2 — check for validation errors (e.g., unconfigured agent type)
    if isinstance(result, dict) and "errorCategory" in result:
        print(f"{RED}  x {agent_type} error: {result['description']}{RESET}")
        return json.dumps(result)

    print(f"{GREEN}  + {agent_type} subagent completed{RESET}")

    if isinstance(result, str):
        return result
    return json.dumps(result)


def run_coordinator(client, topic):
    """
    Run the coordinator agent's agentic loop.

    task 1.1 — continue on stop_reason "tool_use", terminate on "end_turn"
    task 1.2 — hub-and-spoke: coordinator routes all communication
    """
    print(f"\n{BOLD}{'=' * 60}")
    print(f"  Research Coordinator")
    print(f"{'=' * 60}{RESET}")
    print(f"{CYAN}  Topic: {topic}{RESET}\n")

    user_message = f"Research this topic and produce a comprehensive cited report: {topic}"
    messages = [{"role": "user", "content": user_message}]

    tools = [TASK_TOOL]

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=COORDINATOR_PROMPT,
        tools=tools,
        messages=messages
    )

    iteration = 0

    # task 1.1 — agentic loop: stop_reason "tool_use" means continue, "end_turn" means done
    while response.stop_reason == "tool_use":
        iteration += 1
        print(f"\n{BOLD}--- Coordinator iteration {iteration} ---{RESET}")

        # Display any text the coordinator produces between tool calls
        for block in response.content:
            if block.type == "text" and block.text.strip():
                print(f"{GREEN}{block.text}{RESET}")

        # Collect all tool calls from this response
        tool_calls = [block for block in response.content if block.type == "tool_use"]
        tool_results = []

        # TODO (Step 3): Process ALL tool calls for parallel subagent spawning
        # Currently only processes the FIRST tool call — the rest get placeholder errors.
        # task 1.3 — spawn parallel subagents via multiple Task calls in a single response
        #
        # Replace the code below with a loop that processes EVERY tool call:
        #   for call in tool_calls:
        #       task_result = execute_task(client, call.input["agent_type"], call.input["prompt"])
        #       tool_results.append({...})
        #
        # This enables the coordinator to spawn 3 search subagents in one turn.

        first_call = tool_calls[0]
        task_result = execute_task(
            client, first_call.input["agent_type"], first_call.input["prompt"]
        )
        first_result = {
            "type": "tool_result",
            "tool_use_id": first_call.id,
            "content": task_result
        }
        tool_results.append(first_result)

        # Placeholder errors for remaining calls (removed after Step 3)
        for remaining_call in tool_calls[1:]:
            placeholder = {
                "type": "tool_result",
                "tool_use_id": remaining_call.id,
                "content": (
                    "ERROR: Parallel subagent spawning not yet implemented. "
                    "Complete the TODO in Step 3 to process all tool calls."
                )
            }
            tool_results.append(placeholder)

        # Build assistant message from response content blocks
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

        # Append to conversation history and continue the agentic loop
        messages.append({"role": "assistant", "content": assistant_content})
        messages.append({"role": "user", "content": tool_results})

        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=COORDINATOR_PROMPT,
            tools=tools,
            messages=messages
        )

    # task 1.1 — stop_reason is "end_turn", print final response
    print(f"\n{BOLD}{'=' * 60}")
    print(f"  Final Report")
    print(f"{'=' * 60}{RESET}")

    for block in response.content:
        if block.type == "text":
            print(f"\n{block.text}")

    print(f"\n{DIM}Coordinator completed in {iteration} iteration(s){RESET}")


def main():
    client = anthropic.Anthropic()

    print(f"{BOLD}Multi-Agent Research System{RESET}")
    print(f"{DIM}Coordinator + specialized subagents via Task tool{RESET}\n")

    topic = input(f"{CYAN}Enter a research topic (or press Enter for default): {RESET}")
    topic = topic.strip()
    if not topic:
        topic = DEFAULT_TOPIC

    run_coordinator(client, topic)


if __name__ == "__main__":
    main()
