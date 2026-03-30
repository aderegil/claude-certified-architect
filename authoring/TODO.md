# CCA Labs — Outstanding Work

Tracked items for after all 6 labs are built.

---

## Lab 01 — Customer Support Resolution Agent

- [ ] Migrate from Claude API (Client SDK) to Claude Agent SDK — exam guide says S1 uses Agent SDK, but Lab 01 was built with `import anthropic` and manual agentic loops
- [ ] Backfill Lab Plan with detailed format: narrative arc, key concepts with `[Task X.Y]` tags, detailed file tree, specific "What to observe" items

## Lab 02 — Code Generation Workflows

- [ ] Apply 11 gaps from `gap-analysis-02.md` — fixes NOT applied yet
  - [ ] Make fork_session exercise hands-on (student actually runs a fork, compares two approaches)
  - [ ] Teach session naming (`--resume <session-name>`, not just `claude --resume`)
  - [ ] Add MCP resources callout (content catalogs)
  - [ ] Add community MCP servers note
  - [ ] Add enhanced MCP tool description exercise or note
  - [ ] Add `context:fork` hands-on exercise (student runs the skill, not just reads about it)
  - [ ] Add `argument-hint` to the skill exercise
  - [ ] Add plan mode + direct execution comparison exercise
  - [ ] Add concrete input/output examples for iterative refinement
  - [ ] Add test-driven iteration exercise
  - [ ] Add `/compact` usage note for extended sessions
- [ ] Backfill Lab Plan with detailed format (same as Lab 01)

## Lab 03 — Multi-Agent Research System

- [ ] Backfill Lab Plan with detailed format (same as Lab 01)

## Labs 01, 02, 03 — Add _starter/ directories

- [ ] Consider adding `_starter/` folders with `build_reset.py` to labs 1-3 (Labs 4 and 5 already have them). Low priority — mainly useful during active debugging, so may not be worth it for labs that are already stable.

## Labs 03, 04 — Rich Markdown Rendering

- [ ] Use `rich` to render heavy markdown output (research reports, exploration summaries) instead of raw ANSI — applies to labs that produce structured markdown from the agent
- [ ] Pattern: `from rich.markdown import Markdown` + `from rich.console import Console` → `console.print(Markdown(text))`
- [ ] Add `rich` to `requirements.txt` for affected labs
- [ ] Update `AUTHOR.md` console output conventions to document when to use `rich` vs ANSI codes

## All Labs — Rich Spinner for Wait States

- [ ] Add a `rich` spinner (e.g., `console.status("Reviewing files...")`) in labs where the user should just wait while the agent works — gives visual feedback instead of a frozen terminal
- [ ] Applies to any lab step that calls Claude API / Claude Code and blocks for multiple seconds

## All Labs — Startup Banner

- [ ] Add a one-line description below the app title on launch — e.g., `Customer Support Agent — resolves billing disputes, returns, and account issues via MCP tools`
- [ ] Gives the student immediate context of what the running app does without reading the README

## All Labs — Consistency Pass

- [ ] Consolidate setup into Step 0 — all pre-execution tasks (open lab folder, create venv, configure `.env`, `pip install`, launch Claude Code) should be a single Step 0, not spread across Steps 0-3
- [ ] Update `CCA_Lab_Plan.md` README template to reflect the consolidated Step 0 convention
- [ ] Update `AUTHOR.md` README structure section to match

## All Labs — Realistic Timing Pass

- [ ] Run each lab end-to-end as a typical student and record actual elapsed time per step
- [ ] Update Lab Plan estimated times to reflect real measurements (current estimates are guesses)
- [ ] Flag any lab that exceeds a reasonable session length and identify steps to trim or split

## Lab Plan — General

- [ ] Update `CCA_Lab_Reference.docx` to match the `.md` (single pass after all labs built)

---

*Created 3/29/2026*
