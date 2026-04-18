"""Integrate Merge CLI command."""

from __future__ import annotations

import argparse

from talk_extractor.cli_pkg.command_types import CommandBase


class IntegrateMergeCommand(CommandBase):
    """Stub for merging code and docs for a specific run-id."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure arguments for merge command."""

        parser.add_argument("run_id", help="The run ID to merge.")

    def run(self, args: argparse.Namespace) -> int:
        """Execute the merge stub."""

        print(f"Merging run {args.run_id}...")
        return 0
