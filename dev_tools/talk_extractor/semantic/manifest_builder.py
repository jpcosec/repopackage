"""Manifest scaffold builder."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from talk_extractor.semantic.evidence_artifact import EvidenceArtifact
from talk_extractor.semantic.evidence_turn import EvidenceTurn


class ManifestBuilder:
    """Build the machine-readable semantic manifest."""

    def build(
        self,
        source_path: Path,
        turns: list[EvidenceTurn],
        artifacts: list[EvidenceArtifact],
    ) -> dict:
        """Return the manifest scaffold."""

        return {
            "topic": "TBD",
            "work_type": [],
            "source": self._source(source_path, turns, artifacts),
            "final_state": self._final_state(),
            "decisions": [],
            "artifacts": [asdict(item) for item in artifacts],
            "turns": [asdict(item) for item in turns],
        }

    def _source(
        self,
        source_path: Path,
        turns: list[EvidenceTurn],
        artifacts: list[EvidenceArtifact],
    ) -> dict:
        """Build the source summary."""

        return {
            "conversation": source_path.name,
            "turn_count": len(turns),
            "artifact_count": len(artifacts),
            "curated_artifact_count": 0,
        }

    def _final_state(self) -> dict:
        """Build the final-state scaffold."""

        return {
            "summary": "TBD",
            "accepted_decisions": [],
            "final_artifacts": [],
            "open_questions": [],
        }
