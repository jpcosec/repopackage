from typing import Any, Dict
from markdown_it.tree import SyntaxTreeNode
from repopackage.nldb_engine.node_handler import BaseNodeHandler, TextNodeHandler, TableNodeHandler
from repopackage.nldb_engine.template_handler import TemplateContract

class NodeRouter:
    """Routes nodes based on instruction traits (table/dict) or AST type."""
    def __init__(self):
        self.handlers = {
            "standard": TextNodeHandler(),
            "table": TableNodeHandler()
        }

    def route(self, node: SyntaxTreeNode, contract: TemplateContract) -> BaseNodeHandler:
        # If any marker in the node specifies 'table', route to table handler
        if any(m.trait == "table" for m in contract.markers) or node.type == "table":
            return self.handlers["table"]
        
        return self.handlers["standard"]
