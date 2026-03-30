# Lab Reference

This document describes the domains and tasks covered by each lab, including the specific Knowledge and Skills tested on the exam.

The official exam guide defines 6 scenarios that frame the exam questions and each lab here maps directly to one of them. All 5 domains and all 30 tasks are covered.

### Platforms

The exam covers three platforms for building with Claude. Each lab is implemented using one of them:

| Platform | Package | Labs |
|----------|---------|------|
| [Claude API](https://platform.claude.com/docs/en/api/client-sdks) | `pip install anthropic` | L1, L6 |
| [Claude Agent SDK](https://code.claude.com/docs/en/sdk) | `pip install claude-agent-sdk` | L3, L4 |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | CLI tool | L2, L5 |

---

### Lab 01 | [Customer Support Resolution Agent](01_customer_support_agent/)
![D1](https://img.shields.io/badge/D1-Agentic%20Architecture-purple) ![D2](https://img.shields.io/badge/D2-Tool%20Design-purple) ![D5](https://img.shields.io/badge/D5-Context%20Management-purple)

Build a customer support agent with four MCP-style tools, an agentic loop driven by `stop_reason`, a programmatic prerequisite gate, and a PostToolUse hook that enforces refund policy. By the end you will have a working agent that handles real-feeling customer conversations: looking up accounts, processing refunds, and escalating when appropriate.

| Domain | Task | Statement |
|:------:|:----:|-----------|
| D1 | 1.1 | Design and implement agentic loops |
| D1 | 1.2 | Orchestrate multi-agent systems with coordinator-subagent patterns |
| D1 | 1.4 | Implement multi-step workflows with enforcement and handoff patterns |
| D1 | 1.5 | Apply Agent SDK hooks for tool call interception and data normalization |
| D2 | 2.1 | Design effective tool interfaces with clear descriptions and boundaries |
| D2 | 2.2 | Implement structured error responses for MCP tools |
| D2 | 2.3 | Distribute tools across agents and configure tool choice |
| D5 | 5.1 | Manage conversation context across long interactions |
| D5 | 5.2 | Design escalation and ambiguity resolution patterns |

---

### Lab 02 | [Code Generation with Claude Code](02_code_generation_workflows/)
![D3](https://img.shields.io/badge/D3-Claude%20Code%20Config-purple) ![D5](https://img.shields.io/badge/D5-Context%20Management-purple)

Configure a Claude Code workspace from scratch: build a CLAUDE.md hierarchy with `@import`, create path-specific rules for different file types, set up a custom skill with `context:fork` isolation, configure MCP servers, and manage sessions across boundaries with resume and fork. By the end you will have a fully configured workspace where Claude Code understands your project conventions, applies the right rules to the right files, and can maintain context across sessions.

| Domain | Task | Statement |
|:------:|:----:|-----------|
| D1 | 1.7 | Manage session state, resumption, and forking |
| D2 | 2.4 | Integrate MCP servers into Claude Code and agent workflows |
| D3 | 3.1 | Configure CLAUDE.md hierarchy, scoping, and modular organization |
| D3 | 3.2 | Create and configure custom slash commands and skills |
| D3 | 3.3 | Apply path-specific rules for conditional convention loading |
| D3 | 3.4 | Determine when to use plan mode vs direct execution |
| D3 | 3.5 | Apply iterative refinement techniques for progressive improvement |
| D5 | 5.4 | Manage context effectively in large codebase exploration |

---

### Lab 03 | [Multi-Agent Research System](03_multi_agent_research/)
![D1](https://img.shields.io/badge/D1-Agentic%20Architecture-purple) ![D2](https://img.shields.io/badge/D2-Tool%20Design-purple) ![D5](https://img.shields.io/badge/D5-Context%20Management-purple)

Build a multi-agent research system where a **coordinator** agent delegates to four specialized subagents (a **search-agent**, an **analysis-agent**, a **synthesis-agent**, and a **report-agent**) using the Claude Agent SDK. By the end you will have a working system that decomposes research topics, finds sources, analyzes documents, handles errors from unavailable sources, synthesizes findings into cited reports with coverage annotations, and writes the final report to a file.

| Domain | Task | Statement |
|:------:|:----:|-----------|
| D1 | 1.2 | Orchestrate multi-agent systems with coordinator-subagent patterns |
| D1 | 1.3 | Configure subagent invocation, context passing, and spawning |
| D1 | 1.5 | Apply Agent SDK hooks for tool call interception and data normalization |
| D1 | 1.6 | Design task decomposition strategies for complex workflows |
| D2 | 2.1 | Design effective tool interfaces with clear descriptions and boundaries |
| D2 | 2.2 | Implement structured error responses for MCP tools |
| D2 | 2.3 | Distribute tools across agents and configure tool choice |
| D5 | 5.1 | Manage conversation context across long interactions |
| D5 | 5.3 | Implement error propagation across multi-agent systems |
| D5 | 5.6 | Preserve information provenance in multi-source synthesis |

---

### Lab 04 | [Developer Productivity with Claude](04_developer_productivity/)
![D1](https://img.shields.io/badge/D1-Agentic%20Architecture-purple) ![D2](https://img.shields.io/badge/D2-Tool%20Design-purple) ![D3](https://img.shields.io/badge/D3-Claude%20Code%20Config-purple) ![D5](https://img.shields.io/badge/D5-Context%20Management-purple)

Build a developer productivity agent that explores an unfamiliar Python codebase using the Claude Agent SDK. You start with built-in tools (`Grep`, `Glob`, `Read`), add an MCP documentation server, delegate deep exploration to an `AgentDefinition` subagent, persist findings to a scratchpad file, and package the result as a Claude Code skill. By the end you will have a working agent that understands a codebase, remembers what it discovers, and delegates deep investigation to isolated subagents.

| Domain | Task | Statement |
|:------:|:----:|-----------|
| D1 | 1.3 | Configure subagent invocation, context passing, and spawning |
| D2 | 2.1 | Design effective tool interfaces with clear descriptions and boundaries |
| D2 | 2.4 | Integrate MCP servers into Claude Code and agent workflows |
| D2 | 2.5 | Select and apply built-in tools effectively |
| D3 | 3.1 | Configure CLAUDE.md hierarchy, scoping, and modular organization |
| D3 | 3.2 | Create and configure custom slash commands and skills |
| D3 | 3.4 | Determine when to use plan mode vs direct execution |
| D5 | 5.4 | Manage context effectively in large codebase exploration |

---

### Lab 05 | [Claude Code for Continuous Integration](05_ci_cd_integration/)
![D3](https://img.shields.io/badge/D3-Claude%20Code%20Config-purple) ![D4](https://img.shields.io/badge/D4-Prompt%20Engineering-purple)

Build a simulated CI pipeline where Claude Code reviews pull request code in non-interactive mode. You iteratively refine the review prompt, from broad and noisy to explicit criteria to few-shot examples, observing precision improve at each step. You then split reviews into per-file and cross-file passes, add independent review instances, and configure CLAUDE.md to provide project context to CI-invoked Claude Code. By the end you will have a working CI review pipeline that produces precise, structured feedback with calibrated confidence.

| Domain | Task | Statement |
|:------:|:----:|-----------|
| D1 | 1.6 | Design task decomposition strategies for complex workflows |
| D3 | 3.4 | Determine when to use plan mode vs direct execution |
| D3 | 3.5 | Apply iterative refinement techniques for progressive improvement |
| D3 | 3.6 | Integrate Claude Code into CI/CD pipelines |
| D4 | 4.1 | Design prompts with explicit criteria to reduce false positives |
| D4 | 4.2 | Apply few-shot prompting to improve output consistency and quality |
| D4 | 4.6 | Design multi-instance and multi-pass review architectures |

---

### Lab 06 | [Structured Data Extraction](06_structured_extraction/)
![D4](https://img.shields.io/badge/D4-Prompt%20Engineering-purple) ![D5](https://img.shields.io/badge/D5-Context%20Management-purple)

Build an invoice extraction pipeline that converts unstructured documents into schema-compliant JSON using `tool_use` with forced `tool_choice`. You progressively add nullable fields, self-correction, retry with error feedback, few-shot examples, batch processing, and confidence-based human review routing. By the end you will have a working extraction system that handles missing fields, detects inconsistencies, and routes uncertain results to human review.

| Domain | Task | Statement |
|:------:|:----:|-----------|
| D4 | 4.2 | Apply few-shot prompting to improve output consistency and quality |
| D4 | 4.3 | Enforce structured output using tool use and JSON schemas |
| D4 | 4.4 | Implement validation, retry, and feedback loops for extraction quality |
| D4 | 4.5 | Design efficient batch processing strategies |
| D5 | 5.5 | Design human review workflows and confidence calibration |

---

### Coverage Summary

![Scenarios](https://img.shields.io/badge/Scenarios-6%2F6-green) ![Domains](https://img.shields.io/badge/Domains-5%2F5-green) ![Tasks](https://img.shields.io/badge/Tasks-30%2F30-green)

---

## Disclaimer

This is an independent resource, not produced, endorsed, or affiliated with Anthropic.

[![License](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey)](LICENSE)
