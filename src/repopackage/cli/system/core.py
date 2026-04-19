import typer
from repopackage.cli.system.commands import init_project_command

system_app = typer.Typer(help="System management commands.")

@system_app.command()
def info():
    """Display system information."""
    typer.echo("Repopackage System Info")

@system_app.command(name="init-project")
def init_project():
    """Initialize a new repopackage project structure."""
    init_project_command()
