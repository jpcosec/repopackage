"""Init CLI command for scaffolding the workflow."""

from __future__ import annotations

import argparse
from pathlib import Path

from workflow_pkg.cli_pkg.command_types import CommandBase


class InitCommand(CommandBase):
    """Scaffold the workflow directory structure."""

    def run(self, args: argparse.Namespace) -> int:
        """Execute the initialization."""

        print("Initializing workflow structure...")
        self._create_dirs()
        self._ensure_boards()
        print("Initialization complete.")
        return 0

    def _create_dirs(self) -> None:
        """Create necessary directory structure."""

        dirs = [
            "desk/tasks", "desk/pills", "desk/drawers", "desk/design",
            "modules/standardized", "modules/normed", "runs"
        ]
        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)
            print(f"  Created {d}/")

    def _ensure_boards(self) -> None:
        """Ensure initial Board.md files exist."""

        task_board = Path("desk/tasks/Board.md")
        if not task_board.exists():
            task_board.write_text("# Tasks Board\n\n## Active\n\n## Completed\n", encoding="utf-8")

        drawer_board = Path("desk/drawers/Board.md")
        if not drawer_board.exists():
            drawer_board.write_text("# Drawers Board\n\n## Deferred Items\n", encoding="utf-8")
