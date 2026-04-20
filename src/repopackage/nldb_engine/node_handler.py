import re
from typing import Tuple, List, Dict, Any, Type
from markdown_it.tree import SyntaxTreeNode
from abc import ABC, abstractmethod

class BaseNodeHandler(ABC):
    def get_text(self, node: SyntaxTreeNode) -> str:
        if getattr(node, "type", "") == "text": return getattr(node, "content", "")
        if getattr(node, "children", []): return "".join(self.get_text(c) for c in node.children)
        return getattr(node, "content", "") or ""

    @abstractmethod
    def compile_recipe(self, node: SyntaxTreeNode) -> List[Dict[str, Any]]:
        """Returns specific recipes to locate data inside this node boundary."""
        pass

    @abstractmethod
    def extract_data(self, node: SyntaxTreeNode, recipe: Dict[str, Any]) -> Dict[str, Any]:
        """Applies the recipe logic to extract data from this node boundary."""
        pass

class TextNodeHandler(BaseNodeHandler):
    """Handles standard GFM terminal leaf structures identically."""
    def compile_recipe(self, node: SyntaxTreeNode) -> List[Dict[str, Any]]:
        if getattr(node, "children", []): 
            return []
            
        content = getattr(node, "content", "")
        if not content or "⸢" not in content:
            return []
            
        pattern = r"⸢([^⸥]+)⸥"
        markers = []
        for match in re.finditer(pattern, content):
            inner = match.group(1)
            markers.append(inner.split("•", 1)[-1].strip() if "•" in inner else inner.strip()) 
                
        temp = re.sub(pattern, "[[PAYLOAD]]", content)
        regex_str = re.escape(temp).replace(re.escape("[[PAYLOAD]]"), "(.*?)")
        regex_str = f"^{regex_str}$"
        
        return [{"props": markers, "regex": regex_str, "handler": "text"}]

    def extract_data(self, node: SyntaxTreeNode, recipe: Dict[str, Any]) -> Dict[str, Any]:
        content = getattr(node, "content", "")
        if not content:
            return {}
            
        regex_pattern = re.compile(recipe["regex"])
        match = regex_pattern.search(content)
        if match:
            return {prop: match.group(i + 1).strip() for i, prop in enumerate(recipe["props"])}
        return {}

class TableNodeHandler(BaseNodeHandler):
    """Handles Table mapping logic."""
    def compile_recipe(self, node: SyntaxTreeNode) -> List[Dict[str, Any]]:
        tbody = next((c for c in node.children if c.type == "tbody"), None)
        if not tbody or not tbody.children: return []
        
        regex_map, props = {}, []
        for col_idx, td in enumerate(tbody.children[0].children):
            content = self.get_text(td)
            for match in re.finditer(r"⸢([^⸥]+)⸥", content):
                prop = match.group(1).split("•", 1)[-1].strip()
                props.append(prop)
                tmp = re.sub(r"⸢([^⸥]+)⸥", "[[PAYLOAD]]", content)
                rx = re.escape(tmp).replace(re.escape("[[PAYLOAD]]"), "(.*?)")
                regex_map[col_idx] = {"prop": prop, "regex": f"^{rx}$"}
                
        return [{"props": props, "regex_map": regex_map, "handler": "table"}] if props else []
        
    def extract_data(self, node: SyntaxTreeNode, recipe: Dict[str, Any]) -> Dict[str, Any]:
        tbody = next((c for c in node.children if c.type == "tbody"), None)
        results = {}
        if tbody:
            for tr in tbody.children:
                for col_idx, td in enumerate(tr.children):
                    if col_idx in recipe["regex_map"]:
                        rx = recipe["regex_map"][col_idx]
                        match = re.search(rx["regex"], self.get_text(td))
                        if match: results[rx["prop"]] = match.group(1).strip()
        return results

class ListNodeHandler(BaseNodeHandler):
    """Handles bullet_list and ordered_list mapping logic."""
    def compile_recipe(self, node: SyntaxTreeNode) -> List[Dict[str, Any]]:
        regex_map, props = [], []
        for li in node.children:
            content = self.get_text(li)
            for match in re.finditer(r"⸢([^⸥]+)⸥", content):
                prop = match.group(1).split("•", 1)[-1].strip()
                props.append(prop)
                tmp = re.sub(r"⸢([^⸥]+)⸥", "[[PAYLOAD]]", content)
                rx = re.escape(tmp).replace(re.escape("[[PAYLOAD]]"), "(.*?)")
                regex_map.append({"prop": prop, "regex": f"^{rx}$"})
                
        return [{"props": props, "regex_map": regex_map, "handler": "list"}] if props else []
        
    def extract_data(self, node: SyntaxTreeNode, recipe: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        for li in node.children:
            content = self.get_text(li)
            for rx in recipe["regex_map"]:
                match = re.search(rx["regex"], content)
                if match: results[rx["prop"]] = match.group(1).strip()
        return results

class SharedNodeHandler:
    """Factory router that intercepts AST structures traversing through extractors."""
    def __init__(self):
        self.handlers = {
            "text": TextNodeHandler(),
            "table": TableNodeHandler(),
            "list": ListNodeHandler()
        }

    def get_handler_for_node(self, node: SyntaxTreeNode) -> str:
        """Returns the handler key if a special block intercepts the dive, or text if terminal."""
        if node.type == "table":
            return "table"
        if node.type in ["bullet_list", "ordered_list"]:
            return "list"
        if not getattr(node, "children", []):
            return "text"
        return ""
