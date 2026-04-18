"""Run-semantic CLI command."""

from __future__ import annotations

import argparse

from workflow_pkg.cli_pkg.command_types import CommandBase
from workflow_pkg.semantic_packager import prepare_semantic_workspace


class RunSemanticCommand(CommandBase):
    """Prepare semantic scaffolding and emit next-agent pointers."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure command arguments."""

        parser.add_argument("source", help="Path to the input chat transcript.")
        parser.add_argument("--turns-dir", default="extracted talk", help="Input turns directory.")
        parser.add_argument("--artifacts-dir", default="arctifacts", help="Input artifacts directory.")
        parser.add_argument("--semantic-dir", default="semantic_output", help="Output workspace directory.")
        parser.add_argument("--clean", action="store_true", help="Wipe output directory before starting.")

    def run(self, args: argparse.Namespace) -> int:
        """Run the command."""

        prepare_semantic_workspace(
            args.source,
            args.turns_dir,
            args.artifacts_dir,
            args.semantic_dir,
            False, # include_text
            args.clean,
        )
        return 0
