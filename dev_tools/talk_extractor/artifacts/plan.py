"""Planned artifact write model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from talk_extractor.artifacts.model import Artifact


@dataclass(slots=True)
class PlannedArtifact:
    """A planned artifact file write."""

    artifact: Artifact
    filename: str
    path: Path
