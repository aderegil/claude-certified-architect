# Lab 05 — Claude Code for Continuous Integration

## Coding conventions

- **No inline return structures** — assign to a variable first, then return it.
- **No function calls as arguments** — assign the result first, then pass it.
- **Constants in `config.py`** — console colors.
- **File headers** — every Python file starts with `# filename.py - Short description`.
- Functions over classes.
- Comments only where they clarify an exam concept.
- `.env` for API keys — never hardcoded.

## Lab files

- `pipeline.py` — CI pipeline simulator: invokes Claude Code with `-p` flag for non-interactive reviews
- `review_schema.json` — JSON schema for structured review output with severity and confidence
- `config.py` — console colors
- `prompts/review_prompt.txt` — review prompt template (student refines iteratively)
- `pr_files/` — simulated pull request files for review
- `manage.py` — `python manage.py restart` restores starter state, `python manage.py solve` applies solutions
- `_manage/starter/` — starter files with TODOs intact
- `_manage/solved/` — completed files with all TODOs filled in

## Project context

### Testing standards

- Use `unittest.TestCase` for all tests
- Name test methods `test_<scenario>`
- One assertion per test method when possible
- Test both success and failure cases

### Review criteria

When reviewing code, focus on:
- Logic errors and edge cases
- Security vulnerabilities (injection, credential exposure, missing auth)
- Missing error handling for boundary conditions

Do not flag:
- Minor style preferences that do not affect correctness
- Missing type hints unless they mask a bug
