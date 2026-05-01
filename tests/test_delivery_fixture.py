import pytest
import pygit2
from pathlib import Path
from ruamel.yaml import YAML
from repopackage.cli.handlers import handle_resolve, handle_validate
from repopackage.core import constants

yaml = YAML()

def test_ecosystem_fixture_resolution_and_validation(ecosystem_delivery_fixture, monkeypatch):
    """
    Prove that the delivery fixture can be used to resolve and validate a real-world scenario.
    """
    root = ecosystem_delivery_fixture["root"]
    monkeypatch.chdir(root)
    
    # Isolation: use a local cache for GitAdapter
    monkeypatch.setattr(constants, "CACHE_DIR", root / "cache")
    
    # 1. Define Project using the fixture repos
    compose_data = {
        "kind": "project",
        "name": "delivery-project",
        "uses": {
            "ui-kit": {
                "url": str(ecosystem_delivery_fixture["ui-kit"]),
                "branch": "master"
            },
            "diagnostics": {
                "url": str(ecosystem_delivery_fixture["diagnostics"]),
                "branch": "feat/new-check"
            }
        }
    }
    with open(constants.COMPOSE_FILE, "w") as f:
        yaml.dump(compose_data, f)
        
    # 2. Resolve
    handle_resolve()
    
    assert Path(constants.LOCK_FILE).exists()
    with open(constants.LOCK_FILE, "r") as f:
        lock_data = yaml.load(f)
        
    # 3. Simulate Materialization
    ws_packages = root / constants.WORKSPACE_DIR / "packages"
    ws_packages.mkdir(parents=True)
    
    for name, pkg in lock_data["packages"].items():
        pkg_path = ws_packages / name
        # Clone the remote
        repo = pygit2.clone_repository(pkg["url"], str(pkg_path))
        
        # Checkout the specific branch and update HEAD
        branch_name = pkg["branch"]
        try:
            # Try to find remote branch
            remote_branch = repo.branches.remote.get(f"origin/{branch_name}")
            if remote_branch:
                # Create local branch tracking remote
                local_branch = repo.create_branch(branch_name, repo[remote_branch.target])
                repo.checkout(local_branch)
            else:
                # Local branch case
                branch = repo.branches.get(branch_name)
                if branch:
                    repo.checkout(branch)
        except Exception:
            # Already exists or other error
            branch = repo.branches.get(branch_name)
            if branch:
                repo.checkout(branch)
        
    # 4. Validate
    handle_validate()
