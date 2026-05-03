from repopackage.cli import handlers
from unittest.mock import patch, MagicMock
from pathlib import Path

import pytest

def test_handle_exports_no_lockfile(tmp_path, capsys):
    with patch("repopackage.cli.handlers.constants.LOCK_FILE", str(tmp_path / "missing.lock")):
        with pytest.raises(SystemExit):
            handlers.handle_exports()
        out = capsys.readouterr().out
        assert "not found" in out

def test_handle_exports_with_mock_data(tmp_path, capsys):
    lock_file = tmp_path / "compose.lock.yaml"
    lock_file.write_text("""
version: '1.0'
project: test-project
manifest_hash: 'hash'
resolved_at: '2026-05-01'
packages:
  pkg-a:
    name: pkg-a
    url: /tmp/a
    branch: master
    commit: abc123
""", encoding="utf-8")
    
    ws = tmp_path / "workspace" / "packages" / "pkg-a"
    ws.mkdir(parents=True)
    
    contract = ws / "contracts" / "integration.contract.yaml"
    contract.parent.mkdir()
    contract.write_text("""
name: pkg-a
version: 0.1.0
export_surface:
  commands:
    cmd1:
      name: cmd1
      description: "First command"
      entrypoint: "pkg.a:main"
""", encoding="utf-8")
    
    with patch("repopackage.cli.handlers.constants.LOCK_FILE", str(lock_file)), \
         patch("repopackage.cli.handlers.constants.WORKSPACE_DIR", str(tmp_path / "workspace")):
        handlers.handle_exports()
        
    out = capsys.readouterr().out
    assert "Ecosystem Export Surface" in out
    assert "Package: pkg-a" in out
    assert "cmd1: First command" in out
