from markdown_it import MarkdownIt

md = MarkdownIt("gfm-like").enable("table")

markdown_text = """
* ⸢rev|list•items⸥

| Col 1 | Col 2 |
| ----- | ----- |
| ⸢rev|table•col1⸥ | ⸢rev|table•col2⸥ |
"""

tokens = md.parse(markdown_text)

def print_tree(tokens, level=0):
    for t in tokens:
        print("  " * level + f"Type: {t.type} | Tag: {t.tag} | Content: {repr(t.content)}")
        if getattr(t, "children", None):
            print_tree(t.children, level + 1)

print_tree(tokens)
