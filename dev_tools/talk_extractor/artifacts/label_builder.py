"""Artifact label generation."""

from __future__ import annotations

import re

from talk_extractor.artifacts.rules import ArtifactRules
from talk_extractor.common.slugs import slugify
from talk_extractor.common.text import normalize_text


class ArtifactLabelBuilder:
    """Build readable artifact file labels."""

    def build(self, prefix: str, ordinal: int) -> str:
        """Return a label from nearby context or fallback ordinal."""

        return self._candidate(prefix) or f"{ordinal:02d}"

    def _candidate(self, prefix: str) -> str:
        """Return the best candidate slug from the prefix."""

        for line in reversed(prefix.splitlines()[-8:]):
            cleaned = self._clean(line)
            if cleaned and cleaned.lower() not in ArtifactRules().generic_labels():
                return self._short(cleaned)
        return ""

    def _clean(self, text: str) -> str:
        """Remove markdown list and heading markers."""

        text = normalize_text(text)
        text = re.sub(r"^#{1,6}\s+", "", text)
        text = re.sub(r"^[\-*+]\s+", "", text)
        text = re.sub(r"^\d+[-.)]\s+", "", text)
        return text.strip("`*_ :.-")

    def _short(self, text: str) -> str:
        """Clamp long slugs to a readable size."""

        slug = slugify(text)
        return slug if len(slug) <= 72 else slug[:72].rstrip("-")
