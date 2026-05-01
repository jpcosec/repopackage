"""
System-wide constants and filenames.
"""
from pathlib import Path

COMPOSE_FILE = "compose.yaml"
LOCK_FILE = "compose.lock.yaml"
CONTRACT_PATH = "contracts/integration.contract.yaml"
WORKSPACE_DIR = "workspace"
CACHE_DIR = Path.home() / ".repopackage" / "cache"
REPO_TOOL = Path.home() / "bin" / "repo"
DEFAULT_BRANCH = "master"
