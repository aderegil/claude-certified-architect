# Gap Analysis — Lab 06: Structured Data Extraction

**Mode:** PRE-BUILD (lab not yet built — Layers 1 and 2 only)
**Date:** 2026-03-30
**Tasks covered:** 4.2, 4.3, 4.4, 4.5, 5.5

---

## Layer 1 — Exam Guide → Lab Reference

Does CCA_Lab_Reference.md fully map the exam guide knowledge and skills for each task this lab covers?

All items resolved. 7 gaps were found and fixed in the reference before build.

---

### Task 4.2 — Apply few-shot prompting to improve output consistency and quality

**Knowledge:**
- ✅ K1: Few-shot as most effective technique when instructions alone produce inconsistent results
- ✅ K2: Few-shot for demonstrating ambiguous-case handling
- ✅ K3: Few-shot enables generalization to novel patterns
- ✅ K4: Effectiveness for reducing hallucination in extraction tasks

**Skills:**
- ✅ S1: Create 2-4 targeted few-shot examples for ambiguous scenarios with reasoning
- ✅ S2: Few-shot for desired output format (location, issue, severity, fix)
- ✅ S3: Few-shot distinguishing acceptable patterns from genuine issues
- ✅ S4: Few-shot for varied document structures (inline citations vs bibliographies, methodology sections vs embedded details) — *added "methodology sections vs embedded details"*
- ✅ S5: Few-shot to address empty/null extraction of required fields — *added*

---

### Task 4.3 — Enforce structured output using tool use and JSON schemas

**Knowledge:**
- ✅ K1: tool_use with JSON schema = most reliable for schema-compliant output
- ✅ K2: tool_choice "auto" / "any" / forced distinction
- ✅ K3: Strict schemas eliminate syntax errors but not semantic errors
- ✅ K4: Schema design: required vs optional, enum "other" + detail string

**Skills:**
- ✅ S1: Define extraction tools with JSON schemas and extract from tool_use response
- ✅ S2: Set tool_choice "any" for unknown doc type
- ✅ S3: Force specific tool for ordering (extract_metadata before enrichment)
- ✅ S4: Nullable fields to prevent fabrication
- ✅ S5: Enum "unclear" for ambiguous cases + "other" + detail for extensibility — *added "unclear"*
- ✅ S6: Format normalization rules in prompts alongside strict output schemas — *added*

---

### Task 4.4 — Implement validation, retry, and feedback loops for extraction quality

**Knowledge:**
- ✅ K1: Retry-with-error-feedback: append specific validation errors to prompt
- ✅ K2: Retry ineffective when required info is absent from source
- ✅ K3: `detected_pattern` field for tracking which constructs trigger findings — *added*
- ✅ K4: Semantic validation errors vs schema syntax errors distinction

**Skills:**
- ✅ S1: Implement follow-up with original doc + failed extraction + specific errors
- ✅ S2: Identify retryable (format mismatch) vs non-retryable (info absent)
- ✅ S3: `detected_pattern` fields in structured findings for dismissal pattern analysis — *added*
- ✅ S4: Self-correction flows: calculated_total vs stated_total, conflict_detected boolean

---

### Task 4.5 — Design efficient batch processing strategies

**Knowledge:**
- ✅ K1: Message Batches API: 50% savings, 24h window, no latency SLA
- ✅ K2: Batch for non-blocking; inappropriate for blocking (pre-merge)
- ✅ K3: No multi-turn tool calling in batch
- ✅ K4: custom_id for correlation

**Skills:**
- ✅ S1: Match API to latency: sync for blocking, batch for overnight
- ✅ S2: Calculate batch frequency from SLA constraints (4h windows, 30h SLA)
- ✅ S3: Resubmit failed by custom_id with modifications (chunking oversized docs)
- ✅ S4: Prompt refinement on sample set before batch-processing large volumes — *added*

---

### Task 5.5 — Design human review workflows and confidence calibration

**Knowledge:**
- ✅ K1: Aggregate accuracy (97%) masks poor performance on specific types/fields
- ✅ K2: Stratified random sampling for error rates and novel pattern detection
- ✅ K3: Field-level confidence calibrated using labeled validation sets
- ✅ K4: Validate by document type and field before automating

**Skills:**
- ✅ S1: Stratified random sampling for ongoing error rate measurement
- ✅ S2: Analyze accuracy by doc type and field before reducing human review
- ✅ S3: Field-level confidence scores, calibrate thresholds with labeled validation sets
- ✅ S4: Route low-confidence and ambiguous/contradictory sources to human review

---

### Layer 1 Summary

7 gaps found, all resolved:

| Status | Task | Type | Item | Fix |
|--------|------|------|------|-----|
| ✅ | 4.2 | Skill | Varied structures incomplete | Added "methodology sections vs embedded details" |
| ✅ | 4.2 | Skill | Few-shot for null extraction missing | Added skill |
| ✅ | 4.3 | Skill | "unclear" enum missing | Added alongside "other" |
| ✅ | 4.3 | Skill | Format normalization rules missing | Added skill |
| ✅ | 4.4 | Knowledge | `detected_pattern` field missing | Added knowledge item |
| ✅ | 4.4 | Skill | `detected_pattern` for dismissal analysis missing | Added skill |
| ✅ | 4.5 | Skill | Prompt refinement on sample missing | Added skill |

---

## Layer 2 — Lab Reference → Lab Plan

Does CCA_Lab_Plan.md Lab 06 section fully reflect the reference? Does every listed task have a visible exercise or callout?

All items resolved. 18 gaps were found and fixed in the plan before build.

---

### Task 4.2 — Few-shot prompting

- ✅ Few-shot key concepts for extraction context — *was entirely absent; added 2 concepts with [Task 4.2] tags*

---

### Task 4.3 — Structured output via tool use

- ✅ tool_use with JSON schema as most reliable approach
- ✅ tool_choice "any" for unknown doc type
- ✅ Nullable fields to prevent hallucination
- ✅ Enum "other" + detail string
- ✅ Forced tool_choice for ordering — *added*
- ✅ "unclear" enum for ambiguous cases — *added*
- ✅ Format normalization rules — *added*
- ✅ Semantic vs syntax error distinction — *added as part of tool_use concept*

---

### Task 4.4 — Validation, retry, feedback loops

- ✅ Retry-with-error-feedback
- ✅ Distinguish retryable vs non-retryable
- ✅ `detected_pattern` field — *added*
- ✅ Self-correction flows (calculated_total, conflict_detected) — *added*

---

### Task 4.5 — Batch processing

- ✅ Message Batches API with custom_id
- ✅ Failure resubmission
- ✅ Sync vs batch latency matching — *added as explicit concept*
- ✅ SLA calculation — *added*
- ✅ Prompt refinement on sample set — *added*
- ✅ Chunking oversized docs on resubmission — *added*

---

### Task 5.5 — Human review & confidence

- ✅ Field-level confidence scores
- ✅ Stratified sampling for human review routing
- ✅ Calibrated using labeled validation sets — *made explicit*
- ✅ Validate by document type and field before automating — *made explicit*

---

### Structural items

| Status | Item | Fix |
|--------|------|-----|
| ✅ | Narrative arc | Added 7-step arc (invoice extraction for accounts payable) |
| ✅ | `[Task X.Y]` tags | Added to all 18 key concepts |
| ✅ | File tree | Added `config.py`, `CLAUDE.md`, `.gitignore`, `prompts/`, `_starter/` |
| ✅ | Reference build line | Expanded with few-shot, detected_pattern, self-correction, format normalization |
| ✅ | "What to observe" | Expanded from 5 to 10 items with task tags |

---

## Layer 3 — Actual Lab Gaps

Does the README and code fully deliver on the plan and reference? Claims verified against actual code.

**Date:** 2026-03-31

---

### File tree verification

| Planned | Actual | Status |
|---------|--------|--------|
| `.gitignore` | ✅ Present | ⚠️ Has `venv/` but not `.venv/` — lab creates `.venv` |
| `CLAUDE.md` | ✅ Present | ✅ |
| `README.md` | ✅ Present | ✅ |
| `config.py` | ✅ Present | ⚠️ `HIGH_CONFIDENCE_THRESHOLD` and `LOW_CONFIDENCE_THRESHOLD` defined but never used |
| `main.py` | ✅ Present | ✅ |
| `batch.py` | ✅ Present | ✅ |
| `schema.py` | ✅ Present | ✅ |
| `data.py` | ✅ Present | ✅ Also includes `LABELED_VALIDATIONS` (not in plan file description) |
| `prompts/extraction_prompt.txt` | ✅ Present | ✅ |
| `invoices/` (10 files) | ❌ Only 7 | Plan says `invoice_01.txt ... invoice_10.txt`; lab has 01–07 |
| `_starter/build_reset.py` | ✅ Present | ✅ |
| `_starter/main.py` | ✅ Present | ✅ |
| `_starter/schema.py` | ✅ Present | ✅ |
| `reset.py` | ✅ Present | ✅ Preserves `.env` |
| `reset.zip` | ✅ Present | ✅ Contains main.py and schema.py |
| `.env.example` | ✅ Present | ✅ |
| `requirements.txt` | ✅ Present | ✅ |

---

### Convention compliance

| Convention | Status | Notes |
|-----------|--------|-------|
| File headers | ✅ | All 7 Python files have `# filename.py - description` |
| No inline return structures | ✅ | All returns use variables or simple values |
| No function calls as arguments | ✅ | All results assigned before passing |
| Functions over classes | ✅ | No classes anywhere |
| Prompt templates in `.txt` files | ✅ | `prompts/extraction_prompt.txt` with `.format()` |
| Constants in `config.py` | ✅ | MODEL, MAX_RETRIES, colors |
| ANSI colors | ✅ | All defined in config.py, used correctly |
| API error handling | ✅ | Both main.py and batch.py catch credit/balance errors |
| Interactive menu | ✅ | Both main.py and batch.py have `show_menu`, `clear_screen`, q/c |
| Mock data separate | ✅ | data.py for examples + validations, invoices/ for documents |
| `.env` for API keys | ✅ | Never hardcoded |
| reset.py preserves `.env` | ✅ | Only extracts main.py and schema.py from zip |
| `_schema` dict pattern | ✅ | `extract_invoice_schema` follows companion dict pattern |

---

### Task coverage verification

#### Task 4.2 — Few-shot prompting ✅

- ✅ 3 few-shot examples in `data.py` (clean, sparse with nulls, European format with mismatch)
- ✅ `format_few_shot_examples` TODO in `main.py` (Step 7)
- ✅ Examples demonstrate null handling (example 2: `invoice_number: null`, `vendor_phone: null`)
- ✅ Examples demonstrate format normalization (example 3: European comma decimals, DD/MM/YYYY)
- ✅ Examples demonstrate ambiguous-case handling (`"unclear"` for unstated terms)
- ✅ README Step 7.4 covers generalization and exam concept

#### Task 4.3 — Structured output via tool use ✅

- ✅ `tool_use` with JSON schema (`schema.py` — `extract_invoice_schema`)
- ✅ Forced `tool_choice` (`main.py:93` — `{"type": "tool", "name": "extract_invoice"}`)
- ✅ "auto" and "any" explained in README Step 3.4
- ✅ Nullable fields: `vendor_phone`, `due_date`, `purchase_order`, `subtotal`, `tax_rate`, `tax_amount`
- ✅ "unclear" enum for `payment_terms` (Step 4 TODO)
- ✅ "other" + detail object for `category` (Step 4 TODO)
- ✅ Format normalization rules in `extraction_prompt.txt` (dates, currency, addresses)
- ✅ Semantic vs syntax error distinction (README Step 3.4 blockquote)

#### Task 4.4 — Validation, retry, feedback loops ✅ (with one callout-only item)

- ✅ Self-correction: `calculated_total` vs `stated_total` + `conflict_detected` (Step 5)
- ✅ `validate_extraction` with specific error messages (Step 5 + Step 6 TODOs)
- ✅ `retry_with_feedback` using `is_error: True` on tool result (Step 6 TODO)
- ✅ Retryable vs non-retryable: checks for "absent" in error message (`main.py:279`)
- ⚠️ `detected_pattern`: mentioned in README Step 6.6 blockquote as exam note only — not a schema field or hands-on exercise. Plan listed it as a key concept. Acceptable as a callout since the `confidence.flags` array serves a similar tracking role.

#### Task 4.5 — Batch processing ✅

- ✅ `batch.py` with full lifecycle: preview, submit, check status, retrieve results
- ✅ `custom_id` derived from invoice filename (`batch.py:68`)
- ✅ `MessageCreateParamsNonStreaming` and `Request` SDK types (`batch.py:74-82`)
- ✅ Failure handling with 4 result types: succeeded, errored, expired, canceled (`batch.py:162-191`)
- ✅ Resubmission guidance with chunking note (`batch.py:199-201`)
- ✅ 50% cost savings, SLA calculation, sync vs batch — all in README Step 8.4
- ✅ No multi-turn tool calling noted in README Step 8.4
- ⚠️ Prompt refinement on sample set: mentioned as a use case in README Step 8.4 but not a hands-on exercise. Acceptable as a callout.

#### Task 5.5 — Human review & confidence ✅

- ✅ Confidence object: `overall` (high/medium/low) + `flags` array (Step 9 schema TODO)
- ✅ `classify_review_need`: routes to auto_approve / spot_check / human_review (Step 9 TODO)
- ✅ `LABELED_VALIDATIONS` in `data.py` with 4 invoices (01, 02, 06, 07 — different types)
- ✅ `check_accuracy` function compares against ground truth per field (`main.py:318-355`)
- ✅ Stratified sampling concept explained in README Step 9.5-9.6
- ✅ Per-type accuracy analysis discussed with concrete "92% masks 75% on informal" example
- ✅ Calibration with labeled validation sets mentioned in README Step 9.6

---

### README structure compliance

| Convention | Status |
|-----------|--------|
| H1 title with lab number | ✅ `# Lab 06 — Structured Data Extraction` |
| Objective section | ✅ |
| Exam coverage table | ✅ |
| Step 0 — Open the lab folder | ✅ |
| Step 1 — Create venv | ✅ |
| Step 2 — Configure | ✅ |
| Sub-steps with `####` | ✅ All steps use numbered sub-steps |
| What to observe sections | ✅ Every step |
| Exam concept sections | ✅ Every step with `[Task X.Y]` references |
| Blockquotes for exam callouts | ✅ `> **Also know for the exam:**` pattern |
| Copy-paste code for TODOs | ✅ Steps 4-7, 9 provide exact code |
| Reset section | ✅ |
| Footer | ✅ `*v0.1 — 3/30/2026 — Alfredo De Regil*` |
| Orientation before first run | ✅ Step 3.1 "Orient yourself" |

---

### Narrative arc verification

Plan arc (7 steps) maps to README steps:

| Plan | README | Status |
|------|--------|--------|
| 1. Extract with JSON schema | Step 3 | ✅ |
| 2. Handle missing fields | Step 4 | ✅ |
| 3. Add self-correction | Step 5 | ✅ |
| 4. Add validation and retry | Step 6 | ✅ |
| 5. Add few-shot examples | Step 7 | ✅ |
| 6. Batch-process documents | Step 8 | ✅ |
| 7. Route to human review | Step 9 | ✅ |

Progressive build feels coherent — each step addresses a specific extraction failure class. ✅

---

### Issues found

| # | Severity | Item | Details |
|---|----------|------|---------|
| 1 | ❌ Medium | **Plan says 10 invoices, lab has 7** | Plan: `invoice_01.txt ... invoice_10.txt`; actual: 01–07. Update the plan to match. The 7 invoices cover all needed scenarios (clean, missing fields, total mismatch, ambiguous terms, catering/other category, European format, informal). |
| 2 | ⚠️ Low | **config.py unused thresholds** | `HIGH_CONFIDENCE_THRESHOLD = 0.85` and `LOW_CONFIDENCE_THRESHOLD = 0.50` are never referenced. `classify_review_need` uses string comparisons ("high"/"low"). Remove the dead constants or use them. |
| 3 | ⚠️ Low | **.gitignore missing `.venv/`** | Has `venv/` but the lab creates `.venv`. Add `.venv/` to .gitignore. |
| 4 | ⚠️ Info | **`detected_pattern` is callout only** | Plan listed as key concept; README covers as exam note in Step 6.6. `confidence.flags` serves the same purpose in practice. No action needed — acceptable coverage. |
| 5 | ⚠️ Info | **Prompt refinement on sample is callout only** | Plan listed as key concept; README covers as use case in Step 8.4. No action needed — acceptable coverage. |
| 6 | ⚠️ Info | **batch.py duplicates few-shot formatting** | Has inline formatting logic (lines 42-51) instead of importing from main.py. Necessary because main.py's version is a TODO stub at starter state. Acceptable design for an educational lab. |

---

### Layer 3 Summary

**Lab 06 is well-built.** All 5 task statements are covered with hands-on exercises. The narrative arc is coherent. Convention compliance is strong. The README explanations are clear and grounded in exam terminology.

**3 items to fix:**
1. Update plan invoice count: 10 → 7
2. Remove or use dead config.py thresholds
3. Add `.venv/` to .gitignore

---

*Updated 3/31/2026*
