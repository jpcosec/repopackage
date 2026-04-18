"""Drawers Add CLI command."""

from __future__ import annotations

import argparse
from pathlib import Path

from workflow_pkg.cli_pkg.command_types import CommandBase

BOARD_PATH = Path("desk/drawers/Board.md")


class DrawersAddCommand(CommandBase):
    """Add a new specification to the drawers board."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure arguments for adding a spec."""

        parser.add_argument("spec", help="Path to the specification file.")
        parser.add_argument("--title", "-t", required=True, help="Spec title.")
        parser.add_argument("--domain", required=True, help="Domain area.")

    def run(self, args: argparse.Namespace) -> int:
        """Execute the add command."""

        if not BOARD_PATH.exists():
            return 1
        lines = BOARD_PATH.read_text(encoding="utf-8").splitlines()
        count = len([line for line in lines if line.startswith("| SPEC-")])
        new_id = f"SPEC-{count + 1:03d}"
        row = f"| {new_id} | {args.title} | {args.domain} | {args.spec} | pending |"
        with open(BOARD_PATH, "a", encoding="utf-8") as f:
            f.write(row + "\n")
        print(f"Added {new_id} to drawers.")
        return 0
