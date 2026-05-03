"""CRUX command-line interface."""
import os
import sys
import click

from .audit import audit_notebook
from .dossier import render
from .recovery import write_recovered
from .patches.render import render_patches


@click.group()
def main():
    """CRUX - Code Recovery from Undocumented eXperiments."""


@main.command()
@click.argument("notebook", type=click.Path(exists=True))
@click.option("--out", "out_dir", default=None, help="Output directory")
@click.option("--strict", is_flag=True, help="Exit code 2 if BLOCKED")
def audit(notebook, out_dir, strict):
    """Run a CRUX audit on NOTEBOOK."""
    result = audit_notebook(notebook)
    if out_dir is None:
        stem = os.path.splitext(os.path.basename(notebook))[0]
        out_dir = f"out/{stem}"

    paths = render(result, out_dir)
    write_recovered(notebook, out_dir)
    render_patches(result, out_dir)

    click.echo(f"\n=== CRUX AUDIT - {result.notebook_name} ===")
    click.echo(f"Verdict: {result.verdict}")
    click.echo(f"Cells: {result.cells.total} total - "
               f"{result.cells.load_bearing} load-bearing, "
               f"{result.cells.scaffolding} scaffolding, "
               f"{result.cells.exploratory} exploratory, "
               f"{result.cells.dead} dead")
    click.echo(f"Gaps: {result.gaps.blockers} blockers, "
               f"{result.gaps.decisions_required} decisions, "
               f"{result.gaps.auto_patched} auto-patched")
    click.echo(f"\nDossier: {paths['html']}")
    click.echo(f"Summary: {paths['summary_md']}")

    if strict and result.verdict == "BLOCKED":
        sys.exit(2)


if __name__ == "__main__":
    main()