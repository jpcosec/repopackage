import pytest
from pathlib import Path
from textwrap import dedent
from repopackage.workflow.workspace import Workspace
from repopackage.workflow.desk import Desk

@pytest.fixture
def workspace(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    (root / "desk").mkdir()
    (root / "desk" / "tasks").mkdir()
    (root / "desk" / "pills").mkdir()
    return Workspace(root)

def test_inject_pill(workspace):
    desk = Desk(workspace)
    
    # Create a dummy task file
    task_content = dedent("""
        # T-01 - Test Task

        ## Traits (Composición)
        - none

        ## Explanation
        Test explanation.

        ## Reference
        - `none`

        ## What to Fix / Implement
        Fix something.

        ## How to Do It (Suggested)
        - Step 1

        ## Induced Changes
        ⸢revop•induced_changes⸥

        ## Depends On
        - none

        ## Priority
        P2

        ---
        open
        target
        
    """).strip()
    task_file = workspace.tasks_path / "T-01.md"
    task_file.write_text(task_content)
    
    # Create a dummy pill file
    pill_content = dedent("""
        # Test Pill
        (ID: PILL-01)

        ## Metadata
        ```yaml
        id: PILL-01
        type: logic
        scope: component
        language: Python
        nature: implementation
        ```

        ## Why
        Reason.

        ## What
        Description.

        ## When
        Now.

        ## Where
        Here.

        ## How
        Method.

        ---
        Keep
    """).strip()
    pill_file = workspace.pills_path / "PILL-01.md"
    pill_file.write_text(pill_content)
    
    # Test Injection
    desk.ops.inject_pill("T-01", "PILL-01")
    
    # Reload and verify
    updated_task = desk.tasks.get_task("T-01")
    assert "PILL-01" in updated_task.traits
    assert "desk/pills/PILL-01.md" in updated_task.reference
    
    # Verify rendered file
    rendered_text = task_file.read_text()
    assert "PILL-01" in rendered_text
    assert "desk/pills/PILL-01.md" in rendered_text
