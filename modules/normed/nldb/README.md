# nlDB (Natural Language Database Engine)

A structurally aware Markdown extraction and template mapping library based on `mdast` principles. nlDB allows you to treat Markdown files as a structured persistence layer, mapping them directly to Pydantic models.

## Features

- **Structural Synchronicity:** Bi-directional mapping between Markdown and Pydantic.
- **AST-Powered:** Uses `markdown-it-py` for robust structural analysis instead of fragile regex.
- **Stateful Sequential Extraction:** Robustly handles multiple identical blocks via cursor mapping.
- **Rich GFM Support:** Native handlers for Lists, Tables, YAML Metadata, and standard text blocks.
- **Marker-Based Templates:** Define extraction logic directly in Pydantic models using `__template__`.

## Installation

```bash
pip install nldb
```

## Basic Usage

```python
from nldb import StructuredNLDoc, DataExtractor, AST_Handler, TemplateExtractor

class MyModel(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n⸢rev•content⸥"
    title: str
    content: str

# Parsing
ast = AST_Handler()
tpl = TemplateExtractor()
data = DataExtractor()

recipes = tpl.extract_nodes(ast.split_nodes(MyModel.__template__))
payload = data.extract_values(ast.split_nodes("# Hello\n\nWorld"), recipes)

model = MyModel(**payload)
print(model.title) # "Hello"
```

## License

MIT
