from typing import Optional
import typer
from repopackage.workflow import Workspace


def run_eval(
    last_phase: bool = typer.Option(False, "--last-phase", help="Eval the last active phase"),
    phase_id: Optional[str] = typer.Option(None, "--phase", "-p", help="Specific phase ID"),
):
    """Run tests and quality gates for a phase."""
    ws = Workspace()
    if phase_id:
        phase = ws.phase(phase_id)
    else:
        phase = ws.last_phase()

    typer.echo(f"Running eval for phase: {phase.id}")
    result = phase.eval()

    if result.success:
        typer.echo(f"✓ PASSED — {result.passed} passed")
    else:
        typer.echo(f"✗ FAILED — {result.failed} failed")
        if result.output:
            typer.echo(result.output)

    raise typer.Exit(0 if result.success else 1)
