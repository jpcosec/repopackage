import pytest
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from repopackage.repo.manifest import ManifestBuilder

def test_derive_fetch_and_name_ssh():
    manifest = ManifestBuilder(Path("/tmp/ws"))
    fetch, name = manifest._derive_fetch_and_name("git@github.com:org/repo.git")
    assert fetch == "git@github.com:"
    assert name == "org/repo.git"

def test_derive_fetch_and_name_https():
    manifest = ManifestBuilder(Path("/tmp/ws"))
    fetch, name = manifest._derive_fetch_and_name("https://github.com/org/repo.git")
    assert fetch == "https://github.com"
    assert name == "org/repo.git"

def test_derive_fetch_and_name_local():
    manifest = ManifestBuilder(Path("/tmp/ws"))
    fetch, name = manifest._derive_fetch_and_name("/tmp/repos/my-repo")
    assert fetch == "/tmp/repos"
    assert name == "my-repo"

def test_generate_manifest_deduplicates_remotes(tmp_path):
    manifest = ManifestBuilder(tmp_path)
    lock_data = {
        "packages": {
            "p1": {"url": "git@github.com:org/p1.git", "branch": "master"},
            "p2": {"url": "git@github.com:org/p2.git", "branch": "main"},
            "local": {"url": "./local-repo", "branch": "dev"}
        }
    }
    
    manifest_path = manifest.generate_manifest(lock_data)
    tree = ET.parse(Path(manifest_path) / "default.xml")
    root = tree.getroot()
    
    remotes = root.findall("remote")
    # 1 default + 1 github + 1 local (which uses .) = 3? 
    # Actually my implementation for local uses fetch=os.path.dirname(url)
    
    fetch_bases = [r.get("fetch") for r in remotes]
    assert len(fetch_bases) == len(set(fetch_bases))
    assert "git@github.com:" in fetch_bases
