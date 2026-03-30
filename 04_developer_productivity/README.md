# Lab 04 — Developer Productivity Agent

## Objective

Build a developer productivity agent that explores an unfamiliar Python codebase using the Claude Agent SDK. You start with built-in tools (`Grep`, `Glob`, `Read`), add an MCP documentation server, delegate deep exploration to an `AgentDefinition` subagent, persist findings to a scratchpad file, and package the result as a Claude Code skill.

## Exam coverage

**Scenario:** S4 — Developer Productivity with Claude
**Domains:** D1 · D2 · D3 · D5

| Task | Statement |
|------|-----------|
| 1.3 | Configure subagent invocation, context passing, and spawning |
| 2.1 | Design effective tool interfaces with clear descriptions and boundaries |
| 2.4 | Integrate MCP servers into Claude Code and agent workflows |
| 2.5 | Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively |
| 3.1 | Configure CLAUDE.md hierarchy, scoping, and modular organization |
| 3.2 | Create and configure custom slash commands and skills |
| 3.4 | Determine when to use plan mode vs direct execution |
| 5.4 | Manage context effectively in large codebase exploration |

## Lab guide

### Step 0 — Open the lab folder and explore

Open the **`04_developer_productivity/`** folder in VSCode.
Launch Claude Code from the terminal inside this folder.
This ensures Claude Code loads the lab's own `CLAUDE.md`.

Before writing any code, orient yourself:

1. **Read `CLAUDE.md`** at the lab root. Notice the `@import .claude/conventions.md` line — this pulls coding conventions from a separate file. Open `.claude/conventions.md` to see what gets imported.

2. **Browse the file layout.** The lab has two main areas:
   - The **agent code** — `main.py`, `tools.py`, `agents.py`, `data.py`, and `prompts/` — this is what you will modify during the lab
   - The **storefront codebase** in `storefront/` — a small Python e-commerce app that the agent will explore. Open a few files (`app.py`, `models.py`, `utils.py`) to get a feel for the code the agent will be investigating.

3. **Glance at `.claude/commands/explore.md`** — this is a Claude Code skill you will complete in Step 7.

### Step 1 — Create a Python virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### Step 2 — Configure

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key.

```bash
pip install -r requirements.txt
```

### Step 3 — Run the starter code and observe built-in tool selection

Before running, open `main.py` and read through it at a high level. Here is what the code does:

- **`run_query()`** sends the question to the Claude Agent SDK via `query()`. The SDK runs the agentic loop internally — no manual `while stop_reason == "tool_use"` loop needed.
- **`allowed_tools`** controls what the agent can use. The starter gives it `Read`, `Write`, `Edit`, `Grep`, `Glob`. Later steps add MCP tools and the `Agent` tool.
- **`system_prompt.txt`** tells the agent how to select tools and explore incrementally. Open `prompts/system_prompt.txt` and read the "Tool selection" and "Exploration strategy" sections.
- **`PreToolUse` / `PostToolUse` hooks** log every tool call in real time (`→ Grep("...")`, `→ Read (app.py)`). They run in your process, not inside the agent's context — the same pattern used for audit logs and compliance checks in production.
- **Each query creates a fresh session** — no memory between questions. You will fix this in Step 6.

Now run the agent:

```bash
python main.py
```

The system starts with a menu of numbered test queries. Run each one and watch which built-in tools the agent selects. The agent's final answer is rendered as formatted markdown in the terminal — file paths are clickable in VSCode's integrated terminal, so you can Ctrl+click (Cmd+click on macOS) to jump directly to any file the agent references.

#### 3.1 Find test files (Glob)

Type `1`. The agent needs to find files by name pattern.

**What to observe:** The agent uses `Glob` (e.g., `**/test_*.py`) — not `Grep` or `Read`. `Glob` is the correct tool for finding files by name pattern.

#### 3.2 Find callers (Grep)

Type `2`. The agent needs to find where a function is called across the codebase.

**What to observe:** The agent uses `Grep` (e.g., `validate_email`) — not `Glob`. `Grep` is the correct tool for searching file contents.

#### 3.3 Trace a re-exported function

Type `3`. This is a multi-step investigation: where is `validate_email` defined, where is it re-exported, and who calls it?

**What to observe:** The agent builds understanding incrementally:
1. `Grep` to find `validate_email` across all files
2. `Read` `models.py` to see the definition
3. `Read` `utils.py` to discover the re-export (`from models import validate_email`)
4. `Grep` again for each re-exported name to find the actual callers (`app.py`, `routes.py`)

This is the function tracing pattern: identify all exported names in the wrapper module (`utils.py`), then search for each name across the codebase. [Task 2.5]

#### 3.4 Edit fallback on non-unique text

Type `4`. The agent will try to extract the duplicated regex pattern in `middleware.py` into a shared constant.

**What to observe:** `middleware.py` has the same pattern string in two functions. When the agent tries `Edit`, the anchor text matches both locations — `Edit` fails because it is not unique. The agent falls back to `Read` + `Write`. [Task 2.5]

> **Note:** The agent may sometimes succeed with `Edit` if it uses a larger anchor. The key exam concept is knowing that `Edit` requires unique anchor text and `Read` + `Write` is the fallback.

#### 3.5 Technical debt without documentation

Type `5`. Without the MCP documentation tool (not yet wired up), the agent tries to answer a question about known technical debt by reading source files.

**What to observe:** The agent searches source files but the answer is incomplete — known debt items (priorities, planned improvements, root causes) live in project documentation, not in code. You will fix this in Step 4.

#### 3.6 Exam concept

`Grep` searches file _contents_ for patterns; `Glob` finds _files_ by name pattern. Building codebase understanding incrementally (`Grep` entry points → `Read` imports → trace flows) is more efficient than reading all files upfront. When `Edit` fails because its anchor text appears multiple times, use `Read` + `Write` as a fallback. [Task 2.5]

### Step 4 — Add the MCP documentation tool

#### 4.1 The problem

`tools.py` defines a `lookup_docs` MCP tool that searches project documentation, but three things prevent the agent from using it:
1. The tool is not wired up in `main.py`
2. Its description is just `"Search documentation."` — too vague
3. The system prompt only mentions built-in tools, biasing the agent toward `Grep`

#### 4.2 The fix

Three changes are needed in `main.py`. Find the TODO comments for Step 4.

**First**, create the MCP server and wire it up:

```python
from tools import lookup_docs
docs_server = create_sdk_mcp_server(
    name="docs",
    version="1.0.0",
    tools=[lookup_docs],
)
```

Add `"mcp__docs__lookup_docs"` to `allowed_tools`:

```python
allowed_tools.append("mcp__docs__lookup_docs")
```

And add the MCP server to the `ClaudeAgentOptions`:

```python
mcp_servers={"docs": docs_server},
```

**Second**, add the MCP tool to the system prompt so the agent knows when to prefer it. Find the `mcp_tool_guidance` TODO and uncomment:

```python
mcp_tool_guidance = (
    "- **lookup_docs** (MCP) — search project documentation: "
    "architecture decisions, API specs, onboarding guides, tech debt. "
    "Returns structured results with title, section, and content. "
    "Use this for documentation questions; use Grep for source code.\n"
)
```

**Third**, open `tools.py` and improve the `lookup_docs` description. Replace `"Search documentation."` with a description that tells the agent:
- What content it searches (architecture decisions, API specs, onboarding guides, known tech debt — not source code)
- What it returns (structured results with title, section, and full content)
- When to use it instead of `Grep` (documentation questions vs source code patterns)
- Example queries

Example enhanced description:

```python
(
    "Search internal project documentation including architecture "
    "decisions, API specifications, onboarding guides, and known "
    "technical debt. Returns structured results with title, section, "
    "and full content. Use this for questions about system design, "
    "API contracts, project conventions, and architectural decisions. "
    "Use Grep instead for searching source code patterns. "
    "Example queries: 'architecture overview', 'API endpoints', "
    "'onboarding', 'tech debt'."
)
```

Run query `5` (known technical debt).

#### 4.3 What to observe

- The agent now calls `lookup_docs("tech debt")` — the MCP tool is being used
- The hook output shows `→ lookup_docs("tech debt")` instead of only `Grep` and `Read` calls
- The answer includes documented debt items with priorities and root causes — information that exists only in the project documentation, not in source code
- Compare: in Step 3.5, the agent searched source files and found incomplete results; now it gets the full documented debt list in one MCP call
- Also try query `6` (architecture overview) — now that `lookup_docs` is available, compare the output with what you saw in Step 3.5

> **Note:** The agent may occasionally still prefer `Grep` over `lookup_docs` for some queries — tool selection is probabilistic, not deterministic. The system prompt guidance makes it likely but not guaranteed. If the agent skips the MCP tool, re-run the query; the key exam concept is understanding _why_ both the description and the system prompt matter for reliable selection.

#### 4.4 Exam concept

Tool descriptions are the primary mechanism for tool selection, but not sufficient alone. The system prompt's wording also affects selection: "use Grep for content search" biases the agent toward `Grep` even when an MCP tool has a better description. Both the description AND system prompt guidance must work together. [Tasks 2.1, 2.4]

> **Anti-patterns to know for the exam:** Keyword-sensitive instructions in the system prompt can create unintended tool associations. If the system prompt says "always search for documents first," the model may bias toward `web_search` even when `fetch_document` is the correct next step. Review system prompts for wording that might override well-written tool descriptions. [Task 2.1]

> **Also know for the exam:** In production, MCP servers are configured in `.mcp.json` (project-level, version controlled) or `~/.claude.json` (user-level, personal). Environment variables expand at connection time (`${DOCS_API_KEY}`) so credentials never appear in the file. This lab uses `create_sdk_mcp_server` (in-process) for simplicity, but the exam tests `.mcp.json` configuration. MCP resources expose content catalogs (documentation hierarchies, database schemas) so agents see available data without exploratory tool calls. Prefer community MCP servers for standard integrations (Jira, GitHub); reserve custom servers for team-specific workflows. [Task 2.4]

### Step 5 — Define the Explore subagent

#### 5.1 The problem

All exploration happens in the main agent's context window. For simple queries this is fine, but in production codebases with hundreds of files, complex questions generate verbose tool output that fills the context. The exam tests the pattern for solving this: delegating deep investigation to an isolated subagent.

#### 5.2 The fix

Three changes are needed. **First**, open `agents.py` and add `tools` to the `AgentDefinition` to restrict the Explore subagent to read-only tools:

```python
"explore": AgentDefinition(
    description=(...),
    prompt=explore_prompt,
    tools=["Read", "Grep", "Glob"],
),
```

**Second**, open `main.py` and wire up the subagent. Find the TODO comments for Step 5 and uncomment:

```python
from agents import build_explore_agent
agents = build_explore_agent()
```

Add `"Agent"` to the `allowed_tools` list:

```python
allowed_tools.append("Agent")
```

And add agents to the `ClaudeAgentOptions`:

```python
agents=agents,
```

**Third**, still in `main.py`, find the `explore_guidance` TODO and uncomment so the system prompt tells the agent when to delegate:

```python
explore_guidance = (
    "## Delegation\n\n"
    "For complex questions that require reading multiple files, "
    "tracing dependencies across modules, or analyzing architecture "
    "patterns, delegate to the **explore** subagent using the Agent "
    "tool. The subagent investigates autonomously and returns a "
    "structured summary. Use direct Grep/Read only for simple, "
    "single-file lookups.\n"
)
```

Now ask a complex multi-file question:

```
How do imports flow through the storefront codebase? Which module is the most-imported and which is least-imported?
```

#### 5.3 What to observe

- The main agent spawns the **explore** subagent: `↳ Spawning: explore`
- The subagent's tool calls appear indented as `[explore]` messages — this output stays in the subagent's isolated context, not the main agent's
- The main agent receives a structured summary and uses it to answer
- The main agent's context stays clean — it only sees the summary, not every tool call the subagent made

> **Note:** At this codebase size the agent may sometimes answer directly with `Grep` without spawning the subagent. In production codebases, the isolation becomes essential.

**Key detail:** The subagent does NOT inherit the main agent's conversation history — it starts with only the prompt the main agent writes for it. This is _explicit context passing_: the main agent must include everything the subagent needs. [Task 1.3]

#### 5.4 Exam concept

`AgentDefinition` configures a subagent with a description (when to use it), a system prompt (how to behave), and `tools` (what it can access). Restricting `tools=["Read", "Grep", "Glob"]` prevents the subagent from writing files or spawning sub-subagents. The subagent isolates verbose discovery from the main context, serving the same purpose as plan mode's discovery phase in Claude Code. [Tasks 1.3, 2.3, 3.4, 5.4]

> **Also know for the exam:** Plan mode is for large-scale changes (multi-file edits, architectural decisions); direct execution is for simple, well-scoped changes (single-file bug fix). The Explore subagent is the Agent SDK equivalent of plan mode's discovery phase. Use plan mode in Claude Code; use Explore subagents in programmatic agents. In production, summarize findings from one phase before spawning subagents for the next, injecting summaries into initial context. Coordinator prompts should specify goals and quality criteria, not step-by-step procedures. [Tasks 1.3, 3.4]

### Step 6 — Add scratchpad persistence

#### 6.1 Test

Run two related questions in sequence. First, type `3` (trace `validate_email`). After the agent answers, type:

```
Based on what you found about validate_email, which test files need updating if I rename it to is_valid_email?
```

#### 6.2 The problem

Each `run_query()` call creates a new session with fresh context. The system prompt has a `<scratchpad>` section, but its content is never loaded from disk — every question starts with `"No previous findings."` and the agent must re-explore.

#### 6.3 The fix

Open `main.py` and find the scratchpad TODO. Two changes are needed.

**First**, load `scratch.md` so the agent sees prior findings:

```python
scratchpad_path = os.path.join(lab_dir, "scratch.md")
if os.path.exists(scratchpad_path):
    with open(scratchpad_path, "r") as f:
        scratchpad_content = f.read()
else:
    scratchpad_content = "No previous findings."
```

**Second**, set the scratchpad instructions so the agent knows to write findings after each question:

```python
scratchpad_instructions = (
    "After answering each question, write a brief summary of your "
    "key findings to scratch.md. Include file paths, function "
    "locations, and architectural insights you discovered. Before "
    "answering a new question, review the scratchpad above for "
    "relevant prior findings that may save you from re-exploring."
)
```

Re-run the two questions from 6.1.

#### 6.4 What to observe

- After the first question, the agent writes its findings to `scratch.md` (you can open the file to see)
- On the second question, the `<scratchpad>` section in the system prompt now contains the first question's findings
- The agent references those findings instead of re-exploring — it already knows `validate_email` is defined in `models.py`, re-exported through `utils.py`, and called in `app.py` and `routes.py`
- The answer to the follow-up is faster and more accurate because it builds on prior discovery

#### 6.5 Exam concept

Context degradation in extended sessions causes agents to give inconsistent answers and reference "typical patterns" rather than specific classes discovered earlier. Scratchpad files persist key findings across context boundaries, counteracting degradation by keeping critical facts available even when earlier tool results have scrolled out of context. [Task 5.4]

> **Also know for the exam:** Use `/compact` to reduce context usage when context fills with verbose discovery output. For crash recovery in production, agents export state to a manifest file; the coordinator loads the manifest on resume and injects it into agent prompts. [Task 5.4]

### Step 7 — Examine CLAUDE.md and the /explore skill

This step does not add new Python code — it examines the Claude Code configuration files in the lab and completes the `/explore` skill.

#### 7.1 CLAUDE.md with @import

Open `CLAUDE.md` at the lab root. Notice the line:

```markdown
@import .claude/conventions.md
```

This imports conventions from a separate file instead of inlining them. Open `.claude/conventions.md` to see the imported content. Claude Code resolves `@import` automatically when it loads `CLAUDE.md`.

**Exam concept:** `CLAUDE.md` supports a three-level hierarchy: user-level (`~/.claude/CLAUDE.md`), project-level (`.claude/CLAUDE.md` or root), and directory-level. User-level settings are not shared via version control — new teammates will not receive them. Use `@import` for modularity and `.claude/rules/` for topic-specific rule files as an alternative to a monolithic `CLAUDE.md`. [Task 3.1]

#### 7.2 Complete the /explore skill

Open `.claude/commands/explore.md`. This is a Claude Code skill for codebase exploration — invokable via `/explore`. The frontmatter is incomplete. Add the following fields inside the `---` block:

```yaml
---
context: fork
allowed-tools: Read, Grep, Glob
argument-hint: "What part of the codebase should I explore?"
---
```

- `context: fork` — runs the skill in an isolated sub-agent, preventing verbose codebase discovery output from polluting the main Claude Code conversation
- `allowed-tools` — restricts the skill to read-only exploration tools (same principle as the `AgentDefinition` tool restriction in Step 5)
- `argument-hint` — prompts the user for what to explore when they invoke `/explore`

#### 7.3 What to observe

If you are running Claude Code in this lab folder, invoke `/explore` and type a question like "How does order processing work?" Observe:

- The skill runs in a **forked context** — its output appears as a sub-agent response, not mixed into your main conversation
- Only `Read`, `Grep`, and `Glob` are available — the skill cannot write files or spawn further subagents
- The verbose exploration stays isolated; your main session remains clean

This is the same isolation pattern as the Explore subagent in Step 5, but packaged as a reusable Claude Code skill that any team member can invoke.

#### 7.4 Exam concept

Project-scoped skills in `.claude/commands/` are shared via version control. `context:fork` isolates verbose output from the main conversation. `allowed-tools` restricts tool access during execution. `argument-hint` prompts for required parameters. Choose skills for on-demand workflows; use `CLAUDE.md` for always-loaded standards. [Task 3.2]

> **Also know for the exam:** Personal skills in `~/.claude/commands/` are not shared with teammates. For team-wide workflows, use project-scoped `.claude/commands/`. For personal variants, create a copy with a different name. [Task 3.2]

## Reset

To reset the lab and try again:

```bash
python reset.py
```

This restores all modified files (`main.py`, `tools.py`, `agents.py`, `.claude/commands/explore.md`) to their original starter state with TODOs and deletes `scratch.md`. Your `.env` file is preserved — no need to re-enter your API key.

---

*v0.1 — 3/29/2026 — Alfredo De Regil*
