"""Eval Test CLI command."""

from __future__ import annotations

import argparse

from workflow_pkg.cli_pkg.command_types import CommandBase


class EvalTestCommand(CommandBase):
    """Stub for running tests for a specific run-id."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure arguments for test command."""

        parser.add_argument("run_id", help="The run ID to test.")

    def run(self, args: argparse.Namespace) -> int:
        """Execute the test stub."""

        print(f"Running tests for run {args.run_id}...")
        return 0
