import re
from typing import List, Dict, Any
from markdown_it.tree import SyntaxTreeNode
from repopackage.nldb_engine.node_handler import SharedNodeHandler

class DataExtractor:
    """
    Applies compiled template recipes to a parsed Markdown Data Document 
    to robustly recover the payload values using sequential block cursor.
    """
    def __init__(self):
        self.node_handler = SharedNodeHandler()
        
    def extract_values(self, data_blocks: List[SyntaxTreeNode], recipes: List[Dict[str, Any]]) -> Dict[str, Any]:
        extracted_data = {}
        search_index = 0  # Sequential cursor guarantees we don't map backwards
        
        for recipe in recipes:
            target_type = recipe["outer_type"]
            target_tag = recipe.get("outer_tag", "")
            handler_key = recipe.get("handler", "text")
            
            # Scan structural top-level blocks STRICTLY moving forward
            for block_idx in range(search_index, len(data_blocks)):
                block = data_blocks[block_idx]
                
                # Metadata Uniqueness Pass (e.g. heading vs paragraph vs h1 vs h2)
                if getattr(block, "type", "") != target_type:
                    continue
                if getattr(block, "tag", "") != target_tag:
                    continue
                    
                current_node = block
                
                if handler_key == "text":
                    valid_path = True
                    for child_idx in recipe.get("inner_path", []):
                        try:
                            current_node = current_node.children[child_idx]
                        except IndexError:
                            valid_path = False
                            break
                    if not valid_path:
                        continue
                    
                # Delegate extraction logic to the assigned factory handler
                values = self.node_handler.handlers[handler_key].extract_data(current_node, recipe)
                
                if values:
                    extracted_data.update(values)
                    search_index = block_idx  # Ensure we don't jump out of the container for adjacent recipes
                    break # Match achieved; move to next recipe
                    
        return extracted_data
