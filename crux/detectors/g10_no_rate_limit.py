"""Detector for gap #10: No rate limiting."""
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoRateLimitDetector(Detector):
    gap_id = 10
    name = "No rate limiting"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect missing rate limiting infrastructure.
        
        Always fires - notebooks inherently lack rate limiting.
        """
        return [
            GapFinding(
                gap_id=10,
                name="No rate limiting",
                severity="auto_patch",
                location="API infrastructure",
                disposition="auto_patched",
                detail="Notebook lacks rate limiting; will be added to service wrapper"
            )
        ]


# Register this detector
register(NoRateLimitDetector())

# Made with Bob
