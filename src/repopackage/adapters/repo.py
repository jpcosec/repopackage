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
        ET.SubElement(root, "remote", name="default", fetch=".")
        ET.SubElement(root, "default", revision="main", remote="default")
        packages = data.get("packages", data.get("repopackages", {}))
        for name, pkg in packages.items():
            self._add_project_node(root, name, pkg)

    def _add_project_node(self, root, pkg_name, pkg):
        url = pkg["url"]
        rem_name = f"remote_{pkg_name.replace('-', '_')}"
        ET.SubElement(root, "remote", name=rem_name, fetch=os.path.dirname(url))
        ET.SubElement(root, "project", name=os.path.basename(url),
                      path=f"packages/{pkg_name}", remote=rem_name,
                      revision=pkg.get("commit") or pkg.get("branch", "main"))

    def _write_and_commit(self, path, root):
        ET.ElementTree(root).write(path / "default.xml", encoding="utf-8")
        subprocess.run(["git", "add", "default.xml"], cwd=path, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "up"], cwd=path)
        subprocess.run(["git", "checkout", "-q", "-B", "master"], cwd=path)
