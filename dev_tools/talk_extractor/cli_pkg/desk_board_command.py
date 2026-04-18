"""Desk Board CLI command."""

from __future__ import annotations

import argparse
from pathlib import Path

from talk_extractor.cli_pkg.command_types import CommandBase
from talk_extractor.cli_pkg.desk_board_service import TaskBoard
from talk_extractor.cli_pkg.board_writer import BoardWriter


class DeskBoardCommand(CommandBase):
    """Manage the task board on the desk."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Register arguments on a subparser."""
        sub = parser.add_subparsers(dest="desk_board_command", required=True)
        sub.add_parser("sync", help="Synchronize task board.")
        sub.add_parser("status", help="Show current board status.")

    def run(self, args: argparse.Namespace) -> int:
        """Execute the board command."""
        board = TaskBoard()
        tasks = board.load_tasks()
        if args.desk_board_command == "sync": self._sync(tasks)
        if args.desk_board_command == "status": self._status(tasks)
        return 0

    def _sync(self, tasks: list[dict]) -> None:
        """Regenerate Board.md from tasks."""
        writer = BoardWriter()
        content = writer.build(tasks)
        Path("desk/tasks/Board.md").write_text(content, encoding="utf-8")
        print("Board synchronized.")

    def _status(self, tasks: list[dict]) -> None:
        """Show active tasks status."""
        active = [t for t in tasks if t["Status"] in ("open", "in_progress")]
        print(f"Active tasks: {len(active)}")
        for t in active: print(f"- {t['ID']}: {t['Title']} ({t['Priority']})")
