import pytest
from pathlib import Path
import shutil
import os
from repopackage.cli.engines.markdown_engine import MarkdownEngine
from repopackage.cli.desk.commands import atomize_task
from typer.testing import CliRunner
from repopackage.cli.core import app

runner = CliRunner()

def test_extract_checklist_numbered():
    content = "## Section\n1. Item 1\n2. Item 2"
    engine = MarkdownEngine(content)
    items = engine.extract_checklist("Section")
    assert items == ["Item 1", "Item 2"]

def test_extract_checklist_bullet():
    content = "## Section\n- Item A\n* Item B"
    engine = MarkdownEngine(content)
    items = engine.extract_checklist("Section")
    assert items == ["Item A", "Item B"]

def test_atomize_command_logic(tmp_path):
    # Setup mock project structure
    os.chdir(tmp_path)
    (tmp_path / "desk/tasks").mkdir(parents=True)
    (tmp_path / "desk/pills").mkdir(parents=True)
    (tmp_path / "workflow/docs/template").mkdir(parents=True)
    
    task_file = tmp_path / "desk/tasks/T-99.md"
    task_file.write_text("""# T-99 - Test Task
## Reference
- `old/ref.md`
## How to Do It (Suggested)
1. Task 1
2. Task 2
""")
    
    template_file = tmp_path / "workflow/docs/template/context_pills.md"
    template_file.write_text("# PILL-XX - {title}\n- **ID:** PILL-XX")
    
    # Run command
    result = runner.invoke(app, ["desk", "tasks", "atomize", "T-99"])
    
    assert result.exit_code == 0
    assert "Created pill: PILL-01" in result.output
    assert "Created pill: PILL-02" in result.output
    
    # Check pills created
    assert (tmp_path / "desk/pills/PILL-01.md").exists()
    assert (tmp_path / "desk/pills/PILL-02.md").exists()
    
    p1_content = (tmp_path / "desk/pills/PILL-01.md").read_text()
    assert "# PILL-01 - Task 1" in p1_content
    assert "- ID: PILL-01" in p1_content
    
    # Check task updated
    task_content = task_file.read_text()
    assert "1. [PILL-01] - Task 1" in task_content
    assert "- `desk/pills/PILL-01.md`" in task_content
