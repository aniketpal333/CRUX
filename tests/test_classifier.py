"""Tests for crux.classifier cell classification logic."""
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell

from crux.classifier import classify_cell


def test_load_bearing_when_joblib_dump():
    """Code cell containing joblib.dump should be classified as load_bearing."""
    cell = new_code_cell(source='joblib.dump(model, "x.joblib")')
    cell["execution_count"] = 5
    
    result = classify_cell(cell, index=0, downstream_refs=set())
    
    assert result.classification == "load_bearing"
    assert "terminal artifact" in result.reason.lower()


def test_dead_when_unreferenced_assignment():
    """Single assignment with no downstream references should be dead."""
    cell = new_code_cell(source="temp = 42")
    cell["execution_count"] = 3
    
    result = classify_cell(cell, index=0, downstream_refs=set())
    
    assert result.classification == "dead"
    assert "no downstream" in result.reason.lower()


def test_exploratory_when_commented_with_hint():
    """Commented-out code with exploratory hint should be exploratory."""
    cell = new_code_cell(source="# try this approach\n# x = 1")
    cell["execution_count"] = None
    
    result = classify_cell(cell, index=0, downstream_refs=set())
    
    assert result.classification == "exploratory"


def test_scaffolding_for_imports():
    """Import statements should be classified as scaffolding."""
    cell = new_code_cell(source="import pandas as pd")
    cell["execution_count"] = 1
    
    result = classify_cell(cell, index=0, downstream_refs=set())
    
    assert result.classification == "scaffolding"


def test_markdown_classified_as_scaffolding():
    """Any markdown cell should be classified as scaffolding."""
    cell = new_markdown_cell(source="# This is a heading\nSome explanation text.")
    
    result = classify_cell(cell, index=0, downstream_refs=set())
    
    assert result.classification == "scaffolding"
    assert result.reason == "markdown narration retained as scaffolding"


def test_dead_when_never_executed_no_hint():
    """Never-executed code cell without exploratory hint should be dead."""
    cell = new_code_cell(source="x = 1")
    cell["execution_count"] = None
    
    result = classify_cell(cell, index=0, downstream_refs=set())
    
    assert result.classification == "dead"
    assert "never executed" in result.reason.lower()

# Made with Bob
