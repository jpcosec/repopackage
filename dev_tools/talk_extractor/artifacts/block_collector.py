"""Artifact block collection from turn text."""

from __future__ import annotations

from talk_extractor.artifacts.rules import ArtifactRules


class ArtifactBlockCollector:
    """Collect artifact-like blocks from turn content."""

    def collect(self, content: str) -> list[tuple[int, int, str, str]]:
        """Return ordered block matches."""

        matches = self._fenced(content)
        return sorted(
            matches + self._plantuml(content, matches), key=lambda item: item[0]
        )

    def _fenced(self, content: str) -> list[tuple[int, int, str, str]]:
        """Collect fenced blocks."""

        pattern = ArtifactRules().fenced_block()
        return [
            (m.start(), m.end(), m.group("lang").strip(), m.group("body").rstrip())
            for m in pattern.finditer(content)
        ]

    def _plantuml(
        self, content: str, fenced: list[tuple[int, int, str, str]]
    ) -> list[tuple[int, int, str, str]]:
        """Collect non-fenced PlantUML blocks."""

        ranges = [(start, end) for start, end, _, _ in fenced]
        pattern = ArtifactRules().plantuml()
        return [
            self._match_tuple(m)
            for m in pattern.finditer(content)
            if not self._inside(m.start(), m.end(), ranges)
        ]

    def _inside(self, start: int, end: int, ranges: list[tuple[int, int]]) -> bool:
        """Tell whether a block is inside another block."""

        return any(left <= start and end <= right for left, right in ranges)

    def _match_tuple(self, match) -> tuple[int, int, str, str]:
        """Convert a regex match into a block tuple."""

        return (match.start(), match.end(), "plantuml", match.group(0).rstrip())
