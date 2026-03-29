# Lab 03 — Gap Analysis (Post-Build Review)

Comparison of the Exam Guide, Lab Reference, Lab Plan, and actual Lab (README + code) for Scenario 3.
This is the second analysis — after the lab builder applied fixes from the first analysis.

**Tasks covered by Lab 03:** 1.2, 1.3, 1.5, 1.6, 2.1, 2.2, 2.3, 5.1, 5.3, 5.6

**Note:** The lab builder added Task 1.5 (hooks) which was not in the original plan. The lab now uses `PreToolUse` and `PostToolUse` hooks for real-time observability and violation detection. Also added a 4th subagent (**report-agent**) to match the exam scenario which says "one generates reports."

---

## Task 1.2 — Orchestrate multi-agent systems with coordinator-subagent patterns

### Exam Guide says

**Knowledge:**
- Hub-and-spoke: coordinator manages all inter-subagent communication and routing
- Subagents operate with isolated context — do not inherit coordinator history
- Coordinator role: task decomposition, delegation, result aggregation, dynamic subagent selection
- Risks of overly narrow task decomposition leading to incomplete coverage

**Skills:**
- Design coordinator that dynamically selects subagents based on query requirements (not always full pipeline)
- Partition research scope across subagents to minimize duplication
- Implement iterative refinement: evaluate output for gaps, re-delegate, re-synthesize
- Route all communication through coordinator for observability

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Hub-and-spoke | ✅ | Step 3: "The coordinator routes all communication — subagents never talk to each other directly." `allowed_tools=["Agent"]` — coordinator can only spawn subagents, not call MCP tools directly. |
| Isolated subagent context | ✅ | Step 3, Step 7. `coordinator.txt`: "they do NOT inherit your conversation history." |
| Dynamic subagent selection | ✅ | Step 7: "The coordinator dynamically selects which subagents to invoke based on query requirements." |
| Overly narrow decomposition | ✅ | Step 7: Query 3 demonstrates narrow topic with incomplete results. |
| Iterative refinement | ⚠️ GAP | Not exercised or mentioned. The coordinator does one pass: search → analyze → synthesize → report. The exam tests re-delegation when coverage is insufficient. |
| All communication through coordinator | ✅ | Architecture enforces this — `allowed_tools=["Agent"]` means the coordinator purely delegates. |

**Recommend:** Add a note in Step 7 about iterative refinement. Example: "In production, the coordinator would evaluate synthesis output for coverage gaps, re-delegate to search/analysis with targeted queries, and re-invoke synthesis. This lab uses a single pass for simplicity, but the exam tests the iterative refinement pattern. [Task 1.2]"

---

## Task 1.3 — Configure subagent invocation, context passing, and spawning

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Agent tool for spawning | ✅ | `allowed_tools=["Agent"]`. Step 3 and the Agent tool name callout box. |
| Explicit context passing | ✅ | Step 7. `coordinator.txt`: "Include ALL relevant prior findings directly in the subagent's prompt." |
| AgentDefinition | ✅ | `agents.py` — four `AgentDefinition` objects with descriptions, prompts, and tools TODOs. |
| Structured data (content vs metadata) | ✅ | `search_agent.txt` outputs claim-source mappings. `coordinator.txt` context passing rules. |
| Parallel subagent spawning | ⚠️ PARTIAL | The coordinator prompt says "Keep the workflow to exactly 4 subagent calls" but does not explicitly instruct parallel spawning. The README mentions observing spawning but doesn't ask the student to verify parallel vs sequential. |
| Goals/criteria, not step-by-step | ✅ | Step 7: "The coordinator specifies research goals and quality criteria, not step-by-step procedures." |

**Recommend:** Add a brief callout in Step 3 or Step 7 asking the student to observe whether the coordinator spawns agents in the same turn (parallel) or across separate turns (sequential). Note that parallel spawning is more efficient. [Task 1.3]

---

## Task 1.5 — Apply Agent SDK hooks for tool call interception and data normalization

**This is new — added by the lab builder.** Not in the original plan but now exercised.

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| PreToolUse hook | ✅ | `main.py:185` — `on_pre_tool_use` logs every tool call with agent label, detects violations. |
| PostToolUse hook | ✅ | `main.py:240` — `on_post_tool_use` logs completion with result summary. |
| Hooks for observability | ✅ | Step 3 explains how hooks intercept tool calls for real-time feedback. "This is the same pattern used to build audit logs, compliance checks, and real-time dashboards." |
| Hooks run outside context window | ✅ | Step 3: "They run in your process, not inside the agent's context window." |
| Data normalization | ⚠️ GAP | The hooks log and detect violations but do not normalize data formats (timestamps, status codes). This is the same gap noted in Lab 01. |
| Compliance enforcement via hooks | ⚠️ PARTIAL | The violation detection is observability only — it prints a warning but does not block the tool call. Lab 01 demonstrates the blocking pattern. |

**Assessment:** The hooks are a strong addition for observability. The exam's compliance and normalization patterns are covered by Lab 01. A cross-reference note would be sufficient.

---

## Task 1.6 — Design task decomposition strategies for complex workflows

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Overly narrow decomposition | ✅ | Step 7 — Query 3 demonstrates. `coordinator.txt` warns against it. |
| Dynamic vs fixed decomposition | ⚠️ GAP | The README never explicitly names these two patterns. The coordinator uses adaptive decomposition (adjusts search based on topic) but the exam also tests fixed sequential pipelines (prompt chaining). |

**Recommend:** Add a note in Step 7 naming the two patterns. Example: "The coordinator uses adaptive decomposition — adjusting what to search based on the topic. The exam also tests fixed sequential pipelines (prompt chaining) — predictable multi-step workflows like per-file analysis + cross-file integration. Lab 05 demonstrates the fixed pipeline pattern. [Task 1.6]"

---

## Task 2.1 — Design effective tool interfaces with clear descriptions and boundaries

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Detailed tool descriptions | ✅ | `main.py:36-47` and `85-95` — detailed descriptions with purpose, inputs, examples, boundaries. Step 7 calls this out. |
| Boundaries vs similar tools | ✅ | Each description says when to use it vs the other tool. |
| System prompt keyword sensitivity | ⚠️ GAP | Not mentioned. Lab 01 covers this — cross-reference sufficient. |

---

## Task 2.2 — Implement structured error responses for MCP tools

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| `isError` flag | ✅ | `main.py:122` — `"isError": True`. Step 5.5 mentions it. |
| Structured error with context | ✅ | Step 5.3 — student implements structured timeout response. |
| Generic vs structured contrast | ✅ | Step 5.2 shows the problem; Step 5.3 fixes it. |
| Access failure vs valid empty result | ⚠️ GAP | No scenario where a search returns zero results (valid empty). All not-found cases are errors. |

**Recommend:** Brief note in Step 5.5. Lab 01 also has this gap — a conceptual note is sufficient.

---

## Task 2.3 — Distribute tools across agents and configure tool choice

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Tool restriction per subagent | ✅ | Step 4 — student adds `tools` lists. |
| Too many tools degrades reliability | ✅ | Step 4.2 and 4.5. |
| Out-of-role misuse visible | ✅ | Violation warnings make this observable. |
| `tools=[]` for no-tool agents | ✅ | Both synthesis-agent and report-agent get `tools=[]`. |
| `tool_choice` configuration | ⚠️ GAP | Not mentioned. Lab 01 covers this. |
| Scoped cross-role tools | ⚠️ GAP | Not mentioned. The exam says: "Providing scoped cross-role tools for high-frequency needs (e.g., a verify_fact tool for the synthesis agent)." |

**Recommend:** Brief note in Step 4.5 about `tool_choice` (cross-reference Lab 01) and scoped cross-role tools.

---

## Task 5.1 — Manage conversation context across long interactions

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Subagent structured output with metadata | ✅ | `search_agent.txt` and `analysis_agent.txt` output structured claim-source mappings. |
| Key findings at beginning / position effects | ✅ | `synthesis_agent.txt`: "Place key findings at the beginning of the report to mitigate position effects." |
| Context trimming | ✅ | Step 7: "The coordinator trims verbose tool outputs to key findings." |
| "Lost in the middle" effect | ⚠️ GAP | The synthesis prompt mitigates it but the README never names the effect. |

**Recommend:** Brief note in Step 7 naming the "lost in the middle" effect.

---

## Task 5.3 — Implement error propagation across multi-agent systems

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Structured error context | ✅ | Step 5 — student implements structured timeout response. |
| Anti-patterns (suppress/terminate) | ✅ | Step 5.5 mentions both anti-patterns. |
| Coverage gap annotations | ✅ | Step 6 — student enhances synthesis prompt via Claude Code. |
| Local recovery for transient failures | ⚠️ PARTIAL | Step 6.4 mentions it but no subagent actually retries. |

**Recommend:** Brief note in Step 5.5 about local recovery vs propagation.

---

## Task 5.6 — Preserve information provenance in multi-source synthesis

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Claim-source mappings | ✅ | `search_agent.txt`, `synthesis_agent.txt`. Step 7. |
| Well-established vs contested sections | ✅ | `synthesis_agent.txt` has "Key Findings" and "Contested or Uncertain Findings" sections. |
| Conflicting statistics with attribution | ✅ | `data.py` PharmaTech vs WHO disagreement. Step 7. |
| Temporal data / publication dates | ✅ | `analysis_agent.txt` and `synthesis_agent.txt`. |
| Content-type rendering | ⚠️ GAP | Not mentioned. The exam says: "financial data as tables, news as prose, technical as structured lists." |

**Recommend:** Brief note in Step 7.

---

## Changes Since First Analysis

| Item | First Analysis | Current Status |
|------|---------------|----------------|
| Coordinator had MCP tools in allowed_tools | ⚠️ Issue | ✅ Fixed — now `allowed_tools=["Agent"]` only |
| 3 subagents | Original | Now 4 — added **report-agent** (matches exam scenario "one generates reports") |
| No hooks | Original | ✅ Added — `PreToolUse`/`PostToolUse` for observability + violation detection (Task 1.5) |
| Task 1.5 not in coverage | Not listed | ✅ Now listed in exam coverage table |
| Agent tool name callout | Not present | ✅ Added — blockquote explaining Task→Agent rename |

---

## Summary of Remaining Gaps

### Gaps in Lab Reference
None. Updated: 4 subagents, Task 1.5 added, hooks in build line.

### Gaps in Lab Plan
None. Updated: Tasks covered includes 1.5, "What you build" says 4 subagents + hooks, files list complete, "Agent calls" in What to observe.

### Gaps in Actual Lab (README + code)

None. All 10 README note gaps fixed:

| # | Task | Gap | Fix Applied |
|---|------|-----|-------------|
| 1 | 1.2 | Iterative refinement | Note in Step 7 blockquote |
| 2 | 1.3 | Parallel spawning | Callout in Step 3 exam concept |
| 3 | 1.6 | Decomposition patterns | Note in Step 7 blockquote |
| 4 | 2.1 | System prompt keyword sensitivity | Note in Step 7 blockquote |
| 5 | 2.2 | Access failure vs empty result | Note in Step 5.5 blockquote |
| 6 | 2.3 | `tool_choice` | Note in Step 4.5 blockquote |
| 7 | 2.3 | Scoped cross-role tools | Note in Step 4.5 blockquote |
| 8 | 5.1 | "Lost in the middle" effect | Note in Step 7 blockquote |
| 9 | 5.3 | Local recovery | Note in Step 5.5 blockquote |
| 10 | 5.6 | Content-type rendering | Added to Step 7 exam concepts |

### Priority Recommendation

**All gaps resolved.** The lab is architecturally sound — the coordinator is correctly restricted to `Agent` only, hooks provide real-time observability, and the 4-agent structure matches the exam scenario. All 10 README note gaps have been fixed with callouts in existing steps.

**Lab Plan:** Updated. No remaining gaps.
**Lab Reference:** Updated. No remaining gaps.
**Styling inconsistencies:** Verified clean — task reference periods and prompt block specifiers both fixed.

---

*Analysis performed 2026-03-29 — Alfredo De Regil*
