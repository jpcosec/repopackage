"""Drawers Promote CLI command."""

from __future__ import annotations

import argparse
from pathlib import Path

from talk_extractor.cli_pkg.command_types import CommandBase


class DrawersPromoteCommand(CommandBase):
    """Promote a specification from drawers to active work."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure arguments for promotion."""

        parser.add_argument("id", help="The ID of the spec to promote.")
        parser.add_argument("--to", required=True, choices=["tasks", "pills"])

    def run(self, args: argparse.Namespace) -> int:
        """Execute the promote command."""

        dest = Path(f"desk/{args.to}")
        dest.mkdir(parents=True, exist_ok=True)
        (dest / f"{args.id}.md").write_text(f"# {args.id}\n\nPromoted stub.\n")
        print(f"Promoted {args.id} to {args.to}.")
        return 0
