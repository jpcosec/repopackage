"""Slug generation helpers."""

from __future__ import annotations

import re
import unicodedata


class Slugifier:
    """Create filesystem-safe slugs."""

    def slugify(self, value: str) -> str:
        """Return a normalized ASCII slug."""

        value = self._strip_accents(value)
        value = value.lower()
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-") or "turn"

    def _strip_accents(self, value: str) -> str:
        """Remove non-ASCII accents."""

        value = unicodedata.normalize("NFKD", value)
        return value.encode("ascii", "ignore").decode("ascii")


def slugify(value: str) -> str:
    """Expose a small functional entrypoint."""

    return Slugifier().slugify(value)
