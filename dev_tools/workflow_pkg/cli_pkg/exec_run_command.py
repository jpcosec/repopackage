"""Exec run command."""

from __future__ import annotations

import argparse
from workflow_pkg.cli_pkg.command_types import CommandBase


class ExecRunCommand(CommandBase):
    """Run an agent for a specific task."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure the command arguments."""

        parser.add_argument("agent", help="Agent name or ID.")
        parser.add_argument("--task", required=True, help="Task ID to execute.")

    def run(self, args: argparse.Namespace) -> int:
        """Run the command stub."""

        print(f"Executing agent '{args.agent}' for task '{args.task}'...")
        # Stub for running agents
        return 0
