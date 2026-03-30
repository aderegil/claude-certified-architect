---
context: fork
allowed-tools: Read, Grep, Glob
argument-hint: "What part of the codebase should I explore?"
---

Explore the storefront/ codebase in this workspace. The user wants to understand:

$ARGUMENTS

Investigate the codebase thoroughly:
1. Use Glob to find relevant files by name pattern
2. Use Grep to search for function definitions, imports, and usage patterns
3. Use Read to examine files in detail
4. Follow import chains across modules
5. Check for re-exports in utils.py

Provide a structured summary:
- **Files examined** and what each contains
- **Key findings** with specific file paths and line references
- **Architecture patterns** — how modules connect and depend on each other
- **Potential issues** — code quality concerns, duplication, or inconsistencies
