# Lab 02 — Gap Analysis

Comparison of the Exam Guide, Lab Reference, Lab Plan, and actual Lab (README + code) for Scenario 2.

**Tasks covered by Lab 02:** 1.7, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 5.4

---

## Task 1.7 — Manage session state, resumption, and forking

### Exam Guide says

**Knowledge:**
- Named session resumption using `--resume <session-name>` to continue a specific prior conversation
- `fork_session` for creating independent branches from a shared analysis baseline
- Inform agent about changes to previously analyzed files when resuming
- Starting a new session with structured summary is more reliable than resuming with stale tool results

**Skills:**
- Use `--resume` with session names to continue named investigation sessions
- Use `fork_session` to compare two approaches from shared baseline
- Choose between session resumption (context valid) and fresh session with injected summary (stale)
- Inform a resumed session about specific file changes for targeted re-analysis

### Lab Reference
✅ All items listed. Includes gap note: "no scenario naturally covers this. Add explicit step to L2."

### Lab Plan
✅ Listed in key concepts. Mentions "name a session, close it, resume after a file change, then use fork_session to compare two refactoring approaches."

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| `--resume` | ✅ | Step 9.3.2 — student resumes a session with `claude --resume`. |
| Inform about file changes | ✅ | Step 9.3 — student adds a function, then tells the resumed session about the change. |
| `fork_session` | ⚠️ PARTIAL | Step 9.4 explains `--resume --fork-session` conceptually with "when to use it" and "what it does NOT do." But **the student never actually runs a fork**. There is no hands-on exercise — no prompt to paste, no observation to make. It's documentation, not practice. |
| Named sessions (`--resume <session-name>`) | ⚠️ GAP | The exam guide says `--resume <session-name>` to continue a *specific named* session. The lab uses `claude --resume` (which lists all sessions for selection) but never teaches the student to **name** a session or resume by name. |
| Fresh session with structured summary vs stale resume | ✅ | Step 9.3.2 has the note: "If tool results from the prior session are stale... starting a new session with a structured summary is more reliable." |
| Compare two approaches from shared baseline | ⚠️ GAP | The Lab Plan says "use fork_session to compare two refactoring approaches." The README explains the concept but **never asks the student to actually compare two approaches**. |

**Recommend:**
- Make the fork exercise hands-on: after Step 9.3, have the student fork the session and try two different refactoring approaches (e.g., "add input validation with early returns" vs "add input validation with exception handling"), then compare. This directly addresses the Lab Plan's stated goal.
- Teach session naming: have the student pass a session name when starting (if the CLI supports it) or mention the naming mechanism explicitly.

---

## Task 2.4 — Integrate MCP servers into Claude Code and agent workflows

### Exam Guide says

**Knowledge:**
- Project-level `.mcp.json` for shared team tooling vs user-level `~/.claude.json` for personal
- Environment variable expansion in `.mcp.json` (e.g., `${GITHUB_TOKEN}`)
- Tools from all configured MCP servers discovered at connection time, available simultaneously
- MCP resources as mechanism for exposing content catalogs to reduce exploratory tool calls

**Skills:**
- Configure shared MCP servers in project-scoped `.mcp.json` with env var expansion
- Configure personal MCP servers in user-scoped `~/.claude.json`
- Enhance MCP tool descriptions to outcompete built-in tools for more capable alternatives
- Choose existing community MCP servers over custom implementations for standard integrations
- Expose content catalogs as MCP resources

### Lab Reference
✅ All items listed.

### Lab Plan
✅ "MCP server config in `.mcp.json` with `${ENV_VAR}` expansion for credentials" and "Project-level vs user-level MCP server scoping."

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Project-level `.mcp.json` | ✅ | Step 7 — student creates `.mcp.json` with two servers. |
| Env var expansion | ✅ | `${INVENTORY_SECRET}` in the config. The inventory server validates the secret. |
| Community vs custom servers | ✅ | Step 7.2 explains the distinction. Step 7.3 configures both `fetch` (community) and `inventory` (custom). |
| Tools discovered at connection time | ✅ | Step 7.4: "Tools from all configured MCP servers are available simultaneously." |
| MCP resources | ✅ | `inventory_server.py` exposes `inventory://products` resource. Step 7.5 mentions resources. |
| User-level `~/.claude.json` | ⚠️ PARTIAL | Step 7.2 mentions user-level config conceptually ("User-level... personal, not shared"). Step 7.5 exam concept says "user-level `~/.claude.json` for personal tools." But the student never configures one or sees the difference. |
| Enhance MCP tool descriptions to outcompete built-in tools | ⚠️ GAP | The exam guide skill says: "Enhancing MCP tool descriptions to explain capabilities and outputs in detail, preventing the agent from preferring built-in tools (like Grep) over more capable MCP tools." **Not mentioned.** The inventory server has good descriptions, but the README never discusses the concept of MCP tools competing with built-in tools for selection. |

**Recommend:**
- Add a note in Step 7.5 about MCP tool descriptions needing to outcompete built-in tools. Example: "If your MCP tool description says only 'search products' but Grep also searches, Claude Code may prefer Grep. Detailed descriptions that explain what the MCP tool returns and when to use it over built-in tools improve selection reliability."
- User-level config: a brief note is sufficient — the student understands the concept from the hierarchy discussion in Step 4.

---

## Task 3.1 — Configure CLAUDE.md hierarchy, scoping, and modular organization

### Exam Guide says

**Knowledge:**
- Hierarchy: user-level, project-level, directory-level
- User-level settings not shared via version control
- `@import` syntax for modular CLAUDE.md
- `.claude/rules/` directory as alternative to monolithic CLAUDE.md

**Skills:**
- Diagnose hierarchy issues (e.g., new team member missing instructions set at user-level)
- Use `@import` to include relevant standards files per package
- Split large CLAUDE.md into topic files in `.claude/rules/`
- Use `/memory` command to verify loaded files and diagnose inconsistent behavior

### Lab Reference
✅ All items listed.

### Lab Plan
✅ "CLAUDE.md hierarchy: user-level vs project-level vs directory-level" and "`@import` for modular CLAUDE.md."

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Hierarchy (user/project/directory) | ✅ | Step 4.2 explains all three levels. |
| `@import` | ✅ | Step 4.3 — student adds `@import coding_standards.md`. |
| `.claude/rules/` | ✅ | Step 5 — student creates rules directory with glob-scoped files. |
| User-level not shared | ✅ | Step 4.4 mentions it explicitly. |
| Diagnose hierarchy issues | ✅ | Step 4.4: "if a new team member is missing instructions, check whether they were set at user-level." |
| `/memory` command to verify loaded files | ⚠️ GAP | The exam guide says: "Use /memory command to verify which memory files are loaded and diagnose inconsistent behavior across sessions." **Not mentioned anywhere in the lab.** |

**Recommend:** Add a brief note in Step 4.5 or Step 10 mentioning `/memory` as a diagnostic tool. Example: "Use `/memory` in Claude Code to verify which files are loaded and diagnose inconsistent behavior — helpful when instructions seem to be ignored."

---

## Task 3.2 — Create and configure custom slash commands and skills

### Exam Guide says

**Knowledge:**
- Project-scoped `.claude/commands/` (version controlled) vs personal `~/.claude/commands/`
- SKILL.md frontmatter: `context:fork`, `allowed-tools`, `argument-hint`
- `context:fork` runs skill in isolated sub-agent, preventing output from polluting main conversation
- Personal skill customization in `~/.claude/skills/`

**Skills:**
- Create project-scoped slash commands in `.claude/commands/`
- Use `context:fork` to isolate verbose output
- Configure `allowed-tools` to restrict tool access during skill execution
- Use `argument-hint` to prompt for required parameters
- Choose between skills (on-demand) and CLAUDE.md (always-loaded)

### Lab Reference
✅ All items listed.

### Lab Plan
✅ "Custom skill with `context:fork` and `allowed-tools` restriction."

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Project-scoped `.claude/commands/` | ✅ | Step 6.3 — student creates `.claude/commands/review.md`. |
| `context:fork` | ✅ | The skill uses `context: fork`. Step 6.4 explains the isolation. |
| `allowed-tools` | ✅ | The skill restricts to Read, Glob, Grep. Step 6.4 explains. |
| `argument-hint` | ✅ | The skill uses `argument-hint: Path to the file to review`. |
| Personal `~/.claude/commands/` | ✅ | Step 6.4: "Personal skills would go in `~/.claude/commands/`." |
| Skills vs CLAUDE.md choice | ⚠️ GAP | The exam guide says: "Choosing between skills (on-demand invocation for task-specific workflows) and CLAUDE.md (always-loaded universal standards)." **Not explicitly discussed.** The lab creates both a skill and CLAUDE.md but never asks the student to think about when to use one vs the other. |
| Personal skill customization in `~/.claude/skills/` | ⚠️ MINOR | The exam guide mentions `~/.claude/skills/` for personal variants. The lab mentions `~/.claude/commands/` but not `~/.claude/skills/`. The skills/ directory is a newer convention. |

**Recommend:** Add a note in Step 6.5 about when to use skills vs CLAUDE.md: "Skills are for on-demand task-specific workflows (reviews, analysis); CLAUDE.md is for always-loaded universal standards (naming conventions, error patterns). Don't put one-off tasks in CLAUDE.md and don't put universal standards in a skill."

---

## Task 3.3 — Apply path-specific rules for conditional convention loading

### Exam Guide says

**Knowledge:**
- `.claude/rules/` files with YAML frontmatter `paths` fields containing glob patterns
- Path-scoped rules load only when editing matching files, reducing irrelevant context and tokens
- Glob rules better than directory-level CLAUDE.md for conventions spanning multiple directories

**Skills:**
- Create rules with YAML frontmatter path scoping (e.g., `paths: ["terraform/**/*"]`)
- Apply conventions to file types by glob regardless of directory (e.g., `**/*.test.tsx`)
- Choose path-specific rules over subdirectory CLAUDE.md for cross-codebase file types

### Lab Reference
✅ All items listed.

### Lab Plan
✅ "`.claude/rules/` with YAML frontmatter glob patterns."

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| YAML frontmatter with paths | ✅ | Step 5.3 — student creates two rule files with glob patterns. |
| Glob patterns (cross-directory) | ✅ | `**/*.test.py` applies to test files anywhere. |
| Reduced context/token usage | ✅ | Step 5.4 and 5.5 mention it explicitly. |
| Glob rules vs directory-level CLAUDE.md | ✅ | Step 5.2 explains why directory-level CLAUDE.md doesn't work for cross-directory conventions. Step 5.5 repeats the exam concept. |
| Exclusion patterns | ✅ | `api-conventions.md` uses `!**/*.test.py` to exclude test files. |

**Assessment:** Full coverage. No gaps.

---

## Task 3.4 — Determine when to use plan mode vs direct execution

### Exam Guide says

**Knowledge:**
- Plan mode for large-scale changes, multiple approaches, architectural decisions, multi-file edits
- Direct execution for simple, well-scoped single-file changes
- Plan mode enables safe exploration before committing to changes
- Explore subagent for isolating verbose discovery output

**Skills:**
- Select plan mode for architectural tasks (microservice restructuring, library migrations)
- Select direct execution for well-understood single-file changes
- Use Explore subagent for verbose discovery phases
- Combine plan mode for investigation with direct execution for implementation

### Lab Reference
✅ All items listed.

### Lab Plan
✅ "Plan mode vs direct execution — you run both and compare."

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Plan mode exercise | ✅ | Step 8.1 — student toggles plan mode and runs a multi-function refactor. |
| Direct execution exercise | ✅ | Step 8.2 — student runs a single-function fix in direct mode. |
| When to use which | ✅ | Step 8.2 has explicit decision criteria. |
| Explore subagent | ⚠️ GAP | The exam guide says: "The Explore subagent for isolating verbose discovery output and returning summaries to preserve main conversation context." **Not mentioned or exercised in the lab.** This is listed in the Lab Plan as "Observe the Explore subagent keeping verbose output out of main context" (that's Lab 04's plan, not Lab 02's). The Lab Reference lists it under 3.4 skills. |
| Combine plan + direct execution | ⚠️ GAP | The exam guide skill says: "Combining plan mode for investigation with direct execution for implementation." The lab runs them separately but never demonstrates the combined workflow. |

**Recommend:**
- Explore subagent: Add a note in Step 8.4 mentioning the Explore subagent as a related concept. Lab 04 exercises it directly, but students should know the concept here. Example: "For verbose discovery phases (e.g., exploring an unfamiliar codebase), use the Explore subagent to isolate output and return only a summary to the main conversation. Lab 04 exercises this directly."
- Plan-then-execute: Add a brief callout noting that in real projects, you often plan first (investigate the scope of a migration), then switch to direct execution to implement the planned approach.

---

## Task 3.5 — Apply iterative refinement techniques for progressive improvement

### Exam Guide says

**Knowledge:**
- Concrete input/output examples as most effective way to communicate expected transformations
- Test-driven iteration: write test suites first, iterate by sharing failures
- Interview pattern: Claude asks questions before implementing
- When to provide all issues in single message (interacting) vs sequential (independent)

**Skills:**
- Provide 2-3 concrete input/output examples for consistent results
- Write test suites covering expected behavior and edge cases before implementation
- Use interview pattern to surface considerations in unfamiliar domains
- Provide specific test cases with example input/output for edge cases
- Address multiple interacting issues in single message; iterate sequentially for independent issues

### Lab Reference
✅ All items listed.

### Lab Plan
✅ Listed as a key concept.

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Concrete input/output examples | ✅ | Step 8.3.2 — student pastes a prompt with 4 explicit examples. Step 8.4 explains the concept. |
| Vague prompt → inconsistent result | ✅ | Step 8.3.1 — student tries a vague prompt first. |
| Interview pattern | ✅ | Step 8.3.1 mentions Claude may ask clarifying questions — "this is the interview pattern." |
| Test-driven iteration | ⚠️ GAP | The exam guide says: "Test-driven iteration: writing test suites first, then iterating by sharing test failures to guide progressive improvement." **Not exercised.** The lab has `sample_app.test.py` but never asks the student to use test failures to drive iteration. |
| Interacting vs independent issues | ⚠️ GAP | The exam guide says: "Provide all interacting issues in a single message; iterate sequentially for independent issues." **Not mentioned.** |

**Recommend:**
- Test-driven iteration: This could be a meaningful exercise. The lab has `sample_app.test.py` already. A step could ask the student to add a failing test first, then paste the test failure into Claude Code and observe how it uses the failure to guide the fix. This is a natural fit after Step 8.3.
- Interacting vs independent: Add a brief note in Step 8.4. Example: "When fixing multiple interacting issues (e.g., a validation bug that causes a calculation error), provide all in one message so Claude sees the connections. For independent issues, iterate one at a time."

---

## Task 5.4 — Manage context effectively in large codebase exploration

### Exam Guide says

**Knowledge:**
- Context degradation: inconsistent answers, referencing "typical patterns" instead of discovered classes
- Scratchpad files persist key findings across context boundaries
- Subagent delegation for isolating verbose exploration output
- Structured state persistence for crash recovery: agent exports state, coordinator loads manifest on resume

**Skills:**
- Spawn subagents for specific investigation questions; main agent preserves high-level coordination
- Have agents maintain scratchpad files with key findings
- Summarize key findings from one phase before spawning sub-agents for next phase
- Design crash recovery using structured agent state exports (manifests)
- Use `/compact` to reduce context during extended exploration

### Lab Reference
✅ All items listed.

### Lab Plan
✅ "Scratchpad file pattern for context persistence across sessions."

### Actual Lab

| Item | Status | Evidence |
|------|--------|----------|
| Context degradation awareness | ✅ | Step 9.1 explains the problem. |
| Scratchpad files | ✅ | Step 9.2 — student creates `scratch.md`. Step 9.5 discusses persistence. |
| `/compact` | ✅ | Step 9.5: "Use `/compact` during extended exploration sessions." |
| Subagent delegation for exploration | ⚠️ GAP | Not exercised. (Same gap as Task 3.4 — Explore subagent.) |
| Crash recovery / structured state persistence | ⚠️ GAP | The exam guide says: "Structured state persistence for crash recovery: each agent exports state to a known location, and the coordinator loads a manifest on resume." **Not mentioned.** This is an advanced concept — more relevant to agent SDK labs, but the exam assigns it to 5.4. |
| Summarize findings before spawning sub-agents | ⚠️ GAP | Not mentioned. Related to the subagent delegation gap. |

**Recommend:**
- Subagent delegation: covered by the note recommended under Task 3.4.
- Crash recovery: Add a brief awareness note in Step 9.6. Example: "For production agent systems, design structured state persistence: each agent exports its state to a known location, and the coordinator loads a manifest on resume. The scratchpad pattern here is the simplest form of this concept."
- Summarize before spawning: Covered implicitly by the Explore subagent note.

---

## Summary of Gaps

### Gaps in the Lab Reference
None found. The Lab Reference accurately maps all knowledge and skills from the exam guide for each task assigned to Lab 02. The gap note for Task 1.7 is still valid and addressed.

### Gaps in the Lab Plan

| Gap | Severity | Details |
|-----|----------|---------|
| No mention of `/memory` command (3.1) | Low | Plan mentions hierarchy but not the diagnostic command |
| No mention of Explore subagent (3.4) | Low | Plan mentions plan mode but not the Explore subagent (which is listed in the exam guide under 3.4) |
| No mention of test-driven iteration (3.5) | Medium | Plan mentions iterative refinement but not the test-first pattern, which is a distinct exam concept |
| No mention of crash recovery state persistence (5.4) | Low | Plan mentions scratchpad but not the structured manifest pattern |

### Gaps in the Actual Lab (README + code)

| # | Task | Gap | Severity | Fix Effort |
|---|------|-----|----------|------------|
| 1 | 1.7 | Fork session is conceptual only — no hands-on exercise | Medium | Medium — add a guided fork exercise |
| 2 | 1.7 | Named sessions not taught (`--resume <session-name>`) | Medium | Low — add naming instruction |
| 3 | 1.7 | No exercise to compare two approaches from shared baseline | Medium | Medium — part of fixing gap 1 |
| 4 | 2.4 | MCP tool descriptions competing with built-in tools not mentioned | Low | Low — add a note |
| 5 | 3.1 | `/memory` command not mentioned | Low | Low — add a note |
| 6 | 3.2 | Skills vs CLAUDE.md decision criteria not discussed | Low | Low — add a note |
| 7 | 3.4 | Explore subagent not mentioned | Low | Low — add a note referencing Lab 04 |
| 8 | 3.4 | Plan-then-execute combined workflow not demonstrated | Low | Low — add a note |
| 9 | 3.5 | Test-driven iteration not exercised | Medium | Medium — add a step using test failures |
| 10 | 3.5 | Interacting vs independent issues not mentioned | Low | Low — add a note |
| 11 | 5.4 | Crash recovery / structured state persistence not mentioned | Low | Low — add a note |

### Priority Recommendation

**Quick wins (notes/callouts, no workflow changes):** Gaps 4, 5, 6, 7, 8, 10, 11
These can all be addressed by adding brief notes to existing exam concept sections. No code or workflow changes required.

**Medium effort (new or expanded steps):** Gaps 1, 2, 3, 9

- **Gaps 1-3 (fork exercise):** Expand Step 9.4 from conceptual documentation to a hands-on exercise. Have the student fork the session from Step 9.3, try one refactoring approach in the fork, then resume the original session and try a different approach. Add session naming to Step 9.2. This is the most important fix — the Lab Plan explicitly promises this exercise.
- **Gap 9 (test-driven iteration):** Add a sub-step after 8.3. Have the student add a failing test to `sample_app.test.py`, run it, paste the failure into Claude Code, and observe how the failure guides the fix. The test file already exists — minimal setup needed.

---

*Analysis performed 2026-03-29 — Alfredo De Regil*
