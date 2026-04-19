"""Extract-turns CLI command."""

from __future__ import annotations

import argparse

from talk_extractor.cli_pkg.command_types import CommandBase
from talk_extractor.extract_gemini_turns import extract_file_to_directory


class ExtractTurnsCommand(CommandBase):
    """Extract conversation turns into markdown files."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure command arguments."""

        parser.add_argument("source")
        parser.add_argument("--output-dir", default="extracted talk")

    def run(self, args: argparse.Namespace) -> int:
        """Run the command."""

        written = extract_file_to_directory(args.source, args.output_dir)
        print(f"Wrote {len(written)} turn files to {args.output_dir}")
        return 0
