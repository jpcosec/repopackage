from pathlib import Path
from typer.testing import CliRunner
from repopackage.cli.core import app

runner = CliRunner()

def test_init_project_creates_structure(tmp_path):
    """Test that the init-project command creates the expected directories and Board.md."""
    # Run the command in a temporary directory
    with runner.isolated_filesystem(temp_dir=tmp_path) as fs:
        result = runner.invoke(app, ["system", "init-project"])
        
        assert result.exit_code == 0
        assert "Project initialized successfully." in result.output
        
        # Check for created directories
        expected_dirs = [
            "desk/tasks",
            "desk/pills",
            "desk/design",
            "drawers",
            "modules",
            "runs"
        ]
        
        for d in expected_dirs:
            assert Path(d).is_dir(), f"Directory {d} should have been created."
            
        # Check for Board.md
        board_path = Path("desk/tasks/Board.md")
        assert board_path.is_file(), "Board.md should have been created."
        content = board_path.read_text()
        assert "# Tasks Board" in content
        assert "## Active (status=open|in_progress)" in content

def test_init_project_skips_existing_board(tmp_path):
    """Test that init-project doesn't overwrite an existing Board.md."""
    with runner.isolated_filesystem(temp_dir=tmp_path) as fs:
        # Create an existing Board.md
        board_dir = Path("desk/tasks")
        board_dir.mkdir(parents=True)
        board_file = board_dir / "Board.md"
        existing_content = "# Existing Content"
        board_file.write_text(existing_content)
        
        result = runner.invoke(app, ["system", "init-project"])
        
        assert result.exit_code == 0
        assert "Board.md already exists, skipping." in result.output
        assert board_file.read_text() == existing_content
