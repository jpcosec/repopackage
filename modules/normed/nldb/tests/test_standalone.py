import pytest
from nldb import StructuredNLDoc, DataExtractor, AST_Handler, TemplateExtractor, NLDBRenderer

class SimpleDoc(StructuredNLDoc):
    __template__ = """
# ⸢rev•title⸥

## Metadata
```yaml
⸢rev,dict•meta⸥
```

* ⸢rev,list•items⸥
""".strip()
    title: str
    meta: dict
    items: list

def test_nldb_standalone_roundtrip():
    ast = AST_Handler()
    tpl = TemplateExtractor()
    data_ext = DataExtractor()
    renderer = NLDBRenderer()

    # 1. Parsing
    markdown = """
# My Standalone Doc

## Metadata
```yaml
version: 1.0.0
status: stable
```

* First
* Second
""".strip()

    recipes = tpl.extract_nodes(ast.split_nodes(SimpleDoc.__template__))
    payload = data_ext.extract_values(ast.split_nodes(markdown), recipes)
    
    model = SimpleDoc(**payload)
    assert model.title == "My Standalone Doc"
    assert model.meta == {"version": "1.0.0", "status": "stable"}
    assert model.items == ["First", "Second"]

    # 2. Rendering
    rendered = renderer.render(model)
    assert "# My Standalone Doc" in rendered
    assert "version: 1.0.0" in rendered
    assert "* First" in rendered
    assert "* Second" in rendered

if __name__ == "__main__":
    pytest.main([__file__])
