import re
from typing import Dict, Any, Type, TypeVar, ClassVar, List, Tuple, get_origin
from pydantic import BaseModel, Field, ConfigDict
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from jinja2 import Template as JinjaTemplate

M = TypeVar("M", bound="StructuredNLDoc")

class StructuredNLDoc(BaseModel):
    """
    Base class for all Natural Language Documents.
    Requires a __template__ ClassVar using ⸢ ⸥ delimiters.
    """
    model_config = ConfigDict(protected_namespaces=())
    __template__: ClassVar[str] = ""

def validate_template_contract(cls: Type[M]) -> None:
    """Ensures the template satisfies the Pydantic model contract."""
    template = getattr(cls, "__template__", "")
    if not template:
        raise ValueError(f"Class {cls.__name__} is missing a __template__ definition.")
        
    rev_markers = re.findall(r"⸢rev\|(?:table\||dict\|)?([^⸥]+)⸥", template)
    revop_markers = re.findall(r"⸢revop\|(?:table\||dict\|)?([^⸥]+)⸥", template)
    
    all_rev = rev_markers + revop_markers
    if len(all_rev) != len(set(all_rev)):
        raise ValueError(f"Duplicate reversible fields in {cls.__name__}: {all_rev}")

    model_fields = cls.model_fields
    required_fields = [name for name, field in model_fields.items() if field.is_required()]
    for rf in required_fields:
        if rf not in all_rev:
            raise ValueError(f"Required field '{rf}' is missing from template.")

def compile_template_ast(markdown_dsl: str) -> List[Dict[str, Any]]:
    """Compiles a Markdown DSL into an AST-based extraction mask."""
    md = MarkdownIt("gfm-like").enable("table")
    ast_root = SyntaxTreeNode(md.parse(markdown_dsl))
    config = []

    def walk(node: SyntaxTreeNode, path: List[Dict[str, Any]] = []):
        if not node.is_root:
            sig = f"{node.type}_{node.tag}" if node.tag else node.type
            parent = node.parent
            siblings = [c for c in parent.children if (f"{c.type}_{c.tag}" if getattr(c, 'tag', None) else c.type) == sig] if parent else []
            type_index = siblings.index(node) if node in siblings else 0
            
            current_step = {"sig": sig, "idx": type_index}
            new_path = path + [current_step]

            content = node.content or ""
            matches = re.findall(r"⸢(rev|revop)\|(table\||dict\|)?([^⸥]+)⸥", content)
            
            for mode, trait, prop_name in matches:
                config.append({
                    "prop": prop_name,
                    "mode": mode,
                    "trait": trait.strip("|") if trait else None,
                    "path": new_path.copy(),
                    "pattern": content
                })
        else:
            new_path = path

        for child in node.children:
            walk(child, new_path)

    walk(ast_root)
    return config

def render_table_records(data: Any) -> str:
    """Converts records or indexed dict to GFM table."""
    if isinstance(data, dict):
        records = [{"key": k, **(v if isinstance(v, dict) else {"value": v})} for k, v in data.items()]
    elif hasattr(data, "__iter__"):
        records = [r.model_dump() if hasattr(r, "model_dump") else r for r in data]
    else:
        records = []

    if not records: return ""
    headers = list(records[0].keys())
    header_line = "| " + " | ".join(headers) + " |"
    sep_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    rows = ["| " + " | ".join(str(r.get(h, "")) for h in headers) + " |" for r in records]
    return "\n".join([header_line, sep_line] + rows)

def render_dict_records(data: Dict[str, Any]) -> str:
    """Converts a dict to a bullet list (Key : Value)."""
    return "\n".join([f"- {k} : {v}" for k, v in data.items()])

def parse_table_node(node: SyntaxTreeNode) -> List[Dict[str, Any]]:
    """Parses table node to records."""
    thead = next((c for c in node.children if c.type == "thead"), None)
    tbody = next((c for c in node.children if c.type == "tbody"), None)
    if not thead or not tbody: return []
    headers = [th.children[0].content.strip() for th in thead.children[0].children]
    records = []
    for tr in tbody.children:
        records.append({headers[i]: td.children[0].content.strip() for i, td in enumerate(tr.children) if i < len(headers)})
    return records

def parse_dict_node(node: SyntaxTreeNode) -> Dict[str, Any]:
    """Parses a bullet list into a dict."""
    result = {}
    for li in node.children:
        try:
            text = li.children[0].children[0].content.strip()
            if " : " in text:
                k, v = text.split(" : ", 1)
                result[k.strip()] = v.strip()
        except: continue
    return result

def split_doc_components(instance: StructuredNLDoc) -> tuple[Dict[str, Any], str]:
    """Internal helper to split model and template."""
    validate_template_contract(type(instance))
    fields = instance.model_dump()
    template = getattr(instance, "__template__", "")
    return fields, template

def render_nl_doc(instance: StructuredNLDoc) -> str:
    """Entrypoint: Renders a Pydantic Model to Structured Markdown."""
    fields, template = split_doc_components(instance)
    
    def replacer(match):
        content = match.group(1)
        if "|" in content:
            # We must be careful: logic can contain pipes (e.g. {{ x | length }})
            # Reversible markers are: rev|prop or rev|table|prop
            if content.startswith(("rev|", "revop|")):
                parts = content.split("|")
                mode = parts[0]
                if parts[1] == "table":
                    return render_table_records(getattr(instance, parts[2]))
                if parts[1] == "dict":
                    return render_dict_records(fields.get(parts[2], {}))
                return str(fields.get(parts[1], ""))
            
            # For Traits, we split only on the first pipe
            trait, logic = content.split("|", 1)
            trait = trait.strip().lower()
            if trait == "jinja2": return JinjaTemplate(logic).render(**fields)
            if trait == "python":
                safe = {"sum": sum, "len": len, "max": max, "min": min, "str": str, "int": int}
                return str(eval(logic, {"__builtins__": safe}, fields))
        return str(fields.get(content, f"⸢{content}⸥"))

    return re.sub(r"⸢([^⸥]+)⸥", replacer, template)

def extract_nl_doc(cls: Type[M], raw_markdown: str) -> M:
    """Entrypoint: Extracts Structured Markdown back into a Pydantic Model."""
    config = compile_template_ast(cls.__template__)
    ast_root = SyntaxTreeNode(MarkdownIt("gfm-like").enable("table").parse(raw_markdown))
    data = {}

    def find_near(root, path, target_type):
        # 1. Try to find parent node
        node = root
        for step in path[:-1]:
            try:
                matches = [c for c in node.children if (f"{c.type}_{c.tag}" if getattr(c, 'tag', None) else c.type) == step["sig"]]
                node = matches[step["idx"]]
            except:
                break
        
        # 2. Look for target in siblings of parent
        # If node is the parent, search its children
        for child in node.children:
            if child.type == target_type: return child
        
        # 3. Last resort: global search (for simple documents)
        def global_find(n):
            if n.type == target_type: return n
            for c in n.children:
                res = global_find(c)
                if res: return res
            return None
        return global_find(root)

    for entry in config:
        if entry["trait"] == "table":
            node = find_near(ast_root, entry["path"], "table")
            if node:
                records = parse_table_node(node)
                field = cls.model_fields.get(entry["prop"])
                if field and get_origin(field.annotation) is dict:
                    data[entry["prop"]] = {r.pop("key"): r for r in records if "key" in r}
                else:
                    data[entry["prop"]] = records
            continue
        
        if entry["trait"] == "dict":
            node = find_near(ast_root, entry["path"], "bullet_list")
            if node: data[entry["prop"]] = parse_dict_node(node)
            continue

        node = ast_root
        try:
            for step in entry["path"]:
                matches = [c for c in node.children if (f"{c.type}_{c.tag}" if getattr(c, 'tag', None) else c.type) == step["sig"]]
                node = matches[step["idx"]]
        except: continue
        
        node_text = node.content or ""
        markers = re.findall(r"⸢([^⸥]+)⸥", entry["pattern"])
        placeholder = re.sub(r"⸢[^⸥]+⸥", "__PROP__", entry["pattern"])
        regex = re.escape(placeholder)
        def gen(m):
            marker = markers.pop(0)
            if "|" in marker:
                p = marker.split("|")
                if p[0] in ("rev", "revop"): return f"(?P<{p[-1]}>.*?)"
            return ".*?"
        regex = re.sub("__PROP__", gen, regex)
        match = re.search(f"^{regex}$", node_text, re.DOTALL)
        if match: data.update(match.groupdict())

    return cls.model_validate(data)
