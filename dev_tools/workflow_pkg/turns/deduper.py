"""Turn deduplication logic."""

from __future__ import annotations

from workflow_pkg.common.text import normalize_text
from workflow_pkg.turns.models import Turn


class TurnDeduper:
    """Remove empty or repeated turns."""

    def dedupe(self, turns: list[Turn]) -> list[Turn]:
        """Return a normalized deduplicated turn list."""

        deduped: list[Turn] = []
        for turn in turns:
            self._append_if_new(deduped, turn)
        return deduped

    def _append_if_new(self, deduped: list[Turn], turn: Turn) -> None:
        """Append a turn when it is meaningful and new."""

        content = normalize_text(turn.content)
        if not content or self._is_duplicate(deduped, turn.speaker, content):
            return
        deduped.append(Turn(len(deduped) + 1, turn.speaker, content, turn.source))

    def _is_duplicate(self, turns: list[Turn], speaker: str, content: str) -> bool:
        """Tell whether the last turn matches the new one."""

        return bool(
            turns and turns[-1].speaker == speaker and turns[-1].content == content
        )
