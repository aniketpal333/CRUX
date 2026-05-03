"""Top-level audit pipeline: classify, detect, build AuditResult."""
from datetime import datetime, timezone
from collections import Counter

from .classifier import classify_notebook
from .detectors import run_all
from .models import AuditResult, CellCounts, GapCounts


def audit_notebook(nb_path: str) -> AuditResult:
    cells = classify_notebook(nb_path)
    findings = run_all(nb_path)

    cell_counter = Counter(c.classification for c in cells)
    cell_counts = CellCounts(
        total=len(cells),
        load_bearing=cell_counter.get("load_bearing", 0),
        scaffolding=cell_counter.get("scaffolding", 0),
        exploratory=cell_counter.get("exploratory", 0),
        dead=cell_counter.get("dead", 0),
    )

    blockers = [f for f in findings if f.disposition == "blocker"]
    decisions = [f for f in findings if f.disposition == "decisions_required"]
    auto_patched = [f for f in findings if f.disposition == "auto_patched"]

    gap_counts = GapCounts(
        total=len(findings),
        blockers=len(blockers),
        auto_patched=len(auto_patched),
        decisions_required=len(decisions),
        dismissed=0,
    )

    if blockers:
        verdict = "BLOCKED"
    elif decisions:
        verdict = "READY_WITH_DECISIONS"
    else:
        verdict = "CLEAN"

    return AuditResult(
        notebook_name=nb_path.split("/")[-1].split("\\")[-1],
        audit_timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        verdict=verdict,
        cells=cell_counts,
        gaps=gap_counts,
        blockers=[{"id": f.gap_id, "name": f.name, "location": f.location} for f in blockers],
        decisions=[{"id": f.gap_id, "name": f.name, "options": f.options} for f in decisions],
        auto_patched_gaps=[{"id": f.gap_id, "name": f.name} for f in auto_patched],
        cells_detail=cells,
    )