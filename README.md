# Claude Certified Architect — Foundations

Hands-on lab preparation for the CCA Foundations certification exam.
Six scenario-based labs covering all 5 exam domains and 27 task statements.

## Labs

| # | Lab | Domains |
|---|-----|---------|
| 01 | Customer Support Resolution Agent | D1 · D2 · D5 |
| 02 | Code Generation Workflows | D3 · D5 |
| 03 | Multi-Agent Research System | D1 · D2 · D5 |
| 04 | Developer Productivity Agent | D1 · D2 · D3 |
| 05 | CI/CD Integration | D3 · D4 |
| 06 | Structured Data Extraction | D4 · D5 |

Each lab is self-contained. Start any lab in any order.

## How to start a lab

```bash
cd 0X_lab_name
cp .env.example .env        # add your ANTHROPIC_API_KEY
pip install -r requirements.txt
python main.py              # run the lab
python reset.py             # reset state and try again
```

## Exam domains

- **D1** Agentic Architecture & Orchestration (27%)
- **D2** Tool Design & MCP Integration (18%)
- **D3** Claude Code Configuration & Workflows (20%)
- **D4** Prompt Engineering & Structured Output (20%)
- **D5** Context Management & Reliability (15%)

---

*v0.1 — 3/15/2026 — Alfredo de Regil*
