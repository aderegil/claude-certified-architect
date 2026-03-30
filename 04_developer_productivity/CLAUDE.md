# Lab 04 — Developer Productivity Agent

## Coding conventions

@import .claude/conventions.md

## Lab files

- `main.py` — agent setup: hooks, display, interactive menu, MCP server, subagent, scratchpad
- `agents.py` — Explore subagent AgentDefinition
- `tools.py` — MCP documentation server tool definition (lookup_docs)
- `data.py` — mock project documentation (architecture, API, onboarding, testing, tech debt)
- `config.py` — console colors
- `prompts/system_prompt.txt` — main agent system prompt (tool selection, exploration strategy, scratchpad)
- `prompts/explore_agent.txt` — Explore subagent system prompt (investigation output format)
- `storefront/` — sample Python codebase for the agent to explore
- `.claude/conventions.md` — coding conventions (imported by this CLAUDE.md)
- `.claude/commands/explore.md` — /explore skill with context:fork
- `reset.py` — restores starter files from `reset.zip` and deletes scratch.md
- `reset.zip` — pristine copies of files with TODOs (main.py, tools.py, agents.py, explore.md)
- `.env.example` — copy to `.env` and add your ANTHROPIC_API_KEY
- `requirements.txt` — claude-agent-sdk, python-dotenv

## Key exam concepts in this lab

- Built-in tool selection: Grep for content search, Glob for file patterns [Task 2.5]
- Edit fallback: Read + Write when anchor text is non-unique [Task 2.5]
- Incremental understanding: Grep entry points → Read imports → trace flows [Task 2.5]
- Function usage tracing across wrapper modules [Task 2.5]
- MCP server configuration with create_sdk_mcp_server [Task 2.4]
- Tool descriptions as primary selection mechanism [Tasks 2.1, 2.4]
- AgentDefinition: description, system prompt, tool restrictions [Task 1.3]
- Explicit context passing: subagent receives findings in prompt [Task 1.3]
- Explore subagent isolates verbose discovery from main context [Tasks 1.3, 3.4, 5.4]
- Scratchpad file persists findings across questions [Task 5.4]
- CLAUDE.md with @import for modular organization [Task 3.1]
- Custom skill with context:fork and allowed-tools [Task 3.2]
