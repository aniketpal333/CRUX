"""Tests for gap detectors g06, g07, g10, g11, g12."""
import os
import pytest
from crux.detectors.registry import run_all
from crux.detectors.g06_missing_model_artifact import MissingModelArtifactDetector
from crux.detectors.g07_no_input_range import NoInputRangeDetector
from crux.detectors.g10_no_rate_limit import NoRateLimitDetector
from crux.detectors.g11_no_batch_endpoint import NoBatchEndpointDetector
from crux.detectors.g12_no_auth import NoAuthDetector
import nbformat


# Paths to sample notebooks
MESSY_NB = "samples/02_messy.ipynb"
CLEAN_NB = "samples/01_clean.ipynb"


class TestG06MissingModelArtifact:
    """Test gap #6: Missing model artifact detector."""
    
    def test_no_detection_when_model_saved_in_messy_notebook(self):
        """02_messy.ipynb trains and saves model."""
        detector = MissingModelArtifactDetector()
        nb = nbformat.read(MESSY_NB, as_version=4)
        findings = detector.detect(nb, MESSY_NB)
        
        # Messy notebook saves the model, so should not fire
        assert len(findings) == 0
    
    def test_no_detection_when_model_saved_in_clean_notebook(self):
        """01_clean.ipynb trains and saves model."""
        detector = MissingModelArtifactDetector()
        nb = nbformat.read(CLEAN_NB, as_version=4)
        findings = detector.detect(nb, CLEAN_NB)
        
        # Clean notebook saves the model, so should not fire
        assert len(findings) == 0


class TestG07NoInputRange:
    """Test gap #7: No input range validation detector."""
    
    def test_detects_missing_range_validation_in_messy_notebook(self):
        """02_messy.ipynb has no .clip() or min/max bounds."""
        detector = NoInputRangeDetector()
        nb = nbformat.read(MESSY_NB, as_version=4)
        findings = detector.detect(nb, MESSY_NB)
        
        # Should detect missing range validation
        assert len(findings) == 1
        assert findings[0].gap_id == 7
        assert findings[0].severity == "decision"
        assert findings[0].disposition == "decisions_required"
        assert findings[0].options == 2
    
    def test_detects_missing_range_validation_in_clean_notebook(self):
        """01_clean.ipynb also lacks range validation."""
        detector = NoInputRangeDetector()
        nb = nbformat.read(CLEAN_NB, as_version=4)
        findings = detector.detect(nb, CLEAN_NB)
        
        # Clean notebook also lacks range validation
        assert len(findings) == 1


class TestG10NoRateLimit:
    """Test gap #10: No rate limiting detector."""
    
    def test_always_fires_on_messy_notebook(self):
        """Always fires - notebooks lack rate limiting."""
        detector = NoRateLimitDetector()
        nb = nbformat.read(MESSY_NB, as_version=4)
        findings = detector.detect(nb, MESSY_NB)
        
        assert len(findings) == 1
        assert findings[0].gap_id == 10
        assert findings[0].severity == "auto_patch"
        assert findings[0].disposition == "auto_patched"
    
    def test_always_fires_on_clean_notebook(self):
        """Always fires - notebooks lack rate limiting."""
        detector = NoRateLimitDetector()
        nb = nbformat.read(CLEAN_NB, as_version=4)
        findings = detector.detect(nb, CLEAN_NB)
        
        assert len(findings) == 1


class TestG11NoBatchEndpoint:
    """Test gap #11: No batch endpoint detector."""
    
    def test_always_fires_on_messy_notebook(self):
        """Always fires - notebooks lack batch endpoints."""
        detector = NoBatchEndpointDetector()
        nb = nbformat.read(MESSY_NB, as_version=4)
        findings = detector.detect(nb, MESSY_NB)
        
        assert len(findings) == 1
        assert findings[0].gap_id == 11
        assert findings[0].severity == "decision"
        assert findings[0].disposition == "decisions_required"
        assert findings[0].options == 2
    
    def test_always_fires_on_clean_notebook(self):
        """Always fires - notebooks lack batch endpoints."""
        detector = NoBatchEndpointDetector()
        nb = nbformat.read(CLEAN_NB, as_version=4)
        findings = detector.detect(nb, CLEAN_NB)
        
        assert len(findings) == 1


class TestG12NoAuth:
    """Test gap #12: No authentication detector."""
    
    def test_always_fires_on_messy_notebook(self):
        """Always fires - notebooks lack authentication."""
        detector = NoAuthDetector()
        nb = nbformat.read(MESSY_NB, as_version=4)
        findings = detector.detect(nb, MESSY_NB)
        
        assert len(findings) == 1
        assert findings[0].gap_id == 12
        assert findings[0].severity == "decision"
        assert findings[0].disposition == "decisions_required"
        assert findings[0].options == 3
    
    def test_always_fires_on_clean_notebook(self):
        """Always fires - notebooks lack authentication."""
        detector = NoAuthDetector()
        nb = nbformat.read(CLEAN_NB, as_version=4)
        findings = detector.detect(nb, CLEAN_NB)
        
        assert len(findings) == 1


class TestIntegration:
    """Integration tests using run_all."""
    
    def test_run_all_on_messy_notebook_batch_c(self):
        """Run all detectors on 02_messy.ipynb, check batch C gaps."""
        findings = run_all(MESSY_NB)
        
        gap_ids = {f.gap_id for f in findings}
        
        # Should NOT have gap 6 (model is saved)
        assert 6 not in gap_ids
        
        # Should have gap 7 (no input range validation)
        assert 7 in gap_ids
        
        # Should have gap 10 (always fires)
        assert 10 in gap_ids
        
        # Should have gap 11 (always fires)
        assert 11 in gap_ids
        
        # Should have gap 12 (always fires)
        assert 12 in gap_ids
    
    def test_run_all_on_clean_notebook_batch_c(self):
        """Run all detectors on 01_clean.ipynb, check batch C gaps."""
        findings = run_all(CLEAN_NB)
        
        gap_ids = {f.gap_id for f in findings}
        
        # Should NOT have gap 6 (model is saved)
        assert 6 not in gap_ids
        
        # Should have gap 7 (no input range validation)
        assert 7 in gap_ids
        
        # Should have gap 10 (always fires)
        assert 10 in gap_ids
        
        # Should have gap 11 (always fires)
        assert 11 in gap_ids
        
        # Should have gap 12 (always fires)
        assert 12 in gap_ids


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
