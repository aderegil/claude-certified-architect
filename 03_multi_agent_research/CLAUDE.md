# Lab 03 — Multi-Agent Research System

## Coding conventions

- **No inline return structures** — assign to a variable first, then return it.
- **No function calls as arguments** — assign the result first, then pass it.
- **Use the Claude Agent SDK** — `from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition`. Never use `import anthropic` or manual agentic loops.
- **Prompt templates in `prompts/`** — load system prompts from `.txt` files in the `prompts/` folder. Use `.format()` with template variables for dynamic content. Dynamic sections use XML tags.
- **Constants in `config.py`** — console colors.
- **File headers** — every Python file starts with `# filename.py - Short description`.
- Functions over classes.
- Comments only where they clarify an exam concept.
- `.env` for API keys — never hardcoded.

## Lab files

- `main.py` — MCP tool definitions (web_search, fetch_document), hooks, coordinator query, message display, interactive menu
- `agents.py` — AgentDefinition for search-agent, analysis-agent, synthesis-agent, report-agent
- `data.py` — mock research data (articles with keywords, full document content)
- `config.py` — console colors
- `prompts/coordinator.txt` — coordinator system prompt (delegation, context passing, error handling)
- `prompts/search_agent.txt` — search agent system prompt (structured claim-source output)
- `prompts/analysis_agent.txt` — analysis agent system prompt (document analysis, error reporting)
- `prompts/synthesis_agent.txt` — synthesis agent system prompt (report format, provenance rules)
- `prompts/report_agent.txt` — report agent system prompt (markdown formatting, file output)
- `reset.py` — restores starter files from `reset.zip` and removes output/
- `reset.zip` — pristine copies of files that have TODOs (main.py, agents.py, coordinator.txt, synthesis_agent.txt)
- `.env.example` — copy to `.env` and add your ANTHROPIC_API_KEY
- `requirements.txt` — claude-agent-sdk, python-dotenv

## Key exam concepts in this lab

- Hub-and-spoke orchestration: coordinator routes all subagent communication [Task 1.2]
- PreToolUse/PostToolUse hooks for real-time observability and tool call logging [Task 1.5]
- AgentDefinition: descriptions, system prompts, tool restrictions per subagent [Task 1.3]
- Explicit context passing: subagents receive findings in prompt, not via inheritance [Task 1.3]
- Parallel subagent spawning: multiple Agent tool calls in single response [Task 1.3]
- Task decomposition: avoid overly narrow decomposition [Task 1.6]
- Tool descriptions differentiate each tool's purpose [Task 2.1]
- Structured error responses: failure_type, attempted_url, partial_results [Task 2.2]
- Tool distribution: restrict each subagent to role-relevant tools [Task 2.3]
- Context management: subagent findings trimmed to key facts for synthesis [Task 5.1]
- Structured error propagation across multi-agent system [Task 5.3]
- Coverage gap annotation in synthesis output [Task 5.3]
- Claim-source mappings preserved through synthesis [Task 5.6]
