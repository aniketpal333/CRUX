"""Detector for gap #12: No authentication."""
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoAuthDetector(Detector):
    gap_id = 12
    name = "No authentication"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect missing authentication infrastructure.
        
        Always fires - notebooks lack authentication mechanisms.
        """
        return [
            GapFinding(
                gap_id=12,
                name="No authentication",
                severity="decision",
                location="API security",
                disposition="decisions_required",
                options=3,
                detail="Notebook lacks authentication; decide on auth strategy (API key, OAuth, none)"
            )
        ]


# Register this detector
register(NoAuthDetector())

# Made with Bob
