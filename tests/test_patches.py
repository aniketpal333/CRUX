"""Tests for patch template rendering."""
import os
import tempfile
import shutil
from datetime import datetime, UTC
from crux.models import AuditResult, CellCounts, GapCounts
from crux.patches.render import render_patches


def test_render_patches_creates_all_files():
    """Test that render_patches creates all 4 expected files."""
    # Create a mock AuditResult
    audit_result = AuditResult(
        notebook_name="02_messy",
        audit_timestamp=datetime.now(UTC).isoformat(),
        verdict="READY_WITH_DECISIONS",
        cells=CellCounts(
            total=20,
            load_bearing=8,
            scaffolding=5,
            exploratory=4,
            dead=3
        ),
        gaps=GapCounts(
            total=10,
            blockers=1,
            auto_patched=6,
            decisions_required=3,
            dismissed=0
        )
    )
    
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = os.path.join(tmpdir, "test_out")
        
        # Render patches
        files_written = render_patches(audit_result, out_dir, model_name="adult_model.pkl")
        
        # Assert all 4 files were created
        assert len(files_written) == 4
        expected_files = ["Dockerfile", "requirements.txt", "service.py", "parity_test.py"]
        for expected in expected_files:
            expected_path = os.path.join(out_dir, expected)
            assert expected_path in files_written
            assert os.path.exists(expected_path)


def test_service_py_contains_expected_content():
    """Test that service.py contains FastAPI, Pydantic models, and expected fields."""
    audit_result = AuditResult(
        notebook_name="02_messy",
        audit_timestamp=datetime.now(UTC).isoformat(),
        verdict="READY_WITH_DECISIONS",
        cells=CellCounts(total=20, load_bearing=8, scaffolding=5, exploratory=4, dead=3),
        gaps=GapCounts(total=10, blockers=1, auto_patched=6, decisions_required=3, dismissed=0)
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = os.path.join(tmpdir, "test_out")
        render_patches(audit_result, out_dir, model_name="adult_model.pkl")
        
        service_path = os.path.join(out_dir, "service.py")
        with open(service_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Assert expected imports and framework
        assert "from fastapi import FastAPI" in content
        assert "from pydantic import BaseModel" in content
        assert "import joblib" in content
        
        # Assert Pydantic model with expected fields
        assert "class IncomePredictRequest(BaseModel):" in content
        assert "age: int" in content
        assert "workclass: str" in content
        
        # Assert notebook name is embedded
        assert "02_messy" in content
        
        # Assert model loading
        assert 'joblib.load("models/adult_model.pkl")' in content


def test_requirements_txt_contains_expected_dependencies():
    """Test that requirements.txt contains all necessary dependencies."""
    audit_result = AuditResult(
        notebook_name="03_chaos",
        audit_timestamp=datetime.now(UTC).isoformat(),
        verdict="BLOCKED",
        cells=CellCounts(total=30, load_bearing=10, scaffolding=8, exploratory=7, dead=5),
        gaps=GapCounts(total=15, blockers=3, auto_patched=8, decisions_required=4, dismissed=0)
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = os.path.join(tmpdir, "test_out")
        render_patches(audit_result, out_dir)
        
        req_path = os.path.join(out_dir, "requirements.txt")
        with open(req_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Assert all critical dependencies are present
        assert "fastapi" in content
        assert "uvicorn" in content
        assert "pydantic" in content
        assert "scikit-learn" in content
        assert "pandas" in content
        assert "joblib" in content
        assert "structlog" in content


def test_dockerfile_contains_expected_commands():
    """Test that Dockerfile contains expected build and run commands."""
    audit_result = AuditResult(
        notebook_name="01_clean",
        audit_timestamp=datetime.now(UTC).isoformat(),
        verdict="CLEAN",
        cells=CellCounts(total=15, load_bearing=12, scaffolding=2, exploratory=1, dead=0),
        gaps=GapCounts(total=2, blockers=0, auto_patched=2, decisions_required=0, dismissed=0)
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = os.path.join(tmpdir, "test_out")
        render_patches(audit_result, out_dir)
        
        dockerfile_path = os.path.join(out_dir, "Dockerfile")
        with open(dockerfile_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Assert base image and setup
        assert "FROM python:3.11-slim" in content
        assert "WORKDIR /app" in content
        assert "COPY requirements.txt" in content
        assert "RUN pip install" in content
        
        # Assert service exposure and startup
        assert "EXPOSE 8000" in content
        assert "uvicorn" in content
        assert "service:app" in content


def test_parity_test_contains_expected_structure():
    """Test that parity_test.py contains joblib loading and test functions."""
    audit_result = AuditResult(
        notebook_name="02_messy",
        audit_timestamp=datetime.now(UTC).isoformat(),
        verdict="READY_WITH_DECISIONS",
        cells=CellCounts(total=20, load_bearing=8, scaffolding=5, exploratory=4, dead=3),
        gaps=GapCounts(total=10, blockers=1, auto_patched=6, decisions_required=3, dismissed=0)
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = os.path.join(tmpdir, "test_out")
        render_patches(audit_result, out_dir, model_name="test_model.pkl")
        
        test_path = os.path.join(out_dir, "parity_test.py")
        with open(test_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Assert imports
        assert "import joblib" in content
        assert "import pandas as pd" in content
        
        # Assert model path uses the provided model_name
        assert 'MODEL_PATH = "models/test_model.pkl"' in content
        
        # Assert test functions exist
        assert "def test_model_loads():" in content
        assert "def test_model_predicts_on_sample():" in content
        assert "joblib.load(MODEL_PATH)" in content


def test_render_patches_with_custom_model_name():
    """Test that custom model_name is correctly propagated to templates."""
    audit_result = AuditResult(
        notebook_name="custom_notebook",
        audit_timestamp=datetime.now(UTC).isoformat(),
        verdict="CLEAN",
        cells=CellCounts(total=10, load_bearing=8, scaffolding=1, exploratory=1, dead=0),
        gaps=GapCounts(total=1, blockers=0, auto_patched=1, decisions_required=0, dismissed=0)
    )
    
    custom_model = "my_custom_model.joblib"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = os.path.join(tmpdir, "test_out")
        render_patches(audit_result, out_dir, model_name=custom_model)
        
        # Check service.py
        service_path = os.path.join(out_dir, "service.py")
        with open(service_path, "r", encoding="utf-8") as f:
            service_content = f.read()
        assert f'joblib.load("models/{custom_model}")' in service_content
        
        # Check parity_test.py
        test_path = os.path.join(out_dir, "parity_test.py")
        with open(test_path, "r", encoding="utf-8") as f:
            test_content = f.read()
        assert f'MODEL_PATH = "models/{custom_model}"' in test_content


def test_render_patches_creates_output_directory():
    """Test that render_patches creates the output directory if it doesn't exist."""
    audit_result = AuditResult(
        notebook_name="test",
        audit_timestamp=datetime.now(UTC).isoformat(),
        verdict="CLEAN",
        cells=CellCounts(total=5, load_bearing=5, scaffolding=0, exploratory=0, dead=0),
        gaps=GapCounts(total=0, blockers=0, auto_patched=0, decisions_required=0, dismissed=0)
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Use a nested path that doesn't exist
        out_dir = os.path.join(tmpdir, "nested", "path", "test_out")
        assert not os.path.exists(out_dir)
        
        render_patches(audit_result, out_dir)
        
        # Directory should now exist
        assert os.path.exists(out_dir)
        assert os.path.isdir(out_dir)

# Made with Bob
