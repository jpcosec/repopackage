"""Artifact file writer."""

from __future__ import annotations

from pathlib import Path

from workflow_pkg.artifacts.plan import PlannedArtifact


class ArtifactWriter:
    """Write planned artifacts and their index."""

    def write(
        self, planned: list[PlannedArtifact], output_dir: str | Path = "arctifacts"
    ) -> list[Path]:
        """Write all planned artifacts to disk."""

        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        written = [self._write_one(item) for item in planned]
        return written + [self._write_index(planned, directory)]

    def _write_one(self, item: PlannedArtifact) -> Path:
        """Write one planned artifact."""

        item.path.write_text(item.artifact.content, encoding="utf-8")
        return item.path

    def _write_index(self, planned: list[PlannedArtifact], directory: Path) -> Path:
        """Write the artifact index markdown file."""

        lines = ["# Extracted artifacts", ""]
        lines.extend(self._index_line(item) for item in planned)
        path = directory / "index.md"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    def _index_line(self, item: PlannedArtifact) -> str:
        """Build one index line."""

        art = item.artifact
        return f"- `{item.filename}` - turn {art.turn_index:03d}, {art.speaker}, {art.kind}, source `{art.source}`"
