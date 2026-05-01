import pytest
from pathlib import Path
from ruamel.yaml import YAML
from repopackage.cli.handlers import handle_validate
from repopackage.core import constants

yaml = YAML()

@pytest.fixture
def mock_repo(monkeypatch):
    class MockRepo:
        def __init__(self, path):
            self.path = path
            class Head:
                def __init__(self, target): self.target = target
            
            # Map paths to expected commits for tests
            if "pkg-ok" in str(path):
                self.head = Head("aaaaaa11abcdef")
            elif "pkg-mismatch" in str(path):
                self.head = Head("wrong-commit-sha")
            else:
                self.head = Head("some-other-sha")
                
    import pygit2
    monkeypatch.setattr(pygit2, "Repository", MockRepo)
    return MockRepo

def test_handle_validate_fails_on_commit_mismatch(tmp_path, monkeypatch, mock_repo, capsys):
    monkeypatch.chdir(tmp_path)
    
    # 1. Setup Lockfile
    lock_data = {
        "project": "test-project",
        "manifest_hash": "h1",
        "resolved_at": "2026-05-01T12:00:00",
        "packages": {
            "pkg-mismatch": {"name": "pkg-mismatch", "url": "u1", "branch": "b1", "commit": "aaaaaa11"},
        }
    }
    with open(constants.LOCK_FILE, "w") as f:
        yaml.dump(lock_data, f)
        
    # 2. Setup Workspace
    ws = tmp_path / constants.WORKSPACE_DIR / "packages"
    pkg_dir = ws / "pkg-mismatch"
    pkg_dir.mkdir(parents=True)
    
    # Create contract to pass that check
    contract_dir = pkg_dir / "contracts"
    contract_dir.mkdir()
    with open(contract_dir / "integration.contract.yaml", "w") as f:
        yaml.dump({"name": "pkg-mismatch", "version": "1.0.0"}, f)
    
    # 3. Run - Should fail because of commit mismatch
    with pytest.raises(SystemExit) as e:
        handle_validate()
    
    assert e.value.code == 1
    out = capsys.readouterr().out
    assert "Validation failed" in out
    assert "pkg-mismatch commit mismatch" in out.lower()

def test_handle_validate_fails_on_missing_contract(tmp_path, monkeypatch, mock_repo, capsys):
    monkeypatch.chdir(tmp_path)
    
    lock_data = {
        "project": "test-project",
        "manifest_hash": "h1",
        "resolved_at": "2026-05-01T12:00:00",
        "packages": {
            "pkg-no-contract": {"name": "pkg-no-contract", "url": "u1", "branch": "b1", "commit": "aaaaaa11"},
        }
    }
    with open(constants.LOCK_FILE, "w") as f:
        yaml.dump(lock_data, f)
        
    ws = tmp_path / constants.WORKSPACE_DIR / "packages"
    (ws / "pkg-no-contract").mkdir(parents=True)
    
    # Mock pygit2 to return correct commit
    monkeypatch.setattr("pygit2.Repository", lambda p: type('obj', (object,), {'head': type('obj', (object,), {'target': 'aaaaaa11'})}))

    with pytest.raises(SystemExit) as e:
        handle_validate()
    
    assert e.value.code == 1
    out = capsys.readouterr().out
    assert "missing contracts/integration.contract.yaml" in out.lower()

def test_handle_validate_passes_when_all_good(tmp_path, monkeypatch, mock_repo, capsys):
    monkeypatch.chdir(tmp_path)
    
    lock_data = {
        "project": "test-project",
        "manifest_hash": "h1",
        "resolved_at": "2026-05-01T12:00:00",
        "packages": {
            "pkg-ok": {"name": "pkg-ok", "url": "u1", "branch": "b1", "commit": "aaaaaa11"},
        }
    }
    with open(constants.LOCK_FILE, "w") as f:
        yaml.dump(lock_data, f)
        
    ws = tmp_path / constants.WORKSPACE_DIR / "packages"
    pkg_dir = ws / "pkg-ok"
    pkg_dir.mkdir(parents=True)
    
    # Create contract
    contract_dir = pkg_dir / "contracts"
    contract_dir.mkdir()
    with open(contract_dir / "integration.contract.yaml", "w") as f:
        yaml.dump({"name": "pkg-ok", "version": "1.0.0", "exports": []}, f)
    
    handle_validate()
    out = capsys.readouterr().out
    assert "Validation passed" in out
