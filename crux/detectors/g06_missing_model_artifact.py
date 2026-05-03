"""Detector for gap #6: Missing model artifact."""
import re
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class MissingModelArtifactDetector(Detector):
    gap_id = 6
    name = "Missing model artifact"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect if model is trained but not saved.
        
        Fires if:
        - Cell calls model.fit() or model.train()
        - BUT no cell calls joblib.dump or pickle.dump
        """
        has_training = False
        has_save = False
        
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            
            source = cell.source
            
            # Check for model training
            if re.search(r'\.\s*(fit|train)\s*\(', source):
                has_training = True
            
            # Check for model saving
            if re.search(r'(joblib\.dump|pickle\.dump)\s*\(', source):
                has_save = True
        
        if has_training and not has_save:
            return [
                GapFinding(
                    gap_id=6,
                    name="Missing model artifact",
                    severity="blocker",
                    location="model training",
                    disposition="blocker",
                    detail="Model is trained but never saved to disk"
                )
            ]
        
        return []


# Register this detector
register(MissingModelArtifactDetector())

# Made with Bob
