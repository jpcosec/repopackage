import typer
from repopackage.cli.drawers.commands import (
    list_drawers, add_drawer, promote_drawer, audit_drawers
)

drawers_app = typer.Typer(help="Drawers backlog management.")

drawers_app.command(name="list")(list_drawers)
drawers_app.command(name="add")(add_drawer)
drawers_app.command(name="promote")(promote_drawer)
drawers_app.command(name="audit")(audit_drawers)
