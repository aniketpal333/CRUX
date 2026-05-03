"""Registry of all detectors."""
import nbformat
from ..models import GapFinding
from .base import Detector


_REGISTRY: list[Detector] = []


def register(detector: Detector) -> Detector:
    _REGISTRY.append(detector)
    return detector


def all_detectors() -> list[Detector]:
    return list(_REGISTRY)


def run_all(nb_path: str) -> list[GapFinding]:
    nb = nbformat.read(nb_path, as_version=4)
    findings = []
    for det in _REGISTRY:
        try:
            findings.extend(det.detect(nb, nb_path))
        except Exception as e:
            print(f"Detector {det.name} crashed: {e}")
    return findings