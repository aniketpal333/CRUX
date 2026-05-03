"""Detector for gap #4: No versioning."""
import re
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoVersioningDetector(Detector):
    gap_id = 4
    name = "No versioning"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect if model is saved without version information in the path.
        
        Fires if:
        - Cell contains joblib.dump or pickle.dump
        - AND the path string has no version pattern (v\\d, version, timestamp, datetime)
        """
        findings = []
        
        for idx, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            
            source = cell.source
            
            # Check for model save calls
            if re.search(r'(joblib\.dump|pickle\.dump)\s*\(', source):
                # Check if path contains version indicators
                has_version = bool(re.search(
                    r'(v\d|version|timestamp|datetime)',
                    source,
                    re.IGNORECASE
                ))
                
                if not has_version:
                    findings.append(
                        GapFinding(
                            gap_id=4,
                            name="No versioning",
                            severity="decision",
                            location=f"cell {idx}",
                            disposition="decisions_required",
                            options=2,
                            detail="Model saved without version information in path"
                        )
                    )
        
        return findings


# Register this detector
register(NoVersioningDetector())

# Made with Bob
