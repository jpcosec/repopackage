"""
Business logic handlers for CLI commands.
"""
import sys
from pathlib import Path
from ruamel.yaml import YAML
import pygit2
from ..core import constants
from ..adapters.git import GitAdapter
from ..adapters.repo import RepoAdapter
from ..core.solver import CompositionSolver, SolverError
from ..core.models import Lockfile

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
    config = _load_compose_file()
    solver = CompositionSolver(GitAdapter(cache_dir=constants.CACHE_DIR))
    try:
        lock_data = solver.resolve(config)
        _save_lock_file(lock_data)
        print(f"Resolved successfully. Wrote {constants.LOCK_FILE}")
    except SolverError as e:
        print(f"Resolution failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def _load_compose_file():
    if not Path(constants.COMPOSE_FILE).exists():
        print(f"{constants.COMPOSE_FILE} not found!")
        sys.exit(1)
    with open(constants.COMPOSE_FILE, "r") as f:
        return yaml.load(f)


def _save_lock_file(data):
    with open(constants.LOCK_FILE, "w") as f:
        yaml.dump(data, f)


def handle_sync():
    """Materializes workspace using google repo."""
    lock_data = _load_lock_data()
    adapter = RepoAdapter(workspace_dir=Path(constants.WORKSPACE_DIR))
    manifest_repo = adapter.generate_manifest(lock_data)
    adapter.sync(manifest_repo)
    print("Sync complete.")


def _load_lock_data():
    if not Path(constants.LOCK_FILE).exists():
        print(f"{constants.LOCK_FILE} not found! Run 'rp resolve' first.")
        sys.exit(1)
    with open(constants.LOCK_FILE, "r") as f:
        return yaml.load(f)


def handle_validate():
    """Verifies workspace integrity and schema presence."""
    lock = _load_lock_model()
    _perform_validation(lock)


def _load_lock_model():
    raw = _load_lock_data()
    try:
        return Lockfile(**raw)
    except Exception as e:
        print(f"Error parsing lockfile: {e}")
        sys.exit(1)


def _perform_validation(lock: Lockfile):
    ws = Path(constants.WORKSPACE_DIR) / "packages"
    errors = []
    for name, pkg in lock.packages.items():
        errors.extend(_validate_package(ws / name, pkg))
    _report_validation(errors)


def _report_validation(errors):
    if not errors:
        print("Validation passed.")
        return
    print("Validation failed:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)


def _validate_package(path, pkg):
    if not path.exists():
        return [f"{pkg.name} missing from workspace!"]
    errors = _validate_git_state(path, pkg)
    errors.extend(_validate_contract_schemas(path, pkg))
    return errors


def _validate_git_state(path, pkg):
    try:
        repo = pygit2.Repository(str(path))
        ws_sha = str(repo.head.target)
        if not ws_sha.startswith(pkg.commit):
            return [f"{pkg.name} commit mismatch: expected {pkg.commit[:8]}, found {ws_sha[:8]}"]
    except Exception as e:
        return [f"{pkg.name} git error: {e}"]
    return []


def _validate_contract_schemas(path, pkg):
    c_path = path / constants.CONTRACT_PATH
    if not c_path.exists():
        return [f"{pkg.name} missing {constants.CONTRACT_PATH}!"]
    return _check_schema_files(path, pkg, c_path)


def _check_schema_files(path, pkg, c_path):
    errors = []
    try:
        with open(c_path, "r") as f:
            data = yaml.load(f)
        for s in data.get("exports", []) + data.get("consumes", []):
            if not (path / s["schema"]).exists():
                errors.append(f"Schema {s['schema']} for {pkg.name} missing!")
    except Exception as e:
        errors.append(f"{pkg.name} contract parse error: {e}")
    return errors


def handle_status():
    """Shows workspace sync and compatibility status."""
    lock = _load_lock_model()
    ws = Path(constants.WORKSPACE_DIR) / "packages"
    _print_status_header()
    for name, pkg in lock.packages.items():
        _print_package_status(ws / name, pkg)


def _print_status_header():
    print(f"{'Package':<20} {'Lockfile SHA':<12} {'Workspace SHA':<12} {'Status'}")
    print("-" * 65)


def _print_package_status(path, pkg):
    lock_sha = pkg.commit[:8]
    ws_sha, status = _get_ws_status(path, lock_sha)
    print(f"{pkg.name:<20} {lock_sha:<12} {ws_sha:<12} {status}")


def _get_ws_status(path, lock_sha):
    if not path.exists():
        return "n/a", "MISSING"
    try:
        repo = pygit2.Repository(str(path))
        ws_sha = str(repo.head.target)[:8]
        status = "OK" if ws_sha == lock_sha else "DIRTY/DIFF"
        return ws_sha, status
    except Exception:
        return "error", "CORRUPT"


def handle_generate():
    """Identifies contracts and prepares for generation."""
    print("Scanning workspace for contracts...")
    ws = Path(constants.WORKSPACE_DIR) / "packages"
    found = _scan_contracts(ws)
    print(f"Total contracts found: {found}")


def _scan_contracts(ws_path):
    found = 0
    if not ws_path.exists():
        return 0
    for pkg_dir in ws_path.iterdir():
        if pkg_dir.is_dir() and (pkg_dir / constants.CONTRACT_PATH).exists():
            print(f"  - Found {pkg_dir.name} contract")
            found += 1
    return found


def handle_graph():
    """Exports the dependency graph in Mermaid format."""
    config = _load_compose_file()
    solver = CompositionSolver(GitAdapter(cache_dir=constants.CACHE_DIR))
    solver.resolve(config)
    _print_mermaid(solver.graph)


def _print_mermaid(graph):
    print("\nMermaid Dependency Graph:")
    print("graph TD")
    for u, v in graph.edges():
        print(f"    {u} --> {v}")


def handle_exports():
    """Enumerates and exposes package-visible capabilities."""
    lock = _load_lock_model()
    ws = Path(constants.WORKSPACE_DIR) / "packages"
    print(f"## Ecosystem Export Surface (Target: {lock.project})\n")
    for name, pkg in lock.packages.items():
        _report_package_exports(ws / name, pkg)


def _report_package_exports(path, pkg):
    c_path = path / constants.CONTRACT_PATH
    if not c_path.exists():
        return
    try:
        with open(c_path, "r") as f:
            data = yaml.load(f)
        exports = data.get("export_surface")
        if exports:
            _print_export_details(pkg, exports)
    except Exception as e:
        print(f"  ⚠️ Error reading exports for {pkg.name}: {e}")


def _print_export_details(pkg, exports):
    print(f"### Package: {pkg.name}")
    print(f"  Provenance: {pkg.url} @ {pkg.commit[:8]}")
    _print_section("Commands", exports.get("commands"))
    _print_section("Contracts", exports.get("contracts"))
    _print_section("Procedures", exports.get("procedures"))
    print()


def _print_section(title, items):
    if not items:
        return
    print(f"  {title}:")
    for name, data in items.items():
        desc = data.get("description", "No description")
        print(f"    - {name}: {desc}")
