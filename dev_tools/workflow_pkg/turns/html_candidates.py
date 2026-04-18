"""HTML turn candidate discovery."""

from __future__ import annotations

from bs4 import BeautifulSoup, Tag

from workflow_pkg.common.text import normalize_text


SELECTORS = [
    "[data-message-id]",
    "[data-turn-id]",
    "[data-testid*='message']",
    "[data-testid*='response']",
    "[data-testid*='prompt']",
    "[class*='message']",
    "[class*='response']",
    "[class*='prompt']",
    "[class*='query']",
    "main article",
    "main section",
    "main div",
]


class HtmlCandidateFinder:
    """Find candidate message elements in Gemini HTML."""

    def find(self, soup: BeautifulSoup) -> list[Tag]:
        """Return unique candidate elements."""

        found: list[Tag] = []
        seen: set[int] = set()
        for selector in SELECTORS:
            self._collect_selector(soup, selector, found, seen)
        return found

    def _collect_selector(
        self, soup: BeautifulSoup, selector: str, found: list[Tag], seen: set[int]
    ) -> None:
        """Collect one selector into the result list."""

        for element in soup.select(selector):
            if id(element) not in seen and self._valid(element):
                seen.add(id(element))
                found.append(element)

    def _valid(self, element: Tag) -> bool:
        """Filter obvious noise elements."""

        text = normalize_text(element.get_text("\n", strip=True))
        return (
            len(text) >= 20
            and len(text.split()) >= 3
            and text.lower() not in {"google gemini", "cuenta de google"}
        )
