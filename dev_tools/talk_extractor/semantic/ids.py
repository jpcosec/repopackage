"""Semantic identifier helpers."""

from __future__ import annotations


class TurnIdFactory:
    """Build stable turn ids."""

    def build(self, index: int) -> str:
        """Return a zero-padded turn id."""

        return f"turn-{index:03d}"
