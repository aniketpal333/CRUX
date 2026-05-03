"""Detector for gap #13: No reproducibility metadata."""
import re
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoReproMetadataDetector(Detector):
    gap_id = 13
    name = "No reproducibility metadata"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect missing reproducibility metadata.
        
        Fires if:
        - train_test_split call without 'random_state=' parameter
        """
        findings = []
        
        for idx, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            
            source = cell.source
            
            # Check for train_test_split function call (not import)
            # Look for pattern: train_test_split( with actual call, not just import
            if re.search(r'train_test_split\s*\(', source):
                # Check if random_state is specified anywhere in the cell
                # Use re.DOTALL to match across lines
                if not re.search(r'random_state\s*=', source, re.DOTALL):
                    findings.append(
                        GapFinding(
                            gap_id=13,
                            name="No reproducibility metadata",
                            severity="auto_patch",
                            location=f"cell {idx}",
                            disposition="auto_patched",
                            detail="train_test_split called without random_state parameter"
                        )
                    )
        
        return findings


# Register this detector
register(NoReproMetadataDetector())

# Made with Bob
