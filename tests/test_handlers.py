import pytest
from repopackage.cli.handlers import (
    handle_init, handle_resolve, handle_validate,
    handle_status, handle_generate, handle_graph,
)


def test_handle_init_creates_compose_yaml(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    handle_init()
    assert (tmp_path / "compose.yaml").exists()


def test_handle_init_yaml_has_project_kind(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    handle_init()
    assert "kind: project" in (tmp_path / "compose.yaml").read_text()


def test_handle_init_uses_cwd_as_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    handle_init()
    assert tmp_path.name in (tmp_path / "compose.yaml").read_text()


def test_handle_resolve_without_compose_exits(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit):
        handle_resolve()


def test_handle_validate_without_lockfile_exits(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit):
        handle_validate()


def test_handle_status_not_found_exits(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit):
        handle_status()


def test_handle_status_shows_package_states(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    
    # 1. Setup Lockfile
    lock_data = {
        "project": "test-project",
        "manifest_hash": "dummy-hash",
        "resolved_at": "2026-05-01T12:00:00",
        "packages": {
            "pkg-ok": {"name": "pkg-ok", "url": "u1", "branch": "b1", "commit": "aaaaaa11"},
            "pkg-missing": {"name": "pkg-missing", "url": "u2", "branch": "b2", "commit": "bbbbbb22"},
            "pkg-dirty": {"name": "pkg-dirty", "url": "u3", "branch": "b3", "commit": "cccccc33"},
        }
    }
    from ruamel.yaml import YAML
    yaml = YAML()
    with open("compose.lock.yaml", "w") as f:
        yaml.dump(lock_data, f)
        
    # 2. Setup Workspace
    ws = tmp_path / "workspace/packages"
    ws.mkdir(parents=True)
    (ws / "pkg-ok").mkdir()
    (ws / "pkg-dirty").mkdir()
    # pkg-missing remains missing
    
    # 3. Mock pygit2
    class MockRepo:
        def __init__(self, path):
            self.path = path
            class Head:
                def __init__(self, target): self.target = target
            if "pkg-ok" in str(path):
                self.head = Head("aaaaaa11abcdef")
            else:
                self.head = Head("diff-commit-xyz")
                
    import pygit2
    monkeypatch.setattr(pygit2, "Repository", MockRepo)
    
    # 4. Run
    handle_status()
    out = capsys.readouterr().out
    
    assert "pkg-ok" in out
    assert "aaaaaa11" in out
    assert "OK" in out
    
    assert "pkg-missing" in out
    assert "MISSING" in out
    
    assert "pkg-dirty" in out
    assert "DIRTY/DIFF" in out


def test_handle_generate_scans_workspace(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # Create empty workspace to avoid error
    (tmp_path / "workspace/packages").mkdir(parents=True)
    handle_generate()
    out = capsys.readouterr().out
    assert "scanning workspace" in out.lower()
    assert "coming soon" not in out.lower()


def test_handle_graph_not_found_exits(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit):
        handle_graph()
