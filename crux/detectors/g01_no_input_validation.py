"""Detector for gap #1: No input validation."""
import re
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoInputValidationDetector(Detector):
    gap_id = 1
    name = "No input validation"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect if notebook calls .predict() or .fit() without input validation.
        
        Fires if:
        - Any cell calls .predict( or .fit( on a variable
        - AND no cell has validation mechanisms:
          - Pydantic imports
          - isinstance/assert checks
          - sklearn Pipeline with ColumnTransformer (provides schema enforcement)
        """
        # Existing checks
        has_pydantic = any(
            "pydantic" in c.source for c in nb.cells if c.cell_type == "code"
        )
        has_isinstance_check = any(
            "isinstance(" in c.source for c in nb.cells if c.cell_type == "code"
        )

        # NEW: sklearn Pipeline + ColumnTransformer counts as input validation
        # because ColumnTransformer enforces column types/order at predict time
        # and Pipeline ensures the same preprocessing applies at train and serve.
        has_pipeline_validation = False
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            src = cell.source
            if "Pipeline(" in src and (
                "ColumnTransformer(" in src
                or "preprocess" in src.lower()
            ):
                has_pipeline_validation = True
                break

        calls_predict_or_fit = any(
            ".predict(" in c.source or ".fit(" in c.source
            for c in nb.cells if c.cell_type == "code"
        )

        if (calls_predict_or_fit
            and not has_pydantic
            and not has_isinstance_check
            and not has_pipeline_validation):
            return [GapFinding(
                gap_id=1,
                name="No input validation",
                severity="blocker",
                location="model boundary",
                disposition="blocker",
                detail="Model calls .predict() or .fit() without input validation (Pydantic, isinstance, or sklearn Pipeline)"
            )]
        return []


# Register this detector
register(NoInputValidationDetector())

# Made with Bob
