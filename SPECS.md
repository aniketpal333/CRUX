# SPECS.md — CRUX functional specifications

> This is the contract. Everything in this file is what CRUX **must** do. Anything not in this file is out of scope for the hackathon submission. If you (Bob, Claude, or a human) ever feel tempted to add a feature, ask whether the demo gets better — if not, don't build it.

---

## 1. Inputs and outputs (the contract at a glance)

### Input
A single Jupyter notebook (`.ipynb`) somewhere on the local filesystem. The notebook can be:
- **Executed** (cells have `execution_count` values) — preferred; provides the most signal
- **Unexecuted** (no execution counts) — supported, but intent recovery falls back harder onto markdown/lineage signals
- **Partially executed** — supported, treated as executed with missing values handled gracefully

CRUX does not require the notebook to run cleanly end-to-end. It does not require any companion files (no `requirements.txt`, no data file, no model artifact). If those exist, CRUX uses them; if they don't, CRUX infers what it can.

### Output (a directory `out/<notebook-stem>/`)
```
out/<stem>/
├── recovered_pipeline.py      Clean Python module: load-bearing cells stitched in dataflow order
├── intent_report.md           Per-cell classification + reasoning, sorted by original cell index
├── audit_dossier.md           15 gaps, severity-ranked, with patch/decision/scaffold per gap
├── decision_log.md            Structured A/B/C options for every non-autopatched gap
├── service.py                 FastAPI wrapper around recovered_pipeline.py
├── schema.py                  Pydantic input/output models inferred from training df
├── preprocessor.py            Serializable train/serve preprocessor (only if scikit-learn pipeline detected)
├── tests/
│   ├── parity_test.py         Pins recovered_pipeline outputs on a training-data sample
│   └── conftest.py
├── Dockerfile
├── docker-compose.yml         For local one-command testing
├── requirements.txt
└── .env.example               Env vars extracted from hardcoded strings (secrets flagged)
```

---

## 2. The cell taxonomy (Stage 1: Narrative Intent Recovery)

Every cell in the notebook is classified into exactly **one** of four categories. The classification drives whether the cell ends up in `recovered_pipeline.py`.

| Classification | Goes into recovered pipeline? | Definition |
|---|---|---|
| **load-bearing** | Yes | Produces a value (model, dataframe, function, transform) consumed by another cell that ultimately produces the final saved artifact or prediction function. |
| **scaffolding** | Yes (consolidated to top) | Imports, configuration constants, helper-function definitions used by load-bearing cells. |
| **exploratory** | No | Was iterated on, branched off, or whose outputs feed nothing the final artifact depends on. |
| **dead** | No | Errored, was commented-out, has zero outputs, or is explicitly marked junk in surrounding markdown. |

### The three signals (combined into a per-cell score)

CRUX combines three signals into a per-cell classification score. The weights are tuned, not principled — see `skills/notebook-narrative/lineage_graph.py` for the constants. They were tuned against the three sample notebooks during hours 3–14 of the build.

#### Signal A: execution count
- `execution_count == None` → cell never ran → strong dead signal
- `execution_count <= 3` and the cell defines a name used downstream → strong load-bearing signal
- `execution_count >= 10` → exploratory iteration → moderate exploratory signal
- `execution_count >= 30` → near-certain exploratory signal *unless* the cell is the very last in the notebook

#### Signal B: markdown narrative
The Markdown cells immediately *before* a code cell carry intent. CRUX scans them for explicit phrases (regex-based, case-insensitive):

- **Strong-keep cues**: `final`, `the one that worked`, `production`, `keep this`, `# Approach <N> (the one we ship)`, `## Final Model`
- **Strong-discard cues**: `junk`, `delete later`, `broken`, `don't run`, `old version`, `scratch`, `# DEAD`, `# IGNORE`
- **Weak-keep cues**: section headers like `## Train`, `## Predict`, `## Save Model`
- **Weak-discard cues**: `let's try`, `experimenting`, `not sure if this works`, `back to this approach`

Markdown cues override execution-count-derived classifications **only when the cue is unambiguous** (strong-keep or strong-discard). For weak cues, the score is adjusted but execution-count signal still dominates.

#### Signal C: variable lineage
CRUX builds a directed graph of names defined and used across cells using Python's `ast` module:
- **Nodes**: cells
- **Edges**: cell `i → j` if cell `j` uses any name defined by cell `i` (and not redefined in between)

To classify load-bearing-ness, CRUX identifies one or more **terminal artifacts**:
- A cell containing `joblib.dump`, `pickle.dump`, `model.save`, `torch.save` → the saved model is the terminal
- A cell defining a function whose name matches `predict|forecast|infer|score` → that function is terminal
- A cell that is the final cell of the notebook and produces a non-None value → fallback terminal

CRUX then traces backward from terminals via the lineage graph. **Any cell on a path to a terminal is load-bearing.** Any cell *not* on such a path is exploratory or dead (which signal A and B then disambiguate).

---

## 3. The 15 production gaps (Stage 2: Audit)

This list is fixed. **Do not add, remove, reorder, or rename gaps without updating `DEMO_SCRIPT.md` in lockstep** — judges will see these by number.

Severity legend:
- **🔴 Critical** — production breakage or data leak risk
- **🟡 High** — degrades reliability or debuggability
- **🟢 Medium** — operational hygiene
- **🔵 Low** — nice-to-have

Disposition legend:
- **A**: Autopatch — CRUX modifies code and writes the patch
- **D**: Decision — CRUX presents options A/B/C in `decision_log.md`
- **A+D**: Partial autopatch + decision for the part requiring judgment

| # | Gap | Severity | Disposition | What it produces |
|---|---|---|---|---|
| 1 | Input validation | 🔴 | A | `schema.py` with `PredictRequest(BaseModel)`; types inferred from training df dtypes |
| 2 | Schema contract | 🔴 | A | `schema.py` adds `PredictResponse(BaseModel)` with prediction + confidence + metadata fields |
| 3 | Train/serve skew | 🔴 | A | `preprocessor.py`: serializable preprocessor (sklearn `ColumnTransformer` or pandas-pipeline pickle) |
| 4 | Missing-model graceful degradation | 🔴 | A | `service.py` startup check; returns 503 with clear message if model file absent |
| 5 | No model versioning | 🟡 | A | Adds `model_version` field to `PredictResponse`; reads from env var `MODEL_VERSION` (default = git SHA) |
| 6 | Logging gap | 🟡 | A | Replaces `print` with `structlog`; logs request_id, feature values, prediction, latency |
| 7 | Input range validation | 🟡 | A+D | Autopatches: warn-header for out-of-range. Decision: hard-reject? Soft-warn? Silent-clip? (A/B/C) |
| 8 | No drift detection hook | 🟢 | D | Decision: scaffold endpoint that records prediction distributions? Hourly aggregation? Real-time? Defer? (A/B/C) |
| 9 | Hardcoded paths and secrets | 🔴 | A | Extracts to `.env.example`; replaces in code with `os.environ.get(...)`; **flags** any string matching secret patterns for rotation |
| 10 | No rate limiting / timeout | 🟡 | A+D | Autopatches: `@asyncio.timeout(30)` on predict endpoint. Decision: rate limit per-IP / per-key / none (infrastructure call) |
| 11 | No batch endpoint | 🟢 | D | Decision: scaffold `/predict-batch` endpoint? Stream or single response? Defer? (A/B/C) |
| 12 | No authentication scaffolding | 🟡 | D | Decision: scaffold API-key check? OAuth? Defer to ingress? (A/B/C). If A or B chosen, autopatch on next run. |
| 13 | No reproducibility metadata | 🟢 | A | Adds metadata block to every response: `model_version`, `feature_set_hash`, `preprocessor_version`, `served_at` |
| 14 | No tests | 🟡 | A | `tests/parity_test.py`: runs `recovered_pipeline.py` against a 100-row sample of the training df, pins outputs |
| 15 | No Dockerfile / deployment manifest | 🟡 | A | `Dockerfile` (multi-stage, python:3.11-slim base), `docker-compose.yml` for local. Cloud-specific deployment manifests (e.g. Code Engine, Fly.io, Cloud Run) are out of scope — the audit only asserts a working container build. |

### Autopatch invariants
- Every autopatch is **idempotent** (running CRUX twice produces the same output)
- Every autopatch is **annotated** (a comment in the patched file says `# CRUX-PATCHED: gap-N (<short reason>)`)
- The audit dossier always includes a **diff snippet** for each autopatch so a reviewer can see exactly what changed
- Autopatches are **never silent**: even when CRUX is confident, the dossier reports what it did

### Decision-log format
Every entry in `decision_log.md` has this exact shape:

```markdown
### Decision N — <gap title>

**Severity**: 🟢 Medium
**Why CRUX surfaced this**: <one sentence>

**Option A**: <name>. <one sentence trade-off>.
**Option B**: <name>. <one sentence trade-off>.
**Option C**: Defer to later. <one sentence consequence>.

**CRUX recommends**: <A | B | C> because <reason>.
**Action required**: re-run `crux audit --resolve N=<A|B|C>`.
```

---

## 4. The MCP server (Stage 3: DevOps integration)

The MCP server is built on **FastMCP 3.x** (Python 3.11+, Apache 2.0). It exposes exactly **five tools**. Every tool returns a JSON-serializable Pydantic model.

### Tool 1: `audit_notebook(path: str) -> AuditResult`
End-to-end run: intent recovery → audit → returns a summary including notebook ID, count of gaps by severity, count of autopatches applied, count of open decisions.

```python
class AuditResult(BaseModel):
    notebook_id: str
    notebook_path: str
    classification_summary: dict[str, int]   # {"load-bearing": 12, "exploratory": 28, ...}
    gaps_by_severity: dict[str, int]          # {"critical": 3, "high": 5, "medium": 4, "low": 0}
    autopatches_applied: int
    open_decisions: int
    output_dir: str
    completed_at: datetime
```

### Tool 2: `get_dossier(notebook_id: str) -> str`
Returns the full text of `audit_dossier.md` for a given notebook ID. Used by Bob and by the GitHub Actions workflow to surface the audit in PR comments.

### Tool 3: `list_open_decisions(notebook_id: str, severity: str | None = None) -> list[Decision]`
Lists every open decision in `decision_log.md`, optionally filtered by severity. Each `Decision` has the gap number, title, severity, the three options, and CRUX's recommendation.

### Tool 4: `compare_notebooks(before_path: str, after_path: str) -> ComparisonResult`
Given two notebook versions, runs the audit on both and returns a diff: which gaps were resolved, which new ones appeared, which decisions changed. Used in the demo to show the "did this PR make things better?" beat.

### Tool 5: `block_merge_if_critical_gaps(notebook_id: str) -> MergeBlockResult`
Returns `{"allow_merge": False, "blocking_gaps": [...]}` if any 🔴 gap is unresolved. Otherwise `{"allow_merge": True, "blocking_gaps": []}`. The GitHub Actions workflow calls this and exits non-zero if `allow_merge == False`. **This is the closing-the-loop tool**; it must work live in the demo.

---

## 5. Sample notebooks (the three demo inputs)

The samples are version-controlled in the repo. They are derived from public Kaggle competitions but **modified** to exhibit specific intent-recovery and audit signatures. Provenance is in `samples/PROVENANCE.md`.

| Sample | Lines | Cells | Designed to exhibit |
|---|---|---|---|
| `01_clean.ipynb` | ~150 | 18 | Mostly clean: 12 load-bearing, 4 scaffolding, 2 exploratory. Audit finds 5 gaps (mostly medium). **Demo backup if 02 fails.** |
| `02_messy.ipynb` | ~400 | 47 | Realistic mess: 12 load-bearing, 28 exploratory, 5 dead, 2 scaffolding. Markdown explicitly says `## Approach 3 (the one that worked)`. Audit finds 11 gaps including 3 critical. **The hero demo notebook.** |
| `03_chaos.ipynb` | ~700 | 80+ | Stress test: zero markdown narrative, lots of `In [1]:` re-runs, hardcoded paths, an API key in a string, no saved model artifact. Demonstrates how CRUX degrades — the intent_report flags low confidence on some cells. **Stretch demo.** |

---

## 6. Out-of-scope (deliberately not built)

These are tempting but cut for solo / 48h scope:
- A web UI. Bob is the UI.
- Support for non-Python notebooks (R, Julia kernels). Out.
- Automatic conversion of TensorFlow/Keras `Sequential` models to `tflite`. Out.
- A custom-trained classifier for cell categorization. Heuristics + Bob's reasoning are enough.
- A "marketplace" of audit rules. The 15 gaps are the audit; that's the product.
- Real authentication on the MCP server (it runs locally for the demo; production deployment would need it).
- Multi-notebook batch mode. One notebook at a time, every time.

---

## 7. Acceptance criteria (the demo passes when…)

- Pointing CRUX at `samples/02_messy.ipynb` produces all artifacts in `out/02_messy/` in **under 2 minutes** of wall-clock time.
- The recovered_pipeline.py runs without modification when given a sample row of the training data.
- The parity test passes.
- The MCP server starts in <2s and responds to `audit_notebook` over MCP-Inspector.
- The GitHub Actions workflow `ci/block-on-gaps.yml`, when triggered against `03_chaos.ipynb`, exits non-zero.
- The `bob_sessions/` folder contains at least one screenshot and one markdown export per Bob task that produced demo artifacts.
- A judge can scan `out/02_messy/audit_dossier.md` in 30 seconds and tell which gaps are critical, which were patched, and which need a decision.

---

*This spec is the contract. Refer back to it when scope-creep tries to creep.*
