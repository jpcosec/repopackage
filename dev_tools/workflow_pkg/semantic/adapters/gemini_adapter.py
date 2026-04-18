"""Gemini adapter for normalizing logs."""

from __future__ import annotations

from pathlib import Path
from workflow_pkg.semantic.adapters.adapter_types import NormalizedTurn


class GeminiAdapter:
    """Normalizes Gemini-style raw logs."""

    def normalize(self, raw_path: Path) -> list[NormalizedTurn]:
        """Normalize raw log file into common schema."""

        # Stub implementation
        return [
            {
                "timestamp": "2024-01-01T00:00:00Z",
                "speaker": "assistant",
                "content": "Gemini stub content.",
                "tool_use": [],
            }
        ]
