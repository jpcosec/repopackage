"""Text normalization helpers."""

from __future__ import annotations

import re


class TextNormalizer:
    """Normalize plain text for extraction flows."""

    def normalize(self, text: str) -> str:
        """Return a compact normalized text string."""

        text = self._normalize_newlines(text)
        text = self._normalize_spaces(text)
        return self._collapse_breaks(text).strip()

    def _normalize_newlines(self, text: str) -> str:
        """Normalize line endings and nbsp characters."""

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")
        return text.replace("\u00a0", " ")

    def _normalize_spaces(self, text: str) -> str:
        """Trim trailing spaces before line breaks."""

        return re.sub(r"[ \t]+\n", "\n", text)

    def _collapse_breaks(self, text: str) -> str:
        """Reduce repeated blank lines."""

        return re.sub(r"\n{3,}", "\n\n", text)


def normalize_text(text: str) -> str:
    """Expose a small functional entrypoint."""

    return TextNormalizer().normalize(text)
