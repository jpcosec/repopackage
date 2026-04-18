"""Turn extraction service."""

from __future__ import annotations

from pathlib import Path

from talk_extractor.turns.html_extractor import HtmlTurnExtractor
from talk_extractor.turns.markdown_extractor import MarkdownTurnExtractor
from talk_extractor.turns.models import Turn
from talk_extractor.turns.writer import TurnDocumentWriter


class TurnExtractionService:
    """Route extraction by file type and write turn files."""

    def extract(self, path: str | Path) -> list[Turn]:
        """Extract turns from a supported file."""

        path = Path(path)
        return self._from_html(path) or self._from_markdown(path)

    def write(
        self, source_path: str | Path, output_dir: str | Path = "extracted talk"
    ) -> list[Path]:
        """Extract turns and write them to disk."""

        return TurnDocumentWriter().write_all(self.extract(source_path), output_dir)

    def _from_html(self, path: Path) -> list[Turn]:
        """Try HTML extraction when applicable."""

        return (
            HtmlTurnExtractor().extract(path)
            if path.suffix.lower() in {".html", ".htm"}
            else []
        )

    def _from_markdown(self, path: Path) -> list[Turn]:
        """Use markdown extraction when supported."""

        kinds = {".md", ".markdown", ".txt", ".html", ".htm"}
        return (
            MarkdownTurnExtractor().extract(path)
            if path.suffix.lower() in kinds
            else self._unsupported(path)
        )

    def _unsupported(self, path: Path) -> list[Turn]:
        """Raise for unsupported file types."""

        raise ValueError(f"Unsupported file type: {path.suffix}")
