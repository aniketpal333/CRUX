"""Detector for gap #3: Train/serve skew."""
import re
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class TrainServeSkewDetector(Detector):
    gap_id = 3
    name = "Train/serve skew"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect train/serve skew: preprocessing in notebook but not in saved model.
        
        Fires if:
        - LabelEncoder or OneHotEncoder appears in cells
        - AND joblib.dump saves a bare 'model' variable (not a Pipeline)
        
        The smoking gun: separate preprocessing loops + bare model save.
        """
        has_encoder = False
        has_bare_model_save = False
        
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            
            source = cell.source
            
            # Check for encoders
            if re.search(r'(LabelEncoder|OneHotEncoder)\s*\(', source):
                has_encoder = True
            
            # Check for bare model save (not saving a Pipeline)
            # Look for joblib.dump(model, ...) where 'model' is not 'pipeline'
            if re.search(r'joblib\.dump\s*\(\s*model\s*,', source):
                # Check if it's NOT a pipeline
                if 'Pipeline' not in source and 'pipeline' not in source.lower():
                    has_bare_model_save = True
        
        if has_encoder and has_bare_model_save:
            return [
                GapFinding(
                    gap_id=3,
                    name="Train/serve skew",
                    severity="decision",
                    location="preprocessing + model save",
                    disposition="decisions_required",
                    options=3,
                    detail="Preprocessing (LabelEncoder/OneHotEncoder) done separately from model; saved model won't include preprocessing"
                )
            ]
        
        return []


# Register this detector
register(TrainServeSkewDetector())

# Made with Bob
