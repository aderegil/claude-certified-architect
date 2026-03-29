# Lab 01 — Gap Analysis

Comparison of the Exam Guide, Lab Reference, Lab Plan, and actual Lab (README + code) for Scenario 1.

**Tasks covered by Lab 01:** 1.1, 1.2, 1.4, 1.5, 2.1, 2.2, 2.3, 5.1, 5.2

---

## Task 1.1 — Design and implement agentic loops

### Exam Guide says

**Knowledge:**
- Agentic loop lifecycle: `stop_reason` "tool_use" vs "end_turn", executing tools, returning results
- Tool results appended to conversation history for next-iteration reasoning
- Model-driven decision-making vs pre-configured decision trees or tool sequences

**Skills:**
- Implement loop: continue on "tool_use", terminate on "end_turn"
- Add tool results to conversation context between iterations
- Avoid anti-patterns: parsing natural language signals for termination, arbitrary iteration caps as primary stopping mechanism, checking assistant text content as completion indicator

### Lab Reference
✅ Covers all three knowledge items and all three skills verbatim.

### Lab Plan
✅ "Agentic loop: `stop_reason == "tool_use"` → execute → continue; `"end_turn"` → stop" — covers the core.

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Loop lifecycle (tool_use/end_turn) | ✅ | `main.py:133-140` — checks `stop_reason`, prints it on each iteration. README Step 3 explicitly asks student to observe it. |
| Tool results appended to history | ✅ | `main.py:166-169` — appends assistant message and tool results. README Step 3 mentions it. |
| Model-driven decision-making | ✅ | README Step 3: "The model drives decision-making about which tool to call next; there is no pre-configured decision tree." |
| Anti-patterns | ⚠️ GAP | The exam guide lists three anti-patterns to avoid: (1) natural language termination signals, (2) arbitrary iteration caps as primary stopping mechanism, (3) checking assistant text as completion indicator. The README does **not** mention these anti-patterns anywhere. The code uses `MAX_LOOP_ITERATIONS = 10` with a `for` loop — while the `stop_reason` check is the primary mechanism, the iteration cap exists and the README never explains why it's a safety net, not the primary mechanism. A student could mistake the `for range(MAX_LOOP_ITERATIONS)` pattern as the recommended approach. **Recommend:** Add a brief note in Step 3 or Step 8 explaining that the iteration cap is a safety net, not the termination mechanism — the exam tests that `stop_reason` drives the loop, not iteration counts. Mention the three anti-patterns. |

---

## Task 1.2 — Orchestrate multi-agent systems with coordinator-subagent patterns

### Exam Guide says

**Knowledge:**
- Hub-and-spoke: coordinator manages all inter-subagent communication
- Subagents operate with isolated context — no inherited coordinator history
- Coordinator role: task decomposition, delegation, result aggregation, dynamic subagent selection
- Risks of overly narrow task decomposition

**Skills:**
- Dynamic subagent selection based on query requirements
- Partition research scope to minimize duplication
- Iterative refinement loops
- Route all communication through coordinator for observability

### Lab Reference
✅ Full knowledge and skills listed.

### Lab Plan
✅ Listed as a covered task.

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Coverage | ⚠️ MINIMAL | The README lists Task 1.2 in the exam coverage table but **no step in the lab actually demonstrates multi-agent orchestration**. Lab 01 is a single-agent system with tools, not a coordinator-subagent architecture. The Lab Reference correctly lists L3 as the primary lab for 1.2 and L1 as secondary. |

**Assessment:** This is a secondary coverage assignment — L3 is primary. The question is whether Lab 01 adds anything for 1.2. Currently it doesn't. The escalation handoff (`escalate_to_human`) is the closest thing to a "subagent" pattern, but it's a tool call, not a subagent spawn.

**Recommend:** Either (a) remove 1.2 from Lab 01's coverage list if L3 handles it fully, or (b) add a brief callout in Step 8 acknowledging that the single-agent-with-tools pattern here contrasts with the coordinator-subagent pattern in Lab 03, so the student sees the progression. Option (b) is lighter and more honest — Lab 01 shows the single-agent side of the spectrum; Lab 03 shows multi-agent.

---

## Task 1.4 — Implement multi-step workflows with enforcement and handoff patterns

### Exam Guide says

**Knowledge:**
- Programmatic enforcement (hooks, gates) vs prompt-based guidance
- Prompt-only ordering has non-zero failure rate — insufficient for critical business logic
- Structured handoff protocols: customer details, root cause, recommended actions

**Skills:**
- Implement prerequisite gate blocking downstream tools until prior step completes
- Decompose multi-concern requests into parallel investigations, then synthesize unified resolution
- Compile structured handoff summary (customer ID, root cause, amount, action) on escalation

### Lab Reference
✅ All items covered.

### Lab Plan
✅ "Programmatic prerequisite gate: `process_refund` is blocked until `get_customer` has run"

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Prerequisite gate | ✅ | Step 4 — student implements `check_prerequisite`. README explains why prompt-only is insufficient. |
| Prompt vs programmatic distinction | ✅ | Step 4.2 and 4.5 explicitly contrast the two. |
| Structured handoff summary | ✅ | Step 5.4: "The agent should call `escalate_to_human` with a structured summary including customer ID, root cause, and recommended action." `escalate_to_human` schema requires `customer_id`, `reason`, `summary`, `recommended_action`. |
| Multi-concern decomposition | ⚠️ GAP | The exam guide skill says: "Decomposing multi-concern customer requests into distinct items, then investigating each in parallel using shared context before synthesizing a unified resolution." **No step in the lab exercises this.** There is no test query that presents multiple issues in a single message. |

**Recommend:** Add a test query (menu option or manual suggestion) like: "I'm Maria Santos CUST-1001. My headphones from ORD-5501 arrived damaged AND I need to check if my other order ORD-5502 has shipped yet." Then note what to observe: the agent should investigate both issues using shared context, not abandon one. This could be a short callout in Step 8 or a new Step 6.5 without requiring code changes.

---

## Task 1.5 — Apply Agent SDK hooks for tool call interception and data normalization

### Exam Guide says

**Knowledge:**
- PostToolUse hook intercepts tool results for transformation before model processes them
- Hooks intercept outgoing tool calls to enforce compliance rules
- Hooks provide deterministic guarantees that prompts cannot

**Skills:**
- PostToolUse to normalize heterogeneous data formats (Unix timestamps, ISO 8601, status codes)
- Intercept hook to block policy-violating actions and redirect to alternative workflows
- Choose hooks over prompt enforcement when business rules require guaranteed compliance

### Lab Reference
✅ All items covered.

### Lab Plan
✅ "PostToolUse hook: intercepts refunds > $500, returns structured error"

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| PostToolUse interception | ✅ | Step 5 — student implements `post_tool_use_hook`. |
| Compliance enforcement | ✅ | Blocks refunds > $500, redirects to escalation. |
| Deterministic vs probabilistic | ✅ | Step 5.5 explicitly states "PostToolUse hooks provide deterministic guarantees that prompt instructions cannot." |
| Data normalization | ⚠️ GAP | The exam guide specifically lists a skill: "PostToolUse hooks to normalize heterogeneous data formats (Unix timestamps, ISO 8601, numeric status codes)." **The lab does not exercise data normalization at all.** The hook only does compliance blocking. |

**Recommend:** This is a real gap. The data already has mixed formats — `data.py` has ISO 8601 timestamps (`"2025-02-14T16:45:00Z"`). A normalization hook could convert these to human-readable dates before the model processes them. This could be added as a small complement step (e.g., Step 5.5 becomes a new TODO or Claude Code prompt: "Add normalization to `post_tool_use_hook` that converts ISO timestamps to readable format"). Alternatively, note this as an awareness item in the README with a reference to the exam concept and suggest it as a stretch exercise.

---

## Task 2.1 — Design effective tool interfaces with clear descriptions and boundaries

### Exam Guide says

**Knowledge:**
- Tool descriptions are the primary mechanism for tool selection
- Descriptions must include: input formats, example queries, edge cases, boundaries vs similar tools
- Ambiguous/overlapping descriptions cause misrouting
- System prompt wording can create unintended tool associations

**Skills:**
- Write descriptions that differentiate purpose, inputs, outputs, when to use vs alternatives
- Rename tools to eliminate functional overlap
- Split generic tools into purpose-specific tools
- Review system prompts for keyword-sensitive instructions overriding tool descriptions

### Lab Reference
✅ All items listed.

### Lab Plan
✅ "Tool descriptions differentiate each tool's purpose"

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Differentiated descriptions | ✅ | `tools.py` — each `_schema` has a detailed description with input formats, boundaries, and when to use it. Step 8 calls this out explicitly. |
| Input formats, edge cases | ✅ | Descriptions include format examples (e.g., "e.g., 'CUST-1001'"), edge cases (e.g., "Refunds can only be processed for delivered orders"). |
| System prompt keyword sensitivity | ⚠️ GAP | The exam guide mentions "system prompt wording on tool selection: keyword-sensitive instructions can create unintended tool associations." **Not mentioned in the lab.** |
| Renaming/splitting tools | ✅ N/A | Not directly applicable — the lab's 4 tools are already well-differentiated. This is more of a diagnostic skill tested in exam questions. |

**Recommend:** Minor. Consider adding a brief note in Step 8 about how system prompt wording can accidentally override tool descriptions (e.g., if the system prompt said "always look up customer orders" it might bias toward `lookup_order` even when `get_customer` is appropriate). This is a knowledge/awareness item, not a code change.

---

## Task 2.2 — Implement structured error responses for MCP tools

### Exam Guide says

**Knowledge:**
- `isError` flag pattern for communicating tool failures
- Error categories: transient, validation, business, permission
- Why uniform error responses prevent appropriate recovery
- Retryable vs non-retryable distinction prevents wasted retries

**Skills:**
- Return `errorCategory`, `isRetryable`, human-readable description
- Include `retriable: false` and customer-friendly explanations for business rule violations
- Local error recovery for transient failures, propagate only unresolvable errors
- Distinguish access failures from valid empty results

### Lab Reference
✅ All items listed.

### Lab Plan
✅ "Structured error responses: `errorCategory`, `isRetryable`"

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| errorCategory + isRetryable | ✅ | `tools.py` uses both consistently across all error paths. Step 5 and Step 4 exercise them. |
| Multiple error categories | ✅ | `validation` (missing customer), `business` (non-delivered order), `policy_violation` (hook). |
| Retryable vs non-retryable | ✅ | `get_customer` not-found is `isRetryable: True`; `process_refund` on non-delivered order is `isRetryable: False`. |
| Access failures vs valid empty results | ⚠️ GAP | The exam guide distinguishes between "access failures (needing retry decisions) and valid empty results (representing successful queries with no matches)." **The lab does not have a scenario where a query succeeds but returns zero results** (as opposed to a "not found" error). All not-found cases are treated as errors. |
| `isError` flag (MCP pattern) | ⚠️ MINOR | The lab uses `"error": True` in the response dict rather than the MCP `isError` flag. This is because Lab 01 uses the Client SDK pattern (manual tool execution), not MCP. The exam guide references the MCP `isError` flag pattern. Students should be aware this is the same concept in a different form. |

**Recommend:** For the access-vs-empty distinction: consider adding a note (Step 8 or a callout) explaining the difference. A search tool returning `{"results": []}` is a valid empty result; a timeout is an access failure. The current tools don't have a natural search scenario, so this is better as a conceptual note referencing Lab 03 where it's more natural. For `isError`: minor — consider a brief note that the `"error": True` pattern here is equivalent to MCP's `isError` flag.

---

## Task 2.3 — Distribute tools across agents and configure tool choice

### Exam Guide says

**Knowledge:**
- Too many tools (18 vs 4-5) degrades tool selection reliability
- Agents with out-of-role tools tend to misuse them
- Scoped tool access: only tools needed for the role
- `tool_choice` options: "auto", "any", forced selection

**Skills:**
- Restrict each subagent's tool set to role-relevant tools
- Replace generic tools with constrained alternatives
- Scoped cross-role tools for high-frequency needs
- `tool_choice` forced selection to ensure specific tool runs first
- `tool_choice: "any"` to guarantee tool call

### Lab Reference
✅ All items listed.

### Lab Plan
✅ Listed in key concepts.

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Focused tool set (4 tools) | ✅ | Step 8: "The agent has exactly 4 tools — a focused set for its role. Giving an agent 18 tools degrades selection reliability." |
| Role-relevant tools | ✅ | Step 8 discusses tool distribution. |
| `tool_choice` configuration | ⚠️ GAP | The exam guide knowledge includes `tool_choice` options ("auto", "any", forced). **The lab never demonstrates or mentions `tool_choice`.** The code uses the default (`auto`). The exam specifically tests when to use forced tool selection and `"any"`. |

**Recommend:** Add a note in Step 8 about `tool_choice` options. Example: "The lab uses the default `tool_choice: 'auto'` — the model decides which tool to call. The exam also tests `tool_choice: 'any'` (guarantee a tool call, useful when you need structured output) and forced selection `{"type": "tool", "name": "get_customer"}` (ensure a specific tool runs first). Lab 06 exercises `tool_choice: 'any'` for guaranteed structured extraction."

---

## Task 5.1 — Manage conversation context across long interactions

### Exam Guide says

**Knowledge:**
- Progressive summarization risks: loses numerical values, percentages, dates
- "Lost in the middle" effect: models process beginning/end reliably, may omit middle
- Tool results accumulate tokens disproportionately to relevance
- Complete conversation history must be passed in subsequent API requests

**Skills:**
- Extract transactional facts into persistent "case facts" block outside summarized history
- Extract structured issue data into separate context layer for multi-issue sessions
- Trim verbose tool outputs to relevant fields before they accumulate
- Place key findings at beginning of aggregated inputs; use section headers for position effects
- Require subagents to include metadata in structured outputs
- Modify upstream agents to return structured data instead of verbose content

### Lab Reference
✅ All items listed.

### Lab Plan
✅ "Persistent `case_facts` block outside summarized history (D5.1)"

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Persistent case_facts | ✅ | Step 7 — student adds fact extraction via Claude Code. `system_prompt.txt` has `<case_facts>{case_facts}</case_facts>`. |
| Progressive summarization risk | ✅ | Step 7.1 explains the risk explicitly. |
| Tool result token accumulation | ✅ | Step 7.4: "Tool results accumulate tokens disproportionately to their relevance; `case_facts` extracts only the fields that matter." |
| Trimming verbose tool outputs | ⚠️ GAP | The exam guide skill says: "Trimming verbose tool outputs to only relevant fields before they accumulate in context." **The lab does not trim tool results.** Full tool responses (all fields) are appended to conversation history. `case_facts` extracts key facts, but the raw tool results still accumulate untrimmed. |
| "Lost in the middle" effect | ⚠️ GAP | Not mentioned anywhere in the lab. This is a knowledge item students should be aware of. |
| Complete conversation history | ✅ | `main.py:166-169` passes full history. |

**Recommend:** For trimming: this would be a meaningful code addition — a helper that strips the tool result to only relevant fields before appending it to `messages`. Could be a TODO or Claude Code prompt step. For "lost in the middle": add a brief awareness note in Step 7.4 about the position effect.

---

## Task 5.2 — Design escalation and ambiguity resolution patterns

### Exam Guide says

**Knowledge:**
- Escalation triggers: customer requests human, policy gaps, inability to make progress
- Immediate escalation on explicit customer demand vs offering resolution for straightforward issues
- Sentiment-based escalation is unreliable proxy for case complexity
- Multiple customer matches require clarification, not heuristic selection

**Skills:**
- Explicit escalation criteria with few-shot examples in system prompt
- Honor explicit customer requests immediately without investigation
- Acknowledge frustration while offering resolution when within capability
- Escalate when policy is ambiguous or silent
- Ask for additional identifiers when multiple matches, don't select heuristically

### Lab Reference
✅ All items listed.

### Lab Plan
✅ "Explicit escalation criteria with few-shot examples in system prompt"

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Explicit criteria in system prompt | ✅ | `system_prompt.txt` has four explicit criteria. Step 6 walks through them. |
| Few-shot examples | ✅ | Three examples in system prompt. Step 6 references them. |
| Sentiment not a trigger | ✅ | Few-shot Example 3 explicitly shows frustrated-but-resolvable. Step 6.4: "The criteria drive the decision, not sentiment." |
| Immediate escalation on explicit request | ✅ | Step 6.1/6.4 — test query 4 is exactly this scenario. |
| Policy gap escalation | ✅ | Step 6.4 includes a manual query testing the gift return policy gap. |
| Multiple customer matches → ask for identifiers | ⚠️ GAP | The exam guide says: "Multiple customer matches require clarification (requesting additional identifiers) rather than heuristic selection." **The lab data has only unique customers. There is no scenario where a lookup returns multiple matches.** This is a knowledge item the student never encounters. |
| Acknowledge frustration while offering resolution | ⚠️ MINOR | The few-shot Example 3 covers the concept, but the student never runs a test query that exercises this exact scenario (frustrated customer with a solvable issue). Test query 4 is a customer requesting a human, not a frustrated but resolvable case. |

**Recommend:** For multiple matches: this would require adding a `get_customer` scenario where e.g., searching by partial name returns 2 customers. This is a bigger data change. Consider whether it's worth adding or whether a conceptual note in Step 6 or Step 8 suffices. For acknowledge-frustration: suggest a manual test query in Step 6 like: "This is ridiculous! My order ORD-5501 was supposed to arrive last week!" and note that the agent should resolve (look up the order) rather than escalate.

---

## Summary of Gaps

### Gaps in the Lab Reference
None found. The Lab Reference accurately maps all knowledge and skills from the exam guide for each task assigned to Lab 01.

### Gaps in the Lab Plan

| Gap | Severity | Details |
|-----|----------|---------|
| No mention of anti-patterns (1.1) | Low | The plan says "agentic loop" but doesn't flag the three anti-patterns the exam tests |
| No mention of tool_choice (2.3) | Low | Plan mentions tool distribution but not `tool_choice` configuration |
| No mention of data normalization hooks (1.5) | Low | Plan only mentions compliance interception, not the normalization skill |

### Gaps in the Actual Lab (README + code)

| # | Task | Gap | Severity | Fix Effort |
|---|------|-----|----------|------------|
| 1 | 1.1 | Anti-patterns not mentioned (iteration caps, NL termination, text-check completion) | Medium | Low — add a note in Step 3 or Step 8 |
| 2 | 1.2 | Listed in coverage but not demonstrated | Low | Low — add contrast note in Step 8 or remove from coverage |
| 3 | 1.4 | Multi-concern decomposition not exercised | Medium | Low — add a test query with two issues |
| 4 | 1.5 | Data normalization hook not exercised | Medium | Medium — add a normalization step or stretch exercise |
| 5 | 2.1 | System prompt keyword sensitivity not mentioned | Low | Low — add a note in Step 8 |
| 6 | 2.2 | Access failure vs valid empty result not distinguished | Low | Low — add conceptual note |
| 7 | 2.3 | `tool_choice` not demonstrated or mentioned | Medium | Low — add awareness note in Step 8 |
| 8 | 5.1 | Tool result trimming not practiced | Medium | Medium — add a trimming step or Claude Code prompt |
| 9 | 5.1 | "Lost in the middle" effect not mentioned | Low | Low — add a note in Step 7.4 |
| 10 | 5.2 | Multiple customer matches scenario missing | Low | Medium — requires data change or note |
| 11 | 5.2 | Frustrated-but-resolvable test query missing | Low | Low — suggest a manual query |

### Priority Recommendation

**Quick wins (notes/callouts, no code changes):** Gaps 1, 2, 5, 6, 7, 9, 11
These can all be addressed by adding brief notes to existing steps. No code changes required. Estimated: 15 minutes of README editing.

**Medium effort (new test query or small code addition):** Gaps 3, 4, 8, 10
These require either adding test queries to the menu, adding a new TODO/step, or modifying data. Each is ~10-15 minutes.

---

*Analysis performed 2026-03-29 — Alfredo De Regil*
