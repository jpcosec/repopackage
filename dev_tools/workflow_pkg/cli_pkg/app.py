"""CLI application builder."""
from __future__ import annotations
import argparse
from workflow_pkg.cli_pkg.config import CATEGORIES, DESCRIPTIONS


class CliApp:
    """Build and run the Workflow CLI."""

    def build(self) -> argparse.ArgumentParser:
        """Return the root parser."""
        p = argparse.ArgumentParser(prog="workflow", description="Workflow Management CLI.")
        s = p.add_subparsers(dest="command", required=True, metavar="AREA")
        for cat, cmds in CATEGORIES.items(): self._register_area(s, cat, cmds)
        return p

    def _register_area(self, subparsers, area_name, commands) -> None:
        """Register a workflow area and its commands."""
        h = DESCRIPTIONS.get(area_name, f"{area_name.capitalize()} management.")
        p_parser = subparsers.add_parser(area_name, help=h)
        p_sub = p_parser.add_subparsers(dest="subcommand", required=True, metavar="COMMAND")
        for name, cmd, hlp in commands:
            parser = p_sub.add_parser(name, help=hlp)
            cmd.configure(parser)
            parser.set_defaults(func=cmd.run)
