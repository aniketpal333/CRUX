# PHASES.md — the 48-hour solo build plan

> Hour-by-hour. Bobcoin spend tracked at every checkpoint. Cuts pre-defined for every slip-condition. **Read this once at hour 0 and once at hour 24.** Don't re-plan the build; execute the plan.

---

## The macro view

| Phase | Hours | Bobcoins | Output checkpoint |
|---|---|---|---|
| **0 — Setup** | 0–3 | ~2 | Repo bootstrapped, AGENTS.md refined, three samples picked |
| **1 — Intent Recovery** | 3–14 | ~12 | All three samples produce a clean `recovered_pipeline.py` |
| **2 — Production Audit** | 14–24 | ~10 | All 15 gaps detect; autopatches produce a runnable service |
| **3 — MCP Server** | 24–32 | ~6 | Bob calls the server live; CI workflow blocks a merge |
| **4 — Dossier polish + stakeholder template** | 32–38 | ~4 | Stakeholder summary renders deterministically; dossier HTML is demo-ready |
| **5 — Demo polish** | 38–44 | 0 (no Bob) | Demo rehearsed 3x clean; backup video recorded |
| **6 — Submit** | 44–48 | 0 | bob_sessions/ populated; final commit pushed; submission filed ≥2h before deadline |

**Bobcoin total planned: ~34 / 40 Bobcoins.** The remaining 6 are the demo-day reserve.

---

## Phase 0 — Setup (Hours 0–3, ≈2 Bobcoins)

### Hour 0
- [ ] Confirm hackathon Bob account is active. Check ibm-coding-challenge-xxx is the selected team in Bob IDE settings (not your personal account).
- [ ] Confirm 40 Bobcoins are showing in the budget meter.
- [ ] Confirm GitHub account is set up and you can push to a public repo. (CRUX has no IBM Cloud or watsonx.ai dependency — the entire stack runs locally.)
- [ ] Create the GitHub repo. Public. Apache 2.0 license. Push an empty initial commit.

### Hour 1
- [ ] Clone empty repo locally. Open in Bob IDE. Trust the folder.
- [ ] Run `/init` in Bob's chat panel. Bob will scan the empty repo and propose AGENTS.md files. Approve.
- [ ] Replace the auto-generated root AGENTS.md with the AGENTS.md from this docs bundle. Save.
- [ ] Create `.bobignore` (see ARCHITECTURE.md §5).
- [ ] Add CLAUDE.md alongside AGENTS.md (mirror).

### Hour 2
- [ ] Create `samples/` directory.
- [ ] Pick three Kaggle notebooks (or write quick mock-ups). Suggested topics: a binary classification (Titanic-style), a regression (house prices), and one with explicit "tried multiple approaches" structure (any notebook tagged `eda` and `model-comparison`).
- [ ] Save them as `01_clean.ipynb`, `02_messy.ipynb`, `03_chaos.ipynb`. Add `samples/PROVENANCE.md` listing the source URL and license for each.
- [ ] **Read each one yourself for ten minutes.** You need to know what "good intent recovery" looks like on each before tuning the heuristic.

### Hour 3 — Phase 0 checkpoint
- [ ] `pyproject.toml` exists with all deps from ARCHITECTURE.md §3.
- [ ] `uv sync` runs cleanly.
- [ ] `pytest --collect-only` shows zero tests but no errors.
- [ ] You can articulate the 30-second pitch to a stranger from memory.
- [ ] **First Bob session exported to `bob_sessions/`.** Get this habit started early.

**Bobcoin spend at Hour 3: ~2.** If you're at 4+, you over-explored the repo with Bob. Slow down.

---

## Phase 1 — Intent Recovery (Hours 3–14, ≈12 Bobcoins)

The biggest, riskiest phase. Build the simplest version end-to-end first, then tune.

### Hour 3–5: skeletons
- [ ] Create `skills/notebook-narrative/SKILL.md`. Copy from this docs bundle's planned content.
- [ ] Create empty `parse_notebook.py`, `lineage_graph.py`, `narrative_scorer.py`, `classifier.py`, `pipeline_writer.py`, `intent_report.py`.
- [ ] Ask Bob (Plan mode) to read SPECS.md §2 and produce a plan for `parse_notebook.py` only. Review. Switch to Code mode. Implement.
- [ ] Write a smoke test: `parse_notebook(samples/01_clean.ipynb)` returns the right number of cells.

### Hour 5–8: lineage and narrative scoring
- [ ] Implement `lineage_graph.py`. The `_extract_defines_uses` AST visitor is the only tricky bit. Test against three hand-crafted cells where you know the expected names.
- [ ] Implement `narrative_scorer.py`. The regex constants in SPECS.md are the contract. Don't over-engineer them — the demo cares about precision on three samples, not recall on all notebooks.

### Hour 8–11: classifier + writer (the first end-to-end)
- [ ] Implement `classifier.py`. **This is the heuristic-tuning module.** Combine the three signals with weights. First-cut weights: execution_count 0.4, narrative 0.4, lineage 0.2. Iterate.
- [ ] Implement `pipeline_writer.py`. Stitch load-bearing cells in topological order. Consolidate imports.
- [ ] Implement `intent_report.py`. The output format is in SPECS.md §3 — a markdown table with a summary line.
- [ ] Run end-to-end on `01_clean.ipynb`. Verify outputs are sensible.

### Hour 11–14: tune against all three samples
- [ ] Run on `02_messy.ipynb`. Expect over-aggressive deletion or under-aggressive deletion. Tune weights. **Do not re-architect.** Just adjust constants.
- [ ] Run on `03_chaos.ipynb`. Expect lower confidence; that's fine. The intent_report should explicitly say `(no narrative cues — confidence reduced)` for cells with weak signals.
- [ ] Phase 1 checkpoint:
    - [ ] All three samples produce a `recovered_pipeline.py` that imports without errors
    - [ ] `intent_report.md` for `02_messy.ipynb` is the document a senior engineer can scan in 30 seconds
    - [ ] You can demo "messy notebook → clean pipeline in 30 seconds" cleanly

**Bobcoin spend at Hour 14: ~14 cumulative.** If you're at 18+, you're over-iterating. Lock the heuristic and move on.

### Cut conditions for Phase 1
If by **Hour 12** the messy notebook is still misclassifying load-bearing cells, lock the heuristic with the weights it has, and demo on `01_clean.ipynb` instead. The demo on a clean notebook still tells the right story; you just lose some impact on the wow #1 moment.

---

## Phase 2 — Production Audit (Hours 14–24, ≈10 Bobcoins)

### Hour 14–17: scaffolding
- [ ] Create `skills/production-audit/SKILL.md`.
- [ ] Create `audit_runner.py`. Skeleton: imports each `gap_NN_*.py`, calls `detect()`, collects `Finding`s, writes dossier.
- [ ] Create `findings.py` with the `Finding` Pydantic model (see SYSTEM_DESIGN.md §3).
- [ ] Create stub files for all 15 gaps (`gap_01_input_validation.py` through `gap_15_no_dockerfile.py`). Each just returns a placeholder Finding.
- [ ] Run audit_runner against `02_messy.ipynb`'s recovered pipeline. Verify it produces a 15-section dossier (all stubbed).

### Hour 17–20: implement the autopatch gaps (1, 2, 3, 4, 5, 6, 9, 13, 14, 15)
Implement in roughly this order — easiest first, builds momentum:
- [ ] **Gap 9 (hardcoded paths/secrets)**: regex for absolute paths and high-entropy strings. Easy win.
- [ ] **Gap 4 (missing model graceful degradation)**: AST search for joblib.load / pickle.load / torch.load. Wrap the call.
- [ ] **Gap 1 + 2 (input/output Pydantic)**: heuristic to find training df and infer dtypes. Render with jinja.
- [ ] **Gap 5 (model versioning)**: append `model_version` field to the response model template.
- [ ] **Gap 13 (repro metadata)**: same template, larger metadata block.
- [ ] **Gap 6 (logging)**: replace `print` calls with `structlog` calls. Add `request_id` middleware to the FastAPI service template.
- [ ] **Gap 15 (Dockerfile)**: render the template. Multi-stage. python:3.11-slim base.
- [ ] **Gap 14 (parity tests)**: this is the biggest one. Implement `parity_test_generator.py`. Sample 100 rows from the training df, run the recovered pipeline, pickle expected outputs, generate the test.
- [ ] **Gap 3 (train/serve skew)**: detect `ColumnTransformer` or pandas pipeline. Extract to `preprocessor.py`. Verify it pickles cleanly.

### Hour 20–22: the decision gaps (7, 8, 10, 11, 12)
These don't autopatch (or only partially). Each one writes an entry to `decision_log.md` in the SPECS.md §3 format.
- [ ] Gap 7 (input range): A=warn / B=reject / C=clip
- [ ] Gap 8 (drift): A=hourly / B=real-time / C=defer
- [ ] Gap 10 (rate limit): autopatch timeout decorator; decide rate-limit strategy A/B/C
- [ ] Gap 11 (batch endpoint): A=scaffold sync / B=scaffold streaming / C=defer
- [ ] Gap 12 (auth): A=API key / B=OAuth scaffold / C=defer

### Hour 22–24: end-to-end smoke test
- [ ] Run `crux audit samples/02_messy.ipynb` end to end. Verify all artifacts are produced in `out/02_messy/`.
- [ ] Run the parity test. It should pass (or, if you intentionally broke something, fail loudly with a diff).
- [ ] Build the Docker image: `docker build out/02_messy/`. Verify it builds.
- [ ] Run the service locally: `docker compose -f out/02_messy/docker-compose.yml up`. Hit `/predict` with curl. Verify a sane response.
- [ ] Phase 2 checkpoint:
    - [ ] `audit_dossier.md` looks like a senior consultant's deliverable, not a linter output
    - [ ] `decision_log.md` has at least 4 open decisions with A/B/C
    - [ ] `out/02_messy/` is shippable: dockerized, tested, with a clear contract

**Bobcoin spend at Hour 24: ~24 cumulative.** If you're at 30+, you went too deep on autopatch quality. Move on.

### Cut conditions for Phase 2
If by **Hour 22** at least 10 of 15 gaps don't have working detectors, lock what you have and ship the demo with what you've got. The pitch becomes "12 of 15 gaps detected and patched" instead of "all 15." Judges will not subtract points for honest scope.

---

## Phase 3 — MCP Server (Hours 24–32, ≈6 Bobcoins)

### Hour 24–27: server skeleton
- [ ] Add `fastmcp>=3.2` to deps if not already there.
- [ ] Implement `mcp_server/server.py` with three tools first: `audit_notebook`, `get_dossier`, `list_open_decisions`. Total ~80 LOC.
- [ ] Implement `mcp_server/models.py` with the Pydantic I/O models from SPECS.md §4.
- [ ] Implement `mcp_server/tools.py` with thin wrappers around `skills/`.
- [ ] Smoke test: `uv run mcp dev mcp_server/server.py` opens MCP Inspector. Manually call each of the three tools.

### Hour 27–29: register with Bob
- [ ] Edit Bob's MCP config (see MCP_SETUP.md §3 for the exact JSON snippet). Use `command: uv` and `args: ["run", "mcp_server/server.py"]` with absolute path.
- [ ] Restart Bob. Verify CRUX shows up in the MCP servers list in Bob settings.
- [ ] Test from inside Bob: ask Bob "audit `@samples/01_clean.ipynb` using the crux MCP server." Bob should call `audit_notebook` and report results.

### Hour 29–31: the remaining two tools + the CI gate
- [ ] Implement `compare_notebooks(before, after)`. This is the easiest of the five.
- [ ] Implement `block_merge_if_critical_gaps(notebook_id)`. Reads cached `AuditResult` from `out/`, returns the boolean + list.
- [ ] Write `ci/block-on-gaps.yml` GitHub Actions workflow:
    - Triggers on `pull_request` paths matching `*.ipynb`
    - Sets up Python, runs `uv sync`
    - Starts the MCP server in background (with `&`)
    - Calls `block_merge_if_critical_gaps` over Streamable HTTP via curl + jq
    - Exits non-zero if `allow_merge == false`
- [ ] Test the workflow locally with `act` (a GitHub Actions local runner) or `python ci/local_block_check.py samples/03_chaos.ipynb` if `act` is fussy.

### Hour 31–32: dry-run the demo flow
- [ ] On a clean machine state, run the full demo flow:
    1. Open Bob, point at `02_messy.ipynb`
    2. Verify intent recovery wow moment
    3. Verify audit dossier wow moment
    4. Trigger the CI gate, verify the red ❌
- [ ] Time it. Should be under 5 minutes. If it's not, find the slow step and fix it.

**Bobcoin spend at Hour 32: ~28 cumulative.** Remaining: ~12. That's the buffer for Phase 4 + demo retries (split roughly 4 / 8).

### Cut conditions for Phase 3
If by **Hour 30** the MCP server isn't talking to Bob cleanly, **demo it via curl from the terminal** instead. The judges care that it works, not that it's wired into Bob. The story is still intact.

---

## Phase 4 — Dossier polish + stakeholder summary template (Hours 32–38, ≈4 Bobcoins)

> **Earlier drafts of this plan called for a watsonx.ai capstone here.** That feature was cut in favor of a deterministic Jinja2 template — a CI artifact must be byte-identical across runs, which an LLM cannot guarantee. The hours that would have gone to watsonx integration now go to making the dossier itself a more compelling demo asset. This is a strict win.

### What this delivers
1. A polished `dossier.html` that renders cleanly on the demo screen-share — color-coded gaps, expandable decision options, citations linking each entry back to the source notebook cell.
2. The deterministic stakeholder summary at the top of the dossier, rendered from `templates/stakeholder_summary.md.j2` over the structured `AuditResult` (verdict, cell counts, gap counts, blocker list, decision list).
3. Optionally: the third sample notebook (`03_chaos.ipynb`) wired up end-to-end so judges can see CRUX handle a much messier input.

### Hour 32–34: stakeholder summary template

The template lives at `templates/stakeholder_summary.md.j2`. It takes the structured audit result and emits a 3-section Markdown summary: **Verdict** (one of CLEAN / READY_WITH_DECISIONS / BLOCKED), **What was in the notebook** (cell counts), **What the audit found** (gap dispositions + blocker list + decision list).

- [ ] Place the template at `templates/stakeholder_summary.md.j2` (the version shipped with these docs is a good starting point).
- [ ] In `mcp_server/dossier.py`, build a `summary_context` dict from the `AuditResult` and render the template with `jinja2.Environment(loader=FileSystemLoader("templates")).get_template(...).render(**summary_context)`.
- [ ] Embed the rendered Markdown in the top of `dossier.html` (use `markdown` library or a simple `<pre>` wrapper).
- [ ] Run the renderer on `02_messy.ipynb` and confirm the summary reads naturally for all three verdict states (you'll need to mock at least one CLEAN case).
- [ ] **Determinism test:** run the audit twice on `02_messy.ipynb` and `diff` the two rendered dossiers. They must be byte-identical. If they aren't, find the source of nondeterminism (timestamps, set ordering, hash randomization) and fix it.

### Hour 34–36: dossier HTML polish

- [ ] Color-code gaps by severity in the dossier table (red blocker, amber decision, green auto-patched).
- [ ] Make every gap entry expandable to show the cited cell, line number, and proposed patch diff (or option list for decisions).
- [ ] Add a one-click "back to source notebook" link from each gap entry — opens the original `.ipynb` cell in a new tab.
- [ ] Make the verdict banner *visually loud* — full-width colored bar at the top of the page. This is what a judge's eye lands on first.
- [ ] Print to PDF and check it looks good there too — some judges may save the dossier rather than view it live.

### Hour 36–38: third sample (stretch) or extra polish

If the dossier is sharp by Hour 36, spend the remaining ~2 hours on whichever of these adds more demo value:

**Option A — Wire up `03_chaos.ipynb`.** A 3rd sample with 80+ cells and genuinely chaotic structure. If CRUX handles it well, you can flash it during the demo as proof the system isn't tuned to one notebook. Risk: if it crashes, you've spent the time for nothing.

**Option B — Add `compare_notebooks` MCP tool polish.** The tool exists but might be rough. Make it produce a side-by-side dossier diff so a judge can see what changed when the developer re-ran the audit after fixing a blocker.

**Option C — Demo-day kit.** Pre-record the backup video. Pre-stage the failing PR. Write the Q&A flashcard. This is unglamorous but moves the needle more than feature work in many cases.

Pick one. Don't try all three.

### Cut conditions for Phase 4
**At Hour 36, if the stakeholder template isn't rendering cleanly, fall back to a static heading and skip the rest.** The dossier HTML must work — the summary template is a polish item that can be reduced to "no summary, just the gap table" without losing the demo.

---

## Phase 5 — Demo polish (Hours 38–44, 0 Bobcoins)

This phase is **all you, no Bob.** Your fingers, your demo machine, your script.

### Hour 38–40: write the demo script word for word
- [ ] Open `DEMO_SCRIPT.md`. Read it.
- [ ] Adapt the script to your specific samples and the actual artifacts you produced.
- [ ] Run through it once at your desk, narrating to yourself.
- [ ] Identify the three steps most likely to break. Build fallback plans for each.

### Hour 40–42: rehearse three times clean
- [ ] Reset the machine state (delete `out/`, kill any background MCP servers, close all Bob conversations).
- [ ] Run the demo, narrating aloud, timed. Should be 4:30–5:00.
- [ ] If anything went wrong, fix it. Repeat.
- [ ] Do this three full clean run-throughs, end-to-end, with the timer running.

### Hour 42–43: record the backup video
- [ ] Open OBS Studio. Record the screen + your audio.
- [ ] Run the demo cleanly one final time, recording. **No edits.** Save as `bob_sessions/demo_backup.mp4`.
- [ ] If the live demo crashes during the actual judging, you switch to the video without panicking.

### Hour 43–44: README polish
- [ ] Open `README.md`. Read it as if you're a judge with 60 seconds.
- [ ] Tighten anything verbose. Make sure the three uniqueness pillars are visible above the fold.
- [ ] Add a `## Demo` section with a single screenshot or GIF of the audit dossier (this is the most demo-able single artifact).

---

## Phase 6 — Submit (Hours 44–48, 0 Bobcoins)

### Hour 44–46: the bob_sessions/ folder (the deliverable that gets people disqualified)
- [ ] In Bob IDE, open the History panel.
- [ ] For every meaningful task you did during the build (intent recovery, audit, MCP server, dossier polish), find it in the history.
- [ ] For each task: take a screenshot of the consumption summary → save to `bob_sessions/screenshots/<NN>-<slug>.png`.
- [ ] For each task: click the export icon → save the markdown task history to `bob_sessions/exports/<NN>-<slug>.md`.
- [ ] Add `bob_sessions/README.md` indexing what's in there.
- [ ] **Sanity-scan `bob_sessions/` for any accidentally-pasted secrets.** CRUX has no runtime credentials, but Bob conversations might still capture stray API keys or tokens you pasted while debugging unrelated tools. Search for `api_key`, `bearer`, `eyJ` (JWT prefix), and any 32+ character random strings. Redact if found.

### Hour 46–47: final commit
- [ ] `git status` and `git diff` — review every changed file. Ensure no `.env`, no API keys, no client data.
- [ ] Tag: `git tag v1.0-hackathon-submission`
- [ ] Push to GitHub. Verify the public repo looks right (README renders, samples are present, bob_sessions is populated).
- [ ] Visit the repo page at github.com — does it look submission-ready in a 10-second skim?

### Hour 47–48: submit
- [ ] On the hackathon submission portal, paste the GitHub repo URL.
- [ ] Paste the project description (use the README's 30-second pitch verbatim).
- [ ] Add the demo video link if the platform allows.
- [ ] Submit.
- [ ] **Verify the submission shows as accepted.** Take a screenshot of the confirmation.

**Submit at least 2 hours before the deadline.** Submission portals fail. Networks drop. This is non-negotiable.

---

## Cuts, ranked by what to cut first

If you fall behind at any point, cut in this order:

1. **Sample 03 (chaos)** — drop from the demo. Demo on `02_messy` only.
2. **Phase 4 dossier HTML polish** — keep the stakeholder template (already shipped, near-zero cost) but skip the color-coding and expandable-row styling. Plain rendered Markdown is judging-acceptable.
3. **The MCP-Bob wiring** — demo via curl + MCP Inspector instead of through Bob's MCP integration.
4. **2 of the 5 MCP tools** — keep `audit_notebook`, `get_dossier`, `block_merge_if_critical_gaps`. Drop `compare_notebooks`, `list_open_decisions`.
5. **3 of the 15 gaps (cut the decision-only ones first)** — keep all autopatches; drop gaps 11 (batch), 8 (drift), 12 (auth) decision-log entries if needed.

**Never cut**:
- The narrative-intent-recovery wow moment
- The audit dossier
- The `bob_sessions/` folder
- The MCP server existing at all (even if not wired to Bob)

---

## What "done" looks like at Hour 48

- [ ] Public GitHub repo with the 13 docs, all source, samples, tests
- [ ] `bob_sessions/` populated with screenshots and exports
- [ ] Demo video recorded as backup
- [ ] Demo rehearsed clean three times
- [ ] Submission portal shows confirmed
- [ ] At least 2 hours of buffer between submit-time and deadline
- [ ] You have eaten, slept (briefly), and you can articulate the pitch one more time

That's the win condition. Execute the plan.

---

*If you're reading this at hour 30 panicking about hour 14's checkpoints, breathe — refer back to the cut hierarchy and ship the version of CRUX you have.*
