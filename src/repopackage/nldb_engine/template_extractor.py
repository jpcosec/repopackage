import re
from typing import List, Dict, Tuple, Any
from markdown_it.tree import SyntaxTreeNode
from repopackage.nldb_engine.node_handler import SharedNodeHandler

class TemplateExtractor:
    """
    Extracts deterministic search recipes from the Template's block nodes. 
    It identifies exactly where markers live inside the block using SharedNodeHandler.
    """
    def __init__(self):
        self.node_handler = SharedNodeHandler()
        
    def extract_nodes(self, block_nodes: List[SyntaxTreeNode]) -> List[Dict[str, Any]]:
        extracted_recipes = []
        
        for outer_index, block_node in enumerate(block_nodes):
            outer_type = getattr(block_node, "type", "")
            
            def dive(node: SyntaxTreeNode, current_path: List[int]):
                # 1. Does this node trigger a special container handler? (e.g. Table)
                handler_key = self.node_handler.get_handler_for_node(node)
                
                if handler_key and handler_key != "text":
                    # Let the specialized handler digest this container completely!
                    handler_recipes = self.node_handler.handlers[handler_key].compile_recipe(node)
                    for r in handler_recipes:
                        r.update({
                            "outer_index": outer_index, 
                            "outer_type": outer_type,
                            "outer_tag": getattr(block_node, "tag", ""),
                            "inner_path": current_path
                        })
                        extracted_recipes.append(r)
                    return # DO NOT dive deeper into this specialized block naturally
                    
                # 2. Otherwise apply literal leaf mapping if it's terminal
                if handler_key == "text":
                    literal_recipes = self.node_handler.handlers["text"].compile_recipe(node)
                    for r in literal_recipes:
                        r.update({
                            "outer_index": outer_index, 
                            "outer_type": outer_type,
                            "outer_tag": getattr(block_node, "tag", ""),
                            "inner_path": current_path
                        })
                        extracted_recipes.append(r)
                        
                for child_idx, child in enumerate(node.children):
                    dive(child, current_path + [child_idx])
                    
            dive(block_node, [])
            
        return extracted_recipes
