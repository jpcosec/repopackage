import typer
from pathlib import Path
from repopackage.workflow import Workspace


def list_drawers():
    """List all specs in drawers."""
    specs = Workspace().drawers.list()
    if not specs:
        typer.echo("No specs in drawers.")
        return
    typer.echo(f"{'ID':<10} {'Domain':<15} {'Title':<30} {'Status'}")
    typer.echo("-" * 60)
    for s in specs:
        typer.echo(f"{s.id:<10} {s.domain:<15} {s.title:<30} {s.status}")


def add_drawer(
    spec: Path = typer.Argument(..., help="Path to spec file"),
    title: str = typer.Option(..., "--title", "-t", help="Human-readable title"),
    domain: str = typer.Option("unknown", "--domain", "-d", help="Problem domain"),
):
    """Add a spec to drawers backlog."""
    if not spec.exists():
        typer.echo(f"Error: File {spec} not found.", err=True)
        raise typer.Exit(code=1)
    result = Workspace().drawers.add(spec, title, domain)
    typer.echo(f"Added spec: {result.id} - {result.title}")


def promote_drawer(
    spec_id: str = typer.Argument(..., help="Spec ID to promote (e.g. D-01)"),
):
    """Promote a drawer spec to an executable task."""
    try:
        task = Workspace().drawers.promote(spec_id)
        typer.echo(f"Promoted {spec_id} → {task.id}: {task.title}")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


def audit_drawers():
    """Audit all drawer specs for completeness."""
    issues = Workspace().drawers.audit()
    if not issues:
        typer.echo("All specs look good.")
        return
    for issue in issues:
        typer.echo(f"  ⚠ {issue}")
