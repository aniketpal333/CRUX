**User:**

<task>Command 'init' (see below for command content)
</task>

<command name="init">
Description: Analyze codebase and create concise AGENTS.md files for AI assistants

<task>
Please analyze this codebase and create an AGENTS.md file containing:
1. Build/lint/test commands - especially for running a single test
2. Code style guidelines including imports, formatting, types, naming conventions, error handling, etc.
</task>

<initialization>
  <purpose>
    Create (or update) a concise AGENTS.md file that enables immediate productivity for AI assistants.
    Focus ONLY on project-specific, non-obvious information that you had to discover by reading files.
    
    CRITICAL: Only include information that is:
    - Non-obvious (couldn't be guessed from standard practices)
    - Project-specific (not generic to the framework/language)
    - Discovered by reading files (config files, code patterns, custom utilities)
    - Essential for avoiding mistakes or following project conventions
    
    Usage notes:
    - The file you create will be given to agentic coding agents (such as yourself) that operate in this repository
    - Keep the main AGENTS.md concise - aim for about 20 lines, but use more if the project complexity requires it
    - If there's already an AGENTS.md, improve it
    - If there are Claude Code rules (in CLAUDE.md), Cursor rules (in .cursor/rules/ or .cursorrules), or Copilot rules (in .github/copilot-instructions.md), make sure to include them
    - Be sure to prefix the file with: "# AGENTS.md\n\nThis file provides guidance to agents when working with code in this repository."
  </purpose>
  
  <todo_list_creation>
    If the update_todo_list tool is available, create a todo list with these focused analysis steps:
    
    1. Check for existing AGENTS.md files
       CRITICAL - Check these EXACT paths IN THE PROJECT ROOT:
       - AGENTS.md (in project root directory)
       - .bob/rules-code/AGENTS.md (relative to project root)
       - .bob/rules-advanced/AGENTS.md (relative to project root)
       - .bob/rules-ask/AGENTS.md (relative to project root)
       - .bob/rules-plan/AGENTS.md (relative to project root)
       
       IMPORTANT: All paths are relative to the project/workspace root, NOT system root!
       
       If ANY of these exist:
       - Read them thoroughly
       - CRITICALLY EVALUATE: Remove ALL obvious information
       - DELETE entries that are standard practice or framework defaults
       - REMOVE anything that could be guessed without reading files
       - Only KEEP truly non-obvious, project-specific discoveries
       - Then add any new non-obvious patterns you discover
       
       Also check for other AI assistant rules:
       - .cursorrules, CLAUDE.md, .roorules
       - .cursor/rules/, .github/copilot-instructions.md
    
    2. Identify stack
       - Language, framework, build tools
       - Package manager and dependencies
    
    3. Extract commands
       - Build, test, lint, run
       - Critical directory-specific commands
    
    4. Map core architecture
       - Main components and flow
       - Key entry points
    
    5. Document critical patterns
       - Project-specific utilities (that you discovered by reading code)
       - Non-standard approaches (that differ from typical patterns)
       - Custom conventions (that aren't obvious from file structure)
    
    6. Extract code style
       - From config files only
       - Key conventions
    
    7. Testing specifics
       - Framework and run commands
       - Directory requirements
    
    8. Compile/Update AGENTS.md files
       - If files exist: AGGRESSIVELY clean them up
         * DELETE all obvious information (even if it was there before)
         * REMOVE standard practices, framework defaults, common patterns
         * STRIP OUT anything derivable from file structure or names
         * ONLY KEEP truly non-obvious discoveries
         * Then add newly discovered non-obvious patterns
         * Result should be SHORTER and MORE FOCUSED than before
       - If creating new: Follow the non-obvious-only principle
       - Create mode-specific files in .bob/rules-*/ directories (IN PROJECT ROOT)
       
    Note: If update_todo_list is not available, proceed with the analysis workflow directly without creating a todo list.
  </todo_list_creation>
</initialization>

<analysis_workflow>
  Follow the comprehensive analysis workflow to:
  
  1. **Discovery Phase**:
     CRITICAL - First check for existing AGENTS.md files at these EXACT locations IN PROJECT ROOT:
     - AGENTS.md (in project/workspace root)
     - .bob/rules-code/AGENTS.md (relative to project root)
     - .bob/rules-advanced/AGENTS.md (relative to project root)
     - .bob/rules-ask/AGENTS.md (relative to project root)
     - .bob/rules-plan/AGENTS.md (relative to project root)
     
     IMPORTANT: The .roo folder should be created in the PROJECT ROOT, not system root!
     
     If found, perform CRITICAL analysis:
     - What information is OBVIOUS and must be DELETED?
     - What violates the non-obvious-only principle?
     - What would an experienced developer already know?
     - DELETE first, then consider what to add
     - The file should get SHORTER, not longer
     
     Also find other AI assistant rules and documentation
     
  2. **Project Identification**: Identify language, stack, and build system
  3. **Command Extraction**: Extract and verify essential commands
  4. **Architecture Mapping**: Create visual flow diagrams of core processes
  5. **Component Analysis**: Document key components and their interactions
  6. **Pattern Analysis**: Identify project-specific patterns and conventions
  7. **Code Style Extraction**: Extract formatting and naming conventions
  8. **Security & Performance**: Document critical patterns if relevant
  9. **Testing Discovery**: Understand testing setup and practices
  10. **Example Extraction**: Find real examples from the codebase
</analysis_workflow>

<output_structure>
  <main_file>
    Create or deeply improve AGENTS.md with ONLY non-obvious information:
    
    If AGENTS.md exists:
    - FIRST: Delete ALL obvious information
    - REMOVE: Standard commands, framework defaults, common patterns
    - STRIP: Anything that doesn't require file reading to know
    - EVALUATE: Each line - would an experienced dev be surprised?
    - If not surprised, DELETE IT
    - THEN: Add only truly non-obvious new discoveries
    - Goal: File should be SHORTER and MORE VALUABLE
    
    Content should include:
    - Header: "# AGENTS.md\n\nThis file provides guidance to agents when working with code in this repository."
    - Build/lint/test commands - ONLY if they differ from standard package.json scripts
    - Code style - ONLY project-specific rules not covered by linter configs
    - Custom utilities or patterns discovered by reading the code
    - Non-standard directory structures or file organizations
    - Project-specific conventions that violate typical practices
    - Critical gotchas that would cause errors if not followed
    
    EXCLUDE obvious information like:
    - Standard npm/yarn commands visible in package.json
    - Framework defaults (e.g., "React uses JSX")
    - Common patterns (e.g., "tests go in __tests__ folders")
    - Information derivable from file extensions or directory names
    
    Keep it concise (aim for ~20 lines, but expand as needed for complex projects).
    Include existing AI assistant rules from CLAUDE.md, Cursor rules (.cursor/rules/ or .cursorrules), or Copilot rules (.github/copilot-instructions.md).
  </main_file>
  
  <mode_specific_files>
    Create or deeply improve mode-specific AGENTS.md files IN THE PROJECT ROOT.
    
    CRITICAL: For each of these paths (RELATIVE TO PROJECT ROOT), check if the file exists FIRST:
    - .bob/rules-code/AGENTS.md (create .roo in project root, not system root!)
    - .bob/rules-advanced/AGENTS.md (relative to project root)
    - .bob/rules-ask/AGENTS.md (relative to project root)
    - .bob/rules-plan/AGENTS.md (relative to project root)
    
    IMPORTANT: The .roo directory must be created in the current project/workspace root directory,
    NOT at the system root (/) or home directory. All paths are relative to where the project is located.
    
    If files exist:
    - AGGRESSIVELY DELETE obvious information
    - Remove EVERYTHING that's standard practice
    - Strip out framework defaults and common patterns
    - Each remaining line must be surprising/non-obvious
    - Only then add new non-obvious discoveries
    - Files should become SHORTER, not longer
    
    Example structure (ALL IN PROJECT ROOT):
    ```
    project-root/
    ├── AGENTS.md                    # General project guidance
    ├── .bob/                        # IN PROJECT ROOT, NOT SYSTEM ROOT!
    │   ├── rules-code/
    │   │   └── AGENTS.md           # Code mode specific instructions
    │   ├── rules-advanced/
    │   │   └── AGENTS.md           # Advanced mode specific instructions
    │   ├── rules-ask/
    │   │   └── AGENTS.md           # Ask mode specific instructions
    │   └── rules-plan/
    │       └── AGENTS.md           # Plan mode specific instructions
    ├── src/
    ├── package.json
    └── ... other project files
    ```
    
    .bob/rules-code/AGENTS.md - ONLY non-obvious coding rules discovered by reading files:
    - Custom utilities that replace standard approaches
    - Non-standard patterns unique to this project
    - Hidden dependencies or coupling between components
    - Required import orders or naming conventions not enforced by linters
    - No access to tools like MCP and Browser
    
    Example of non-obvious rules worth documenting:
    ```
    # Project Coding Rules (Non-Obvious Only)
    - Always use safeWriteJson() from src/utils/ instead of JSON.stringify for file writes (prevents corruption)
    - API retry mechanism in src/api/providers/utils/ is mandatory (not optional as it appears)
    - Database queries MUST use the query builder in packages/evals/src/db/queries/ (raw SQL will fail)
    - Provider interface in packages/types/src/ has undocumented required methods
    - Test files must be in same directory as source for vitest to work (not in separate test folder)
    ```
    
    .bob/rules-advanced/AGENTS.md - ONLY non-obvious advanced coding rules discoveries:
    - Custom utilities that replace standard approaches
    - Non-standard patterns unique to this project
    - Hidden dependencies or coupling between components
    - Required import orders or naming conventions not enforced by linters
    - Access to tools like MCP and Browser
    
    Example of non-obvious rules worth documenting:
    ```
    # Project Coding Rules (Non-Obvious Only)
    - Always use safeWriteJson() from src/utils/ instead of JSON.stringify for file writes (prevents corruption)
    - API retry mechanism in src/api/providers/utils/ is mandatory (not optional as it appears)
    - Database queries MUST use the query builder in packages/evals/src/db/queries/ (raw SQL will fail)
    - Provider interface in packages/types/src/ has undocumented required methods
    - Test files must be in same directory as source for vitest to work (not in separate test folder)
    ```
    
    .bob/rules-ask/AGENTS.md - ONLY non-obvious documentation context:
    - Hidden or misnamed documentation
    - Counterintuitive code organization
    - Misleading folder names or structures
    - Important context not evident from file structure
    
    Example of non-obvious documentation rules worth documenting:
    ```
    # Project Documentation Rules (Non-Obvious Only)
    - "src/" contains VSCode extension code, not source for web apps (counterintuitive)
    - Provider examples in src/api/providers/ are the canonical reference (docs are outdated)
    - UI runs in VSCode webview with restrictions (no localStorage, limited APIs)
    - Package.json scripts must be run from specific directories, not root
    - Locales in root are for extension, webview-ui/src/i18n for UI (two separate systems)
    ```
    
    .bob/rules-plan/AGENTS.md - ONLY non-obvious architectural constraints:
    - Hidden coupling between components
    - Undocumented architectural decisions
    - Non-standard patterns that must be followed
    - Performance bottlenecks discovered through investigation
    
    Example of non-obvious architecture rules worth documenting:
    ```
    # Project Architecture Rules (Non-Obvious Only)
    - Providers MUST be stateless - hidden caching layer assumes this
    - Webview and extension communicate through specific IPC channel patterns only
    - Database migrations cannot be rolled back - forward-only by design
    - React hooks required because external state libraries break webview isolation
    - Monorepo packages have circular dependency on types package (intentional)
    ```
  </mode_specific_files>
</output_structure>

<quality_criteria>
  - ONLY include non-obvious information discovered by reading files
  - Exclude anything that could be guessed from standard practices
  - Focus on gotchas, hidden requirements, and counterintuitive patterns
  - Include specific file paths when referencing custom utilities
  - Be extremely concise - if it's obvious, don't include it
  - Every line should prevent a potential mistake or confusion
  - Test: Would an experienced developer be surprised by this information?
  - If updating existing files: DELETE obvious info first, files should get SHORTER
  - Measure success: Is the file more concise and valuable than before?
</quality_criteria>

Remember: The goal is to create documentation that enables AI assistants to be immediately productive in this codebase, focusing on project-specific knowledge that isn't obvious from the code structure alone.
</command>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:30:57.209Z
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
<slug>plan</slug>
<name>📝 Plan</name>


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

I'll analyze the CRUX codebase and create/update AGENTS.md files with only non-obvious, project-specific information discovered by reading the actual code and configuration files.

<update_todo_list>
<todos>
[ ] Check for existing AGENTS.md files in project root and .bob/rules-* directories
[ ] Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.)
[ ] Analyze project structure and identify stack/build tools
[ ] Extract non-obvious build/test/lint commands from config files
[ ] Discover project-specific code patterns and utilities
[ ] Document non-obvious architectural constraints
[ ] Create/update main AGENTS.md with critical cleanup
[ ] Create/update mode-specific AGENTS.md files in .bob/rules-* directories
</todos>
</update_todo_list>

<read_file>
<args>
  <file>
    <path>AGENTS.md</path>
  </file>
  <file>
    <path>CLAUDE.md</path>
  </file>
  <file>
    <path>pyproject.toml</path>
  </file>
  <file>
    <path>.gitignore</path>
  </file>
  <file>
    <path>SPECS.md</path>
    <line_range>1-100</line_range>
  </file>
</args>
</read_file>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
Tool [read_file] was not executed because a tool has already been used in this message. Only one tool may be used per message. You must assess the first tool's result before proceeding to use the next tool.
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:31:19.513Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.05

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Pending |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Pending |
| 3 | Analyze project structure and identify stack/build tools | Pending |
| 4 | Extract non-obvious build/test/lint commands from config files | Pending |
| 5 | Discover project-specific code patterns and utilities | Pending |
| 6 | Document non-obvious architectural constraints | Pending |
| 7 | Create/update main AGENTS.md with critical cleanup | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/rules-* directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>AGENTS.md</path>
  </file>
  <file>
    <path>CLAUDE.md</path>
  </file>
  <file>
    <path>pyproject.toml</path>
  </file>
  <file>
    <path>.gitignore</path>
  </file>
  <file>
    <path>SPECS.md</path>
    <line_range>1-100</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>AGENTS.md</path>
<content lines="1-123">
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
</content>
</file>
<file><path>CLAUDE.md</path>
<content lines="1-111">
  1 | # CLAUDE.md — CRUX project context for Claude (and other CLAUDE.md-aware assistants)
  2 | 
  3 | > This file mirrors [`AGENTS.md`](./AGENTS.md) but is named so that Claude Code, Cursor, and other Anthropic-aligned tooling auto-load it as project context. **Keep both files in sync** when refining; treat AGENTS.md as the canonical version and regenerate this one from it whenever the structure changes substantively.
  4 | 
  5 | ---
  6 | 
  7 | ## TL;DR for an assistant new to this repo
  8 | 
  9 | CRUX is a **solo, 48-hour, hackathon submission** for IBM Bob Dev Day. It is a Bob-driven agent that converts a messy Jupyter notebook into a production-ready FastAPI service plus a 15-gap audit dossier and a structured decision log, all reachable as MCP tools. The submission is judged on a **5-minute live demo**, so every architectural decision is biased toward demo clarity over engineering elegance.
 10 | 
 11 | If you, the assistant, are reading this without other context: read [`README.md`](./README.md) first, then [`SPECS.md`](./SPECS.md) for the cell-classification taxonomy and the 15-gap list, then [`PHASES.md`](./PHASES.md) for the hour-by-hour build order. Skip the rest unless asked.
 12 | 
 13 | ---
 14 | 
 15 | ## What CRUX does in three steps
 16 | 
 17 | 1. **Narrative intent recovery** — read the notebook as a *document* (execution counts + markdown narrative + variable lineage), classify each cell as load-bearing / exploratory / dead / scaffolding, emit a clean `recovered_pipeline.py` containing only the load-bearing cells stitched in dataflow order.
 18 | 2. **15-gap production-readiness audit** — run a fixed, severity-ranked checklist of fifteen gaps (input validation, train/serve skew, no logging, no model versioning, hardcoded secrets, no tests, no Dockerfile, …); autopatch the safe ones; surface the rest as a structured decision log with options A/B/C.
 19 | 3. **MCP server** — every capability above is also a tool over MCP (`audit_notebook`, `get_dossier`, `list_open_decisions`, `compare_notebooks`, `block_merge_if_critical_gaps`). A real GitHub Actions job calls it to refuse merges with unresolved critical gaps.
 20 | 
 21 | The differentiator vs. existing notebook-to-script tools (`nbconvert`, Jupytext, paid platforms): those treat a notebook as a flat list of cells and convert all of them. CRUX reads the notebook as a narrative artifact and recovers only what was meant to ship.
 22 | 
 23 | ---
 24 | 
 25 | ## Behavioral defaults the assistant should adopt
 26 | 
 27 | ### Be biased toward the demo
 28 | Every artifact CRUX generates has to look good when a judge reads it for ten seconds. Whenever there's a tension between engineering elegance and demo clarity, **pick demo clarity**. That means:
 29 | - Audit dossiers use ✅/⚠️/❌ at the top of each section so a judge can scan in five seconds
 30 | - Decision logs label options literally **A / B / C** with one-sentence trade-offs each
 31 | - The recovered pipeline is heavily commented even when the comments restate obvious things — judges read code differently from engineers
 32 | 
 33 | ### Be conservative with Bobcoins / API spend
 34 | The user has a 40-Bobcoin budget for the entire build. If a request is ambiguous, ask one short clarifying question rather than producing a speculative draft. Don't volunteer refactors. Don't add dependencies without checking the license.
 35 | 
 36 | ### Hard rules
 37 | - Never modify `samples/`. Read-only.
 38 | - Never push to `main`. Always feature branches.
 39 | - Never add a non-permissive dependency (Apache 2.0 / MIT / BSD only — submission is public).
 40 | - Never train a custom model. Heuristics + Bob's reasoning are sufficient. The stakeholder summary in the dossier is rendered from a deterministic Jinja2 template (`templates/stakeholder_summary.md.j2`) — no LLM call at audit time.
 41 | - Never paste long source code from third-party docs into committed files. Cite + paraphrase + adapt.
 42 | 
 43 | ### Code style
 44 | - Python 3.11+, `uv` not `pip`, type hints on public functions, Pydantic v2 for data, `structlog` for logs, `ruff` for lint, `pytest` for tests
 45 | - Comment the *why*, not the *what*. Especially around the heuristic weights in `skills/notebook-narrative/` — those weights are tuned, not principled
 46 | - snake_case filenames. No spaces, no hyphens
 47 | 
 48 | ---
 49 | 
 50 | ## Repo layout (where things live)
 51 | 
 52 | | Path | Purpose |
 53 | |---|---|
 54 | | `README.md`, `SPECS.md`, `SYSTEM_DESIGN.md`, `ARCHITECTURE.md`, `WORKFLOW_DIAGRAM.md` | Planning + spec docs |
 55 | | `PHASES.md`, `BOBCOIN_BUDGET.md`, `JUDGING_PLAYBOOK.md`, `DEMO_SCRIPT.md` | Hackathon execution docs |
 56 | | `MCP_SETUP.md`, `TECH_STACK.md` | Wiring + dependency docs |
 57 | | `AGENTS.md`, `CLAUDE.md` | Persistent agent context (you're reading one) |
 58 | | `.bob/modes/crux-mode.md` | Custom Bob mode for end-to-end runs |
 59 | | `.bob/rules/*.md` | Project-level Bob behavior rules |
 60 | | `skills/notebook-narrative/` | Intent-recovery skill + helpers (`parse_notebook.py`, `lineage_graph.py`) |
 61 | | `skills/production-audit/` | Audit skill + 15 gap detectors + autopatch templates |
 62 | | `mcp_server/server.py` | FastMCP entrypoint (~200 LOC; the LOC count is part of the pitch) |
 63 | | `mcp_server/tools.py` | The five MCP tools |
 64 | | `samples/01_clean.ipynb`, `02_messy.ipynb`, `03_chaos.ipynb` | Demo inputs, increasing in mess |
 65 | | `out/<stem>/` | Per-notebook generated artifacts |
 66 | | `tests/` | pytest parity tests |
 67 | | `ci/block-on-gaps.yml` | GitHub Actions workflow that calls the MCP server |
 68 | | `bob_sessions/` | **Required for hackathon judging** — screenshots + markdown exports |
 69 | | `internal-monologue/` | Per-task notes Bob writes after non-trivial work |
 70 | 
 71 | ---
 72 | 
 73 | ## Common asks (canonical responses)
 74 | 
 75 | - **"Help me start"** → point at `PHASES.md` Hours 0–3 block. Don't generate code yet.
 76 | - **"Recover intent from a notebook"** → invoke the `notebook-narrative` skill on the specific path; produce `recovered_pipeline.py` + `intent_report.md` only; **stop before audit**.
 77 | - **"Audit the recovered pipeline"** → invoke `production-audit`; produce `audit_dossier.md`, `decision_log.md`, autopatched files, and parity tests; run tests; report pass/fail.
 78 | - **"Wire the MCP server into Bob"** → see `MCP_SETUP.md` § "Bob IDE mcp.json registration"; do not edit Bob's global config without asking.
 79 | - **"What should I cut if I'm behind?"** → cut order is: sample `03_chaos` → polish on sample `02` → bottom 5 gap autopatches (detect-only). Never cut the MCP server, the dossier, or `bob_sessions/`. (The watsonx.ai/Granite capstone is already out of scope — the stakeholder summary uses a deterministic Jinja2 template.)
 80 | 
 81 | ---
 82 | 
 83 | ## Internal-monologue convention
 84 | 
 85 | After any multi-step task that touched code, write a short bullet note to `internal-monologue/<YYYY-MM-DD>-<slug>.md`: what was attempted, what worked, what didn't, what to try next. This survives context-window resets and gives the user an audit trail to send to judges. Keep these terse — bullets, not essays.
 86 | 
 87 | ---
 88 | 
 89 | ## Things that look obvious but aren't
 90 | 
 91 | - **The intent_report.md is part of the demo.** It's not a debug log. It must be readable by a senior engineer in 30 seconds. Use a table for cell classifications.
 92 | - **The audit dossier is part of the demo.** It must look like the output of a senior consultant's week-three review, not a linter. Group by severity, lead each gap with a one-sentence summary, then the patch (or the decision options).
 93 | - **The MCP server's tool signatures matter for the demo.** They appear on screen during the live MCP-Inspector segment of the pitch. Naming should be obviously load-bearing: `block_merge_if_critical_gaps()` is better than `check_status()`.
 94 | 
 95 | ---
 96 | 
 97 | ## Honest expectations for the assistant to internalize
 98 | 
 99 | This is a strong solo submission, not a guaranteed win. The factors that actually decide the outcome, in order of weight:
100 | 1. How cleanly the live demo runs
101 | 2. How tight the README is for a 60-second skim
102 | 3. Whether the `bob_sessions/` folder is correctly populated
103 | 4. How clearly the three focus areas (AI agents / app modernization / DevOps) are mapped in the pitch
104 | 5. Whether the audit dossier feels *specific* (not generic) when a judge reads it
105 | 6. Whether the MCP server demo actually works live or has to fall back to the recorded video
106 | 
107 | Optimize for #1–#3 over everything else. Build for the demo, not for the codebase.
108 | 
109 | ---
110 | 
111 | *See `AGENTS.md` for the IBM-Bob-flavored version of this file. They should always say the same things.*
</content>
</file>
<file><path>pyproject.toml</path>
<content lines="1-34">
 1 | [project]
 2 | name = "crux"
 3 | version = "0.1.0"
 4 | description = "Code Recovery from Undocumented eXperiments"
 5 | requires-python = ">=3.11"
 6 | dependencies = [
 7 |     "nbformat>=5.9",
 8 |     "networkx>=3.2",
 9 |     "pydantic>=2.5",
10 |     "fastapi>=0.110",
11 |     "uvicorn>=0.27",
12 |     "structlog>=24.1",
13 |     "fastmcp>=3.2",
14 |     "jinja2>=3.1",
15 |     "scikit-learn>=1.5",
16 |     "pandas>=2.2",
17 |     "joblib>=1.4",
18 |     "click>=8.1",
19 |     "markdown>=3.5",
20 | ]
21 | 
22 | [project.optional-dependencies]
23 | dev = ["ruff>=0.5", "pytest>=8", "pytest-asyncio>=0.23", "httpx>=0.27"]
24 | 
25 | [project.scripts]
26 | crux = "crux.cli:main"
27 | crux-mcp = "mcp_server.server:main"
28 | 
29 | [tool.setuptools]
30 | packages = ["crux", "crux.detectors", "crux.patches", "mcp_server"]
31 | 
32 | [build-system]
33 | requires = ["setuptools>=68"]
34 | build-backend = "setuptools.build_meta"
</content>
</file>
<file><path>.gitignore</path>
<content lines="1-13">
 1 | ﻿.cruxvenv/
 2 | __pycache__/
 3 | *.pyc
 4 | *.egg-info/
 5 | out/
 6 | .env
 7 | *.key
 8 | .pytest_cache/
 9 | .ruff_cache/
10 | /tmp/
11 | .ipynb_checkpoints/
12 | models/
13 | data/adult.zip
</content>
</file>
<file><path>SPECS.md</path>
<content lines="1-100">
  1 | # SPECS.md — CRUX functional specifications
  2 | 
  3 | > This is the contract. Everything in this file is what CRUX **must** do. Anything not in this file is out of scope for the hackathon submission. If you (Bob, Claude, or a human) ever feel tempted to add a feature, ask whether the demo gets better — if not, don't build it.
  4 | 
  5 | ---
  6 | 
  7 | ## 1. Inputs and outputs (the contract at a glance)
  8 | 
  9 | ### Input
 10 | A single Jupyter notebook (`.ipynb`) somewhere on the local filesystem. The notebook can be:
 11 | - **Executed** (cells have `execution_count` values) — preferred; provides the most signal
 12 | - **Unexecuted** (no execution counts) — supported, but intent recovery falls back harder onto markdown/lineage signals
 13 | - **Partially executed** — supported, treated as executed with missing values handled gracefully
 14 | 
 15 | CRUX does not require the notebook to run cleanly end-to-end. It does not require any companion files (no `requirements.txt`, no data file, no model artifact). If those exist, CRUX uses them; if they don't, CRUX infers what it can.
 16 | 
 17 | ### Output (a directory `out/<notebook-stem>/`)
 18 | ```
 19 | out/<stem>/
 20 | ├── recovered_pipeline.py      Clean Python module: load-bearing cells stitched in dataflow order
 21 | ├── intent_report.md           Per-cell classification + reasoning, sorted by original cell index
 22 | ├── audit_dossier.md           15 gaps, severity-ranked, with patch/decision/scaffold per gap
 23 | ├── decision_log.md            Structured A/B/C options for every non-autopatched gap
 24 | ├── service.py                 FastAPI wrapper around recovered_pipeline.py
 25 | ├── schema.py                  Pydantic input/output models inferred from training df
 26 | ├── preprocessor.py            Serializable train/serve preprocessor (only if scikit-learn pipeline detected)
 27 | ├── tests/
 28 | │   ├── parity_test.py         Pins recovered_pipeline outputs on a training-data sample
 29 | │   └── conftest.py
 30 | ├── Dockerfile
 31 | ├── docker-compose.yml         For local one-command testing
 32 | ├── requirements.txt
 33 | └── .env.example               Env vars extracted from hardcoded strings (secrets flagged)
 34 | ```
 35 | 
 36 | ---
 37 | 
 38 | ## 2. The cell taxonomy (Stage 1: Narrative Intent Recovery)
 39 | 
 40 | Every cell in the notebook is classified into exactly **one** of four categories. The classification drives whether the cell ends up in `recovered_pipeline.py`.
 41 | 
 42 | | Classification | Goes into recovered pipeline? | Definition |
 43 | |---|---|---|
 44 | | **load-bearing** | Yes | Produces a value (model, dataframe, function, transform) consumed by another cell that ultimately produces the final saved artifact or prediction function. |
 45 | | **scaffolding** | Yes (consolidated to top) | Imports, configuration constants, helper-function definitions used by load-bearing cells. |
 46 | | **exploratory** | No | Was iterated on, branched off, or whose outputs feed nothing the final artifact depends on. |
 47 | | **dead** | No | Errored, was commented-out, has zero outputs, or is explicitly marked junk in surrounding markdown. |
 48 | 
 49 | ### The three signals (combined into a per-cell score)
 50 | 
 51 | CRUX combines three signals into a per-cell classification score. The weights are tuned, not principled — see `skills/notebook-narrative/lineage_graph.py` for the constants. They were tuned against the three sample notebooks during hours 3–14 of the build.
 52 | 
 53 | #### Signal A: execution count
 54 | - `execution_count == None` → cell never ran → strong dead signal
 55 | - `execution_count <= 3` and the cell defines a name used downstream → strong load-bearing signal
 56 | - `execution_count >= 10` → exploratory iteration → moderate exploratory signal
 57 | - `execution_count >= 30` → near-certain exploratory signal *unless* the cell is the very last in the notebook
 58 | 
 59 | #### Signal B: markdown narrative
 60 | The Markdown cells immediately *before* a code cell carry intent. CRUX scans them for explicit phrases (regex-based, case-insensitive):
 61 | 
 62 | - **Strong-keep cues**: `final`, `the one that worked`, `production`, `keep this`, `# Approach <N> (the one we ship)`, `## Final Model`
 63 | - **Strong-discard cues**: `junk`, `delete later`, `broken`, `don't run`, `old version`, `scratch`, `# DEAD`, `# IGNORE`
 64 | - **Weak-keep cues**: section headers like `## Train`, `## Predict`, `## Save Model`
 65 | - **Weak-discard cues**: `let's try`, `experimenting`, `not sure if this works`, `back to this approach`
 66 | 
 67 | Markdown cues override execution-count-derived classifications **only when the cue is unambiguous** (strong-keep or strong-discard). For weak cues, the score is adjusted but execution-count signal still dominates.
 68 | 
 69 | #### Signal C: variable lineage
 70 | CRUX builds a directed graph of names defined and used across cells using Python's `ast` module:
 71 | - **Nodes**: cells
 72 | - **Edges**: cell `i → j` if cell `j` uses any name defined by cell `i` (and not redefined in between)
 73 | 
 74 | To classify load-bearing-ness, CRUX identifies one or more **terminal artifacts**:
 75 | - A cell containing `joblib.dump`, `pickle.dump`, `model.save`, `torch.save` → the saved model is the terminal
 76 | - A cell defining a function whose name matches `predict|forecast|infer|score` → that function is terminal
 77 | - A cell that is the final cell of the notebook and produces a non-None value → fallback terminal
 78 | 
 79 | CRUX then traces backward from terminals via the lineage graph. **Any cell on a path to a terminal is load-bearing.** Any cell *not* on such a path is exploratory or dead (which signal A and B then disambiguate).
 80 | 
 81 | ---
 82 | 
 83 | ## 3. The 15 production gaps (Stage 2: Audit)
 84 | 
 85 | This list is fixed. **Do not add, remove, reorder, or rename gaps without updating `DEMO_SCRIPT.md` in lockstep** — judges will see these by number.
 86 | 
 87 | Severity legend:
 88 | - **🔴 Critical** — production breakage or data leak risk
 89 | - **🟡 High** — degrades reliability or debuggability
 90 | - **🟢 Medium** — operational hygiene
 91 | - **🔵 Low** — nice-to-have
 92 | 
 93 | Disposition legend:
 94 | - **A**: Autopatch — CRUX modifies code and writes the patch
 95 | - **D**: Decision — CRUX presents options A/B/C in `decision_log.md`
 96 | - **A+D**: Partial autopatch + decision for the part requiring judgment
 97 | 
 98 | | # | Gap | Severity | Disposition | What it produces |
 99 | |---|---|---|---|---|
100 | | 1 | Input validation | 🔴 | A | `schema.py` with `PredictRequest(BaseModel)`; types inferred from training df dtypes |
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:31:46.546Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.09

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Pending |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Pending |
| 3 | Analyze project structure and identify stack/build tools | Pending |
| 4 | Extract non-obvious build/test/lint commands from config files | Pending |
| 5 | Discover project-specific code patterns and utilities | Pending |
| 6 | Document non-obvious architectural constraints | Pending |
| 7 | Create/update main AGENTS.md with critical cleanup | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/rules-* directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Check for existing AGENTS.md files in project root and .bob/rules-* directories
[x] Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.)
[-] Analyze project structure and identify stack/build tools
[ ] Extract non-obvious build/test/lint commands from config files
[ ] Discover project-specific code patterns and utilities
[ ] Document non-obvious architectural constraints
[ ] Create/update main AGENTS.md with critical cleanup
[ ] Create/update mode-specific AGENTS.md files in .bob/rules-* directories
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:31:58.115Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.16

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Completed |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Completed |
| 3 | Analyze project structure and identify stack/build tools | In Progress |
| 4 | Extract non-obvious build/test/lint commands from config files | Pending |
| 5 | Discover project-specific code patterns and utilities | Pending |
| 6 | Document non-obvious architectural constraints | Pending |
| 7 | Create/update main AGENTS.md with critical cleanup | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/rules-* directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<list_files>
<path>.bob</path>
<recursive>true</recursive>
</list_files>

---

**User:**

[list_files for '.bob'] Result:
🛡️ modes/
🛡️ rules/
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:32:21.391Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.24

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Completed |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Completed |
| 3 | Analyze project structure and identify stack/build tools | In Progress |
| 4 | Extract non-obvious build/test/lint commands from config files | Pending |
| 5 | Discover project-specific code patterns and utilities | Pending |
| 6 | Document non-obvious architectural constraints | Pending |
| 7 | Create/update main AGENTS.md with critical cleanup | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/rules-* directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>crux/__init__.py</path>
  </file>
  <file>
    <path>mcp_server/__init__.py</path>
  </file>
  <file>
    <path>tests/__init__.py</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'crux/__init__.py', 'mcp_server/__init__.py', 'tests/__init__.py'] Result:
<files>
<file><path>crux/__init__.py</path>
<content/><notice>File is empty</notice>
</file>
<file><path>mcp_server/__init__.py</path>
<content/><notice>File is empty</notice>
</file>
<file><path>tests/__init__.py</path>
<content/><notice>File is empty</notice>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:32:31.453Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.31

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Completed |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Completed |
| 3 | Analyze project structure and identify stack/build tools | In Progress |
| 4 | Extract non-obvious build/test/lint commands from config files | Pending |
| 5 | Discover project-specific code patterns and utilities | Pending |
| 6 | Document non-obvious architectural constraints | Pending |
| 7 | Create/update main AGENTS.md with critical cleanup | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/rules-* directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<list_files>
<path>crux</path>
<recursive>true</recursive>
</list_files>

---

**User:**

[list_files for 'crux'] Result:
__init__.py
detectors/
detectors/__init__.py
patches/
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:32:41.878Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.38

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Completed |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Completed |
| 3 | Analyze project structure and identify stack/build tools | In Progress |
| 4 | Extract non-obvious build/test/lint commands from config files | Pending |
| 5 | Discover project-specific code patterns and utilities | Pending |
| 6 | Document non-obvious architectural constraints | Pending |
| 7 | Create/update main AGENTS.md with critical cleanup | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/rules-* directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<search_files>
<path>.</path>
<regex>def\s+\w+|class\s+\w+</regex>
<file_pattern>*.py</file_pattern>
</search_files>

---

**User:**

[search_files for 'def\s+\w+|class\s+\w+' in '*.py'] Result:
Found 0 results.
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:33:10.248Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.46

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Completed |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Completed |
| 3 | Analyze project structure and identify stack/build tools | In Progress |
| 4 | Extract non-obvious build/test/lint commands from config files | Pending |
| 5 | Discover project-specific code patterns and utilities | Pending |
| 6 | Document non-obvious architectural constraints | Pending |
| 7 | Create/update main AGENTS.md with critical cleanup | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/rules-* directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<list_files>
<path>scripts</path>
<recursive>false</recursive>
</list_files>

---

**User:**

[list_files for 'scripts'] Result:
prepare_adult.py
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:33:17.368Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.54

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Completed |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Completed |
| 3 | Analyze project structure and identify stack/build tools | In Progress |
| 4 | Extract non-obvious build/test/lint commands from config files | Pending |
| 5 | Discover project-specific code patterns and utilities | Pending |
| 6 | Document non-obvious architectural constraints | Pending |
| 7 | Create/update main AGENTS.md with critical cleanup | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/rules-* directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>scripts/prepare_adult.py</path>
  </file>
  <file>
    <path>README.md</path>
    <line_range>1-50</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'scripts/prepare_adult.py', 'README.md'] Result:
<files>
<file><path>scripts/prepare_adult.py</path>
<content lines="1-14">
 1 | """Add the canonical column header to UCI Adult and clean basic issues."""
 2 | import pandas as pd
 3 | 
 4 | COLUMNS = [
 5 |     "age", "workclass", "fnlwgt", "education", "education_num",
 6 |     "marital_status", "occupation", "relationship", "race", "sex",
 7 |     "capital_gain", "capital_loss", "hours_per_week", "native_country",
 8 |     "income",
 9 | ]
10 | 
11 | df = pd.read_csv("data/adult.data", names=COLUMNS, skipinitialspace=True, na_values="?")
12 | df.to_csv("data/adult.csv", index=False)
13 | print(f"Shape: {df.shape}")
14 | print(df["income"].value_counts())
</content>
</file>
<file><path>README.md</path>
<content lines="1-50">
 1 | # CRUX
 2 | 
 3 | **Code Recovery from Undocumented eXperiments**
 4 | 
 5 | > A solo IBM Bob agent that reads a Jupyter notebook as a *narrative*, recovers what the data scientist meant to ship, audits the gaps that production will punish, and patches what it safely can — turning a messy `.ipynb` into a deployable FastAPI service in minutes.
 6 | 
 7 | ---
 8 | 
 9 | ## The 30-second pitch
10 | 
11 | Data scientists prototype in notebooks. Notebooks are messy by design — thinking made visible, full of dead-end experiments, abandoned approaches, debugging cells, "let me just try this" detours. Somewhere in that mess is the 20% that actually needs to ship. Today, turning that 20% into a production service takes engineers weeks of meetings, rewrites, and judgment calls.
12 | 
13 | **CRUX collapses that work into minutes.** It uses IBM Bob as an agent that:
14 | 
15 | 1. **Recovers intent** — reads execution counts, markdown commentary, and variable lineage to classify every cell as load-bearing, exploratory, dead, or scaffolding. Keeps only what was meant to ship.
16 | 2. **Audits production-readiness** — runs a 15-gap audit (input validation, train/serve skew, missing logging, no model versioning, hardcoded secrets, no tests, no Dockerfile…) and either autonomously patches each gap or surfaces it as a decision for a human.
17 | 3. **Exposes everything as an MCP server** — so any CI/CD pipeline, Bob session, or downstream agent can audit a notebook, fetch the dossier, list open decisions, or block a merge with critical unresolved gaps.
18 | 
19 | The output is a runnable, dockerized FastAPI service plus an audit dossier and a decision log — the document a senior engineer would produce in week three of a client engagement, generated in five minutes.
20 | 
21 | ---
22 | 
23 | ## Why this wins the brief
24 | 
25 | The hackathon theme is **"turn idea into impact faster."** For a data scientist, the notebook *is* the idea, and a deployed service *is* the impact. CRUX collapses that exact gap, and the brief's three focus areas all map cleanly onto a single product:
26 | 
27 | | Focus area | How CRUX hits it |
28 | |---|---|
29 | | **AI agents doing complex multi-step work** | Intent recovery + 15-gap audit + autonomous patching + decision surfacing is exactly that. |
30 | | **App modernization** | Notebooks are legacy from birth — no contracts, no tests, no docs, no deployment story. CRUX modernizes them in one pass. |
31 | | **DevOps** | The audit is exposed as an MCP server. A real CI job calls it to refuse merges with critical gaps. "MCP servers in minutes" delivered as a tangible demo step. |
32 | 
33 | Three boxes, one product, one demo.
34 | 
35 | ---
36 | 
37 | ## The three things that make CRUX unique
38 | 
39 | These are the differentiation pillars. Every README sentence, every demo line, every commit message reinforces one of these three.
40 | 
41 | ### 1. Narrative Intent Recovery
42 | Existing tools (`nbconvert`, Jupytext, paid platforms) treat a notebook as a flat list of cells and convert all of them. They preserve the mess. CRUX reads the notebook as a **narrative artifact** — a document where intent is buried under exploration — and recovers only the load-bearing logic by combining three signals no rule-based tool reads:
43 | 
44 | - **Execution counts** — `In [47]:` is exploration; `In [2]:` is often production logic
45 | - **Markdown commentary** — section headers like `## Final Model`, `## Approach 3 (the one that worked)`, `## Junk to delete later` carry explicit intent the data scientist wrote down
46 | - **Variable lineage graph** — built via `ast`, traces backward from the final artifact (saved model, prediction function) to find the minimal set of cells that produce it
47 | 
48 | Combined, these signals produce a per-cell classification: **load-bearing**, **exploratory**, **dead**, or **scaffolding**. The recovered pipeline is the load-bearing cells, stitched in dataflow order.
49 | 
50 | ### 2. Production-Readiness Audit
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:33:24.831Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.62

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Completed |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Completed |
| 3 | Analyze project structure and identify stack/build tools | In Progress |
| 4 | Extract non-obvious build/test/lint commands from config files | Pending |
| 5 | Discover project-specific code patterns and utilities | Pending |
| 6 | Document non-obvious architectural constraints | Pending |
| 7 | Create/update main AGENTS.md with critical cleanup | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/rules-* directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Check for existing AGENTS.md files in project root and .bob/rules-* directories
[x] Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.)
[x] Analyze project structure and identify stack/build tools
[-] Extract non-obvious build/test/lint commands from config files
[ ] Discover project-specific code patterns and utilities
[ ] Document non-obvious architectural constraints
[ ] Create/update main AGENTS.md with critical cleanup
[ ] Create/update mode-specific AGENTS.md files in .bob/rules-* directories
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:33:41.280Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.70

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Completed |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Completed |
| 3 | Analyze project structure and identify stack/build tools | Completed |
| 4 | Extract non-obvious build/test/lint commands from config files | In Progress |
| 5 | Discover project-specific code patterns and utilities | Pending |
| 6 | Document non-obvious architectural constraints | Pending |
| 7 | Create/update main AGENTS.md with critical cleanup | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/rules-* directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<ask_followup_question>
<question>I've analyzed the CRUX codebase and found that the existing AGENTS.md and CLAUDE.md files are comprehensive but contain significant amounts of **obvious information** that violates the "non-obvious only" principle. 

The current files include:
- Standard Python conventions (imports, snake_case, type hints)
- Obvious project structure explanations
- Generic hackathon advice
- Redundant context about what CRUX does

According to the init command's quality criteria, I should **DELETE obvious information first** and make the files **SHORTER and MORE FOCUSED** on truly non-obvious discoveries.

However, I notice the codebase appears to be in early stages - the `crux/`, `mcp_server/`, and `tests/` directories exist but contain only empty `__init__.py` files with no actual implementation code yet.

Should I:
1. **Aggressively clean up** the existing AGENTS.md/CLAUDE.md by removing ~70% of obvious content and focus only on the truly non-obvious project-specific rules (like the 15-gap list being fixed, `out/<stem>/` output structure, `samples/` being read-only, `uv` not `pip`, etc.)
2. **Wait for implementation** to discover actual non-obvious code patterns before cleaning up, since there's no code to analyze yet
3. **Create minimal mode-specific files** in `.bob/rules-*` directories with only the non-obvious rules discovered so far</question>
<follow_up>
<suggest>Aggressively clean up existing files now - remove obvious content, keep only non-obvious rules like the 15-gap list, output structure, samples/ read-only, uv requirement, and hackathon-specific constraints</suggest>
<suggest>Wait for code implementation - the codebase is too early to discover non-obvious patterns; revisit after actual code exists</suggest>
<suggest>Do both - clean up existing files AND create minimal mode-specific stubs that can be expanded as code is written</suggest>
</follow_up>
</ask_followup_question>

---

**User:**

[ask_followup_question for 'I've analyzed the CRUX codebase and found that the existing AGENTS.md and CLAUDE.md files are comprehensive but contain significant amounts of **obvious information** that violates the "non-obvious only" principle. 

The current files include:
- Standard Python conventions (imports, snake_case, type hints)
- Obvious project structure explanations
- Generic hackathon advice
- Redundant context about what CRUX does

According to the init command's quality criteria, I should **DELETE obvious information first** and make the files **SHORTER and MORE FOCUSED** on truly non-obvious discoveries.

However, I notice the codebase appears to be in early stages - the `crux/`, `mcp_server/`, and `tests/` directories exist but contain only empty `__init__.py` files with no actual implementation code yet.

Should I:
1. **Aggressively clean up** the existing AGENTS.md/CLAUDE.md by removing ~70% of obvious content and focus only on the truly non-obvious project-specific rules (like the 15-gap list being fixed, `out/<stem>/` output structure, `samples/` being read-only, `uv` not `pip`, etc.)
2. **Wait for implementation** to discover actual non-obvious code patterns before cleaning up, since there's no code to analyze yet
3. **Create minimal mode-specific files** in `.bob/rules-*` directories with only the non-obvious rules discovered so far'] Result:
<answer>
Wait for code implementation - the codebase is too early to discover non-obvious patterns; revisit after actual code exists
</answer>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:36:13.023Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.79

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Completed |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Completed |
| 3 | Analyze project structure and identify stack/build tools | Completed |
| 4 | Extract non-obvious build/test/lint commands from config files | In Progress |
| 5 | Discover project-specific code patterns and utilities | Pending |
| 6 | Document non-obvious architectural constraints | Pending |
| 7 | Create/update main AGENTS.md with critical cleanup | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/rules-* directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Check for existing AGENTS.md files in project root and .bob/rules-* directories
[x] Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.)
[x] Analyze project structure and identify stack/build tools
[x] Extract non-obvious build/test/lint commands from config files
[x] Discover project-specific code patterns and utilities
[x] Document non-obvious architectural constraints
[-] Create summary of findings and recommendations
[ ] Document decision to defer cleanup until implementation exists
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs


# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T00:36:26.300Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.87

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
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/rules-* directories | Completed |
| 2 | Read existing AGENTS.md and other AI assistant rules (CLAUDE.md, etc.) | Completed |
| 3 | Analyze project structure and identify stack/build tools | Completed |
| 4 | Extract non-obvious build/test/lint commands from config files | Completed |
| 5 | Discover project-specific code patterns and utilities | Completed |
| 6 | Document non-obvious architectural constraints | Completed |
| 7 | Create summary of findings and recommendations | In Progress |
| 8 | Document decision to defer cleanup until implementation exists | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Analysis complete. The CRUX codebase is in **early planning stage** with comprehensive documentation but minimal implementation code.

## Key Findings

**Existing AGENTS.md files:**
- [`AGENTS.md`](AGENTS.md:1) (123 lines) - Comprehensive Bob-specific context
- [`CLAUDE.md`](CLAUDE.md:1) (111 lines) - Mirror of AGENTS.md for Claude/Anthropic tools
- No mode-specific files in `.bob/rules-*` directories yet

**Current state:**
- Core directories ([`crux/`](crux/__init__.py:1), [`mcp_server/`](mcp_server/__init__.py:1), [`tests/`](tests/__init__.py:1)) contain only empty `__init__.py` files
- No implementation code to analyze for non-obvious patterns
- Build system: Python 3.11+, [`uv`](pyproject.toml:1) for dependencies, [`ruff`](pyproject.toml:23) for linting, [`pytest`](pyproject.toml:23) for testing

**Non-obvious rules already documented:**
- 15-gap audit list is **fixed** - do not modify without updating [`SPECS.md`](SPECS.md:85) and demo script
- All outputs go to `out/<notebook-stem>/` directory structure
- [`samples/`](samples/) notebooks are **read-only** demo inputs
- Must use `uv` not `pip` for dependency management
- 40 Bobcoin budget constraint for entire hackathon
- MCP server must stay at ~200 LOC (part of pitch)
- Custom mode at [`.bob/modes/crux-mode.md`](.bob/modes/crux-mode.md:1) for end-to-end runs

## Recommendation

**Defer AGENTS.md cleanup until implementation exists.** The current files contain planning context valuable for the hackathon build phase. Once actual code patterns emerge (custom utilities, non-standard approaches, hidden coupling), revisit with aggressive cleanup to remove obvious information and document only truly non-obvious discoveries.

The init command's "non-obvious only" principle is correct, but premature optimization here would remove context needed for the build phase before discovering what the actual non-obvious patterns will be.
</result>
</attempt_completion>

