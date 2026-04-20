import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(__file__))

# Make sure our new redesign components import
from repopackage.nldb_engine.ast_handler import AST_Handler
from repopackage.nldb_engine.template_extractor import TemplateExtractor
from repopackage.nldb_engine.data_extractor import DataExtractor
from test_model import BasicParagraphModel

def test_ast_handler_redesign():
    # --- PHASE 1: TEMPLATE RECIPE COMPILATION ---
    ast_handler = AST_Handler()
    tpl_extractor = TemplateExtractor()
    data_extractor = DataExtractor()

    # Split root AST heavily into specific node blocks using live model
    tpl_blocks = ast_handler.split_nodes(BasicParagraphModel.__template__)
    recipes = tpl_extractor.extract_nodes(tpl_blocks)

    # --- PHASE 2: EVALUATING EXTRACTOR AGAINST PAYLOAD DATA ---
    filepath = os.path.join(os.path.dirname(__file__), "test_markdown.md")
    with open(filepath, "r") as f:
        markdown_data = f.read().strip()

    data_blocks = ast_handler.split_nodes(markdown_data)
    payload = data_extractor.extract_values(data_blocks, recipes)

    print("\n=== Extracted Final Dictionary ===")
    print(payload)

    assert payload["heading1"] == "My Expected Heading"
    assert payload["paragraph1"] == "expected paragraph"
    assert payload["quote1"] == "My expected quote block"
    assert payload["code1"] == 'print("Hello Expected Code")'
    assert payload["setext_heading"] == "My Setext Heading"
    
    # These should work now with the stripping fix
    assert payload["indented_code"] == "my indented code"
    assert payload["html_block"] == "my html payload"

    # Grouped fields: item_id and item_name are in the same list item template
    assert isinstance(payload["item_id"], list)
    assert len(payload["item_id"]) == 3
    assert payload["item_id"][0] == {"item_id": "1", "item_name": "Alpha"}

    assert payload["olist_item1"] == ["First", "Second"]

    # Table grouped fields
    assert isinstance(payload["tc1"], dict)
    assert payload["tc1"][0] == {"tc1": "Val1", "tc2": "Val2"}

if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
