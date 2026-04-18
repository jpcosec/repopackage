"""Extract-artifacts CLI command."""

from __future__ import annotations

import argparse

from workflow_pkg.artifact_extractor import extract_artifacts_to_directory
from workflow_pkg.cli_pkg.command_types import CommandBase


class ExtractArtifactsCommand(CommandBase):
    """Extract structured artifacts into files."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure command arguments."""

        parser.add_argument("source", help="Path to the input chat transcript.")
        parser.add_argument("--output-dir", default="arctifacts",
                            help="Directory where extracted artifacts (UML, YAML, etc.) will be saved.")
        parser.add_argument("--include-text", action="store_true")

    def run(self, args: argparse.Namespace) -> int:
        """Run the command."""

        written = extract_artifacts_to_directory(
            args.source, args.output_dir, args.include_text
        )
        print(f"Wrote {len(written) - 1} artifacts to {args.output_dir}")
        return 0
