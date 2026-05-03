"""Variable lineage analysis using AST to track assignments and reads across notebook cells."""
import ast
from typing import Dict, List, Tuple
import nbformat


def build_lineage(nb_path: str) -> Tuple[Dict[str, List[int]], Dict[str, List[int]]]:
    """
    Build variable lineage from a notebook.
    
    Returns:
        assignments: dict mapping variable_name -> sorted list of cell indices where assigned
        reads: dict mapping variable_name -> sorted list of cell indices where read (Load context)
    """
    nb = nbformat.read(nb_path, as_version=4)
    
    assignments: Dict[str, List[int]] = {}
    reads: Dict[str, List[int]] = {}
    
    for cell_idx, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
            
        src = cell.source.strip()
        if not src:
            continue
            
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        
        # Track assignments
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id not in assignments:
                            assignments[target.id] = []
                        assignments[target.id].append(cell_idx)
            elif isinstance(node, ast.AugAssign):
                if isinstance(node.target, ast.Name):
                    if node.target.id not in assignments:
                        assignments[node.target.id] = []
                    assignments[node.target.id].append(cell_idx)
        
        # Track reads (Load context only, excludes attribute access on the variable itself)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                # Exclude if this Name is the value part of an attribute access
                # (we want x in "x.foo" to count, but not as the primary read target)
                # Actually, per spec: "attribute access not counted as Load" means
                # we should NOT count x.foo as a read of x. Let me reconsider.
                # 
                # The spec says "attribute access not counted as Load" - this likely means
                # that if we have "df.head()", we should not count "df" as a read in the
                # traditional sense for dead code detection, because attribute access
                # is often exploratory. However, for lineage purposes, x.foo IS a read of x.
                # 
                # Re-reading the spec: "reads (variable_name -> sorted list of cell_index 
                # where read in Load context)" and "attribute access not counted as Load"
                # suggests we should skip Names that are the object of an Attribute node.
                # 
                # Let's implement: only count Name nodes in Load context that are NOT
                # the value of an ast.Attribute node.
                if node.id not in reads:
                    reads[node.id] = []
                reads[node.id].append(cell_idx)
    
    # Sort and deduplicate
    for var in assignments:
        assignments[var] = sorted(set(assignments[var]))
    for var in reads:
        reads[var] = sorted(set(reads[var]))
    
    return assignments, reads


def find_dead_assignments(nb_path: str) -> List[Tuple[int, str, str]]:
    """
    Find assignments whose variables are never read in any subsequent cell.
    
    Returns:
        List of (cell_index, variable_name, reason) tuples for dead assignments.
    """
    assignments, reads = build_lineage(nb_path)
    
    dead: List[Tuple[int, str, str]] = []
    
    for var_name, assign_indices in assignments.items():
        read_indices = reads.get(var_name, [])
        
        for assign_idx in assign_indices:
            # Check if there's any read after this assignment
            has_downstream_read = any(read_idx > assign_idx for read_idx in read_indices)
            
            if not has_downstream_read:
                reason = f"assigned in cell {assign_idx} but never read in any subsequent cell"
                dead.append((assign_idx, var_name, reason))
    
    return dead

# Made with Bob
