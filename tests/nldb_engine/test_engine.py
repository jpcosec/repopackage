import pytest
from typing import List, Dict, Any
from pydantic import BaseModel
from repopackage.nldb_engine.engine import (
    StructuredNLDoc, render_nl_doc, extract_nl_doc
)

# --- NESTED MODELS TEST ---

class Item(BaseModel):
    id: str
    name: str
    status: bool

class NestedDoc(StructuredNLDoc):
    __template__: str = """
# Project: ⸢rev|title⸥

## Items
⸢rev|table|items⸥

## Summary
⸢jinja2|Total items: {{ items | length }}⸥
""".strip()
    title: str
    items: List[Item]

def test_nested_pydantic_list_roundtrip():
    doc = NestedDoc(
        title="Alpha",
        items=[
            Item(id="1", name="One", status=True),
            Item(id="2", name="Two", status=False)
        ]
    )
    
    # Render
    md = render_nl_doc(doc)
    assert "# Project: Alpha" in md
    assert "| One | True |" in md
    assert "Total items: 2" in md
    
    # Extract
    extracted = extract_nl_doc(NestedDoc, md)
    assert extracted.title == "Alpha"
    assert len(extracted.items) == 2
    assert isinstance(extracted.items[0], Item)
    assert extracted.items[0].name == "One"
    assert extracted.items[1].status is False

# --- STANDARD TESTS ---

class SimpleDoc(StructuredNLDoc):
    __template__: str = "# ⸢rev|name⸥\nAge: ⸢rev|age⸥"
    name: str
    age: int

def test_simple_roundtrip():
    doc = SimpleDoc(name="Rex", age=5)
    md = render_nl_doc(doc)
    extracted = extract_nl_doc(SimpleDoc, md)
    assert extracted == doc

class DictDoc(StructuredNLDoc):
    __template__: str = "## Meta\n⸢rev|dict|data⸥"
    data: Dict[str, str]

def test_dict_roundtrip():
    doc = DictDoc(data={"Key1": "Val1", "Key2": "Val2"})
    md = render_nl_doc(doc)
    extracted = extract_nl_doc(DictDoc, md)
    assert extracted.data == doc.data

def test_logic_traits():
    class Logic(StructuredNLDoc):
        __template__: str = "Score: ⸢python|sum(vals)⸥\n⸢rev|vals⸥"
        vals: List[int]
    
    doc = Logic(vals=[1, 2, 3])
    md = render_nl_doc(doc)
    assert "Score: 6" in md
    # Extraction should skip logic and pull vals (though list extraction is simple regex here)
    # Note: Complex list extraction without tables is a deferred item.
