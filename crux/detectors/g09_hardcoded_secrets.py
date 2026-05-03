"""Detector for gap #9: Hardcoded secrets."""
import re
import nbformat
from ..models import GapFinding
from .base import Detector
from .registry import register


class HardcodedSecretsDetector(Detector):
    gap_id = 9
    name = "Hardcoded secrets"

    def detect(self, nb: nbformat.NotebookNode, nb_path: str) -> list[GapFinding]:
        """
        Detect hardcoded API keys, passwords, and JWTs.
        
        Patterns:
        - API keys: (sk|kg|tok|pat)_(live|test|prod)?_[A-Za-z0-9_]{16,}
        - Passwords: password|passwd|pwd = "..."
        - JWTs: eyJ[A-Za-z0-9_-]{20,}
        """
        findings = []
        
        # Regex patterns
        api_key_pattern = re.compile(r'(sk|kg|tok|pat)_(live|test|prod)?_[A-Za-z0-9_]{16,}')
        password_pattern = re.compile(r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']', re.IGNORECASE)
        jwt_pattern = re.compile(r'eyJ[A-Za-z0-9_-]{20,}')
        
        for idx, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            
            source = cell.source
            
            # Check for API keys
            api_matches = api_key_pattern.findall(source)
            for match in api_matches:
                findings.append(
                    GapFinding(
                        gap_id=9,
                        name="Hardcoded secrets",
                        severity="blocker",
                        location=f"cell {idx}",
                        disposition="blocker",
                        detail=f"Hardcoded API key pattern detected: {match[0]}_..."
                    )
                )
            
            # Check for passwords
            pwd_matches = password_pattern.findall(source)
            for match in pwd_matches:
                findings.append(
                    GapFinding(
                        gap_id=9,
                        name="Hardcoded secrets",
                        severity="blocker",
                        location=f"cell {idx}",
                        disposition="blocker",
                        detail=f"Hardcoded password assignment: {match} = ..."
                    )
                )
            
            # Check for JWTs
            jwt_matches = jwt_pattern.findall(source)
            for match in jwt_matches:
                findings.append(
                    GapFinding(
                        gap_id=9,
                        name="Hardcoded secrets",
                        severity="blocker",
                        location=f"cell {idx}",
                        disposition="blocker",
                        detail=f"Hardcoded JWT token detected: {match[:20]}..."
                    )
                )
        
        return findings


# Register this detector
register(HardcodedSecretsDetector())

# Made with Bob
