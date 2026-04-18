"""Integrate Rollback CLI command."""

from __future__ import annotations

import argparse

from workflow_pkg.cli_pkg.command_types import CommandBase


class IntegrateRollbackCommand(CommandBase):
    """Stub for reverting integration for a specific run-id."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure arguments for rollback command."""

        parser.add_argument("run_id", help="The run ID to rollback.")

    def run(self, args: argparse.Namespace) -> int:
        """Execute the rollback stub."""

        print(f"Rolling back run {args.run_id}...")
        return 0
