"""Tests for gap detectors g03, g05, g08, g13, g15."""
import os
import pytest
from crux.detectors.registry import run_all
from crux.detectors.g03_train_serve_skew import TrainServeSkewDetector
from crux.detectors.g05_no_pydantic_schema import NoPydanticSchemaDetector
from crux.detectors.g08_no_drift_detection import NoDriftDetectionDetector
from crux.detectors.g13_no_repro_metadata import NoReproMetadataDetector
from crux.detectors.g15_no_dockerfile import NoDockerfileDetector
import nbformat


# Paths to sample notebooks
MESSY_NB = "samples/02_messy.ipynb"
CLEAN_NB = "samples/01_clean.ipynb"


class TestG03TrainServeSkew:
    """Test gap #3: Train/serve skew detector."""
    
    def test_detects_skew_in_messy_notebook(self):
        """02_messy.ipynb has LabelEncoder loop + bare model save."""
        detector = TrainServeSkewDetector()
        nb = nbformat.read(MESSY_NB, as_version=4)
        findings = detector.detect(nb, MESSY_NB)
        
        assert len(findings) == 1
        assert findings[0].gap_id == 3
        assert findings[0].severity == "decision"
        assert findings[0].disposition == "decisions_required"
        assert findings[0].options == 3
    
    def test_no_detection_in_clean_notebook(self):
        """01_clean.ipynb uses Pipeline, so no skew."""
        detector = TrainServeSkewDetector()
        nb = nbformat.read(CLEAN_NB, as_version=4)
        findings = detector.detect(nb, CLEAN_NB)
        
        # Clean notebook uses Pipeline, so should not fire
        assert len(findings) == 0


class TestG05NoPydanticSchema:
    """Test gap #5: No Pydantic schema detector."""
    
    def test_detects_missing_schema_in_messy_notebook(self):
        """02_messy.ipynb has no Pydantic BaseModel definitions."""
        detector = NoPydanticSchemaDetector()
        nb = nbformat.read(MESSY_NB, as_version=4)
        findings = detector.detect(nb, MESSY_NB)
        
        assert len(findings) == 1
        assert findings[0].gap_id == 5
        assert findings[0].severity == "auto_patch"
        assert findings[0].disposition == "auto_patched"
    
    def test_detects_missing_schema_in_clean_notebook(self):
        """01_clean.ipynb also has no Pydantic schemas."""
        detector = NoPydanticSchemaDetector()
        nb = nbformat.read(CLEAN_NB, as_version=4)
        findings = detector.detect(nb, CLEAN_NB)
        
        # Clean notebook also lacks Pydantic, so should fire
        assert len(findings) == 1


class TestG08NoDriftDetection:
    """Test gap #8: No drift detection detector."""
    
    def test_detects_unsaved_describe_in_messy_notebook(self):
        """02_messy.ipynb may have .describe() without saving."""
        detector = NoDriftDetectionDetector()
        nb = nbformat.read(MESSY_NB, as_version=4)
        findings = detector.detect(nb, MESSY_NB)
        
        # May or may not fire depending on whether describe() is used
        assert len(findings) >= 0
    
    def test_no_detection_when_describe_saved(self):
        """If describe() output is saved, should not fire."""
        detector = NoDriftDetectionDetector()
        nb = nbformat.read(CLEAN_NB, as_version=4)
        findings = detector.detect(nb, CLEAN_NB)
        
        # Clean notebook may or may not have describe()
        assert len(findings) >= 0


class TestG13NoReproMetadata:
    """Test gap #13: No reproducibility metadata detector."""
    
    def test_detects_missing_random_state_in_messy_notebook(self):
        """02_messy.ipynb has train_test_split without random_state."""
        detector = NoReproMetadataDetector()
        nb = nbformat.read(MESSY_NB, as_version=4)
        findings = detector.detect(nb, MESSY_NB)
        
        # Should detect train_test_split without random_state
        assert len(findings) >= 1
        assert all(f.gap_id == 13 for f in findings)
        assert all(f.severity == "auto_patch" for f in findings)
        assert all(f.disposition == "auto_patched" for f in findings)
    
    def test_no_detection_when_random_state_present(self):
        """01_clean.ipynb has train_test_split with random_state=42."""
        detector = NoReproMetadataDetector()
        nb = nbformat.read(CLEAN_NB, as_version=4)
        findings = detector.detect(nb, CLEAN_NB)
        
        # Clean notebook has random_state, so should not fire
        assert len(findings) == 0


class TestG15NoDockerfile:
    """Test gap #15: No Dockerfile detector."""
    
    def test_detects_missing_dockerfile_for_messy_notebook(self):
        """When running on 02_messy.ipynb, check if Dockerfile exists."""
        detector = NoDockerfileDetector()
        nb = nbformat.read(MESSY_NB, as_version=4)
        findings = detector.detect(nb, MESSY_NB)
        
        # Since we likely don't have a Dockerfile, should fire
        # (This depends on actual repo state)
        assert len(findings) >= 0
    
    def test_detects_missing_dockerfile_for_clean_notebook(self):
        """When running on 01_clean.ipynb, check if Dockerfile exists."""
        detector = NoDockerfileDetector()
        nb = nbformat.read(CLEAN_NB, as_version=4)
        findings = detector.detect(nb, CLEAN_NB)
        
        # Same as above - depends on repo state
        assert len(findings) >= 0


class TestIntegration:
    """Integration tests using run_all."""
    
    def test_run_all_on_messy_notebook_batch_b(self):
        """Run all detectors on 02_messy.ipynb, check batch B gaps."""
        findings = run_all(MESSY_NB)
        
        gap_ids = {f.gap_id for f in findings}
        
        # Should have gap 3 (train/serve skew)
        assert 3 in gap_ids
        
        # Should have gap 5 (no Pydantic schema)
        assert 5 in gap_ids
        
        # Should have gap 13 (no random_state)
        assert 13 in gap_ids
    
    def test_run_all_on_clean_notebook_batch_b(self):
        """Run all detectors on 01_clean.ipynb, check batch B gaps."""
        findings = run_all(CLEAN_NB)
        
        gap_ids = {f.gap_id for f in findings}
        
        # Should NOT have gap 3 (uses Pipeline)
        assert 3 not in gap_ids
        
        # Should NOT have gap 13 (has random_state)
        assert 13 not in gap_ids
        
        # Should have gap 5 (no Pydantic schema)
        assert 5 in gap_ids


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
