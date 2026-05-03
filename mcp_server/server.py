"""FastMCP server exposing CRUX as MCP tools."""
from fastmcp import FastMCP
from crux.audit import audit_notebook
from crux.dossier import render
from crux.recovery import write_recovered
from crux.patches.render import render_patches


mcp = FastMCP("crux")
_AUDIT_CACHE: dict[str, dict] = {}


@mcp.tool()
def audit_notebook_tool(notebook_path: str, generate_artifacts: bool = True) -> dict:
    """Run a CRUX audit. Returns AuditResult dict. If generate_artifacts is True,
    also writes dossier + recovered pipeline + autopatches to out/<stem>/."""
    result = audit_notebook(notebook_path)
    out_dir = f"out/{result.notebook_name.replace('.ipynb', '')}"
    if generate_artifacts:
        render(result, out_dir)
        write_recovered(notebook_path, out_dir)
        render_patches(result, out_dir)
    payload = result.model_dump()
    _AUDIT_CACHE[notebook_path] = payload
    return payload


@mcp.tool()
def get_dossier(notebook_path: str) -> dict:
    """Return file paths to dossier artifacts."""
    if notebook_path not in _AUDIT_CACHE:
        audit_notebook_tool(notebook_path)
    stem = notebook_path.split("/")[-1].split("\\")[-1].replace(".ipynb", "")
    return {
        "dossier_html": f"out/{stem}/dossier.html",
        "stakeholder_summary": f"out/{stem}/stakeholder_summary.md",
        "recovered_pipeline": f"out/{stem}/recovered_pipeline.py",
    }


@mcp.tool()
def list_open_decisions(notebook_path: str) -> list[dict]:
    """List decision-required gaps."""
    if notebook_path not in _AUDIT_CACHE:
        audit_notebook_tool(notebook_path, generate_artifacts=False)
    return _AUDIT_CACHE[notebook_path].get("decisions", [])


@mcp.tool()
def compare_notebooks(nb_path_a: str, nb_path_b: str) -> dict:
    """Compare two notebooks: verdict, blocker count delta."""
    a = audit_notebook(nb_path_a)
    b = audit_notebook(nb_path_b)
    return {
        "a": {"name": a.notebook_name, "verdict": a.verdict, "blockers": a.gaps.blockers},
        "b": {"name": b.notebook_name, "verdict": b.verdict, "blockers": b.gaps.blockers},
        "verdict_changed": a.verdict != b.verdict,
        "blockers_delta": b.gaps.blockers - a.gaps.blockers,
    }


@mcp.tool()
def block_merge_if_critical_gaps(notebook_path: str) -> dict:
    """CI gate: returns block decision."""
    result = audit_notebook(notebook_path)
    if result.verdict == "BLOCKED":
        return {
            "block": True,
            "reason": f"{result.gaps.blockers} critical blocker(s) detected",
            "blockers": result.blockers,
            "verdict": result.verdict,
        }
    return {
        "block": False,
        "reason": "audit passed",
        "blockers": [],
        "verdict": result.verdict,
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()