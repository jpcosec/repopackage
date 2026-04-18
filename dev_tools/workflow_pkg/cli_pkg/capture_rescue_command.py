"""Capture rescue command."""

from __future__ import annotations

import argparse
from pathlib import Path
from workflow_pkg.cli_pkg.command_types import CommandBase


class CaptureRescueCommand(CommandBase):
    """Rescue raw logs for a run."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure the command arguments."""

        parser.add_argument("run_id", help="Unique identifier for the agent run (RUN-XXX).")


    def run(self, args: argparse.Namespace) -> int:
        """Run the command stub."""

        run_dir = Path.cwd() / "runs" / args.run_id / "raw"
        run_dir.mkdir(parents=True, exist_ok=True)

        print(f"Rescuing logs for {args.run_id} to {run_dir}...")
        # Stub for pulling logs
        return 0
