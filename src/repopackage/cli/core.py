import typer
from repopackage.cli.system.core import system_app

app = typer.Typer(help="Repopackage CLI tool.")

# Category routing
app.add_typer(system_app, name="system")

def main():
    """Entry point for the rp command."""
    app()

if __name__ == "__main__":
    main()
