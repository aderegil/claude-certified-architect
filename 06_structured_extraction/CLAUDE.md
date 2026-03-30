# Lab 06 — Structured Data Extraction

## Coding conventions

- **No inline return structures** — assign to a variable first, then return it.
- **No function calls as arguments** — assign the result first, then pass it.
- **Mock data in separate files** — invoice documents in `invoices/`, few-shot data in `data.py`.
- **Use the Anthropic SDK** — `import anthropic`. Never make manual REST calls.
- **Tool definitions follow the companion `_schema` dict pattern** — define the schema dict with `name`, `description`, and `input_schema`. No executable function; the tool exists only to force structured output.
- **Prompt templates in `.txt` files** — load from `prompts/extraction_prompt.txt`. Use `.format()` with template variables (e.g., `{few_shot_examples}`). Dynamic sections use XML tags. Never use f-strings to build prompts.
- **Constants in `config.py`** — model name, thresholds, console colors.
- **File headers** — every Python file starts with `# filename.py - Short description`.
- Functions over classes.
- Comments only where they clarify an exam concept.
- `.env` for API keys — never hardcoded.

## Lab files

- `main.py` — extraction pipeline: API call with forced tool_choice, validation, retry with error feedback, confidence routing, interactive menu
- `batch.py` — Message Batches API: preview, submit, poll status, retrieve results with custom_id correlation
- `schema.py` — extract_invoice tool schema (JSON schema for structured output)
- `data.py` — few-shot examples (3 example docs + correct extractions), labeled validation set (ground truth for accuracy check)
- `config.py` — MODEL, MAX_RETRIES, console colors
- `prompts/extraction_prompt.txt` — system prompt with format normalization rules and `{few_shot_examples}` template variable
- `invoices/` — 7 invoice documents with varying formats, missing fields, inconsistencies
- `manage.py` — `python manage.py restart` restores starter state, `python manage.py solve` applies solutions
- `_manage/starter/` — starter files with TODOs intact
- `_manage/solved/` — completed files with all TODOs filled in
- `.env.example` — copy to `.env` and add your ANTHROPIC_API_KEY
- `requirements.txt` — anthropic, python-dotenv