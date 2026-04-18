"""Desk Tasks CLI command."""

from __future__ import annotations

import argparse

from workflow_pkg.cli_pkg.command_types import CommandBase


class DeskTasksCommand(CommandBase):
    """Manage tasks on the desk."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Register arguments on a subparser."""

        subparsers = parser.add_subparsers(dest="desk_task_command", required=True)
        atomize_parser = subparsers.add_parser("atomize", help="Break a task into atomic pills.")
        atomize_parser.add_argument("task", help="Task ID (T-XXX) or short description.")
        atomize_parser.add_argument(
            "--min-size", "-m", type=int, default=1, 
            help="Minimum number of context pills to generate."
        )

    def run(self, args: argparse.Namespace) -> int:
        """Execute the tasks command."""

        if args.desk_task_command == "atomize":
            print(f"STUB: Atomizing task '{args.task}' (min-size: {args.min_size})")
        return 0
