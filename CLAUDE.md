# CLAUDE.md — CRUX project context for Claude (and other CLAUDE.md-aware assistants)

> This file mirrors [`AGENTS.md`](./AGENTS.md) but is named so that Claude Code, Cursor, and other Anthropic-aligned tooling auto-load it as project context. **Keep both files in sync** when refining; treat AGENTS.md as the canonical version and regenerate this one from it whenever the structure changes substantively.

---

## TL;DR for an assistant new to this repo

CRUX is a **solo, 48-hour, hackathon submission** for IBM Bob Dev Day. It is a Bob-driven agent that converts a messy Jupyter notebook into a production-ready FastAPI service plus a 15-gap audit dossier and a structured decision log, all reachable as MCP tools. The submission is judged on a **5-minute live demo**, so every architectural decision is biased toward demo clarity over engineering elegance.

If you, the assistant, are reading this without other context: read [`README.md`](./README.md) first, then [`SPECS.md`](./SPECS.md) for the cell-classification taxonomy and the 15-gap list, then [`PHASES.md`](./PHASES.md) for the hour-by-hour build order. Skip the rest unless asked.

---

## What CRUX does in three steps

1. **Narrative intent recovery** — read the notebook as a *document* (execution counts + markdown narrative + variable lineage), classify each cell as load-bearing / exploratory / dead / scaffolding, emit a clean `recovered_pipeline.py` containing only the load-bearing cells stitched in dataflow order.
2. **15-gap production-readiness audit** — run a fixed, severity-ranked checklist of fifteen gaps (input validation, train/serve skew, no logging, no model versioning, hardcoded secrets, no tests, no Dockerfile, …); autopatch the safe ones; surface the rest as a structured decision log with options A/B/C.
3. **MCP server** — every capability above is also a tool over MCP (`audit_notebook`, `get_dossier`, `list_open_decisions`, `compare_notebooks`, `block_merge_if_critical_gaps`). A real GitHub Actions job calls it to refuse merges with unresolved critical gaps.

The differentiator vs. existing notebook-to-script tools (`nbconvert`, Jupytext, paid platforms): those treat a notebook as a flat list of cells and convert all of them. CRUX reads the notebook as a narrative artifact and recovers only what was meant to ship.

---

## Behavioral defaults the assistant should adopt

### Be biased toward the demo
Every artifact CRUX generates has to look good when a judge reads it for ten seconds. Whenever there's a tension between engineering elegance and demo clarity, **pick demo clarity**. That means:
- Audit dossiers use ✅/⚠️/❌ at the top of each section so a judge can scan in five seconds
- Decision logs label options literally **A / B / C** with one-sentence trade-offs each
- The recovered pipeline is heavily commented even when the comments restate obvious things — judges read code differently from engineers

### Be conservative with Bobcoins / API spend
The user has a 40-Bobcoin budget for the entire build. If a request is ambiguous, ask one short clarifying question rather than producing a speculative draft. Don't volunteer refactors. Don't add dependencies without checking the license.

### Hard rules
- Never modify `samples/`. Read-only.
- Never push to `main`. Always feature branches.
- Never add a non-permissive dependency (Apache 2.0 / MIT / BSD only — submission is public).
- Never train a custom model. Heuristics + Bob's reasoning are sufficient. The stakeholder summary in the dossier is rendered from a deterministic Jinja2 template (`templates/stakeholder_summary.md.j2`) — no LLM call at audit time.
- Never paste long source code from third-party docs into committed files. Cite + paraphrase + adapt.

### Code style
- Python 3.11+, `uv` not `pip`, type hints on public functions, Pydantic v2 for data, `structlog` for logs, `ruff` for lint, `pytest` for tests
- Comment the *why*, not the *what*. Especially around the heuristic weights in `skills/notebook-narrative/` — those weights are tuned, not principled
- snake_case filenames. No spaces, no hyphens

---

## Repo layout (where things live)

| Path | Purpose |
|---|---|
| `README.md`, `SPECS.md`, `SYSTEM_DESIGN.md`, `ARCHITECTURE.md`, `WORKFLOW_DIAGRAM.md` | Planning + spec docs |
| `PHASES.md`, `BOBCOIN_BUDGET.md`, `JUDGING_PLAYBOOK.md`, `DEMO_SCRIPT.md` | Hackathon execution docs |
| `MCP_SETUP.md`, `TECH_STACK.md` | Wiring + dependency docs |
| `AGENTS.md`, `CLAUDE.md` | Persistent agent context (you're reading one) |
| `.bob/modes/crux-mode.md` | Custom Bob mode for end-to-end runs |
| `.bob/rules/*.md` | Project-level Bob behavior rules |
| `skills/notebook-narrative/` | Intent-recovery skill + helpers (`parse_notebook.py`, `lineage_graph.py`) |
| `skills/production-audit/` | Audit skill + 15 gap detectors + autopatch templates |
| `mcp_server/server.py` | FastMCP entrypoint (~200 LOC; the LOC count is part of the pitch) |
| `mcp_server/tools.py` | The five MCP tools |
| `samples/01_clean.ipynb`, `02_messy.ipynb`, `03_chaos.ipynb` | Demo inputs, increasing in mess |
| `out/<stem>/` | Per-notebook generated artifacts |
| `tests/` | pytest parity tests |
| `ci/block-on-gaps.yml` | GitHub Actions workflow that calls the MCP server |
| `bob_sessions/` | **Required for hackathon judging** — screenshots + markdown exports |
| `internal-monologue/` | Per-task notes Bob writes after non-trivial work |

---

## Common asks (canonical responses)

- **"Help me start"** → point at `PHASES.md` Hours 0–3 block. Don't generate code yet.
- **"Recover intent from a notebook"** → invoke the `notebook-narrative` skill on the specific path; produce `recovered_pipeline.py` + `intent_report.md` only; **stop before audit**.
- **"Audit the recovered pipeline"** → invoke `production-audit`; produce `audit_dossier.md`, `decision_log.md`, autopatched files, and parity tests; run tests; report pass/fail.
- **"Wire the MCP server into Bob"** → see `MCP_SETUP.md` § "Bob IDE mcp.json registration"; do not edit Bob's global config without asking.
- **"What should I cut if I'm behind?"** → cut order is: sample `03_chaos` → polish on sample `02` → bottom 5 gap autopatches (detect-only). Never cut the MCP server, the dossier, or `bob_sessions/`. (The watsonx.ai/Granite capstone is already out of scope — the stakeholder summary uses a deterministic Jinja2 template.)

---

## Internal-monologue convention

After any multi-step task that touched code, write a short bullet note to `internal-monologue/<YYYY-MM-DD>-<slug>.md`: what was attempted, what worked, what didn't, what to try next. This survives context-window resets and gives the user an audit trail to send to judges. Keep these terse — bullets, not essays.

---

## Things that look obvious but aren't

- **The intent_report.md is part of the demo.** It's not a debug log. It must be readable by a senior engineer in 30 seconds. Use a table for cell classifications.
- **The audit dossier is part of the demo.** It must look like the output of a senior consultant's week-three review, not a linter. Group by severity, lead each gap with a one-sentence summary, then the patch (or the decision options).
- **The MCP server's tool signatures matter for the demo.** They appear on screen during the live MCP-Inspector segment of the pitch. Naming should be obviously load-bearing: `block_merge_if_critical_gaps()` is better than `check_status()`.

---

## Honest expectations for the assistant to internalize

This is a strong solo submission, not a guaranteed win. The factors that actually decide the outcome, in order of weight:
1. How cleanly the live demo runs
2. How tight the README is for a 60-second skim
3. Whether the `bob_sessions/` folder is correctly populated
4. How clearly the three focus areas (AI agents / app modernization / DevOps) are mapped in the pitch
5. Whether the audit dossier feels *specific* (not generic) when a judge reads it
6. Whether the MCP server demo actually works live or has to fall back to the recorded video

Optimize for #1–#3 over everything else. Build for the demo, not for the codebase.

---

*See `AGENTS.md` for the IBM-Bob-flavored version of this file. They should always say the same things.*
