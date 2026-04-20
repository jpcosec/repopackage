from typing import List, Tuple, Dict, Any
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

class AstPairingEngine:
    def __init__(self):
        self.md = MarkdownIt("gfm-like").enable("table")

    def get_all_nodes(self, raw: str) -> List[SyntaxTreeNode]:
        """Flattens the entire AST into a deterministic sequence of nodes."""
        tokens = self.md.parse(raw)
        root = SyntaxTreeNode(tokens)
        nodes = []
        def walk(n):
            if not n.is_root: nodes.append(n)
            for c in n.children: walk(c)
        walk(root)
        return nodes

    def pair_trees(self, template_dsl: str, data_markdown: str) -> List[Tuple[SyntaxTreeNode, SyntaxTreeNode]]:
        """Aligns every node in the template with its corresponding node in the data."""
        tpl_nodes = self.get_all_nodes(template_dsl)
        doc_nodes = self.get_all_nodes(data_markdown)
        
        # Index document nodes by signature
        doc_registry: Dict[str, List[SyntaxTreeNode]] = {}
        for n in doc_nodes:
            sig = f"{n.type}_{n.tag}"
            doc_registry.setdefault(sig, []).append(n)
        
        pairs = []
        usage_counters = {}
        for t_node in tpl_nodes:
            sig = f"{t_node.type}_{t_node.tag}"
            usage_counters[sig] = usage_counters.get(sig, -1) + 1
            idx = usage_counters[sig]
            
            if sig in doc_registry and idx < len(doc_registry[sig]):
                pairs.append((t_node, doc_registry[sig][idx]))
        return pairs
