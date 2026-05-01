"""
Git Adapter for high-fidelity repository inspection.
"""
import pygit2
from pathlib import Path
from typing import Optional


class GitAdapter:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_commit_hash(self, repo_url: str, branch: str = "main") -> str:
        """Retrieves the latest commit hash for a branch, cloning or fetching as needed."""
        repo_path = self._get_repo_path(repo_url)
        repo = self._ensure_repo(repo_url, repo_path)
        
        # Try to find the branch in remotes
        remote_branch = f"origin/{branch}"
        try:
            branch_ref = repo.branches.remote.get(remote_branch)
            if branch_ref:
                return str(branch_ref.target)
            
            # Fallback to revparse (handles local branches, tags, or SHAs)
            obj = repo.revparse_single(branch)
            return str(obj.id)
        except (KeyError, pygit2.GitError) as e:
            raise ValueError(f"Could not resolve branch/ref '{branch}' in {repo_url}: {e}")

    def read_file(self, repo_url: str, commit_hash: str, file_path: str) -> str:
        """Reads a file directly from a Git tree without checkout."""
        repo_path = self._get_repo_path(repo_url)
        repo = pygit2.Repository(str(repo_path))
        
        try:
            commit = repo.get(commit_hash)
        except Exception:
            commit = None

        if not commit:
            raise ValueError(f"Commit {commit_hash} not found in {repo_url}")
            
        tree = commit.tree
        try:
            entry = tree[file_path]
            obj = repo[entry.id]
            if obj.type == pygit2.enums.ObjectType.BLOB:
                return obj.data.decode("utf-8")
            raise IsADirectoryError(f"'{file_path}' in {repo_url} is a {obj.type}, not a blob")
        except KeyError:
            raise FileNotFoundError(f"File '{file_path}' not found in {repo_url} at {commit_hash}")

    def _ensure_repo(self, url: str, path: Path) -> pygit2.Repository:
        """Ensures the repository exists locally and is up to date."""
        if not path.exists():
            # If it's a local path that doesn't exist, we can't clone it from "nothing"
            # unless it's a URL. If it's a local path, raise FileNotFoundError.
            if not url.startswith(("git@", "http")):
                raise FileNotFoundError(f"Local repository not found at {path}")
            return pygit2.clone_repository(url, str(path), bare=True)
        
        repo = pygit2.Repository(str(path))
        # Fetch updates only for non-local repos
        if url.startswith(("git@", "http")):
            for remote in repo.remotes:
                remote.fetch()
        return repo

    def _get_repo_path(self, url: str) -> Path:
        """Translates URL to local cache path."""
        if url.startswith(("git@", "http")):
            # Simple hash-based or name-based directory
            name = url.split("/")[-1].replace(".git", "")
            return self.cache_dir / name
        return Path(url)
