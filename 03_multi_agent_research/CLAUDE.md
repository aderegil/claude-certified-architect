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
- `manage.py` — `python manage.py restart` restores starter state and removes output/, `python manage.py solve` applies solutions
- `_manage/starter/` — starter files with TODOs intact
- `_manage/solved/` — completed files with all TODOs filled in
- `.env.example` — copy to `.env` and add your ANTHROPIC_API_KEY
- `requirements.txt` — claude-agent-sdk, python-dotenv