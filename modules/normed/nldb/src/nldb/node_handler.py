import re
from typing import Tuple, List, Dict, Any, Type
from markdown_it.tree import SyntaxTreeNode
from abc import ABC, abstractmethod

class BaseNodeHandler(ABC):
    def __init__(self, router=None):
        """Allows specialized handlers to recursively delegate to standard extractors."""
        self.router = router

    def get_text(self, node: SyntaxTreeNode) -> str:
        if getattr(node, "type", "") == "text": return getattr(node, "content", "")
        if getattr(node, "children", []): return "".join(self.get_text(c) for c in node.children)
        return getattr(node, "content", "") or ""

    @abstractmethod
    def compile_recipe(self, node: SyntaxTreeNode) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def extract_data(self, node: SyntaxTreeNode, recipe: Dict[str, Any]) -> Any:
        pass

class TextNodeHandler(BaseNodeHandler):
    """Handles standard GFM terminal leaf structures identically."""
    def compile_recipe(self, node: SyntaxTreeNode) -> List[Dict[str, Any]]:
        if getattr(node, "children", []): 
            return []

        content = getattr(node, "content", "").strip()
        if not content or "⸢" not in content:
            return []

        pattern = r"⸢([^⸥]+)⸥"
        markers_info = []
        for match in re.finditer(pattern, content):
            inner = match.group(1)
            traits = inner.split(",") if "," in inner.split("•")[0] else []
            prop = inner.split("•", 1)[-1].strip() if "•" in inner else inner.strip()
            markers_info.append({"name": prop, "traits": [t.strip() for t in traits]})

        temp = re.sub(pattern, "[[PAYLOAD]]", content)
        regex_str = re.escape(temp).replace(re.escape("[[PAYLOAD]]"), "(.*?)")
        regex_str = f"^{regex_str}$"

        return [{"props": [m["name"] for m in markers_info], "props_info": markers_info, "regex": regex_str, "handler": "text"}]

    def extract_data(self, node: SyntaxTreeNode, recipe: Dict[str, Any]) -> Dict[str, Any]:
        content = getattr(node, "content", "").strip()
        if not content:
            return {}
            
        regex_pattern = re.compile(recipe["regex"])
        match = regex_pattern.match(content)
        if match:
            results = {}
            if "props_info" not in recipe:
                return {}
            for i, info in enumerate(recipe["props_info"]):
                val = match.group(i + 1).strip()
                traits = info["traits"]
                if "dict" in traits or "json" in traits:
                    import yaml
                    try: val = yaml.safe_load(val)
                    except: pass
                elif "list" in traits or (val.startswith("[") and val.endswith("]")):
                    clean_val = val.strip("`").strip()
                    if clean_val.startswith("[") and clean_val.endswith("]"):
                        import json
                        try: val = json.loads(clean_val.replace("'", '"'))
                        except:
                            inner = clean_val[1:-1].strip()
                            val = [i.strip() for i in inner.split("|")] if inner else []
                results[info["name"]] = val
            return results
        return {}

class YamlNodeHandler(BaseNodeHandler):
    """Handles YAML blocks (frontmatter or fences) natively."""
    def compile_recipe(self, node: SyntaxTreeNode) -> List[Dict[str, Any]]:
        content = getattr(node, "content", "").strip()
        if not content or "⸢" not in content:
            return []
        pattern = r"⸢([^⸥]+)⸥"
        match = re.search(pattern, content)
        if match:
            inner = match.group(1)
            prop = inner.split("•", 1)[-1].strip() if "•" in inner else inner.strip()
            return [{"props": [prop], "handler": "yaml"}]
        return []

    def extract_data(self, node: SyntaxTreeNode, recipe: Dict[str, Any]) -> Dict[str, Any]:
        content = getattr(node, "content", "").strip()
        if not content: return {}
        import yaml
        try:
            data = yaml.safe_load(content)
            if recipe["props"]: return {recipe["props"][0]: data}
        except: pass
        return {}

class TableNodeHandler(BaseNodeHandler):
    """Handles Table iterative generation via 2-step block and inner-node scanning."""
    def compile_recipe(self, node: SyntaxTreeNode) -> List[Dict[str, Any]]:
        tbody = next((c for c in node.children if c.type == "tbody"), None)
        if not tbody or not tbody.children: return []
        regex_map, all_props = {}, []
        for col_idx, td in enumerate(tbody.children[0].children):
            content = self.get_text(td)
            col_props = []
            for match in re.finditer(r"⸢([^⸥]+)⸥", content):
                prop = match.group(1).split("•", 1)[-1].strip()
                col_props.append(prop)
                all_props.append(prop)
            if col_props:
                tmp = re.sub(r"⸢([^⸥]+)⸥", "[[PAYLOAD]]", content)
                rx = re.escape(tmp).replace(re.escape("[[PAYLOAD]]"), "(.*?)")
                regex_map[col_idx] = {"props": col_props, "regex": f"^{rx}$"}
        return [{"props": all_props, "regex_map": regex_map, "handler": "table"}] if all_props else []
        
    def extract_data(self, node: SyntaxTreeNode, recipe: Dict[str, Any]) -> Dict[int, Dict[str, str]]:
        tbody = next((c for c in node.children if c.type == "tbody"), None)
        result_array = {}
        if not tbody: return result_array
        for row_index, tr in enumerate(tbody.children):
            row_data = {}
            for col_idx, td in enumerate(tr.children):
                if col_idx in recipe["regex_map"]:
                    rx_data = recipe["regex_map"][col_idx]
                    match = re.search(rx_data["regex"], self.get_text(td))
                    if match: 
                        for i, p in enumerate(rx_data["props"]):
                            row_data[p] = match.group(i + 1).strip()
            if row_data: result_array[row_index] = row_data
        return {recipe["props"][0]: result_array}

class ListNodeHandler(BaseNodeHandler):
    """Handles dynamic array N-length iterations cleanly for Lists via 2-step block checks."""
    def compile_recipe(self, node: SyntaxTreeNode) -> List[Dict[str, Any]]:
        if not node.children: return []
        content = self.get_text(node.children[0])
        props = []
        for match in re.finditer(r"⸢([^⸥]+)⸥", content):
            props.append(match.group(1).split("•", 1)[-1].strip())
        if not props: return []
        tmp = re.sub(r"⸢([^⸥]+)⸥", "[[PAYLOAD]]", content)
        rx = re.escape(tmp).replace(re.escape("[[PAYLOAD]]"), "(.*?)")
        return [{"props": props, "regex": f"^{rx}$", "handler": "list"}]
        
    def extract_data(self, node: SyntaxTreeNode, recipe: Dict[str, Any]) -> Dict[str, List[str]]:
        results_array = []
        regex_pattern = re.compile(recipe["regex"])
        for li in node.children:
            content = self.get_text(li)
            item_data = {}
            match = regex_pattern.search(content)
            if match:
                for i, p in enumerate(recipe["props"]):
                    item_data[p] = match.group(i + 1).strip()
            if item_data:
                results_array.append(item_data[recipe["props"][0]] if len(recipe["props"]) == 1 else item_data)
        if recipe["props"]: return {recipe["props"][0]: results_array}
        return {}

class SharedNodeHandler:
    """Factory router that intercepts AST structures traversing through extractors."""
    def __init__(self):
        self.handlers = {"text": TextNodeHandler(self), "table": TableNodeHandler(self), "list": ListNodeHandler(self), "yaml": YamlNodeHandler(self)}
    def get_handler_for_node(self, node: SyntaxTreeNode) -> str:
        if node.type == "table": return "table"
        if node.type in ["bullet_list", "ordered_list"]: return "list"
        if node.type in ["front_matter", "fence"]: return "yaml"
        if not getattr(node, "children", []): return "text"
        return ""
