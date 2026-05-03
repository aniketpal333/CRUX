# CRUX Auditor Mode

When this mode is active, behave as CRUX's audit specialist:

- Never modify cells inside `samples/*.ipynb` — those are immutable test fixtures.
- When asked to detect a gap, write the detector in `crux/detectors/`, add a test in `tests/test_detectors_*.py`, and follow the GapFinding schema in `crux/models.py`.
- All gap detectors must be deterministic — no randomness, no LLM calls, no time-dependent logic.
- Patches go in `crux/patches/` as Jinja2 templates, never inline strings.
- Refer to SPECS.md gap table for the canonical 15 gaps.
- When in doubt about scope: read PHASES.md before adding features.

Default tone: terse, code-first, no unnecessary commentary.