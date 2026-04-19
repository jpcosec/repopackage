"""Write semantic scaffolds to disk."""

from __future__ import annotations

from pathlib import Path

from talk_extractor.semantic.decisions_scaffold import DecisionsScaffoldBuilder
from talk_extractor.semantic.specs_scaffold import SpecsScaffoldBuilder
from talk_extractor.semantic.timeline_scaffold import TimelineScaffoldBuilder
from talk_extractor.semantic.turn_scaffold import TurnScaffoldBuilder
from talk_extractor.turns.models import Turn


class SemanticScaffoldWriter:
    """Materialize semantic markdown scaffolds."""

    def write_root(
        self, semantic_dir: Path, turns: list[Turn], mapping: dict[str, list[str]]
    ) -> None:
        """Write root semantic scaffold files."""

        (semantic_dir / "specs.md").write_text(
            SpecsScaffoldBuilder().build(), encoding="utf-8"
        )
        (semantic_dir / "decisions.md").write_text(
            DecisionsScaffoldBuilder().build(), encoding="utf-8"
        )
        (semantic_dir / "timeline.md").write_text(
            TimelineScaffoldBuilder().build(turns, mapping), encoding="utf-8"
        )

    def write_turns(
        self, turn_dir: Path, turns: list[Turn], mapping: dict[str, list[str]]
    ) -> None:
        """Write per-turn semantic scaffold files."""

        builder = TurnScaffoldBuilder()
        for turn in turns:
            tid = f"turn-{turn.index:03d}"
            path = turn_dir / f"{tid}.md"
            path.write_text(builder.build(turn, mapping.get(tid, [])), encoding="utf-8")
