"""Turn semantic scaffold builder."""

from __future__ import annotations

from workflow_pkg.semantic.ids import TurnIdFactory
from workflow_pkg.turns.models import Turn


HEAD_TEMPLATE = """# {tid}

## Summary
- TBD

## Intent
- TBD

## Conversation Role
- TBD

## Semantic Contribution
- TBD

## Artifacts"""


TAIL_TEMPLATE = """
## Decisions
- TBD

## Resulting State
- TBD

## Evidence
- {tid}"""


class TurnScaffoldBuilder:
    """Build semantic scaffolds for per-turn files."""

    def build(self, turn: Turn, artifact_paths: list[str]) -> str:
        """Return the per-turn scaffold markdown."""

        tid = TurnIdFactory().build(turn.index)
        lines = (
            self._head(tid)
            + self._artifacts(artifact_paths)
            + self._tail(tid, artifact_paths)
        )
        return "\n".join(lines)

    def _head(self, tid: str) -> list[str]:
        """Build the shared turn header."""

        return HEAD_TEMPLATE.format(tid=tid).splitlines()

    def _artifacts(self, artifact_paths: list[str]) -> list[str]:
        """Build artifact summary lines."""

        return [f"- `{path}` - TBD" for path in artifact_paths] or ["- none"]

    def _tail(self, tid: str, artifact_paths: list[str]) -> list[str]:
        """Build the trailing sections."""

        tail = TAIL_TEMPLATE.format(tid=tid).splitlines()
        return tail + [f"- `{path}`" for path in artifact_paths] + [""]
