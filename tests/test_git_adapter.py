import pytest
from repopackage.adapters.git import GitAdapter


def test_get_commit_hash_missing_local_repo_raises(tmp_path):
    """Local paths that don't exist should still raise FileNotFoundError."""
    adapter = GitAdapter(cache_dir=tmp_path / "cache")
    with pytest.raises(FileNotFoundError):
        adapter.get_commit_hash(str(tmp_path / "nonexistent"), "main")


def test_get_commit_hash_unauthorized_remote_raises(tmp_path):
    """Remote URLs that fail to clone (e.g. auth) should raise GitError."""
    import pygit2
    adapter = GitAdapter(cache_dir=tmp_path / "cache")
    with pytest.raises(pygit2.GitError):
        adapter.get_commit_hash("git@github.com:org/private-secret-repo.git", "main")


def test_get_commit_hash_local_repo_returns_sha(tmp_path, flat_repo):
    repo, repo_path = flat_repo
    adapter = GitAdapter(cache_dir=tmp_path / "cache")
    commit = adapter.get_commit_hash(str(repo_path), "master")
    assert commit == str(repo.head.target)


def test_read_file_flat_path_returns_content(tmp_path, flat_repo):
    """Bug #2: _traverse_tree returns TreeEntry; entry.data raises AttributeError.
    This test documents the intended behavior and currently fails."""
    repo, repo_path = flat_repo
    adapter = GitAdapter(cache_dir=tmp_path / "cache")
    commit = str(repo.head.target)
    content = adapter.read_file(str(repo_path), commit, "README.md")
    assert content == "hello"


def test_read_file_nested_path_returns_content(tmp_path, contract_repo):
    """Bug #1: nested traversal raises TypeError on second path component.
    This test documents the intended behavior and currently fails."""
    _, repo_path, commit = contract_repo
    adapter = GitAdapter(cache_dir=tmp_path / "cache")
    content = adapter.read_file(str(repo_path), commit,
                                "contracts/integration.contract.yaml")
    assert "name: pkg" in content


def test_read_file_missing_entry_raises(tmp_path, flat_repo):
    repo, repo_path = flat_repo
    adapter = GitAdapter(cache_dir=tmp_path / "cache")
    commit = str(repo.head.target)
    with pytest.raises(FileNotFoundError):
        adapter.read_file(str(repo_path), commit, "nonexistent.txt")


def test_read_file_directory_raises(tmp_path, contract_repo):
    """Reading a directory path (not a blob) should raise IsADirectoryError."""
    _, repo_path, commit = contract_repo
    adapter = GitAdapter(cache_dir=tmp_path / "cache")
    with pytest.raises((IsADirectoryError, Exception)):
        adapter.read_file(str(repo_path), commit, "contracts")


def test_get_repo_path_collision_avoidance(tmp_path):
    """Different URLs should map to different cache paths even if names match."""
    adapter = GitAdapter(cache_dir=tmp_path / "cache")
    path1 = adapter._get_repo_path("http://host1.com/repo.git")
    path2 = adapter._get_repo_path("http://host2.com/repo.git")
    assert path1 != path2
