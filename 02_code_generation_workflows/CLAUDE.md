# Lab 02 — Code Generation with Claude Code

## Coding conventions

- **No inline return structures** — assign to a variable first, then return it.
- **No function calls as arguments** — assign the result first, then pass it.
- **Constants in `config.py`** — model name, console colors.
- **File headers** — every Python file starts with `# filename.py - Short description`.
- Functions over classes.
- Comments only where they clarify an exam concept.
- `.env` for API keys — never hardcoded.

## Lab files

- `main.py` — validates workspace configuration, checks files exist
- `config.py` — console colors
- `mcp_server/inventory_server.py` — custom MCP server exposing inventory data (FastMCP)
- `app/sample_app.py` — sample inventory management module
- `app/sample_app.test.py` — tests for sample_app.py
- `manage.py` — `python manage.py restart` restores starter state, `python manage.py solve` applies all configurations
- `_manage/starter/` — starter files (CLAUDE.md, app/sample_app.py, app/sample_app.test.py)
- `_manage/solved/` — completed configurations (CLAUDE.md with @import, rules, commands, .mcp.json)
