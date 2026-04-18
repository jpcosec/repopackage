"""Segment helpers for markdown turn extraction."""

from __future__ import annotations

from workflow_pkg.common.text import normalize_text
from workflow_pkg.turns.markdown_splitter import MarkdownUserSplitter
from workflow_pkg.turns.models import Turn


class MarkdownSegmentBuilder:
    """Build turns from markdown marker segments."""

    def prelude(self, source: str, lines: list[str], stop: int) -> list[Turn]:
        """Create the leading user prelude turn."""

        content = normalize_text("\n".join(lines[:stop]))
        return [Turn(1, "user", content, source)] if content else []

    def append_segment(self, turns: list[Turn], source: str, lines: list[str]) -> None:
        """Append assistant and trailing user turns from one segment."""

        assistant, user = MarkdownUserSplitter().split(lines)
        self._append(turns, source, "assistant", assistant)
        self._append(turns, source, "user", user)

    def _append(
        self, turns: list[Turn], source: str, speaker: str, lines: list[str]
    ) -> None:
        """Append a normalized turn if it has content."""

        content = normalize_text("\n".join(lines))
        if content:
            turns.append(Turn(len(turns) + 1, speaker, content, source))
