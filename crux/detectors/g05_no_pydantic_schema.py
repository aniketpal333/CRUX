"""Detector for gap #5: No Pydantic schema."""
import re
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoPydanticSchemaDetector(Detector):
    gap_id = 5
    name = "No Pydantic schema"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect missing Pydantic schema definitions.
        
        Fires if:
        - No 'class .*BaseModel' definition anywhere in the notebook
        """
        has_pydantic_model = False
        
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            
            source = cell.source
            
            # Check for Pydantic BaseModel class definitions
            if re.search(r'class\s+\w+.*\(.*BaseModel.*\)', source):
                has_pydantic_model = True
                break
        
        if not has_pydantic_model:
            return [
                GapFinding(
                    gap_id=5,
                    name="No Pydantic schema",
                    severity="auto_patch",
                    location="notebook",
                    disposition="auto_patched",
                    detail="No Pydantic BaseModel schema definitions found"
                )
            ]
        
        return []


# Register this detector
register(NoPydanticSchemaDetector())

# Made with Bob
