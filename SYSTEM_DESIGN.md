# SYSTEM_DESIGN.md — CRUX system design

> This document describes **how the parts fit together** at a level above the code. For "what each part does" see [`SPECS.md`](./SPECS.md). For "where each file lives" see [`ARCHITECTURE.md`](./ARCHITECTURE.md). For "what flows where" with diagrams, see [`WORKFLOW_DIAGRAM.md`](./WORKFLOW_DIAGRAM.md).

---

## 1. The three-layer model

CRUX is one product with three layers. Each layer can be reasoned about, demoed, and tested independently — which is exactly the resilience needed in a 48-hour solo build where any one layer might slip.

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 3 — Integration / DevOps                                 │
│  • MCP server (FastMCP 3.x) exposing five tools                 │
│  • GitHub Actions workflow calling block_merge_if_critical_gaps │
│  • IBM Bob IDE registered as MCP client                         │
└────────────────────────────────▲────────────────────────────────┘
                                 │ calls
┌────────────────────────────────┴────────────────────────────────┐
│  Layer 2 — Production audit                                     │
│  • 15 gap detectors (one Python module each)                    │
│  • Autopatch templates (jinja2 → Python)                        │
│  • Decision-log generator                                       │
│  • Service wrapper generator (FastAPI scaffold)                 │
└────────────────────────────────▲────────────────────────────────┘
                                 │ consumes
┌────────────────────────────────┴────────────────────────────────┐
│  Layer 1 — Intent recovery                                      │
│  • Notebook parser (nbformat)                                   │
│  • Variable lineage builder (ast)                               │
│  • Markdown narrative scorer (regex + heuristics)               │
│  • Cell classifier (combines all three signals)                 │
└─────────────────────────────────────────────────────────────────┘
                                 ▲
                                 │ ingests
                            input.ipynb
```

Why three layers and not one: **the demo needs three "wow" moments, and they correspond exactly to these three layers.** See [`DEMO_SCRIPT.md`](./DEMO_SCRIPT.md).

---

## 2. Dataflow

The end-to-end happy path, traced from a judge handing CRUX a notebook to the audit dossier appearing on screen:

```
input.ipynb
   │
   ▼
parse_notebook.py
   │ produces: list[Cell] with code, markdown_before, execution_count
   │
   ▼
lineage_graph.py
   │ produces: DiGraph<Cell> with edges where one cell uses another's names
   │
   ▼
narrative_scorer.py
   │ produces: per-cell score from regex matches on surrounding markdown
   │
   ▼
classifier.py
   │ produces: per-cell label ∈ {load-bearing, scaffolding, exploratory, dead}
   │           plus confidence ∈ [0.0, 1.0]
   │
   ▼  ──────────────►  intent_report.md
   │                   recovered_pipeline.py
   │
   ▼
gaps/01_input_validation.py through gaps/15_dockerfile.py
   │ each consumes recovered_pipeline.py + the original notebook
   │ each produces: a Finding(gap_id, severity, disposition, evidence, patch_or_options)
   │
   ▼
audit_assembler.py
   │ produces: ordered list[Finding]
   │
   ▼  ──────────────►  audit_dossier.md
   │                   decision_log.md
   │                   service.py, schema.py, preprocessor.py, Dockerfile, …
   │                   tests/parity_test.py
   │
   ▼
mcp_server/server.py
   │ exposes: audit_notebook, get_dossier, list_open_decisions,
   │          compare_notebooks, block_merge_if_critical_gaps
   │
   ▼
IBM Bob IDE  ──or── GitHub Actions ci/block-on-gaps.yml
```

The dataflow is intentionally one-directional. Layer 1 outputs are inputs to Layer 2; Layer 2 outputs are inputs to Layer 3. **Nothing loops back.** This makes each layer independently demoable and independently buildable in the 48-hour window.

---

## 3. Component contracts (what each layer promises to the next)

### Layer 1 → Layer 2 contract

Layer 1 produces a `RecoveredPipeline` object:

```python
class Cell(BaseModel):
    index: int                    # original cell index in the notebook
    source: str                   # the cell's code, raw
    classification: Literal["load-bearing", "scaffolding", "exploratory", "dead"]
    confidence: float             # ∈ [0.0, 1.0]
    reasons: list[str]            # human-readable: ["high execution count: 47", "markdown says 'junk'"]
    defines: set[str]             # names assigned in this cell (from ast)
    uses: set[str]                # names referenced in this cell (from ast)

class RecoveredPipeline(BaseModel):
    notebook_path: Path
    notebook_id: str              # short hash used as filename stem
    cells: list[Cell]             # all cells, classified
    load_bearing_indices: list[int]   # ordered subset that goes into the pipeline
    terminal_artifacts: list[str]     # ["model.pkl", "predict()"] — what the pipeline ultimately produces
    pipeline_source: str          # the stitched .py file as a string
```

Layer 2 must accept any `RecoveredPipeline` instance and run all 15 gap detectors against it.

### Layer 2 → Layer 3 contract

Layer 2 produces an `AuditResult`:

```python
class Finding(BaseModel):
    gap_id: int                   # 1..15
    title: str
    severity: Literal["critical", "high", "medium", "low"]
    disposition: Literal["autopatch", "decision", "autopatch_and_decision"]
    evidence: str                 # what CRUX saw that triggered this gap
    patch_diff: str | None        # unified diff if autopatched
    decision_options: list[Option] | None   # A/B/C if a decision

class AuditResult(BaseModel):
    notebook_id: str
    findings: list[Finding]
    artifacts_written: list[Path]
    parity_test_passed: bool
    completed_at: datetime
```

Layer 3 (MCP server) reads `AuditResult` from disk (each `notebook_id` has its own subdirectory under `out/`) and serializes it over MCP. **The MCP server never re-runs Layer 1 or Layer 2 — it only reads cached results.** This keeps MCP calls fast (<100ms for `get_dossier`) and lets Bob batch-query without spending Bobcoins on re-computation.

---

## 4. Invariants (things that must always be true)

These are the design rules CRUX enforces. If any of them break, the build is wrong.

1. **Layer 1 is deterministic given the same input notebook.** No randomness, no LLM calls during cell classification. The heuristic is replicable; the demo is replicable. Layers 2 and 3 are also LLM-free at audit time — patches come from rule-based templates, and the stakeholder summary in the dossier is rendered from a Jinja2 template (`templates/stakeholder_summary.md.j2`) over the structured audit result. Bob is used to *write* CRUX during the hackathon, but Bob is not in the runtime path.
2. **Every autopatch is annotated.** Every line CRUX writes that wasn't in the recovered pipeline has a `# CRUX-PATCHED: gap-N` comment.
3. **Every autopatch is idempotent.** Running CRUX twice on the same notebook produces byte-identical output (modulo timestamps in the dossier header).
4. **The audit dossier never contradicts the autopatched files.** If gap 6 (logging) is marked "autopatched" in the dossier, `service.py` must contain `structlog.get_logger()`.
5. **The MCP server is a thin facade.** All real logic lives in `skills/`. The server is ~200 LOC. The number is a feature.
6. **`samples/` is read-only.** The build must never modify a sample notebook in place.
7. **The recovered pipeline runs.** The parity test catches violations of this. No "we'll fix it later" pipelines ship.

---

## 5. Failure modes and how CRUX handles them

A demo that handles its own failures gracefully looks more polished than one that pretends failures can't happen. CRUX is designed to degrade visibly rather than crash silently.

| Failure | What CRUX does |
|---|---|
| Notebook has no markdown narrative at all | Falls back to execution-count + lineage signals; flags low confidence in `intent_report.md`; the report explicitly says `(no narrative cues — classification confidence reduced)` |
| Notebook has no terminal artifact (no `joblib.dump`, no predict function, no final cell) | Treats the last cell that produces a non-None value as a fallback terminal; logs the heuristic in `intent_report.md` |
| Notebook can't be parsed (corrupt JSON) | Aborts at Layer 1; returns a structured error to Bob; does not silently produce a half-baked output |
| `recovered_pipeline.py` raises on import | Layer 2 still runs (gaps 1–13 don't require executable code); the audit dossier surfaces this as gap 0 (a special prepended gap: "recovered pipeline does not import cleanly") |
| Parity test fails | Audit dossier marks the test as failing in red and includes the diff between expected and actual outputs; CRUX does **not** silently regenerate the test against actual outputs |
| MCP server can't bind to port | Logs to stderr (never stdout — corrupts JSON-RPC), exits with code 1; Bob's mcp.json is configured with a different fallback port |
| External LLM dependency | None — the entire pipeline (recovery, audit, dossier rendering) runs locally with no API keys required. This is by design, not by accident. |

---

## 6. Trade-offs taken (with reasoning)

These are the design decisions where there was a real choice and CRUX picked one explicitly.

- **Heuristics over a custom classifier for cell labeling.** A trained model would be more accurate on diverse notebooks but burns Bobcoins, training infra, and a labeled dataset CRUX doesn't have. Heuristics tuned against three sample notebooks are good enough for the demo and cheaper to debug.
- **15 fixed gaps over a configurable rule engine.** A configurable system is more flexible but harder to demo. Fixed gaps let the dossier feel authoritative ("here are the 15 things that always go wrong") rather than abstract.
- **FastMCP over hand-rolled JSON-RPC.** FastMCP eats the protocol details so the demo sentence "an MCP server in 200 lines" is true. The framework is Apache 2.0 and battle-tested.
- **Local MCP server over remote.** Remote deployment adds a network failure mode for the demo with no upside for a 5-minute pitch. Local stdio + local HTTP transport is simpler and judges don't care about deployment topology. The MCP surface is identical either way — the same five tools work whether the server is running on `localhost:8765` or behind a load balancer.
- **Pydantic v2 over dataclasses for all data models.** Pydantic v2 is fast and FastMCP integrates with it natively for schema generation. Dataclasses would require parallel JSON serializers.
- **`uv` over `pip` for dependency management.** `uv` resolves and installs in single-digit seconds; demos benefit from fast cold starts.
- **No web UI.** Bob is the UI. A web UI would burn 8+ hours and dilute the agent narrative.

---

## 7. Where Bob fits in (and where it doesn't)

Bob is the **driver** of the demo, not the runtime of the audit. The split is intentional.

- **Bob's job**: read AGENTS.md, understand the user's intent ("recover and audit this notebook"), invoke the right skill, narrate progress to the user, present results, and surface decisions for the user to resolve. Bob is also the MCP **client** that calls the CRUX server during the demo.
- **CRUX's job**: do the deterministic work (parsing, classification, gap detection, patching, dossier generation). All of this runs as plain Python invoked through Bob's skill mechanism.

Why the split: if the audit logic lived inside Bob's reasoning, it would be non-deterministic, slow, and Bobcoin-expensive to re-run. By making the heuristic layer plain Python and using Bob only for orchestration during the hackathon build, CRUX runs cheaply, predictably, and with no runtime dependency on any LLM provider.

The dossier's stakeholder summary: in `mcp_server/dossier.py`, the summary at the top of the rendered dossier is produced by `templates/stakeholder_summary.md.j2` — a Jinja2 template over the structured `AuditResult`. This is a deliberate design choice over an LLM-generated summary. Determinism is the feature: the dossier is a CI artifact, and CI artifacts must be byte-identical across runs. A handwritten template guarantees this; an LLM call cannot.

---

## 8. Performance and resource budget

For the demo to feel snappy:

| Operation | Target wall-clock |
|---|---|
| Layer 1 on `01_clean.ipynb` (18 cells) | < 1 second |
| Layer 1 on `02_messy.ipynb` (47 cells) | < 3 seconds |
| Layer 1 on `03_chaos.ipynb` (80+ cells) | < 6 seconds |
| Layer 2 (full audit, all 15 gaps) | < 10 seconds |
| Service generation (Layer 2 last step) | < 2 seconds |
| Parity test execution | < 5 seconds |
| MCP server cold start | < 2 seconds |
| Single MCP tool call (e.g., `get_dossier`) | < 100 ms |
| `block_merge_if_critical_gaps` over GitHub Actions | < 30 seconds end-to-end |

Memory: the entire pipeline runs in <500MB on a laptop. No GPU required, no network calls during audit — CRUX itself does not run or call any model.

Bobcoin budget: the **build** consumes ~34 of 40 Bobcoins. The **demo run** consumes ~1 Bobcoin (one Bob session that orchestrates the live run). See [`BOBCOIN_BUDGET.md`](./BOBCOIN_BUDGET.md).

---

## 9. Security posture (for a hackathon submission)

This is a hackathon prototype, not production software. Security is scoped accordingly:

- **MCP server**: runs locally on `127.0.0.1`, no auth. Production deployment would need API-key auth + TLS — there's a comment in `server.py` saying so.
- **Secrets**: Gap 9 (hardcoded paths and secrets) is a CRUX feature, not a CRUX risk. CRUX itself never logs secrets it finds; it flags them and writes a redacted reference to `.env.example`.
- **Credentials**: CRUX has no runtime credential dependencies. No API keys, no service accounts, no secrets need to be in the repo or environment for the audit pipeline to work. The only credential surface is GitHub's `GITHUB_TOKEN` inside the Actions workflow, which is auto-provisioned. The `.gitignore` includes `.env`, `*.key`, and `config/credentials.json` defensively in case a future contributor adds an integration that needs them.
- **GitHub Actions**: the `ci/block-on-gaps.yml` workflow calls a locally-run MCP server during the demo via a self-hosted runner; for the public repo version it runs `crux audit` directly without the MCP indirection.
- **Sample data**: derived from public Kaggle competitions, no PI, no client data, no scraped social-media data. Provenance documented in `samples/PROVENANCE.md`.

---

*If something in the build feels off, check whether it violates one of the seven invariants in §4 first. Most "is this a bug?" questions resolve there.*
