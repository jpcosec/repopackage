"""Artifact kind resolution."""

from __future__ import annotations

from talk_extractor.artifacts.kind_checks import infer_kind
from talk_extractor.artifacts.rules import ArtifactRules
from talk_extractor.common.slugs import slugify


class ArtifactKindResolver:
    """Resolve artifact kinds and output extensions."""

    def kind(self, language: str, content: str) -> str:
        """Return the artifact kind for a block."""

        return self._aliased(language) or infer_kind(content.strip())

    def extension(self, kind: str) -> str:
        """Return the preferred extension for a kind."""

        return ArtifactRules().extensions().get(kind, "txt")

    def _aliased(self, language: str) -> str:
        """Normalize language aliases."""

        return ArtifactRules().aliases().get(slugify(language).replace("-", ""), "")
