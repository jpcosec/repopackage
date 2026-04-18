"""Infer turn speaker from HTML attributes."""

from __future__ import annotations

import re

from bs4 import Tag


class HtmlSpeakerInference:
    """Infer user or assistant speaker labels."""

    def infer(self, element: Tag) -> str | None:
        """Return a speaker from DOM metadata."""

        haystack = self._attrs_text(element)
        if re.search(r"\b(user|query|prompt|human)\b", haystack):
            return "user"
        if re.search(r"\b(model|assistant|response|gemini|bard)\b", haystack):
            return "assistant"
        return None

    def _attrs_text(self, element: Tag) -> str:
        """Join element attributes into one lowercased string."""

        values: list[str] = []
        for value in element.attrs.values():
            values.extend(value if isinstance(value, list) else [str(value)])
        return " ".join(values).lower()
