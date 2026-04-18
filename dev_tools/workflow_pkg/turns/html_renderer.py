"""Render HTML elements as markdown."""

from bs4 import NavigableString, Tag
from workflow_pkg.common.text import normalize_text

class HtmlMarkdownRenderer:
    """Convert supported HTML nodes to markdown."""

    def render(self, node: Tag | NavigableString) -> str:
        """Render one node recursively."""

        return (
            str(node)
            if isinstance(node, NavigableString)
            else HANDLERS.get(node.name.lower(), render_children)(node, self)
        )

    def render_element(self, element: Tag) -> str:
        """Render a full element and normalize it."""

        return normalize_text(self.render(element))


def render_children(node: Tag, renderer: HtmlMarkdownRenderer) -> str:
    """Render all children of a node."""

    return "".join(renderer.render(child) for child in node.children)


def render_break(_node: Tag, _renderer: HtmlMarkdownRenderer) -> str:
    """Render a line break."""

    return "\n"


def render_block(node: Tag, renderer: HtmlMarkdownRenderer) -> str:
    """Render a block container."""

    content = render_children(node, renderer).strip()
    return f"{content}\n\n" if content else ""


def render_code(node: Tag, renderer: HtmlMarkdownRenderer) -> str:
    """Render inline code."""

    return (
        render_pre(node.parent, renderer)
        if node.parent and node.parent.name == "pre"
        else f"`{node.get_text(strip=True)}`"
    )


def render_pre(node: Tag, _renderer: HtmlMarkdownRenderer) -> str:
    """Render fenced code blocks."""

    return f"\n```\n{node.get_text(chr(10)).rstrip()}\n```\n\n"


def render_link(node: Tag, renderer: HtmlMarkdownRenderer) -> str:
    """Render markdown links."""

    text = render_children(node, renderer).strip() or node.get("href", "")
    return f"[{text}]({node.get('href', '')})" if node.get("href") else text


HANDLERS = {
    "br": render_break,
    "pre": render_pre,
    "a": render_link,
    "code": render_code,
    "p": render_block,
    "div": render_block,
    "section": render_block,
    "article": render_block,
    "main": render_block,
    "header": render_block,
    "footer": render_block,
    "aside": render_block,
}
