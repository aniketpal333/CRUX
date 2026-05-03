"""Tests for crux.models Pydantic schemas."""
import json
import pytest
from pydantic import ValidationError

from crux.models import AuditResult, GapFinding, CellCounts, GapCounts


def test_audit_result_round_trips_through_json():
    """AuditResult should serialize to JSON and deserialize back identically."""
    original = AuditResult(
        notebook_name="test.ipynb",
        audit_timestamp="2026-05-03T01:00:00Z",
        crux_version="0.1.0",
        verdict="CLEAN",
        cells=CellCounts(
            total=10,
            load_bearing=5,
            scaffolding=2,
            exploratory=2,
            dead=1
        ),
        gaps=GapCounts(
            total=0,
            blockers=0,
            auto_patched=0,
            decisions_required=0,
            dismissed=0
        ),
        blockers=[],
        decisions=[],
        auto_patched_gaps=[],
        top_recommendation="No issues found",
        cells_detail=[]
    )
    
    # Serialize to JSON
    json_str = original.model_dump_json()
    
    # Deserialize back
    reconstructed = AuditResult.model_validate_json(json_str)
    
    # Should be identical
    assert reconstructed == original
    assert reconstructed.verdict == "CLEAN"
    assert reconstructed.notebook_name == "test.ipynb"
    assert reconstructed.cells.total == 10


def test_invalid_verdict_raises_validation_error():
    """AuditResult should reject invalid verdict values."""
    with pytest.raises(ValidationError) as exc_info:
        AuditResult(
            notebook_name="test.ipynb",
            audit_timestamp="2026-05-03T01:00:00Z",
            verdict="INVALID_VERDICT",  # Not in Literal["CLEAN", "READY_WITH_DECISIONS", "BLOCKED"]
            cells=CellCounts(
                total=10,
                load_bearing=5,
                scaffolding=2,
                exploratory=2,
                dead=1
            ),
            gaps=GapCounts(
                total=0,
                blockers=0,
                auto_patched=0,
                decisions_required=0,
                dismissed=0
            )
        )
    
    # Verify the error mentions the verdict field
    assert "verdict" in str(exc_info.value).lower()


def test_gap_finding_requires_gap_id_and_severity():
    """GapFinding should require gap_id and severity fields."""
    # Missing gap_id
    with pytest.raises(ValidationError) as exc_info:
        GapFinding(
            name="Test Gap",
            severity="blocker",
            location="test.py:10",
            disposition="blocker"
        )
    assert "gap_id" in str(exc_info.value).lower()
    
    # Missing severity
    with pytest.raises(ValidationError) as exc_info:
        GapFinding(
            gap_id=1,
            name="Test Gap",
            location="test.py:10",
            disposition="blocker"
        )
    assert "severity" in str(exc_info.value).lower()
    
    # Valid construction should work
    valid_gap = GapFinding(
        gap_id=1,
        name="Test Gap",
        severity="blocker",
        location="test.py:10",
        disposition="blocker"
    )
    assert valid_gap.gap_id == 1
    assert valid_gap.severity == "blocker"

# Made with Bob
