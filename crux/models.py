"""Pydantic models for the CRUX pipeline. The audit contract."""
from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, Field

CellClass = Literal["load_bearing", "scaffolding", "exploratory", "dead"]
Disposition = Literal["auto_patched", "decisions_required", "blocker", "dismissed"]
Severity = Literal["blocker", "decision", "auto_patch", "info"]


class CellRecord(BaseModel):
    index: int
    execution_count: Optional[int]
    classification: CellClass
    source_preview: str
    citation: str
    reason: str


class GapFinding(BaseModel):
    gap_id: int
    name: str
    severity: Severity
    location: str
    disposition: Disposition
    options: int = 0
    patch_path: Optional[str] = None
    detail: str = ""


class CellCounts(BaseModel):
    total: int
    load_bearing: int
    scaffolding: int
    exploratory: int
    dead: int


class GapCounts(BaseModel):
    total: int
    blockers: int
    auto_patched: int
    decisions_required: int
    dismissed: int


class AuditResult(BaseModel):
    notebook_name: str
    audit_timestamp: str
    crux_version: str = "0.1.0"
    verdict: Literal["CLEAN", "READY_WITH_DECISIONS", "BLOCKED"]
    cells: CellCounts
    gaps: GapCounts
    blockers: list[dict] = Field(default_factory=list)
    decisions: list[dict] = Field(default_factory=list)
    auto_patched_gaps: list[dict] = Field(default_factory=list)
    top_recommendation: Optional[str] = None
    cells_detail: list[CellRecord] = Field(default_factory=list)