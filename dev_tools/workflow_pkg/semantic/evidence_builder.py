"""Evidence assembly for the semantic layer."""

from __future__ import annotations

from workflow_pkg.artifacts.plan import PlannedArtifact
from workflow_pkg.semantic.evidence_artifact import EvidenceArtifact
from workflow_pkg.semantic.evidence_turn import EvidenceTurn
from workflow_pkg.semantic.ids import TurnIdFactory
from workflow_pkg.turns.models import Turn


class EvidenceBuilder:
    """Build evidence models and artifact maps."""

    def artifact_map(self, planned: list[PlannedArtifact]) -> dict[str, list[str]]:
        """Map turn ids to artifact paths."""

        mapping: dict[str, list[str]] = {}
        for item in planned:
            mapping.setdefault(
                TurnIdFactory().build(item.artifact.turn_index), []
            ).append(item.path.as_posix())
        return mapping

    def artifacts(self, planned: list[PlannedArtifact]) -> list[EvidenceArtifact]:
        """Build evidence artifacts from plans."""

        return [
            self._artifact(index, item) for index, item in enumerate(planned, start=1)
        ]

    def turns(
        self,
        source: str,
        turns: list[Turn],
        mapping: dict[str, list[str]],
        turn_dir: str,
    ) -> list[EvidenceTurn]:
        """Build evidence turns from extracted turns."""

        return [self._turn(source, turn, mapping, turn_dir) for turn in turns]

    def _artifact(self, index: int, item: PlannedArtifact) -> EvidenceArtifact:
        """Build one evidence artifact."""

        return EvidenceArtifact(
            f"ART-{index:03d}",
            item.path.as_posix(),
            item.path.as_posix(),
            TurnIdFactory().build(item.artifact.turn_index),
            item.artifact.kind,
            item.artifact.speaker,
            item.artifact.label,
        )

    def _turn(
        self, source: str, turn: Turn, mapping: dict[str, list[str]], turn_dir: str
    ) -> EvidenceTurn:
        """Build one evidence turn."""

        tid = TurnIdFactory().build(turn.index)
        path = f"{turn_dir}/{tid}.md"
        return EvidenceTurn(tid, source, turn.speaker, path, mapping.get(tid, []))
