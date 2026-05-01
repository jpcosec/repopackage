"""
Business logic handlers for CLI commands.
"""
import sys
from pathlib import Path
from ruamel.yaml import YAML
from ..core import constants
from ..adapters.git import GitAdapter
from ..adapters.repo import RepoAdapter
from ..core.solver import CompositionSolver

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)

def handle_init():
    """Initializes a new compose.yaml project model."""
    print("Initializing new project...")
    data = {"kind": "project", "name": Path.cwd().name, "uses": {}}
    with open(constants.COMPOSE_FILE, "w") as f:
        yaml.dump(data, f)
    print(f"Created {constants.COMPOSE_FILE}")

def handle_resolve():
    """Resolves graph and generates compose.lock.yaml."""
    if not Path(constants.COMPOSE_FILE).exists():
        print(f"{constants.COMPOSE_FILE} not found!")
        sys.exit(1)
    with open(constants.COMPOSE_FILE, "r") as f:
        config = yaml.load(f)
    solver = CompositionSolver(GitAdapter(cache_dir=constants.CACHE_DIR))
    try:
        lock_data = solver.resolve(config)
        with open(constants.LOCK_FILE, "w") as f:
            yaml.dump(lock_data, f)
        print(f"Resolved successfully. Wrote {constants.LOCK_FILE}")
    except Exception as e:
        print(f"Resolution failed: {e}")
        sys.exit(1)

def handle_sync():
    """Materializes workspace using google repo."""
    if not Path(constants.LOCK_FILE).exists():
        print(f"{constants.LOCK_FILE} not found! Run 'rp resolve' first.")
        sys.exit(1)
    with open(constants.LOCK_FILE, "r") as f:
        lock_data = yaml.load(f)
    adapter = RepoAdapter(workspace_dir=Path(constants.WORKSPACE_DIR))
    manifest_repo = adapter.generate_manifest(lock_data)
    adapter.sync(manifest_repo)
    print("Sync complete.")

from ..core.models import Lockfile

def handle_validate():
    """Verifies workspace integrity and schema presence."""
    if not Path(constants.LOCK_FILE).exists():
        print(f"{constants.LOCK_FILE} not found!")
        sys.exit(1)
    with open(constants.LOCK_FILE, "r") as f:
        raw_data = yaml.load(f)
    
    try:
        lock = Lockfile(**raw_data)
    except Exception as e:
        print(f"Error parsing lockfile: {e}")
        sys.exit(1)

    _perform_validation(lock)

def _perform_validation(lock: Lockfile):
    ws = Path(constants.WORKSPACE_DIR) / "packages"
    errors = []
    
    for name, pkg in lock.packages.items():
        pkg_path = ws / name
        pkg_errors = _validate_package_state(pkg_path, pkg)
        errors.extend(pkg_errors)
        
    if not errors:
        print("Validation passed.")
    else:
        print("Validation failed:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

def _validate_package_state(pkg_path, pkg):
    errors = []
    if not pkg_path.exists():
        errors.append(f"{pkg.name} missing from workspace!")
        return errors
        
    # Check commit
    try:
        repo = pygit2.Repository(str(pkg_path))
        ws_sha = str(repo.head.target)
        if not ws_sha.startswith(pkg.commit):
            errors.append(f"{pkg.name} commit mismatch: expected {pkg.commit[:8]}, found {ws_sha[:8]}")
    except Exception as e:
        errors.append(f"{pkg.name} git error: {e}")

    # Check contract
    c_path = pkg_path / constants.CONTRACT_PATH
    if not c_path.exists():
        errors.append(f"{pkg.name} missing {constants.CONTRACT_PATH}!")
    else:
        try:
            with open(c_path, "r") as f:
                data = yaml.load(f)
            # Check schemas
            for s in data.get("exports", []) + data.get("consumes", []):
                s_file = pkg_path / s["schema"]
                if not s_file.exists():
                    errors.append(f"Schema {s['schema']} for {pkg.name} missing!")
        except Exception as e:
            errors.append(f"{pkg.name} contract parse error: {e}")
            
    return errors

import pygit2
import networkx as nx

def handle_status():
    """Shows workspace sync and compatibility status."""
    if not Path(constants.LOCK_FILE).exists():
        print(f"{constants.LOCK_FILE} not found!")
        sys.exit(1)
        
    with open(constants.LOCK_FILE, "r") as f:
        raw_data = yaml.load(f)
        
    try:
        lock = Lockfile(**raw_data)
    except Exception as e:
        print(f"Error parsing lockfile: {e}")
        sys.exit(1)
        
    ws = Path(constants.WORKSPACE_DIR) / "packages"
    print(f"{'Package':<20} {'Lockfile SHA':<12} {'Workspace SHA':<12} {'Status'}")
    print("-" * 65)
    
    for name, pkg in lock.packages.items():
        pkg_path = ws / name
        lock_sha = pkg.commit[:8]
        
        if not pkg_path.exists():
            status = "MISSING"
            ws_sha = "n/a"
        else:
            try:
                repo = pygit2.Repository(str(pkg_path))
                ws_sha = str(repo.head.target)[:8]
                status = "OK" if ws_sha == lock_sha else "DIRTY/DIFF"
            except Exception:
                ws_sha = "error"
                status = "CORRUPT"
                
        print(f"{name:<20} {lock_sha:<12} {ws_sha:<12} {status}")

def handle_generate():
    """Identifies contracts and prepares for generation."""
    print("Scanning workspace for contracts...")
    ws = Path(constants.WORKSPACE_DIR) / "packages"
    found = 0
    for pkg_dir in ws.iterdir():
        if not pkg_dir.is_dir():
            continue
        c_path = pkg_dir / constants.CONTRACT_PATH
        if c_path.exists():
            print(f"  - Found {pkg_dir.name} contract at {c_path}")
            found += 1
    print(f"Total contracts found: {found}")

def handle_graph():
    """Exports the dependency graph in Mermaid format."""
    if not Path(constants.COMPOSE_FILE).exists():
        print(f"{constants.COMPOSE_FILE} not found!")
        sys.exit(1)
    with open(constants.COMPOSE_FILE, "r") as f:
        config = yaml.load(f)
        
    solver = CompositionSolver(GitAdapter(cache_dir=constants.CACHE_DIR))
    solver.resolve(config)
    
    print("\nMermaid Dependency Graph:")
    print("graph TD")
    for u, v in solver.graph.edges():
        print(f"    {u} --> {v}")

