**User:**

<task>
@crux/classifier.py refactor variable lineage analysis into crux/lineage.py. Use Python's ast module to walk each cell. Build two dicts: assignments (variable_name -> sorted list of cell_index where assigned) and reads (variable_name -> sorted list of cell_index where read in Load context). Add function find_dead_assignments(nb_path) -> list[tuple[int, str, str]] returning (cell_index, variable_name, reason) for any assignment whose variable is never read in any cell with index > assignment_index. Update classifier.py classify_cell to use this for more accurate dead-code detection - if the cell's assigned names appear in dead_assignments, classify as dead. Add tests in tests/test_lineage.py covering: simple assign-then-never-read case, assign-then-read-later case (not dead), augmented assign, attribute access not counted as Load.
</task>
<environment_details>
# VSCode Visible Files
samples\03_chaos.ipynb,samples\03_chaos.ipynb,samples\03_chaos.ipynb,samples\03_chaos.ipynb,samples\03_chaos.ipynb,bob_sessions\budget_log.md

# VSCode Open Tabs
.bob/modes/crux-auditor.md,AGENTS.md,.gitignore,README.md,bob_sessions/budget_log.md,crux/models.py,tests/test_models.py,crux/classifier.py,tests/test_classifier.py,samples/02_messy.ipynb,samples/PROVENANCE.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-03T01:49:32.037Z
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
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>


# Current Workspace Directory (c:/Users/anike/Desktop/CRUX) Files
.gitignore
AGENTS.md
ARCHITECTURE.md
CLAUDE.md
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
bob_sessions/budget_log.md
ci/
crux/
crux/__init__.py
crux/classifier.py
crux/models.py
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
samples/01_clean.ipynb
samples/02_messy.ipynb
samples/03_chaos.ipynb
samples/PROVENANCE.md
scripts/
scripts/prepare_adult.py
submission/
templates/
templates/stakeholder_summary.md.j2
tests/
tests/__init__.py
tests/test_classifier.py
tests/test_models.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

