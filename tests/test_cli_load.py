from typer.testing import CliRunner
from repopackage.cli.core import app

runner = CliRunner()

def test_app_loads():
    """Test that the CLI app loads and shows help."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Repopackage CLI tool." in result.output

def test_system_category_loads():
    """Test that the system category is registered and shows help."""
    result = runner.invoke(app, ["system", "--help"])
    assert result.exit_code == 0
    assert "System management commands." in result.output
