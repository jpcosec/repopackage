"""CLI application builder."""

from __future__ import annotations

import argparse

from workflow_pkg.cli_pkg.agent_prompt_command import AgentPromptCommand
from workflow_pkg.cli_pkg.extract_artifacts_command import ExtractArtifactsCommand
from workflow_pkg.cli_pkg.extract_turns_command import ExtractTurnsCommand
from workflow_pkg.cli_pkg.lint_constraints_command import LintConstraintsCommand
from workflow_pkg.cli_pkg.prepare_semantic_command import PrepareSemanticCommand
from workflow_pkg.cli_pkg.run_semantic_command import RunSemanticCommand
from workflow_pkg.cli_pkg.standardize_command import StandardizeCreateCommand
from workflow_pkg.cli_pkg.drawers_add_command import DrawersAddCommand
from workflow_pkg.cli_pkg.drawers_list_command import DrawersListCommand
from workflow_pkg.cli_pkg.drawers_promote_command import DrawersPromoteCommand
from workflow_pkg.cli_pkg.drawers_audit_command import DrawersAuditCommand
from workflow_pkg.cli_pkg.desk_tasks_command import DeskTasksCommand
from workflow_pkg.cli_pkg.desk_pills_command import DeskPillsCommand
from workflow_pkg.cli_pkg.desk_board_command import DeskBoardCommand
from workflow_pkg.cli_pkg.exec_run_command import ExecRunCommand
from workflow_pkg.cli_pkg.exec_dispatch_command import ExecDispatchCommand
from workflow_pkg.cli_pkg.capture_rescue_command import CaptureRescueCommand
from workflow_pkg.cli_pkg.capture_normalize_command import CaptureNormalizeCommand
from workflow_pkg.cli_pkg.eval_test_command import EvalTestCommand
from workflow_pkg.cli_pkg.eval_lint_command import EvalLintCommand
from workflow_pkg.cli_pkg.eval_audit_command import EvalAuditCommand
from workflow_pkg.cli_pkg.integrate_merge_command import IntegrateMergeCommand
from workflow_pkg.cli_pkg.integrate_rollback_command import IntegrateRollbackCommand
from workflow_pkg.cli_pkg.integrate_promote_command import IntegratePromoteCommand
from workflow_pkg.cli_pkg.init_command import InitCommand

CATEGORIES = {
    "system": [("initialize", InitCommand(), "Scaffold.", ["init"])],
    "distill": [("turns", ExtractTurnsCommand(), "Turns.", ["extract-turns"]), ("artifacts", ExtractArtifactsCommand(), "Artifacts.", ["extract-artifacts"]), ("prepare", PrepareSemanticCommand(), "Prep.", ["prepare-semantic"]), ("run", RunSemanticCommand(), "Run.", ["run-semantic"]), ("prompt", AgentPromptCommand(), "Prompt.", ["agent-prompt"])],
    "standardize": [("create", StandardizeCreateCommand(), "Create.", [])],
    "drawers": [("add", DrawersAddCommand(), "Add.", []), ("list", DrawersListCommand(), "List.", []), ("promote", DrawersPromoteCommand(), "Promote.", []), ("audit", DrawersAuditCommand(), "Audit.", [])],
    "desk": [("tasks", DeskTasksCommand(), "Tasks.", []), ("pills", DeskPillsCommand(), "Pills.", []), ("board", DeskBoardCommand(), "Board.", [])],
    "exec": [("run", ExecRunCommand(), "Run.", []), ("dispatch", ExecDispatchCommand(), "Dispatch.", [])],
    "capture": [("rescue", CaptureRescueCommand(), "Rescue.", []), ("normalize", CaptureNormalizeCommand(), "Normalize.", [])],
    "eval": [("test", EvalTestCommand(), "Test.", []), ("lint", EvalLintCommand(), "Lint.", []), ("audit", EvalAuditCommand(), "Audit.", []), ("constraints", LintConstraintsCommand(), "Constraints.", ["lint-constraints"])],
    "integrate": [("merge", IntegrateMergeCommand(), "Merge.", []), ("rollback", IntegrateRollbackCommand(), "Rollback.", []), ("promote", IntegratePromoteCommand(), "Promote.", [])],
}

class CliApp:
    """Build and run the workflow_pkg CLI."""

    def build(self) -> argparse.ArgumentParser:
        """Return the root parser."""
        parser = self._root_parser()
        self._register_all(parser.add_subparsers(dest="command", required=True))
        return parser

    def _root_parser(self) -> argparse.ArgumentParser:
        """Build the root parser."""
        return argparse.ArgumentParser(prog="workflow", description="Central CLI for Workflow.")

    def _register_all(self, subparsers) -> None:
        """Register all configured categories and commands."""
        for cat, cmds in CATEGORIES.items(): self._register_category(subparsers, cat, cmds)

    def _register_category(self, subparsers, category, commands) -> None:
        """Register a category and its commands."""
        cat_parser = subparsers.add_parser(category, help=f"{category.capitalize()} commands.")
        cat_subparsers = cat_parser.add_subparsers(dest="subcommand", required=True)
        for name, cmd, hlp, als in commands:
            self._register(cat_subparsers, name, cmd, hlp)
            for alias in als: self._register(subparsers, alias, cmd, hlp)

    def _register(self, subparsers, name: str, command, help_text: str) -> None:
        """Register one subcommand."""
        parser = subparsers.add_parser(name, help=help_text)
        command.configure(parser)
        parser.set_defaults(func=command.run)
