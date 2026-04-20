from typing import List, Dict, Any, Optional
from pydantic import Field
from nldb.structuredNLDoc import StructuredNLDoc

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

* Item ⸢rev,list•item_id⸥: ⸢rev,list•item_name⸥

1. Ordered: ⸢rev,list•olist_item1⸥

| Col 1 | Col 2 |
| ----- | ----- |
| ⸢rev,table•tc1⸥ | ⸢rev,table•tc2⸥ |
"""
    heading1: str
    paragraph1: str
    quote1: str
    code1: str
    setext_heading: str
    indented_code: Optional[str] = None
    html_block: Optional[str] = None
    
    # Grouped fields: 
    # item_id and item_name are in the same list, 
    # so they are returned as a list of dicts under the first key
    item_id: List[Dict[str, str]] = Field(default_factory=list)
    
    olist_item1: List[str] = Field(default_factory=list)
    
    # tc1 and tc2 are in the same table, 
    # so they are returned as a dict of dicts under the first key
    tc1: Dict[int, Dict[str, str]] = Field(default_factory=dict)
