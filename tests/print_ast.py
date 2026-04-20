import json
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

md = MarkdownIt("gfm-like").enable("table")
text = "The user ⸢rev•username⸥ has requested to join."
root = SyntaxTreeNode(md.parse(text))

def tree_to_dict(n):
    is_root = getattr(n, "is_root", False)
    d = {
        "type": n.type,
        "tag": getattr(n, "tag", "") if not is_root else ""
    }
    if not is_root:
        content = getattr(n, "content", "")
        if content:
            d["content"] = content
            
    d["children"] = [tree_to_dict(c) for c in n.children]
    return d

print(json.dumps(tree_to_dict(root), indent=2))
