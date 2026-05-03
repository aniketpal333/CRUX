"""Detector for gap #8: No drift detection."""
import re
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoDriftDetectionDetector(Detector):
    gap_id = 8
    name = "No drift detection"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect missing drift detection infrastructure.
        
        Fires if:
        - .describe() appears but output is not saved
        - Crude heuristic: if 'describe()' appears, it's not saved unless
          followed by '.to_csv' or '.to_json' on the same expression
        """
        has_unsaved_describe = False
        
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            
            source = cell.source
            
            # Check for .describe() calls
            if '.describe()' in source:
                # Check if the describe output is saved
                # Look for patterns like: df.describe().to_csv or df.describe().to_json
                if not re.search(r'\.describe\(\)\s*\.\s*(to_csv|to_json)', source):
                    has_unsaved_describe = True
        
        if has_unsaved_describe:
            return [
                GapFinding(
                    gap_id=8,
                    name="No drift detection",
                    severity="decision",
                    location="data exploration",
                    disposition="decisions_required",
                    options=2,
                    detail="Data statistics computed with .describe() but not saved for drift monitoring"
                )
            ]
        
        return []


# Register this detector
register(NoDriftDetectionDetector())

# Made with Bob
