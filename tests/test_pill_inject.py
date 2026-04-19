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

@patch("repopackage.cli.desk.commands.Path")
def test_inject_pill_success(mock_path):
    # Setup mock
    mock_file = MagicMock()
    mock_file.exists.return_value = True
    mock_file.read_text.return_value = TASK_CONTENT
    mock_path.return_value = mock_file
    
    # Execute
    result = runner.invoke(app, ["desk", "pills", "inject", "--task", "T-99", "--pill", "PILL-99"])
    
    # Verify
    assert result.exit_code == 0
    assert "Successfully injected pill PILL-99 into task T-99" in result.output
    
    # Check that write_text was called with updated content
    called_content = mock_file.write_text.call_args[0][0]
    assert "`[Impl] | [PILL-99]`" in called_content
    assert "- desk/pills/PILL-99.md" in called_content
    assert "- Injected pill PILL-99" in called_content
    assert "(Completar por Executor)" not in called_content

@patch("repopackage.cli.desk.commands.Path")
def test_inject_pill_task_not_found(mock_path):
    # Setup mock
    mock_file = MagicMock()
    mock_file.exists.return_value = False
    mock_path.return_value = mock_file
    
    # Execute
    result = runner.invoke(app, ["desk", "pills", "inject", "--task", "T-NONEXISTENT", "--pill", "PILL-01"])
    
    # Verify
    assert result.exit_code == 1
    assert "Error: Task file desk/tasks/T-NONEXISTENT.md not found." in result.output

@patch("repopackage.cli.desk.commands.Path")
def test_inject_pill_already_present(mock_path):
    # Setup mock
    mock_file = MagicMock()
    mock_file.exists.return_value = True
    # Pill already in Reference
    content_with_pill = TASK_CONTENT.replace("- desk/tasks/T-01.md", "- desk/tasks/T-01.md\n- desk/pills/PILL-99.md")
    mock_file.read_text.return_value = content_with_pill
    mock_path.return_value = mock_file
    
    # Execute
    result = runner.invoke(app, ["desk", "pills", "inject", "--task", "T-99", "--pill", "PILL-99"])
    
    # Verify
    assert result.exit_code == 0
    assert "Pill PILL-99 is already in task T-99." in result.output
    # write_text should NOT have been called
    mock_file.write_text.assert_not_called()
