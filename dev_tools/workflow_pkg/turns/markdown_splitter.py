"""Split assistant markdown segments into turns."""

import re
from workflow_pkg.common.text import normalize_text

class MarkdownUserSplitter:
    """Detect trailing user prompts after assistant text."""

    def split(self, lines: list[str]) -> tuple[list[str], list[str]]:
        """Return assistant lines and trailing user lines."""

        paragraphs = self._paragraphs(lines)
        user = self._tail_user(paragraphs)
        return (lines, []) if not user else self._partition(lines, user)

    def _paragraphs(self, lines: list[str]) -> list[list[str]]:
        """Split raw lines by blank lines."""

        text = "\n".join(lines).strip()
        return [
            chunk.splitlines() for chunk in re.split(r"\n\s*\n", text) if chunk.strip()
        ]

    def _tail_user(self, paragraphs: list[list[str]]) -> list[list[str]]:
        """Collect user-like trailing paragraphs."""

        user: list[list[str]] = []
        for paragraph in reversed(paragraphs):
            if self._strong(normalize_text("\n".join(paragraph))):
                user.insert(0, paragraph)
            elif user:
                break
        return user

    def _partition(
        self, lines: list[str], user: list[list[str]]
    ) -> tuple[list[str], list[str]]:
        """Partition raw lines using collected user paragraphs."""

        user_lines = [line for block in user for line in block + [""]]
        count = len(lines) - len(user_lines)
        return (lines, []) if count <= 0 else (lines[:count], lines[count:])

    def _strong(self, text: str) -> bool:
        """Detect strong user-prompt signals."""

        return is_strong_user_signal(text)


def is_strong_user_signal(text: str) -> bool:
    """Detect strong user-prompt signals."""

    return text.endswith("?") or _list_item(text) or _prefixed(text)


def _list_item(text: str) -> bool:
    """Detect numbered or bulleted prompts."""

    return re.match(r"^(\d+[-.)]|[-*])\s", text) is not None


def _prefixed(text: str) -> bool:
    """Detect common prompt prefixes."""

    return text.lower().startswith(PREFIXES)


PREFIXES = (
    "podrias",
    "podrías",
    "me ",
    "volvamos",
    "no,",
    "desde este",
    "perdon",
    "perdón",
)
