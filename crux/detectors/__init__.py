"""Auto-import all detector modules so they self-register."""
from . import (
    g01_no_input_validation,
    g02_no_logging,
    g03_train_serve_skew,
    g04_no_versioning,
    g05_no_pydantic_schema,
    g06_missing_model_artifact,
    g07_no_input_range,
    g08_no_drift_detection,
    g09_hardcoded_secrets,
    g10_no_rate_limit,
    g11_no_batch_endpoint,
    g12_no_auth,
    g13_no_repro_metadata,
    g14_no_tests,
    g15_no_dockerfile,
)
from .registry import all_detectors, run_all

__all__ = [
    "g01_no_input_validation",
    "g02_no_logging",
    "g03_train_serve_skew",
    "g04_no_versioning",
    "g05_no_pydantic_schema",
    "g06_missing_model_artifact",
    "g07_no_input_range",
    "g08_no_drift_detection",
    "g09_hardcoded_secrets",
    "g10_no_rate_limit",
    "g11_no_batch_endpoint",
    "g12_no_auth",
    "g13_no_repro_metadata",
    "g14_no_tests",
    "g15_no_dockerfile",
    "all_detectors",
    "run_all",
]

# Made with Bob
