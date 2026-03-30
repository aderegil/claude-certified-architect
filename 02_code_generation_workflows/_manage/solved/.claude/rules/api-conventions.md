---
paths:
  - "app/**/*.py"
  - "!**/*.test.py"
---

# API Code Conventions

- Every function must validate its inputs before processing
- Return None for not-found cases — never raise KeyError or similar
- Use type hints for function parameters and return values
- Keep functions under 20 lines — extract helpers for complex logic
- All dict lookups use .get() with a default, never direct key access
