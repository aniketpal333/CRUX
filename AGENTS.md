# AGENTS.md — CRUX project context for IBM Bob

> This file is auto-loaded by IBM Bob (and any other AGENTS.md-aware agent) at the start of every conversation in this repository. It is the **single source of truth for Bob about what CRUX is, how the repo is organized, and how Bob should behave inside it.** Refine this file rather than re-explaining context every chat.

---

## What this project is

CRUX (Code Recovery from Undocumented eXperiments) is a Bob-driven agentic pipeline that turns a messy Jupyter notebook into a production-ready FastAPI service plus a senior-engineer-grade audit dossier. It does this in three stages:

1. **Narrative intent recovery** — classify every cell of a notebook as load-bearing / exploratory / dead / scaffolding using execution-count, markdown-narrative, and variable-lineage signals; emit a clean recovered pipeline.
2. **15-gap production audit** — run a fixed list of fifteen gap checks against the recovered pipeline, autopatch the safe ones, and surface the rest as a structured decision log with options A/B/C.
3. **MCP server exposure** — every capability above is also reachable as a tool over MCP so other agents and CI/CD pipelines can use CRUX programmatically.

A judge running the demo should see the notebook collapse into intent in ~30 seconds, see a real audit dossier in ~60 seconds, and see a CI job block a merge using the MCP server in another ~30 seconds. **Optimize for the demo, not for the codebase.**

---

## How Bob should behave in this repo

### Defaults
- **Mode**: When a user asks Bob to "recover" or "audit" a notebook, switch to the custom `crux-mode` defined in `.bob/modes/crux-mode.md`. For ambiguous tasks, stay in Plan mode and confirm before writing code.
- **Auto-approve**: Off by default for `Write` and `Execute`. On for `Read`. The hackathon judges will be watching tool calls — explicit approvals make Bob look deliberate.
- **Working area**: All generated artifacts go in `out/<notebook-stem>/`. Never write to `samples/` (those are demo inputs, treat as read-only).
- **Bob sessions**: After every meaningful task in this repo, remind the user to export the task history to `bob_sessions/exports/` and capture a screenshot of the consumption summary into `bob_sessions/screenshots/`. **This is required for hackathon judging.**

### Style and conventions
- **Python**: 3.11+. Use `uv` for dependency management, not `pip` directly. Type hints required on all public functions. Use Pydantic v2 for data models. Use `ruff` for linting; never bypass with `# noqa` without a comment explaining why.
- **Imports**: Stdlib → third-party → local, separated by blank lines. No wildcard imports.
- **Filenames**: snake_case. No spaces, no hyphens, no capitals.
- **Tests**: `pytest`. Parity tests pin the recovered pipeline's outputs on a small training-data sample so any future change that breaks behavior is caught.
- **Comments**: Comment the *why*, not the *what*. Especially for the heuristic weights in `notebook-narrative` — those weights look magic without context.
- **No print debugging in committed code**. Use `structlog` (it's also one of the autopatches the audit produces — eat the dogfood).

### Prompting Bob inside this repo
- **Be specific about which notebook**: always reference it by `@samples/<filename>` so Bob has explicit context.
- **Plan before code**: for any change affecting more than one file, ask Bob to produce a plan first, review it, then ask Bob to implement.
- **One concern per task**: don't ask Bob to "recover intent and add the audit and wire the MCP server" in one prompt. Three separate tasks. Bobcoin budget is tight (see `BOBCOIN_BUDGET.md`).

### Things Bob should *never* do without explicit permission
- Modify any file under `samples/` (those are demo inputs).
- Modify `.bob/modes/crux-mode.md` (that's the custom mode definition; changes to it ripple across every conversation).
- Push to `main`. Always work on a feature branch.
- Add a new third-party dependency without first checking it's permissively licensed (Apache 2.0, MIT, BSD). The hackathon submission will be public.
- Suggest fine-tuning a custom model. Heuristics + Bob's reasoning are sufficient. Training burns Bobcoins and adds zero demo value.

---

## Repo map (quick reference for Bob)

```
README.md, SPECS.md, SYSTEM_DESIGN.md, ARCHITECTURE.md, …  ← planning docs (read these first if context needed)
.bob/modes/crux-mode.md                                    ← custom mode for end-to-end runs
.bob/rules/                                                ← project-level Bob rules
skills/notebook-narrative/SKILL.md                         ← when to run intent recovery + how
skills/notebook-narrative/parse_notebook.py                ← nbformat-based cell parsing
skills/notebook-narrative/lineage_graph.py                 ← AST-based variable lineage
skills/production-audit/SKILL.md                           ← 15-gap audit invocation logic
skills/production-audit/gaps/*.py                          ← one detector per gap (15 total)
skills/production-audit/patches/*                          ← jinja templates for autonomous patches
mcp_server/server.py                                       ← FastMCP entrypoint
mcp_server/tools.py                                        ← MCP tool implementations
samples/01_clean.ipynb, 02_messy.ipynb, 03_chaos.ipynb     ← demo notebooks (read-only)
out/<stem>/                                                ← generated per-notebook outputs
tests/                                                     ← pytest-based parity tests
ci/block-on-gaps.yml                                       ← GitHub Actions: blocks merges with critical gaps
bob_sessions/                                              ← REQUIRED submission deliverable: screenshots + exports
```

---

## The 15 gaps the audit checks (so Bob doesn't reinvent them)

These are fixed and deliberate. Do not add or remove without updating `SPECS.md` and the demo script in lockstep.

1. **Input validation** — autopatchable: infer schema from training df, generate Pydantic input model.
2. **Schema contract** — autopatchable: generate Pydantic models for input + output.
3. **Train/serve skew** — autopatchable: extract `ColumnTransformer`/pandas ops into a serializable preprocessor.
4. **Missing-model graceful degradation** — autopatchable: startup check + 503 health status.
5. **No model versioning** — autopatchable: add `model_version` field to every response.
6. **Logging gap** — autopatchable: replace `print` with structured logs (`structlog`) including request IDs.
7. **Input range validation** — *decision*: warn header on out-of-range, or hard-reject? Options A/B/C.
8. **No drift detection hook** — *decision*: scaffold endpoint that records prediction distributions? Hourly or real-time? Or defer.
9. **Hardcoded paths and secrets** — autopatchable: extract to env vars; *flag* the secret for rotation.
10. **No rate limiting / timeout** — autopatchable for timeout decorator; *decision* for rate limit (infrastructure call).
11. **No batch endpoint** — *decision*: scaffold or not?
12. **No authentication scaffolding** — *decision*: scaffold API-key check, or defer entirely?
13. **No reproducibility metadata** — autopatchable: add metadata block to every response (model_version, features, preproc).
14. **No tests** — autopatchable: generate parity tests pinning recovered pipeline outputs on training-data sample.
15. **No Dockerfile / deployment manifest** — autopatchable: Dockerfile and docker-compose. Cloud-specific manifests (Code Engine, Cloud Run, etc.) are out of scope.

Severity ranking lives in `skills/production-audit/SKILL.md`. Always re-read it before changing severities.

---

## Common tasks (paste-ready prompts)

When the user asks for one of these, Bob should already know what to do:

- **"Recover intent from `@samples/02_messy.ipynb`"** → invoke `notebook-narrative` skill, write `out/02_messy/recovered_pipeline.py` and `out/02_messy/intent_report.md`, then stop and ask before running the audit.
- **"Audit `out/02_messy/recovered_pipeline.py`"** → invoke `production-audit` skill, generate `audit_dossier.md`, `decision_log.md`, plus all autopatch outputs and parity tests. Run the parity tests locally and report pass/fail.
- **"Wrap as a service"** → produce `service.py`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`. Verify it builds with `docker build .` (do not push).
- **"Show me the open decisions for the chaos notebook"** → call MCP tool `list_open_decisions(notebook_id="03_chaos", severity="critical")` and pretty-print.
- **"Block the merge"** → run `ci/block-on-gaps.yml` against the staged notebook; surface the exit code and the failing gap.

---

## Internal monologue convention

Per the Bob `Standardize Bob's behavior` tutorial: after every non-trivial multi-step task, Bob writes a short note to `internal-monologue/<YYYY-MM-DD>-<task-slug>.md` describing **what was attempted, what worked, what didn't, what to try next**. This gives the human (and future Bob sessions) an audit trail that survives context-window resets. Keep these terse — bullets, not essays.

---

## Hackathon-specific reminders for Bob

- The user has **40 Bobcoins total**. Treat this like a credit budget: don't redo work, don't burn cycles on speculative refactors, don't over-explore. If a task feels under-scoped, ask one clarifying question before spending Bobcoins.
- The user must export task sessions to `bob_sessions/`. After any session that produced meaningful artifacts, remind them to export — but do it **once per session**, not after every reply.
- The MCP server is the keystone of the DevOps demo beat. If anything in the build slips, drop sample 03 first, then sample 02 polish — but **never drop the MCP server**. (The watsonx.ai capstone has already been cut from scope; the stakeholder summary is now generated from a deterministic Jinja2 template — see `templates/stakeholder_summary.md.j2`.)
- The brief uses the phrase *"MCP servers in minutes"*. CRUX's `mcp_server/server.py` lives in **~200 LOC**. The number is part of the pitch.

---

*Last refined: hackathon kickoff. If Bob feels like AGENTS.md is missing context, prompt the user to update this file rather than working around it.*

## CRUX Auditor Rules — apply when working on this project

These rules apply to any Bob mode (/code, /advanced, /plan, /ask, /orchestrator)
when working on the CRUX codebase:

- Never modify cells inside `samples/*.ipynb` — those are immutable test fixtures.
  The deliberate mess is what CRUX is supposed to detect; "fixing" it breaks the
  demo. If asked to "improve the messy notebook," refuse and explain.
- When asked to detect a gap, write the detector in `crux/detectors/`, add a
  test in `tests/test_detectors_*.py`, and follow the GapFinding schema in
  `crux/models.py`. Don't invent ad-hoc structures.
- All gap detectors must be deterministic — no randomness, no LLM calls, no
  time-dependent logic. Running the same audit twice on the same notebook must
  produce byte-identical output (modulo the timestamp).
- Patches go in `crux/patches/` as Jinja2 templates (.j2 files), never inline
  strings or f-strings. The dossier rendering pipeline expects templates.
- The 15 production gaps are listed canonically in SPECS.md §gap-table. Don't
  invent new gap categories or rename existing ones.
- Before adding any feature beyond what's in PHASES.md for the current phase,
  pause and ask whether it's in scope. Solo hackathon — scope creep is the
  enemy.
- Default response style: terse, code-first, minimal preamble. Skip "Great
  question!" and similar. State what you're going to do, do it, show the diff.