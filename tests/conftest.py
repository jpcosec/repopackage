import sys
from pathlib import Path

import pytest
import pygit2
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

_SIG = pygit2.Signature("Test", "t@test.com")


def _init(path):
    path.mkdir(parents=True, exist_ok=True)
    return pygit2.init_repository(str(path))


def _commit(repo, tree_id, message="init", ref="refs/heads/master"):
    repo.create_commit(ref, _SIG, _SIG, message, tree_id, [])


def _create_contract(repo, name, version="1.0.0"):
    content = f"name: {name}\nversion: {version}\nexports: []\nconsumes: []".encode()
    bid = repo.create_blob(content)
    inner = repo.TreeBuilder()
    inner.insert("integration.contract.yaml", bid, pygit2.GIT_FILEMODE_BLOB)
    outer = repo.TreeBuilder()
    outer.insert("contracts", inner.write(), pygit2.GIT_FILEMODE_TREE)
    return outer.write()


@pytest.fixture
def ecosystem_delivery_fixture(tmp_path):
    """
    Sets up a realistic multi-repo environment:
    - ui-kit (central line, master)
    - diagnostics (has master and feat/new-check)
    """
    remotes = tmp_path / "remotes"
    remotes.mkdir()

    # 1. UI KIT (Central)
    ui_path = remotes / "ui-kit"
    ui_repo = _init(ui_path)
    ui_tree = _create_contract(ui_repo, "ui-kit")
    _commit(ui_repo, ui_tree)

    # 2. DIAGNOSTICS
    diag_path = remotes / "diagnostics"
    diag_repo = _init(diag_path)

    # Master branch
    diag_tree_master = _create_contract(diag_repo, "diagnostics", version="1.0.0")
    _commit(diag_repo, diag_tree_master)

    # Contextual branch: feat/new-check
    # We need a different tree or just a different commit
    diag_tree_feat = _create_contract(diag_repo, "diagnostics", version="1.1.0-alpha")
    diag_repo.create_commit(
        "refs/heads/feat/new-check",
        _SIG,
        _SIG,
        "add new check",
        diag_tree_feat,
        [diag_repo.head.target],
    )

    return {
        "root": tmp_path,
        "ui-kit": ui_path,
        "diagnostics": diag_path,
    }


@pytest.fixture
def flat_repo(tmp_path):
    """Repo with a single root-level file: README.md → 'hello'."""
    p = tmp_path / "repo"
    repo = _init(p)
    bid = repo.create_blob(b"hello")
    root = repo.TreeBuilder()
    root.insert("README.md", bid, pygit2.GIT_FILEMODE_BLOB)
    _commit(repo, root.write())
    return repo, p


@pytest.fixture
def contract_repo(tmp_path):
    """Repo with contracts/integration.contract.yaml nested one level deep."""
    p = tmp_path / "repo"
    repo = _init(p)
    content = b"name: pkg\nversion: 1.0.0\nexports: []\nconsumes: []"
    bid = repo.create_blob(content)
    inner = repo.TreeBuilder()
    inner.insert("integration.contract.yaml", bid, pygit2.GIT_FILEMODE_BLOB)
    outer = repo.TreeBuilder()
    outer.insert("contracts", inner.write(), pygit2.GIT_FILEMODE_TREE)
    _commit(repo, outer.write())
    commit = str(repo.head.target)
    return repo, p, commit


@pytest.fixture
def mock_git():
    m = MagicMock()
    m.get_commit_hash.return_value = "abc123"
    # Return a valid minimal contract by default
    m.read_file.return_value = "name: pkg\nversion: 1.0.0\nexports: []\nconsumes: []"
    return m
