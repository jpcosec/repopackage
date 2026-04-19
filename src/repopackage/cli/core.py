import typer
from repopackage.cli.system.core import system_app
from repopackage.cli.desk.core import desk_app
from repopackage.cli.drawers.core import drawers_app

app = typer.Typer(help="Repopackage CLI tool.")

# Category routing
app.add_typer(system_app, name="system")
app.add_typer(desk_app, name="desk")
app.add_typer(drawers_app, name="drawers")

def main():
    """Entry point for the rp command."""
    app()

if __name__ == "__main__":
    main()
