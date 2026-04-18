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
    "system": [("init", InitCommand(), "Setup project structure.", [])],
    "distill": [("turns", ExtractTurnsCommand(), "Extract turns.", ["extract-turns"]), ("artifacts", ExtractArtifactsCommand(), "Extract artifacts.", ["extract-artifacts"]), ("prepare", PrepareSemanticCommand(), "Setup shells.", ["prepare-semantic"]), ("run", RunSemanticCommand(), "Next prompt.", ["run-semantic"]), ("prompt", AgentPromptCommand(), "Show entrypoints.", ["agent-prompt"])],
    "standardize": [("create", StandardizeCreateCommand(), "Scaffold modules.", [])],
    "drawers": [("add", DrawersAddCommand(), "Defer spec.", []), ("list", DrawersListCommand(), "List deferred.", []), ("promote", DrawersPromoteCommand(), "Promote spec.", []), ("audit", DrawersAuditCommand(), "Check health.", [])],
    "desk": [("tasks", DeskTasksCommand(), "Manage tasks.", []), ("pills", DeskPillsCommand(), "Manage pills.", []), ("board", DeskBoardCommand(), "Sync board.", [])],
    "exec": [("run", ExecRunCommand(), "Run agent.", []), ("dispatch", ExecDispatchCommand(), "Batch tasks.", [])],
    "capture": [("rescue", CaptureRescueCommand(), "Pull logs.", []), ("normalize", CaptureNormalizeCommand(), "Convert evidence.", [])],
    "eval": [("test", EvalTestCommand(), "Run tests.", []), ("lint", EvalLintCommand(), "Run linters.", []), ("audit", EvalAuditCommand(), "Quality gate.", []), ("constraints", LintConstraintsCommand(), "Check rules.", ["lint-constraints"])],
    "integrate": [("merge", IntegrateMergeCommand(), "Merge work.", []), ("rollback", IntegrateRollbackCommand(), "Revert.", []), ("promote", IntegratePromoteCommand(), "Push prod.", [])],
}

class CliApp:
    """Build and run the workflow_pkg CLI."""

    def build(self) -> argparse.ArgumentParser:
        """Return the root parser."""
        p = argparse.ArgumentParser(prog="workflow", description="Workflow Management CLI.")
        s = p.add_subparsers(dest="command", required=True, metavar="PHASE")
        for cat, cmds in CATEGORIES.items(): self._register_phase(s, cat, cmds)
        return p

    def _register_phase(self, subparsers, phase_name, commands) -> None:
        """Register a phase and its commands."""
        p_help = f"{phase_name.capitalize()} lifecycle phase."
        p_parser = subparsers.add_parser(phase_name, help=p_help)
        p_sub = p_parser.add_subparsers(dest="subcommand", required=True, metavar="COMMAND")
        for name, cmd, hlp, als in commands:
            self._register(p_sub, name, cmd, hlp)
            for alias in als:
                self._register(subparsers, alias, cmd, argparse.SUPPRESS)

    def _register(self, sub, name: str, command, help_text: str | None) -> None:
        """Register one subcommand."""
        parser = sub.add_parser(name, help=help_text)
        command.configure(parser)
        parser.set_defaults(func=command.run)
