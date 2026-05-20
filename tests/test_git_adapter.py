import pytest
from repopackage.git.client import GitClient


def test_get_commit_hash_missing_local_repo_raises(tmp_path):
    client = GitClient(cache_dir=tmp_path / "cache")
    with pytest.raises(FileNotFoundError):
        client.get_commit_hash(str(tmp_path / "nonexistent"), "main")


def test_get_commit_hash_unauthorized_remote_raises(tmp_path):
    import pygit2
    client = GitClient(cache_dir=tmp_path / "cache")
    with pytest.raises(pygit2.GitError):
        client.get_commit_hash("git@github.com:org/private-secret-repo.git", "main")


def test_get_commit_hash_local_repo_returns_sha(tmp_path, flat_repo):
    repo, repo_path = flat_repo
    client = GitClient(cache_dir=tmp_path / "cache")
    commit = client.get_commit_hash(str(repo_path), "master")
    assert commit == str(repo.head.target)


def test_read_file_flat_path_returns_content(tmp_path, flat_repo):
    repo, repo_path = flat_repo
    client = GitClient(cache_dir=tmp_path / "cache")
    commit = str(repo.head.target)
    content = client.read_file(str(repo_path), commit, "README.md")
    assert content == "hello"


def test_read_file_nested_path_returns_content(tmp_path, contract_repo):
    _, repo_path, commit = contract_repo
    client = GitClient(cache_dir=tmp_path / "cache")
    content = client.read_file(str(repo_path), commit,
                                "contracts/integration.contract.yaml")
    assert "name: pkg" in content


def test_read_file_missing_entry_raises(tmp_path, flat_repo):
    repo, repo_path = flat_repo
    client = GitClient(cache_dir=tmp_path / "cache")
    commit = str(repo.head.target)
    with pytest.raises(FileNotFoundError):
        client.read_file(str(repo_path), commit, "nonexistent.txt")


def test_read_file_directory_raises(tmp_path, contract_repo):
    _, repo_path, commit = contract_repo
    client = GitClient(cache_dir=tmp_path / "cache")
    with pytest.raises((IsADirectoryError, Exception)):
        client.read_file(str(repo_path), commit, "contracts")


def test_get_repo_path_collision_avoidance(tmp_path):
    client = GitClient(cache_dir=tmp_path / "cache")
    path1 = client._get_repo_path("http://host1.com/repo.git")
    path2 = client._get_repo_path("http://host2.com/repo.git")
    assert path1 != path2
