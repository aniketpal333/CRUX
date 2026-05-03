"""Render patch templates and write them to out/<stem>/."""
import os
from jinja2 import Environment, FileSystemLoader


_env = Environment(loader=FileSystemLoader("crux/patches"))


def render_patches(audit_result, out_dir: str, model_name: str = "adult_model.pkl"):
    os.makedirs(out_dir, exist_ok=True)
    ctx = {
        "notebook_name": audit_result.notebook_name,
        "model_name": model_name,
    }
    files_written = []
    for tpl in ("Dockerfile.j2", "requirements.txt.j2", "service.py.j2", "parity_test.py.j2"):
        out_name = tpl.replace(".j2", "")
        out_path = os.path.join(out_dir, out_name)
        rendered = _env.get_template(tpl).render(**ctx)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        files_written.append(out_path)
    return files_written