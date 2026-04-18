"""Artifact write planning."""

from __future__ import annotations

from pathlib import Path

from workflow_pkg.artifacts.model import Artifact
from workflow_pkg.artifacts.plan import PlannedArtifact


class ArtifactWritePlanner:
    """Plan unique artifact file names."""

    def plan(
        self, artifacts: list[Artifact], output_dir: str | Path = "arctifacts"
    ) -> list[PlannedArtifact]:
        """Return artifact write plans."""

        directory = Path(output_dir)
        used: set[str] = set()
        return [self._plan_one(artifact, directory, used) for artifact in artifacts]

    def _plan_one(
        self, artifact: Artifact, directory: Path, used: set[str]
    ) -> PlannedArtifact:
        """Plan one file name and path."""

        base = f"{artifact.kind}_turn{artifact.turn_index:03d}_{artifact.label}"
        name = self._unique_name(base, artifact.extension, used)
        return PlannedArtifact(artifact, name, directory / name)

    def _unique_name(self, base: str, ext: str, used: set[str]) -> str:
        """Generate a unique file name."""

        name, counter = f"{base}.{ext}", 2
        while name in used:
            name = f"{base}_{counter}.{ext}"
            counter += 1
        used.add(name)
        return name
