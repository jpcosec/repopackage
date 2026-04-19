import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from pathlib import Path
from repopackage.cli.core import app

runner = CliRunner()

TASK_CONTENT = """# T-99 - Mock Task

## Traits (Composición)
`[Impl]`

## Explanation
Mock explanation.

## Reference
- desk/tasks/T-01.md

## What to Fix / Implement
- Nothing.

## How to Do It (Suggested)
1. Just wait.

## Induced Changes
(Completar por Executor)

## Depends On
- None

## Priority
P2

---
**Status:** open
**Lifecycle:** target
**Commit SHA:**
"""

@patch("repopackage.cli.desk.commands.Workspace")
def test_inject_pill_success(mock_workspace_class):
    # Setup mock
    mock_workspace = MagicMock()
    mock_workspace_class.return_value = mock_workspace

    # Execute
    result = runner.invoke(app, ["desk", "pills", "inject", "--task", "T-99", "--pill", "PILL-99"])

    # Verify
    assert result.exit_code == 0
    assert "Successfully injected pill PILL-99 into task T-99" in result.output

    # Verify that inject was called with correct arguments
    mock_workspace.desk.pills.inject.assert_called_once_with("T-99", "PILL-99")

@patch("repopackage.cli.desk.commands.Workspace")
def test_inject_pill_task_not_found(mock_workspace_class):
    # Setup mock to raise FileNotFoundError
    mock_workspace = MagicMock()
    mock_workspace_class.return_value = mock_workspace
    mock_workspace.desk.pills.inject.side_effect = FileNotFoundError("Task file desk/tasks/T-NONEXISTENT.md not found.")

    # Execute
    result = runner.invoke(app, ["desk", "pills", "inject", "--task", "T-NONEXISTENT", "--pill", "PILL-01"])

    # Verify
    assert result.exit_code == 1
    assert "Error: Task file desk/tasks/T-NONEXISTENT.md not found." in result.output

@patch("repopackage.cli.desk.commands.Workspace")
def test_inject_pill_already_present(mock_workspace_class):
    # Setup mock - inject does nothing if pill already present (no-op)
    mock_workspace = MagicMock()
    mock_workspace_class.return_value = mock_workspace

    # Execute
    result = runner.invoke(app, ["desk", "pills", "inject", "--task", "T-99", "--pill", "PILL-99"])

    # Verify
    assert result.exit_code == 0
    assert "Successfully injected pill PILL-99 into task T-99" in result.output
