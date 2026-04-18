"""Artifact extraction service."""

from __future__ import annotations

from pathlib import Path

from workflow_pkg.artifacts.planner import ArtifactWritePlanner
from workflow_pkg.artifacts.turn_extractor import TurnArtifactExtractor
from workflow_pkg.artifacts.writer import ArtifactWriter
from workflow_pkg.turns.service import TurnExtractionService


class ArtifactExtractionService:
    """Extract artifacts from all conversation turns."""

    def extract(self, source_path: str | Path, include_text: bool = False) -> list:
        """Return artifacts extracted from the source."""

        artifacts = self._all_artifacts(source_path)
        return artifacts if include_text else self._structured(artifacts)

    def _all_artifacts(self, source_path: str | Path) -> list:
        """Extract all artifacts from all turns."""

        turns = TurnExtractionService().extract(source_path)
        return [
            artifact
            for turn in turns
            for artifact in TurnArtifactExtractor().extract(turn)
        ]

    def _structured(self, artifacts: list) -> list:
        """Drop plain text artifacts."""

        return [artifact for artifact in artifacts if artifact.kind != "text"]

    def plan(
        self,
        source_path: str | Path,
        output_dir: str | Path = "arctifacts",
        include_text: bool = False,
    ) -> list:
        """Plan artifact writes for a source file."""

        return ArtifactWritePlanner().plan(
            self.extract(source_path, include_text), output_dir
        )

    def write(
        self,
        source_path: str | Path,
        output_dir: str | Path = "arctifacts",
        include_text: bool = False,
    ) -> list[Path]:
        """Extract artifacts and write them to disk."""

        planned = self.plan(source_path, output_dir, include_text)
        return ArtifactWriter().write(planned, output_dir)
