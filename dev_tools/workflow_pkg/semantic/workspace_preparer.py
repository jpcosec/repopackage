"""Semantic workspace preparation service."""

from __future__ import annotations

from pathlib import Path

from workflow_pkg.semantic.artifact_packager import ArtifactPackager
from workflow_pkg.semantic.directories import WorkspaceDirectoryManager
from workflow_pkg.semantic.materializer import SemanticMaterializer


class SemanticWorkspacePreparer:
    """Prepare semantic evidence and scaffold files."""

    def prepare(
        self,
        source_path: str,
        turns_dir: str,
        artifacts_dir: str,
        semantic_dir: str,
        include_text: bool,
        clean: bool,
    ) -> dict:
        """Prepare the full semantic workspace."""

        paths = self._paths(turns_dir, artifacts_dir, semantic_dir)
        WorkspaceDirectoryManager().prepare(
            [paths["semantic"], paths["semantic_turns"], paths["curated"]], clean
        )
        turns, planned = ArtifactPackager().prepare(
            source_path, paths["turns"], paths["artifacts"], include_text, clean
        )
        return SemanticMaterializer().write(
            Path(source_path), paths, turns, planned, include_text
        )

    def _paths(
        self, turns_dir: str, artifacts_dir: str, semantic_dir: str
    ) -> dict[str, Path]:
        """Build workspace path objects."""

        base = Path(semantic_dir)
        return {
            "turns": Path(turns_dir),
            "artifacts": Path(artifacts_dir),
            "semantic": base,
            "semantic_turns": base / "turns",
            "curated": base / "artifacts",
        }
