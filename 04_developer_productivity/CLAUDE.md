# Lab 04 — Developer Productivity with Claude

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
- `manage.py` — `python manage.py restart` restores starter state and deletes scratch.md, `python manage.py solve` applies solutions
- `_manage/starter/` — starter files with TODOs intact
- `_manage/solved/` — completed files with all TODOs filled in
- `.env.example` — copy to `.env` and add your ANTHROPIC_API_KEY
- `requirements.txt` — claude-agent-sdk, python-dotenv