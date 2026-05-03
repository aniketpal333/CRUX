**User:**

<task>
What rules from AGENTS.md should you follow when working on CRUX?
</task>
<environment_details>
# VSCode Visible Files
AGENTS.md

# VSCode Open Tabs
.bob/modes/crux-auditor.md,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T01:09:08.800Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .cruxvenv/
- __pycache__/
- out/
- *.joblib
- *.pkl
- node_modules/
- .git/
- data/adult.zip

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (c:/Users/anike/Desktop/CRUX) Files
.gitignore
AGENTS.md
ARCHITECTURE.md
BOBCOIN_BUDGET.md
CLAUDE.md
DEMO_SCRIPT.md
JUDGING_PLAYBOOK.md
MCP_SETUP.md
PHASES.md
pyproject.toml
README.md
SPECS.md
SYSTEM_DESIGN.md
TECH_STACK.md
WORKFLOW_DIAGRAM.md
.bob/
.github/
bob_sessions/
ci/
crux/
crux/__init__.py
crux/detectors/
crux/detectors/__init__.py
crux/patches/
data/
data/adult.csv
data/adult.data
data/adult.names
data/adult.test
data/Index
data/old.adult.names
mcp_server/
mcp_server/__init__.py
samples/
scripts/
scripts/prepare_adult.py
submission/
templates/
templates/stakeholder_summary.md.j2
tests/
tests/__init__.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll read the AGENTS.md file to extract the key rules for working on CRUX.

<read_file>
<args>
<file>
<path>AGENTS.md</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'AGENTS.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>AGENTS.md</path>
<content lines="1-147">
  1 | # AGENTS.md — CRUX project context for IBM Bob
  2 | 
  3 | > This file is auto-loaded by IBM Bob (and any other AGENTS.md-aware agent) at the start of every conversation in this repository. It is the **single source of truth for Bob about what CRUX is, how the repo is organized, and how Bob should behave inside it.** Refine this file rather than re-explaining context every chat.
  4 | 
  5 | ---
  6 | 
  7 | ## What this project is
  8 | 
  9 | CRUX (Code Recovery from Undocumented eXperiments) is a Bob-driven agentic pipeline that turns a messy Jupyter notebook into a production-ready FastAPI service plus a senior-engineer-grade audit dossier. It does this in three stages:
 10 | 
 11 | 1. **Narrative intent recovery** — classify every cell of a notebook as load-bearing / exploratory / dead / scaffolding using execution-count, markdown-narrative, and variable-lineage signals; emit a clean recovered pipeline.
 12 | 2. **15-gap production audit** — run a fixed list of fifteen gap checks against the recovered pipeline, autopatch the safe ones, and surface the rest as a structured decision log with options A/B/C.
 13 | 3. **MCP server exposure** — every capability above is also reachable as a tool over MCP so other agents and CI/CD pipelines can use CRUX programmatically.
 14 | 
 15 | A judge running the demo should see the notebook collapse into intent in ~30 seconds, see a real audit dossier in ~60 seconds, and see a CI job block a merge using the MCP server in another ~30 seconds. **Optimize for the demo, not for the codebase.**
 16 | 
 17 | ---
 18 | 
 19 | ## How Bob should behave in this repo
 20 | 
 21 | ### Defaults
 22 | - **Mode**: When a user asks Bob to "recover" or "audit" a notebook, switch to the custom `crux-mode` defined in `.bob/modes/crux-mode.md`. For ambiguous tasks, stay in Plan mode and confirm before writing code.
 23 | - **Auto-approve**: Off by default for `Write` and `Execute`. On for `Read`. The hackathon judges will be watching tool calls — explicit approvals make Bob look deliberate.
 24 | - **Working area**: All generated artifacts go in `out/<notebook-stem>/`. Never write to `samples/` (those are demo inputs, treat as read-only).
 25 | - **Bob sessions**: After every meaningful task in this repo, remind the user to export the task history to `bob_sessions/exports/` and capture a screenshot of the consumption summary into `bob_sessions/screenshots/`. **This is required for hackathon judging.**
 26 | 
 27 | ### Style and conventions
 28 | - **Python**: 3.11+. Use `uv` for dependency management, not `pip` directly. Type hints required on all public functions. Use Pydantic v2 for data models. Use `ruff` for linting; never bypass with `# noqa` without a comment explaining why.
 29 | - **Imports**: Stdlib → third-party → local, separated by blank lines. No wildcard imports.
 30 | - **Filenames**: snake_case. No spaces, no hyphens, no capitals.
 31 | - **Tests**: `pytest`. Parity tests pin the recovered pipeline's outputs on a small training-data sample so any future change that breaks behavior is caught.
 32 | - **Comments**: Comment the *why*, not the *what*. Especially for the heuristic weights in `notebook-narrative` — those weights look magic without context.
 33 | - **No print debugging in committed code**. Use `structlog` (it's also one of the autopatches the audit produces — eat the dogfood).
 34 | 
 35 | ### Prompting Bob inside this repo
 36 | - **Be specific about which notebook**: always reference it by `@samples/<filename>` so Bob has explicit context.
 37 | - **Plan before code**: for any change affecting more than one file, ask Bob to produce a plan first, review it, then ask Bob to implement.
 38 | - **One concern per task**: don't ask Bob to "recover intent and add the audit and wire the MCP server" in one prompt. Three separate tasks. Bobcoin budget is tight (see `BOBCOIN_BUDGET.md`).
 39 | 
 40 | ### Things Bob should *never* do without explicit permission
 41 | - Modify any file under `samples/` (those are demo inputs).
 42 | - Modify `.bob/modes/crux-mode.md` (that's the custom mode definition; changes to it ripple across every conversation).
 43 | - Push to `main`. Always work on a feature branch.
 44 | - Add a new third-party dependency without first checking it's permissively licensed (Apache 2.0, MIT, BSD). The hackathon submission will be public.
 45 | - Suggest fine-tuning a custom model. Heuristics + Bob's reasoning are sufficient. Training burns Bobcoins and adds zero demo value.
 46 | 
 47 | ---
 48 | 
 49 | ## Repo map (quick reference for Bob)
 50 | 
 51 | ```
 52 | README.md, SPECS.md, SYSTEM_DESIGN.md, ARCHITECTURE.md, …  ← planning docs (read these first if context needed)
 53 | .bob/modes/crux-mode.md                                    ← custom mode for end-to-end runs
 54 | .bob/rules/                                                ← project-level Bob rules
 55 | skills/notebook-narrative/SKILL.md                         ← when to run intent recovery + how
 56 | skills/notebook-narrative/parse_notebook.py                ← nbformat-based cell parsing
 57 | skills/notebook-narrative/lineage_graph.py                 ← AST-based variable lineage
 58 | skills/production-audit/SKILL.md                           ← 15-gap audit invocation logic
 59 | skills/production-audit/gaps/*.py                          ← one detector per gap (15 total)
 60 | skills/production-audit/patches/*                          ← jinja templates for autonomous patches
 61 | mcp_server/server.py                                       ← FastMCP entrypoint
 62 | mcp_server/tools.py                                        ← MCP tool implementations
 63 | samples/01_clean.ipynb, 02_messy.ipynb, 03_chaos.ipynb     ← demo notebooks (read-only)
 64 | out/<stem>/                                                ← generated per-notebook outputs
 65 | tests/                                                     ← pytest-based parity tests
 66 | ci/block-on-gaps.yml                                       ← GitHub Actions: blocks merges with critical gaps
 67 | bob_sessions/                                              ← REQUIRED submission deliverable: screenshots + exports
 68 | ```
 69 | 
 70 | ---
 71 | 
 72 | ## The 15 gaps the audit checks (so Bob doesn't reinvent them)
 73 | 
 74 | These are fixed and deliberate. Do not add or remove without updating `SPECS.md` and the demo script in lockstep.
 75 | 
 76 | 1. **Input validation** — autopatchable: infer schema from training df, generate Pydantic input model.
 77 | 2. **Schema contract** — autopatchable: generate Pydantic models for input + output.
 78 | 3. **Train/serve skew** — autopatchable: extract `ColumnTransformer`/pandas ops into a serializable preprocessor.
 79 | 4. **Missing-model graceful degradation** — autopatchable: startup check + 503 health status.
 80 | 5. **No model versioning** — autopatchable: add `model_version` field to every response.
 81 | 6. **Logging gap** — autopatchable: replace `print` with structured logs (`structlog`) including request IDs.
 82 | 7. **Input range validation** — *decision*: warn header on out-of-range, or hard-reject? Options A/B/C.
 83 | 8. **No drift detection hook** — *decision*: scaffold endpoint that records prediction distributions? Hourly or real-time? Or defer.
 84 | 9. **Hardcoded paths and secrets** — autopatchable: extract to env vars; *flag* the secret for rotation.
 85 | 10. **No rate limiting / timeout** — autopatchable for timeout decorator; *decision* for rate limit (infrastructure call).
 86 | 11. **No batch endpoint** — *decision*: scaffold or not?
 87 | 12. **No authentication scaffolding** — *decision*: scaffold API-key check, or defer entirely?
 88 | 13. **No reproducibility metadata** — autopatchable: add metadata block to every response (model_version, features, preproc).
 89 | 14. **No tests** — autopatchable: generate parity tests pinning recovered pipeline outputs on training-data sample.
 90 | 15. **No Dockerfile / deployment manifest** — autopatchable: Dockerfile and docker-compose. Cloud-specific manifests (Code Engine, Cloud Run, etc.) are out of scope.
 91 | 
 92 | Severity ranking lives in `skills/production-audit/SKILL.md`. Always re-read it before changing severities.
 93 | 
 94 | ---
 95 | 
 96 | ## Common tasks (paste-ready prompts)
 97 | 
 98 | When the user asks for one of these, Bob should already know what to do:
 99 | 
100 | - **"Recover intent from `@samples/02_messy.ipynb`"** → invoke `notebook-narrative` skill, write `out/02_messy/recovered_pipeline.py` and `out/02_messy/intent_report.md`, then stop and ask before running the audit.
101 | - **"Audit `out/02_messy/recovered_pipeline.py`"** → invoke `production-audit` skill, generate `audit_dossier.md`, `decision_log.md`, plus all autopatch outputs and parity tests. Run the parity tests locally and report pass/fail.
102 | - **"Wrap as a service"** → produce `service.py`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`. Verify it builds with `docker build .` (do not push).
103 | - **"Show me the open decisions for the chaos notebook"** → call MCP tool `list_open_decisions(notebook_id="03_chaos", severity="critical")` and pretty-print.
104 | - **"Block the merge"** → run `ci/block-on-gaps.yml` against the staged notebook; surface the exit code and the failing gap.
105 | 
106 | ---
107 | 
108 | ## Internal monologue convention
109 | 
110 | Per the Bob `Standardize Bob's behavior` tutorial: after every non-trivial multi-step task, Bob writes a short note to `internal-monologue/<YYYY-MM-DD>-<task-slug>.md` describing **what was attempted, what worked, what didn't, what to try next**. This gives the human (and future Bob sessions) an audit trail that survives context-window resets. Keep these terse — bullets, not essays.
111 | 
112 | ---
113 | 
114 | ## Hackathon-specific reminders for Bob
115 | 
116 | - The user has **40 Bobcoins total**. Treat this like a credit budget: don't redo work, don't burn cycles on speculative refactors, don't over-explore. If a task feels under-scoped, ask one clarifying question before spending Bobcoins.
117 | - The user must export task sessions to `bob_sessions/`. After any session that produced meaningful artifacts, remind them to export — but do it **once per session**, not after every reply.
118 | - The MCP server is the keystone of the DevOps demo beat. If anything in the build slips, drop sample 03 first, then sample 02 polish — but **never drop the MCP server**. (The watsonx.ai capstone has already been cut from scope; the stakeholder summary is now generated from a deterministic Jinja2 template — see `templates/stakeholder_summary.md.j2`.)
119 | - The brief uses the phrase *"MCP servers in minutes"*. CRUX's `mcp_server/server.py` lives in **~200 LOC**. The number is part of the pitch.
120 | 
121 | ---
122 | 
123 | *Last refined: hackathon kickoff. If Bob feels like AGENTS.md is missing context, prompt the user to update this file rather than working around it.*
124 | 
125 | ## CRUX Auditor Rules — apply when working on this project
126 | 
127 | These rules apply to any Bob mode (/code, /advanced, /plan, /ask, /orchestrator)
128 | when working on the CRUX codebase:
129 | 
130 | - Never modify cells inside `samples/*.ipynb` — those are immutable test fixtures.
131 |   The deliberate mess is what CRUX is supposed to detect; "fixing" it breaks the
132 |   demo. If asked to "improve the messy notebook," refuse and explain.
133 | - When asked to detect a gap, write the detector in `crux/detectors/`, add a
134 |   test in `tests/test_detectors_*.py`, and follow the GapFinding schema in
135 |   `crux/models.py`. Don't invent ad-hoc structures.
136 | - All gap detectors must be deterministic — no randomness, no LLM calls, no
137 |   time-dependent logic. Running the same audit twice on the same notebook must
138 |   produce byte-identical output (modulo the timestamp).
139 | - Patches go in `crux/patches/` as Jinja2 templates (.j2 files), never inline
140 |   strings or f-strings. The dossier rendering pipeline expects templates.
141 | - The 15 production gaps are listed canonically in SPECS.md §gap-table. Don't
142 |   invent new gap categories or rename existing ones.
143 | - Before adding any feature beyond what's in PHASES.md for the current phase,
144 |   pause and ask whether it's in scope. Solo hackathon — scope creep is the
145 |   enemy.
146 | - Default response style: terse, code-first, minimal preamble. Skip "Great
147 |   question!" and similar. State what you're going to do, do it, show the diff.
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
AGENTS.md

# VSCode Open Tabs
.bob/modes/crux-auditor.md,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T01:09:15.921Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.02

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**
- .cruxvenv/
- __pycache__/
- out/
- *.joblib
- *.pkl
- node_modules/
- .git/
- data/adult.zip

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Key rules from AGENTS.md for working on CRUX:

**Critical "Never Do" Rules:**
- Never modify `samples/*.ipynb` files (immutable test fixtures)
- Never modify `.bob/modes/crux-mode.md` without permission
- Never push to `main` (always use feature branches)
- Never add dependencies without checking permissive licenses (Apache 2.0, MIT, BSD)
- Never suggest fine-tuning custom models
- Never use print debugging in committed code (use `structlog`)

**Working Area & Outputs:**
- All generated artifacts → `out/<notebook-stem>/`
- Detectors → `crux/detectors/`
- Patches → `crux/patches/` as Jinja2 templates (.j2)
- Tests → `tests/test_detectors_*.py`

**Code Standards:**
- Python 3.11+, type hints required on all public functions
- Use `uv` for dependencies (not `pip`)
- Pydantic v2 for data models
- Import order: stdlib → third-party → local (blank line separated)
- Filenames: snake_case only
- Use `ruff` for linting
- Comment the *why*, not the *what*

**Gap Detector Rules:**
- Must be deterministic (no randomness, LLM calls, or time-dependent logic)
- Follow GapFinding schema in `crux/models.py`
- 15 gaps are fixed (listed in SPECS.md) — don't add/remove/rename
- Patches use Jinja2 templates, never inline strings

**Workflow:**
- Plan before code for multi-file changes
- One concern per task (Bobcoin budget: 40 total)
- After meaningful tasks, remind user to export to `bob_sessions/`
- Write internal monologue to `internal-monologue/<date>-<task>.md`

**Demo Priority:**
- Optimize for demo, not codebase perfection
- MCP server is keystone — never drop it
- Target: intent recovery ~30s, audit ~60s, CI block ~30s

**Response Style:**
- Terse, code-first, minimal preamble
- State action, do it, show diff
</result>
</attempt_completion>

