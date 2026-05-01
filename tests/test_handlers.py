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
