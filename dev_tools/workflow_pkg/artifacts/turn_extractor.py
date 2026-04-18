"""Artifact extraction from a single turn."""

from __future__ import annotations

from workflow_pkg.artifacts.block_collector import ArtifactBlockCollector
from workflow_pkg.artifacts.kind_resolver import ArtifactKindResolver
from workflow_pkg.artifacts.label_builder import ArtifactLabelBuilder
from workflow_pkg.artifacts.model import Artifact
from workflow_pkg.turns.models import Turn


class TurnArtifactExtractor:
    """Extract artifacts from one turn."""

    def extract(self, turn: Turn) -> list[Artifact]:
        """Return all artifacts found in a turn."""

        blocks = ArtifactBlockCollector().collect(turn.content)
        return [
            self._artifact(turn, ordinal, block)
            for ordinal, block in enumerate(blocks, start=1)
        ]

    def _artifact(self, turn: Turn, ordinal: int, block: tuple[int, int, str, str]) -> Artifact:
        """Build one artifact from a block match."""

        start, _end, language, content = block
        resolver = ArtifactKindResolver()
        kind = resolver.kind(language, content)
        label = ArtifactLabelBuilder().build(turn.content[:start], ordinal)
        return Artifact(turn.index, turn.speaker, turn.source, kind, resolver.extension(kind), ordinal, label, content.rstrip() + "\n")
