# Authoring Instructions

This file is for Claude Code during lab authoring sessions.
Read this before building or modifying any lab.

## Reference documents

### Exam references (in this `authoring/` folder)

- `CCA_Lab_Plan.md` — the blueprint for all 6 labs: what to build, files, key concepts, what to observe
- `CCA_Lab_Reference.md` — full mapping of all 27 task statements to labs (both perspectives)
- `CCA_Exam_Guide.md` — source of truth for all terminology, task statements, knowledge and skills

Always use exam guide terminology verbatim. Never paraphrase concepts from the guide.

### Completed labs as references

The completed labs at the repo root are the canonical examples. When building a new lab, study the completed labs that share the same platform or domain overlap:

- `01_customer_support_agent/` — **Agent SDK** reference (D1/D2/D5). Primary reference for tool definitions, agentic loops, interactive menus, system prompts, and file structure.
- `02_code_generation_workflows/` — **Claude Code** reference (D3/D5). Primary reference for README step progression and configuration-oriented labs.

Every "Lab 01" or "Lab 02" mention in this document refers to these folders.

### Coding references (`courses/`)

Official Anthropic Academy and course materials. Use them to ground lab code in canonical patterns. The exam guide has priority for terminology and concepts, but these courses define how the code should look.

**Skilljar course — Building with the Claude API** (`courses/Building with the Claude API/`)
- `04 Prompt evaluation/` — prompt eval patterns, grader functions
- `05 Project engineering techniques/` — prompting patterns and techniques
- `06 Tools use with Claude/` — **primary reference for tool definitions**: function + companion `_schema` dict pattern, tool streaming, text editor tool, web search tool
- `07 RAG and Agentic Search/` — chunking, embeddings, vector DB, hybrid search
- `08 Features of Claude/` — extended thinking, images, citations, caching, code execution
- `Model Context Protocol/` — MCP client/server examples

**GitHub course — anthropics/courses** (https://github.com/anthropics/courses)
- `tool_use/` — 6-lesson progression: overview, first tool, structured outputs via tool use, complete workflow, tool choice, multi-tool chatbot. Good reference for Labs 01 and 03.
- `prompt_engineering_interactive_tutorial/` — step-by-step prompting techniques. Good reference for D4 labs.
- `prompt_evaluations/` — production eval patterns. Good reference for D4/D5 labs.
- `anthropic_api_fundamentals/` — SDK basics, streaming, multimodal. Overlaps with Skilljar course.

### How to use references

1. **Exam guide first** — terminology, task statements, and concepts always come from the exam guide.
2. **Completed labs for structure** — when unsure how something should look, check `01_customer_support_agent/` (Agent SDK) or `02_code_generation_workflows/` (Claude Code).
3. **Courses for code patterns** — when writing lab code, match the patterns from the course materials (tool schemas, API calls, prompt structure).
4. **Cross-reference** — if a course shows a pattern that contradicts the exam guide terminology, the exam guide wins.

## Lab pedagogy

Labs are **guided walkthroughs**. The student does not write code from scratch. The progression is:

1. **See it work** — starter code runs out of the box and produces visible output.
2. **Complete it** — the student fills in `# TODO` sections guided by the README.
3. **Complement it** — later steps add features, often via Claude Code with a provided prompt.

Every README step tells the student exactly what to do, what to observe, and why it matters for the exam. No step should require guesswork.

### Sub-step structure for complete/complement steps

Every README step that asks the student to complete or complement code must use `####` sub-headings numbered as X.1, X.2, etc.:

- **X.1 Test** — run the query to see current behavior
- **X.2 The problem** or **X.2 The question** — frame the issue
- **X.3 The fix** or **X.3 The answer** — the solution (code to add, TODO to fill, or Claude Code prompt)
- **X.4 What to observe** — verify it works
- **X.5 Exam concept** — tie to a specific task statement

Steps where the test comes after the fix (e.g., Claude Code prompts) may skip X.1 and place the test run inside X.3 or X.4. Lab 01 Steps 4–7 as the canonical example.

### Copy-paste prompts

When a step asks the student to use Claude Code, the README **must** include the exact prompt to paste. Use a **Prompt for Claude Code:** heading followed by a fenced code block (triple backticks). This renders with a copy button in VSCode and GitHub.

Example:

**Prompt for Claude Code:**
```
Add a validation check to process_refund that rejects
amounts over $500 and returns a structured error with
errorCategory "policy_violation" and isRetryable false.
```

Prompt text inside fenced code blocks must be manually wrapped at ~65 characters for readability — no single-line prompts. Claude Code handles multi-line pastes correctly.

Never write "ask Claude Code to do X" without providing the literal prompt. Lab 01 Step 7 as the canonical example.

### Step-by-step detail

Every README starts from zero and walks through every action:

1. Create the lab folder
2. Create each file (by hand, scaffold script, or Claude Code prompt)
3. Configure (`.env`, `pip install`)
4. Run the starter code and observe output
5. Complete TODO sections, re-run, observe the difference
6. Complement with additional features in later steps

## How to build a lab

When asked to build Lab 0X:

1. **Read the lab plan** — read `CCA_Lab_Plan.md`, find the section for that lab. Note the scenario, domains, task statement IDs, files, and key concepts.
2. **Study the exam guide** — read `CCA_Exam_Guide.md`. For each task statement listed in the lab plan, read the full task statement text, its associated knowledge statements, and its skills statements. Extract:
   - The **exact terminology** the exam uses (e.g., `stop_reason`, `tool_use`, `end_turn`, `errorCategory`, `isRetryable`) — use these verbatim in code, comments, and README.
   - The **concepts the student must understand** — these drive what the lab demonstrates and what the README asks the student to observe.
   - The **skills the student must practice** — these drive what the lab asks the student to do (complete, complement, or configure).
3. **Cross-reference with the lab reference** — read `CCA_Lab_Reference.md` to confirm which task statements map to this lab and verify nothing is missed.
4. **Create the lab folder** at the repo root following the plan exactly.
5. **Apply all coding conventions** (see below).
6. **Design a coherent progression** — before writing any code, outline the lab steps as a narrative arc:
   - The lab must feel like **one exercise that builds progressively**, not a checklist of exam concepts stitched together.
   - Start simple: the first step should produce a working, minimal result the student can run and understand.
   - Each subsequent step **builds on the previous one** — adding a capability, handling an edge case, or improving the design. The student should feel momentum, not context-switching.
   - Exam concepts are woven into the progression naturally. The student practices them *because the exercise needs them*, not because a task statement says so.
   - By the final step, the student has built something **complete and functional** — something they can actually run, interact with, and enjoy using. The finished lab is not throwaway scaffolding; it becomes the student's **go-to reference** for reviewing exam concepts in real, working code.
   - Make it satisfying: the end result should do something tangible and interesting (e.g., an agent that handles real-feeling conversations, a pipeline that produces real output). If the student wouldn't want to show it to a colleague, it's not good enough.
7. **Keep steps minimal** — every step must earn its place in the progression:
   - A step exists because **the exercise needs it next**, not because a task statement needs coverage. If a concept (e.g., good tool descriptions) is naturally practiced while building, it does not need its own step.
   - Merge steps that would feel like context-switching into a single step when they serve the same part of the build.
   - **Watch for checklist risk** — especially in config-heavy labs (L02, L04) where each feature is discrete. Thread them together: e.g., "create a CLAUDE.md → now add a path rule that extends it → now add a skill that uses the rule" is a progression; "configure CLAUDE.md, now configure path rules, now configure a skill" is a checklist.
   - Aim for **5–8 substantive steps** per lab (excluding setup/reset). Fewer if the lab is tight; more only if each step genuinely builds on the last.
   - After outlining the steps, read them back as a story: "First the student builds X, then they see it fail at Y, so they add Z." If it doesn't read as a story, restructure.
8. **Write the README** grounded in the exam guide — every "what to observe" and "which exam concept" citation must trace back to a specific task statement, knowledge item, or skill from step 2.

## Repo structure

```
claude-certified-architect/
  README.md                        ← project overview, loaded by Claude Code at repo root
  authoring/                       ← authoring workspace, not for students
    AUTHOR.md                      ← authoring instructions (this file)
    CCA_*.md/.pdf/.docx            ← exam guide, lab plan, lab reference
    courses/                       ← Anthropic Academy code references
    prompts/                       ← reusable prompts for authoring tasks (e.g., build_lab_prompt.txt)
  01_customer_support_agent/       ← lab folders at root, for students
  02_code_generation_workflows/
  03_multi_agent_research/
  04_developer_productivity/
  05_ci_cd_integration/
  06_structured_extraction/
```

## Standard lab structure

Every lab must contain these files:

```
0X_lab_name/
  .gitignore          # ignores .env, .venv/, __pycache__/
  CLAUDE.md           # lab-specific instructions — loaded automatically by Claude Code
  README.md           # step-by-step lab guide, objectives, what to observe
  reset.zip        # snapshot of files with TODOs / files modified during the lab
  .env.example        # required env vars with placeholder values
  requirements.txt    # pip install -r requirements.txt
  config.py           # constants: model name, thresholds, policy values
  main.py             # starter script — the thing the student runs
  reset.py            # restores starter files from reset.zip
  prompts/            # all .txt prompt templates (system prompts, agent prompts)
```

Additional files (e.g., `tools.py`, `agents.py`, `schema.py`, `sample_docs/`) as specified in the lab plan.

## Workspace convention

The student's experience must feel scoped to the lab folder:

- **VSCode:** open the **lab folder** (e.g., `01_customer_support_agent/`) as the workspace — not the repo root.
- **Claude Code:** launch from the **lab folder** terminal. This ensures Claude Code loads the lab's own `CLAUDE.md`.
- **Every lab has its own `CLAUDE.md`** with the coding conventions and any lab-specific instructions Claude Code needs. Do not rely on the repo-root `README.md` — the student will never open the repo root as a workspace.

The student should never need to think about files outside their lab folder.

## README.md structure for each lab

Every README must follow this structure:

```markdown
# Lab 0X — Lab Name

## Objective
One paragraph. What you build and why it matters for the exam.

## Exam coverage
Scenario, domains, and task statements this lab covers.

## Lab guide

### Step 0 — Open the lab folder
Open the **lab folder** (e.g., `01_customer_support_agent/`) in VSCode.
Launch Claude Code from the terminal inside this folder.
This ensures Claude Code loads the lab's own CLAUDE.md.

### Step 1 — Create a Python virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### Step 2 — Create the starter files
Either:
- A scaffold script the student runs, OR
- Claude Code prompt the student pastes, OR
- Explicit file-by-file creation instructions

### Step 3 — Configure
Copy .env.example, add API key, install dependencies.

### Step 4 — Run the starter code
What to run, what output to expect, what to observe.

### Step N — Complete / Complement
Each subsequent step has:
- What to do (explicit command, code to add, or Claude Code prompt to paste)
- What to observe after running
- Which exam concept it demonstrates (cite task statement ID)

When the step involves Claude Code, always include:
**Prompt for Claude Code:**
```
the exact prompt to paste
```

## Reset
How to reset and try again.

---

*v0.1 — 3/15/2026 — Alfredo De Regil*
```

## Coding conventions

Apply these to every Python file without exception.

### File structure

**File header** — every Python file must start with a single comment line:
```python
# filename.py - Short description of the file's purpose
```
No author name in file headers. Author credit goes only in the README footer (`*v0.1 — date — Alfredo De Regil*`). Lab 01's files as the canonical example.

**Mock data in separate files** — never inline mock data in Python code. Put it in a dedicated data file (e.g., `data.py`, `data.json`) and import/load from there.

**Functions over classes** — prefer plain functions. Use classes only when truly needed.

### Code style

**No inline return structures** — assign to a variable first, then return it.
```python
# correct
result = {"status": "ok", "data": data}
return result
```

**No function calls as arguments** — assign the result first, then pass it.
```python
# correct
messages = build_messages(history, prompt)
response = client.messages.create(messages=messages)
```

**Comments** — only where they clarify an exam concept, not obvious code. Always reference the exam guide task statement where relevant (e.g., `# [Task 1.1] agentic loop: check stop_reason`).

### API and tools

**Use the SDK that matches the lab's platform** — the exam guide specifies which platform each scenario uses. Each platform has its own SDK, patterns, and documentation:

| Platform | Package | Import | Docs | Labs |
|----------|---------|--------|------|------|
| **Claude Agent SDK** | `pip install claude-agent-sdk` | `from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, HookMatcher` | https://docs.anthropic.com/en/docs/claude-code/sdk | L01, L03, L04 |
| **Claude API (Client SDK)** | `pip install anthropic` | `import anthropic` | https://docs.anthropic.com/en/api/client-sdks | L06 |
| **Claude Code** | No SDK — labs configure Claude Code, not code tools | N/A | N/A | L02, L05 |

**The two SDKs are fundamentally different:**

- **Claude Agent SDK** — Claude handles tools autonomously. You call `query()` with a prompt, `allowed_tools`, and optional `AgentDefinition` subagents. The SDK runs the agentic loop internally using built-in tools (Read, Edit, Bash, Grep, Glob). Hooks are callback functions via `HookMatcher`. MCP servers are configured via `mcp_servers` parameter. Do **not** manually implement `while stop_reason == "tool_use"` loops — the SDK does this for you.
- **Claude API (Client SDK)** — You implement the tool loop yourself: `client.messages.create()` → check `stop_reason` → execute tools → loop. Tool definitions use companion `_schema` dicts. See `courses/Building with the Claude API/06 Tools use with Claude/` for canonical examples.

Do **not** mix patterns: if the lab plan says "Claude Agent SDK", use `claude_agent_sdk`. If it says "Claude API", use `anthropic`.

> ⚠ **Tool rename:** The exam guide refers to the subagent spawning tool as `"Task"` and says `allowedTools` must include `"Task"`. The SDK renamed this to `"Agent"` in Claude Code v2.1.63. **Use `"Agent"` in all lab code** — this is the current SDK name. The exam guide text is outdated on this point. Both names may appear in exam questions; the labs should use the current name.

> ⚠ **Known debt:** Lab 01 was built with the Claude API (Client SDK) pattern — manual agentic loops, `import anthropic`, `_schema` dicts. The exam guide says its scenario (S1) uses the Claude Agent SDK. To be migrated to `claude_agent_sdk` in a future pass. **New labs must use the correct platform from the start — do not copy the Client SDK pattern from Lab 01 for Agent SDK labs.**

### Prompts

**Prompt template convention** — all system prompts must live in `.txt` files inside a `prompts/` folder. Never hardcode multi-line prompts in Python code.
- **Location:** `prompts/` subfolder within the lab (e.g., `prompts/system_prompt.txt`, `prompts/coordinator.txt`, `prompts/search_agent.txt`).
- Use Python `.format()` template variables for any dynamic content — never string concatenation or f-strings.
- Wrap dynamic sections in XML tags that describe their purpose (e.g., `<case_facts>{case_facts}</case_facts>`, `<search_results>{search_results}</search_results>`).
- The starter code must load the template, initialize all variables with sensible defaults (e.g., `"No results yet."`), and call `.format()` on every API call. The template is always complete and valid from the first run.
- When a lab step asks the student to add dynamic content to the prompt, the XML section and template variable should already exist in the `.txt` file — the student only implements the logic that populates the variable.
- Lab 01's `system_prompt.txt` and `main.py` as the canonical example (note: Lab 01 has the prompt at root level, not in `prompts/` — new labs should use the `prompts/` folder).

### Console output

**ANSI color codes** — all labs with interactive terminal output must use ANSI escape codes for colored output. No external libraries (e.g., `rich`). Define color constants in `config.py` alongside other constants; main scripts import them from there.
- `CYAN` — user input/messages
- `GREEN` — agent responses
- `YELLOW` — tool calls
- `RED` — errors and blocks
- `DIM` — metadata (iterations, stop_reason, JSON)
- `BOLD` — headers
- `RESET` — clear formatting

**JSON formatting** — all JSON displayed in the console must use `json.dumps(result, indent=2)` for readability. Never truncated single-line output.

**Interactive mode** — every lab with an interactive `main.py` must include:
1. A `show_menu()` function that displays numbered test queries covering key lab scenarios, a `c` option to clear screen, and a `q` option to quit.
2. A `clear_screen()` helper using `os.system("cls" if os.name == "nt" else "clear")`.
3. Clear screen on startup (right after `load_dotenv()`) and on the `c` command, redisplaying the menu both times.
4. Support for custom free-text input in addition to the numbered options.

Lab 01's `main.py` as the canonical example.

### API error handling

All labs that make API calls (Claude Agent SDK or Claude API) must wrap the main API call in a try/except that catches billing and authentication errors with a clear message. The student should see what went wrong and where to check their balance — not a raw stack trace.

- **Both SDK types**: catch `Exception` around the main API call. Check if the error message contains "credit" or "balance" — if so, print `"API credit balance is too low."` with a link to `https://console.anthropic.com`. Otherwise print the generic error message. This pattern is consistent across both SDKs.
- **Claude Code labs** (L02, L05): no code to protect — Claude Code handles its own errors.

Lab 01's `main.py` as the canonical example for the Client SDK pattern. Lab 03's `main.py` as the canonical example for the Agent SDK pattern.

### General

- `.env` for API keys — never hardcoded
- Keep scripts short and focused — educational over production-quality
- Simple folder structures — no over-engineering

## File conventions

### config.py

Centralizes **hardcoded constants** needed by the rest of the lab:
- **Model name** — e.g., `MODEL = "claude-sonnet-4-20250514"` — single place to change it
- **Console color constants** — `CYAN`, `GREEN`, `YELLOW`, `RED`, `DIM`, `BOLD`, `RESET`
- **Thresholds and limits** — e.g., `MAX_REFUND_AMOUNT = 500`
- **Policy values** — e.g., `ESCALATION_REASONS = ["fraud", "policy_gap", "customer_request"]`

Only for constants with hardcoded values. Not for logic, not for mock data generators, not for settings that change at runtime. Other modules import from it.

### Mock data

All lab data is **hardcoded mock data**. No databases, no external services, no network calls beyond the Anthropic API.

- **Format:** plain Python dicts, JSON files, or text files inside the lab folder. Never a database, CSV download, or external dependency.
- **Realistic:** use real-sounding names, plausible amounts, documents with actual missing fields. The scenario should feel genuine, not like `"test_user_1"`.
- **Deterministic:** the student sees the same behavior every time. When the README says "observe X," the data must reliably produce X.
- **Self-contained:** everything the lab needs lives in its folder. The student can revisit the finished lab months later without restoring infrastructure.
- **Focus:** the lab teaches exam concepts, not data management. Zero setup friction — clone, install, run.

### reset.zip

At lab build time, create a `reset.zip` in the lab folder containing **only** the files that:
- Have `# TODO` sections the student fills in, OR
- Get modified during the lab (e.g., via Claude Code prompts)

Static files that never change during the lab (`config.py`, `data.py`, `system_prompt.txt`, etc.) should **NOT** be included. Lab 01 as the canonical example.

### _starter/ directory

Keep a `_starter/` folder in each lab containing the canonical copies of all files that are modified during the lab (the same files that go into `reset.zip`). This folder is for **authoring and debugging only** — it lets the author inspect or diff starter state without extracting the zip. It includes a `build_reset.py` script that rebuilds `reset.zip` from its contents.

`_starter/` is not referenced by the README or by students. It exists purely so the author can:
- See the starter state of every modified file at a glance
- Rebuild `reset.zip` after editing a starter file
- Diff working files against their starter versions during testing

### reset.py

Every `reset.py` must:
- Restore starter files by extracting `reset.zip` using `zipfile.extractall`, overwriting modified files
- Print each restored filename
- Print a confirmation message
- Be safe to run multiple times
- Preserve `.env` — the student should not have to re-enter their API key after a reset

### .env.example

Always include at minimum:
```
ANTHROPIC_API_KEY=your_api_key_here
```

Add any other required env vars with placeholder values and a comment explaining each.

### Starter scripts (main.py)

`main.py` should be a working starter — not a blank file. It should:
- Import dependencies
- Load `.env`
- Have the core structure in place with clearly marked `# TODO` sections where the student fills in logic
- Include enough comments to orient the student without doing the work for them

## Language and tone in README

- Direct and concise
- Use exam guide terminology exactly
- Each step tells the student what to do AND what to observe AND why it matters for the exam
- No fluff

## README formatting conventions

### Inline code (backticks)

Everything that is a code/config identifier gets backticks:

- Function names: `get_customer`, `fetch_document`
- Variable names: `stop_reason`, `case_facts`
- File names/paths: `main.py`, `.env`, `app/sample_app.py`, `CLAUDE.md`
- Tool names: `web_search`, `Agent`
- CLI commands: `python main.py`, `claude --resume`
- Config keys/values: `errorCategory`, `isRetryable`, `context:fork`
- Special values: `"tool_use"`, `"end_turn"`, `True`, `False`
- XML tags: `<case_facts>`, `<coverage_gaps>`
- Directory paths: `~/.claude/CLAUDE.md`, `.claude/rules/`
- Formats/patterns: `"PROD-XXX"`, `"CUST-1001"`

**Not backticked:** agent role names (use bold), exam domain labels (D1, D2), concept names in prose.

### Bold

- Agent names/roles: **coordinator**, **search-agent**, **synthesis-agent**
- Section labels: **What to observe:**, **Exam concept:**
- Key concept introductions: **Hub-and-spoke architecture**, **PostToolUse hooks**
- Callout labels: **Note:**, **Anti-patterns to know for the exam:**, **Also know for the exam:**
- Prompt labels: **Prompt for Claude Code:**

### Task references

Format: `[Task X.Y]` or `[Tasks X.Y, X.Z]`

- Always in square brackets with capital "T"
- Placed at the end of the paragraph or sentence
- Period goes **outside** the brackets: `...the correct signal. [Task 1.1]`
- Multiple tasks separated by comma: `[Tasks 1.5, 2.2]`

### Blockquotes

Used for exam awareness callouts that are supplementary to the main step content. Always start with a bold label:

- `> **Note:**` — general supplementary information
- `> **Anti-patterns to know for the exam:**` — anti-patterns the exam tests
- `> **Also know for the exam:**` — related exam concepts not directly exercised in the step
- `> **Note on [topic]:**` — specific clarification (e.g., `> **Note on the Agent tool name:**`)

**Not blockquotes:** main step content, "What to observe" lists, "Exam concept" paragraphs.

### Code blocks

| Content type | Specifier |
|-------------|-----------|
| Shell commands | ` ```bash ` |
| Python code | ` ```python ` |
| JSON config | ` ```json ` |
| Markdown file content | ` ```markdown ` |
| Claude Code prompts | ` ``` ` (no specifier) |
| Plain output/text | ` ``` ` (no specifier) |

**Prompt for Claude Code format:** Bold label on its own line, followed by blank line, then fenced code block with no language specifier. Prompt text manually wrapped at ~65 characters.

### Headers

| Level | Usage | Format |
|-------|-------|--------|
| H1 `#` | Document title | `# Lab 0X — Lab Name` |
| H2 `##` | Major sections | `## Objective`, `## Exam coverage`, `## Lab guide`, `## Reset` |
| H3 `###` | Steps | `### Step N — Description` (em-dash) |
| H4 `####` | Sub-steps | `#### N.Y Title` |

**Never go deeper than H4.** Standard sub-step titles: Test → The problem → The fix → What to observe → Exam concept.

### Lists, tables, emphasis

- **Dash (`-`)** for all unordered lists (never `*`)
- **Numbered lists** only for ordered sequences
- **Tables** for exam coverage (Task + Statement) and inline comparisons
- **Bold** is the primary emphasis. _Italics_ rare, for single-word emphasis using underscores (`_word_`)
- ALL-CAPS only for acronyms (API, MCP) and Python constants (`MAX_REFUND_AMOUNT`)

### Footer

```markdown
---

*v0.1 — 3/28/2026 — Alfredo De Regil*
```

---

*v0.1 — 3/15/2026 — Alfredo De Regil*
