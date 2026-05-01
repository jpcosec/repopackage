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

def handle_validate():
    """Verifies workspace integrity and schema presence."""
    if not Path(constants.LOCK_FILE).exists():
        print(f"{constants.LOCK_FILE} not found!")
        sys.exit(1)
    with open(constants.LOCK_FILE, "r") as f:
        lock_data = yaml.load(f)
    _perform_validation(lock_data)

def _perform_validation(lock_data):
    ws = Path(constants.WORKSPACE_DIR)
    all_passed = True
    packages = lock_data.get("packages", lock_data.get("repopackages", {}))
    for pkg in packages.keys():
        if not _validate_package(ws / "packages" / pkg, pkg):
            all_passed = False
    if all_passed:
        print("Validation passed.")
    else:
        print("Validation failed.")
        sys.exit(1)

import pygit2
import networkx as nx

def handle_status():
    """Shows workspace sync and compatibility status."""
    if not Path(constants.LOCK_FILE).exists():
        print(f"{constants.LOCK_FILE} not found!")
        sys.exit(1)
        
    with open(constants.LOCK_FILE, "r") as f:
        lock_data = yaml.load(f)
        
    ws = Path(constants.WORKSPACE_DIR) / "packages"
    print(f"{'Package':<20} {'Lockfile SHA':<12} {'Workspace SHA':<12} {'Status'}")
    print("-" * 65)
    
    packages = lock_data.get("packages", lock_data.get("repopackages", {}))
    for name, data in packages.items():
        # Handle both old dict format and new ResolvedPackage model (which becomes a dict here)
        pkg_path = ws / name
        lock_sha = data["commit"][:8]
        
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

def _validate_package(pkg_path, pkg_name):
    if not pkg_path.exists():
        print(f"Error: {pkg_name} missing from workspace!")
        return False
    c_path = pkg_path / constants.CONTRACT_PATH
    if not c_path.exists():
        print(f"Error: {pkg_name} missing {constants.CONTRACT_PATH}!")
        return False
    with open(c_path, "r") as f:
        data = yaml.load(f)
    return _check_schemas(pkg_path, pkg_name, data)

def _check_schemas(pkg_path, pkg_name, data):
    ok = True
    for s in data.get("exports", []) + data.get("consumes", []):
        s_file = pkg_path / s["schema"]
        if not s_file.exists():
            print(f"Error: Schema {s_file} for {pkg_name} missing!")
            ok = False
    return ok
