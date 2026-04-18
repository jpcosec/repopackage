"""Semantic evidence artifact model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EvidenceArtifact:
    """An artifact record used by the semantic layer."""

    artifact_id: str
    source_path: str
    extracted_path: str
    turn_id: str
    kind: str
    speaker: str
    label: str
