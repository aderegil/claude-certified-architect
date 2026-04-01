# Lab 01 — Customer Support Resolution Agent

## Objective

Build a customer support agent with four MCP-style tools, an agentic loop driven by `stop_reason`, a programmatic prerequisite gate, and a PostToolUse hook that enforces refund policy. By the end you will have a working agent that handles real-feeling customer conversations — looking up accounts, processing refunds, and escalating when appropriate — all grounded in exam concepts you can trace back to specific task statements.

## Exam coverage

**Scenario:** S1 — Customer Support Resolution Agent
**Domains:** D1 · D2 · D5

| Task | Statement |
|------|-----------|
| 1.1 | Design and implement agentic loops |
| 1.2 | Orchestrate multi-agent systems with coordinator-subagent patterns |
| 1.4 | Implement multi-step workflows with enforcement and handoff patterns |
| 1.5 | Apply Agent SDK hooks for tool call interception and data normalization |
| 2.1 | Design effective tool interfaces with clear descriptions and boundaries |
| 2.2 | Implement structured error responses for MCP tools |
| 2.3 | Distribute tools across agents and configure tool choice |
| 5.1 | Manage conversation context across long interactions |
| 5.2 | Design escalation and ambiguity resolution patterns |

## Lab guide

### Step 0 — Open the lab folder

Open the **`01_customer_support_agent/`** folder in VSCode.
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

### Step 3 — Run the agent and observe the agentic loop

#### 3.1 Orient yourself

Before running, open these files to understand the starter design:

- **`tools.py`** — four tool functions (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`), each paired with a companion `_schema` dict. The schema is what Claude sees; the function is what executes when Claude calls it.
- **`main.py`** — find the `while` loop. It checks `stop_reason == "tool_use"` to continue and `"end_turn"` to stop. This is the agentic loop you will observe in action.
- **`system_prompt.txt`** — the system prompt with escalation criteria and a `{case_facts}` template variable (currently empty — you will populate it in Step 7).

#### 3.2 Run

```bash
python main.py
```

The agent starts with a menu of numbered test queries covering key lab scenarios. You can also type any custom message. Use `c` to clear the screen or `q` to quit.

Type `1` to run the first test query (an order status check for Maria Santos).

**What to observe:**
- The agent calls `get_customer` first, then `lookup_order` — each tool call is a separate iteration of the agentic loop
- Each iteration prints `stop_reason: tool_use` — this tells the loop to execute the tool and continue
- After all tool calls are done, `stop_reason: end_turn` appears — this tells the loop to stop and print the final response
- Tool results are appended to the conversation history so the model can reason about them on the next iteration
- `case_facts` prints on each iteration — currently "No facts collected yet." (you'll populate this in Step 7)

**Exam concept:** The agentic loop lifecycle — `stop_reason == "tool_use"` means continue, `"end_turn"` means stop. The model drives decision-making about which tool to call next; there is no pre-configured decision tree. [Task 1.1]

> **Anti-patterns to know for the exam:** The code uses `MAX_LOOP_ITERATIONS` as a safety net, but `stop_reason` is the real termination mechanism — not the iteration cap. The exam tests three anti-patterns: (1) using arbitrary iteration caps as the *primary* stopping mechanism, (2) parsing natural language signals to decide when to stop (e.g., checking if the agent said "I'm done"), (3) checking for assistant text content as a completion indicator. All three bypass `stop_reason`, which is the correct signal. [Task 1.1]

### Step 4 — Complete the prerequisite gate

#### 4.1 Test

Type `2` to test a refund request for Maria Santos.

#### 4.2 The problem

The agent calls `get_customer`, then `lookup_order`, then `process_refund` — and the refund succeeds. That looks correct. But there is no _programmatic guarantee_ that `get_customer` runs first. The system prompt says "always verify the customer," but prompt instructions have a non-zero failure rate. If the model ever skips `get_customer` and calls `process_refund` directly, the refund goes through on an unverified customer. For financial operations, "usually works" is not good enough.

#### 4.3 The fix

Open `main.py` and find the `check_prerequisite` function — it's a TODO that currently does nothing. Complete it:

```python
def check_prerequisite(tool_name, tool_history):
    """Block process_refund unless get_customer has already been called successfully."""
    if tool_name == "process_refund" and "get_customer" not in tool_history:
        result = {
            "error": True,
            "errorCategory": "validation",
            "isRetryable": True,
            "message": "Customer identity must be verified via get_customer before processing a refund.",
        }
        return result
    return None
```

Re-run with query `2`. The behavior should be the same because the model already calls `get_customer` first. The gate is a safety net — it guarantees compliance even when prompts fail.

#### 4.4 What to observe

- The gate checks `tool_history` — a set of tool names that have completed successfully
- If `get_customer` is missing, the gate returns a structured error with `isRetryable: True`
- The agent receives this error and calls `get_customer` before retrying the refund

#### 4.5 Exam concept

Programmatic enforcement (hooks, prerequisite gates) vs prompt-based guidance. When deterministic compliance is required — like identity verification before financial operations — prompt instructions alone are insufficient. [Task 1.4]

#### 4.6 Try a multi-concern request

Type `5` to test a message where Maria Santos asks about two issues at once: a damaged-item refund AND a delivery status check on a different order.

**What to observe:**
- The agent should investigate both issues — not abandon one to focus on the other
- It calls `get_customer` once, then uses the shared customer context to handle both `lookup_order` calls and the refund
- The final response synthesizes both answers into a unified reply

**Exam concept:** Decomposing multi-concern customer requests into distinct items, investigating each using shared context, and synthesizing a unified resolution. [Task 1.4]

### Step 5 — Complete the PostToolUse hook

#### 5.1 Test

Type `3` to test James Chen requesting a refund for his $649.99 monitor (order ORD-5503).

#### 5.2 The problem

The refund amount is $649.99, but company policy caps refunds at $500. Right now the agent processes the refund anyway — there is nothing stopping it. The system prompt does not mention a dollar limit, and even if it did, a prompt instruction like "don't process refunds over $500" can be ignored by the model. You need a hook that _deterministically_ blocks the refund before the model ever sees the result.

#### 5.3 The fix

Open `main.py` and find the `post_tool_use_hook` function — it's a TODO that currently passes all results through unchanged. Complete it:

```python
def post_tool_use_hook(tool_name, tool_input, tool_result):
    """Intercept tool results to enforce policy rules."""
    if tool_name == "process_refund" and tool_input.get("amount", 0) > MAX_REFUND_AMOUNT:
        result = {
            "error": True,
            "errorCategory": "policy_violation",
            "isRetryable": False,
            "message": f"Refund amount ${tool_input['amount']:.2f} exceeds the ${MAX_REFUND_AMOUNT} policy limit. This refund must be escalated to a human agent.",
            "action": "escalate_to_human",
        }
        return result
    return tool_result
```

Re-run with query `3`.

#### 5.4 What to observe

- The hook intercepts _after_ the tool executes but _before_ the model processes the result
- The replacement result includes `errorCategory: "policy_violation"` and `isRetryable: False` — structured metadata that tells the agent not to retry
- The `action: "escalate_to_human"` hint guides the agent to escalate instead
- The agent should call `escalate_to_human` with a structured summary including customer ID, root cause, and recommended action

#### 5.5 Exam concept

PostToolUse hooks provide deterministic guarantees that prompt instructions cannot. The hook enforces compliance (refunds > $500 are always blocked) while the structured error response (`errorCategory`, `isRetryable`) gives the agent the information it needs to recover appropriately. [Tasks 1.5, 2.2]

> **Also know for the exam:** PostToolUse hooks have a second use beyond compliance: **data normalization**. Tools from different MCP servers may return dates as Unix timestamps, ISO 8601, or locale strings. A normalization hook can convert all formats to a consistent one before the model processes them. This lab demonstrates the compliance pattern; the exam also tests the normalization pattern. [Task 1.5]

### Step 6 — Observe escalation criteria and few-shot examples

#### 6.1 Test

Type `4` to test a customer who says: "I've been going back and forth on this for days. I want to talk to a real person."

#### 6.2 The question

How does the agent decide when to escalate vs when to keep trying? A naive approach would be to escalate when the customer sounds frustrated — but sentiment is an unreliable proxy for case complexity. A frustrated customer with a simple order issue doesn't need a human; a calm customer asking about an uncovered policy edge case does.

#### 6.3 The answer

Open `system_prompt.txt` and read the escalation criteria and few-shot examples. The criteria are explicit: customer requests human, policy gaps, inability to make progress, suspected fraud. The few-shot examples show the model _what action to take_ for each scenario, including what NOT to do (e.g., Example 3 shows a frustrated customer who should NOT be escalated).

#### 6.4 What to observe

- The agent escalates immediately — it does not attempt further investigation first, because the customer explicitly requested a human
- The criteria drive the decision, not sentiment

Now try this query manually:

```
I bought a gift for my friend under my account CUST-1001, and they want to return it. Can they process the return themselves?
```

- This is a policy gap — gift returns with a different recipient are not covered by standard policy
- The agent should escalate with reason `policy_gap`, not attempt to process the refund

#### 6.5 Try a frustrated but resolvable case

Try this query manually:

```
This is ridiculous! I'm James Chen, CUST-1002. I ordered a keyboard weeks ago and I have no idea where it is. Order ORD-5504.
```

- ORD-5504 has status `shipped` — the agent can give a concrete update
- The agent should acknowledge the frustration but resolve the issue, **not** escalate
- Compare this to query `4` — that customer explicitly asked for a human; this one is just frustrated

#### 6.6 Exam concept

Explicit escalation criteria with few-shot examples in the system prompt. Sentiment-based escalation is an unreliable proxy for case complexity. Few-shot examples are the most effective technique for consistent output when instructions alone produce ambiguous behavior. [Tasks 5.2, 4.2]

> **Also know for the exam:** When a customer lookup (e.g., by name) returns **multiple matches**, the agent should ask for additional identifiers (email, phone) to disambiguate — not pick one heuristically. This lab's data has unique customers, but the exam tests the ambiguous-match scenario. [Task 5.2]

### Step 7 — Add persistent case_facts with Claude Code

#### 7.1 The problem

In a long support conversation, the context window fills up and older messages get summarized. Progressive summarization loses exact values — the $249.99 refund becomes "a refund," order ORD-5501 becomes "the customer's order." When the agent later needs to reference these facts, it hallucinates or gives vague answers.

Notice that `system_prompt.txt` already has the infrastructure for this — a `<case_facts>{case_facts}</case_facts>` XML section with a template variable. And `main.py` already formats the template with `system_template.format(case_facts=case_facts)` on every iteration. But right now `case_facts` is just the default string `"No facts collected yet."` — nothing ever updates it.

#### 7.2 The fix

Use Claude Code to add the extraction logic that populates `case_facts` after each tool call.

**Prompt for Claude Code:**

```
Add case_facts extraction logic to main.py. After each successful
(non-error) tool result, extract key transactional facts
(customer_id, customer_name, order_id, order_total, refund_amount,
refund_status) and update the case_facts variable so it contains a
formatted string of all collected facts. The system prompt template
and .format() call are already in place — just populate the variable.
Print the current case_facts after each update so the student can
see facts accumulating.
```

After Claude Code makes the changes, re-run with query `2` (Maria Santos refund).

#### 7.3 What to observe

- After `get_customer` returns, `case_facts` captures `customer_id` and `customer_name`
- After `lookup_order` returns, `case_facts` adds `order_id` and `order_total`
- The `<case_facts>` XML section in the system prompt updates on every iteration with the latest facts
- The agent's final response should reference exact amounts and IDs from `case_facts`

#### 7.4 Exam concept

Persistent fact extraction — amounts, dates, order numbers — into a structured block outside summarized history prevents loss during progressive summarization. Tool results accumulate tokens disproportionately to their relevance; `case_facts` extracts only the fields that matter. The system prompt uses an XML-tagged section with a template variable — no string manipulation. [Task 5.1]

> **Also know for the exam:** Two related context management concepts:
> - **"Lost in the middle" effect:** Models reliably process information at the beginning and end of long inputs but may miss findings buried in the middle. Place key findings at the beginning of aggregated inputs and use section headers to mitigate this. The `<case_facts>` block at the top of the system prompt is an example of this placement strategy.
> - **Trimming tool outputs:** In this lab, full tool results are appended to conversation history. In production, you would trim verbose tool outputs to only the relevant fields *before* appending — e.g., keeping only return-relevant fields from a 40-field order lookup. This reduces token accumulation without losing the information that matters.
>
> [Task 5.1]

### Step 8 — Explore tool design and distribution

Before finishing, review how the tools are designed in `tools.py`:

- Each tool has a clear, differentiated description — `get_customer` for identity lookup, `lookup_order` for order details, `process_refund` for refunds, `escalate_to_human` for escalation. No ambiguous overlap. [Task 2.1]
- The agent has exactly 4 tools — a focused set for its role. Giving an agent 18 tools degrades selection reliability. [Task 2.3]
- Error responses use `errorCategory` and `isRetryable` — the agent knows whether to retry or take a different action. [Task 2.2]
- Tool descriptions include input formats, boundaries, and when to use each tool versus alternatives. [Task 2.1]

**Exam concept:** Tool descriptions are the primary mechanism the model uses for tool selection. Descriptions must differentiate each tool's purpose, inputs, outputs, and when to use it versus alternatives. Too many tools degrades selection reliability. [Tasks 2.1, 2.3]

#### Additional exam concepts to review

**Single-agent vs multi-agent (Task 1.2):** This lab is a single agent with 4 tools. Lab 03 shows the multi-agent pattern — a coordinator spawning specialized subagents via the Task tool. Know the contrast: a single agent is simpler and appropriate when one role handles all tasks; a coordinator-subagent architecture is needed when subagents require isolated context, different tool sets, or parallel execution.

**System prompt keyword sensitivity (Task 2.1):** Tool descriptions are the primary selection mechanism, but system prompt wording can override them. If the system prompt says "always look up customer orders first," the model may bias toward `lookup_order` even when `get_customer` is the correct first step. Review system prompts for keyword-sensitive instructions that create unintended tool associations.

**Access failures vs valid empty results (Task 2.2):** This lab's tools return errors for not-found cases (`"errorCategory": "validation"`). The exam also tests the distinction between an *access failure* (timeout, service down — needs a retry decision) and a *valid empty result* (query succeeded, no matches — not an error). A search tool returning `{"results": []}` is a success; a search tool timing out is a failure. They require different recovery paths.

**`tool_choice` configuration (Task 2.3):** This lab uses the default `tool_choice: "auto"` — the model decides which tool to call. The exam also tests:
- `tool_choice: "any"` — guarantees the model calls *some* tool (useful when you need structured output, not conversational text)
- Forced selection `{"type": "tool", "name": "extract_metadata"}` — ensures a *specific* tool runs first (e.g., before enrichment steps)

Lab 06 exercises `tool_choice: "any"` for guaranteed structured extraction.

## Reset

To reset the lab and try again:

```bash
python reset.py
```

This restores all modified files (`main.py`) to their original starter state with TODOs. Your `.env` file is preserved — no need to re-enter your API key.

---

*v0.1 — 3/28/2026 — Alfredo De Regil*
