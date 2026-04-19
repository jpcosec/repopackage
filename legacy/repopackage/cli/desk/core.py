import typer
from repopackage.cli.desk.commands import board_app, tasks_app, pills_app

desk_app = typer.Typer(help="Project desk commands.")

desk_app.add_typer(board_app, name="board", help="Board management.")
desk_app.add_typer(tasks_app, name="tasks", help="Task management.")
desk_app.add_typer(pills_app, name="pills", help="Context pill management.")
