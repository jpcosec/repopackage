"""Drawers List CLI command."""

from __future__ import annotations

import argparse
from pathlib import Path

from talk_extractor.cli_pkg.command_types import CommandBase

BOARD_PATH = Path("desk/drawers/Board.md")


class DrawersListCommand(CommandBase):
    """List all specifications currently in drawers."""

    def run(self, args: argparse.Namespace) -> int:
        """Execute the list command."""

        if not BOARD_PATH.exists():
            print("Board not found.")
            return 1
        print(BOARD_PATH.read_text(encoding="utf-8"))
        return 0
