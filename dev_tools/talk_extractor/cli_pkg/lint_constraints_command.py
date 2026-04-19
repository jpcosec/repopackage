"""Lint-constraints CLI command."""

from __future__ import annotations

import argparse

from talk_extractor.cli_pkg.command_types import CommandBase
from talk_extractor.lint_constraints import main as lint_main


class LintConstraintsCommand(CommandBase):
    """Run the local structural constraint linter."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure command arguments."""

        return None

    def run(self, _args: argparse.Namespace) -> int:
        """Run the command."""

        return lint_main()
