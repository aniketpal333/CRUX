"""The dossier must be byte-identical across runs (modulo timestamp)."""
from crux.audit import audit_notebook
from crux.dossier import render


def test_dossier_byte_identical(tmp_path):
    nb = "samples/02_messy.ipynb"
    out_a = tmp_path / "a"
    out_b = tmp_path / "b"

    audit_a = audit_notebook(nb)
    audit_a.audit_timestamp = "2026-01-01T00:00:00Z"
    render(audit_a, str(out_a))

    audit_b = audit_notebook(nb)
    audit_b.audit_timestamp = "2026-01-01T00:00:00Z"
    render(audit_b, str(out_b))

    summary_a = (out_a / "stakeholder_summary.md").read_text()
    summary_b = (out_b / "stakeholder_summary.md").read_text()
    assert summary_a == summary_b