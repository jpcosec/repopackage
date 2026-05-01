import pytest
import pygit2
from unittest.mock import MagicMock

_SIG = pygit2.Signature("Test", "t@test.com")


def _init(path):
    path.mkdir(parents=True, exist_ok=True)
    return pygit2.init_repository(str(path))


def _commit(repo, tree_id):
    repo.create_commit("refs/heads/master", _SIG, _SIG, "init", tree_id, [])


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
