"""Semantic evidence turn model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EvidenceTurn:
    """A turn record used by the semantic layer."""

    turn_id: str
    source_path: str
    speaker: str
    turn_path: str
    artifact_paths: list[str]
