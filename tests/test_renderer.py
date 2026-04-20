import os
import sys
import pytest
from repopackage.nldb_engine.renderer import NLDBRenderer
from test_model import BasicParagraphModel

def test_renderer_basic():
    renderer = NLDBRenderer()
    
    data = {
        "heading1": "My Heading",
        "paragraph1": "my paragraph",
        "quote1": "my quote",
        "code1": "print('hello')",
        "setext_heading": "My Setext",
        "indented_code": "my indented",
        "html_block": "my html",
        "item_id": [
            {"item_id": "1", "item_name": "Alpha"},
            {"item_id": "2", "item_name": "Beta"}
        ],
        "olist_item1": ["First", "Second"],
        "tc1": {
            0: {"tc1": "V1", "tc2": "V2"},
            1: {"tc1": "V3", "tc2": "V4"}
        }
    }
    
    model = BasicParagraphModel(**data)
    rendered = renderer.render(model)
    
    print("\n=== Rendered Output ===")
    print(rendered)
    
    assert "# My Heading" in rendered
    assert "This is an my paragraph." in rendered
    assert "> my quote" in rendered
    assert "```python\nprint('hello')\n```" in rendered
    assert "* Item 1: Alpha" in rendered
    assert "* Item 2: Beta" in rendered
    assert "1. Ordered: First" in rendered
    assert "1. Ordered: Second" in rendered
    assert "| V1 | V2 |" in rendered
    assert "| V3 | V4 |" in rendered

if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])
