"""Artifact domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Artifact:
    """A structured artifact extracted from a turn."""

    turn_index: int
    speaker: str
    source: str
    kind: str
    extension: str
    ordinal: int
    label: str
    content: str
