# ARCHITECTURE.md — CRUX repo architecture

> Where every file lives, why, and what it depends on. For *what* the code does, see [`SPECS.md`](./SPECS.md). For *how the parts fit together*, see [`SYSTEM_DESIGN.md`](./SYSTEM_DESIGN.md).

---

## 1. Top-level repo layout

```
crux/
├── README.md
├── AGENTS.md                       # auto-loaded by Bob; project context
├── CLAUDE.md                       # mirror for Claude/other CLAUDE.md-aware tools
├── SPECS.md
├── SYSTEM_DESIGN.md
├── ARCHITECTURE.md                 # ← this file
├── WORKFLOW_DIAGRAM.md
├── PHASES.md
├── BOBCOIN_BUDGET.md
├── JUDGING_PLAYBOOK.md
├── DEMO_SCRIPT.md
├── MCP_SETUP.md
├── TECH_STACK.md
│
├── pyproject.toml                  # uv project file; declares all deps
├── uv.lock
├── ruff.toml
├── .gitignore
├── .bobignore                      # files Bob should never read (.env, secrets/, *.key)
│
├── .bob/
│   ├── modes/
│   │   └── crux-mode.md            # custom Bob mode for end-to-end runs
│   └── rules/
│       ├── 01-style.md             # python style; commit-message format
│       ├── 02-internal-monologue.md  # write notes after multi-step tasks
│       └── 03-no-samples-edits.md  # never modify samples/ in place
│
├── skills/
│   ├── notebook-narrative/
│   │   ├── SKILL.md                # when Bob should activate this skill
│   │   ├── parse_notebook.py       # nbformat → list[Cell]
│   │   ├── lineage_graph.py        # ast → DiGraph<Cell>
│   │   ├── narrative_scorer.py     # regex on surrounding markdown
│   │   ├── classifier.py           # combines all three signals
│   │   ├── pipeline_writer.py      # emits recovered_pipeline.py
│   │   ├── intent_report.py        # emits intent_report.md
│   │   └── tests/
│   │       ├── test_parse_notebook.py
│   │       ├── test_lineage_graph.py
│   │       └── test_classifier.py
│   │
│   └── production-audit/
│       ├── SKILL.md
│       ├── audit_runner.py         # orchestrates all 15 gaps, emits dossier
│       ├── findings.py             # Finding dataclass / Pydantic model
│       ├── decision_log.py         # writes decision_log.md
│       ├── service_generator.py    # writes service.py + Dockerfile + compose
│       ├── parity_test_generator.py # writes tests/parity_test.py
│       ├── gaps/
│       │   ├── __init__.py
│       │   ├── gap_01_input_validation.py
│       │   ├── gap_02_schema_contract.py
│       │   ├── gap_03_train_serve_skew.py
│       │   ├── gap_04_missing_model.py
│       │   ├── gap_05_no_versioning.py
│       │   ├── gap_06_logging.py
│       │   ├── gap_07_input_range.py
│       │   ├── gap_08_drift_detection.py
│       │   ├── gap_09_hardcoded_paths.py
│       │   ├── gap_10_rate_limit_timeout.py
│       │   ├── gap_11_batch_endpoint.py
│       │   ├── gap_12_authentication.py
│       │   ├── gap_13_repro_metadata.py
│       │   ├── gap_14_no_tests.py
│       │   └── gap_15_no_dockerfile.py
│       ├── patches/                 # jinja2 templates for autopatching
│       │   ├── pydantic_input.py.j2
│       │   ├── pydantic_output.py.j2
│       │   ├── preprocessor.py.j2
│       │   ├── service.py.j2
│       │   ├── parity_test.py.j2
│       │   ├── Dockerfile.j2
│       │   ├── docker-compose.yml.j2
│       │   └── env.example.j2
│       └── tests/
│           ├── test_audit_runner.py
│           └── test_each_gap.py     # parametrized over the 15 gaps
│
├── templates/                       # dossier rendering templates
│   ├── stakeholder_summary.md.j2    # deterministic plain-language summary (no LLM)
│   ├── dossier.html.j2              # the full HTML dossier (renders to out/<nb>/dossier.html)
│   └── decision_log.md.j2           # decision-required entries with options
│
├── mcp_server/
│   ├── __init__.py
│   ├── server.py                    # FastMCP entrypoint (~200 LOC; pitch-relevant)
│   ├── tools.py                     # the five MCP tools
│   ├── dossier.py                   # builds AuditResult and renders templates/
│   ├── models.py                    # Pydantic models for tool I/O
│   └── README.md                    # how to run + connect to Bob
│
├── samples/
│   ├── PROVENANCE.md                # where each sample came from + license
│   ├── 01_clean.ipynb               # demo-easy: 18 cells
│   ├── 02_messy.ipynb               # demo-realistic: 47 cells     ← hero notebook
│   └── 03_chaos.ipynb               # demo-stretch: 80+ cells
│
├── out/                             # gitignored runtime outputs (per-notebook)
│   └── <notebook-stem>/
│       ├── recovered_pipeline.py
│       ├── service.py
│       ├── schema.py
│       ├── preprocessor.py
│       ├── intent_report.md
│       ├── audit_dossier.md
│       ├── decision_log.md
│       ├── Dockerfile
│       ├── docker-compose.yml
│       ├── requirements.txt
│       ├── .env.example
│       ├── deployment/
│       │   └── code-engine.yaml
│       └── tests/
│           ├── parity_test.py
│           └── conftest.py
│
├── tests/                           # repo-wide tests (skills' own tests live alongside their code)
│   ├── test_end_to_end_clean.py     # runs full pipeline on 01_clean.ipynb
│   ├── test_end_to_end_messy.py     # runs full pipeline on 02_messy.ipynb
│   └── test_mcp_server.py           # spins up server, hits each tool
│
├── ci/
│   └── block-on-gaps.yml            # GitHub Actions workflow
│
├── internal-monologue/              # Bob's per-task notes (gitignored after submission, kept for judges)
│
└── bob_sessions/                    # ===== REQUIRED FOR HACKATHON SUBMISSION =====
    ├── README.md                    # what's in here and why
    ├── screenshots/
    │   └── *.png                    # consumption-summary screenshots
    └── exports/
        └── *.md                     # exported task histories
```

---

## 2. Module-by-module purpose and responsibilities

### `skills/notebook-narrative/`

The intent-recovery layer. One skill, six modules + tests.

#### `parse_notebook.py`
- **Input**: path to `.ipynb`
- **Output**: `list[Cell]` (ordered, with `index`, `source`, `markdown_before`, `markdown_after`, `execution_count`, `cell_type`, `outputs`)
- **Dependencies**: `nbformat`
- **Why a separate module**: testable in isolation; useful as a building block elsewhere

#### `lineage_graph.py`
- **Input**: `list[Cell]`
- **Output**: `networkx.DiGraph` where nodes are cell indices and edges are name-flow relationships
- **Dependencies**: `ast` (stdlib), `networkx`
- **Key function**: `_extract_defines_uses(source: str) -> tuple[set[str], set[str]]` — uses `ast.NodeVisitor` to find `Assign` and `FunctionDef` targets vs. `Name` references
- **Note**: handles tuple unpacking, augmented assign, `for` targets, `with ... as`. Does *not* handle dynamic `globals()` mutation (out of scope; flagged as a known limitation in `intent_report.md` if detected).

#### `narrative_scorer.py`
- **Input**: `list[Cell]`
- **Output**: `dict[int, NarrativeScore]` where key is cell index
- **Dependencies**: `re` (stdlib)
- **Key data**: `STRONG_KEEP_PATTERNS`, `STRONG_DISCARD_PATTERNS`, `WEAK_KEEP_PATTERNS`, `WEAK_DISCARD_PATTERNS` — all module-level constants, easy to tune

#### `classifier.py`
- **Input**: `list[Cell]`, lineage graph, narrative scores
- **Output**: `RecoveredPipeline` (per `SPECS.md` §3)
- **Algorithm**: combines the three signals via weighted scoring; decides terminals; traces backward; classifies each cell; orders load-bearing cells in dataflow order via topological sort

#### `pipeline_writer.py`
- **Input**: `RecoveredPipeline`
- **Output**: writes `recovered_pipeline.py` to disk
- **Behavior**: stitches cells in dataflow order; consolidates imports at top; renames cells' implicit results to local-variable scope; produces a clean Python module

#### `intent_report.py`
- **Input**: `RecoveredPipeline`
- **Output**: writes `intent_report.md` to disk
- **Format**: a markdown table with columns `index | classification | confidence | reason | preview` plus a top-level summary line `12 load-bearing / 28 exploratory / 5 dead / 2 scaffolding`

### `skills/production-audit/`

The audit layer. Two top-level orchestrators (`audit_runner.py`, `service_generator.py`) and 15 single-purpose gap detectors.

#### `audit_runner.py`
- **Input**: `RecoveredPipeline` + path to original `.ipynb`
- **Output**: `AuditResult` plus side-effects (writes dossier, decision log, service files, tests)
- **Behavior**: calls each `gap_NN_*.py`'s `detect()` function in order; collects findings; writes the dossier in severity-ranked sections; calls service-generator and parity-test-generator; runs the parity test and records pass/fail in the AuditResult

#### `gaps/gap_NN_*.py`
Each gap module exposes a single `detect(pipeline, notebook) -> Finding` function. A gap detector is a **plain Python function** — no LLM calls, no I/O beyond reading the recovered pipeline source. This keeps the audit deterministic and replicable.

The naming convention `gap_NN_<short_name>.py` is enforced (numeric prefix matches the gap number in `SPECS.md` §3). The gap number is part of the demo and the dossier; reordering would be a breaking change.

#### `service_generator.py`
- Reads jinja2 templates from `patches/`
- Renders `service.py`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `.env.example`
- Writes them to `out/<stem>/`
- Optionally writes `deployment/code-engine.yaml` if user opted in

#### `parity_test_generator.py`
- Detects the training dataframe in the recovered pipeline (heuristic: the largest pandas DataFrame still in scope at the terminal cell)
- Samples 100 rows
- Runs the recovered pipeline against those rows
- Pickles expected outputs alongside the test
- Generates `tests/parity_test.py` that re-runs the pipeline on the same rows and asserts the outputs match

### `mcp_server/`

The DevOps layer. Thin facade over `skills/`.

#### `server.py`
A single FastMCP `mcp = FastMCP("crux")` declaration plus five `@mcp.tool` decorators. Imports tool implementations from `tools.py` so `server.py` is purely declarative. Runnable two ways:

```bash
# stdio transport (Bob will use this)
uv run mcp_server/server.py

# Streamable HTTP transport (MCP Inspector / GitHub Actions will use this)
uv run mcp_server/server.py --transport streamable-http --port 8080
```

#### `tools.py`
Contains the five tool implementations:
- `audit_notebook(path)` → invokes `skills/notebook-narrative` then `skills/production-audit`
- `get_dossier(notebook_id)` → reads `out/<id>/audit_dossier.md`
- `list_open_decisions(notebook_id, severity)` → parses `decision_log.md`, filters
- `compare_notebooks(before, after)` → audits both, diffs the findings
- `block_merge_if_critical_gaps(notebook_id)` → reads cached AuditResult, returns boolean + list

Each tool is async-friendly (uses `async def` even when not strictly necessary; FastMCP handles both, but async future-proofs against the GitHub Actions step running over Streamable HTTP).

#### `models.py`
Pydantic v2 models for tool I/O — mirrors the contracts in `SYSTEM_DESIGN.md` §3. Lives in its own file so the MCP schema stays readable when FastMCP auto-generates JSON Schema from Python type hints.

### `.bob/modes/crux-mode.md`

The custom Bob mode definition. Per IBM Bob docs, this is a markdown file with a YAML frontmatter and structured sections: `Slug`, `Name`, `Description`, `Scope`, `Role definition`, `When to use`, `Mode-specific Custom Instructions`. The mode is **project-scoped** (lives in `.bob/`, not `~/.bob/`), so it's version-controlled with the rest of CRUX.

---

## 3. External dependencies (what's in `pyproject.toml`)

```toml
[project]
name = "crux"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "nbformat>=5.10",          # parse .ipynb
    "networkx>=3.2",           # variable lineage graph
    "pydantic>=2.7",           # all data models
    "fastapi>=0.115",          # service wrapper template
    "uvicorn[standard]>=0.30", # service runtime in Dockerfile
    "structlog>=24.1",         # log autopatch
    "fastmcp>=3.2",            # MCP server (Apache 2.0, jlowin/fastmcp)
    "jinja2>=3.1",             # patch templates
    "scikit-learn>=1.5",       # only used for ColumnTransformer detection in gap 3
    "pandas>=2.2",             # parity test scaffolding
    "joblib>=1.4",             # detect saved-model cells in lineage analysis
    "click>=8.1",              # CLI for `crux audit` invocation outside Bob
    "ruff>=0.5",               # linter (dev)
    "pytest>=8",               # test runner (dev)
]

[project.scripts]
crux = "skills.production_audit.audit_runner:cli"
crux-mcp = "mcp_server.server:main"
```

Total transitive footprint: ~70 packages, all permissively licensed (Apache 2.0, MIT, BSD-3). `uv install` completes in ~10 seconds on a warm cache. No optional extras — what's listed above is the entire dependency surface.

> **Why no `[project.optional-dependencies]` block?** Earlier drafts of this project included an `ibm-watsonx-ai` optional extra for an LLM-generated stakeholder summary. That feature was removed in favor of a deterministic Jinja2 template (`templates/stakeholder_summary.md.j2`) over the structured `AuditResult`. The dossier is a CI artifact; CI artifacts need to be byte-identical across runs, and template rendering guarantees that while LLM calls cannot.

---

## 4. The custom Bob mode (`.bob/modes/crux-mode.md`)

```markdown
---
slug: crux-mode
name: CRUX (notebook recovery)
scope: project
---

# CRUX mode

You are operating inside the CRUX repository. When the user asks you to recover, audit, or convert a notebook, follow this fixed workflow:

## When to use
- User mentions a notebook by path or by `@samples/<filename>`
- User asks to "recover", "audit", "convert", "modernize", or "productionize" a notebook
- User asks "what gaps does this notebook have"

## Role definition
Be a meticulous, judgment-calibrated agent that recovers production-grade artifacts from messy notebooks. Always read AGENTS.md before acting. Always read SPECS.md when unsure about gap definitions or cell taxonomy.

## Workflow (do not skip steps)
1. Confirm the input notebook path with the user. Do not guess.
2. Run the `notebook-narrative` skill against that path. Stop after Layer 1. Show the user the cell-classification summary table from `intent_report.md`. Wait for confirmation before proceeding.
3. Run the `production-audit` skill against the recovered pipeline. Show the user the `audit_dossier.md` summary. Highlight any 🔴 critical gaps explicitly.
4. If decisions are open, walk the user through them one at a time. Do not skip any.
5. After completion, remind the user **once** to export the task session to `bob_sessions/`.

## Auto-approve scope
- Read: yes
- Write: only inside `out/<notebook-stem>/`
- Execute: only `pytest` and `python -c "from skills...; ..."` smoke tests
- MCP: yes (calls to the local crux MCP server are routine)
- Browser: no

## Custom instructions
- Cite gap numbers from SPECS.md when narrating audit findings (e.g., "gap 6: logging").
- When a gap has options A/B/C, present them in a markdown table, not prose.
- When the parity test fails, do not silently regenerate it. Surface the failure with the diff.
```

---

## 5. The `.bobignore`

Bob respects `.bobignore` the same way git respects `.gitignore`. CRUX's `.bobignore` keeps Bob away from anything Bob shouldn't read:

```
.env
.env.*
secrets/
*.key
config/credentials.json
out/        # Bob shouldn't waste context on per-notebook generated artifacts
.venv/
__pycache__/
*.pyc
```

---

## 6. Directory ownership and lifecycle

| Directory | Edited by humans? | Edited by Bob? | Edited at runtime? | Committed? |
|---|---|---|---|---|
| `README.md`, `*.md` (top level) | Yes | Yes (rare; needs explicit ask) | No | Yes |
| `AGENTS.md`, `CLAUDE.md` | Yes (refinements) | Yes (when context evolves) | No | Yes |
| `.bob/` | Yes | Yes (modes/rules) | No | Yes |
| `skills/` | Yes (Bob writes most of it) | Yes | No | Yes |
| `mcp_server/` | Yes (Bob writes most of it) | Yes | No | Yes |
| `samples/` | Yes (one-time setup) | **No** (read-only) | No | Yes |
| `tests/` | Yes | Yes | Yes (pytest creates fixtures) | Yes (test code) / No (fixtures gitignored) |
| `out/` | No | No (Bob calls skills which write here) | Yes | **No** (gitignored) |
| `internal-monologue/` | Sometimes | Yes (after multi-step tasks) | Yes | Yes (judges read these) |
| `bob_sessions/` | Yes (you upload screenshots + exports) | No | No | Yes (REQUIRED for judging) |
| `ci/` | Yes | Yes | No | Yes |

---

## 7. Build, test, lint commands (paste-ready)

```bash
# Install
uv venv && source .venv/bin/activate
uv sync

# Lint
uv run ruff check .

# Test (everything)
uv run pytest

# Test (only intent recovery)
uv run pytest skills/notebook-narrative/tests

# Run end-to-end on a notebook (without Bob)
uv run crux audit samples/02_messy.ipynb

# Start the MCP server
uv run crux-mcp                                    # stdio
uv run crux-mcp --transport streamable-http        # HTTP for the inspector

# Inspect MCP tools
uv run mcp dev mcp_server/server.py                # opens MCP Inspector at http://127.0.0.1:6274

# Trigger CI gate locally (simulates the GitHub Actions workflow)
uv run python ci/local_block_check.py samples/03_chaos.ipynb
```

---

*If a new module needs a home, ask: "is this Layer 1, Layer 2, or Layer 3?" Then put it in the corresponding directory. If it doesn't fit any of the three, it probably shouldn't be built.*
