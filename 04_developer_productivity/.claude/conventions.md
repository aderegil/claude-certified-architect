## Coding conventions

- **No inline return structures** — assign to a variable first, then return it.
- **No function calls as arguments** — assign the result first, then pass it.
- **Use the Claude Agent SDK** — `from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition`. Never use `import anthropic` or manual agentic loops.
- **Prompt templates in `prompts/`** — load system prompts from `.txt` files. Use `.format()` with template variables. Dynamic sections use XML tags.
- **Constants in `config.py`** — console colors.
- **File headers** — every Python file starts with `# filename.py - Short description`.
- Functions over classes.
- Comments only where they clarify an exam concept.
- `.env` for API keys — never hardcoded.
