"""CLI application builder."""

from __future__ import annotations

import argparse

from talk_extractor.cli_pkg.agent_prompt_command import AgentPromptCommand
from talk_extractor.cli_pkg.extract_artifacts_command import ExtractArtifactsCommand
from talk_extractor.cli_pkg.extract_turns_command import ExtractTurnsCommand
from talk_extractor.cli_pkg.lint_constraints_command import LintConstraintsCommand
from talk_extractor.cli_pkg.prepare_semantic_command import PrepareSemanticCommand
from talk_extractor.cli_pkg.run_semantic_command import RunSemanticCommand


COMMANDS = [
    ("extract-turns", ExtractTurnsCommand(), "Extract conversation turns."),
    ("extract-artifacts", ExtractArtifactsCommand(), "Extract structured artifacts."),
    ("prepare-semantic", PrepareSemanticCommand(), "Prepare semantic scaffolding."),
    ("run-semantic", RunSemanticCommand(), "Prepare semantic scaffolding and next prompt."),
    ("agent-prompt", AgentPromptCommand(), "Show semantic agent entrypoints."),
    ("lint-constraints", LintConstraintsCommand(), "Lint local structural constraints."),
]

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
        """Register all configured commands."""

        for name, command, help_text in COMMANDS:
            self._register(subparsers, name, command, help_text)

    def _register(self, subparsers, name: str, command, help_text: str) -> None:
        """Register one subcommand."""

        parser = subparsers.add_parser(name, help=help_text)
        command.configure(parser)
        parser.set_defaults(func=command.run)
