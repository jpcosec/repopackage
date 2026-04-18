"""Shared CLI command protocol."""

from __future__ import annotations

import argparse


class CommandBase:
    """Small command interface for the CLI."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Register arguments on a subparser."""

    def run(self, args: argparse.Namespace) -> int:
        """Execute the command."""

        return 0
