"""Shared types for agent adapters."""

from __future__ import annotations

from typing import Any, TypedDict


class NormalizedTurn(TypedDict):
    """Common schema for normalized turns."""

    timestamp: str
    speaker: str
    content: str
    tool_use: list[dict[str, Any]]
