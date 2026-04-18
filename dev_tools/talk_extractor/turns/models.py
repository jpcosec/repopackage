"""Turn domain model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Turn:
    """A single conversation turn."""

    index: int
    speaker: str
    content: str
    source: str
