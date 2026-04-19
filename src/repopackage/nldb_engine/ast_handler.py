from typing import List, Tuple, Dict, Any
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

class AstPairingEngine:
    """Orchestrates AST parsing and alignments between two Markdown sources."""
    def __init__(self):
        self.md = MarkdownIt("gfm-like").enable("table")

    def get_nodes(self, raw: str) -> List[SyntaxTreeNode]:
        """Converts raw text to top-level AST nodes."""
        return SyntaxTreeNode(self.md.parse(raw)).children

    def pair_trees(self, template_dsl: str, data_markdown: str) -> List[Tuple[SyntaxTreeNode, SyntaxTreeNode]]:
        """
        Aligns nodes from the template with nodes from the document.
        Ensures that the 1st paragraph in template matches the 1st paragraph in data.
        """
        tpl_nodes = self.get_nodes(template_dsl)
        doc_nodes = self.get_nodes(data_markdown)
        
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
            
            # Match by signature and physical order
            if sig in doc_registry and idx < len(doc_registry[sig]):
                pairs.append((t_node, doc_registry[sig][idx]))
        
        return pairs
