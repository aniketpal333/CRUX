"""Tests for pipeline recovery from notebooks."""
import os
from crux.recovery import recover_pipeline


def test_recover_pipeline_contains_load_bearing_code():
    """Test that recovered pipeline contains load-bearing code from 02_messy.ipynb."""
    nb_path = os.path.join("samples", "02_messy.ipynb")
    
    recovered = recover_pipeline(nb_path)
    
    # Should contain joblib.dump (terminal artifact)
    assert "joblib.dump" in recovered, "Recovered pipeline should contain joblib.dump"
    
    # Should contain RandomForestClassifier (the model that was actually trained)
    assert "RandomForestClassifier" in recovered, "Recovered pipeline should contain RandomForestClassifier"


def test_recover_pipeline_excludes_dead_code():
    """Test that recovered pipeline does NOT contain code from commented-out/dead cells."""
    nb_path = os.path.join("samples", "02_messy.ipynb")
    
    recovered = recover_pipeline(nb_path)
    
    # Should NOT contain XGBClassifier (which is in commented-out exploratory cells)
    assert "XGBClassifier" not in recovered, "Recovered pipeline should NOT contain XGBClassifier from dead cells"

# Made with Bob
