# CCA Foundations — Lab Reference

All 27 task statements with Knowledge & Skills mapped to 6 scenario-based labs.
1 gap noted: task 1.7 has no natural scenario home — added as explicit step to L2.

---

## Table 1 — Tasks by Domain → Lab

For each task statement: Knowledge, Skills, and which lab(s) practice it.

---

### D1 · Agentic Architecture & Orchestration · 27%

#### 1.1 Design and implement agentic loops
**Labs:** L1 · L3

**Knowledge**
- Agentic loop lifecycle: stop_reason "tool_use" vs "end_turn", executing tools, returning results
- Tool results appended to conversation history for next-iteration reasoning
- Model-driven decision-making vs pre-configured decision trees or tool sequences

**Skills**
- Implement loop control flow: continue on stop_reason "tool_use", terminate on "end_turn"
- Add tool results to conversation context between iterations
- Avoid anti-patterns: natural language termination signals, arbitrary iteration caps

---

#### 1.2 Orchestrate multi-agent systems with coordinator-subagent patterns
**Labs:** L3 · L1

**Knowledge**
- Hub-and-spoke: coordinator manages all inter-subagent communication and routing
- Subagents operate with isolated context — do not inherit coordinator history
- Risk of overly narrow task decomposition leading to incomplete topic coverage

**Skills**
- Design coordinator to dynamically select subagents based on query requirements
- Partition research scope across subagents to minimize duplication
- Implement iterative refinement: evaluate output for gaps, re-delegate, re-synthesize

---

#### 1.3 Configure subagent invocation, context passing, and spawning
**Labs:** L3 · L4

**Knowledge**
- Agent tool is the mechanism for spawning subagents; allowedTools must include "Agent" (exam guide says "Task" — renamed to "Agent" in Claude Code v2.1.63; both names are valid)
- Subagent context must be explicitly provided — no automatic parent context inheritance
- AgentDefinition: descriptions, system prompts, tool restrictions per subagent type
- Fork-based session management for divergent approaches from a shared baseline

**Skills**
- Include complete prior findings directly in subagent prompt
- Use structured data formats to separate content from metadata (source URLs, page numbers)
- Spawn parallel subagents via multiple Agent tool calls in a single coordinator response
- Design coordinator prompts with goals and quality criteria, not step-by-step procedures

---

#### 1.4 Implement multi-step workflows with enforcement and handoff patterns
**Labs:** L1

**Knowledge**
- Programmatic enforcement (hooks, gates) vs prompt-based guidance for workflow ordering
- Prompt-only ordering has non-zero failure rate — insufficient for critical business logic
- Structured handoff protocols for mid-process escalation include root cause and recommendations

**Skills**
- Implement prerequisite gate blocking downstream tools until prior step completes
- Decompose multi-concern requests into parallel investigations before synthesizing unified response
- Compile structured handoff summary (customer ID, root cause, amount, action) on escalation

---

#### 1.5 Apply Agent SDK hooks for tool call interception and data normalization
**Labs:** L1 · L3

**Knowledge**
- PostToolUse hook intercepts tool results for transformation before model processes them
- Hooks intercept outgoing tool calls to enforce compliance rules
- Hooks provide deterministic guarantees that prompt instructions cannot

**Skills**
- PostToolUse to normalize heterogeneous data formats (Unix timestamps, ISO 8601, status codes)
- Intercept hook to block policy-violating actions (e.g., refunds > $500) and redirect to escalation
- Choose hooks over prompt enforcement when business rules require guaranteed compliance

---

#### 1.6 Design task decomposition strategies for complex workflows
**Labs:** L3 · L5

**Knowledge**
- Fixed sequential pipelines (prompt chaining) vs dynamic adaptive decomposition
- Prompt chaining for predictable multi-aspect reviews (per-file then cross-file)
- Adaptive investigation plans generate subtasks based on what is discovered at each step

**Skills**
- Split large code reviews into per-file local analysis plus separate cross-file integration pass
- Decompose open-ended tasks: map structure → identify high-impact areas → create prioritized adaptive plan

---

#### 1.7 Manage session state, resumption, and forking
**Labs:** L2
> ⚠ Gap: no scenario naturally covers this. Add explicit step to L2 — name a session, close it, resume after a file change, then use fork_session to compare two refactoring approaches.

**Knowledge**
- --resume \<session-name\> to continue a specific prior conversation
- fork_session creates independent branches from a shared analysis baseline
- Inform agent about file changes on resume for targeted re-analysis
- New session with structured summary is more reliable than resuming with stale tool results

**Skills**
- Use --resume with session names to continue named investigation sessions
- Use fork_session to compare two approaches (testing strategies, refactoring) from shared baseline
- Choose between session resumption (context valid) and fresh session with injected summary (stale)

---

### D2 · Tool Design & MCP Integration · 18%

#### 2.1 Design effective tool interfaces with clear descriptions and boundaries
**Labs:** L1 · L3 · L4

**Knowledge**
- Tool descriptions are the primary mechanism LLMs use for tool selection
- Descriptions must include: input formats, example queries, edge cases, boundaries vs similar tools
- System prompt wording can create unintended tool associations

**Skills**
- Write descriptions that differentiate each tool's purpose, inputs, outputs, and when to use vs alternatives
- Rename tools to eliminate functional overlap (e.g., analyze_content → extract_web_results)
- Split generic tools into purpose-specific tools with defined input/output contracts

---

#### 2.2 Implement structured error responses for MCP tools
**Labs:** L1 · L3

**Knowledge**
- isError flag pattern for communicating tool failures back to the agent
- Error categories: transient (timeouts), validation (invalid input), business (policy), permission
- Retryable vs non-retryable errors — structured metadata prevents wasted retry attempts

**Skills**
- Return errorCategory, isRetryable boolean, and human-readable description
- Implement local recovery for transient failures; propagate only unresolvable errors with partial results
- Distinguish access failures (needs retry decision) from valid empty results (successful query, no matches)

---

#### 2.3 Distribute tools across agents and configure tool choice
**Labs:** L1 · L3

**Knowledge**
- Too many tools (18 vs 4-5) degrades tool selection reliability
- Agents with out-of-role tools tend to misuse them
- tool_choice options: "auto" / "any" / forced {"type":"tool", "name":"..."}

**Skills**
- Restrict each subagent's tool set to role-relevant tools only
- Use forced tool_choice to ensure a specific tool runs first (e.g., extract_metadata before enrichment)
- Set tool_choice: "any" to guarantee tool call rather than conversational text

---

#### 2.4 Integrate MCP servers into Claude Code and agent workflows
**Labs:** L4 · L2

**Knowledge**
- Project-level .mcp.json for shared team tooling vs user-level ~/.claude.json for personal/experimental
- Environment variable expansion in .mcp.json (e.g., ${GITHUB_TOKEN}) for credential management
- MCP resources expose content catalogs to reduce exploratory tool calls

**Skills**
- Configure shared MCP servers in .mcp.json with env var expansion for auth tokens
- Enhance MCP tool descriptions to outcompete built-in tools for more capable alternatives
- Expose content catalogs as MCP resources so agents see available data without exploratory calls

---

#### 2.5 Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively
**Labs:** L4

**Knowledge**
- Grep = content search (file contents for patterns); Glob = file path pattern matching
- Edit for targeted changes using unique text; Read + Write as fallback when anchor text is non-unique

**Skills**
- Select Grep for code content search; Glob for finding files by naming pattern
- Build codebase understanding incrementally: Grep entry points → Read imports → trace flows
- Trace function usage: identify all exported names then search each across codebase

---

### D3 · Claude Code Configuration & Workflows · 20%

#### 3.1 Configure CLAUDE.md hierarchy, scoping, and modular organization
**Labs:** L2 · L4

**Knowledge**
- Hierarchy: user-level (~/.claude/CLAUDE.md), project-level (.claude/CLAUDE.md), directory-level
- User-level settings are not shared with teammates via version control
- @import syntax for referencing external files to keep CLAUDE.md modular
- .claude/rules/ directory as alternative to monolithic CLAUDE.md

**Skills**
- Diagnose hierarchy issues (e.g., new team member missing instructions because set at user-level)
- Use @import to include relevant standards files per package
- Split large CLAUDE.md into topic files in .claude/rules/
- Use /memory command to verify loaded files and diagnose inconsistent behavior

---

#### 3.2 Create and configure custom slash commands and skills
**Labs:** L2 · L4

**Knowledge**
- Project-scoped .claude/commands/ (version controlled) vs personal ~/.claude/commands/
- SKILL.md frontmatter options: context:fork, allowed-tools, argument-hint
- context:fork runs skill in isolated sub-agent, preventing output polluting main conversation

**Skills**
- Create project-scoped slash commands in .claude/commands/ for team-wide availability
- Use context:fork to isolate verbose skill output (codebase analysis, brainstorming)
- Configure allowed-tools to restrict tool access during skill execution
- Use argument-hint to prompt developers for required parameters on invocation

---

#### 3.3 Apply path-specific rules for conditional convention loading
**Labs:** L2

**Knowledge**
- .claude/rules/ files with YAML frontmatter paths fields containing glob patterns
- Path-scoped rules load only when editing matching files, reducing irrelevant context and tokens
- Glob rules beat directory-level CLAUDE.md for conventions spanning multiple directories

**Skills**
- Create rules with YAML frontmatter path scoping (e.g., paths: ["terraform/**/*"])
- Apply conventions to file types by glob regardless of directory (e.g., **/*.test.tsx)
- Choose path-specific rules over subdirectory CLAUDE.md for cross-codebase file types

---

#### 3.4 Determine when to use plan mode vs direct execution
**Labs:** L2 · L4 · L5

**Knowledge**
- Plan mode for large-scale changes, multiple approaches, architectural decisions, multi-file edits
- Direct execution for simple, well-scoped single-file changes
- Explore subagent isolates verbose discovery output to preserve main context

**Skills**
- Select plan mode for microservice restructuring, library migrations affecting many files
- Select direct execution for single-file bug fix with clear stack trace
- Use Explore subagent for verbose discovery phases to prevent context window exhaustion

---

#### 3.5 Apply iterative refinement techniques for progressive improvement
**Labs:** L2 · L5

**Knowledge**
- Concrete input/output examples are the most effective way to communicate expected transformations
- Test-driven iteration: write test suites first, share failures to guide improvement
- Interview pattern: have Claude ask questions before implementing, surfacing unanticipated considerations

**Skills**
- Provide 2-3 concrete input/output examples when prose descriptions produce inconsistent results
- Write test suites covering expected behavior and edge cases before implementation
- Provide all interacting issues in a single message; iterate sequentially for independent issues

---

#### 3.6 Integrate Claude Code into CI/CD pipelines
**Labs:** L5

**Knowledge**
- -p (or --print) flag for running Claude Code in non-interactive mode in automated pipelines
- --output-format json and --json-schema CLI flags for structured output in CI
- CLAUDE.md provides project context (testing standards, fixtures, criteria) to CI-invoked Claude
- Session context isolation: same session that generated code is less effective at reviewing it

**Skills**
- Run Claude Code in CI with -p flag to prevent interactive input hangs
- Use --output-format json with --json-schema for machine-parseable findings as inline PR comments
- Include prior review findings on re-runs — report only new or still-unaddressed issues
- Document testing standards and fixtures in CLAUDE.md to improve test generation quality

---

### D4 · Prompt Engineering & Structured Output · 20%

#### 4.1 Design prompts with explicit criteria to reduce false positives
**Labs:** L5

**Knowledge**
- Explicit criteria outperform vague instructions ("flag only when behavior contradicts code" vs "check accuracy")
- General instructions like "be conservative" fail to improve precision vs specific categorical criteria
- High false positive categories undermine developer trust in accurate categories

**Skills**
- Write criteria defining which issues to report (bugs, security) vs skip (minor style, local patterns)
- Temporarily disable high false-positive categories to restore trust while improving prompts
- Define explicit severity criteria with concrete code examples per severity level

---

#### 4.2 Apply few-shot prompting to improve output consistency and quality
**Labs:** L5 · L6

**Knowledge**
- Few-shot examples are the most effective technique for consistent output when instructions alone fail
- Few-shot demonstrates ambiguous-case handling and enables generalization to novel patterns
- Few-shot reduces hallucination in extraction tasks with varied document structures

**Skills**
- Create 2-4 targeted few-shot examples for ambiguous scenarios showing reasoning for chosen action
- Include examples showing desired output format (location, issue, severity, suggested fix)
- Add examples demonstrating correct extraction from varied structures (inline citations vs bibliographies)

---

#### 4.3 Enforce structured output using tool use and JSON schemas
**Labs:** L6

**Knowledge**
- tool_use with JSON schema is the most reliable approach for schema-compliant structured output
- tool_choice: "auto" (may return text), "any" (must call a tool), forced (must call specific tool)
- Strict schemas eliminate syntax errors but not semantic errors (e.g., line items not summing to total)

**Skills**
- Define extraction tools with JSON schemas and extract structured data from tool_use response
- Set tool_choice: "any" when multiple schemas exist and doc type is unknown
- Force specific tool to ensure it runs before enrichment steps
- Design nullable fields to prevent fabrication; use enum "other" + detail string for extensibility

---

#### 4.4 Implement validation, retry, and feedback loops for extraction quality
**Labs:** L6

**Knowledge**
- Retry-with-error-feedback: append specific validation errors to prompt on retry
- Retry is ineffective when required information is absent from source document (not a format error)
- Semantic validation errors (values don't sum, wrong field) vs schema syntax errors (eliminated by tool_use)

**Skills**
- Implement follow-up requests with original document + failed extraction + specific validation errors
- Identify when retries will be ineffective (info absent) vs effective (format mismatch, structural errors)
- Design self-correction flows: calculated_total vs stated_total, add conflict_detected boolean

---

#### 4.5 Design efficient batch processing strategies
**Labs:** L6

**Knowledge**
- Message Batches API: 50% cost savings, up to 24-hour processing window, no guaranteed latency SLA
- Batch inappropriate for blocking workflows (pre-merge checks); ideal for overnight/weekly reports
- No multi-turn tool calling within a single batch request; custom_id for correlation

**Skills**
- Match API to latency requirement: sync for blocking pre-merge, batch for overnight/weekly analysis
- Calculate batch submission frequency based on SLA constraints
- Handle batch failures: resubmit only failed documents by custom_id with modifications

---

#### 4.6 Design multi-instance and multi-pass review architectures
**Labs:** L5

**Knowledge**
- Self-review limitation: generator retains reasoning context, less likely to question own decisions
- Independent review instances (without prior reasoning) are more effective than self-review instructions
- Multi-pass: per-file local analysis passes + cross-file integration passes to avoid attention dilution

**Skills**
- Use second independent Claude instance to review generated code without generator's reasoning context
- Split large multi-file reviews into per-file passes plus separate cross-file integration pass
- Run verification passes where model self-reports confidence per finding for calibrated review routing

---

### D5 · Context Management & Reliability · 15%

#### 5.1 Manage conversation context across long interactions
**Labs:** L1 · L3

**Knowledge**
- Progressive summarization risks: loses numerical values, percentages, dates, customer expectations
- "Lost in the middle" effect: models reliably process beginning and end, may omit middle sections
- Tool results accumulate tokens disproportionately to their relevance (40+ fields when only 5 needed)

**Skills**
- Extract transactional facts (amounts, dates, order numbers) into persistent "case facts" block outside summarized history
- Trim verbose tool outputs to only relevant fields before they accumulate in context
- Place key findings at beginning of aggregated inputs; use section headers to mitigate position effects

---

#### 5.2 Design escalation and ambiguity resolution patterns
**Labs:** L1

**Knowledge**
- Escalation triggers: customer explicitly requests human, policy gaps, inability to make progress
- Sentiment-based escalation is unreliable proxy for case complexity
- Multiple customer matches require clarification (additional identifiers), not heuristic selection

**Skills**
- Add explicit escalation criteria with few-shot examples to system prompt
- Honor explicit customer requests for human agents immediately, without first attempting investigation
- Escalate when policy is ambiguous or silent on the customer's specific request

---

#### 5.3 Implement error propagation across multi-agent systems
**Labs:** L3

**Knowledge**
- Structured error context (failure type, attempted query, partial results) enables intelligent coordinator recovery
- Access failures vs valid empty results require different recovery paths
- Silently suppressing errors AND terminating entire workflow on single failure are both anti-patterns

**Skills**
- Return structured error context: failure type, what was attempted, partial results, alternatives
- Have subagents implement local recovery for transient failures; propagate only unresolvable errors
- Structure synthesis output with coverage annotations: well-supported findings vs gaps from unavailable sources

---

#### 5.4 Manage context effectively in large codebase exploration
**Labs:** L4 · L2

**Knowledge**
- Context degradation: inconsistent answers, references to "typical patterns" instead of discovered classes
- Scratchpad files persist key findings across context boundaries
- Structured state persistence for crash recovery: agent exports state, coordinator loads manifest on resume

**Skills**
- Spawn subagents for specific investigation questions; main agent preserves high-level coordination
- Have agents maintain scratchpad files with key findings; reference for subsequent questions
- Use /compact to reduce context usage during extended exploration sessions

---

#### 5.5 Design human review workflows and confidence calibration
**Labs:** L6

**Knowledge**
- Aggregate accuracy (97% overall) can mask poor performance on specific document types or fields
- Stratified random sampling measures error rates in high-confidence extractions, detects novel patterns
- Field-level confidence scores calibrated using labeled validation sets for routing review attention

**Skills**
- Implement stratified random sampling of high-confidence extractions for ongoing error rate measurement
- Analyze accuracy by document type and field before reducing human review
- Route low-confidence and ambiguous/contradictory source documents to human review

---

#### 5.6 Preserve information provenance in multi-source synthesis
**Labs:** L3

**Knowledge**
- Source attribution is lost during summarization when findings are compressed without claim-source mappings
- Conflicting statistics: annotate conflict with attribution rather than arbitrarily selecting one
- Temporal data: require publication/collection dates to prevent misinterpretation as contradictions

**Skills**
- Require subagents to output structured claim-source mappings (URLs, excerpts) preserved through synthesis
- Structure reports with distinct sections: well-established vs contested findings
- Render content types appropriately: financial data as tables, news as prose, technical as structured lists

---

## Table 2 — Labs → Domain / Tasks

For each lab: every task statement it covers with Knowledge and Skills. Use this as your lab brief.

---

### L1 · S1 · Customer Support Resolution Agent
**Domains:** D1 · D2 · D5
**Build:** Agent with 4 MCP tools (get_customer, lookup_order, process_refund, escalate_to_human), agentic loop with stop_reason handling, programmatic prerequisite gate, PostToolUse hooks, structured escalation handoff.

| Task | Domain | Task Statement |
|------|--------|---------------|
| 1.1 | D1 | Design and implement agentic loops |
| 1.2 | D1 | Orchestrate multi-agent systems with coordinator-subagent patterns |
| 1.4 | D1 | Implement multi-step workflows with enforcement and handoff patterns |
| 1.5 | D1 | Apply Agent SDK hooks for tool call interception and data normalization |
| 2.1 | D2 | Design effective tool interfaces with clear descriptions and boundaries |
| 2.2 | D2 | Implement structured error responses for MCP tools |
| 2.3 | D2 | Distribute tools across agents and configure tool choice |
| 5.1 | D5 | Manage conversation context across long interactions |
| 5.2 | D5 | Design escalation and ambiguity resolution patterns |

See Table 1 entries above for full Knowledge and Skills per task.

---

### L2 · S2 · Code Generation Workflows
**Domains:** D3 · D5
**Build:** CLAUDE.md hierarchy (user/project/dir), path-specific rules with glob patterns, custom skill with context:fork, plan mode vs direct execution comparison, session naming + resume + fork_session.
> ⚠ Gap coverage for task 1.7: name a session, close it, resume after a file change, use fork_session to compare two refactoring approaches.

| Task | Domain | Task Statement |
|------|--------|---------------|
| 1.7 | D1 | Manage session state, resumption, and forking |
| 2.4 | D2 | Integrate MCP servers into Claude Code and agent workflows |
| 3.1 | D3 | Configure CLAUDE.md hierarchy, scoping, and modular organization |
| 3.2 | D3 | Create and configure custom slash commands and skills |
| 3.3 | D3 | Apply path-specific rules for conditional convention loading |
| 3.4 | D3 | Determine when to use plan mode vs direct execution |
| 3.5 | D3 | Apply iterative refinement techniques for progressive improvement |
| 5.4 | D5 | Manage context effectively in large codebase exploration |

---

### L3 · S3 · Multi-Agent Research System
**Domains:** D1 · D2 · D5
**Build:** Coordinator agent with 4 specialized subagents (search, analysis, synthesis, report), parallel Agent tool spawning, PreToolUse/PostToolUse hooks for observability and violation detection, structured claim-source output, simulated timeout with structured error propagation, coverage gap annotation in synthesis.

| Task | Domain | Task Statement |
|------|--------|---------------|
| 1.2 | D1 | Orchestrate multi-agent systems with coordinator-subagent patterns |
| 1.3 | D1 | Configure subagent invocation, context passing, and spawning |
| 1.5 | D1 | Apply Agent SDK hooks for tool call interception and data normalization |
| 1.6 | D1 | Design task decomposition strategies for complex workflows |
| 2.1 | D2 | Design effective tool interfaces with clear descriptions and boundaries |
| 2.2 | D2 | Implement structured error responses for MCP tools |
| 2.3 | D2 | Distribute tools across agents and configure tool choice |
| 5.1 | D5 | Manage conversation context across long interactions |
| 5.3 | D5 | Implement error propagation across multi-agent systems |
| 5.6 | D5 | Preserve information provenance in multi-source synthesis |

---

### L4 · S4 · Developer Productivity Agent
**Domains:** D1 · D2 · D3
**Build:** Agent exploring a sample Python codebase with built-in tools (Grep/Glob/Read), MCP documentation server in `.mcp.json` with env var credentials and enhanced descriptions, `AgentDefinition` Explore subagent with explicit context passing and `allowedTools` restriction, scratchpad file for cross-question persistence, `/explore` skill with `context:fork`, CLAUDE.md with `@import`.

| Task | Domain | Task Statement |
|------|--------|---------------|
| 1.3 | D1 | Configure subagent invocation, context passing, and spawning |
| 2.1 | D2 | Design effective tool interfaces with clear descriptions and boundaries |
| 2.4 | D2 | Integrate MCP servers into Claude Code and agent workflows |
| 2.5 | D2 | Select and apply built-in tools effectively |
| 3.1 | D3 | Configure CLAUDE.md hierarchy, scoping, and modular organization |
| 3.2 | D3 | Create and configure custom slash commands and skills |
| 3.4 | D3 | Determine when to use plan mode vs direct execution |
| 5.4 | D5 | Manage context effectively in large codebase exploration |

---

### L5 · S5 · CI/CD Integration
**Domains:** D3 · D4
**Build:** Claude Code in CI with -p flag, structured output via --output-format json, independent review instance, per-file passes + cross-file integration pass, explicit review criteria with few-shot examples.

| Task | Domain | Task Statement |
|------|--------|---------------|
| 1.6 | D1 | Design task decomposition strategies for complex workflows |
| 3.4 | D3 | Determine when to use plan mode vs direct execution |
| 3.5 | D3 | Apply iterative refinement techniques for progressive improvement |
| 3.6 | D3 | Integrate Claude Code into CI/CD pipelines |
| 4.1 | D4 | Design prompts with explicit criteria to reduce false positives |
| 4.2 | D4 | Apply few-shot prompting to improve output consistency and quality |
| 4.6 | D4 | Design multi-instance and multi-pass review architectures |

---

### L6 · S6 · Structured Data Extraction
**Domains:** D4 · D5
**Build:** Extraction tool with JSON schema (required/optional/nullable/enum+other), validation-retry loop with error feedback, batch submission via Message Batches API with custom_id, field-level confidence scoring and human review routing.

| Task | Domain | Task Statement |
|------|--------|---------------|
| 4.2 | D4 | Apply few-shot prompting to improve output consistency and quality |
| 4.3 | D4 | Enforce structured output using tool use and JSON schemas |
| 4.4 | D4 | Implement validation, retry, and feedback loops for extraction quality |
| 4.5 | D4 | Design efficient batch processing strategies |
| 5.5 | D5 | Design human review workflows and confidence calibration |
