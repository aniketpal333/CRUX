"""Detector for gap #14: No tests."""
import os
import glob
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoTestsDetector(Detector):
    gap_id = 14
    name = "No tests"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect if no test files exist in the tests/ directory.
        
        Fires if:
        - No tests/test_*.py files exist in the repo root tests/ directory
        """
        # Get the repo root (parent of the notebook's directory)
        nb_dir = os.path.dirname(os.path.abspath(nb_path))
        
        # Look for tests directory at various levels
        # Try current dir, parent dir, and grandparent dir
        possible_roots = [
            nb_dir,
            os.path.dirname(nb_dir),
            os.path.dirname(os.path.dirname(nb_dir))
        ]
        
        has_tests = False
        for root in possible_roots:
            tests_dir = os.path.join(root, "tests")
            if os.path.exists(tests_dir):
                # Check for test_*.py files
                test_files = glob.glob(os.path.join(tests_dir, "test_*.py"))
                if test_files:
                    has_tests = True
                    break
        
        if not has_tests:
            return [
                GapFinding(
                    gap_id=14,
                    name="No tests",
                    severity="auto_patch",
                    location="tests/",
                    disposition="auto_patched",
                    detail="No test files found in tests/ directory"
                )
            ]
        
        return []


# Register this detector
register(NoTestsDetector())

# Made with Bob
