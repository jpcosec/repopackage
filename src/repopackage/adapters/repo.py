"""
Adapter for Google Repo tool interaction.
"""
import xml.etree.ElementTree as ET
import subprocess
from pathlib import Path
import os
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
        subprocess.run([rb, "init", "-q", "-u", manifest_url, "-b", "master"], 
                       cwd=self.workspace_dir, check=True)
        subprocess.run([rb, "sync", "-q", "-j4"], 
                       cwd=self.workspace_dir, check=True)

    def _ensure_git_repo(self, path):
        if not (path / ".git").exists():
            subprocess.run(["git", "init", "-q"], cwd=path, check=True)
            subprocess.run(["git", "config", "user.email", "rp@ex.com"], 
                           cwd=path, check=True)
            subprocess.run(["git", "config", "user.name", "RP"], 
                           cwd=path, check=True)

    def _build_manifest_xml(self, root, data):
        # Default remote for relative paths
        default_fetch = "."
        ET.SubElement(root, "remote", name="origin", fetch=default_fetch)
        ET.SubElement(root, "default", revision="master", remote="origin")
        
        packages = data.get("packages", data.get("repopackages", {}))
        remotes_map = {default_fetch: "origin"} # fetch_base -> remote_name
        
        for name, pkg in packages.items():
            url = pkg["url"]
            fetch_base, project_name = self._derive_fetch_and_name(url)
            
            if fetch_base not in remotes_map:
                rem_name = f"remote_{len(remotes_map)}"
                remotes_map[fetch_base] = rem_name
                ET.SubElement(root, "remote", name=rem_name, fetch=fetch_base)
            
            rem_name = remotes_map[fetch_base]
            ET.SubElement(root, "project", name=project_name,
                          path=f"packages/{name}", remote=rem_name,
                          revision=pkg.get("commit") or pkg.get("branch", "master"))

    def _derive_fetch_and_name(self, url):
        """Robustly derives the fetch base and project name from various URL forms."""
        if url.startswith("git@"):
            if ":" in url:
                base, path = url.split(":", 1)
                return f"{base}:", path
            return os.path.dirname(url), os.path.basename(url)
        elif "://" in url:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            fetch = f"{parsed.scheme}://{parsed.netloc}"
            path = parsed.path.lstrip("/")
            return fetch, path
        # Local paths
        return os.path.dirname(url), os.path.basename(url)

    def _write_and_commit(self, path, root):
        ET.ElementTree(root).write(path / "default.xml", encoding="utf-8")
        subprocess.run(["git", "add", "default.xml"], cwd=path, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "up"], cwd=path)
        subprocess.run(["git", "checkout", "-q", "-B", "master"], cwd=path)
