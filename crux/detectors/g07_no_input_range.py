"""Detector for gap #7: No input range validation."""
import re
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoInputRangeDetector(Detector):
    gap_id = 7
    name = "No input range validation"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect missing input range validation.
        
        Fires if:
        - No .clip() calls
        - No min/max bounds checks anywhere
        """
        has_range_validation = False
        
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            
            source = cell.source
            
            # Check for range validation mechanisms
            if any(pattern in source for pattern in [
                '.clip(',
                'np.clip(',
                'min=',
                'max=',
                '< min',
                '> max',
                '<= min',
                '>= max'
            ]):
                has_range_validation = True
                break
        
        if not has_range_validation:
            return [
                GapFinding(
                    gap_id=7,
                    name="No input range validation",
                    severity="decision",
                    location="data processing",
                    disposition="decisions_required",
                    options=2,
                    detail="No input range validation (clip, min/max bounds) detected"
                )
            ]
        
        return []


# Register this detector
register(NoInputRangeDetector())

# Made with Bob
