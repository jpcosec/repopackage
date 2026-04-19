import typer
from repopackage.cli.eval.commands import run_eval

eval_app = typer.Typer(help="Evaluation and quality gate commands.")

eval_app.command(name="run")(run_eval)
