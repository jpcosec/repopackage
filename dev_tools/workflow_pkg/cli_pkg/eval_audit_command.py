"""Eval Audit CLI command."""

from __future__ import annotations

import argparse

from workflow_pkg.cli_pkg.command_types import CommandBase


class EvalAuditCommand(CommandBase):
    """Stub for full audit for a specific run-id."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure arguments for audit command."""

        parser.add_argument("run_id", help="Unique identifier for the agent run (RUN-XXX).")

    def run(self, args: argparse.Namespace) -> int:
        """Execute the audit stub."""

        print(f"Auditing run {args.run_id}...")
        return 0
