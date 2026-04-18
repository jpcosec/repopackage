"""Extract turns from static Gemini HTML."""

from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup

from workflow_pkg.turns.deduper import TurnDeduper
from workflow_pkg.turns.html_candidates import HtmlCandidateFinder
from workflow_pkg.turns.html_renderer import HtmlMarkdownRenderer
from workflow_pkg.turns.html_speaker import HtmlSpeakerInference
from workflow_pkg.turns.models import Turn


class HtmlTurnExtractor:
    """Extract conversation turns from HTML files."""

    def extract(self, path: str | Path) -> list[Turn]:
        """Return deduplicated turns from an HTML file."""

        path = Path(path)
        soup = BeautifulSoup(
            path.read_text(encoding="utf-8", errors="ignore"), "html.parser"
        )
        turns = self._turns_from_soup(soup, path.name)
        return TurnDeduper().dedupe(turns)

    def _turns_from_soup(self, soup: BeautifulSoup, source: str) -> list[Turn]:
        """Build turns from candidate elements."""

        turns: list[Turn] = []
        for element in HtmlCandidateFinder().find(soup):
            self._append_turn(turns, element, source)
        return turns

    def _append_turn(self, turns: list[Turn], element, source: str) -> None:
        """Append one HTML-derived turn if possible."""

        speaker = HtmlSpeakerInference().infer(element)
        if speaker:
            content = HtmlMarkdownRenderer().render_element(element)
            turns.append(Turn(len(turns) + 1, speaker, content, source))
