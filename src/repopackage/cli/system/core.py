import typer

system_app = typer.Typer(help="System management commands.")

@system_app.command()
def info():
    """Display system information."""
    typer.echo("Repopackage System Info")
