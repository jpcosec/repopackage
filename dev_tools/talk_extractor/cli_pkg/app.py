"""CLI application builder."""

from __future__ import annotations

import argparse
from talk_extractor.cli_pkg.agent_prompt_command import AgentPromptCommand
from talk_extractor.cli_pkg.extract_artifacts_command import ExtractArtifactsCommand
from talk_extractor.cli_pkg.extract_turns_command import ExtractTurnsCommand
from talk_extractor.cli_pkg.lint_constraints_command import LintConstraintsCommand
from talk_extractor.cli_pkg.prepare_semantic_command import PrepareSemanticCommand
from talk_extractor.cli_pkg.run_semantic_command import RunSemanticCommand
from talk_extractor.cli_pkg.standardize_command import StandardizeCreateCommand
from talk_extractor.cli_pkg.drawers_add_command import DrawersAddCommand
from talk_extractor.cli_pkg.drawers_list_command import DrawersListCommand
from talk_extractor.cli_pkg.drawers_promote_command import DrawersPromoteCommand
from talk_extractor.cli_pkg.drawers_audit_command import DrawersAuditCommand
from talk_extractor.cli_pkg.desk_tasks_command import DeskTasksCommand
from talk_extractor.cli_pkg.desk_pills_command import DeskPillsCommand
from talk_extractor.cli_pkg.desk_board_command import DeskBoardCommand


CATEGORIES = {
    "extract": [
        ("turns", ExtractTurnsCommand(), "Extract turns.", ["extract-turns"]),
        ("artifacts", ExtractArtifactsCommand(), "Extract artifacts.", ["extract-artifacts"]),
        ("prepare", PrepareSemanticCommand(), "Prepare semantic.", ["prepare-semantic"]),
        ("run", RunSemanticCommand(), "Run semantic.", ["run-semantic"]),
        ("prompt", AgentPromptCommand(), "Agent prompt.", ["agent-prompt"]),
        ("lint-constraints", LintConstraintsCommand(), "Lint constraints.", ["lint-constraints"]),
    ],
    "standardize": [("create", StandardizeCreateCommand(), "Create module.", [])],
    "drawers": [
        ("add", DrawersAddCommand(), "Add spec.", []),
        ("list", DrawersListCommand(), "List specs.", []),
        ("promote", DrawersPromoteCommand(), "Promote spec.", []),
        ("audit", DrawersAuditCommand(), "Audit specs.", []),
    ],
    "desk": [
        ("tasks", DeskTasksCommand(), "Tasks.", []),
        ("pills", DeskPillsCommand(), "Pills.", []),
        ("board", DeskBoardCommand(), "Board.", []),
    ],
    "exec": [], "capture": [], "eval": [], "integrate": [],
}
class CliApp:
    """Build and run the talk_extractor CLI."""

    def build(self) -> argparse.ArgumentParser:
        """Return the root parser."""

        parser = self._root_parser()
        self._register_all(parser.add_subparsers(dest="command", required=True))
        return parser

    def _root_parser(self) -> argparse.ArgumentParser:
        """Build the root parser."""

        return argparse.ArgumentParser(prog="talk-extractor", description="Central CLI for talk_extractor.")

    def _register_all(self, subparsers) -> None:
        """Register all configured categories and commands."""
        for cat, cmds in CATEGORIES.items(): self._register_category(subparsers, cat, cmds)

    def _register_category(self, subparsers, category, commands) -> None:
        """Register a category and its commands."""
        cat_parser = subparsers.add_parser(category, help=f"{category.capitalize()} commands.")
        cat_subparsers = cat_parser.add_subparsers(dest="subcommand", required=True)
        for name, command, help_text, aliases in commands:
            self._register(cat_subparsers, name, command, help_text)
            for alias in aliases: self._register(subparsers, alias, command, help_text)
    def _register(self, subparsers, name: str, command, help_text: str) -> None:
        """Register one subcommand."""

        parser = subparsers.add_parser(name, help=help_text)
        command.configure(parser)
        parser.set_defaults(func=command.run)
