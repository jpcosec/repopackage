import re, ast
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type, Optional, get_origin
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
            val = fields.get(marker.prop, f"⸢{marker.prop}⸥")
            out = out.replace(marker.raw, str(val))
        return out

    def extract(self, node: SyntaxTreeNode, template: TemplateContract, model_cls: Type[Any]) -> Dict[str, Any]:
        text = self.get_text(node).strip()
        # Non-greedy regex mask
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
    def render(self, template: TemplateContract, payload: Any, fields: Dict[str, Any]) -> str:
        marker = next(m for m in template.markers if m.trait == "table")
        data = fields.get(marker.prop, [])
        if not data: return ""
        recs = [r.model_dump() if hasattr(r, "model_dump") else r for r in data]
        h = list(recs[0].keys())
        rows = ["| " + " | ".join(str(r.get(x, "")) for x in h) + " |" for r in recs]
        return "| " + " | ".join(h) + " |\n| " + " | ".join(["---"]*len(h)) + " |\n" + "\n".join(rows)

    def extract(self, node: SyntaxTreeNode, template: TemplateContract, model_cls: Type[Any]) -> Dict[str, Any]:
        marker = next(m for m in template.markers if m.trait == "table")
        tbody = next((c for c in node.children if c.type == "tbody"), None)
        thead = next((c for c in node.children if c.type == "thead"), None)
        # Search deeper if needed (for nested tables)
        if not thead or not tbody:
             for c in node.children:
                  res = self.extract(c, template, model_cls)
                  if res: return res
             return {}
        
        headers = [self.get_text(th).strip() for th in thead.children[0].children]
        records = []
        for tr in tbody.children:
            row = {}
            for i, td in enumerate(tr.children):
                if i < len(headers):
                    v = self.get_text(td).strip()
                    try: row[headers[i]] = ast.literal_eval(v)
                    except: row[headers[i]] = v
            records.append(row)
        return {marker.prop: records}

class CodeNodeHandler(BaseNodeHandler):
    def render(self, template: TemplateContract, payload: Any, fields: Dict[str, Any]) -> str:
        marker = template.markers[0]
        val = fields.get(marker.prop, "")
        return f"```python\n{val}\n```"

    def extract(self, node: SyntaxTreeNode, template: TemplateContract, model_cls: Type[Any]) -> Dict[str, Any]:
        marker = template.markers[0]
        return {marker.prop: node.content.strip()}

class ListNodeHandler(BaseNodeHandler):
    def render(self, template: TemplateContract, payload: Any, fields: Dict[str, Any]) -> str:
        return TextNodeHandler().render(template, payload, fields)
    def extract(self, node: SyntaxTreeNode, template: TemplateContract, model_cls: Type[Any]) -> Dict[str, Any]:
        return TextNodeHandler().extract(node, template, model_cls)
