from repopackage.nldb_engine.models import StructuredNLDoc

class BasicParagraphModel(StructuredNLDoc):
    __template__ = """# ⸢rev•heading1⸥

This is an ⸢rev•paragraph1⸥.

> ⸢rev•quote1⸥

```python
⸢rev•code1⸥
```

⸢rev•setext_heading⸥
===================

    ⸢rev•indented_code⸥

<div class="test">⸢rev•html_block⸥</div>

* Item A: ⸢rev•list_item1⸥
* Item B: ⸢rev•list_item2⸥

1. Ordered: ⸢rev•olist_item1⸥

| Col 1 | Col 2 |
| ----- | ----- |
| ⸢rev•tc1⸥ | ⸢rev•tc2⸥ |
"""
    heading1: str
    paragraph1: str
    quote1: str
    code1: str
    setext_heading: str
    indented_code: str
    html_block: str
    list_item1: str
    list_item2: str
    olist_item1: str
    tc1: str
    tc2: str