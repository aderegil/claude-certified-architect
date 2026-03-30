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

**Scenario:** S1 | **Domains:** D1 · D2 · D5 | **Platform:** Claude Agent SDK
**Estimated time:** 20–30 min
**Tasks covered:** 1.1, 1.2, 1.4, 1.5, 2.1, 2.2, 2.3, 5.1, 5.2

### **Scenario Description From Exam Guide**
> **Scenario 1: Customer Support Resolution Agent**
> You are building a customer support resolution agent using the Claude Agent SDK. The agent handles high-ambiguity requests like returns, billing disputes, and account issues. It has access to your backend systems through custom Model Context Protocol (MCP) tools (get_customer, lookup_order, process_refund, escalate_to_human). Your target is 80%+ first-contact resolution while knowing when to escalate.
>
> **Primary domains:** Agentic Architecture & Orchestration, Tool Design & MCP Integration, Context Management & Reliability

### What you build
A customer support agent with 4 MCP-style tools: `get_customer`, `lookup_order`,
`process_refund`, `escalate_to_human`. The agent runs an agentic loop, enforces
a verification gate, intercepts tool calls via a hook, and maintains a persistent
context block.

### Key concepts practiced
- Agentic loop: `stop_reason == "tool_use"` → execute → continue; `"end_turn"` → stop
- Anti-patterns: arbitrary iteration caps as primary stop, natural language termination, text-content completion checks
- Programmatic prerequisite gate: `process_refund` is blocked until `get_customer` has run
- Multi-concern decomposition: distinct items investigated with shared context, unified resolution
- PostToolUse hook: intercepts outgoing tool calls, blocks refunds > $500; also covers data normalization awareness (timestamps, status codes)
- Structured error responses: `errorCategory`, `isRetryable`
- `tool_choice` configuration: `"auto"` (default), `"any"` (guarantee tool call), forced selection (specific tool first)
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

**Scenario:** S2 | **Domains:** D3 · D5 | **Platform:** Claude Code
**Estimated time:** 25–35 min
**Tasks covered:** 1.7, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 5.4

### **Scenario Description From Exam Guide**
> **Scenario 2: Code Generation with Claude Code**
> You are using Claude Code to accelerate software development. Your team uses it for code generation, refactoring, debugging, and documentation. You need to integrate it into your development workflow with custom slash commands, CLAUDE.md configurations, and understand when to use plan mode vs direct execution.
>
> **Primary domains:** Claude Code Configuration & Workflows, Context Management & Reliability

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

**Scenario:** S3 | **Domains:** D1 · D2 · D5 | **Platform:** Claude Agent SDK
**Estimated time:** 25–35 min
**Tasks covered:** 1.2, 1.3, 1.5, 1.6, 2.1, 2.2, 2.3, 5.1, 5.3, 5.6

### **Scenario Description From Exam Guide**
> **Scenario 3: Multi-Agent Research System**
> You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.
>
> **Primary domains:** Agentic Architecture & Orchestration, Tool Design & MCP Integration, Context Management & Reliability

### What you build
A coordinator agent that spawns 4 specialized subagents via the `Agent` tool:
a search agent, a document analysis agent, a synthesis agent, and a report agent.
Subagents return structured claim-source outputs. PreToolUse/PostToolUse hooks
provide real-time observability and violation detection. One subagent simulates
a timeout to exercise error propagation.

### Key concepts practiced
- Hub-and-spoke orchestration: coordinator routes all communication; iterative refinement awareness (re-delegate, re-synthesize)
- PreToolUse/PostToolUse hooks for real-time tool call observability and role-violation detection
- `allowedTools` must include `"Agent"` for the coordinator to spawn subagents (exam guide says "Task" — renamed to "Agent" in SDK v2.1.63)
- Explicit context passing: subagents receive findings in their prompt, not via inheritance
- Parallel subagent spawning: multiple `Agent` calls in a single coordinator response
- Task decomposition: fixed sequential pipelines (prompt chaining) vs dynamic adaptive decomposition
- `tool_choice` awareness: "auto" (default), "any" (guarantee tool call), forced selection; scoped cross-role tools for high-frequency needs
- Structured claim-source mappings: `{claim, source_url, excerpt, date}`
- Structured error propagation: `{failure_type, attempted_query, partial_results, alternatives}`
- Coverage gap annotation in synthesis output (D5.3)
- Provenance preserved through synthesis — no attribution loss (D5.6)
- Content-type rendering: financial data as tables, news as prose, technical as structured lists

### Files
```
03_multi_agent_research/
  README.md
  main.py           # MCP tools, hooks, coordinator query, message display, menu
  agents.py         # search-agent, analysis-agent, synthesis-agent, report-agent definitions
  data.py           # mock research data (articles, documents)
  config.py         # console colors
  prompts/          # coordinator.txt, search_agent.txt, analysis_agent.txt, synthesis_agent.txt, report_agent.txt
  reset.py
  reset.zip
  .env.example
  requirements.txt
```

### What to observe
1. Run a research query — observe parallel subagent Agent calls in a single turn
2. Trigger the simulated timeout — verify the coordinator receives structured error context
3. Inspect synthesis output — verify claim-source mappings are preserved
4. Try an overly narrow topic decomposition — observe incomplete coverage, then fix it

---

## Lab 04 — Developer Productivity Agent

**Scenario:** S4 | **Domains:** D1 · D2 · D3 | **Platform:** Claude Agent SDK
**Estimated time:** 25–35 min
**Tasks covered:** 1.3, 2.1, 2.4, 2.5, 3.1, 3.2, 3.4, 5.4

### **Scenario Description From Exam Guide**
> **Scenario 4: Developer Productivity with Claude**
> You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks. It uses the built-in tools (Read, Write, Bash, Grep, Glob) and integrates with Model Context Protocol (MCP) servers.
>
> **Primary domains:** Tool Design & MCP Integration, Claude Code Configuration & Workflows, Agentic Architecture & Orchestration

### What you build
A developer productivity agent that helps explore a sample Python codebase.
The agent starts with built-in tools (Grep, Glob, Read), adds an MCP documentation
server with enhanced descriptions, delegates deep exploration to a defined
`AgentDefinition` subagent, persists findings to a scratchpad file, and gets
packaged as a Claude Code skill with `context:fork` for team reuse.

### Narrative arc
The student is onboarding onto a legacy codebase and needs to understand it fast.
Each step adds a capability that makes the agent more effective:

1. **Explore with built-in tools** — learn which tool does what
2. **Add an MCP server** — give the agent richer external context
3. **Define an Explore subagent** — let the agent go deep without losing focus
4. **Add a scratchpad** — let the agent remember across questions
5. **Package it for the team** — skill + CLAUDE.md for repeatability

### Key concepts practiced
- **Grep vs Glob selection discipline:** Grep for content search (find callers of a function), Glob for file path patterns (find test files) [Task 2.5]
- **Edit fallback:** when anchor text is non-unique, use Read + Write instead of Edit [Task 2.5]
- **Incremental codebase understanding:** Grep entry points → Read imports → trace flows [Task 2.5]
- **Function usage tracing:** identify all exported names in a wrapper module, then search each across the codebase [Task 2.5]
- **MCP server configuration:** project-level `.mcp.json` with `${ENV_VAR}` expansion for credentials; project-level vs user-level scoping [Task 2.4]
- **MCP tool description enhancement:** improve a tool description so the agent prefers the MCP tool over a built-in alternative — demonstrates descriptions as the primary tool selection mechanism [Tasks 2.1, 2.4]
- **MCP resources awareness:** content catalogs that reduce exploratory tool calls (exam note, not hands-on) [Task 2.4]
- **Community MCP servers:** prefer existing servers for standard integrations; reserve custom for team-specific workflows (exam note) [Task 2.4]
- **`AgentDefinition` configuration:** description, system prompt, and `allowedTools` restriction for the Explore subagent [Task 1.3]
- **Explicit context passing:** subagent receives prior findings in its prompt — no automatic inheritance [Task 1.3]
- **Explore subagent isolation:** verbose discovery output stays out of main agent context; programmatic equivalent of plan mode's discovery phase [Tasks 1.3, 3.4, 5.4]
- **Plan mode vs direct execution awareness:** when to use plan mode (large-scale, multi-file) vs direct (single-file, clear scope); Explore subagent as the SDK equivalent [Task 3.4]
- **Scratchpad persistence:** agent writes findings to `scratch.md`, reads it on subsequent questions to counteract context degradation [Task 5.4]
- **Context degradation awareness:** agent loses specifics after extended sessions; scratchpad and `/compact` as mitigations [Task 5.4]
- **Crash recovery awareness:** structured state exports (manifests) for coordinator resume (exam note, not hands-on) [Task 5.4]
- **Custom skill with `context:fork`:** `/explore` skill that runs codebase analysis in an isolated sub-agent, keeping verbose output from polluting main conversation [Task 3.2]
- **`allowed-tools` restriction:** skill frontmatter restricts which tools the skill can use [Task 3.2]
- **CLAUDE.md with `@import`:** lab's CLAUDE.md imports a coding conventions file; light demonstration of hierarchy and modular organization [Task 3.1]

### Files
```
04_developer_productivity/
  .gitignore
  CLAUDE.md           # lab-specific instructions, uses @import for conventions file
  README.md
  config.py           # model name, colors, constants
  main.py             # agent setup: built-in tools, MCP config, subagent, scratchpad
  agents.py           # Explore subagent AgentDefinition
  tools.py            # MCP documentation server tool definitions
  data.py             # mock project documentation (API docs, architecture notes)
  prompts/
    system_prompt.txt       # main agent system prompt
    explore_agent.txt       # Explore subagent system prompt
  storefront/                     # small Python project for the agent to explore
    app.py                        # main application, imports from utils and api/
    models.py                     # data models: User, Order, Product
    utils.py                      # re-exports validate_email, format_currency from models
    api/
      routes.py                   # API endpoints calling functions from app and utils
      middleware.py               # auth middleware with duplicate pattern strings
    tests/
      test_app.py
      test_models.py
      test_routes.py
  .claude/
    conventions.md          # coding conventions file (imported by CLAUDE.md)
    commands/
      explore.md            # /explore skill with context:fork + allowed-tools
  reset.py
  reset.zip
  .env.example
  requirements.txt
```

### What to observe
1. Ask the agent to find all test files — verify it uses Glob, not Read or Grep
2. Ask it to find all callers of `validate_email` — verify it uses Grep
3. Ask it to trace `validate_email` through `utils.py` — verify it identifies the re-export and searches each name
4. Trigger a non-unique Edit on `middleware.py` — verify fallback to Read + Write
5. Run a query where both the MCP docs tool and Grep could answer — observe tool preference before and after description enhancement
6. Run the Explore subagent on a complex question — verify verbose output stays isolated and findings return to main agent
7. Ask multiple questions, then a follow-up requiring earlier findings — verify `scratch.md` persists context
8. Run the `/explore` skill — verify `context:fork` keeps output isolated from main session

---

## Lab 05 — CI/CD Integration

**Scenario:** S5 | **Domains:** D3 · D4 | **Platform:** Claude Code
**Estimated time:** 25–35 min
**Tasks covered:** 1.6, 3.4, 3.5, 3.6, 4.1, 4.2, 4.6

### **Scenario Description From Exam Guide**
> **Scenario 5: Claude Code for Continuous Integration**
> You are integrating Claude Code into your Continuous Integration/Continuous Deployment (CI/CD) pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.
>
> **Primary domains:** Claude Code Configuration & Workflows, Prompt Engineering & Structured Output

### What you build
A simulated CI pipeline: Claude Code runs in non-interactive mode with `-p`,
produces structured JSON review output, uses an independent review instance
(not the generator), and splits a multi-file review into per-file passes
plus a cross-file integration pass. The student iteratively refines the
review prompt — from vague instructions to explicit criteria to few-shot
examples — observing progressive improvement in precision.

> **Note:** Like Lab 02, this combines Claude Code CLI usage with a Python
> orchestration script that simulates the CI pipeline runner.

### Key concepts practiced
- `-p` / `--print` flag: non-interactive mode, no hangs in CI (D3.6)
- `--output-format json` with `--json-schema`: machine-parseable review findings (D3.6)
- Direct execution in CI vs plan mode for investigation: CI pipelines use `-p` (direct, non-interactive); developers use plan mode interactively to investigate complex findings (D3.4)
- Iterative prompt refinement: vague criteria → explicit categorical criteria → few-shot examples, observing progressive improvement at each step (D3.5)
- Explicit review criteria with severity levels: define what to report (bugs, security) vs skip (minor style), with concrete code examples per severity level (D4.1)
- Disabling high false-positive categories to restore developer trust (D4.1)
- Few-shot examples created by the student: format includes file, line, issue, severity, suggested_fix, reasoning — with examples that distinguish acceptable code patterns from genuine issues (D4.2)
- Session context isolation: independent review instance vs self-review (D4.6)
- Per-file local pass + cross-file integration pass (task decomposition, D1.6)
- Per-finding confidence scores (high/medium/low) for calibrated review routing (D4.6)
- Existing test file context in CLAUDE.md to prevent duplicate test suggestions (D3.6)
- JSON review output formatted as simulated PR comments (D3.6)

> **Note:** Sync API for blocking pre-merge vs batch API for overnight jobs
> is covered in Lab 06 (D4.5). This lab mentions the distinction for
> awareness only — no exercise.

### Files
```
05_ci_cd_integration/
  README.md
  pipeline.py        # simulates CI runner — invokes Claude Code with -p flag
  review_schema.json # JSON schema with severity levels for structured review output
  CLAUDE.md          # project context: testing standards, review criteria, existing tests
  pr_files/          # 3 Python files simulating a pull request + 1 existing test file
    auth.py
    orders.py
    utils.py
    test_utils.py    # existing tests — referenced in CLAUDE.md for test generation context
  reset.py
  .env.example
  requirements.txt
```

### What to observe
1. Run `pipeline.py` — verify it does not hang (non-interactive mode works)
2. Inspect JSON output — verify it matches the schema, including severity levels per finding
3. **Iterative refinement loop (D3.5):**
   a. Run review with vague criteria ("be conservative") — count false positives
   b. Replace with explicit categorical criteria (what to report vs skip) — observe fewer false positives
   c. Add 2-3 few-shot examples showing acceptable patterns vs genuine issues — observe further improvement
4. Disable a high false-positive category (e.g., naming conventions) — observe remaining output is higher quality and more trustworthy (D4.1)
5. Compare: single-pass review of all 3 files vs per-file + integration pass — see consistency difference (D1.6)
6. Inspect per-finding confidence scores — filter by confidence, observe low-confidence findings have higher false positive rate (D4.6)
7. Run review twice on same files — verify second run only reports new issues (D3.6)
8. Add `test_utils.py` reference to CLAUDE.md — run test generation and observe suggestions avoid duplicating existing test scenarios (D3.6)
9. Format JSON review output as simulated PR inline comments — observe how structured output maps to developer-facing feedback (D3.6)
10. **Plan mode contrast (D3.4):** Run Claude Code interactively to investigate a complex finding using plan mode — contrast CI's automated direct execution with the developer's exploratory workflow

---

## Lab 06 — Structured Data Extraction

**Scenario:** S6 | **Domains:** D4 · D5 | **Platform:** Claude API
**Estimated time:** 25–30 min
**Tasks covered:** 4.2, 4.3, 4.4, 4.5, 5.5

### **Scenario Description From Exam Guide**
> **Scenario 6: Structured Data Extraction**
> You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JavaScript Object Notation (JSON) schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.
>
> **Primary domains:** Prompt Engineering & Structured Output, Context Management & Reliability

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
