"""Assistant marker detection."""

from __future__ import annotations

from talk_extractor.common.text import normalize_text


class AssistantMarkerDetector:
    """Detect assistant marker lines in markdown transcripts."""

    def is_marker(self, line: str) -> bool:
        """Tell whether a line marks the assistant speaker."""

        return normalize_text(line).lower() in self._markers()

    def positions(self, lines: list[str]) -> list[int]:
        """Return marker positions."""

        return [index for index, line in enumerate(lines) if self.is_marker(line)]

    def _markers(self) -> set[str]:
        """Return supported assistant labels."""

        return {
            "gem personalizado",
            "gemini",
            "bard",
            "arquitecto tecnico directo",
            "arquitecto técnico directo",
        }
