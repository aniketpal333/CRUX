"""Detector for gap #11: No batch endpoint."""
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoBatchEndpointDetector(Detector):
    gap_id = 11
    name = "No batch endpoint"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect missing batch prediction endpoint.
        
        Always fires - notebooks process single samples, not batches.
        """
        return [
            GapFinding(
                gap_id=11,
                name="No batch endpoint",
                severity="decision",
                location="API design",
                disposition="decisions_required",
                options=2,
                detail="Notebook lacks batch prediction capability; decide whether to add batch endpoint"
            )
        ]


# Register this detector
register(NoBatchEndpointDetector())

# Made with Bob
