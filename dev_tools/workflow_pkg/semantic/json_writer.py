"""JSON writer helpers for semantic output."""

from __future__ import annotations

import json
from pathlib import Path


class JsonWriter:
    """Write JSON files with stable formatting."""

    def write(self, path: Path, payload: dict) -> None:
        """Write one JSON payload to disk."""

        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )
