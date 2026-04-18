"""Extract turns from markdown transcripts."""

from __future__ import annotations

from pathlib import Path

from workflow_pkg.common.text import normalize_text
from workflow_pkg.turns.deduper import TurnDeduper
from workflow_pkg.turns.markdown_markers import AssistantMarkerDetector
from workflow_pkg.turns.markdown_segments import MarkdownSegmentBuilder
from workflow_pkg.turns.models import Turn


class MarkdownTurnExtractor:
    """Extract turns from markdown dumps."""

    def extract(self, path: str | Path) -> list[Turn]:
        """Return deduplicated turns from markdown."""

        path = Path(path)
        turns = self._turns(path.name, path.read_text(encoding="utf-8", errors="ignore").splitlines())
        return TurnDeduper().dedupe(turns)

    def _turns(self, source: str, lines: list[str]) -> list[Turn]:
        """Build turns from marker-based segments."""

        detector = AssistantMarkerDetector()
        positions = detector.positions(lines)
        return self._unknown(source, lines) if not positions else self._marked(source, lines, positions, detector)

    def _unknown(self, source: str, lines: list[str]) -> list[Turn]:
        """Fallback for files without markers."""

        content = normalize_text("\n".join(lines))
        return [Turn(1, "unknown", content, source)] if content else []

    def _marked(self, source: str, lines: list[str], positions: list[int], detector: AssistantMarkerDetector) -> list[Turn]:
        """Parse files that contain assistant markers."""

        builder = MarkdownSegmentBuilder()
        turns = builder.prelude(source, lines, positions[0])
        for index, start in enumerate(positions):
            builder.append_segment(turns, source, self._segment(lines, start, self._next(positions, index, lines), detector))
        return turns

    def _segment(self, lines: list[str], start: int, stop: int, detector: AssistantMarkerDetector) -> list[str]:
        """Return one segment without marker lines."""

        while start < stop and detector.is_marker(lines[start]):
            start += 1
        return lines[start:stop]

    def _next(self, positions: list[int], index: int, lines: list[str]) -> int:
        """Return the next marker or the file end."""

        return positions[index + 1] if index + 1 < len(positions) else len(lines)
