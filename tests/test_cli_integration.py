import subprocess
import pytest
import shutil

def test_cli_help():
    """Verify that 'rp --help' works when the package is installed."""
    result = subprocess.run(["rp", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Repopackage" in result.stdout
    assert "commands" in result.stdout

def test_cli_init_integration(tmp_path):
    """Verify 'rp init' creates files in a real-world subprocess call."""
    # We use rp as a command, assuming it is installed in the environment
    # or accessible via the entry point.
    result = subprocess.run(["rp", "init"], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0
    assert (tmp_path / "compose.yaml").exists()
    assert "kind: project" in (tmp_path / "compose.yaml").read_text()

def test_cli_alias_integration():
    """Verify that 'repopackage' alias also works."""
    result = subprocess.run(["repopackage", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Repopackage" in result.stdout
