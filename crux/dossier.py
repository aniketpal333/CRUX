"""Render AuditResult into stakeholder summary + HTML dossier."""
import os
import markdown
from jinja2 import Environment, FileSystemLoader
from .models import AuditResult


_env = Environment(loader=FileSystemLoader("templates"))


def render(audit: AuditResult, out_dir: str) -> dict:
    os.makedirs(out_dir, exist_ok=True)

    ctx = audit.model_dump()
    ctx["cells_detail"] = [c.model_dump() for c in audit.cells_detail]

    summary_md = _env.get_template("stakeholder_summary.md.j2").render(**ctx)
    summary_html = markdown.markdown(summary_md, extensions=["tables"])

    html = _env.get_template("dossier.html.j2").render(
        summary_html=summary_html,
        **ctx,
    )

    summary_path = os.path.join(out_dir, "stakeholder_summary.md")
    html_path = os.path.join(out_dir, "dossier.html")

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_md)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return {"summary_md": summary_path, "html": html_path}