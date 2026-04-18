"""Capture normalize command."""

from __future__ import annotations

import argparse
from pathlib import Path
from workflow_pkg.cli_pkg.command_types import CommandBase


class CaptureNormalizeCommand(CommandBase):
    """Normalize captured logs into evidence.json."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure the command arguments."""

        parser.add_argument("run_id", help="Run ID (e.g., RUN-001).")

    def run(self, args: argparse.Namespace) -> int:
        """Run the command stub."""

        norm_dir = Path.cwd() / "runs" / args.run_id / "normalized"
        norm_dir.mkdir(parents=True, exist_ok=True)

        print(f"Normalizing logs for {args.run_id} into {norm_dir}/evidence.json...")
        # Stub for generating evidence.json
        return 0
