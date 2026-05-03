"""Detector for gap #15: No Dockerfile."""
import os
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class NoDockerfileDetector(Detector):
    gap_id = 15
    name = "No Dockerfile"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect missing Dockerfile in repo root.
        
        Fires if:
        - No Dockerfile exists in repo root (walk up from notebook directory)
        """
        # Get the notebook's directory
        nb_dir = os.path.dirname(os.path.abspath(nb_path))
        
        # Walk up to find repo root and check for Dockerfile
        # Try current dir, parent dir, and grandparent dir
        possible_roots = [
            nb_dir,
            os.path.dirname(nb_dir),
            os.path.dirname(os.path.dirname(nb_dir))
        ]
        
        has_dockerfile = False
        for root in possible_roots:
            dockerfile_path = os.path.join(root, "Dockerfile")
            if os.path.exists(dockerfile_path):
                has_dockerfile = True
                break
        
        if not has_dockerfile:
            return [
                GapFinding(
                    gap_id=15,
                    name="No Dockerfile",
                    severity="auto_patch",
                    location="repo root",
                    disposition="auto_patched",
                    detail="No Dockerfile found in repository root"
                )
            ]
        
        return []


# Register this detector
register(NoDockerfileDetector())

# Made with Bob
