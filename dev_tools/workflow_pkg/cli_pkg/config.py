"""CLI command and category configuration."""
from __future__ import annotations
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
    "system": [("setup-project", InitCommand(), "Scaffold project structure.")],
    "distill": [
        ("extract-turns", ExtractTurnsCommand(), "Split transcripts into turns."),
        ("extract-artifacts", ExtractArtifactsCommand(), "Extract diagrams/code."),
        ("scaffold-workspace", PrepareSemanticCommand(), "Prepare semantic shells."),
        ("agent-prompt", RunSemanticCommand(), "Generate next agent prompt."),
        ("show-entrypoints", AgentPromptCommand(), "List available entrypoints.")
    ],
    "standardize": [("scaffold-module", StandardizeCreateCommand(), "Create reusable modules.")],
    "drawers": [
        ("defer-spec", DrawersAddCommand(), "Move spec to backlog."),
        ("list-backlog", DrawersListCommand(), "View deferred specs."),
        ("promote-spec", DrawersPromoteCommand(), "Convert spec to task."),
        ("check-health", DrawersAuditCommand(), "Verify backlog maturity.")
    ],
    "desk": [
        ("split-tasks", DeskTasksCommand(), "Atomize work units."),
        ("bind-context", DeskPillsCommand(), "Attach pills to tasks."),
        ("sync-board", DeskBoardCommand(), "Refresh task board.")
    ],
    "exec": [
        ("execute-task", ExecRunCommand(), "Dispatch agent to task."),
        ("batch-dispatch", ExecDispatchCommand(), "Run parallel batch.")
    ],
    "capture": [
        ("rescue-logs", CaptureRescueCommand(), "Pull execution traces."),
        ("normalize-trace", CaptureNormalizeCommand(), "Convert logs to evidence.")
    ],
    "eval": [
        ("test-suite", EvalTestCommand(), "Run project tests."),
        ("lint-code", EvalLintCommand(), "Run style linters."),
        ("audit-laws", LintConstraintsCommand(), "Verify 'Laws of Physics'."),
        ("full-gate", EvalAuditCommand(), "Run quality gate.")
    ],
    "integrate": [
        ("merge-work", IntegrateMergeCommand(), "Merge verified work."),
        ("revert-change", IntegrateRollbackCommand(), "Revert integration."),
        ("promote-artifacts", IntegratePromoteCommand(), "Push to production.")
    ],
}
DESCRIPTIONS = {
    "system": "Project Lifecycle: Core environment management.",
    "distill": "Design Distillation: Transform material into specs.",
    "standardize": "Standardization: Define reusable patterns.",
    "drawers": "Backlog (Drawers): Manage deferred work.",
    "desk": "Active Desk: Orchestrate tasks and context.",
    "exec": "Execution: Run AI agents and batches.",
    "capture": "Trace Ingestion: Process agent run logs.",
    "eval": "Quality Control: Automated verification.",
    "integrate": "Integration: Final merging and promotion."
}
