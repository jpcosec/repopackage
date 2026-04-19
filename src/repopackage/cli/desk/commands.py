import typer
from pathlib import Path
from repopackage.workflow import Workspace

board_app = typer.Typer(help="Board management commands.")
tasks_app = typer.Typer(help="Task management commands.")
pills_app = typer.Typer(help="Pill management commands.")


@board_app.command(name="sync")
def sync_board():
    """Synchronize Board.md with current task files."""
    try:
        Workspace().desk.board_sync()
        typer.echo("Board.md synchronized successfully.")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@tasks_app.command(name="atomize")
def atomize_task(task_id: str): #todo: there is a huge conceptual distance between what this does and it's name
    """Generate Context Pills from a task's checklist."""
    try:
        pills = Workspace().desk.tasks.atomize(task_id)
        if not pills:
            typer.echo("No checklist items found.")
            return
        for p in pills:
            typer.echo(f"Created pill: {p.id}")
        typer.echo(f"Updated {task_id} with {len(pills)} pills.")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@pills_app.command(name="inject")
def inject_pill(
    task_id: str = typer.Option(..., "--task", "-t", help="Task ID"),
    pill_id: str = typer.Option(..., "--pill", "-p", help="Pill ID"),
):
    """Link an existing context pill to a task."""
    try:
        Workspace().desk.pills.inject(task_id, pill_id)
        typer.echo(f"Successfully injected pill {pill_id} into task {task_id}.")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo(str(e))
