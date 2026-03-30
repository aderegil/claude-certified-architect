# Lab 01 — Customer Support Resolution Agent

## Coding conventions

- **No inline return structures** — assign to a variable first, then return it.
- **No function calls as arguments** — assign the result first, then pass it.
- **Mock data in separate files** — never inline mock data in Python code. Import from `data.py`.
- **Use the Anthropic SDK** — `import anthropic`. Never make manual REST calls.
- **Tool definitions follow the companion `_schema` dict pattern** — define the Python function separately, then define a `_schema` dict with `name`, `description`, and `input_schema`.
- **Prompt templates in `.txt` files** — load system prompts from `system_prompt.txt`. Use `.format()` with template variables for dynamic content. Dynamic sections use XML tags (e.g., `<case_facts>{case_facts}</case_facts>`). Never use string concatenation or f-strings to build prompts.
- **Constants in `config.py`** — model name, thresholds, policy values, console colors.
- **File headers** — every Python file starts with `# filename.py - Short description`.
- Functions over classes.
- Comments only where they clarify an exam concept.
- `.env` for API keys — never hardcoded.

## Lab files

- `main.py` — agentic loop, tool execution, prerequisite gate, PostToolUse hook
- `tools.py` — get_customer, lookup_order, process_refund, escalate_to_human (function + _schema)
- `data.py` — mock customer and order data
- `config.py` — MODEL, MAX_REFUND_AMOUNT, MAX_LOOP_ITERATIONS, ESCALATION_REASONS, console colors
- `system_prompt.txt` — system prompt with escalation criteria, few-shot examples, and `{case_facts}` template variable
- `manage.py` — `python manage.py restart` restores starter state, `python manage.py solve` applies solutions
- `_manage/starter/` — starter files with TODOs intact
- `_manage/solved/` — completed files with all TODOs filled in
- `.env.example` — copy to `.env` and add your ANTHROPIC_API_KEY
- `requirements.txt` — anthropic, python-dotenv