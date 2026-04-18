"""Timeline scaffold builder."""

from __future__ import annotations

from workflow_pkg.semantic.ids import TurnIdFactory
from workflow_pkg.turns.models import Turn


class TimelineScaffoldBuilder:
    """Build the turn-by-turn timeline scaffold."""

    def build(self, turns: list[Turn], artifact_map: dict[str, list[str]]) -> str:
        """Return a timeline scaffold for all turns."""

        blocks = ["# Timeline", ""]
        for turn in turns:
            blocks.extend(self._entry(turn, artifact_map))
        return "\n".join(blocks)

    def _entry(self, turn: Turn, artifact_map: dict[str, list[str]]) -> list[str]:
        """Build one timeline entry."""

        tid = TurnIdFactory().build(turn.index)
        return self._header(tid, turn.speaker) + self._artifacts(
            artifact_map.get(tid, []), tid
        )

    def _header(self, tid: str, speaker: str) -> list[str]:
        """Build the common entry header."""

        return HEADER_TEMPLATE.format(tid=tid, speaker=speaker).splitlines()

    def _artifacts(self, artifacts: list[str], tid: str) -> list[str]:
        """Build artifact and evidence lines."""

        lines = [f"  - `{path}`" for path in artifacts] or ["  - none"]
        lines += ["- Decisions Touched:", "  - TBD", "- Evidence:", f"  - {tid}"]
        return lines + [f"  - `{path}`" for path in artifacts] + [""]


HEADER_TEMPLATE = """## {tid}
- Speaker: {speaker}
- Intent: TBD
- What Happened:
  - TBD
- State Change:
  - Added: TBD
  - Revised: TBD
  - Rejected: TBD
  - Finalized: TBD
- Artifacts Mentioned:"""
