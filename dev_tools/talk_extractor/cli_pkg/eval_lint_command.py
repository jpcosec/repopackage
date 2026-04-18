"""Eval Lint CLI command."""

from __future__ import annotations

import argparse

from talk_extractor.cli_pkg.command_types import CommandBase


class EvalLintCommand(CommandBase):
    """Stub for linting a specific run-id."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure arguments for lint command."""

        parser.add_argument("run_id", help="The run ID to lint.")

    def run(self, args: argparse.Namespace) -> int:
        """Execute the lint stub."""

        print(f"Linting run {args.run_id}...")
        return 0
