import re, ast
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type, Optional
from markdown_it.tree import SyntaxTreeNode
from repopackage.nldb_engine.template_handler import TemplateContract

class BaseNodeHandler(ABC):
    @abstractmethod
    def render(self, template: TemplateContract, payload: Any, fields: Dict[str, Any]) -> str: pass
    
    @abstractmethod
    def extract(self, node: SyntaxTreeNode, template: TemplateContract, model_cls: Type[Any]) -> Dict[str, Any]: pass

    def get_text(self, node: SyntaxTreeNode) -> str:
        if node.type == "text": return node.content
        if node.type == "inline": return "".join(self.get_text(c) for c in node.children)
        if node.children: return "".join(self.get_text(c) for c in node.children)
        return node.content or ""

class TextNodeHandler(BaseNodeHandler):
    def render(self, template: TemplateContract, payload: Any, fields: Dict[str, Any]) -> str:
        out = template.raw
        for marker in template.markers:
            # Handle View traits (jinja2, python)
            if marker.mode == "jinja2":
                 # Logic for Jinja...
                 pass
            
            # Get value from fields
            val = fields.get(marker.prop, f"⸢{marker.prop}⸥")
            out = out.replace(marker.raw, str(val))
        return out

    def extract(self, node: SyntaxTreeNode, template: TemplateContract, model_cls: Type[Any]) -> Dict[str, Any]:
        text = self.get_text(node).strip()
        regex = re.escape(template.get_clean_pattern()).replace(re.escape("[[PAYLOAD]]"), "(.*?)")
        match = re.search(regex, text, re.DOTALL)
        results = {}
        if match:
            for i, marker in enumerate(template.markers):
                if marker.mode in ("rev", "revop"):
                    val = match.group(i + 1).strip()
                    try: results[marker.prop] = ast.literal_eval(val)
                    except: results[marker.prop] = val
        return results

class TableNodeHandler(BaseNodeHandler):
    def render(self, template: TemplateContract, payload: List[Dict[str, Any]], fields: Dict[str, Any]) -> str:
        if not payload: return ""
        headers = list(payload[0].keys())
        rows = ["| " + " | ".join(str(r.get(h, "")) for h in headers) + " |" for r in payload]
        return "| " + " | ".join(headers) + " |\n| " + " | ".join(["---"]*len(headers)) + " |\n" + "\n".join(rows)

    def extract(self, node: SyntaxTreeNode, template: TemplateContract, model_cls: Type[Any]) -> Dict[str, Any]:
        # Implementation logic for table extraction...
        return {}
