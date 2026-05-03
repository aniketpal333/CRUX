"""Detector for gap #2: No logging."""
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoLoggingDetector(Detector):
    gap_id = 2
    name = "No logging"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect if notebook uses print() but has no logging imports.
        
        Fires if:
        - Any cell contains print() calls
        - AND no cell imports logging or structlog
        """
        has_print = False
        has_logging = False
        
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            
            source = cell.source
            
            # Check for print calls
            if 'print(' in source:
                has_print = True
            
            # Check for logging imports
            if any(pattern in source for pattern in [
                'import logging',
                'from logging',
                'import structlog',
                'from structlog'
            ]):
                has_logging = True
        
        if has_print and not has_logging:
            return [
                GapFinding(
                    gap_id=2,
                    name="No logging",
                    severity="auto_patch",
                    location="throughout notebook",
                    disposition="auto_patched",
                    detail="Notebook uses print() calls but has no structured logging"
                )
            ]
        
        return []


# Register this detector
register(NoLoggingDetector())

# Made with Bob
