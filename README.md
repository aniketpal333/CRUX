# CRUX

**Code Recovery from Undocumented eXperiments**

> A solo IBM Bob agent that reads a Jupyter notebook as a *narrative*, recovers what the data scientist meant to ship, audits the gaps that production will punish, and patches what it safely can — turning a messy `.ipynb` into a deployable FastAPI service in minutes.

---

## The 30-second pitch

Data scientists prototype in notebooks. Notebooks are messy by design — thinking made visible, full of dead-end experiments, abandoned approaches, debugging cells, "let me just try this" detours. Somewhere in that mess is the 20% that actually needs to ship. Today, turning that 20% into a production service takes engineers weeks of meetings, rewrites, and judgment calls.

**CRUX collapses that work into minutes.** It uses IBM Bob as an agent that:

1. **Recovers intent** — reads execution counts, markdown commentary, and variable lineage to classify every cell as load-bearing, exploratory, dead, or scaffolding. Keeps only what was meant to ship.
2. **Audits production-readiness** — runs a 15-gap audit (input validation, train/serve skew, missing logging, no model versioning, hardcoded secrets, no tests, no Dockerfile…) and either autonomously patches each gap or surfaces it as a decision for a human.
3. **Exposes everything as an MCP server** — so any CI/CD pipeline, Bob session, or downstream agent can audit a notebook, fetch the dossier, list open decisions, or block a merge with critical unresolved gaps.

The output is a runnable, dockerized FastAPI service plus an audit dossier and a decision log — the document a senior engineer would produce in week three of a client engagement, generated in five minutes.

---

## Why this wins the brief

The hackathon theme is **"turn idea into impact faster."** For a data scientist, the notebook *is* the idea, and a deployed service *is* the impact. CRUX collapses that exact gap, and the brief's three focus areas all map cleanly onto a single product:

| Focus area | How CRUX hits it |
|---|---|
| **AI agents doing complex multi-step work** | Intent recovery + 15-gap audit + autonomous patching + decision surfacing is exactly that. |
| **App modernization** | Notebooks are legacy from birth — no contracts, no tests, no docs, no deployment story. CRUX modernizes them in one pass. |
| **DevOps** | The audit is exposed as an MCP server. A real CI job calls it to refuse merges with critical gaps. "MCP servers in minutes" delivered as a tangible demo step. |

Three boxes, one product, one demo.

---

## The three things that make CRUX unique

These are the differentiation pillars. Every README sentence, every demo line, every commit message reinforces one of these three.

### 1. Narrative Intent Recovery
Existing tools (`nbconvert`, Jupytext, paid platforms) treat a notebook as a flat list of cells and convert all of them. They preserve the mess. CRUX reads the notebook as a **narrative artifact** — a document where intent is buried under exploration — and recovers only the load-bearing logic by combining three signals no rule-based tool reads:

- **Execution counts** — `In [47]:` is exploration; `In [2]:` is often production logic
- **Markdown commentary** — section headers like `## Final Model`, `## Approach 3 (the one that worked)`, `## Junk to delete later` carry explicit intent the data scientist wrote down
- **Variable lineage graph** — built via `ast`, traces backward from the final artifact (saved model, prediction function) to find the minimal set of cells that produce it

Combined, these signals produce a per-cell classification: **load-bearing**, **exploratory**, **dead**, or **scaffolding**. The recovered pipeline is the load-bearing cells, stitched in dataflow order.

### 2. Production-Readiness Audit
CRUX enumerates **15 specific gaps** that notebooks always have, ranks them by severity, autonomously patches what's safe, and flags what needs human judgment. See [`SPECS.md`](./SPECS.md#the-15-production-gaps) for the full list. Output is an audit dossier — the document a senior engineer would produce in week three of an engagement.

### 3. Decision Log + MCP Server
The thing that separates an agent from a code generator is **judgment under uncertainty**. CRUX produces a decision log alongside the audit: "I auto-patched gaps 1, 3, 5, 6, 7, 9, 11, 13, 14; the following four need your call, with options A/B/C for each." The audit and decision log are then exposed via an **MCP server** — a small FastMCP-based Python service that any other agent or CI/CD pipeline can call. Tools include `audit_notebook(path)`, `get_dossier(notebook_id)`, `list_open_decisions(severity)`, `compare_notebooks(before, after)`, and `block_merge_if_critical_gaps()`. The last one closes the loop: a real CI job refuses to merge a PR with unresolved critical gaps.

---

## Repo layout

```
crux/
├── README.md                  ← you are here
├── AGENTS.md                  ← Bob's persistent project context (auto-injected)
├── CLAUDE.md                  ← Same content for non-Bob LLM tooling
├── SPECS.md                   ← Functional specs: cell taxonomy, 15 gaps, MCP surface
├── SYSTEM_DESIGN.md           ← Three-layer system, dataflow, invariants
├── ARCHITECTURE.md            ← Module boundaries, dependencies, file-level layout
├── WORKFLOW_DIAGRAM.md        ← Mermaid diagrams for every flow
├── PHASES.md                  ← 48-hour solo plan, hour by hour
├── MCP_SETUP.md               ← IBM Bob + GitHub Actions wiring
├── TECH_STACK.md              ← Versions, libraries, services
├── BOBCOIN_BUDGET.md          ← 40 Bobcoins allocation across phases
├── JUDGING_PLAYBOOK.md        ← How each demo beat hits each judging axis
├── DEMO_SCRIPT.md             ← The 5-minute pitch, word for word
│
├── .bob/
│   ├── modes/crux-mode.md     ← custom Bob mode definition
│   └── rules/                 ← project-level rules
├── skills/
│   ├── notebook-narrative/    ← intent recovery skill
│   │   ├── SKILL.md
│   │   ├── parse_notebook.py
│   │   └── lineage_graph.py
│   └── production-audit/      ← 15-gap audit skill
│       ├── SKILL.md
│       ├── gaps/              ← one .py per gap
│       └── patches/           ← templates for autonomous fixes
├── templates/
│   └── stakeholder_summary.md.j2  ← deterministic Jinja2 dossier summary (no LLM)
├── mcp_server/
│   ├── server.py              ← FastMCP entrypoint, ~200 LOC
│   └── tools.py               ← tool implementations
├── samples/
│   ├── 01_clean.ipynb         ← demo-easy
│   ├── 02_messy.ipynb         ← demo-realistic
│   └── 03_chaos.ipynb         ← demo-stretch
├── tests/                     ← parity tests scaffolding
├── ci/
│   └── block-on-gaps.yml      ← GitHub Actions workflow
└── bob_sessions/              ← REQUIRED for hackathon judging
    ├── screenshots/
    └── exports/
```

See [`ARCHITECTURE.md`](./ARCHITECTURE.md) for the why behind every directory.

---

## Quick start (post-build)

```bash
# 1. Clone and bootstrap
git clone https://github.com/<user>/crux && cd crux
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 2. Point Bob at the repo
#    Open Bob IDE, /init to read AGENTS.md, switch to "crux-mode"

# 3. Run end-to-end on a sample notebook
#    In Bob: "Recover production service from samples/02_messy.ipynb"
#    Output appears in: out/02_messy/
#       ├── recovered_pipeline.py
#       ├── service.py            (FastAPI wrapper)
#       ├── intent_report.md
#       ├── audit_dossier.md
#       ├── decision_log.md
#       ├── tests/parity_test.py
#       └── Dockerfile

# 4. Start the MCP server (Bob can also call it)
uv run mcp_server/server.py
#    Bob's mcp.json already wires this in — see MCP_SETUP.md

# 5. Watch CI block a bad merge
gh workflow run block-on-gaps.yml -f notebook=samples/03_chaos.ipynb
```

---

## Status

This repository starts as the planning artifact for a solo, 48-hour build during **IBM Bob Dev Day Hackathon**. The 13 markdown files in this folder are the spec; the implementation lives alongside them as it gets built.

**Hackathon constraints (deliberate):**
- 1 builder
- 40 Bobcoins (no IBM Cloud / watsonx.ai dependency — the entire stack runs locally)
- 48 hours wall-clock
- A 5-minute demo at the end where three live "wow moments" happen back-to-back

See [`PHASES.md`](./PHASES.md) for the hour-by-hour plan and [`BOBCOIN_BUDGET.md`](./BOBCOIN_BUDGET.md) for the spend allocation.

---

## License & attribution

CRUX is released under Apache 2.0. It uses IBM Bob (hackathon-provisioned account), the FastMCP framework (Apache 2.0, jlowin/fastmcp), `nbformat` (BSD), and Jinja2 (BSD-3-Clause) for deterministic dossier rendering — including the stakeholder summary, which uses no language model so the audit output is byte-identical on every run. Sample notebooks are derived from public Kaggle competitions; provenance is recorded in `samples/PROVENANCE.md`.

No client data, no PI, no scraped social-media data — see hackathon data policy in the guide PDF.
