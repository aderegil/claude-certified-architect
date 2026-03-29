# Lab 03 — Multi-Agent Research System

## Objective

Build a coordinator agent that spawns specialized subagents via the Task tool to research a topic and produce a cited report. You will implement hub-and-spoke orchestration, parallel subagent spawning, structured error propagation, and provenance-preserving synthesis — the core multi-agent patterns tested on the exam.

## Exam coverage

**Scenario:** S3 — Multi-Agent Research System
**Domains:** D1 (Agentic Architecture & Orchestration) · D2 (Tool Design & MCP Integration) · D5 (Context Management & Reliability)

| Task | Statement |
|------|-----------|
| 1.2 | Orchestrate multi-agent systems with coordinator-subagent patterns |
| 1.3 | Configure subagent invocation, context passing, and spawning |
| 1.6 | Design task decomposition strategies for complex workflows |
| 2.1 | Design effective tool interfaces with clear descriptions and boundaries |
| 2.2 | Implement structured error responses for MCP tools |
| 2.3 | Distribute tools across agents and configure tool choice |
| 5.1 | Manage conversation context across long interactions |
| 5.3 | Implement error propagation across multi-agent systems |
| 5.6 | Preserve information provenance in multi-source synthesis |

## Lab guide

### Step 0 — Open the lab folder

Open `03_multi_agent_research/` in VSCode. Launch Claude Code from the terminal inside this folder so it loads the lab's own `CLAUDE.md`.

### Step 1 — Configure and install

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

pip install -r requirements.txt
```

Review the file structure before continuing:

| File | Role |
|------|------|
| `config.py` | Constants: model name, token limits, timeout flag |
| `data.py` | All mock data: search results, analysis findings, timeout error |
| `agents.py` | Subagent definitions: tool handlers, system prompts, spawn logic |
| `main.py` | Coordinator: system prompt, task tool definition, agentic loop |

### Step 2 — Run the starter code

```bash
python main.py
```

Press Enter to use the default topic ("impact of artificial intelligence on healthcare").

**What to observe:**

1. The coordinator decomposes the topic into subtopics and calls the `task` tool to spawn search subagents.
2. Only the **first** tool call executes — the rest return placeholder errors. This is the TODO you fix in Step 3.
3. When the coordinator tries to call analysis or synthesis agents, it gets a validation error: `"Agent type 'analysis' is not configured."` This is the TODO you fix in Step 4.
4. The coordinator still produces a response using whatever results it got.

**Exam concepts demonstrated:**
- **Hub-and-spoke orchestration** (task 1.2): the coordinator manages all communication — subagents never talk to each other directly.
- **Agentic loop** (task 1.1): the loop checks `stop_reason == "tool_use"` to continue and `"end_turn"` to stop.
- **Isolated subagent context** (task 1.3): the search subagent receives only the context in its prompt — it does not inherit the coordinator's history.
- **Structured error responses** (task 2.2): unconfigured agent types return `errorCategory` and `isRetryable` metadata.

### Step 3 — Enable parallel subagent spawning

Open `main.py` and find the TODO in the `while response.stop_reason == "tool_use"` loop (around line 100).

Currently the code only processes the first tool call and returns placeholder errors for the rest. Replace the sequential block with a loop that processes **all** tool calls:

```python
        for call in tool_calls:
            task_result = execute_task(
                client, call.input["agent_type"], call.input["prompt"]
            )
            result_entry = {
                "type": "tool_result",
                "tool_use_id": call.id,
                "content": task_result
            }
            tool_results.append(result_entry)
```

Remove the placeholder error block below it.

Run `python main.py` again.

**What to observe:**

1. The coordinator now spawns **multiple search subagents in a single turn** — one per subtopic.
2. All search results flow back to the coordinator before it decides the next step.
3. The analysis/synthesis agents still fail (you fix that next), but the coordinator now has search results from all subtopics.

**Exam concept demonstrated:**
- **Parallel subagent spawning** (task 1.3): multiple Task tool calls in a single coordinator response, rather than one per turn.

### Step 4 — Complete the analysis and synthesis agents

Open `agents.py`. You need to fill in three groups of TODOs:

**4a. Define the `analyze_document` tool** (find the TODO after the search agent tools):

```python
@tool(
    description=(
        "Analyze research documents and extract structured claim-source mappings "
        "for a given subtopic. "
        "Input: a subtopic keyword (e.g., 'diagnosis', 'drug_discovery', 'patient_care'). "
        "Returns: list of findings, each with claim, source_url, excerpt, date, and confidence. "
        "Use for: extracting structured findings from collected research sources. "
        "Do NOT use for: searching for new sources — use web_search instead."
    ),
    param_descriptions={
        "subtopic": "The subtopic keyword to analyze documents for"
    }
)
def analyze_document(subtopic: str):
    """Extract structured findings from mock analysis data."""
    for keyword, findings in ANALYSIS_FINDINGS.items():
        if keyword in subtopic.lower() or subtopic.lower() in keyword:
            return findings
    first_key = list(ANALYSIS_FINDINGS.keys())[0]
    fallback = ANALYSIS_FINDINGS[first_key]
    return fallback
```

**4b. Define the `compile_report` tool** (find the TODO after analyze_document):

```python
@tool(
    description=(
        "Compile analyzed findings into a structured research report with "
        "claim-source mappings preserved. "
        "Input: findings_json containing all analyzed findings as a JSON string, "
        "and optional coverage_notes describing any gaps. "
        "Returns: structured report with findings, coverage annotations, and "
        "compilation status. "
        "Use for: producing the final synthesis output. "
        "Do NOT use for: searching or analyzing — all findings must be provided as input."
    ),
    param_descriptions={
        "findings_json": "JSON string containing all analyzed findings with claim-source mappings",
        "coverage_notes": "Notes on coverage gaps or unavailable sources to annotate in the report"
    }
)
def compile_report(findings_json: str, coverage_notes: str = ""):
    """Compile findings into a structured report."""
    findings = json.loads(findings_json)
    report = {
        "findings": findings,
        "coverage_notes": coverage_notes or "No gaps noted",
        "compiled": True
    }
    return report
```

**4c. Define the agent prompts and configs** (find the remaining TODOs):

Replace `ANALYSIS_AGENT_PROMPT = None` with:

```python
ANALYSIS_AGENT_PROMPT = (
    "You are a document analysis research agent. Your role is to extract "
    "structured claim-source mappings from research documents.\n\n"
    "Instructions:\n"
    "- Use the analyze_document tool to extract findings for the given subtopic\n"
    "- Every claim MUST have a source_url and excerpt — never state a finding "
    "without attribution (task 5.6)\n"
    "- Include the publication date for temporal context\n"
    "- Flag conflicting statistics with source attribution rather than selecting one\n"
    "- Rate confidence as 'high', 'medium', or 'low'\n\n"
    "Output your findings as structured data the synthesis agent can use directly."
)
```

Replace `SYNTHESIS_AGENT_PROMPT = None` with:

```python
SYNTHESIS_AGENT_PROMPT = (
    "You are a research synthesis agent. Your role is to compile analyzed findings "
    "into a comprehensive, cited research report.\n\n"
    "Instructions:\n"
    "- Use the compile_report tool to produce the final report\n"
    "- Preserve ALL source attributions — every claim must trace to a source URL "
    "and excerpt (task 5.6)\n"
    "- Organize findings into: well-supported (multiple sources), contested "
    "(conflicting data), and coverage gaps\n"
    "- When statistics conflict, annotate the conflict with both values and sources\n"
    "- Include publication dates to prevent temporal differences from being "
    "misinterpreted as contradictions\n"
    "- Note any coverage gaps due to unavailable sources or failed subagent tasks "
    "(task 5.3)\n\n"
    "The report should be useful as a standalone reference document."
)
```

Add the analysis and synthesis entries to `AGENT_CONFIGS`:

```python
AGENT_CONFIGS = {
    "search": {
        "system": SEARCH_AGENT_PROMPT,
        "tools": [web_search.tool_schema],
        "handlers": {"web_search": web_search}
    },
    "analysis": {
        "system": ANALYSIS_AGENT_PROMPT,
        "tools": [analyze_document.tool_schema],
        "handlers": {"analyze_document": analyze_document}
    },
    "synthesis": {
        "system": SYNTHESIS_AGENT_PROMPT,
        "tools": [compile_report.tool_schema],
        "handlers": {"compile_report": compile_report}
    }
}
```

Run `python main.py` again.

**What to observe:**

1. The full pipeline now works: search → analysis → synthesis → final report.
2. The **analysis agent** extracts structured claim-source mappings — each finding has `claim`, `source_url`, `excerpt`, `date`, and `confidence`.
3. The **synthesis agent** compiles a report that preserves source attribution through every stage.
4. The coordinator passes **all search results explicitly** in the analysis prompt — subagents don't inherit context (task 1.3).

**Exam concepts demonstrated:**
- **Explicit context passing** (task 1.3): the coordinator includes complete prior findings in each subagent's prompt.
- **Tool distribution** (task 2.3): each subagent has only its role-relevant tool — the search agent cannot analyze, the analysis agent cannot search.
- **Tool descriptions with boundaries** (task 2.1): each tool description states what it does AND what NOT to use it for.
- **Provenance preservation** (task 5.6): claim-source mappings flow from search → analysis → synthesis without losing attribution.

### Step 5 — Trigger a search timeout and observe error propagation

Open `config.py` and change:

```python
SIMULATE_SEARCH_TIMEOUT = True
```

Run `python main.py` again with the default topic.

**What to observe:**

1. One search subagent (the one querying drug discovery) returns a **structured timeout error** instead of results.
2. The error includes `failure_type`, `attempted_query`, `partial_results`, and `alternatives` — not a generic "search failed" message.
3. The coordinator receives this structured error and passes it to the synthesis agent.
4. The synthesis output should annotate the **coverage gap** for the drug discovery subtopic.

**Exam concepts demonstrated:**
- **Structured error propagation** (task 5.3): the error includes context that enables intelligent recovery — failure type, what was attempted, partial results, and alternative approaches.
- **Not silently suppressing errors** (task 5.3): the error is not hidden or returned as empty success — it flows through to synthesis as an explicit gap.
- **Coverage gap annotation** (task 5.3): the synthesis output distinguishes well-supported findings from areas where sources were unavailable.
- **Partial results preserved** (task 5.3): even the failed subagent returned one result before timing out — this partial data is available to the coordinator.

### Step 6 — Add narrow-decomposition detection

The coordinator can decompose a topic too narrowly — for example, splitting "AI in healthcare" into three radiology subtopics. This is a key exam concept (task 1.2).

> **Prompt for Claude Code:**
> `Add a validate_decomposition function to main.py that takes the original topic and the list of subtopics from the coordinator's first response. It should check whether subtopics overlap excessively by looking for repeated keywords. If more than half the subtopics share the same key terms, print a warning in YELLOW suggesting the decomposition may be too narrow. Call this function after the coordinator's first iteration, extracting subtopics from the task tool call prompts.`

Run `python main.py` and try a topic like "machine learning applications" to verify the validator works.

**What to observe:**

1. The validator analyzes the coordinator's subtopic decomposition before subagents run.
2. For well-decomposed topics, no warning appears.
3. If you re-run and the coordinator happens to produce overlapping subtopics, the warning fires.

**Exam concept demonstrated:**
- **Risks of overly narrow task decomposition** (task 1.2): the coordinator might create subtopics that all cover the same narrow area, leading to incomplete coverage of the broader topic — exactly the failure mode described in exam question 7.

## Reset

To restore the lab to its starter state:

```bash
python reset.py
```

Set `SIMULATE_SEARCH_TIMEOUT = False` in `config.py` to disable the timeout simulation.
