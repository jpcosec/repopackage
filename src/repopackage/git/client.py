import pygit2
import hashlib
from pathlib import Path


class GitClient:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_commit_hash(self, repo_url: str, branch: str = "main") -> str:
        repo_path = self._get_repo_path(repo_url)
        repo = self._ensure_repo(repo_url, repo_path)
        return self._resolve_ref(repo, branch)

    def read_file(self, repo_url: str, commit_hash: str, file_path: str) -> str:
        repo_path = self._get_repo_path(repo_url)
        repo = pygit2.Repository(str(repo_path))
        commit = self._get_commit(repo, commit_hash)
        return self._read_blob(repo, commit.tree, file_path)

    def _get_repo_path(self, url: str) -> Path:
        if not url.startswith(("git@", "http")):
            return Path(url)
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:12]
        name = url.split("/")[-1].replace(".git", "")
        return self.cache_dir / f"{name}-{url_hash}"

    def _ensure_repo(self, url: str, path: Path) -> pygit2.Repository:
        if not path.exists():
            return self._clone(url, path)
        repo = pygit2.Repository(str(path))
        if url.startswith(("git@", "http")):
            self._fetch(repo)
        return repo

    def _clone(self, url: str, path: Path) -> pygit2.Repository:
        if not url.startswith(("git@", "http")):
            raise FileNotFoundError(f"Local repository not found at {path}")
        return pygit2.clone_repository(url, str(path), bare=True)

    def _fetch(self, repo: pygit2.Repository):
        for remote in repo.remotes:
            remote.fetch()

    def _resolve_ref(self, repo: pygit2.Repository, ref: str) -> str:
        try:
            remote_ref = repo.branches.remote.get(f"origin/{ref}")
            if remote_ref:
                return str(remote_ref.target)
            return str(repo.revparse_single(ref).id)
        except (KeyError, pygit2.GitError) as e:
            raise ValueError(f"Could not resolve ref '{ref}': {e}")

    def _get_commit(self, repo: pygit2.Repository, sha: str) -> pygit2.Commit:
        try:
            commit = repo.get(sha)
            if isinstance(commit, pygit2.Commit):
                return commit
        except Exception:
            pass
        raise ValueError(f"Commit {sha} not found")

    def _read_blob(self, repo: pygit2.Repository, tree: pygit2.Tree, path: str) -> str:
        try:
            entry = tree[path]
            obj = repo[entry.id]
            if obj.type == pygit2.enums.ObjectType.BLOB:
                return obj.data.decode("utf-8")
            raise IsADirectoryError(f"'{path}' is a {obj.type}")
        except KeyError:
            raise FileNotFoundError(f"File '{path}' not found")
