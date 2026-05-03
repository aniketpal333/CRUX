"""Stage 1: classify each cell into one of 4 categories."""
import ast
import re
import nbformat
from .models import CellRecord
from .lineage import find_dead_assignments


LOAD_BEARING_TERMINALS = [
    r"\bjoblib\.dump\b", r"\bpickle\.dump\b", r"\.save\s*\(",
    r"\b\.fit\s*\(", r"\b\.train\s*\(", r"\bmodel\s*=\s*\w+\(",
]
DATA_PREP_PATTERNS = [
    r"\bpd\.read_", r"\.dropna\b", r"\.fillna\b", r"\.drop\s*\(",
    r"\bColumnTransformer\b", r"\bPipeline\b", r"\btrain_test_split\b",
    r"\bLabelEncoder\b", r"\bOneHotEncoder\b", r"\bStandardScaler\b",
]
DEBUG_PATTERNS = [
    r"^\s*print\s*\(", r"\.head\s*\(\)?$", r"\.tail\s*\(\)?$",
    r"\.describe\s*\(\)?$", r"\.shape\s*$", r"\.dtypes\s*$",
    r"\.info\s*\(\)?$", r"\.value_counts\b",
]
EXPLORATORY_HINTS = [
    r"^\s*#\s*(try|test|attempt|experiment|maybe|todo)",
    r"^\s*#\s*(version|v\d|alternate)",
]


def _extract_assigned_names(src: str) -> set[str]:
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return set()
    names = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return names


def _extract_referenced_names(src: str) -> set[str]:
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return set()
    refs = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            refs.add(node.id)
    return refs


def _all_commented_out(src: str) -> bool:
    lines = [l for l in src.split("\n") if l.strip()]
    if not lines:
        return False
    return all(l.strip().startswith("#") for l in lines)


def classify_cell(cell: nbformat.NotebookNode, index: int, downstream_refs: set[str], dead_assignments: set[tuple[int, str]] | None = None) -> CellRecord:
    if cell.cell_type == "markdown":
        return CellRecord(
            index=index, execution_count=None, classification="scaffolding",
            source_preview=cell.source[:80],
            citation=f"cell {index+1} (markdown)",
            reason="markdown narration retained as scaffolding",
        )

    src = cell.source.strip()
    preview = (src[:80] + "...") if len(src) > 80 else src

    if not src:
        return CellRecord(
            index=index, execution_count=cell.get("execution_count"),
            classification="dead", source_preview=preview,
            citation=f"cell {index+1}", reason="empty cell",
        )

    if _all_commented_out(src):
        cls = "exploratory" if any(re.search(p, src, re.I | re.M) for p in EXPLORATORY_HINTS) else "dead"
        return CellRecord(
            index=index, execution_count=cell.get("execution_count"),
            classification=cls, source_preview=preview,
            citation=f"cell {index+1}",
            reason=f"all lines commented out -> {cls}",
        )

    if cell.get("execution_count") is None:
        cls = "exploratory" if any(re.search(p, src, re.I | re.M) for p in EXPLORATORY_HINTS) else "dead"
        return CellRecord(
            index=index, execution_count=None,
            classification=cls, source_preview=preview,
            citation=f"cell {index+1}",
            reason=f"never executed -> {cls}",
        )

    for pat in LOAD_BEARING_TERMINALS:
        if re.search(pat, src):
            return CellRecord(
                index=index, execution_count=cell.get("execution_count"),
                classification="load_bearing", source_preview=preview,
                citation=f"cell {index+1}",
                reason=f"contains terminal artifact (matched: {pat})",
            )

    assigned = _extract_assigned_names(src)
    
    # Use lineage-based dead assignment detection if available
    if dead_assignments is not None:
        dead_vars_in_cell = {var for (idx, var) in dead_assignments if idx == index}
        if assigned and dead_vars_in_cell and assigned == dead_vars_in_cell:
            try:
                tree = ast.parse(src)
                non_assign = [n for n in tree.body if not isinstance(n, (ast.Assign, ast.AugAssign, ast.Import, ast.ImportFrom))]
                if not non_assign:
                    return CellRecord(
                        index=index, execution_count=cell.get("execution_count"),
                        classification="dead", source_preview=preview,
                        citation=f"cell {index+1}",
                        reason=f"assigns {sorted(dead_vars_in_cell)} but never read in subsequent cells (lineage analysis)",
                    )
            except SyntaxError:
                pass
    # Fallback to original downstream_refs check
    elif assigned and not (assigned & downstream_refs):
        try:
            tree = ast.parse(src)
            non_assign = [n for n in tree.body if not isinstance(n, (ast.Assign, ast.AugAssign, ast.Import, ast.ImportFrom))]
            if not non_assign:
                return CellRecord(
                    index=index, execution_count=cell.get("execution_count"),
                    classification="dead", source_preview=preview,
                    citation=f"cell {index+1}",
                    reason=f"assigns {sorted(assigned)} but no downstream cell reads them",
                )
        except SyntaxError:
            pass

    for pat in DATA_PREP_PATTERNS:
        if re.search(pat, src):
            return CellRecord(
                index=index, execution_count=cell.get("execution_count"),
                classification="scaffolding", source_preview=preview,
                citation=f"cell {index+1}",
                reason=f"data preparation step (matched: {pat})",
            )

    non_comment_lines = [l for l in src.split("\n") if l.strip() and not l.strip().startswith("#")]
    if len(non_comment_lines) <= 2:
        for pat in DEBUG_PATTERNS:
            if re.search(pat, src, re.M):
                return CellRecord(
                    index=index, execution_count=cell.get("execution_count"),
                    classification="dead", source_preview=preview,
                    citation=f"cell {index+1}",
                    reason=f"debug inspection only (matched: {pat})",
                )

    return CellRecord(
        index=index, execution_count=cell.get("execution_count"),
        classification="scaffolding", source_preview=preview,
        citation=f"cell {index+1}",
        reason="default classification",
    )


def classify_notebook(nb_path: str) -> list[CellRecord]:
    nb = nbformat.read(nb_path, as_version=4)

    # Build lineage-based dead assignments
    dead_assign_list = find_dead_assignments(nb_path)
    dead_assignments = {(idx, var) for idx, var, _ in dead_assign_list}

    all_refs_per_cell = []
    for cell in nb.cells:
        if cell.cell_type == "code":
            all_refs_per_cell.append(_extract_referenced_names(cell.source))
        else:
            all_refs_per_cell.append(set())

    records = []
    for i, cell in enumerate(nb.cells):
        downstream = set().union(*all_refs_per_cell[i+1:]) if i + 1 < len(nb.cells) else set()
        records.append(classify_cell(cell, i, downstream, dead_assignments))

    return records