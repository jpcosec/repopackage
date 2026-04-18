"""Exec dispatch command."""

from __future__ import annotations

import argparse
from talk_extractor.cli_pkg.command_types import CommandBase


class ExecDispatchCommand(CommandBase):
    """Dispatch multiple tasks for execution."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure the command arguments."""
        # No specific arguments for the stub yet

    def run(self, args: argparse.Namespace) -> int:
        """Run the command stub."""

        print("Dispatching multiple tasks...")
        # Stub for multiple tasks
        return 0
