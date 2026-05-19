"""
Adapter for Google Repo tool interaction.
"""
import xml.etree.ElementTree as ET
import subprocess
from pathlib import Path
import os
from urllib.parse import urlparse
from ..core import constants


class RepoAdapter:
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

    def generate_manifest(self, lockfile_data: dict) -> str:
        """Translates lockfile into manifest.xml repo."""
        m_repo = self.workspace_dir / "manifest-repo"
        m_repo.mkdir(parents=True, exist_ok=True)
        self._ensure_git_repo(m_repo)
        root = ET.Element("manifest")
        self._build_manifest_xml(root, lockfile_data)
        self._write_and_commit(m_repo, root)
        return str(m_repo.absolute())

    def sync(self, manifest_url: str):
        """Executes repo init and sync."""
        rb = str(constants.REPO_TOOL)
        self._run_cmd([rb, "init", "-q", "-u", manifest_url, "-b", "master"])
        self._run_cmd([rb, "sync", "-q", "-j4"])

    def _run_cmd(self, args):
        subprocess.run(args, cwd=self.workspace_dir, check=True)

    def _ensure_git_repo(self, path):
        if not (path / ".git").exists():
            subprocess.run(["git", "init", "-q"], cwd=path, check=True)
        return {**os.environ, 
                "GIT_AUTHOR_NAME": "RP", "GIT_AUTHOR_EMAIL": "rp@ex.com",
                "GIT_COMMITTER_NAME": "RP", "GIT_COMMITTER_EMAIL": "rp@ex.com"}

    def _build_manifest_xml(self, root, data):
        self._add_defaults(root)
        pkgs = data.get("packages", data.get("repopackages", {}))
        remotes = {"." : "origin"} # fetch_base -> remote_name
        for name, pkg in pkgs.items():
            self._add_project(root, name, pkg, remotes)

    def _add_defaults(self, root):
        ET.SubElement(root, "remote", name="origin", fetch=".")
        ET.SubElement(root, "default", revision="master", remote="origin")

    def _add_project(self, root, name, pkg, remotes):
        fetch, proj_name = self._derive_fetch_and_name(pkg["url"])
        if fetch not in remotes:
            remotes[fetch] = f"remote_{len(remotes)}"
            ET.SubElement(root, "remote", name=remotes[fetch], fetch=fetch)
        
        rev = pkg.get("commit") or pkg.get("branch", "master")
        ET.SubElement(root, "project", name=proj_name,
                      path=f"packages/{name}", remote=remotes[fetch],
                      revision=rev)

    def _derive_fetch_and_name(self, url):
        if url.startswith("git@"):
            return self._derive_ssh(url)
        if "://" in url:
            return self._derive_http(url)
        return os.path.dirname(url), os.path.basename(url)

    def _derive_ssh(self, url):
        if ":" in url:
            base, path = url.split(":", 1)
            return f"{base}:", path
        return os.path.dirname(url), os.path.basename(url)

    def _derive_http(self, url):
        parsed = urlparse(url)
        fetch = f"{parsed.scheme}://{parsed.netloc}"
        path = parsed.path.lstrip("/")
        return fetch, path

    def _write_and_commit(self, path, root):
        ET.ElementTree(root).write(path / "default.xml", encoding="utf-8")
        env = self._ensure_git_repo(path)
        subprocess.run(["git", "add", "default.xml"], cwd=path, check=True, env=env)
        subprocess.run(["git", "commit", "-q", "-m", "up"], cwd=path, env=env)
        subprocess.run(["git", "checkout", "-q", "-B", "master"], cwd=path, env=env)
