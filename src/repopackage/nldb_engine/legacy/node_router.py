from typing import Any, Dict
from markdown_it.tree import SyntaxTreeNode
from repopackage.nldb_engine.node_handler import (
    BaseNodeHandler, TextNodeHandler, TableNodeHandler, 
    CodeNodeHandler, ListNodeHandler
)
from repopackage.nldb_engine.template_handler import TemplateContract

class NodeRouter:
    def __init__(self):
        self.handlers = {
            "standard": TextNodeHandler(),
            "table": TableNodeHandler(),
            "code": CodeNodeHandler(),
            "list": ListNodeHandler()
        }

    def route(self, node: SyntaxTreeNode, contract: TemplateContract) -> BaseNodeHandler:
        if any(m.trait == "table" for m in contract.markers) or node.type == "table":
            return self.handlers["table"]
        if node.type == "fence":
            return self.handlers["code"]
        if node.type in ("bullet_list", "ordered_list"):
            return self.handlers["list"]
        
        return self.handlers["standard"]
