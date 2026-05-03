"""Base contracts for gap detectors."""
from abc import ABC, abstractmethod
import nbformat
from ..models import GapFinding


class Detector(ABC):
    gap_id: int
    name: str

    @abstractmethod
    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        ...