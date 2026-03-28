# CCA Foundations — Lab Plan

## General Considerations

### Environment
- **Language:** Python 3.11+
- **API:** Anthropic Claude API (`anthropic` SDK)
- **Editor:** VSCode with Claude Code (terminal or extension)
- **VSCode workspace:** Open the **lab folder** (e.g., `01_customer_support_agent/`) in VSCode — not the repo root. The student's experience should feel scoped to the lab they're working on.
- **Claude Code:** Launch from the terminal inside the lab folder. Each lab has its own `CLAUDE.md` that Claude Code loads automatically.
- **Dependencies:** managed per-lab via `requirements.txt`

### Lab pedagogy
Labs are **guided walkthroughs**, not open-ended exercises. The student does not write code from scratch. Instead, the lab:

1. **Provides working starter code** — enough to run and see something happen immediately.
2. **Asks the student to complete it** — clearly marked `# TODO` sections where the student fills in specific logic, guided by the README.
3. **Asks the student to complement it** — additional features or improvements added in later steps, often via Claude Code with a copy-paste prompt.

The learning happens by seeing code work, understanding why it works, then extending it. Every step in the README tells the student exactly what to do — no guesswork.

### Copy-paste prompts for Claude Code
When a lab step asks the student to use Claude Code (e.g., "ask Claude Code to add X"), the README **must** include the exact prompt the student should paste. Format:

```
> **Prompt for Claude Code:**
> `Add a validation check to process_refund that rejects amounts over $500 and returns a structured error with errorCategory "policy_violation" and isRetryable false.`
```

Never say "ask Claude Code to do something" without providing the literal prompt.

### Step-by-step detail level
Every README walks the student through the lab from zero:

1. **Create the lab folder** — `mkdir 01_customer_support_agent && cd 01_customer_support_agent`
2. **Create each file** — either by hand, by running a scaffold script, or via Claude Code with a copy-paste prompt
3. **Configure** — copy `.env.example` to `.env`, install dependencies
4. **Run** — execute the starter code, observe the output
5. **Complete** — fill in TODO sections, re-run, observe the difference
6. **Complement** — add features in later steps, re-run, observe

No step should assume the student "just knows" what to do. Every action is explicit.

### Conventions
- Functions over classes
- Comments only where they clarify a concept from the exam guide — not obvious code
- All exam-guide terminology used verbatim (e.g., `stop_reason`, `tool_use`, `end_turn`)
- `.env` for API keys — never hardcoded
- Each lab is fully self-contained — no shared code across labs

### Folder Structure (root)
```
claude-certified-architect/
  CLAUDE.md                        ← student-facing, auto-loaded by Claude Code
  authoring/                       ← authoring workspace (not for students)
    AUTHOR.md
    CCA_Lab_Plan.md
    CCA_Lab_Reference_v3.docx
    Claude_Certified_..._Exam_Guide.pdf
  01_customer_support_agent/       ← labs at root, numbered for ordering
  02_code_generation_workflows/
  03_multi_agent_research/
  04_developer_productivity/
  05_ci_cd_integration/
  06_structured_extraction/
```

### Every Lab Contains
```
XX_lab_name/
  CLAUDE.md         # lab-specific instructions, loaded by Claude Code
  README.md         # instructions, objectives, what to observe
  config.py         # constants, model name, thresholds, policy values
  main.py           # starter script — the thing you run
  reset.py          # resets all lab state so you can try again cleanly
  .env.example      # required env vars (copy to .env and fill in)
  requirements.txt  # pip install -r requirements.txt
```

> `config.py` centralizes hardcoded constants needed by the rest of the lab. Other modules import from it.
> Some labs add extra files (e.g., `tools.py`, `sample_docs/`). These are always described in the lab's README.

### Reset Convention
Every lab has a `reset.py` that:
- Deletes any output files or state the lab created
- Prints a confirmation so you know it's clean
- Can be run as many times as needed: `python reset.py`

### How to Start Any Lab
1. Open the **lab folder** (e.g., `01_customer_support_agent/`) in VSCode.
2. Open the integrated terminal (already in the lab folder) and run:
```bash
cp .env.example .env          # add your ANTHROPIC_API_KEY
pip install -r requirements.txt
python main.py                # run the lab
python reset.py               # reset and try again
```
3. Launch Claude Code from this same terminal when a step requires it.

---

## Lab 01 — Customer Support Resolution Agent

**Scenario:** S1 | **Domains:** D1 · D2 · D5
**Estimated time:** 20–30 min
**Tasks covered:** 1.1, 1.2, 1.4, 1.5, 2.1, 2.2, 2.3, 5.1, 5.2

### What you build
A customer support agent with 4 MCP-style tools: `get_customer`, `lookup_order`,
`process_refund`, `escalate_to_human`. The agent runs an agentic loop, enforces
a verification gate, intercepts tool calls via a hook, and maintains a persistent
context block.

### Key concepts practiced
- Agentic loop: `stop_reason == "tool_use"` → execute → continue; `"end_turn"` → stop
- Programmatic prerequisite gate: `process_refund` is blocked until `get_customer` has run
- PostToolUse hook: intercepts outgoing tool calls, blocks refunds > $500
- Structured error responses: `errorCategory`, `isRetryable`
- Explicit escalation criteria with few-shot examples in system prompt
- Persistent `case_facts` block outside summarized history (D5.1)

### Files
```
01_customer_support_agent/
  README.md
  main.py           # agentic loop + tool execution + hook
  tools.py          # get_customer, lookup_order, process_refund, escalate_to_human
  reset.py
  .env.example
  requirements.txt
```

### What to observe
1. Run a request that should escalate — verify the agent uses the explicit criteria
2. Try to call `process_refund` before `get_customer` — verify the gate blocks it
3. Try a refund > $500 — verify the hook intercepts and redirects
4. Watch how `case_facts` stays accurate across a multi-turn session

---

## Lab 02 — Code Generation Workflows

**Scenario:** S2 | **Domains:** D3 · D5
**Estimated time:** 25–35 min
**Tasks covered:** 1.7, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 5.4

### What you build
A configured Claude Code workspace: CLAUDE.md hierarchy, path-specific rules,
a custom skill with `context:fork`, and a deliberate session lifecycle
(name → close → resume → fork) to cover task 1.7.

> **Note:** This lab is Claude Code configuration, not a Python script.
> `main.py` is a helper that validates your setup and runs checks.
> The real work happens in config files and Claude Code sessions.

### Key concepts practiced
- CLAUDE.md hierarchy: user-level vs project-level vs directory-level
- `@import` for modular CLAUDE.md
- `.claude/rules/` with YAML frontmatter glob patterns (e.g., `**/*.test.py`)
- Custom skill with `context:fork` and `allowed-tools` restriction
- Plan mode vs direct execution — you run both and compare
- `--resume <session-name>` and `fork_session` (gap coverage for task 1.7)
- Scratchpad file pattern for context persistence across sessions (D5.4)

### Files
```
02_code_generation_workflows/
  README.md
  main.py                         # validates CLAUDE.md setup, checks files exist
  reset.py                        # removes generated config files
  .env.example
  requirements.txt
  scaffold/                       # example files for Claude Code to work on
    sample_app.py
    sample_app.test.py
```

### What to observe
1. Verify user-level vs project-level instructions behave differently
2. Edit `sample_app.py` — confirm API rules load; edit `sample_app.test.py` — confirm test rules load
3. Run the skill and observe `context:fork` keeping output isolated
4. Name a session, close it, make a change to `sample_app.py`, resume — verify agent notices the change
5. Fork the session and try two different refactoring approaches from the same baseline

---

## Lab 03 — Multi-Agent Research System

**Scenario:** S3 | **Domains:** D1 · D2 · D5
**Estimated time:** 25–35 min
**Tasks covered:** 1.2, 1.3, 1.6, 2.1, 2.2, 2.3, 5.1, 5.3, 5.6

### What you build
A coordinator agent that spawns 3 specialized subagents via the `Task` tool:
a search agent, a document analysis agent, and a synthesis agent. Subagents return
structured claim-source outputs. One subagent simulates a timeout to exercise
error propagation.

### Key concepts practiced
- Hub-and-spoke orchestration: coordinator routes all communication
- `allowedTools` must include `"Task"` for the coordinator to spawn subagents
- Explicit context passing: subagents receive findings in their prompt, not via inheritance
- Parallel subagent spawning: multiple `Task` calls in a single coordinator response
- Structured claim-source mappings: `{claim, source_url, excerpt, date}`
- Structured error propagation: `{failure_type, attempted_query, partial_results, alternatives}`
- Coverage gap annotation in synthesis output (D5.3)
- Provenance preserved through synthesis — no attribution loss (D5.6)

### Files
```
03_multi_agent_research/
  README.md
  main.py           # coordinator loop + subagent spawning
  agents.py         # search_agent, analysis_agent, synthesis_agent definitions
  reset.py
  .env.example
  requirements.txt
```

### What to observe
1. Run a research query — observe parallel subagent Task calls in a single turn
2. Trigger the simulated timeout — verify the coordinator receives structured error context
3. Inspect synthesis output — verify claim-source mappings are preserved
4. Try an overly narrow topic decomposition — observe incomplete coverage, then fix it

---

## Lab 04 — Developer Productivity Agent

**Scenario:** S4 | **Domains:** D1 · D2 · D3
**Estimated time:** 20–30 min
**Tasks covered:** 1.3, 2.1, 2.4, 2.5, 3.1, 3.2, 3.4, 5.4

### What you build
An agent that explores a small sample codebase using the built-in tools
(Read, Grep, Glob), integrates an MCP server via `.mcp.json`, delegates verbose
discovery to an Explore subagent, and uses a scratchpad file to persist findings.

### Key concepts practiced
- Grep (content search) vs Glob (file path patterns) — tool selection discipline
- Edit fallback: when anchor text is non-unique, use Read + Write instead
- Incremental codebase understanding: Grep entry points → Read imports → trace flows
- MCP server config in `.mcp.json` with `${ENV_VAR}` expansion for credentials
- Project-level vs user-level MCP server scoping
- Explore subagent: isolates verbose discovery, returns summary to main agent
- Scratchpad file: agent writes findings to `scratch.md`, reads it on next question (D5.4)

### Files
```
04_developer_productivity/
  README.md
  main.py           # agent loop with built-in tool dispatch
  mcp_config/
    .mcp.json       # sample MCP server config with env var expansion
  sample_codebase/  # small Python project for the agent to explore
    app.py
    utils.py
    tests/
      test_app.py
  reset.py
  .env.example
  requirements.txt
```

### What to observe
1. Ask the agent to find all callers of a function — verify it uses Grep, not Read
2. Ask it to find all test files — verify it uses Glob
3. Trigger a non-unique Edit — verify it falls back to Read + Write
4. Observe the Explore subagent keeping verbose output out of main context
5. Check `scratch.md` after a session — verify findings persisted correctly

---

## Lab 05 — CI/CD Integration

**Scenario:** S5 | **Domains:** D3 · D4
**Estimated time:** 20–25 min
**Tasks covered:** 1.6, 3.4, 3.5, 3.6, 4.1, 4.2, 4.6

### What you build
A simulated CI pipeline: Claude Code runs in non-interactive mode with `-p`,
produces structured JSON review output, uses an independent review instance
(not the generator), and splits a multi-file review into per-file passes
plus a cross-file integration pass.

> **Note:** Like Lab 02, this combines Claude Code CLI usage with a Python
> orchestration script that simulates the CI pipeline runner.

### Key concepts practiced
- `-p` / `--print` flag: non-interactive mode, no hangs in CI
- `--output-format json` with `--json-schema`: machine-parseable review findings
- Explicit review criteria: define what to report vs skip (not "be conservative")
- Few-shot examples in system prompt for consistent output format
- Session context isolation: independent review instance vs self-review
- Per-file local pass + cross-file integration pass (task decomposition, D1.6)
- Sync API for blocking pre-merge vs batch API for overnight jobs (D4.5 awareness)

### Files
```
05_ci_cd_integration/
  README.md
  pipeline.py       # simulates CI runner — invokes Claude Code with -p flag
  review_schema.json # JSON schema for structured review output
  CLAUDE.md         # project context: testing standards, review criteria, fixtures
  sample_pr/        # 3 Python files simulating a pull request
    auth.py
    orders.py
    utils.py
  reset.py
  .env.example
  requirements.txt
```

### What to observe
1. Run `pipeline.py` — verify it does not hang (non-interactive mode works)
2. Inspect JSON output — verify it matches the schema
3. Compare: run with vague criteria ("be conservative") vs explicit criteria — see false positive difference
4. Compare: single-pass review of all 3 files vs per-file + integration pass — see consistency difference
5. Run review twice on same files — verify second run only reports new issues

---

## Lab 06 — Structured Data Extraction

**Scenario:** S6 | **Domains:** D4 · D5
**Estimated time:** 25–30 min
**Tasks covered:** 4.2, 4.3, 4.4, 4.5, 5.5

### What you build
A document extraction pipeline: a JSON schema extraction tool, a
validation-retry loop with error feedback, batch submission via the
Message Batches API, and a confidence-based human review router.

### Key concepts practiced
- `tool_use` with JSON schema: most reliable for schema-compliant structured output
- `tool_choice: "any"` to guarantee tool call when doc type is unknown
- Nullable fields to prevent hallucination on absent information
- Enum `"other"` + detail string pattern for extensible categories
- Retry-with-error-feedback: append specific validation errors to retry prompt
- Distinguish retryable errors (format mismatch) from non-retryable (info absent)
- Message Batches API: `custom_id` correlation, failure resubmission
- Field-level confidence scores + stratified sampling for human review routing (D5.5)

### Files
```
06_structured_extraction/
  README.md
  main.py           # extraction loop + validation + retry
  batch.py          # Message Batches API submission + polling + failure handling
  schema.py         # JSON extraction schema definition
  sample_docs/      # 10 sample documents with varying formats and missing fields
    doc_01.txt ... doc_10.txt
  reset.py
  .env.example
  requirements.txt
```

### What to observe
1. Run extraction on a doc with a missing field — verify model returns `null`, not fabricated value
2. Trigger a validation error — verify retry prompt includes the specific error
3. Try a doc where the required info is genuinely absent — verify retry is skipped (non-retryable)
4. Submit the batch — observe `custom_id` correlation in results
5. Inspect confidence scores — verify low-confidence extractions are routed to human review

---

## Coding Conventions

**No inline return structures**
Assign the structure to a variable first, then return it.
```python
# ✗ avoid
return {"role": "user", "content": prompt}

# ✓ correct
message = {"role": "user", "content": prompt}
return message
```

**No function calls as arguments**
Assign the result of any function call to a variable before passing it as an argument.
```python
# ✗ avoid
response = client.messages.create(messages=build_messages(history, prompt))

# ✓ correct
messages = build_messages(history, prompt)
response = client.messages.create(messages=messages)
```

---

## Notes

- Labs do not need to be done in order, but L01 and L03 share D1/D2/D5 — doing them
  back to back reinforces the agentic architecture concepts well.
- L02 and L04 both touch D3 configuration — same benefit if done consecutively.
- L05 and L06 are the most independent — good to do last as they cover D4 which
  requires confidence in tool_use and prompt engineering already practiced in earlier labs.

---

*v0.1 — 3/15/2026 — Alfredo de Regil*
