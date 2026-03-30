# Gap Analysis — Lab 05: CI/CD Integration

**Date:** 2026-03-30
**Tasks covered:** 1.6, 3.4, 3.5, 3.6, 4.1, 4.2, 4.6
**Domains:** D3 (Claude Code Configuration & Workflows), D4 (Prompt Engineering & Structured Output)
**Lab status:** Not yet built — analysis covers Layer 1 (Exam Guide vs Reference) and Layer 2 (Reference vs Plan) only.

---

## Layer 1 — Lab Reference Gaps (Exam Guide → Reference)

Does the lab reference fully capture the exam guide's knowledge and skills for each L5 task?

---

### Task 1.6 — Design task decomposition strategies

| Item | Status |
|------|--------|
| Fixed sequential pipelines vs dynamic adaptive decomposition | ✅ |
| Prompt chaining for predictable multi-aspect reviews (per-file then cross-file) | ✅ |
| Adaptive investigation plans generating subtasks based on discoveries | ✅ |
| Split code reviews into per-file local + cross-file integration pass | ✅ |
| Decompose open-ended tasks: map structure, identify high-impact, adaptive plan | ✅ |

**No gaps.** All exam guide knowledge and skills are captured in the reference.

---

### Task 3.4 — Determine when to use plan mode vs direct execution

| Item | Status |
|------|--------|
| Plan mode for large-scale changes, architectural decisions, multi-file edits | ✅ |
| Direct execution for simple, well-scoped single-file changes | ✅ |
| Plan mode enables safe exploration before committing | ✅ |
| Explore subagent for isolating verbose discovery | ✅ |
| Select plan mode for architectural tasks (microservice restructuring, 45+ files) | ✅ |
| Select direct execution for clear-scope changes (single-file bug fix) | ✅ |
| Explore subagent for verbose discovery to prevent context exhaustion | ✅ |
| **Combining plan mode for investigation with direct execution for implementation** | ⚠️ |

**1 gap.** Exam guide explicitly lists a skill: "Combining plan mode for investigation with direct execution for implementation (e.g., planning a library migration, then executing the planned approach)." The reference covers plan and direct as separate choices but not the combined pattern of using plan mode for discovery then switching to direct execution.

> **Fix:** Add to reference 3.4 skills: "Combine plan mode for investigation with direct execution for implementation — use plan to explore and design, then switch to direct for execution"

---

### Task 3.5 — Apply iterative refinement techniques

| Item | Status |
|------|--------|
| Concrete input/output examples as most effective technique | ✅ |
| Test-driven iteration: write tests first, share failures | ✅ |
| Interview pattern: have Claude ask questions before implementing | ✅ |
| Interacting issues in single message vs sequential for independent | ✅ |
| Provide 2-3 examples when prose produces inconsistent results | ✅ |
| Write test suites before implementation, iterate by sharing failures | ✅ |
| **Specific test cases with example input/expected output for edge cases** | ⚠️ |
| **Interview pattern for surfacing considerations in unfamiliar domains** | ⚠️ |

**2 minor gaps.** The exam guide calls out "providing specific test cases with example input and expected output to fix edge case handling (e.g., null values in migration scripts)" as a distinct skill — the reference rolls this into the general examples skill. Similarly, the exam guide specifies the interview pattern is for "unfamiliar domains" — the reference mentions the pattern but loses the domain-scoping context.

> **Fix:** These are minor wording gaps. Add "with example input and expected output" to the test case skill, and add "in unfamiliar domains" qualifier to the interview pattern skill.

---

### Task 3.6 — Integrate Claude Code into CI/CD pipelines

| Item | Status |
|------|--------|
| `-p` / `--print` flag for non-interactive mode | ✅ |
| `--output-format json` and `--json-schema` CLI flags | ✅ |
| CLAUDE.md provides project context to CI-invoked Claude | ✅ |
| Session context isolation: independent instance vs self-review | ✅ |
| Run with -p flag to prevent interactive hangs | ✅ |
| `--output-format json` + `--json-schema` for machine-parseable PR comments | ✅ |
| Include prior review findings on re-runs — only new/unaddressed issues | ✅ |
| Document testing standards and fixtures in CLAUDE.md | ✅ |
| **Provide existing test files in context to avoid suggesting duplicate test scenarios** | ❌ |

**1 gap.** The exam guide has an explicit skill: "Providing existing test files in context so test generation avoids suggesting duplicate scenarios already covered by the test suite." This is entirely absent from the reference.

> **Fix:** Add to reference 3.6 skills: "Provide existing test files in context when generating tests so Claude avoids suggesting scenarios already covered by the suite"

---

### Task 4.1 — Design prompts with explicit criteria to reduce false positives

| Item | Status |
|------|--------|
| Explicit criteria outperform vague instructions | ✅ |
| "Be conservative" fails to improve precision vs specific categorical criteria | ✅ |
| High false positive rates undermine developer trust | ✅ |
| Write criteria defining what to report vs skip | ✅ |
| Temporarily disable high false-positive categories to restore trust | ✅ |
| Define explicit severity criteria with concrete code examples per level | ✅ |

**No gaps.**

---

### Task 4.2 — Apply few-shot prompting to improve output consistency

| Item | Status |
|------|--------|
| Few-shot examples most effective for consistent, actionable output | ✅ |
| Demonstrate ambiguous-case handling and enable generalization | ✅ |
| Reduce hallucination in extraction tasks | ✅ |
| Create 2-4 targeted examples showing reasoning for chosen action | ✅ |
| Include examples with desired output format (location, issue, severity, fix) | ✅ |
| Examples for varied document structures (extraction context, L6) | ✅ |
| **Examples distinguishing acceptable code patterns from genuine issues** | ❌ |

**1 gap.** Exam guide skill: "Providing few-shot examples distinguishing acceptable code patterns from genuine issues to reduce false positives while enabling generalization." This directly ties 4.2 (few-shot) to 4.1 (false positive reduction) in the code review context — the exact use case of Lab 05. Missing from reference.

> **Fix:** Add to reference 4.2 skills: "Provide few-shot examples that distinguish acceptable code patterns from genuine issues to reduce false positives while enabling generalization to novel patterns"

---

### Task 4.6 — Design multi-instance and multi-pass review architectures

| Item | Status |
|------|--------|
| Self-review limitation: retains reasoning context | ✅ |
| Independent review instances more effective than self-review | ✅ |
| Multi-pass: per-file local + cross-file integration avoids attention dilution | ✅ |
| Use second independent instance without generator's context | ✅ |
| Split reviews into per-file + cross-file integration passes | ✅ |
| Verification passes with confidence self-reporting for calibrated routing | ✅ |

**No gaps.**

---

### Layer 1 Summary

| Severity | Count | Tasks |
|----------|-------|-------|
| ❌ Missing | 2 | 3.6 (test file context), 4.2 (acceptable vs genuine pattern examples) |
| ⚠️ Partial | 3 | 3.4 (combined plan+direct pattern), 3.5 (edge case test specificity, domain scoping) |
| ✅ Complete | 2 | 1.6, 4.1, 4.6 |

---

## Layer 2 — Lab Plan Gaps (Reference → Plan)

Does the Lab 05 plan fully deliver on the reference's knowledge and skills?

---

### Task 1.6 — Design task decomposition strategies

| Plan element | Status |
|-------------|--------|
| Per-file + cross-file integration pass in key concepts | ✅ |
| Observation #4: compare single-pass vs per-file + integration pass | ✅ |
| Fixed sequential pipeline embodied in pipeline.py design | ✅ |

**Covered.** The prompt chaining pattern is the natural fit for CI code review. Adaptive decomposition is L3's responsibility.

---

### Task 3.4 — Determine when to use plan mode vs direct execution

| Plan element | Status |
|-------------|--------|
| Any exercise or observation about plan mode vs direct execution | ❌ |
| Any mention of when CI should or should not use plan mode | ❌ |
| Explore subagent usage for verbose discovery | ❌ |

**Major gap.** Task 3.4 is listed as covered by L5 but has zero presence in the plan. No key concept, no observation, no exercise.

In a CI context, 3.4 applies in two ways:
1. CI pipelines use direct execution (`-p` flag) by default — the plan should explain *why* (non-interactive, no plan mode approval step).
2. When a developer investigates complex CI findings, they might switch to plan mode for multi-file exploration before fixing.

> **Fix options:**
> - **Minimum:** Add a callout/note in the README explaining that CI uses direct execution because `-p` is non-interactive, and reference plan mode as what developers use when investigating complex review findings.
> - **Better:** Add a step where the student runs a complex review finding through Claude Code in plan mode (interactively) to investigate it, contrasting the CI experience (direct, automated) with the developer experience (plan mode, exploratory).

---

### Task 3.5 — Apply iterative refinement techniques

| Plan element | Status |
|-------------|--------|
| Observation #3: vague criteria → explicit criteria (implicit iteration) | ⚠️ |
| Few-shot examples in system prompt | ⚠️ |
| Explicit iterative loop: run → assess → refine prompt → re-run | ❌ |
| Test-driven iteration or interview pattern exercise | ❌ |

**Partially covered.** The comparison exercises (vague vs explicit, single-pass vs multi-pass) *are* iterative refinement in practice — the student sees poor output, improves the prompt, sees better output. But the plan doesn't structure this as an explicit refinement loop or label it as 3.5.

> **Fix:** Structure one step as an explicit 3-iteration refinement loop:
> 1. Run review with vague criteria ("be conservative") → observe false positives
> 2. Replace with explicit categorical criteria → observe improvement
> 3. Add 2-3 few-shot examples of acceptable-vs-genuine patterns → observe further improvement
>
> This converts the existing comparison observations into a progressive refinement exercise that directly maps to 3.5.

---

### Task 3.6 — Integrate Claude Code into CI/CD pipelines (core task)

| Plan element | Status |
|-------------|--------|
| `-p` flag for non-interactive mode | ✅ |
| `--output-format json` + `--json-schema` | ✅ |
| CLAUDE.md with testing standards, review criteria, fixtures | ✅ |
| Session context isolation (independent review instance) | ✅ |
| Observation #1: verify no hang (non-interactive works) | ✅ |
| Observation #2: verify JSON matches schema | ✅ |
| Observation #5: second run only reports new issues | ✅ |
| How JSON output maps to PR comment workflow | ⚠️ |
| **Existing test files in context for test generation** | ❌ |

**1 missing skill, 1 partial.** The plan covers the core 3.6 mechanics well. Two gaps:

1. The plan says "produces structured JSON review output" but never shows how this feeds into a PR comment workflow. Even a simulated example (parse JSON → format as PR comment text) would close this.
2. The exam guide skill about providing existing test files so test generation avoids duplicates is absent from the plan entirely.

> **Fix:**
> - Add a step or observation showing the JSON output formatted as a PR comment (even if simulated — no actual GitHub integration needed).
> - Add a step where the student adds an existing test file to the CLAUDE.md context and observes that generated test suggestions no longer duplicate existing coverage.

---

### Task 4.1 — Design prompts with explicit criteria

| Plan element | Status |
|-------------|--------|
| Key concept: explicit criteria, define what to report vs skip | ✅ |
| Observation #3: vague vs explicit criteria comparison | ✅ |
| Temporarily disabling high false-positive categories | ❌ |
| Explicit severity criteria with concrete code examples per level | ⚠️ |

**1 missing, 1 partial.** The comparison exercise covers the core concept well. But two reference skills are absent:

1. No step where the student disables a high false-positive category and observes trust improvement.
2. The plan mentions "explicit review criteria" but doesn't specify that the criteria include severity levels with concrete code examples.

> **Fix:**
> - Add severity levels (e.g., "critical", "warning", "info") to the review schema with concrete example for each level.
> - Add a step where one review category (e.g., naming conventions) produces mostly false positives, so the student disables it and observes the remaining output is higher quality.

---

### Task 4.2 — Apply few-shot prompting

| Plan element | Status |
|-------------|--------|
| Key concept: few-shot examples in system prompt | ✅ |
| Structure of few-shot examples (location, issue, severity, fix) | ⚠️ |
| Student creates or modifies few-shot examples hands-on | ❌ |
| Examples distinguishing acceptable patterns from genuine issues | ❌ |

**2 missing, 1 partial.** The plan mentions few-shot examples as a key concept but treats them as pre-existing in the system prompt. The student never creates, modifies, or experiments with few-shot examples.

> **Fix:**
> - Make few-shot creation a student exercise: provide the system prompt without examples, have the student run the review, then add 2-3 few-shot examples and re-run.
> - Specify the few-shot format: `{file, line, issue, severity, suggested_fix, reasoning}`.
> - Include at least one example showing an acceptable pattern (e.g., a deliberate `# type: ignore` comment) that should NOT be flagged.

---

### Task 4.6 — Multi-instance and multi-pass review

| Plan element | Status |
|-------------|--------|
| Independent review instance vs self-review | ✅ |
| Per-file + cross-file integration pass | ✅ |
| Observation #4: single-pass vs per-file + integration comparison | ✅ |
| **Verification pass with confidence self-reporting per finding** | ❌ |

**1 missing.** The plan covers two of three reference skills well. The verification pass — where the model self-reports confidence alongside each finding for calibrated review routing — is absent.

> **Fix:** Add a step where the review prompt asks Claude to include a confidence score (high/medium/low) per finding. The student then filters findings by confidence, observing that low-confidence findings have higher false positive rates — connecting to the review routing concept.

---

### Additional Plan Observations

**D4.5 reference:** The plan's key concepts include "Sync API for blocking pre-merge vs batch API for overnight jobs (D4.5 awareness)." Task 4.5 belongs to L6, not L5. This is fine as contextual awareness but should be explicitly marked as a NOTE or callout, not an exercise.

**Observation-heavy structure:** The plan lists 5 "What to observe" items but few explicit "do this" steps. The lab builder will need clear guidance to convert these observations into active student exercises with specific instructions.

**`pr_files/` design:** The three sample files (auth.py, orders.py, utils.py) need to contain deliberate issues at varying severity levels, plus at least one "acceptable pattern" that a vague prompt would incorrectly flag. This is critical for the false positive comparison to work.

---

## Layer 2 Summary

| Severity | Count | Details |
|----------|-------|---------|
| ❌ Missing | 6 | 3.4 (no plan mode exercise), 3.5 (no explicit iteration loop), 3.6 (test file context), 4.1 (disable FP category), 4.2 (student creates examples, acceptable-vs-genuine), 4.6 (confidence self-reporting) |
| ⚠️ Partial | 4 | 3.5 (implicit iteration via comparison), 3.6 (JSON→PR comment mapping), 4.1 (severity levels with examples), 4.2 (few-shot format structure) |
| ✅ Complete | 3 | 1.6, 3.6 core mechanics, 4.6 core mechanics |

---

## Recommended Plan Improvements (Priority Order)

> These recommendations were written before the lab was built. See Layer 3
> below for what was actually delivered and which of these were addressed.

### High — Missing task coverage

1. **Add explicit iterative refinement loop (3.5):** Restructure the vague→explicit→few-shot comparison as a 3-step progressive refinement exercise. This is the easiest fix because the plan already has the comparisons — they just need to be sequenced as an iteration loop. **→ Addressed in actual lab (Steps 3→4→5).**

2. **Add student-created few-shot examples (4.2):** The student should build the few-shot examples, not just use pre-existing ones. Include the acceptable-vs-genuine pattern distinction. **→ Addressed: Step 5 has student add examples, including an acceptable-pattern example. Student copies from README rather than authoring from scratch, but this is consistent with lab pedagogy.**

3. **Add confidence self-reporting step (4.6):** Have the review prompt include per-finding confidence scores. Student filters by confidence to see false positive correlation. **→ Addressed: Schema includes confidence field; Step 7.1 and 7.4 cover filtering.**

4. **Add plan mode vs direct execution callout (3.4):** At minimum, a README note explaining why CI uses direct execution. Better: a step where the student uses plan mode interactively to investigate a complex finding. **→ Addressed: Step 8.3-8.4 has interactive plan mode exercise with copy-paste prompt and "when to use which" table.**

### Medium — Missing skills within covered tasks

5. **Add test file context for test generation (3.6):** A step showing CLAUDE.md with existing test references prevents duplicate suggestions. **→ Addressed: Step 8.1.**

6. **Add severity levels with code examples to review criteria (4.1):** The review_schema.json should define severity levels; the criteria prompt should include concrete code examples per level. **→ Addressed: Schema has severity enum; Step 4.3 prompt defines critical/warning/info with concrete descriptions.**

7. **Add disable-high-FP-category step (4.1):** Student disables a noisy category and observes output quality improvement. **→ Partially addressed: The transition from Step 3 (broad categories including style/naming) to Step 4 (only bugs/security) effectively disables high-FP categories. Framed as prompt replacement rather than category disabling, but the effect is the same. Callout in Step 4.4 notes the exam concept.**

### Low — Wording and framing

8. **Mark D4.5 sync-vs-batch as awareness only:** Add a NOTE callout — this is L6's exercise, not L5's. **→ Addressed: Step 8.5 has explicit callout marking batch API as "covered in Lab 06."**

9. **Specify few-shot example format:** The plan should name the fields: file, line, issue, severity, suggested_fix, reasoning. **→ Addressed: Step 5.3 examples include all fields.**

10. **Add JSON→PR comment mapping step (3.6):** Even a simulated formatter showing how structured JSON becomes inline comments. **→ Addressed: Menu option 4 (`format_as_pr_comments`) formats JSON as simulated PR inline comments.**

---

## Layer 3 — Actual Lab Gaps (README + Code vs Plan + Reference)

Does the built lab fully deliver on the updated plan and reference?

---

### Task 1.6 — Design task decomposition strategies

| Deliverable | Status |
|------------|--------|
| Per-file + cross-file integration pass (Step 6) | ✅ |
| Student implements `run_multi_pass()` with per-file loop + integration pass | ✅ |
| Integration prompt (`prompts/integration_prompt.txt`) asks for cross-file issues only | ✅ |
| Exam callout: prompt chaining vs adaptive decomposition (Step 6.5) | ✅ |

**Well-covered.** Step 6 is a complete implementation exercise. The integration prompt template is well-designed — receives per-file findings and all source code, asks for cross-file issues only.

---

### Task 3.4 — Plan mode vs direct execution

| Deliverable | Status |
|------------|--------|
| Step 8.3: Interactive plan mode exercise with copy-paste prompt | ✅ |
| Step 8.4: "When to use which" table (direct for CI, plan for investigation, combine) | ✅ |
| Step 8.5: Exam concept connecting plan mode to Explore subagent from Lab 04 | ✅ |

**Well-covered.** The contrast between `-p` (every prior step) and plan mode (Step 8.3) is clear.

---

### Task 3.5 — Iterative refinement

| Deliverable | Status |
|------------|--------|
| Three-step progression: vague (Step 3) → explicit (Step 4) → few-shot (Step 5) | ✅ |
| Each step labels itself as part of the refinement loop in exam concept | ✅ |
| "Also know for the exam" callout covers test-driven iteration, interview pattern (Step 5.5) | ✅ |

**Well-covered.** The iterative structure is the backbone of the lab — the student experiences progressive improvement firsthand.

---

### Task 3.6 — CI/CD integration

| Deliverable | Status |
|------------|--------|
| `-p` flag for non-interactive mode | ✅ |
| `--output-format json` for structured output | ✅ |
| `--json-schema` disclosure as planned CLI feature (Step 3.2) | ✅ |
| CLAUDE.md with project context (testing standards, review criteria) | ✅ |
| Test file context in CLAUDE.md to prevent duplicate test suggestions (Step 8.1) | ✅ |
| Test generation exercise with copy-paste prompt (Step 8.1) | ✅ |
| Simulated PR inline comment formatting (menu option 4) | ✅ |
| **Prior review findings injected into prompt for re-run deduplication** | ❌ |

**Addressed via callout.** Prior findings are not injected into the prompt — the pipeline compares output files after-the-fact via `compare_reviews()`. However, the exam concept is explicitly taught in Step 8.5: "On re-runs after new commits, instruct Claude to report only new or unaddressed issues." The skill is taught as an awareness note, not implemented hands-on. Acceptable given the lab's length (8 steps, 25-35 min estimate).

---

### Task 4.1 — Explicit criteria to reduce false positives

| Deliverable | Status |
|------------|--------|
| Step 4: Replace vague prompt with explicit categorical criteria | ✅ |
| Severity levels (critical/warning/info) with concrete definitions | ✅ |
| "Do NOT report" list (naming, docstrings, style, acceptable patterns) | ✅ |
| Category disabling: transition from 6 broad categories to 2 focused (Step 3→4) | ✅ |
| Callout about disabling high-FP categories (Step 4.4) | ✅ |

**Well-covered.** The prompt in Step 4.3 is a strong example of explicit criteria. The "Do NOT report" section with "returning None for not-found cases is a deliberate API design choice" is a concrete example of acceptable-pattern documentation.

---

### Task 4.2 — Few-shot prompting

| Deliverable | Status |
|------------|--------|
| Three few-shot examples with full format (file, line, issue, severity, ...) | ✅ |
| Example 2: acceptable pattern (DO NOT REPORT) — returning None | ✅ |
| Student adds examples to prompt (Step 5.3) | ✅ |
| Observations about generalization and consistent formatting (Step 5.4) | ✅ |
| Exam concept about distinguishing acceptable patterns (Step 5.5) | ✅ |

**Well-covered.** The three examples cover genuine bug, acceptable pattern, and security issue — good range. Example 2 directly addresses the "distinguishing acceptable code patterns from genuine issues" skill.

---

### Task 4.6 — Multi-instance and multi-pass review

| Deliverable | Status |
|------------|--------|
| Independent review: two `claude -p` calls compared (Step 7) | ✅ |
| Comparison by file:line location showing agreement and unique findings | ✅ |
| Confidence field in schema (high/medium/low) | ✅ |
| Confidence filtering observation (Step 7.1, 7.4) | ✅ |
| Exam concept about confidence-based routing (Step 7.5) | ✅ |

**Well-covered.**

---

### PR Files Design Quality

| Quality aspect | Status |
|---------------|--------|
| `utils.py`: `calculate_percentage` — division by zero bug (critical) | ✅ |
| `utils.py`: `sanitize_input` — only strips `<>`, weak sanitization (security) | ✅ |
| `utils.py`: `parse_json_safe` returns None — acceptable pattern, not error swallowing | ✅ |
| `orders.py`: `search_orders` constructs SQL-like injection string (security) | ✅ |
| `orders.py`: `get_order` checks role but not resource ownership (auth gap) | ✅ |
| `test_utils.py`: covers validate_email, format_currency, truncate_string — leaves room for test generation | ✅ |
| Mix of severities: critical bugs, security issues, acceptable patterns | ✅ |

**Well-designed.** The PR files contain deliberate issues at varying severity levels, plus acceptable patterns that a vague prompt would incorrectly flag. Good for demonstrating the false positive reduction across Steps 3→4→5.

---

### README Accuracy

| Claim | Status |
|-------|--------|
| **Step 6.4:** "The integration pass should find that `orders.py` never calls `check_permission()` from `auth.py`" | ❌ **Wrong** |
| **Step 8.3 prompt:** "get_order function has no authorization check even though auth.py provides check_permission" | ❌ **Wrong** |

**2 factual errors.** Every order function except `calculate_discount` calls `check_permission`. The code at `orders.py:42-44` shows `get_order` does call `check_permission(token, "user")`.

The actual cross-file issue is **ownership authorization**, not missing authorization:
- `get_order` checks the user's role but not whether the user owns the order — any authenticated "user" can access any order
- `search_orders` constructs a SQL-injection-vulnerable string without using `sanitize_input` from `utils.py`
- `calculate_discount` has no auth check at all (though it may not need one)

> **Fix Step 6.4:** Change to: "The integration pass should find that `orders.py` `get_order` checks role via `check_permission` but does not verify the requesting user owns the order — any authenticated user can access any order. It should also find that `search_orders` does not use `sanitize_input()` from `utils.py` when building its query string."
>
> **Fix Step 8.3 prompt:** Change to: "The code review flagged that orders.py get_order function checks role-based authorization but not resource ownership — any authenticated user can retrieve any order. Investigate: where should the ownership check go, what would it look like, and what other functions in orders.py have the same gap?"

---

### Convention Compliance

| Convention | Status |
|-----------|--------|
| File headers (`# filename.py - Short description`) | ✅ |
| No inline returns — variables assigned before return | ✅ |
| No function calls as arguments | ✅ |
| Functions over classes | ✅ |
| ANSI colors from config.py | ✅ |
| Rich spinner for wait states (`console.status`) | ✅ |
| `_starter/` with `build_reset.py` for reset.zip | ✅ |
| `reset.py` preserves `.env` | ✅ |
| `.env.example` present | ✅ |
| Interactive menu with ANSI colors | ✅ |
| Exam concept callouts with `[Task X.Y]` tags | ✅ |
| Copy-paste prompts for Claude Code steps | ✅ |

**Fully compliant.** The lab follows all established conventions. Nice touch using `rich.console.Console.status()` for the spinner during Claude Code calls.

---

### Structural Observations

**Strengths:**
- The test/problem/fix/observe pattern in Steps 4-7 is pedagogically strong — student sees the problem before the fix
- The iterative arc (Steps 3→4→5) is the best demonstration of progressive refinement across all labs
- Pipeline saves reviews to `output/` with timestamps, enabling comparison across runs
- Two TODO exercises (Steps 6, 7) with clear guidance comments in the starter code
- Integration prompt template is a good design — receives prior findings and asks for cross-file issues only

**Pipeline note:** `pipeline.py` passes the entire prompt as a command-line argument to `claude -p` (line 100-103). For large PR files, this could hit shell argument length limits. A more robust approach would pipe the prompt via stdin. This is not a gap analysis finding but something to test during the timing pass.

---

## Layer 3 Summary

| Severity | Count | Details |
|----------|-------|---------|
| ⚠️ Callout only | 1 | 3.6 (prior-findings deduplication taught in exam callout, not hands-on — acceptable) |
| ✅ Fixed | 2 | README Step 6.4 and Step 8.3 — code updated to match claims (auth removed from orders.py) |
| ⚠️ Note | 1 | Pipeline passes prompt as CLI argument — may hit shell limits with large files |
| ✅ Complete | 6 | 1.6, 3.4, 3.5, 4.1, 4.2, 4.6 |

---

## Overall Assessment

The lab builder addressed **all 10 recommended improvements** from the pre-build analysis. The lab is well-structured, follows all conventions, and covers 6 of 7 tasks completely.

**Post-review fixes applied:**

1. **README Step 6.4 + 8.3** — ✅ Fixed. Lab builder removed auth checks from `orders.py` so the README claims are now accurate (orders.py genuinely never calls `check_permission`).
2. **Prior-findings deduplication (Task 3.6)** — ✅ Accepted as callout-only. Step 8.5 teaches the concept; hands-on implementation deferred to keep lab within time budget.

---

*Layer 1-2 analysis: 2026-03-30 (pre-build) | Layer 3 analysis: 2026-03-30 (post-build)*
