# Lab 03 — Multi-Agent Research System

## Objective

Build a multi-agent research system where a **coordinator** agent delegates to four specialized subagents — a **search-agent**, a **analysis-agent**, a **synthesis-agent**, and a **report-agent** — using the Claude Agent SDK. By the end you will have a working system that decomposes research topics, finds sources, analyzes documents, handles errors from unavailable sources, synthesizes findings into cited reports with coverage annotations, and writes the final report to a file — all grounded in exam concepts you can trace back to specific task statements.

## Exam coverage

**Scenario:** S3 — Multi-Agent Research System
**Domains:** D1 · D2 · D5

| Task | Statement |
|------|-----------|
| 1.2 | Orchestrate multi-agent systems with coordinator-subagent patterns |
| 1.3 | Configure subagent invocation, context passing, and spawning |
| 1.5 | Apply Agent SDK hooks for tool call interception and data normalization |
| 1.6 | Design task decomposition strategies for complex workflows |
| 2.1 | Design effective tool interfaces with clear descriptions and boundaries |
| 2.2 | Implement structured error responses for MCP tools |
| 2.3 | Distribute tools across agents and configure tool choice |
| 5.1 | Manage conversation context across long interactions |
| 5.3 | Implement error propagation across multi-agent systems |
| 5.6 | Preserve information provenance in multi-source synthesis |

## Lab guide

### Step 0 — Open the lab folder

Open the **`03_multi_agent_research/`** folder in VSCode.
Launch Claude Code from the terminal inside this folder.
This ensures Claude Code loads the lab's own `CLAUDE.md`.

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

### Step 3 — Run the starter code and observe the coordinator

#### 3.1 Orient yourself

Before running, open these files to understand the starter design:

- **`agents.py`** — four `AgentDefinition` entries: **search-agent**, **analysis-agent**, **synthesis-agent**, **report-agent**. Each has a description, system prompt path, and tool restrictions (currently empty — you will restrict them in Step 4).
- **`main.py`** — find the `hooks` list and the `query()` call. The hooks intercept every tool call for logging; `query()` runs the coordinator with the Agent SDK's managed agentic loop (no manual `while` loop needed).
- **`prompts/coordinator.txt`** — the coordinator's system prompt that controls delegation and context passing.

#### 3.2 Run

```bash
python main.py
```

The system starts with a menu of numbered test queries. Type `1` to run the first query: a broad research topic on AI in healthcare.

**What to observe:**

- The **coordinator** receives the topic and decides to delegate — it spawns subagents via the `Agent` tool
- Each subagent spawn appears with a timestamp and its tool list: `[12.3s] ↳ Spawning: search-agent` followed by `Tools: ALL (no restriction)` — this tells you the agent inherits every tool
- Every tool call is labeled with the agent that made it: `[search-agent] → web_search("AI healthcare")`
- The **search-agent** calls `web_search` to find articles; the **analysis-agent** calls `fetch_document` to read full documents
- The **synthesis-agent** receives findings in its prompt and produces cited findings
- The **report-agent** receives the synthesis output and writes a timestamped file to `output/report_YYMMDD-HHmm.md` (e.g., `report_260329-1430.md`)
- The **coordinator** routes all communication — subagents never talk to each other directly (hub-and-spoke)
- The SDK handles the agentic loop internally — no manual `while stop_reason == "tool_use"` loop
- Watch for red `⚠ VIOLATION` warnings — these flag when an agent calls a tool outside its expected role (e.g., **synthesis-agent** calling `web_search`)

**How the hooks work:** The `PreToolUse` and `PostToolUse` hooks in `main.py` intercept every tool call before and after execution. They run in your process, not inside the agent's context window, so they print immediately as each tool call happens — even while `query()` is still running. This is the same pattern used to build audit logs, compliance checks, and real-time dashboards for production agents. [Task 1.5]

**Note on lab conveniences:** The tool list display (`Tools: ALL` / `Tools: web_search`) and the `⚠ VIOLATION` warnings are lab conveniences — they read from our own `AgentDefinition` objects, not from an SDK-provided feature. The SDK hooks give you `tool_name`, `tool_input`, and `tool_use_id`, but do not expose which tools a subagent has access to. In production, you would track tool assignments through your own registry.

**Note:** The starter code works end-to-end, but with issues you will fix in the next steps:
- All agents inherit all tools (no role-based restriction) — you will see `⚠ VIOLATION` warnings
- Error handling for unreachable sources is generic
- Coverage gaps are not annotated in the synthesis

> **Note on the Agent tool name:** The exam guide references the `Task` tool for spawning subagents. This was renamed to `Agent` in Claude Code v2.1.63. Current SDK releases emit `Agent` in tool_use blocks. The lab code checks for both names (`"Task"` and `"Agent"`) for compatibility across SDK versions.

**Exam concept:** Hub-and-spoke architecture — the **coordinator** manages all inter-subagent communication, error handling, and information routing. Subagents operate with isolated context; they do not inherit the **coordinator**'s conversation history automatically. Watch whether the **coordinator** spawns multiple agents in the same turn (parallel) or across separate turns (sequential) — parallel spawning via multiple `Agent` tool calls in a single response is more efficient. [Tasks 1.2, 1.3]

### Step 4 — Complete tool distribution

#### 4.1 Test

Run query `1` again and watch the output. Each subagent spawn shows its tool access, and each tool call is labeled with the agent that made it:

```
  [16.9s] ↳ Spawning: search-agent
    Search AI in healthcare
    Tools: ALL (no restriction)
    [search-agent] → web_search("AI healthcare")
    [search-agent] → fetch_document (jama.example.com)  ← ⚠ VIOLATION: should not use fetch_document

  [45.2s] ↳ Spawning: synthesis-agent
    Synthesize findings
    Tools: ALL (no restriction)
    [synthesis-agent] → web_search("AI ethics")  ← ⚠ VIOLATION: should not use web_search
```

Notice two things: every agent shows `Tools: ALL (no restriction)` because no `tools` list is set, and agents call tools outside their role — the **search-agent** uses `fetch_document`, the **synthesis-agent** uses `web_search`. The `⚠ VIOLATION` warnings (in bold red) make these cross-role tool calls visible.

#### 4.2 The problem

All four agents inherit all available tools because their `AgentDefinition` objects do not specify a `tools` list. The **search-agent** could call `fetch_document`, the **analysis-agent** could call `web_search`, and the **synthesis-agent** could call either — even though none of these cross-role tool uses make sense. Giving an agent too many tools (e.g., 18 instead of 4-5) degrades tool selection reliability, and agents with tools outside their specialization tend to misuse them.

#### 4.3 The fix

Open `agents.py` and add `tools` lists to each `AgentDefinition`:

```python
"search-agent": AgentDefinition(
    description=(...),
    prompt=search_prompt,
    tools=["mcp__research__web_search"],
),
"analysis-agent": AgentDefinition(
    description=(...),
    prompt=analysis_prompt,
    tools=["mcp__research__fetch_document"],
),
"synthesis-agent": AgentDefinition(
    description=(...),
    prompt=synthesis_prompt,
    tools=[],
),
"report-agent": AgentDefinition(
    description=(...),
    prompt=report_prompt,
    tools=[],
),
```

Re-run with query `1`.

#### 4.4 What to observe

- Each agent now shows its restricted tool list at spawn time: `Tools: web_search`, `Tools: fetch_document`, `Tools: none`
- **No more `⚠ VIOLATION` warnings** — all tool calls are now within each agent's expected role
- The **search-agent** only calls `web_search` — it cannot call `fetch_document`
- The **analysis-agent** only calls `fetch_document` — it cannot call `web_search`
- The **synthesis-agent** has no tools (`tools=[]`) — it produces its findings purely from data the **coordinator** passes in its prompt
- The **report-agent** has no tools (`tools=[]`) — it formats the report from synthesis data, file saving is handled by `main.py`

#### 4.5 Exam concept

Restricting each subagent's tool set to those relevant to its role prevents cross-specialization misuse. Too many tools degrades selection reliability. A **synthesis-agent** attempting web searches is a clear sign of improper tool distribution. `tools=[]` means the **synthesis-agent** receives all data in its prompt — no tool access needed. Both the **synthesis-agent** and **report-agent** use `tools=[]` — they work purely from data passed in their prompts. [Task 2.3]

> **Also know for the exam:** In production, you might give the **synthesis-agent** a single cross-role tool like `verify_fact` for high-frequency spot-checks while routing complex cases through the **coordinator**. This balances role isolation with practical needs. The exam also tests `tool_choice` configuration: `"auto"` (default — model decides), `"any"` (guarantees a tool call, useful for structured output), and forced selection `{"type": "tool", "name": "..."}` (ensures a specific tool runs first). This lab uses the default `"auto"`. [Task 2.3]

### Step 5 — Handle structured error propagation

#### 5.1 Test

Type `2` to run the second query. This query asks about surgical planning from "restricted-access journals" — the **analysis-agent** will try to fetch the restricted URL, which simulates a timeout.

#### 5.2 The problem

The `fetch_document` MCP tool returns `"Error: Request timed out."` — a generic string with no structured context. The **coordinator** receives this error but has no information about:
- What URL was attempted
- Whether any partial results are available
- What alternative approaches might work

Generic error responses like "search unavailable" hide valuable context from the **coordinator** and prevent intelligent recovery decisions. This is the difference between a coordinator that can work around failures and one that silently produces incomplete results.

#### 5.3 The fix

Open `main.py` and find the `fetch_document` function's timeout handling (the `if url == TIMEOUT_URL:` block). Replace the generic error with a structured response:

```python
if url == TIMEOUT_URL:
    # Find the article excerpt for partial results
    partial = None
    for article in ARTICLES:
        if article["url"] == url:
            partial = article["excerpt"]
            break

    error_data = {
        "error": True,
        "failure_type": "timeout",
        "attempted_url": url,
        "partial_results": partial,
        "alternatives": (
            "Use the search excerpt as a partial source, or "
            "search for alternative articles on surgical planning."
        ),
    }
    error_text = json.dumps(error_data, indent=2)
    content = [{"type": "text", "text": error_text}]
    response = {"content": content, "isError": True}
    return response
```

Re-run with query `2`.

#### 5.4 What to observe

- The **analysis-agent** reports the structured error — failure type, attempted URL, partial results, and alternatives
- The **coordinator** receives this context and can make an informed recovery decision
- The **coordinator** continues with results from other subagents instead of terminating the workflow
- The **synthesis-agent** receives the error context and can annotate coverage gaps

#### 5.5 Exam concept

Structured error context (failure type, attempted query, partial results, alternative approaches) enables intelligent **coordinator** recovery. The `isError` flag communicates tool failure back to the agent. Silently suppressing errors (returning empty results as success) AND terminating the entire workflow on a single failure are both anti-patterns. [Tasks 2.2, 5.3]

> **Also know for the exam:** The exam distinguishes _access failures_ (timeout, service down — needs a retry decision) from _valid empty results_ (query succeeded, zero matches — not an error). A search returning `{"results": []}` is a success; a search timing out is a failure. They require different recovery paths. In production, the **analysis-agent** would implement local recovery for transient failures — retrying a timed-out request once or twice before propagating the error. Only unresolvable errors (e.g., permanent access denied) should reach the **coordinator**. This lab simulates the error on the first attempt for simplicity. [Tasks 2.2, 5.3]

### Step 6 — Add coverage gap annotation with Claude Code

#### 6.1 The problem

The **coordinator** tells the **synthesis-agent** about errors, but the **synthesis-agent**'s coverage gap section is minimal — it just says "Note any topic areas where information was not available." The synthesis output may mention unavailable sources in passing, but it does not produce a structured coverage gap annotation that tells the reader exactly what is missing and why.

Similarly, the **coordinator**'s error handling instruction just says to "continue with results from other subagents" — it does not explicitly tell the **coordinator** to pass structured error context to the **synthesis-agent** or instruct the **synthesis-agent** to annotate gaps.

#### 6.2 The fix

Use Claude Code to enhance both the **coordinator** and **synthesis-agent** prompts.

**Prompt for Claude Code:**

```
Update prompts/coordinator.txt and prompts/synthesis_agent.txt
to improve coverage gap handling:

In coordinator.txt, update the "Error handling" section to
instruct the coordinator to:
- Pass structured error context to the synthesis agent
  (failure_type, attempted_url, partial_results)
- Tell the synthesis agent which topic areas have gaps
  and why (timeout, access denied, etc.)

In synthesis_agent.txt, update the "Coverage Gaps" section
under "Output format" to produce structured annotations:
- What topic or subtopic has incomplete coverage
- What source was attempted and what error occurred
- What partial information is available
- Whether the gap affects the reliability of findings
- Keep the existing heading level (### Coverage Gaps)
```

Re-run with query `2` after Claude Code makes the changes.

#### 6.3 What to observe

- The synthesis output now has a structured "Coverage Gaps" section
- The gap annotation includes the specific URL that failed, the failure type, and what partial information is available
- The reader can assess which findings in the report are well-supported versus which topic areas have incomplete coverage
- The **coordinator** passes error context to the **synthesis-agent** so nothing is silently dropped

#### 6.4 Exam concept

Structuring synthesis output with coverage annotations — which findings are well-supported versus which topic areas have gaps from unavailable sources. Subagents implement local recovery for transient failures; only unresolvable errors propagate to the coordinator with partial results and what was attempted. Source attribution is preserved through synthesis when findings are structured as claim-source mappings. [Tasks 5.3, 5.6]

### Step 7 — Observe task decomposition and provenance

Before finishing, run all three queries and compare the results:

**Query 1 (broad topic)** — The **coordinator** decomposes "AI in healthcare" into multiple subtopics: diagnostics, drug discovery, patient monitoring, mental health, ethics. This is good task decomposition — broad coverage across distinct aspects.

**Query 2 (includes timeout)** — Same broad decomposition, but one source is unavailable. The report annotates the gap rather than silently dropping the topic. Partial results from the search excerpt are preserved.

**Query 3 (narrow topic)** — "Only AI in radiology image analysis — nothing else." The **coordinator** searches for a narrow topic and gets fewer, less diverse results. Compare the coverage of query 1 vs query 3 — the narrow query misses drug discovery, mental health, patient monitoring, and ethics.

**What to observe across all queries:**

- **Task decomposition** [Task 1.6]: The **coordinator** decides how to decompose the topic. Broad topics get comprehensive coverage; narrow topics produce incomplete results. Overly narrow decomposition by the **coordinator** (e.g., splitting "AI in creative industries" into only visual arts subtopics) would miss entire domains.

- **Context passing** [Task 1.3]: Each subagent receives findings in its prompt, not via context inheritance. The **coordinator** includes search results in the **analysis-agent**'s prompt, and all findings in the **synthesis-agent**'s prompt. Without explicit passing, the **synthesis-agent** would have nothing to work with.

- **Claim-source mappings** [Task 5.6]: Every claim in the synthesis traces back to a specific source with publication name, date, and URL. When two sources disagree on a statistic (e.g., PharmaTech Analytics reports $150M savings vs WHO estimates $95M), both values are preserved with attribution rather than arbitrarily selecting one.

- **Tool descriptions** [Task 2.1]: Open `main.py` and read the `@tool` descriptions for `web_search` and `fetch_document`. Each description includes the tool's purpose, input format, example usage, and when to use it versus the other tool. These descriptions are the primary mechanism the model uses for tool selection.

- **Context management** [Task 5.1]: The **coordinator** trims verbose tool outputs to key findings before passing to the **synthesis-agent**. Subagent findings are structured (claim, source, excerpt) rather than raw document dumps, reducing token accumulation.

**Exam concepts:** The **coordinator** dynamically selects which subagents to invoke based on query requirements — it does not always route through the full pipeline. [Task 1.2] The **coordinator** specifies research goals and quality criteria, not step-by-step procedures, enabling subagent adaptability. [Task 1.3] Conflicting statistics are preserved with attribution rather than arbitrarily selected. Temporal data (publication dates) is included to prevent misinterpretation as contradictions. The exam also tests rendering content types appropriately in synthesis — financial data as tables, news as prose, technical findings as structured lists — rather than converting everything to uniform paragraph text. [Task 5.6]

> **Additional exam concepts to review:**
>
> **Iterative refinement (Task 1.2):** In production, the **coordinator** would evaluate synthesis output for coverage gaps, re-delegate to search/analysis with targeted queries to fill those gaps, and re-invoke synthesis until coverage is sufficient. This lab uses a single pass for simplicity, but the exam tests the iterative refinement pattern.
>
> **Decomposition patterns (Task 1.6):** The **coordinator** uses adaptive decomposition — adjusting what to search based on the topic. The exam also tests fixed sequential pipelines (prompt chaining) — predictable multi-step workflows like per-file analysis followed by cross-file integration. Lab 05 demonstrates the fixed pipeline pattern.
>
> **System prompt keyword sensitivity (Task 2.1):** Tool descriptions are the primary selection mechanism, but system prompt wording can override them. If the system prompt says "always search for documents first," the model may bias toward `web_search` even when `fetch_document` is the correct next step. Review system prompts for keyword-sensitive instructions that create unintended tool associations.
>
> **"Lost in the middle" effect (Task 5.1):** Models reliably process information at the beginning and end of long inputs but may miss findings buried in the middle. The **synthesis-agent** prompt places key findings at the beginning — this is a deliberate mitigation strategy. Use section headers in aggregated inputs to further reduce position effects.

## Reset

To reset the lab and try again:

```bash
python reset.py
```

This restores all modified files (`main.py`, `agents.py`, `prompts/coordinator.txt`, `prompts/synthesis_agent.txt`) to their original starter state with TODOs and removes the `output/` directory. Your `.env` file is preserved — no need to re-enter your API key.

---

*v0.1 — 3/28/2026 — Alfredo De Regil*
