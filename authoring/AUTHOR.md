# Authoring Instructions

This file is for Claude Code during lab authoring sessions.
Read this before building or modifying any lab.

## Reference documents

All in this `authoring/` folder:

- `CCA_Lab_Plan.md` — the blueprint for all 6 labs: what to build, files, key concepts, what to observe
- `CCA_Lab_Reference.md` — full mapping of all 27 task statements to labs (both perspectives)
- `CCA_Exam_Guide.md` — source of truth for all terminology, task statements, knowledge and skills

Always use exam guide terminology verbatim. Never paraphrase concepts from the guide.

## Lab pedagogy

Labs are **guided walkthroughs**. The student does not write code from scratch. The progression is:

1. **See it work** — starter code runs out of the box and produces visible output.
2. **Complete it** — the student fills in `# TODO` sections guided by the README.
3. **Complement it** — later steps add features, often via Claude Code with a provided prompt.

Every README step tells the student exactly what to do, what to observe, and why it matters for the exam. No step should require guesswork.

### Copy-paste prompts
When a step asks the student to use Claude Code, the README **must** include the exact prompt to paste. Use this format:

```
> **Prompt for Claude Code:**
> `Add a validation check to process_refund that rejects amounts over $500 and returns a structured error with errorCategory "policy_violation" and isRetryable false.`
```

Never write "ask Claude Code to do X" without providing the literal prompt.

### Step-by-step detail
Every README starts from zero and walks through every action:

1. Create the lab folder
2. Create each file (by hand, scaffold script, or Claude Code prompt)
3. Configure (`.env`, `pip install`)
4. Run the starter code and observe output
5. Complete TODO sections, re-run, observe the difference
6. Complement with additional features in later steps

## Repo structure

```
claude-certified-architect/
  CLAUDE.md                        ← student-facing, do not modify unless asked
  authoring/                       ← authoring workspace, not for students
  01_customer_support_agent/       ← lab folders at root, for students
  02_code_generation_workflows/
  03_multi_agent_research/
  04_developer_productivity/
  05_ci_cd_integration/
  06_structured_extraction/
```

## How to build a lab

When asked to build Lab 0X:

1. **Read the lab plan** — read `authoring/CCA_Lab_Plan.md`, find the section for that lab. Note the scenario, domains, task statement IDs, files, and key concepts.
2. **Study the exam guide** — read `authoring/CCA_Exam_Guide.md`. For each task statement listed in the lab plan, read the full task statement text, its associated knowledge statements, and its skills statements. Extract:
   - The **exact terminology** the exam uses (e.g., `stop_reason`, `tool_use`, `end_turn`, `errorCategory`, `isRetryable`) — use these verbatim in code, comments, and README.
   - The **concepts the student must understand** — these drive what the lab demonstrates and what the README asks the student to observe.
   - The **skills the student must practice** — these drive what the lab asks the student to do (complete, complement, or configure).
3. **Cross-reference with the lab reference** — read `authoring/CCA_Lab_Reference.md` to confirm which task statements map to this lab and verify nothing is missed.
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

## Standard lab structure

Every lab must contain these files:

```
0X_lab_name/
  CLAUDE.md           # lab-specific instructions — loaded automatically by Claude Code
  README.md           # step-by-step lab guide, objectives, what to observe
  config.py           # constants: model name, thresholds, policy values
  main.py             # starter script — the thing the student runs
  reset.py            # deletes all lab-generated state, prints confirmation
  .env.example        # required env vars with placeholder values
  requirements.txt    # pip install -r requirements.txt
```

Additional files (e.g., `tools.py`, `agents.py`, `schema.py`, `sample_docs/`) as specified in the lab plan.

## Workspace convention

The student's experience must feel scoped to the lab folder:

- **VSCode:** open the **lab folder** (e.g., `01_customer_support_agent/`) as the workspace — not the repo root.
- **Claude Code:** launch from the **lab folder** terminal. This ensures Claude Code loads the lab's own `CLAUDE.md`.
- **Every lab has its own `CLAUDE.md`** with the coding conventions and any lab-specific instructions Claude Code needs. Do not rely on the repo-root `CLAUDE.md` — the student will never open the repo root as a workspace.

The student should never need to think about files outside their lab folder.

## config.py convention

Every lab has a `config.py` that centralizes **hardcoded constants** needed by the rest of the lab:
- **Model name** — e.g., `MODEL = "claude-sonnet-4-20250514"` — single place to change it
- **Thresholds and limits** — e.g., `MAX_REFUND_AMOUNT = 500`
- **Policy values** — e.g., `ESCALATION_REASONS = ["fraud", "policy_gap", "customer_request"]`

`config.py` is only for constants with hardcoded values. Not for logic, not for mock data generators, not for settings that change at runtime. Other modules import from it.

## Mock data convention

All lab data is **hardcoded mock data**. No databases, no external services, no network calls beyond the Anthropic API.

- **Format:** plain Python dicts, JSON files, or text files inside the lab folder. Never a database, CSV download, or external dependency.
- **Realistic:** use real-sounding names, plausible amounts, documents with actual missing fields. The scenario should feel genuine, not like `"test_user_1"`.
- **Deterministic:** the student sees the same behavior every time. When the README says "observe X," the data must reliably produce X.
- **Self-contained:** everything the lab needs lives in its folder. The student can revisit the finished lab months later without restoring infrastructure.
- **Focus:** the lab teaches exam concepts, not data management. Zero setup friction — clone, install, run.

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

### Step 1 — Create the starter files
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
> **Prompt for Claude Code:**
> `the exact prompt to paste`

## Reset
How to reset and try again.
```

## Coding conventions

Apply these to every Python file without exception.

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

**Additional conventions:**
- Functions over classes
- Comments only where they clarify an exam concept — not obvious code
- Always reference the exam guide task statement in comments where relevant (e.g., `# task 1.1 — agentic loop: check stop_reason`)
- `.env` for API keys — never hardcoded
- Keep scripts short and focused — educational over production-quality
- Simple folder structures — no over-engineering

## reset.py convention

Every `reset.py` must:
- Delete all files and state the lab creates at runtime
- Print a clear confirmation message for each thing deleted
- Exit cleanly if there is nothing to reset
- Be safe to run multiple times

## .env.example convention

Always include at minimum:
```
ANTHROPIC_API_KEY=your_api_key_here
```

Add any other required env vars with placeholder values and a comment explaining each.

## Starter scripts

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

---

*v0.1 — 3/15/2026 — Alfredo de Regil*
