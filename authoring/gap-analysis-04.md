# Lab 04 — Pre-Build Gap Analysis

Comparison of the Exam Guide and Lab Reference against the Lab Plan for Scenario 4 — **before the lab is built**. The third layer (Actual Lab) will be analyzed after construction.

**Tasks covered by Lab 04:** 1.3, 2.1, 2.4, 2.5, 3.1, 3.2, 3.4, 5.4

---

## Task 1.3 — Configure subagent invocation, context passing, and spawning

### Exam Guide says

**Knowledge:**
- The Task/Agent tool as the mechanism for spawning subagents; `allowedTools` must include `"Task"`/`"Agent"`
- Subagent context must be explicitly provided — no automatic parent context inheritance
- `AgentDefinition`: descriptions, system prompts, tool restrictions per subagent type
- Fork-based session management for divergent approaches from a shared analysis baseline

**Skills:**
- Include complete prior findings directly in subagent prompt (e.g., passing search results to synthesis)
- Use structured data formats to separate content from metadata (source URLs, page numbers)
- Spawn parallel subagents via multiple Agent tool calls in a single coordinator response
- Design coordinator prompts with goals and quality criteria, not step-by-step procedures

### Lab Reference
✅ All knowledge and skills listed. Notes both `"Task"` and `"Agent"` names. Includes fork-based session management.

### Lab Plan
⚠️ PARTIAL — The plan says the lab uses an "Explore subagent for verbose discovery" and delegates to a subagent, but:

| Item | Status | Detail |
|------|--------|--------|
| Agent tool as spawning mechanism | ✅ | Plan mentions "Explore subagent" — implies Agent tool usage. |
| Explicit context passing (no inheritance) | ⚠️ GAP | Not explicitly called out. The plan says "Explore subagent: isolates verbose discovery, returns summary to main agent" but doesn't mention that the student must explicitly pass context in the subagent prompt. |
| `AgentDefinition` configuration | ⚠️ GAP | Plan doesn't mention defining `AgentDefinition` with descriptions, system prompts, or tool restrictions. It only says "Explore subagent" generically. |
| Fork-based session management | ❌ MISSING | Not mentioned in the Lab 04 plan at all. The reference maps this to L3/L4, but the plan only covers Explore subagent, not fork_session. |
| Complete findings in subagent prompt | ⚠️ GAP | Not explicit. The plan focuses on the Explore subagent returning results, not on passing prior findings *into* the subagent. |
| Structured data separating content from metadata | ❌ MISSING | Not mentioned. |
| Parallel subagent spawning | ❌ MISSING | Plan only mentions one Explore subagent. No parallel spawning exercise. |
| Coordinator prompts with goals vs procedures | ⚠️ GAP | Not explicit in the plan. |

**Recommend:**
- Add an exercise where the student defines an `AgentDefinition` with a description, system prompt, and `allowedTools` restriction for the Explore subagent.
- Add explicit context passing: show the student the subagent's prompt and highlight that it must contain all needed context.
- Parallel spawning and fork_session are better covered in L3 (parallel) and L2 (fork). Confirm these are the primary homes, and L4 plays a secondary role for 1.3.

---

## Task 2.1 — Design effective tool interfaces with clear descriptions and boundaries

### Exam Guide says

**Knowledge:**
- Tool descriptions are the primary mechanism LLMs use for tool selection
- Descriptions must include: input formats, example queries, edge cases, boundaries vs similar tools
- Ambiguous/overlapping descriptions cause misrouting (e.g., `analyze_content` vs `analyze_document`)
- System prompt wording can create unintended tool associations

**Skills:**
- Write descriptions that differentiate each tool's purpose, inputs, outputs, and when to use vs alternatives
- Rename tools to eliminate functional overlap
- Split generic tools into purpose-specific tools with defined input/output contracts
- Review system prompts for keyword-sensitive instructions that override tool descriptions

### Lab Reference
✅ All items present. Maps to L1, L3, L4.

### Lab Plan
⚠️ PARTIAL — The plan focuses on built-in tool selection (Grep vs Glob) and MCP tool descriptions, but:

| Item | Status | Detail |
|------|--------|--------|
| Tool descriptions as primary selection mechanism | ✅ | Implicitly covered — plan mentions "MCP server config" and built-in tool selection. |
| Rich descriptions (input formats, edge cases, boundaries) | ⚠️ GAP | Plan mentions "Grep (content search) vs Glob (file path patterns)" which is tool *selection*, not tool *description design*. No exercise where the student writes or improves a tool description. |
| Ambiguous/overlapping descriptions cause misrouting | ❌ MISSING | No exercise demonstrating misrouting or fixing overlapping descriptions. |
| System prompt keyword-sensitive wording | ❌ MISSING | Not mentioned. |
| Rename tools to eliminate overlap | ❌ MISSING | Not mentioned. |
| Split generic tools into purpose-specific tools | ❌ MISSING | Not mentioned. |

**Recommend:**
- This task is primarily exercised in L1 (tool definitions) and L3 (multi-agent tool routing). L4's contribution should focus on the **MCP tool description** angle: the student configures an MCP server and then enhances its tool description so the agent prefers it over a built-in tool. This would naturally cover "descriptions that differentiate" and "descriptions that outcompete built-in tools" (which overlaps with Task 2.4).
- Keep L1/L3 as the primary homes for misrouting, renaming, and splitting exercises.

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
✅ All items present. Maps to L4 (primary) and L2 (secondary).

### Lab Plan
✅ WELL COVERED — Plan explicitly lists:
- "MCP server config in `.mcp.json` with `${ENV_VAR}` expansion for credentials"
- "Project-level vs user-level MCP server scoping"
- File structure includes `mcp_config/.mcp.json`

| Item | Status | Detail |
|------|--------|--------|
| `.mcp.json` with env var expansion | ✅ | Explicitly in plan. |
| Project-level vs user-level scoping | ✅ | Explicitly in plan. |
| Tools discovered at connection time | ⚠️ GAP | Not called out. Should be mentioned in README as an exam concept. |
| MCP resources for content catalogs | ❌ MISSING | Plan doesn't mention MCP resources at all. |
| Enhance MCP tool descriptions to outcompete built-in | ⚠️ GAP | Not explicit, but could be woven into the MCP config step. |
| Community MCP servers over custom for standard integrations | ❌ MISSING | Not mentioned. |

**Recommend:**
- Add an MCP resources exercise or at minimum a README callout explaining the concept and when to use it.
- Add a step where the student enhances an MCP tool description so the agent prefers it over a built-in tool (ties to Task 2.1 as well).
- Add a README note about choosing community MCP servers for standard integrations (Jira, GitHub, etc.) vs building custom.

---

## Task 2.5 — Select and apply built-in tools effectively

### Exam Guide says

**Knowledge:**
- Grep = content search (file contents for patterns); Glob = file path pattern matching
- Edit for targeted changes using unique text; Read + Write as fallback when anchor text is non-unique
- When Edit fails due to non-unique text matches, use Read + Write

**Skills:**
- Select Grep for searching code content; Glob for finding files by naming pattern
- Use Read + Write when Edit cannot find unique anchor text
- Build codebase understanding incrementally: Grep entry points → Read imports → trace flows
- Trace function usage: identify all exported names, then search each across codebase

### Lab Reference
✅ All items present. Maps to L4 (primary).

### Lab Plan
✅ WELL COVERED — This is the core of the lab. Plan explicitly lists:
- "Grep (content search) vs Glob (file path patterns)"
- "Edit fallback: when anchor text is non-unique, use Read + Write instead"
- "Incremental codebase understanding: Grep entry points → Read imports → trace flows"

| Item | Status | Detail |
|------|--------|--------|
| Grep vs Glob selection | ✅ | Core of the lab. "What to observe" items 1-2 directly test this. |
| Edit → Read + Write fallback | ✅ | "What to observe" item 3 directly tests this. |
| Incremental codebase understanding | ✅ | Listed in key concepts. |
| Trace function usage across wrapper modules | ⚠️ GAP | Not explicitly exercised. Plan mentions incremental understanding but not the specific "identify exported names → search each" pattern. |

**Recommend:**
- Add a step or sub-step where the student asks the agent to trace all usages of a function that's re-exported through a wrapper module, demonstrating the "identify exports → search each" pattern.

---

## Task 3.1 — Configure CLAUDE.md hierarchy, scoping, and modular organization

### Exam Guide says

**Knowledge:**
- Hierarchy: user-level (`~/.claude/CLAUDE.md`), project-level (`.claude/CLAUDE.md`), directory-level
- User-level settings not shared via version control
- `@import` syntax for referencing external files
- `.claude/rules/` directory as alternative to monolithic CLAUDE.md

**Skills:**
- Diagnose hierarchy issues (e.g., new team member missing instructions)
- Use `@import` to include relevant standards files per package
- Split large CLAUDE.md into topic files in `.claude/rules/`
- Use `/memory` to verify loaded files and diagnose inconsistent behavior

### Lab Reference
✅ All items present. Maps to L2 (primary), L4 (secondary).

### Lab Plan
⚠️ MINIMAL — Plan does not mention CLAUDE.md configuration at all for Lab 04. The only reference is in the task coverage table (tasks 3.1 listed).

| Item | Status | Detail |
|------|--------|--------|
| CLAUDE.md hierarchy | ❌ MISSING | Not in plan's key concepts or files section. |
| `@import` syntax | ❌ MISSING | Not mentioned. |
| `.claude/rules/` | ❌ MISSING | Not mentioned. |
| `/memory` command | ❌ MISSING | Not mentioned. |
| Hierarchy diagnosis | ❌ MISSING | Not mentioned. |

**Recommend:**
- L2 is the primary home for CLAUDE.md configuration (7 out of 8 L2 tasks are D3). L4's role should be secondary: the lab already has a `CLAUDE.md` in the lab folder. Add a brief step or note showing the student how the lab-level CLAUDE.md fits into the hierarchy, and optionally use `@import` to pull in a coding convention file. This gives L4 a light touch on 3.1 without duplicating L2.
- Alternatively, if L2 fully covers 3.1, remove 3.1 from L4's task list in the reference to avoid confusion.

---

## Task 3.2 — Create and configure custom slash commands and skills

### Exam Guide says

**Knowledge:**
- Project-scoped `.claude/commands/` (version controlled) vs personal `~/.claude/commands/`
- `SKILL.md` frontmatter: `context:fork`, `allowed-tools`, `argument-hint`
- `context:fork` runs skill in isolated sub-agent
- Personal skill customization in `~/.claude/skills/`

**Skills:**
- Create project-scoped slash commands for team-wide availability
- Use `context:fork` to isolate verbose skill output
- Configure `allowed-tools` to restrict tool access during skill execution
- Use `argument-hint` to prompt for required parameters
- Choose between skills (on-demand) and CLAUDE.md (always-loaded)

### Lab Reference
✅ All items present. Maps to L2 (primary), L4 (secondary).

### Lab Plan
⚠️ MINIMAL — Plan mentions "custom slash command" in the build description but provides no detail.

| Item | Status | Detail |
|------|--------|--------|
| Project-scoped slash command | ✅ | Plan mentions "custom slash command" generically. |
| `SKILL.md` with frontmatter | ⚠️ GAP | Not specified. Plan says "custom slash command" but doesn't distinguish command vs skill or mention SKILL.md. |
| `context:fork` | ❌ MISSING | Not mentioned in L4 plan. |
| `allowed-tools` | ❌ MISSING | Not mentioned. |
| `argument-hint` | ❌ MISSING | Not mentioned. |
| Skills vs CLAUDE.md choice | ❌ MISSING | Not mentioned. |

**Recommend:**
- L2 is the primary home for skills (including `context:fork`, `allowed-tools`). L4 should add a focused slash command or skill that's relevant to the developer productivity scenario — e.g., a `/explore` command that runs codebase analysis with `context:fork` to keep verbose output isolated. This naturally ties to the Explore subagent pattern (Task 5.4) and demonstrates `context:fork` in a practical context.
- Don't duplicate L2's full coverage of all frontmatter options. Focus on one or two that fit the scenario.

---

## Task 3.4 — Determine when to use plan mode vs direct execution

### Exam Guide says

**Knowledge:**
- Plan mode for large-scale changes, multiple approaches, architectural decisions, multi-file edits
- Direct execution for simple, well-scoped single-file changes
- Plan mode enables safe exploration before committing to changes
- Explore subagent for isolating verbose discovery output

**Skills:**
- Select plan mode for architectural tasks (microservice restructuring, 45+ file migrations)
- Select direct execution for single-file bug fix with clear stack trace
- Use Explore subagent for verbose discovery to prevent context window exhaustion
- Combine plan mode for investigation with direct execution for implementation

### Lab Reference
✅ All items present. Maps to L2 (primary), L4 (secondary), L5 (secondary).

### Lab Plan
✅ PARTIAL — The plan mentions the Explore subagent but doesn't explicitly cover plan mode vs direct execution:

| Item | Status | Detail |
|------|--------|--------|
| Plan mode for large-scale changes | ❌ MISSING | Not in plan's key concepts. |
| Direct execution for simple changes | ❌ MISSING | Not mentioned. |
| Explore subagent isolation | ✅ | "Explore subagent: isolates verbose discovery, returns summary to main agent" — core of the lab. |
| Combine plan + direct execution | ❌ MISSING | Not mentioned. |
| When to choose plan vs direct | ❌ MISSING | No comparison exercise. |

**Recommend:**
- L2 is the primary home for the plan mode vs direct execution comparison. L4's main contribution is the **Explore subagent** — which is the D3.4 concept that naturally lives here. Add a README note connecting the Explore subagent pattern to plan mode: "The Explore subagent serves the same purpose as plan mode's discovery phase — isolating verbose exploration from the action context."
- Optionally, add a brief exercise: have the student try a large-scope question (use plan mode), then a small-scope question (direct execution), and observe the difference. But this is secondary to L2's coverage.

---

## Task 5.4 — Manage context effectively in large codebase exploration

### Exam Guide says

**Knowledge:**
- Context degradation: inconsistent answers, references to "typical patterns" instead of discovered classes
- Scratchpad files for persisting key findings across context boundaries
- Subagent delegation for isolating verbose exploration output
- Structured state persistence for crash recovery: agent exports state, coordinator loads manifest on resume

**Skills:**
- Spawn subagents for specific investigation questions; main agent preserves high-level coordination
- Agents maintain scratchpad files recording key findings
- Summarize key findings from one phase before spawning sub-agents for the next
- Design crash recovery using structured agent state exports (manifests)
- Use `/compact` to reduce context usage during extended sessions

### Lab Reference
✅ All items present. Maps to L4 (primary), L2 (secondary).

### Lab Plan
✅ WELL COVERED — Core of the lab. Plan explicitly lists:
- "Explore subagent: isolates verbose discovery, returns summary to main agent"
- "Scratchpad file: agent writes findings to `scratch.md`, reads it on next question (D5.4)"

| Item | Status | Detail |
|------|--------|--------|
| Context degradation awareness | ⚠️ GAP | Not explicitly addressed. Plan should include a step showing degradation (e.g., asking the agent many questions until it starts losing context). |
| Scratchpad files | ✅ | "What to observe" item 5 directly tests this. |
| Subagent delegation | ✅ | Explore subagent is core to the lab. |
| Structured state persistence / crash recovery | ❌ MISSING | Plan doesn't mention manifests or crash recovery. |
| Summarize findings before next phase | ⚠️ GAP | Implicit in Explore subagent pattern but not explicitly exercised. |
| `/compact` command | ❌ MISSING | Not mentioned. |

**Recommend:**
- Add a README note about context degradation symptoms and when the student should notice them.
- Add a step or note about `/compact` — even a brief "if your context fills up, use `/compact` to summarize and continue."
- Crash recovery (manifests) is an advanced concept. Add a README "Also know for the exam" callout explaining the pattern without requiring a hands-on exercise.

---

## Summary

### Layer 1: Lab Reference → Exam Guide

The Lab Reference accurately maps all 8 task statements to Lab 04. No missing task mappings.

| Rating | Count | Detail |
|--------|-------|--------|
| ✅ Well mapped | 8/8 | All tasks listed with correct knowledge and skills |
| ⚠️ Gaps | 0 | — |
| ❌ Missing | 0 | — |

### Layer 2: Lab Plan → Lab Reference + Exam Guide

| Task | Plan Coverage | Key Gaps |
|------|--------------|----------|
| 1.3 | ⚠️ Partial | No `AgentDefinition`, no explicit context passing, no parallel spawning, no fork_session |
| 2.1 | ⚠️ Partial | Covers tool selection but not tool description design, misrouting, or renaming |
| 2.4 | ✅ Good | Missing MCP resources and description enhancement |
| 2.5 | ✅ Good | Missing function usage tracing pattern |
| 3.1 | ❌ Missing | No CLAUDE.md hierarchy exercises |
| 3.2 | ⚠️ Partial | Mentions "custom slash command" but no detail on skills/frontmatter |
| 3.4 | ⚠️ Partial | Covers Explore subagent but not plan mode vs direct execution comparison |
| 5.4 | ✅ Good | Missing context degradation awareness, crash recovery, `/compact` |

### Top Recommendations (prioritized for lab builder)

1. **Define an `AgentDefinition` exercise** — The student should configure at least one `AgentDefinition` with description, system prompt, and `allowedTools`. This is the natural home for 1.3 in a developer productivity context.

2. **Add MCP tool description enhancement step** — After configuring the MCP server in `.mcp.json`, have the student improve the tool description so the agent prefers it over a built-in tool. Covers both 2.1 and 2.4.

3. **Add an MCP resources callout** — Even if not hands-on, the README should explain MCP resources as content catalogs (2.4 knowledge).

4. **Light CLAUDE.md hierarchy touch** — Add a step showing `@import` or `.claude/rules/` in the lab's own `CLAUDE.md`, or add an "Also know for the exam" note. Don't duplicate L2's full coverage.

5. **Create a meaningful slash command/skill** — e.g., `/explore` with `context:fork` that runs codebase analysis. Ties 3.2 to 5.4 naturally.

6. **Add a `/compact` callout** — Brief note in the README about when to use it (5.4).

7. **Add exam concept notes for items not exercised hands-on** — Crash recovery manifests (5.4), community MCP servers (2.4), parallel subagent spawning (1.3). Use "Also know for the exam" blockquotes.

8. **Function usage tracing exercise** — Add a step where the agent traces a re-exported function across wrapper modules (2.5).

---

*Pre-build analysis — 3/29/2026*
