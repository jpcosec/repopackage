"""Desk Pills CLI command."""

from __future__ import annotations

import argparse

from workflow_pkg.cli_pkg.command_types import CommandBase


class DeskPillsCommand(CommandBase):
    """Manage pills on the desk."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Register arguments on a subparser."""

        subparsers = parser.add_subparsers(dest="desk_pill_command", required=True)
        inject_parser = subparsers.add_parser("inject", help="Inject context into a pill.")
        inject_parser.add_argument("pill_id", help="Target pill/task ID.")
        inject_parser.add_argument(
            "--with", "-w", action="append", required=True, help="Context pill IDs to inject."
        )

    def run(self, args: argparse.Namespace) -> int:
        """Execute the pills command."""

        if args.desk_pill_command == "inject":
            pills = ", ".join(getattr(args, "with"))
            print(f"STUB: Injecting context '{pills}' into pill '{args.pill_id}'")
        return 0
