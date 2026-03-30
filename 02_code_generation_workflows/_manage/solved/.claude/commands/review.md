---
context: fork
allowed-tools:
  - Read
  - Glob
  - Grep
argument-hint: Path to the file to review
---

Review the file at $ARGUMENTS for code quality issues.

Check for:
1. Functions missing input validation
2. Functions missing docstrings
3. Direct dict key access without .get()
4. Functions longer than 20 lines
5. Missing error handling for edge cases

For each issue found, report:
- File and line number
- Issue category
- Suggested fix

Summarize the total number of issues by category at the end.
