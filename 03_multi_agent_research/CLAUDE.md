# Lab 03 — Multi-Agent Research System

## What this lab builds
A coordinator agent that spawns specialized subagents (search, analysis, synthesis) via the Task tool to produce cited research reports. Covers hub-and-spoke orchestration, parallel spawning, structured error propagation, and provenance preservation.

## Coding conventions
- Functions over classes
- No inline return structures — assign to variable first, then return
- No function calls as arguments — assign result first, then pass
- Mock data lives in `data.py` — never inline mock data in Python files
- Use the `@tool` decorator from `agents.py` for all tool definitions
- Comments reference task statement IDs where relevant (e.g., `# task 1.3`)
- File headers: `# filename.py - Short description`

## File roles
- `config.py` — constants only (model name, token limits, feature flags)
- `data.py` — all mock data (search results, analysis findings, timeout error)
- `agents.py` — subagent definitions: tool handlers, system prompts, configs, spawn logic
- `main.py` — coordinator loop: system prompt, task tool, agentic loop, console output

## Key exam terminology (use verbatim)
- `stop_reason`: `"tool_use"` (continue loop) or `"end_turn"` (terminate)
- `allowedTools`: must include `"Task"` for coordinator to spawn subagents
- `errorCategory`: transient, validation, permission, business
- `isRetryable`: boolean flag on structured errors
- `failure_type`, `attempted_query`, `partial_results`, `alternatives`: structured error context
- Claim-source mappings: `{claim, source_url, excerpt, date}`
- Hub-and-spoke: coordinator manages all inter-subagent communication
