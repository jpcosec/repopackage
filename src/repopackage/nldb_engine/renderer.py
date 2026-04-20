import re
from typing import Any, Dict, List
from nldb.structuredNLDoc import StructuredNLDoc
from nldb.ast_handler import AST_Handler
from nldb.node_handler import SharedNodeHandler

class NLDBRenderer:
    """
    Renders a Pydantic model (StructuredNLDoc) back into Markdown 
    using its __template__ and mapping data into markers.
    """
    def __init__(self):
        self.ast_handler = AST_Handler()
        self.node_handler = SharedNodeHandler()

    def render(self, model: StructuredNLDoc) -> str:
        template = model.__template__
        data = model.model_dump(mode='json')
        blocks = self.ast_handler.split_nodes(template)
        template_lines = template.splitlines()
        
        output_parts = []
        
        # We process each top-level block.
        # If it's a list or table, we expand it.
        # Otherwise, we just replace markers in its lines.
        
        for block in blocks:
            start_line, end_line = block.map
            block_lines = template_lines[start_line:end_line]
            block_text = "\n".join(block_lines)
            
            handler_key = self.node_handler.get_handler_for_node(block)
            
            if handler_key == "list":
                rendered = self._render_list_block(block, block_text, data)
                output_parts.append(rendered)
            elif handler_key == "table":
                rendered = self._render_table_block(block, block_text, data)
                output_parts.append(rendered)
            elif handler_key == "yaml":
                rendered = self._render_yaml_block(block, block_text, data)
                output_parts.append(rendered)
            else:
                rendered = self._replace_markers(block_text, data)
                output_parts.append(rendered)
                
        return "\n\n".join(output_parts).strip()

    def _render_yaml_block(self, node, block_text: str, data: Dict[str, Any]) -> str:
        # If it's front_matter, we might need to add ---
        is_front_matter = node.type == "front_matter"
        content = self._replace_markers(block_text, data)
        if is_front_matter:
            return f"---\n{content}\n---"
        return content

    def _replace_markers(self, text: str, data: Dict[str, Any]) -> str:
        def sub_marker(match):
            inner = match.group(1)
            traits = inner.split(",") if "," in inner.split("•")[0] else []
            prop = inner.split("•", 1)[-1].strip() if "•" in inner else inner.strip()
            val = data.get(prop)
            if val is None:
                return match.group(0) # Keep marker if no data
                
            if "dict" in [t.strip() for t in traits] or isinstance(val, (dict, list)):
                import yaml
                # Avoid adding --- at start of snippet
                return yaml.dump(val, allow_unicode=True, sort_keys=False).strip()
                
            return str(val)
            
        return re.sub(r"⸢([^⸥]+)⸥", sub_marker, text)

    def _render_list_block(self, node, block_text: str, data: Dict[str, Any]) -> str:
        # A list block in template typically has ONE item as a template.
        # We need to extract that item's text (including the bullet/number).
        # And repeat it for each item in the data.
        
        if not node.children:
            return self._replace_markers(block_text, data)
            
        # Get the first item as template
        first_item = node.children[0]
        item_start, item_end = first_item.map
        # Map is relative to the whole template, not block_text
        # But we can just use the template_lines if we want.
        # Actually, let's use the node structure.
        
        # Identify the root property from the first marker in the first item
        item_text = self._get_node_source(first_item, block_text, node.map[0])
        
        match = re.search(r"⸢([^⸥]+)⸥", item_text)
        if not match:
            return self._replace_markers(block_text, data)
            
        inner = match.group(1)
        root_prop = inner.split("•", 1)[-1].strip() if "•" in inner else inner.strip()
        
        list_items_data = data.get(root_prop, [])
        if not isinstance(list_items_data, list):
            return "" # Or maybe just empty?
            
        rendered_items = []
        for item_data in list_items_data:
            # If item_data is a dict, we use it to replace markers in item_text
            # If it's a simple value, we treat it as the value for root_prop
            if isinstance(item_data, dict):
                rendered_items.append(self._replace_markers(item_text, item_data))
            else:
                rendered_items.append(self._replace_markers(item_text, {root_prop: item_data}))
                
        return "\n".join(rendered_items)

    def _render_table_block(self, node, block_text: str, data: Dict[str, Any]) -> str:
        # Tables are: Header, Separator, Body Rows.
        # We keep Header and Separator, and replace Body Rows with data.
        
        lines = block_text.splitlines()
        if len(lines) < 3:
            return self._replace_markers(block_text, data)
            
        header = lines[0]
        separator = lines[1]
        row_template = lines[2] # Assume 3rd line is the row template
        
        # Identify root property from first marker in row_template
        match = re.search(r"⸢([^⸥]+)⸥", row_template)
        if not match:
            return self._replace_markers(block_text, data)
            
        inner = match.group(1)
        root_prop = inner.split("•", 1)[-1].strip() if "•" in inner else inner.strip()
        
        rows_data = data.get(root_prop, {})
        # Handle dict or list of items
        items_to_render = []
        if isinstance(rows_data, dict):
            sorted_keys = sorted(rows_data.keys(), key=lambda x: int(x) if str(x).isdigit() else x)
            items_to_render = [rows_data[k] for k in sorted_keys]
        elif isinstance(rows_data, list):
            items_to_render = rows_data
            
        rendered_rows = []
        for item in items_to_render:
            item_data = item.model_dump() if hasattr(item, "model_dump") else item
            rendered_rows.append(self._replace_markers(row_template, item_data))
            
        if rendered_rows:
            return "\n".join([header, separator] + rendered_rows)
        
        return self._replace_markers(block_text, data)

    def _get_node_source(self, node, block_text: str, block_start_line: int) -> str:
        lines = block_text.splitlines()
        start = node.map[0] - block_start_line
        end = node.map[1] - block_start_line
        return "\n".join(lines[start:end])
