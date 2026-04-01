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
- `reset.py` — restores starter files from `reset.zip`
- `reset.zip` — pristine copies of files with TODOs (main.py, schema.py)
- `.env.example` — copy to `.env` and add your ANTHROPIC_API_KEY
- `requirements.txt` — anthropic, python-dotenv

## Key exam concepts in this lab

- tool_use with JSON schema forces schema-compliant structured output [Task 4.3]
- tool_choice forced vs "any" vs "auto": forced guarantees the specific tool runs [Task 4.3]
- Nullable fields (`["string", "null"]`) prevent fabrication of missing data [Task 4.3]
- Enum with "unclear" for ambiguous values, "other" + detail for extensibility [Task 4.3]
- Format normalization rules in the prompt work alongside the strict schema [Task 4.3]
- Self-correction: calculated_total vs stated_total with conflict_detected boolean [Task 4.4]
- Retry-with-error-feedback: append validation errors + failed extraction to prompt [Task 4.4]
- Retryable (format mismatch) vs non-retryable (info absent from source) [Task 4.4]
- Few-shot examples for consistent extraction across varied document formats [Task 4.2]
- Few-shot to demonstrate null handling for absent fields [Task 4.2]
- Message Batches API: 50% cost savings, custom_id for result correlation [Task 4.5]
- Batch for overnight/non-blocking runs; sync API for blocking workflows [Task 4.5]
- No multi-turn tool calling in batch (single-turn extraction works fine) [Task 4.5]
- Resubmit failed requests by custom_id; chunk oversized documents [Task 4.5]
- Field-level confidence scores with flags for reduced-confidence fields [Task 5.5]
- Confidence routing: high → auto_approve, medium → spot_check, low → human_review [Task 5.5]
- Accuracy check against labeled validation set before adjusting thresholds [Task 5.5]
- Aggregate accuracy masks per-type/per-field weakness — stratified checking required [Task 5.5]
