"""Directory management for semantic workspaces."""

from __future__ import annotations

import shutil
from pathlib import Path


class WorkspaceDirectoryManager:
    """Prepare or reset semantic workspace directories."""

    def prepare(self, paths: list[Path], clean: bool) -> None:
        """Ensure output directories exist."""

        for path in paths:
            self._prepare_one(path, clean)

    def _prepare_one(self, path: Path, clean: bool) -> None:
        """Prepare one directory."""

        if clean and path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
