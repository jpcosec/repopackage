"""Turn document writer."""

from __future__ import annotations

from pathlib import Path

from talk_extractor.common.slugs import slugify
from talk_extractor.turns.models import Turn


class TurnDocumentWriter:
    """Write each turn to a standalone markdown file."""

    def write_all(self, turns: list[Turn], output_dir: str | Path) -> list[Path]:
        """Write turn documents and return their paths."""

        directory = Path(output_dir)
        directory.mkdir(parents=True, exist_ok=True)
        return [self._write_turn(turn, directory) for turn in turns]

    def _write_turn(self, turn: Turn, directory: Path) -> Path:
        """Write one turn document."""

        path = directory / self._filename(turn)
        path.write_text(self._body(turn), encoding="utf-8")
        return path

    def _filename(self, turn: Turn) -> str:
        """Build a turn file name."""

        return f"turn-{turn.index:03d}-{slugify(turn.speaker)}.md"

    def _body(self, turn: Turn) -> str:
        """Build markdown content for one turn."""

        return (
            f"# Turn {turn.index:03d} - {turn.speaker}\n\n"
            f"- Source: `{turn.source}`\n- Speaker: `{turn.speaker}`\n\n"
            f"{turn.content.rstrip()}\n"
        )
